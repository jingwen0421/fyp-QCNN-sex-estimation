# FYP2 Handoff Notes

Paste this file into a new Claude session (or read it yourself) to continue the work on the Mac.

## Project

- **Course:** WIA3003 Academic Project II (FYP2), UM FSKTM
- **Student:** Wong Jing Wen (23004924)
- **Supervisor:** Dr. Erma Rahayu Mohd Faizal
- **Collaborators:** Dr. Sharifah Nabilah Bt Syed Mohd Hamdan, Dr. Lai Poh Soon
- **Title:** A Quantum Convolutional Neural Network (QCNN) Framework for Automated Sex Estimation Using Orbital and Nasal Craniofacial Measurements
- **Repo:** https://github.com/jingwen0421/fyp-QCNN-sex-estimation (keep it **private**)

## Moving to the Mac

1. Clone the repo:
   ```bash
   git clone https://github.com/jingwen0421/fyp-QCNN-sex-estimation.git
   ```
2. Copy the dataset by hand (it is **not** in Git, and must never be committed):
   `Orbital, Nasal and Craniofacial Class Pattern.xls` → `~/Downloads/`
   The notebooks read it from `Path.home() / "Downloads"`, so the same path works on the Mac. Notebooks 14–16 check its SHA-256 hash, so copy the exact same file.
3. Create a Python environment and install packages:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install pennylane scikit-learn xgboost tensorflow pandas numpy matplotlib xlrd openpyxl joblib streamlit altair jupyter nbformat nbclient
   ```
   (The Windows PC used Python 3.14 + TensorFlow 2.22 rc. On the Mac, Python 3.11 or 3.12 is safer for TensorFlow.)
4. Run the app: `streamlit run app.py` (the Windows shortcut `Start CranioLab.cmd` does not work on macOS).
5. Use `.ipynb` notebooks in `notebooks/`, numbered 01–16.

**Not in Git (copy by hand if needed):** the dataset, and the slide-builder scripts that only existed in a Windows temp folder. The finished decks are in `monitoring/`, and the live version is in Canva.

## Data

- 1,042 Malaysian cases: 587 Male, 455 Female; Malay, Chinese and Indian
- 8 features: 6 orbital (Ec-Dc, REc-RDc, LEc-LDc, UMo-Lmo, RUMo-RLMo, LUMo-LLMo) + 2 nasal (RAI-LAI, Rh-Ns)
- The "Autopsy Num" column is dropped on load. Case IDs must never appear in notebooks, outputs or the repo.
- 5 groups of identical measurement records; 4 of them contain both sexes. Ask the collaborator to check them.
- **Open question:** is the data source HKL Forensic or UM Faculty of Dentistry? The slides say UM. Confirm it.

## Method

- **Splitting:** StratifiedGroupKFold, 5 folds. Groups = identical-measurement records (prevents leakage). Strata = sex × ethnicity. Settings are tuned on an inner validation split only; each test fold is used once.
- **Why CV:** a single 80:20 split was unstable and about 4 points optimistic (notebook 12).
- **Metrics:** accuracy, macro F1, per-class recall, ROC AUC.

### QCNN (PennyLane, 8 qubits)

- RY angle embedding → 2 shared convolution layers (Rot, Rot, CNOT on neighbouring pairs) → CRY pooling onto wires 1, 3, 5, 7 → PauliZ readout.
- **Initial QCNN:** 13 parameters (6 + 6 + 1), min-max scaling to [0, π], fixed average readout. 13 epochs selected out of 30.
- **Improved QCNN:** 34 parameters. Standardized inputs, trainable encoding RY(w·x + b) (8 weights + 8 offsets), learned sigmoid readout (4 weights + 1 bias), Adam with lr 0.01, batch 32, BCE loss, up to 100 epochs with early stopping (patience 10).
- Shared training code: `qcnn_training.py` (`REFERENCE`, `build_model`, `make_scaler`, `train`).

### Baselines

Logistic regression (9 parameters), MLP (64, 32), XGBoost (100 trees, depth 3), 1D-CNN.

## Results

| Model | Accuracy | Evaluation |
|---|---|---|
| Logistic regression | 77.0% ± 3.2 (macro F1 76.5%) | 5-fold CV |
| **Improved QCNN** | **76.6% ± 2.5** (macro F1 76.2%, female recall 73.0%) | 5-fold CV |
| Initial QCNN | 68.9% ± 3.7 (female recall 56.7%) | 5-fold CV |
| CNN | 80.0% | single split only |
| XGBoost | 79.0% | single split only |
| MLP | 71.4% | single split only |

**Main message:** about 77% is the limit of these 8 features. The improved QCNN is **competitive with** logistic regression, not better.

### Experiments (all on validation data)

- **Readout:** learned 0.72 vs fixed average 0.68 macro F1 (notebooks 05, 08).
- **Split ratio:** about 0.76 from 60:40 to 90:10; smaller test sets are only noisier (notebook 12).
- **Ablation:** learning rate, batch size and layers change macro F1 by about 0.01, the same as changing the random seed, so the reference settings are kept (notebook 16, 65 runs).
- **Features:** nasal only 0.72, all eight 0.72, orbital only 0.62 (notebook 10). XGBoost importance: nasal height 0.38.
- **Ethnicity** (notebooks 11, 13, 14): ethnicity as an input changes the score by less than 0.1 point. Leaving each group out of training: only Indian drops (about 3 points). CV accuracy for the initial QCNN / logistic regression: Chinese 70.0 / 76.8, Indian 72.7 / 79.4, Malay 65.0 / 75.3.
- **60 vs 30 epochs:** no gain (`results/qcnn_sigmoid_60_epochs`).

## Notebooks

01 EDA + MLP · 02 XGBoost · 03 CNN · 04 initial QCNN · 05 readout · 06 learning rate · 07 logistic regression · 08 sigmoid readout · 09 epoch limit (**never run**) · 10 feature ablation · 11 ethnicity subgroups · 12 split ratio · 13 ethnicity effect · 14 ethnicity CV · 15 improved QCNN · 16 QCNN ablation

## App (CranioLab, Streamlit)

- `app.py` + `qcnn_inference.py`. Four pages: Overview, Dataset upload, Sex estimation (manual or upload, optional ethnicity), Evaluation (includes accuracy by ethnicity).
- Error handling: missing values and out-of-range warnings.
- **Still predicts with the initial QCNN** (`results/qcnn_baseline`).

## Monitoring slides (Week 7)

- Latest deck in Canva (imported from `monitoring/FYP II Monitoring - Overview style v2.pptx`, 25 slides).
- Remaining fixes from the last review:
  - Slide 17: rename the chart labels 1.0 / 2.0 / 3.0 → Chinese / Indian / Malay.
  - Slide 6: stack two code screenshots at the same width; drop the `feature_cols` screenshot.
  - Slide 11: crop the code to lines 18–35; fix the typo "Rarly" → "Early".
  - Slide 7: include the `groups = ...ngroup()` line.
  - Slide 13: header "Parameter s" → "Params".
  - Slide 22: confirm HKL vs UM and add the collaborator evidence.
  - Slide 25: use a sharper skull image.
- Code screenshot sources: nb01 cells 9 and 14 · nb14 cell 3, lines 32–41 · nb07 cell 5 lines 1–7 and cell 7 lines 1–3 · nb15 cell 5 lines 4–18 · nb15 cell 9 lines 1–5 and 18–35.

## AP1 panel feedback and responses

- "Extend to include racial context": compared Malay, Chinese and Indian; ethnicity as input; leave-one-group-out.
- "Gender detection is not population specific": mostly supported; only the Indian group drops (about 3 points) when unseen.
- "Imbalance?": mild (56/44); stratified folds plus macro F1 and per-class recall. No class weighting.
- "Baseline / requirements from collaborator?": four classical baselines; requirements to be confirmed in UAT.

## To do

1. Run 5-fold CV for CNN, XGBoost and MLP.
2. Choose the final QCNN and put the improved QCNN into the app.
3. Test the upload path end to end and measure response time.
4. UAT with the collaborators.
5. Statistical test comparing QCNN vs logistic regression (ask the supervisor which one).
6. Run or remove notebook 09.
7. Clean up the old decks in `monitoring/`.
8. Final report, slides, video, viva (Weeks 11–14).

## AI usage declaration

Claude (and Codex earlier) wrote substantial code, notebooks and slides; several notebooks say so in their notes. Per the AP briefing, declare the **highest** level reached, which is realistically **Level 4**. Declare it accurately.

## Questions for the supervisor

- Is matching logistic regression an acceptable outcome?
- Which statistical test should compare the two models?
- Who should take part in UAT?
- Data source: HKL or UM?
