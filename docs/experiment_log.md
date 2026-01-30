# Experiment Log

## EXP-001 — Baseline Training (MobileNetV2, Frozen Backbone)

Date: 2026-01-24  
Goal: Establish baseline accuracy for banana ripeness classification.

Dataset:
- Source: Kaggle — Banana Ripeness Classification Dataset
- Classes: unripe, ripe, overripe, rotten

Config:
- Input Size: 224x224
- Batch Size: 32 (to be reduced if memory issues occur)
- Optimizer: Adam (1e-3)
- Epochs: 15
- Augmentation: None (baseline)

Status:
- Training interrupted due to system overload.
- Next step: Reduce memory load (batch size ↓, remove cache, fewer epochs).

Next Actions:
- Try batch size 16 or 8
- Remove dataset caching
- Limit epochs to 8–10 for MVP
