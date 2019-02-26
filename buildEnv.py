#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import subprocess
import  cmd
import tempfile

class BuildEnv(object):

    SDK = "/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS10.2.sdk"
    def __init__(self):
        self.platform = "iOS"
        self.sdk = BuildEnv.SDK
        self._tool_cache = dict()

    @staticmethod
    def creatTmpDir(Prefix=""):
        return tempfile.mkdtemp(prefix=Prefix)
    def getDylibs(self, lib):

        if lib.startswith("{SDKPATH}"):
            lib =os.path.splitext(lib[9:])[0]
            lib_path = self.sdk + lib
            lib_path = os.path.join(os.path.dirname(lib_path), os.path.basename(lib_path))
            lib_path = lib_path + ".tbd"
            if os.path.isfile(lib_path):
                return lib_path

env = BuildEnv()
