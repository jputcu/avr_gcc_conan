cmake_minimum_required(VERSION 3.13)
project(PackageTest CXX)

add_executable(example example.cpp)
target_compile_features(example PUBLIC cxx_std_20)

