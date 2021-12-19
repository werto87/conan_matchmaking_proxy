cmake_minimum_required(VERSION 3.5)
project(test_package CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_executable(${PROJECT_NAME} 
example.cpp
userDefinedGameOption.hxx
)
target_link_libraries(${PROJECT_NAME} PRIVATE CONAN_PKG::matchmaking_proxy)
target_compile_features(${PROJECT_NAME} PUBLIC cxx_std_20)
target_compile_definitions(CONAN_PKG::matchmaking_proxy INTERFACE PATH_TO_USER_DEFINED_GAME_OPTION="${CMAKE_CURRENT_SOURCE_DIR}/userDefinedGameOption.hxx")

