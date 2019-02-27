# iPAObfuscator
to Obfuscate iPA which contain bitcode， 是一款针对二进制的加固工具，底层使用的clang是ollvm编译的。

# useage
python main.py  bctest -o bctest_new

# 注意事项
  目前只支持单架构的arm64的macho文件，还不支持fat file

# 加固对比
* 2.使用的混淆参数如下:
    -mllvm -bcf -mllvm -bcf_loop=3 -mllvm -bcf_prob=40 -mllvm-fla -mllvm -split -mllvm -split_num=2
* 3.加固效果如下：
  加固前：
  ![LOGO](https://github.com/godshield/iOSObfuscator/blob/master/logo.png)

  加固后:
  ![LOGO](https://github.com/godshield/iOSObfuscator/blob/master/logo.png)