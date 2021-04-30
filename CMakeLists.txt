cmake_minimum_required (VERSION 3.10)
project(SCAPE)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

add_subdirectory(libRender)
add_subdirectory(libSCAPE)

file(GLOB SOURCE_FILES ${CMAKE_CURRENT_LIST_DIR}/src/*.cpp)
file(GLOB HEADER_FILES ${CMAKE_CURRENT_LIST_DIR}/include/SCAPE/*.h)
file(GLOB SHADER_FILES ${CMAKE_CURRENT_LIST_DIR}/shader/*)
set(INCLUDE_FILES ${CMAKE_CURRENT_LIST_DIR}/include/SCAPE)

set(INCLUDE_RENDER_FILES ${CMAKE_CURRENT_LIST_DIR}/libRender/include/)
set(INCLUDE_SCAPE_FILES ${CMAKE_CURRENT_LIST_DIR}/libSCAPE/include/)

add_executable(SCAPE ${SOURCE_FILES} ${HEADER_FILES} ${SHADER_FILES})
source_group("Shader Files" FILES ${SHADER_FILES})

set(GLM_INCLUDE_DIR "Path to GLM include directory" CACHE PATH "Location of include directory")
set(SFML_INCLUDE_DIR "Path to SFML include directory" CACHE PATH "Location of include directory")
set(AMD_INCLUDE_DIR "Path to AMD include directory" CACHE PATH "Location of include directory")
set(UMFPACK_INCLUDE_DIR "Path to UMFPACK include directory" CACHE PATH "Location of include directory")
set(SUITESPARSE_CONFIG_DIR "Path to SuiteSparse_config directory" CACHE PATH "Location of directory")
set(GLEW_INCLUDE_DIR "Path to GLEW include directory" CACHE PATH "Location of directory")
set(GSL_DIR "Path to GSL directory" CACHE PATH "Location of directory")
set(OPENSIM_INCLUDE_DIR "Path to OpenSim include directory" CACHE PATH "Location of directory")
set(OPENSIM_INCLUDE_OPENSIM_DIR "Path to OpenSim include OpenSim directory" CACHE PATH "Location of directory")
set(SIMBODY_INCLUDE_DIR "Path to Simbody include directory" CACHE PATH "Location of directory")
set(SPDLOG_INCLUDE_DIR "Path to spdlog include directory" CACHE PATH "Location of directory")
set(ASSIMP_INCLUDE_DIR "Path to Assimp include directory" CACHE PATH "Location of directory")

set(OPENSIM_LIB_DIR "Path to OpenSim lib directory" CACHE PATH "Location of directory")
set(SIMBODY_LIB_DIR "Path to Simbody lib directory" CACHE PATH "Location of directory")
set(SUITESPARSE_LIB_DIR "Path to SuiteSparse lib directory" CACHE PATH "Location of directory")
set(GSL_LIB_DIR "Path to gsl lib directory" CACHE PATH "Location of directory")
set(GLEW_LIB_DIR "Path to glew lib directory" CACHE PATH "Location of directory")
set(SFML_LIB_DIR "Path to sfml lib directory" CACHE PATH "Location of directory")
set(ASSIMP_LIB_DIR "Path to assimp lib directory" CACHE PATH "Location of directory")

	
target_include_directories(SCAPE PRIVATE ${INCLUDE_FILES})
target_include_directories(SCAPE PUBLIC ${INCLUDE_RENDER_FILES} ${GLM_INCLUDE_DIR} ${GLEW_INCLUDE_DIR} ${OPENSIM_INCLUDE_DIR} ${OPENSIM_INCLUDE_OPENSIM_DIR} ${ASSIMP_INCLUDE_DIR} ${SPDLOG_INCLUDE_DIR} ${INCLUDE_SCAPE_FILES}  ${SIMBODY_INCLUDE_DIR} ${SFML_INCLUDE_DIR} ${AMD_INCLUDE_DIR} ${UMFPACK_INCLUDE_DIR} ${SUITESPARSE_CONFIG_DIR} ${GSL_DIR})

# I don't get where opengl32.lib and glu32.lib are but that seems okay.
# TODO: not sure that's where libRender.lib and libSCAPE.lib will be.
target_link_libraries(SCAPE PUBLIC ${OPENSIM_LIB_DIR}/osimActuators.lib ${OPENSIM_LIB_DIR}/osimAnalyses.lib ${OPENSIM_LIB_DIR}/osimCommon.lib 
${OPENSIM_LIB_DIR}/osimSimulation.lib ${OPENSIM_LIB_DIR}/osimTools.lib ${OPENSIM_LIB_DIR}/osimLepton.lib ${SIMBODY_LIB_DIR}/liblapack.lib ${SIMBODY_LIB_DIR}/libblas.lib
${SIMBODY_LIB_DIR}/SimTKcommon.lib ${SIMBODY_LIB_DIR}/SimTKmath.lib ${SIMBODY_LIB_DIR}/SimTKsimbody.lib ${SUITESPARSE_LIB_DIR}/libamd.lib ${SUITESPARSE_LIB_DIR}/libbtf.lib
${SUITESPARSE_LIB_DIR}/libcamd.lib ${SUITESPARSE_LIB_DIR}/libccolamd.lib ${SUITESPARSE_LIB_DIR}/libcholmod.lib ${SUITESPARSE_LIB_DIR}/libcolamd.lib
${SUITESPARSE_LIB_DIR}/libcxsparse.lib ${SUITESPARSE_LIB_DIR}/libklu.lib ${SUITESPARSE_LIB_DIR}/libldl.lib ${SUITESPARSE_LIB_DIR}/libspqr.lib
${SUITESPARSE_LIB_DIR}/libumfpack.lib ${SUITESPARSE_LIB_DIR}/metis.lib ${SUITESPARSE_LIB_DIR}/suitesparseconfig.lib ${GSL_LIB_DIR}/gsl.lib ${GLEW_LIB_DIR}/glew32.lib
${SFML_LIB_DIR}/sfml-graphics.lib  ${SFML_LIB_DIR}/sfml-window.lib  ${SFML_LIB_DIR}/sfml-system.lib ${CMAKE_CURRENT_BINARY_DIR}/libRender/Release/libRender.lib ${CMAKE_CURRENT_BINARY_DIR}/libSCAPE/Release/libSCAPE.lib
${ASSIMP_LIB_DIR}/assimp.lib opengl32.lib glu32.lib)
