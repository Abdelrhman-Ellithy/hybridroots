cmake_minimum_required(VERSION 3.11)
project(hybridroots_cpp CXX)
set(CMAKE_CXX_STANDARD 11)

include_directories(include)

# Header-only library

add_executable(benchmarks tests/benchmarks.cpp)
