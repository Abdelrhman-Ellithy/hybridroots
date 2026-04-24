cmake_minimum_required(VERSION 3.10)
project(hybridroots-c)
set(CMAKE_C_STANDARD 99)

include_directories(include)

add_library(hybridroots src/hybridroots.c)
target_link_libraries(hybridroots m)

add_executable(benchmarks tests/benchmarks.c)
target_link_libraries(benchmarks hybridroots m)
