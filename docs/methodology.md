# Methodology

## Model Choice
MobileNetV2 is selected for:
- Low compute footprint
- Fast inference on CPU
- Good transfer learning performance on small datasets

## Training Strategy
- Transfer learning with frozen backbone for MVP stability
- Softmax classifier head for 4 classes
- Early stopping to prevent overfitting

## Evaluation
Primary Metric: Accuracy  
Secondary: Confusion between overripe vs rotten (visually similar)


3. Methodology
3.1 System Overview

This work proposes CVLab, a modular computer vision experimentation and deployment framework, demonstrated through a fruit ripeness classification system for bananas. The framework is designed to support collaborative development, reproducible experiments, dataset auditing, model registry management, and real-time inference via a web interface.

The overall pipeline consists of dataset ingestion, dataset intelligence analysis, model training with controlled experimentation, model registry management, and production deployment through a web-based inference application.

3.2 Dataset Description

The dataset used in this study is a publicly available Banana Ripeness Classification Dataset, consisting of images categorized into four classes: unripe, ripe, overripe, and rotten. The dataset is divided into training, validation, and testing splits.

A total of 13,478 images were used. The class-wise distribution is summarized as follows:

Unripe: 2,179 images

Ripe: 4,015 images

Overripe: 2,691 images

Rotten: 4,593 images

3.3 Dataset Intelligence and Bias Analysis

Prior to model training, an automated dataset intelligence module was employed to analyze class distribution and detect imbalance. The imbalance ratio, defined as the ratio between the maximum and minimum class frequencies, was computed as 2.11:1, indicating moderate class imbalance.

The framework automatically flags imbalance conditions and low-sample classes to ensure transparency and to guide future dataset refinement. All dataset audits generate persistent reports and visualizations, ensuring reproducibility and traceability of dataset quality assessments.

3.4 Model Architecture

A transfer learning approach was adopted using MobileNetV2 as the backbone architecture due to its computational efficiency and suitability for low-resource environments. The pretrained ImageNet weights were utilized, and the backbone layers were frozen during initial training.

The classification head consists of:

Global Average Pooling layer

Dropout layer (rate = 0.2)

Fully connected softmax output layer with four neurons

This architecture balances performance and computational efficiency.

3.5 Training Strategy and Experimentation

Model training was conducted under two controlled modes:

Development Mode (Dev): Reduced epochs and optional dataset sampling for rapid validation and debugging.

Full Training Mode: Extended training for performance optimization.

All experiments are assigned unique experiment identifiers containing timestamps, contributor identity, and mode information. Training metrics, loss curves, accuracy plots, and model artifacts are automatically stored per experiment.

3.6 Model Registry and Selection

A JSON-based model registry is maintained to track all trained models, associated experiments, accuracy scores, and contributors. The registry supports automatic best-model detection as well as manual production model selection.

Only explicitly approved models are promoted to production, ensuring strict separation between experimental and deployed models.

3.7 Deployment and Inference

The production model is deployed through a web-based inference application built using Streamlit. The application automatically loads the current production model from the registry and supports both image uploads and webcam-based predictions.

Prediction outputs include class labels, confidence scores, and user-oriented recommendations, enabling real-world usability.

3.8 Reproducibility and Collaboration

The CVLab framework integrates version control, experiment logging, team activity tracking, and environment reproducibility through virtual environments and setup scripts. This ensures that experiments can be reproduced across multiple systems and contributors without configuration drift.