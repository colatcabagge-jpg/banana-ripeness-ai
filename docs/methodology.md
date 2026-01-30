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
