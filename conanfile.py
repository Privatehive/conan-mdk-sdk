#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, download

required_conan_version = ">=2.0"


class MdkSdkConan(ConanFile):
    jsonInfo = json.load(open("info.json", 'r'))
    # ---Package reference---
    name = jsonInfo["projectName"]
    version = jsonInfo["version"]
    user = jsonInfo["domain"]
    channel = "stable"
    # ---Metadata---
    description = jsonInfo["projectDescription"]
    license = jsonInfo["license"]
    author = jsonInfo["vendor"]
    topics = jsonInfo["topics"]
    homepage = jsonInfo["homepage"]
    url = jsonInfo["repository"]
    # ---Requirements---
    requires = []
    tool_requires = ["cmake/[~3]"]
    # ---Sources---
    exports = ["info.json"]
    exports_sources = []
    # ---Binary model---
    package_type = "shared-library"
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = {}
    # ---Folders---
    no_copy_source = True

    @property
    def android_arch_folder(self):
        return {
            "armv7": "armeabi-v7a",
            "armv8": "arm64-v8a",
            "x86": "x86",
            "x86_64": "x86_64",
        }.get(str(self.settings.arch), None)

    def validate(self):
        valid_os = ["Windows", "Linux", "Android"]
        if str(self.settings.os) not in valid_os:
            raise ConanInvalidConfiguration(
                f"{self.name} {self.version} is only supported for the following operating systems: {valid_os}")
        valid_arch = ["x86_64", "x86", "armv7", "armv8"]
        if str(self.settings.arch) not in valid_arch:
            raise ConanInvalidConfiguration(
                f"{self.name} {self.version} is only supported for the following architectures on {self.settings.os}: {valid_arch}")

    def build(self):
        download(self, **self.conan_data["sources"]["mdksdk"][str(self.version)][str(self.settings.os)])
        self.run("cmake -E tar xzf %s" % self.conan_data["sources"]["mdksdk"][str(self.version)][str(self.settings.os)]["filename"])

    def package(self):
        if self.settings.os == "Linux":
            copy(self, "include/*", src="mdk-sdk", dst=self.package_folder)
            copy(self, "libmdk.so*", src=os.path.join("mdk-sdk", "lib", "amd64"), dst=os.path.join(self.package_folder, "lib"))
            copy(self, "libc++.so*", src=os.path.join("mdk-sdk", "lib", "amd64"), dst=os.path.join(self.package_folder, "lib"))
        if self.settings.os == "Windows":
            copy(self, "include/*", src="mdk-sdk", dst=self.package_folder)
            copy(self, "mdk.lib", src=os.path.join("mdk-sdk", "lib", "x64"), dst=os.path.join(self.package_folder, "lib"))
            copy(self, "mdk.dll", src=os.path.join("mdk-sdk", "bin", "x64"), dst=os.path.join(self.package_folder, "bin"))
        elif self.settings.os == "Android":
            copy(self, "include/*", src="mdk-sdk", dst=self.package_folder)
            copy(self, "libmdk.so", src=os.path.join("mdk-sdk", "lib", self.android_arch_folder), dst=os.path.join(self.package_folder, "lib"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "mdk-sdk")
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.components["mdk"].set_property("cmake_target_name", "mdk::mdk")
        self.cpp_info.components["mdk"].set_property("cmake_find_mode", "both")
        self.cpp_info.components["mdk"].libs = ["mdk"]

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.build_type
