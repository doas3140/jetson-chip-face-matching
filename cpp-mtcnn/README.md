# C++ MTCNN Implementation

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
mkdir -p build && cd build  
cmake -DCMAKE_BUILD_TYPE=Release ..  
make -j${nproc}  
./cpp_mtcnn
```
