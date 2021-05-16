# Jetson Nano ID Card Face Matching

## Prep

### Visual Studio Code

```bash
git clone https://github.com/JetsonHacksNano/installVSCode.git
cd installVSCode
./installVSCode.sh
```

### CPP MTCNN

```bash
# openblas
sudo apt install cmake libopenblas-dev
# Install system packages required by TensorFlow:
sudo apt update
sudo apt install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
# Install and upgrade pip3
sudo apt install python3-pip
sudo pip3 install -U pip testresources setuptools
# Install the Python package dependencies
sudo pip3 install -U numpy==1.16.1 future==0.18.2 mock==3.0.5 h5py==2.10.0 keras_preprocessing==1.1.1 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11
# Install TensorFlow using the pip3 command. This command will install the latest version of TensorFlow compatible with JetPack 4.4.
sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v44 'tensorflow<2'
```

```bash
cd cpp-mtcnn
mkdir build && cd build  
cmake -DCMAKE_BUILD_TYPE=Release ..  
make -j${nproc}  
./main
```

### Java Card Reader

```bash
cd java-card-reader
sudo apt-get install -y openjdk-11-jre openjdk-11-jdk maven
mvn -e package  
```

```bash
# build openjdk(to decode JPEG2000) (https://github.com/uclouvain/openjpeg/blob/master/INSTALL.md):
git clone https://github.com/uclouvain/openjpeg.git  
cd openjpeg  
mkdir build  
cd build  
cmake .. -DCMAKE_BUILD_TYPE=Release  
make  
sudo make install  
sudo make clean  
pip3 uninstall pillow # (if needed)  
pip3 install pillow  
pip3 install py4j  
```

### Python Main

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

## Run

```bash
cd java-card-reader
sudo java -jar target/consoleApp-1.0-SNAPSHOT.jar  
```

```bash
cd python-main
python3 main.py
```