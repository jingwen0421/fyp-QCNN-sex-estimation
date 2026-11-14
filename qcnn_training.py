"""Configurable QCNN training shared by the ablation and tuning notebooks."""

import time

import numpy as np
import pennylane as qml
from pennylane import numpy as pnp
from sklearn.metrics import accuracy_score, f1_score, recall_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler

N_QUBITS = 8
SURVIVING_WIRES = (1, 3, 5, 7)

# Settings of the improved QCNN from notebook 15.
REFERENCE = {
    "scaling": "standard",        # "standard" or "minmax"
    "trainable_encoding": True,   # train w and b in RY(w*x + b)
    "readout": "sigmoid",         # "sigmoid" (learned) or "average" (fixed)
    "layers": 2,                  # shared convolution layers
    "learning_rate": 0.01,
    "batch_size": 32,
    "max_epochs": 100,
    "patience": 10,
    "seed": 42,
}


def _convolution_layer(parameters):
    for first in (0, 2, 4, 6, 1, 3, 5):
        qml.Rot(*parameters[:3], wires=first)
        qml.Rot(*parameters[3:], wires=first + 1)
        qml.CNOT(wires=[first, first + 1])


def build_model(config):
    """Return (predict_probability, initial_parameters) for one configuration."""
    layers = config["layers"]
    n_circuit = 6 * layers + 1
    trainable = config["trainable_encoding"]
    learned_readout = config["readout"] == "sigmoid"
    # Min-max inputs are already angles. Standardised inputs are centred on pi/2.
    start_weight, start_offset = (1.0, 0.0) if config["scaling"] == "minmax" else (np.pi / 6, np.pi / 2)

    @qml.qnode(qml.device("default.qubit", wires=N_QUBITS), interface="autograd", diff_method="backprop")
    def circuit(angles, weights):
        for wire in range(N_QUBITS):
            qml.RY(angles[..., wire], wires=wire)
        for layer in range(layers):
            _convolution_layer(weights[6 * layer:6 * layer + 6])
        for source in (0, 2, 4, 6):
            qml.CRY(weights[6 * layers], wires=[source, source + 1])
        return [qml.expval(qml.PauliZ(wire)) for wire in SURVIVING_WIRES]

    def predict_probability(parameters, inputs):
        position = n_circuit
        if trainable:
            angles = inputs * parameters[position:position + N_QUBITS] + parameters[position + N_QUBITS:position + 2 * N_QUBITS]
            position += 2 * N_QUBITS
        else:
            angles = inputs * start_weight + start_offset
        expectations = pnp.stack(circuit(angles, parameters[:n_circuit]))
        if not learned_readout:
            return (1 - pnp.mean(expectations, axis=0)) / 2
        score = pnp.tensordot(parameters[position:position + 4], expectations, axes=1) + parameters[position + 4]
        return 1 / (1 + pnp.exp(-score))

    rng = np.random.default_rng(config["seed"])
    parts = [rng.uniform(-0.1, 0.1, n_circuit)]
    if trainable:
        parts += [np.full(N_QUBITS, start_weight), np.full(N_QUBITS, start_offset)]
    if learned_readout:
        parts += [np.full(4, -0.5), [0.0]]
    return predict_probability, pnp.array(np.concatenate(parts), requires_grad=True)


def make_scaler(config):
    if config["scaling"] == "minmax":
        return MinMaxScaler(feature_range=(0, np.pi), clip=True)
    return StandardScaler()


def train(config, fit_inputs, fit_labels, val_inputs, val_labels):
    """Train on the fitting records. Keep the weights with the lowest validation loss."""
    started = time.perf_counter()
    scaler = make_scaler(config).fit(fit_inputs)
    fit_x = pnp.array(scaler.transform(fit_inputs), requires_grad=False)
    val_x = pnp.array(scaler.transform(val_inputs), requires_grad=False)
    fit_y = pnp.array(fit_labels, requires_grad=False)
    val_y = pnp.array(val_labels, requires_grad=False)
    predict_probability, weights = build_model(config)

    def loss(parameters, inputs, labels):
        probabilities = pnp.clip(predict_probability(parameters, inputs), 1e-7, 1 - 1e-7)
        return -pnp.mean(labels * pnp.log(probabilities) + (1 - labels) * pnp.log(1 - probabilities))

    optimiser = qml.AdamOptimizer(stepsize=config["learning_rate"])
    rng = np.random.default_rng(config["seed"])
    best_loss, best_weights, best_epoch, waiting, history = np.inf, None, 0, 0, []
    for epoch in range(1, config["max_epochs"] + 1):
        order = rng.permutation(len(fit_x))
        for start in range(0, len(order), config["batch_size"]):
            batch = order[start:start + config["batch_size"]]
            weights = optimiser.step(lambda current: loss(current, fit_x[batch], fit_y[batch]), weights)
        val_loss = float(loss(weights, val_x, val_y))
        if not np.isfinite(val_loss):
            raise FloatingPointError("Validation loss is not finite.")
        history.append(val_loss)
        if val_loss < best_loss:
            best_loss, best_weights, best_epoch, waiting = val_loss, np.asarray(weights).copy(), epoch, 0
        else:
            waiting += 1
        if waiting >= config["patience"]:
            break

    frozen = pnp.array(best_weights, requires_grad=False)
    predicted = (np.asarray(predict_probability(frozen, val_x), dtype=float) >= 0.5).astype(int)
    return {
        "Parameters": len(best_weights), "Best epoch": best_epoch, "Epochs run": len(history),
        "Validation loss": best_loss,
        "Validation macro F1": f1_score(val_labels, predicted, average="macro"),
        "Validation accuracy": accuracy_score(val_labels, predicted),
        "Female recall": recall_score(val_labels, predicted, pos_label=0),
        "Male recall": recall_score(val_labels, predicted, pos_label=1),
        "Seconds": time.perf_counter() - started,
    }, best_weights, scaler, history
