#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools

class MdkSdkConan(ConanFile):
    name = "mdk-sdk"
    version = "0.12.0"
    license = "proprietary"
    url = "https://github.com/Tereius/conan-mdk-sdk"
    description = "Multimedia development kit"
    author = "wang-bin"
    homepage = "https://github.com/wang-bin/mdk-sdk"
    settings = ("os", "compiler", "arch", "build_type")

    def source(self):
        switcher = {
            "Windows": "mdk-sdk-windows-desktop.7z",
            "WindowsStore": "mdk-sdk-uwp.7z",
            "Linux": "mdk-sdk-linux.tar.xz",
            "Macos": "mdk-sdk-macOS.tar.xz",
            "Android": "mdk-sdk-android.7z",
            "iOS": "mdk-sdk-iOS.tar.xz"
        }

        tools.get("https://github.com/wang-bin/mdk-sdk/releases/download/v%s/%s" % (
        self.version, switcher.get(str(self.settings.os))))

    def package(self):
        self.copy("*", src="mdk-sdk")

    def package_info(self):
        self.cpp_info.builddirs = ['lib/cmake']

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.arch
        del self.info.settings.build_type
