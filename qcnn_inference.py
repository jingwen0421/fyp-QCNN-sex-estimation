"""Inference for the fixed-average QCNN saved by notebook 04."""

import json

import joblib
import numpy as np
import pandas as pd
import pennylane as qml


def convolution_layer(parameters):
    for first in (0, 2, 4, 6, 1, 3, 5):
        second = first + 1
        qml.Rot(*parameters[:3], wires=first)
        qml.Rot(*parameters[3:], wires=second)
        qml.CNOT(wires=[first, second])


@qml.qnode(qml.device("default.qubit", wires=8), interface=None)
def qcnn_circuit(angles, weights):
    for wire in range(8):
        qml.RY(angles[..., wire], wires=wire)
    convolution_layer(weights[:6])
    convolution_layer(weights[6:12])
    for source in (0, 2, 4, 6):
        qml.CRY(weights[12], wires=[source, source + 1])
    return [qml.expval(qml.PauliZ(wire)) for wire in (1, 3, 5, 7)]


def load_qcnn(folder):
    details = json.loads((folder / "run_details.json").read_text(encoding="utf-8"))
    weights = np.load(folder / "qcnn_weights.npy", allow_pickle=False)
    scaler = joblib.load(folder / "scaler.joblib")
    if weights.shape != (13,) or details["label_mapping"] != {"F": 0, "M": 1}:
        raise ValueError("The saved files do not match the initial QCNN.")
    if list(scaler.feature_names_in_) != details["features"]:
        raise ValueError("The saved scaler and feature order do not match.")
    return details, weights, scaler


def predict_measurements(values, model):
    details, weights, scaler = model
    features = details["features"]
    measurements = np.array([values[name] for name in features], dtype=float)
    if not np.isfinite(measurements).all() or (measurements <= 0).any():
        raise ValueError("Enter a positive number for each of the eight measurements.")
    outside = (measurements < scaler.data_min_) | (measurements > scaler.data_max_)
    angles = scaler.transform(pd.DataFrame([measurements], columns=features))[0]
    score = (1 - float(np.mean(qcnn_circuit(angles, weights)))) / 2
    label = "Male" if score >= details["threshold"] else "Female"
    return label, [name for name, clipped in zip(features, outside) if clipped]
