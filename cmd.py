#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import subprocess


class Cmd(object):

    def __init__(self,cmd,workDir):
        self.cmd = cmd
        self.workDir = workDir
        self.stdout = None
        self.returncode = 0

    def runCmd(self):
        try:
            out = subprocess.check_output(self.cmd, stderr=subprocess.STDOUT,cwd=self.workDir)
        except subprocess.CalledProcessError as err:
            pass
        else:
            self.returncode = 0
            self.stdout = out



class Xar(Cmd):

    def __init__(self,cmd,workDir = os.getcwd()):
        self._Xar = [workDir + "/bin/xar"]
        self._Xar.extend(cmd)
        super(Xar, self).__init__(self._Xar,workDir)
    def run(self):
        self.runCmd()
        return self

class Segedit(Cmd):

    def __init__(self, input, output, workDir = os.getcwd()):
        self._Segedit = [workDir + "/bin/Segedit"]
        self._Segedit.extend(input)
        self._Segedit.extend(output)
        super(Segedit, self).__init__(self._Segedit,workDir)
    def run(self):
        self.runCmd()
        return self

class Clang(Cmd):

    def __init__(self, input, output, workDir = os.getcwd()):
        self._clang = [workDir + "/bin/clang" ]
        self._clang.extend(["-cc1"])
        self.input = input
        self.output = output
        self.inputtype = "ir"
        super(Clang, self).__init__(self._clang, workDir)
    def addArgs(self, args):
        self.cmd.extend(args)
    def run(self):
        self.cmd.extend(["-x", self.inputtype])
        self._clang.extend(self.input)
        self._clang.extend(["-o"])
        self._clang.extend(self.output)
        self.runCmd()
        return self


class Ld(Cmd):

    def __init__(self, output, workDir = os.getcwd()):
        self._Ld = [workDir + "/bin/ld"]
        self.output = output
        super(Ld,self).__init__(self._Ld,workDir)

    def addArgs(self, args):
        self.cmd.extend(args)

    def run(self):
        self.cmd.extend(["-o", self.output])
        self.runCmd()
        return self