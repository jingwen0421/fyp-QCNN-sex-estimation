# FYP2 Handoff Notes

Paste this file into a new Claude session (or read it yourself) to continue the work on the Mac.

## Project

- **Course:** WIA3003 Academic Project II (FYP2), UM FSKTM
- **Student:** Wong Jing Wen (23004924)
- **Supervisor:** Dr. Erma Rahayu Mohd Faizal
- **Collaborators:** Dr. Sharifah Nabilah Bt Syed Mohd Hamdan, Dr. Lai Poh Soon
- **Title:** A Quantum Convolutional Neural Network (QCNN) Framework for Automated Sex Estimation Using Orbital and Nasal Craniofacial Measurements
- **Repo:** https://github.com/jingwen0421/fyp-QCNN-sex-estimation (keep it **private**)
- **Collaborators' institution:** Faculty of Dentistry, UM (collaboration letter signed). **Data source:** Hospital Kuala Lumpur (HKL), per the FYP1 scope slide. Both are true: the collaborators are at UM and the case data comes from HKL. Say it this way consistently.

## Deadlines (Semester 1 2026/2027, from the AP Briefing)

| Week | Dates | What |
|---|---|---|
| 1–6 | 5 Oct – 15 Nov 2026 | Detail design and system development |
| **7** | **16 – 22 Nov 2026** | **Monitoring session** (0%, but mandatory: Satisfactory/Unsatisfactory, assessed by the supervisor) |
| 8 | 23 – 29 Nov 2026 | Improve based on monitoring feedback |
| Break | 30 Nov – 6 Dec 2026 | Mid-semester break |
| 9–12 | 7 Dec 2026 – 3 Jan 2027 | Testing, **UAT**, finalise the report |
| **13–14** | **4 – 17 Jan 2027** | **AP2 viva (physical)** plus presentation and defence |
| After viva | **within 3 days of your viva** | **Final report submission via Ilmiah** |

Other rules:
- Log **all** supervisor meetings in the Ilmiah logbook (date, platform, summary).
- Collaborator details must be in Ilmiah (done in FYP1).
- Deliverables: slides, recorded video, report, code.
- Missing the viva, scoring below 25/50 in the viva, or not submitting the report = **automatic fail**. A re-viva is capped at B-.

## Assessment (100% continuous)

| Component | Weight | Assessor |
|---|---|---|
| Technical viva | 40% | 2 panels |
| Presentation and defence | 10% | 2 panels (or industry, iFEST) |
| Report | 40% | Supervisor |
| Soft skills | 10% | Supervisor |
| Monitoring (Week 7) | 0% | Supervisor (pass/fail) |

The AP1 viva form weighted **Technical Implementation (Mastery of Tools) the highest (20–25%)**, then Analysis and Design (10%), Requirements (5%) and Stakeholder Collaboration (5%). Expect AP2 to be similar: the panel cares most about what you built and whether you can explain it.

Projects graded A may be chosen for APAC (the Excellence Academic Project Award: a 5-minute industry pitch with prizes).

## Requirements

### Objectives (from FYP1)

1. **Data Extraction:** construct a Malaysian craniofacial morphometric dataset based on orbital and nasal anatomical landmarks.
2. **QCNN Development:** develop a QCNN-based model for sex classification using craniofacial data.
3. **Benchmarking:** evaluate the QCNN against selected classical machine-learning models.

### Problem statement (from FYP1)

- Manual measurement is slow, subjective and prone to observer bias.
- Most studies use 2D data or non-Malaysian populations.
- QCNN has rarely been used for craniofacial morphometric classification.

### Functional requirements

- **FR1:** upload and parse structured datasets (.xlsx/.csv). Implemented.
- **FR2:** process orbital and nasal features (validation and scaling). Implemented.
- **FR3:** run the QCNN prediction workflow. Partly: the app still uses the initial QCNN.
- **FR4:** show the prediction and metrics. Implemented, including results by ethnicity.

### Non-functional requirements

- **Performance:** at least 80% accuracy. **Not met**: 76.6%. The limit comes from the features (every model stops at about 77%).
- **Privacy:** 100% anonymised, no personal data stored. Met: autopsy number dropped, dataset not in Git.
- **Latency:** under 5 s per batch. **Not yet measured.**
- Usability and reliability: need UAT and an upload test.

### Week 7 monitoring slides had to cover

1. Progress on each objective
2. Progress on FR and NFR
3. Methodology as implemented
4. System development (modules, features)
5. Testing and evaluation (preliminary results)
6. Actions on the AP1 panel feedback

Each needs evidence: screenshots, outputs, results.

### Final report structure (AP2)

- Updated Chapters 1–3 from AP1 (Introduction; Literature Review; Methodology), revised to match what was actually built (e.g. 5-fold CV instead of 80:20, the improved QCNN, the ethnicity analysis)
- Chapters on system design and development, and implementation
- **Chapter 6: Results and Discussion, plus UAT and testing**
- **Chapter 7: Conclusion and Future Work**
- Updated references and appendices

## Concepts to explain in the viva (plain language)

- **Sex estimation:** predicting Male/Female from skull measurements. It halves the list of possible missing persons in forensic identification.
- **Features:** the 8 measurements, 6 orbital (eye socket) and 2 nasal (nose opening). Nasal height is the most informative (XGBoost importance 0.38).
- **Qubit:** the quantum version of a bit. A rotation angle sets its state, and measuring it gives a value between −1 and +1.
- **Angle embedding (RY):** each measurement becomes the rotation angle of one qubit. 8 measurements → 8 qubits.
- **Trainable encoding:** the model learns a scale *w* and shift *b* for each measurement before rotating: RY(w·x + b).
- **Quantum convolution:** a small block of rotations (Rot) plus an entangling gate (CNOT), applied to neighbouring qubit pairs with the **same weights** (like a CNN filter sliding over the input).
- **CNOT / entanglement:** links two qubits so the model can capture relationships between measurements.
- **Quantum pooling (CRY):** a controlled rotation passes information from qubits 0, 2, 4, 6 to 1, 3, 5, 7, halving the qubits (like max-pooling in a CNN).
- **PauliZ measurement:** reads each remaining qubit as a number between −1 and +1.
- **Readout:** the initial model averaged the 4 values. The improved model learns a weight for each and applies a sigmoid to get P(Male).
- **Parameters:** the numbers the model learns. Initial QCNN 13 (6 + 6 + 1); improved 34 (13 circuit + 16 encoding + 5 readout); logistic regression 9.
- **Simulator:** the circuit runs on PennyLane's `default.qubit` on a normal computer, not real quantum hardware. No noise.
- **Loss (binary cross-entropy):** measures how wrong the predicted probabilities are. Training makes it smaller.
- **Adam optimiser / learning rate 0.01:** the method that adjusts the weights, and its step size.
- **Batch size 32:** the weights are updated after every 32 records.
- **Epoch:** one pass through all the training data.
- **Early stopping (patience 10):** stop when the validation loss hasn't improved for 10 epochs, and keep the best weights. Prevents overfitting.
- **Overfitting:** memorising the training data, so the model does worse on new data.
- **Train / validation / test:** train = learn the weights; validation = choose settings; test = final score, used once.
- **5-fold cross-validation:** split the data into 5 parts; each part is the test set once. Every record is tested exactly once. More reliable than one 80:20 split, which was ~4 points optimistic.
- **Stratified:** every fold has the same mix of sex and ethnicity.
- **Grouped:** records with identical measurements stay in the same fold, which prevents **data leakage** (test data effectively seen during training).
- **Standardisation:** rescale each measurement to mean 0 and standard deviation 1. Fit on training data only.
- **Accuracy:** % correct. **Recall (per class):** % of actual females (or males) found. **Macro F1:** the average of the Female and Male F1 scores, so the larger Male class can't dominate. **ROC AUC:** how well the model ranks Male above Female, from 0.5 (guessing) to 1.
- **Class imbalance:** 56% Male / 44% Female, which is mild. Handled with stratified folds and macro F1. No class weighting.
- **Baseline:** a standard model to compare against: logistic regression, MLP, XGBoost, CNN.
- **Ablation:** remove or change one part at a time to see whether it matters. Result: the learning rate, batch size and layers change the score by about 0.01, the same as random-seed noise.
- **Random seed:** fixes the random starting point. Changing it moved the score by about 0.011, which is the "noise level".
- **Leave-one-group-out:** train without one ethnicity, test on it. Only Indian dropped (about 3 points).

### The five key lines

1. About 77% is the limit of these 8 features, not of the model.
2. The improved QCNN (76.6%) ≈ logistic regression (77.0%). It's competitive, not better; the 0.4-point gap is within the fold variation (±2–3).
3. Five-fold grouped CV, because a single split is unstable.
4. Grouping prevents data leakage.
5. Nasal height matters most; ethnicity has little effect.

### Likely panel questions

- *Why QCNN if it doesn't beat logistic regression?* → It shows that a 34-parameter quantum model can match classical performance on real forensic data; that is the contribution. It is a feasibility study on a simulator.
- *Why not 80%?* → Every model stops at about 77% under CV, so the features limit the accuracy.
- *Why 8 qubits?* → One per measurement.
- *Is it population specific?* → Mostly no: ethnicity as an input didn't help, and only the Indian group dropped when unseen.
- *Real quantum hardware?* → No, a noiseless simulator. Noise and finite shots are future work.
- *Did you tune on the test set?* → No. All tuning used validation data, and the test folds were used once.

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
- Data comes from HKL; the collaborators are at the UM Faculty of Dentistry (see Project above).

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
  - Slide 22: add the collaborator evidence (the collaboration letter PDF is in the FYP folder); mention the data comes from HKL.
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

