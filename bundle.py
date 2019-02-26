#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from cmd import Xar,Clang,Ld
from buildEnv import env

import xml.etree.ElementTree as ET
import  subprocess



class XarFile(object):

      def __init__(self,input):
        self.input = input
        self.dir = env.creatTmpDir()
        ExtraxmlCmd = ["-d", "-", "-f", input]
        retInfo = Xar(ExtraxmlCmd).run()
        self.xml = ET.fromstring(retInfo.stdout)
        Extracmd = ["-x", "-C", self.dir, "-f", input]
        Xar(Extracmd).run()
        cmd = ['/bin/chmod', "-R", "+r", self.dir]
        try:
            out = subprocess.check_output(cmd)
        except subprocess.CalledProcessError:
            print "error"

      @property
      def subdoc(self):
          return self.xml.find("subdoc")
      @property
      def toc(self):
          return self.xml.find("toc")

class Bitcode(XarFile):

      def __init__(self, arch, bundle, output):
          self.arch = arch
          self.bundle = bundle
          self.output = os.path.realpath(output)
          super(Bitcode, self).__init__(bundle)

          self.platform = "iPhoneOS"
          self.sdk_version = "10.2.0"
          self.version = "1.0"
      def getAllFiles(self, type):
          return filter(lambda x: x.find("file-type").text == type, self.toc.findall("file"))

      def getobf(self):
          return ["-mllvm", "-enable-bcfobf", "-mllvm", "-enable-strcry", "-mllvm", "-enable-splitobf"]

      def consObj(self, xmlNode):
          name = os.path.join(self.dir, xmlNode.find("name").text)
          output = name + ".o"
          if xmlNode.find("clang") is not None:
            clang = Clang([name], [output])
            options = ['-triple', 'arm64-apple-ios8.0.0', '-emit-obj', '-disable-llvm-optzns', '-target-abi', 'darwinpcs', '-Os']
          if '-disable-llvm-passes' in options:
              options.remove('-disable-llvm-passes')
          clang.addArgs(options)
          clang.addArgs(self.getobf())
          return clang

      def run_J(self, job):
           rv = job.run()
           return rv
      def run(self):
          l_inputs = []
          lin = Ld(self.output)
          lin.addArgs(["-arch", self.arch])
          lin.addArgs(["-ios_version_min", "8.0.0"])
          lin.addArgs(["-syslibroot", env.SDK])
          lin.addArgs(["-sdk_version", self.sdk_version])
          bitcodefiles = self.getAllFiles("Bitcode")

          bitcodeBundle = map(self.consObj, bitcodefiles)
          l_inputs.extend(bitcodeBundle)

          map(self.run_J,l_inputs)
          inputs = sorted([os.path.basename(x.output[0]) for x in l_inputs])
          LinkFileList = os.path.join(self.dir, self.output + ".LinkFileList")
          with open(LinkFileList, 'w') as f:
             for i in inputs:
                 f.write(os.path.join(self.dir, i))
                 f.write('\n')
          lin.addArgs(["-filelist", LinkFileList])
          dylibs_node = self.subdoc.find("dylibs")
          if dylibs_node is not None:
             for lib_node in dylibs_node.iter():
                 if lib_node.tag == "lib":
                     lib_path = env.getDylibs(lib_node.text)
                     lin.addArgs([lib_path])

          retinfo = self.run_J(lin)
          return self
