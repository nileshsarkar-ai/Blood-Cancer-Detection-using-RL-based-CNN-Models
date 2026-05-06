# Blood-Cancer-Detection-using-RL-based-CNN-Models

RL-augmented CNN classifiers for 4-class Blood Cell Cancer (Acute Lymphoblastic Leukemia) classification on peripheral blood smear images.

**Authors:** Nilesh Sarkar, Sreedevi Sreedhar, Ram Charan Athyam, K Sai Charan
**Date:** 30 November 2025

## Overview

Six pretrained CNN backbones are fine-tuned on the 4-class Blood Cell Cancer (ALL) dataset, then each is paired with a small REINFORCE-style **contextual bandit** that learns to pick one of three augmentation pipelines per image to improve robustness.

**Backbones:** ResNet18, ResNet50, DenseNet121, EfficientNet-B0, MobileNetV2, ConvNeXt-Tiny

## Dataset

- Source: Kaggle — `mohammadamireshraghi/blood-cell-cancer-all-4class`
- 3,242 images across 4 classes: `Benign`, `[Malignant] Pre-B`, `[Malignant] Pro-B`, `[Malignant] early Pre-B`
- Stratified split: train 70% (2269) / val 15% (486) / test 15% (487)

The raw dataset is not committed. To reproduce, download via Kaggle CLI into `data/blood-cell-cancer-all-4class/`.

## Setup

- GPU: NVIDIA A100 (CUDA)
- Python 3.10, torch 2.7.1+cu118, torchvision 0.22.1+cu118
- Supervised: 150 epochs, batch 256, AdamW (lr=1e-4, wd=1e-4), CrossEntropy, mixed precision (AMP)
- RL bandit: frozen ResNet18 feature extractor → small FC policy → 3-action augmentation space, binary reward, 10 episodes, Adam lr=1e-4

## Wall-clock

- Supervised training (all 6 backbones): ~4.5 hours
- RL policy training (all 6 backbones, 10 episodes each): ~5 minutes

## Results (summary)

| Backbone        | Test acc | Best val acc | RL avg reward (last episode) |
|-----------------|---------:|-------------:|-----------------------------:|
| ResNet18        | ~0.99    | 0.999        | 0.16–0.29                    |
| ResNet50        | ~0.99    | 0.999        | 0.29–0.39                    |
| DenseNet121     | ~0.99    | 0.999        | 0.48–0.58                    |
| EfficientNet-B0 | ~0.99    | 0.999        | 0.37–0.53                    |
| MobileNetV2     | ~0.99    | 0.999        | 0.34–0.46                    |
| ConvNeXt-Tiny   | ~0.99    | 0.999        | 0.53–0.63                    |

ConvNeXt-Tiny and DenseNet121 produced the strongest RL reward trends in the short run.

## Repository contents

- `blood_all_rl_cnn_models.ipynb` — main training & evaluation notebook
- `figures/` — accuracy / loss / confusion-matrix / RL-reward plots per backbone (24 figures)
- `rl_policies/` — saved RL policy weights (`{model_name}_rl_policy.pth`)
- `report/report.md` — full project report (also rendered as PDF)
- `blood_all_rl_report_python.pdf` — final PDF report

Excluded from this repo (regenerable):
- `data/` — raw Kaggle dataset (~1.7 GB)
- `checkpoints/` — supervised CNN weights (~300 MB; some files exceed GitHub's 100 MB limit)

## Reproduction

1. Install deps: `pip install torch torchvision numpy scikit-learn matplotlib`
2. Download dataset into `data/blood-cell-cancer-all-4class/` via Kaggle CLI
3. Run `blood_all_rl_cnn_models.ipynb` end-to-end (supervised → RL → evaluation)
4. Rebuild the PDF report:
   ```bash
   pandoc -V geometry:margin=1in -V papersize:a4 \
     -o blood_all_rl_report.pdf report/report.md --pdf-engine=xelatex
   ```

## Limitations & future work

- Binary RL reward is high-variance; soft confidence or loss-delta rewards would help
- Only 10 RL episodes per backbone (demonstration run)
- No comparison against AutoAugment / RandAugment baselines yet
- Cross-dataset validation needed to support generalisation claims
