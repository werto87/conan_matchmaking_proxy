cmake_minimum_required(VERSION 3.12)
project(test_package LANGUAGES CXX)

set(LIB_NAME matchmaking_proxy)
find_package(${LIB_NAME} REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE ${LIB_NAME}::${LIB_NAME})
