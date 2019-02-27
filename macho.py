#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import cmd
import buildEnv
import bundle
import shutil


class MachO(object):

    def __init__(self, input):
        self.inputfile = input
        self.baseName = os.path.basename(input)
        self.type = 1
        self.archs = ['arm64'];
        self.slices = dict()
        self.xarOutPath =dict()
        self.tmpdir = buildEnv.BuildEnv.creatTmpDir(self.baseName)
        self.output_slices = []


    def getXar(self,arch):
        self.slices[arch] = self.inputfile
        self.xarOutPath[arch] = self.inputfile + "_.xar"
        sliceOut = self.inputfile
        xarCmd = [sliceOut, "-extract", "__LLVM", "__bundle"]
        cmd.Segedit(xarCmd, [self.xarOutPath[arch]]).run()
        return self.xarOutPath[arch]
    def buildBitcode(self,arch):
        xarOut = self.getXar(arch)
        output_path = os.path.join(self.tmpdir,self.baseName + "." + arch + ".out")
        bitcode_bundle = bundle.Bitcode(arch,xarOut,output_path).doWork()
        self.output_slices.append(bitcode_bundle)
        return bitcode_bundle
    def Output(self, path):
        shutil.move(self.output_slices[0].output, path)

