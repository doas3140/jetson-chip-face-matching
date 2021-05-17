# Python (Numpy) <-> C++ (OpenCV Mat)

## 1. install opencv (no need for jetson)

```bash
sudo apt update && sudo apt install -y cmake g++ wget unzip
wget -O opencv.zip https://github.com/opencv/opencv/archive/master.zip
unzip opencv.zip
mkdir -p build && cd build
cmake  ../opencv-master
cmake --build .
```

## 2. install cmake & boost

```bash
sudo apt install build-essential libboost-all-dev
sudo apt-get install cmake cmake-gui build-essential
# set opencv (no need for jetson), boost src in CMakeLists.txt
```

## 3. build

```bash
mkdir -p build && cd build
cmake ..
make 
```

## 4. test

```bash
python3
```

```python
import numpy as np
import pbcvt

a = np.array([[1., 2., 3.]])
b = np.array([[1.],
              [2.],
              [3.]])
print(pbcvt.dot(a, b)) # should print [[14.]]
print(pbcvt.dot2(a, b)) # should also print [[14.]]
```

## 5. copy built python .so file

```bash
cp build/pbcvt.cpython-36m-aarch64-linux-gnu.so ../python-main/
cp -r mtCNNModels .. # mtcnn model requires this
```
