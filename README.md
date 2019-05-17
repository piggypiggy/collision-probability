# counting-derangement

## 功能
python代码包含递推公式的实现和碰撞概率的仿真   
c++代码包含递推公式的实现

## 如何使用
### python
```
python main.py n m t
```
例：
```
python main.py 12 15 3
```

### cc
python的大数运算似乎有误差，没有正确保存大整数乘加运算的结果，导致计算出的概率不正常。   
c++版本使用[GMP](https://gmplib.org/) ，计算的中间结果都用整数或有理分数表示，没有精度误差。
```
g++ main.cc -lgmpxx -lgmp -o main
./main n m t
```
例:
```
./main 12 15 3
```
