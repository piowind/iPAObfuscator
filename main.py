#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, getopt
import bundle
from macho import MachO

def main(argv):
   outputfile = ''
   try:
      opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   inputfile = argv[0]
   outputfile =argv[2]
   if inputfile is not None:
       # 对输入的文件进行Macho处理
       machoFile = MachO(inputfile)
       # 对macho里面的每个Arch 进行bitCode重编译
       map(machoFile.buildBitcode, machoFile.archs)
       machoFile.Output(outputfile)
       # 最后执行lipo create

if __name__ == "__main__":
   main(sys.argv[1:])