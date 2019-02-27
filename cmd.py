#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import subprocess




class Xar:

    def __init__(self,cmd,workDir = os.getcwd()):
        self._Xar = [workDir + "/bin/xar"]
        self.cmd = cmd
        self.workDir = workDir
        self.stdout = None
        self.returncode = 0
        self._Xar.extend(cmd)
    def run(self):
        try:
            out = subprocess.check_output(self._Xar, stderr=subprocess.STDOUT, cwd=self.workDir)
        except subprocess.CalledProcessError as err:
            pass
        else:
            self.returncode = 0
            self.stdout = out
        return self

class Segedit:

    def __init__(self, input, output, workDir = os.getcwd()):
        self._Segedit = [workDir + "/bin/Segedit"]
        self.workDir = workDir
        self.stdout = None
        self.returncode = 0
        self._Segedit.extend(input)
        self._Segedit.extend(output)
    def run(self):
        try:
            out = subprocess.check_output(self._Segedit, stderr=subprocess.STDOUT, cwd=self.workDir)
        except subprocess.CalledProcessError as err:
            pass
        else:
            self.returncode = 0
            self.stdout = out
        return self

class Clang:

    def __init__(self, input, output, workDir = os.getcwd()):
        self._clang = [workDir + "/bin/clang" ]
        self._clang.extend(["-cc1"])
        self.workDir = workDir
        self.stdout = None
        self.returncode = 0
        self.input = input
        self.output = output
        self.inputtype = "ir"
    def addArgs(self, args):
        self._clang.extend(args)
    def run(self):
        self._clang.extend(["-x", self.inputtype])
        self._clang.extend(self.input)
        self._clang.extend(["-o"])
        self._clang.extend(self.output)
        try:
            out = subprocess.check_output(self._clang, stderr=subprocess.STDOUT, cwd=self.workDir)
        except subprocess.CalledProcessError as err:
            pass
        else:
            self.returncode = 0
            self.stdout = out
        return self


class Ld:

    def __init__(self, output, workDir = os.getcwd()):
        self._Ld = [workDir + "/bin/ld"]
        self.workDir = workDir
        self.stdout = None
        self.returncode = 0
        self.output = output


    def addArgs(self, args):
        self._Ld.extend(args)

    def run(self):
        self._Ld.extend(["-o", self.output])
        try:
            out = subprocess.check_output(self._Ld, stderr=subprocess.STDOUT, cwd=self.workDir)
        except subprocess.CalledProcessError as err:
            pass
        else:
            self.returncode = 0
            self.stdout = out
        return self