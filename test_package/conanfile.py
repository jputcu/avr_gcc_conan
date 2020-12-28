from conans import ConanFile, CMake, tools

class AvrGccTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_paths"
    build_requires = "AvrGcc/10.2"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        pass

    def test(self):
        pass

