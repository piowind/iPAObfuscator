#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import subprocess
import  cmd
import tempfile

class BuildEnv(object):

    SDK = subprocess.check_output(['xcrun', '--sdk', 'iphoneos', '--show-sdk-path'], stderr=subprocess.STDOUT)
    SDK = SDK.replace("\n", "")
    SDK_VER = subprocess.check_output(['xcrun', '--sdk', 'iphoneos', '--show-sdk-version'], stderr=subprocess.STDOUT)
    SDK_VER = SDK_VER.replace("\n", "")
    def __init__(self):
        self.platform = "iOS"
        self.sdk = BuildEnv.SDK
        self._tool_cache = dict()

    @staticmethod
    def creatTmpDir(Prefix=""):
        return tempfile.mkdtemp(prefix=Prefix)
env = BuildEnv()
