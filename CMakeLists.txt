cmake_minimum_required(VERSION 3.4)
project(cpp_utils)

add_subdirectory(third_party/pybind11)
pybind11_add_module(cpp_utils master_mind/utils/common.cpp)
