cmake_minimum_required (VERSION 3.10)
project(libRender)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

file(GLOB SOURCE_FILES ${CMAKE_CURRENT_LIST_DIR}/src/*.cpp)
file(GLOB HEADER_FILES ${CMAKE_CURRENT_LIST_DIR}/include/render/*.h)
set(INCLUDE_FILES ${CMAKE_CURRENT_LIST_DIR}/include/render)

add_library(libRender STATIC ${SOURCE_FILES} ${HEADER_FILES})

set(SFML_INCLUDE_DIR "Path to SFML include directory" CACHE PATH "Location of include directory")
set(GLEW_INCLUDE_DIR "Path to GLEW include directory" CACHE PATH "Location of include directory")
set(GLM_INCLUDE_DIR "Path to GLM include directory" CACHE PATH "Location of include directory")
	
target_include_directories(libRender PRIVATE ${INCLUDE_FILES})
target_include_directories(libRender PUBLIC ${SFML_INCLUDE_DIR} ${GLEW_INCLUDE_DIR} ${GLM_INCLUDE_DIR})
