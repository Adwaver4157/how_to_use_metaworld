#!/bin/bash
pip install git+https://github.com/rlworkgroup/metaworld.git@master#egg=metaworld
pip install gym==0.21.0
pip install scipy stable-baselines3 wandb
pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 -f https://download.pytorch.org/whl/torch_stable.html
git config --global --add safe.directory /root/workspace