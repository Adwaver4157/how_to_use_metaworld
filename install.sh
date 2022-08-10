#!/bin/bash
cd /metaworld
pip install -e .
pip install gym==0.20.0
pip install scipy
git config --global --add safe.directory /root/workspace