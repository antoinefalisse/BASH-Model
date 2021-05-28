#pragma once

#include "util.h"


// Default input OSIM model
//#define FILEPATH_DEFAULT_OSIM "./data/OSIM/JK_Data/JK_SCALED.osim"
//#define FILEPATH_DEFAULT_MOT "./data/OSIM/JK_Data/JK_SCALED_running1_kinematics_subTrans.mot"
//#define FILEPATH_DEFAULT_STO "./data/OSIM/JK_Data/JK_SCALED_running1_kinetics_activation.sto"

// Scale factors
#define ESTIMATE_SCALEFACTORS_MARKERDATA true
#define APPLY_SCALEFACTORS_INPUTMODEL false // only for test purposes!

// Default Baseline model in static pose
#define FILEPATH_DEFAULT_BASELINEMODEL_DIR "./data/baselineModel/"
#define FILENAME_BASELINEMODEL "baselineModel.dae" // exported mesh of the baseline model
#define FILENAME_BASELINEMODEL_MARKERS "markers.obj" // exported marker placement of the baseline model

// Default output dir
#define FILEPATH_DEFAULT_OUTPUT_DIR "./data/Videos/Default/"

// Default camera
#define DEFAULT_INDEX_CAMERA "0"

// SCAPE data
#define FILEPATH_SCAPE_DATADIRECTORY "./data/SCAPE/"
#define FILENAME_SCAPE_BINARYDATA "SCAPE_pose.bin"

// Muscles
enum class MuscleMode { LoadFromFile, kNN };
#define MUSCLE_MODE MuscleMode::kNN
#define MUSCLE_MAX_DISTANCE_TO_SURFACE 0.08
#define MUSCLE_MAX_ACTIVITY 14000.0
#define FILEPATH_MUSCLES "./data/muscles/"
// debugging
#define ONLY_RENDER_SINGLE_MUSCLE ""

// cache the model's mesh for every frame
#define CACHE_ALL_MESHES true
#define MESH_NAME_DEFAULT "0_default"
#define MESH_NAME_SCALED "1_scaled"
#define MESH_NAME_TRANSFORMED "2_transformed"
#define MESH_NAME_SCAPE "3_scapespace"
#define FILEPATH_CACHE_MESH "./data/cache/mesh/"

// temporary mapping data
#define FILEPATH_CACHE_MAPPING "./data/cache/mapping/"
#define FILENAME_MARKERSONSCAPE_TRC "markersOnSCAPE.trc" // temporary file that stores the markers in a specific format required for the OpenSim API
#define FILENAME_POSEMAPPING_MOT "OSIMinSCAPEpose.mot" // here the joint angles are stored that define the mapping from the static baseline model to the OSIM model
#define FILENAME_SETUPIK_XML "SetupIK_OSIMinSCAPEpose.xml" // Inverse kinematics setup file used for the mapping from the static baseline model to the OSIM model 

// Shader
#define BIND_ID_BUFFER_POINTLIGHTS 1
#define BIND_ID_BUFFER_MUSCLEDATA 2

// Main BASH directory
#define FILEPATH_BASH_DIR "./"

// Window
#define DEFAULT_WINDOW_MODE WindowMode::window
#define DEFAULT_WINDOW_WIDTH 1280
#define DEFAULT_WINDOW_HEIGHT 720
//#define DEFAULT_WINDOW_WIDTH 1080
//#define DEFAULT_WINDOW_HEIGHT 1920

// Camera
#define M_PI 3.14159265358979323846264338327950288
#define CAMERA_NAME "Camera"
#define DEFAULT_CAMERA_FOV (70.0*M_PI/180)
#define DEFAULT_CAMERA_DISTANCE 5.0f
#define CAMERA_SCROLL_SENSITIVITY 0.2f
#define CAMERA_ROTATION_SENSITIVITY 0.006f
#define CAMERA_PANNING_SENSITIVITY 0.005f
//#define MOUSE_BUTTON_ROTATE_PRESSED MouseButton::LeftPressed
//#define MOUSE_BUTTON_ROTATE_RELEASED MouseButton::LeftReleased
//#define MOUSE_BUTTON_PAN_PPRESSED MouseButton::MiddlePressed
//#define MOUSE_BUTTON_PAN_RELEASED MouseButton::MiddleReleased

#define DEFAULT_SCAPE_SPACE_TRANSFORMATION 1.0f

// OpenGL
#define DEFAULT_POINT_SIZE 1.0f
#define DEFAULT_LINE_WIDTH 1.0f
#define DEFAULT_CLEAR_COLOR 0.2f, 0.2f, 0.2f, 1.0f
#define PRESENTATION_COLOR 1.0f, 1.0f, 1.0f, 1.0f
#define POSITION_FRONT_LIGHT glm::vec3(8.0, 3.0, 0.0)
#define POSITION_BACK_LIGHT glm::vec3(-8.0, 5.0, 3.0)

//// Keys: Window
//#define KEY_CLOSE_WINDOW sf::Keyboard::F9
//#define KEY_TOGGLE_VSYNC sf::Keyboard::V
//#define KEY_RELOAD_SHADERS sf::Keyboard::Slash
//#define KEY_RESET_CAMERA sf::Keyboard::Num0
//#define KEY_CAMERA_FRONT sf::Keyboard::Num1
//#define KEY_CAMERA_BACK sf::Keyboard::Num2
//#define KEY_CAMERA_45RIGHTSIDE sf::Keyboard::Num3
//#define KEY_CAMERA_90RIGHTSIDE sf::Keyboard::Num4
//#define KEY_CAMERA_135RIGHTSIDE sf::Keyboard::Num5
//#define KEY_CAMERA_45LEFTSIDE sf::Keyboard::Num6
//#define KEY_CAMERA_90LEFTSIDE sf::Keyboard::Num7
//#define KEY_CAMERA_135LEFTSIDE sf::Keyboard::Num8
//#define KEY_CAMERA_DEFINED sf::Keyboard::D
//
//// Keys: Rendering
//#define KEY_SHOW_WIREFRAME sf::Keyboard::Comma
//#define KEY_SHOW_POINTS sf::Keyboard::Period
//#define KEY_SHOW_NORMALS sf::Keyboard::N
//
//// Keys: Scene
//#define KEY_PRESENTATION_MODE sf::Keyboard::Enter
//#define KEY_TOOGLE_FLOOR sf::Keyboard::F1
//#define KEY_TOOGLE_ORIGIN sf::Keyboard::F2
//#define KEY_TOOGLE_BOUNDING_BOX sf::Keyboard::F3
//
//// Keys: model
//#define KEY_MODEL_OSIM sf::Keyboard::O
//#define KEY_TOOGLE_MODEL sf::Keyboard::M
//#define KEY_TOOGLE_BONES sf::Keyboard::B
//#define KEY_TOOGLE_MARKERS sf::Keyboard::P
//#define KEY_TOOGLE_MUSCLES sf::Keyboard::F
//
//// Keys: Model state
//#define KEY_MODEL_STATE_DEFAULT sf::Keyboard::Numpad0
//#define KEY_MODEL_STATE_SCALED sf::Keyboard::Numpad1
//#define KEY_MODEL_STATE_TRANSFORMED sf::Keyboard::Numpad2
//#define KEY_MODEL_STATE_SCAPESPACE sf::Keyboard::Numpad3
//#define KEY_OSIM_STATE_DEFAULT sf::Keyboard::Numpad7
//#define KEY_OSIM_STATE_SCAPE sf::Keyboard::Numpad8
//#define KEY_OSIM_STATE_ANIMATION sf::Keyboard::Numpad9
//
//// Keys: Playback
//#define KEY_PLAYBACK_NEXT_FRAME sf::Keyboard::Right
//#define KEY_PLAYBACK_PREV_FRAME sf::Keyboard::Left
//#define KEY_PLAYBACK_SINGLE_FRAME sf::Keyboard::S
//#define KEY_TOGGLE_PLAYBACK_REPEAT sf::Keyboard::R

//
// Settings
//
class Settings {
private:
	Settings() {}
	Settings(const Settings&) = delete;
	Settings& operator=(const Settings&) = delete;
public:
	static Settings& GetInstance() {
		static Settings instance;
		return instance;
	}

	// filepaths
	std::string inputModelOSIM;
	std::string inputModelScale;
	std::string inputModelMOT;
	std::string inputModelSTO;
	std::string ikTaskSetPath;
	std::string baselineModelDir = FILEPATH_DEFAULT_BASELINEMODEL_DIR;
	std::string scapeDataDir = FILEPATH_SCAPE_DATADIRECTORY;
	std::string cacheMeshDir = FILEPATH_CACHE_MESH;
	std::string cacheMappingDir = FILEPATH_CACHE_MAPPING;
	std::string bashDir = FILEPATH_BASH_DIR;
	std::string outputDir = FILEPATH_DEFAULT_OUTPUT_DIR;
	std::string idxCamera = DEFAULT_INDEX_CAMERA;
	float cameraDistance = DEFAULT_CAMERA_DISTANCE;
	float fov = DEFAULT_CAMERA_FOV;
	float scapeSpace = DEFAULT_SCAPE_SPACE_TRANSFORMATION;

	// other parameters
	int limitFrames = -1;
	bool visualizeMuscleActivity = false;
	std::string filepathModelCache;

	// scene
	bool repeatPlayback = false;

	// render settings
	bool showWireframe = false;
	bool showPoints = false;
	bool presentationMode = false;

	// scene
	bool showFloor = false;
	bool showOrigin = false;
	bool showBounds = false;
	bool showNormals = false;

	// model
	bool showModel = true;
	bool showMarkers = false;
	bool showMuscles = false;
	bool showBodyParts = false;

	// osim model
	bool showModelOsim = false;
	bool showMarkersOsim = false;
	bool showMusclesOsim = false;
	bool showBonesOsim = false;

	// Colors
	const std::vector<glm::vec3> COLOR_MAP = { {230, 25, 75}, {60, 180, 75}, {255, 225, 25}, {0, 130, 200}, {245, 130, 48}, {145, 30, 180}, {70, 240, 240}, {240, 50, 230}, {210, 245, 60}, {250, 190, 190}, {0, 128, 128}, {230, 190, 255}, {170, 110, 40}, {255, 250, 200}, {128, 0, 0}, {170, 255, 195}, {128, 128, 0}, {255, 215, 180}, {0, 0, 128}, {128, 128, 128}, {255, 255, 255}, {0, 0, 0} };

};
