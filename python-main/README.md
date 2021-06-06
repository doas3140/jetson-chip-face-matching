# Installation

```bash
# install the dependencies (if not already onboard)
sudo apt-get install -y python3-pip libopenblas-dev libopenmpi-dev libomp-dev
sudo -H pip3 install future
# upgrade setuptools 47.1.1 -> 54.0.0
sudo -H pip3 install --upgrade setuptools
sudo -H pip3 install Cython
# install gdown to download from Google drive
sudo -H pip3 install gdown
# sudo cp ~/.local/bin/gdown /usr/local/bin/gdown
# download the wheel
gdown https://drive.google.com/uc?id=1-b9rg2yGEdBATdUmIWcSqjkL1b0gvToQ
# install PyTorch 1.7.1
sudo -H pip3 install torch-1.7.1a0-cp36-cp36m-linux_aarch64.whl
```

```bash
pip3 install pyserial tabulate
pip3 install facenet-pytorch
```
