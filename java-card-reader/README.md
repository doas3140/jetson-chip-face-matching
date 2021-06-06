
# Java Card Reader

java:

```bash
sudo apt-get install openjdk-11-jre  
sudo apt-get install openjdk-11-jdk  
mvn -e package  
sudo java -jar target/consoleApp-1.0-SNAPSHOT.jar  
```

python:  

```bash
build openjdk(to decode JPEG2000) (https://github.com/uclouvain/openjpeg/blob/master/INSTALL.md):
git clone https://github.com/uclouvain/openjpeg.git  
cd openjpeg  
mkdir build  
cd build  
cmake .. -DCMAKE_BUILD_TYPE=Release  
make  
sudo make install  
sudo make clean  
# install pillow:  
pip3 uninstall pillow # (if needed)  
pip3 install pillow  
pip3 install py4j  
```
