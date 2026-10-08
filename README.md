# Faces in the Office (FIO) Dataset Code

This repository contains the supporting materials accompanying the **Faces in the Office (FIO)** dataset. It includes the data acquisition and preprocessing pipeline, the face recognition evaluation code, the gallery/query split used for validation, aggregate evaluation results, and environment/dependency information needed to reproduce the technical validation.

The face images themselves are **not** included in this repository. Due to the biometric and sensitive nature of the data, the FIO dataset is hosted separately on Zenodo under restricted access.

## Repository Contents

| File | Description |
|---|---|
| `extractor.py` | Connects to the camera's HikVision ISAPI event-notification stream, extracts JPEG snapshots during working hours, and applies RetinaFace-based face detection and cropping. |
| `clean_public.ipynb` | Dataset cleaning and organization pipeline: alternating-frame downsampling, exact and near-duplicate detection (MD5 / perceptual hashing), directory consistency checks, and identity anonymization (`Person_N` renaming). |
| `database.ipynb` | Builds the gallery embedding database using the SFace model (via InsightFace `model_zoo`). |
| `main.ipynb` | Runs the identification evaluation: computes query embeddings, matches against the gallery via cosine similarity, applies an acceptance threshold fixed a priori at t = 0.42 (close to the default SFace operating points of OpenCV and DeepFace; not tuned on the evaluation data), and computes Accuracy, Precision, Recall, F1-score, CMC@1, CMC@3, mAP, latency, throughput, and memory usage. |
| `split_gallery_query.py` | Splits an identity-organized face crop directory into gallery (55%) and query (45%) sets per identity, with a fixed random seed for reproducibility. Produces `gallery_query_split.csv`. |
| `recognition_results.csv` | Per-query results for all 1,052 query images: filename, true identity, top-1 gallery identity and cosine similarity, rank of the true identity, and predicted identity at the fixed threshold (t = 0.42) and at the supplementary leave-one-out threshold. |
| `environment-gpu.yml` | Conda environment specification (Python 3.9, TensorFlow 2.13, DeepFace 0.0.95, retina-face 0.0.17, ONNX Runtime GPU 1.19.2) used to run the pipeline. |
| `per_identity_counts.csv` | Per-identity summary (Table 2 of the article): anonymized identity ID, gender, age range, and the number of gallery, query and total images. |
| `gallery_query_split.csv` | Gallery/query assignment of all 2,340 images (seed = 42, 55/45 per identity), produced by `split_gallery_query.py`. |

## Dataset Access

The FIO dataset is available on Zenodo: https://doi.org/10.5281/zenodo.21863771

The dataset metadata is openly registered, but the face images are **not openly accessible**. Access is granted only upon request for bona fide research purposes, subject to a signed Data Use Agreement (DUA) and approval by the authors. See the article's Data Availability section for full details on the request process, permitted uses, and retention terms.

## Reproducing the Pipeline

1. **Set up the environment**
   ```bash
   conda env create -f environment-gpu.yml
   conda activate facegpu2
   ```

2. **Set camera credentials as environment variables** (if re-running acquisition; not needed for evaluation only)
   ```bash
   export CAMERA_HOST="http://<camera-ip>"
   export USERNAME="<camera-username>"
   export PASSWORD="<camera-password>"
   ```

3. **Run preprocessing** — see `clean_public.ipynb` for the full cleaning and organization pipeline.

4. **Split gallery/query** (requires the dataset, obtained separately via DUA)
   ```bash
   python split_gallery_query.py
   ```

5. **Build the gallery database and run evaluation**
   Run `database.ipynb` followed by `main.ipynb`.

## Contact

For questions about the dataset or Data Use Agreement, contact N.Amilbek@astanait.edu.kz.
