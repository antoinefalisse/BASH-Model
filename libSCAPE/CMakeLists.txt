cmake_minimum_required (VERSION 3.10)
project(libSCAPE)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

file(GLOB SOURCE_FILES ${CMAKE_CURRENT_LIST_DIR}/src/*.cpp)
file(GLOB HEADER_FILES ${CMAKE_CURRENT_LIST_DIR}/include/SCAPE/*.h)
set(INCLUDE_FILES ${CMAKE_CURRENT_LIST_DIR}/include/SCAPE)

add_library(libSCAPE STATIC ${SOURCE_FILES} ${HEADER_FILES})

# set(SFML_INCLUDE_DIR "Path to SFML include directory" CACHE PATH "Location of include directory")
# set(GLEW_INCLUDE_DIR "Path to GLEW include directory" CACHE PATH "Location of include directory")
# set(GLM_INCLUDE_DIR "Path to GLM include directory" CACHE PATH "Location of include directory")
	
target_include_directories(libSCAPE PRIVATE ${INCLUDE_FILES})
# target_include_directories(libRender PUBLIC ${SFML_INCLUDE_DIR} ${GLEW_INCLUDE_DIR} ${GLM_INCLUDE_DIR})
