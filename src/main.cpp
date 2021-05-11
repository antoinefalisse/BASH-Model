
#include "util.h"
#include "io.h"
#include "osim.h"
#include "scapeWrapper.h"
#include "window.h"

//
// ArgumentParser
//
class ArgumentParser {
public:
	ArgumentParser(int argc, char** argv) {
		for (uint i = 1; i < argc; i++) {
			args.push_back(std::string(argv[i]));
		}
	}
	const std::string& Get(const std::string& option) const {
		std::vector<std::string>::const_iterator itr = std::find(args.begin(), args.end(), option);
		if (itr != args.end() && ++itr != args.end()) {
			return *itr;
		}
		return "";
	}
	bool Exists(const std::string& option) const {
		return std::find(args.begin(), args.end(), option) != args.end();
	}
private:
	std::vector<std::string> args;
};


//
// The main application
//
int main(int argc, char* argv[]) {

	PRINT("---------------------------------------------------------------");
	PRINT("Animation of 3D Human Surface Models for Biomechanical Analysis");
	PRINT("---------------------------------------------------------------");

	// parse arguments
	ArgumentParser args(argc, argv);

	// help
	if (args.Exists("-h") || args.Exists("--help")) {
		PRINT("Help");
		PRINT("Usage: ...");

		// TODO: explain hotkeys

		exit(EXIT_SUCCESS);
	}

	// OSIM
	if (args.Exists("--osim")) {
		const std::string& filenameOSIM = args.Get("--osim");
		if (!filenameOSIM.empty()) {
			Settings::GetInstance().inputModelOSIM = filenameOSIM;
			PRINT("OSIM file: " << Settings::GetInstance().inputModelOSIM);
		} else {
			PRINT_ERR("Argument .osim was empty.");
		}
	} else {
		PRINT_ERR("No .osim file was specified.");
	}

	// Scaling
	if (args.Exists("--scale")) {
		const std::string& filenameScale = args.Get("--scale");
		if (!filenameScale.empty()) {
			Settings::GetInstance().inputModelScale = filenameScale;
			PRINT("Scale file: " << Settings::GetInstance().inputModelScale);
		} else {
			PRINT_ERR("Argument ScaleFile was empty.");
		}
	} else {
		PRINT("No ScaleFile file was specified. Using generic model.");
	}

	// MOT
	if (args.Exists("--mot")) {
		const std::string& filenameMOT = args.Get("--mot");
		if (!filenameMOT.empty()) {
			Settings::GetInstance().inputModelMOT = filenameMOT;
			PRINT("MOT file: " << Settings::GetInstance().inputModelMOT);
		} else {
			PRINT_ERR("Argument .mot was empty.");
		}
	} else {
		PRINT_ERR("No .mot file was specified.");
	}

	// STO
	if (args.Exists("--sto")) {
		const std::string& filenameSTO = args.Get("--sto");
		if (!filenameSTO.empty()) {
			Settings::GetInstance().inputModelSTO = filenameSTO;
			Settings::GetInstance().visualizeMuscleActivity = true;
			PRINT("STO file: " << Settings::GetInstance().inputModelSTO);
		} else {
			Settings::GetInstance().visualizeMuscleActivity = false;
			Settings::GetInstance().showMuscles = false;
			PRINT("No .sto file was specified. Skipping visualization of muscle activity...");
		}
	} else {
		Settings::GetInstance().visualizeMuscleActivity = false;
		Settings::GetInstance().showMuscles = false;
		PRINT("No .sto file was specified. Skipping visualization of muscle activity...");
	}

	// BASH dir
	if (args.Exists("--bash")) {
		const std::string& bash = args.Get("--bash");
		if (!bash.empty()) {
			Settings::GetInstance().bashDir = bash;
		}
		else {
			PRINT("No BASH directory was specified. Using default...");
		}
	}
	else {
		PRINT("No BASH directory was specified. Using default...");
	}
	PRINT("BASH: " << Settings::GetInstance().bashDir);

	// Baseline Model
	if (args.Exists("--model")) {
		const std::string& filenameModel = args.Get("--model");
		if (!filenameModel.empty()) {
			Settings::GetInstance().baselineModelDir = filenameModel;
		} else {
			PRINT("No Baseline-Model directory was specified. Using default...");
		}
	} else {
		PRINT("No Baseline-Model directory was specified. Using default...");
	}
	PRINT("Baseline-Model: " << Settings::GetInstance().baselineModelDir);

	// SCAPE data dir
	if (args.Exists("--scapedata")) {
		const std::string& scapeData = args.Get("--scapedata");
		if (!scapeData.empty()) {
			Settings::GetInstance().scapeDataDir = scapeData;
		}
		else {
			PRINT("No Scape-data directory was specified. Using default...");
		}
	}
	else {
		PRINT("No Scape-data directory was specified. Using default...");
	}
	PRINT("Scape-data directory: " << Settings::GetInstance().scapeDataDir);

	// Cache mapping dir
	if (args.Exists("--cachemapping")) {
		const std::string& cachemapping = args.Get("--cachemapping");
		if (!cachemapping.empty()) {
			Settings::GetInstance().cacheMappingDir = cachemapping;
		}
		else {
			PRINT("No Cache-mapping directory was specified. Using default...");
		}
	}
	else {
		PRINT("No Cache-mapping directory was specified. Using default...");
	}
	PRINT("Cache-mapping directory: " << Settings::GetInstance().cacheMappingDir);

	// Cache mesh dir
	if (args.Exists("--cachemesh")) {
		const std::string& cachemesh = args.Get("--cachemesh");
		if (!cachemesh.empty()) {
			Settings::GetInstance().cacheMeshDir = cachemesh;
		}
		else {
			PRINT("No Cache-mesh directory was specified. Using default...");
		}
	}
	else {
		PRINT("No Cache-mesh directory was specified. Using default...");
	}
	PRINT("Cache-mesh directory: " << Settings::GetInstance().cacheMeshDir);
	
	// Frames
	if (args.Exists("--frames")) {
		const std::string& limitFrames = args.Get("--frames");
		if (!limitFrames.empty()) {
			Settings::GetInstance().limitFrames = std::stoi(limitFrames);
			PRINT("Limited animation to " << Settings::GetInstance().limitFrames << " frames.");
		}
	}

	// Output
	if (args.Exists("--output")) {
		const std::string& outputDir = args.Get("--output");
		if (!outputDir.empty()) {
			Settings::GetInstance().outputDir = outputDir;
		}
	}
	else {
		PRINT("No Output directory was specified. Using default...");
	}
	PRINT("Output dir: " << Settings::GetInstance().outputDir);

	// Camera
	if (args.Exists("--camera")) {
		const std::string& idxCamera = args.Get("--camera");
		if (!idxCamera.empty()) {
			Settings::GetInstance().idxCamera = idxCamera;
		}
	}
	else {
		PRINT("No Camera index was specified. Using default...");
	}
	PRINT("Camera index: " << Settings::GetInstance().idxCamera);

	// Distance
	if (args.Exists("--distance")) {
		const std::string& distanceCamera = args.Get("--distance");
		if (!distanceCamera.empty()) {
			Settings::GetInstance().cameraDistance = std::stof(distanceCamera);
		}
	}
	else {
		PRINT("No Camera distance was specified. Using default...");
	}
	PRINT("Camera distance: " << Settings::GetInstance().cameraDistance);

	// fov
	if (args.Exists("--fov")) {
		const std::string& fov = args.Get("--fov");
		if (!fov.empty()) {
			Settings::GetInstance().fov = std::stof(fov) * M_PI / 180;
		}
	}
	else {
		PRINT("No fov was specified. Using default...");
	}
	PRINT("Camera fov: " << Settings::GetInstance().fov);

	PRINT("---------------------------------------------------------------");

	// create necessary folders
	if (!CreateFolder(Settings::GetInstance().cacheMappingDir)) {
		PRINT_ERR("Unable to create folder: " + std::string(Settings::GetInstance().cacheMappingDir));
	}
	if (CACHE_ALL_MESHES) {
		std::string osimfile = GetFileFromPath(Settings::GetInstance().inputModelOSIM);
		std::string scaleFile = GetFileFromPath(Settings::GetInstance().inputModelScale);
		std::string motFile = GetFileFromPath(Settings::GetInstance().inputModelMOT);
		Settings::GetInstance().filepathModelCache = std::string(Settings::GetInstance().cacheMeshDir) + osimfile + "/" + scaleFile + "/" + motFile + "/";
		if (!CreateFolder(Settings::GetInstance().filepathModelCache)) {
			PRINT_ERR("Unable to create folder: " + Settings::GetInstance().filepathModelCache);
		}
	}

	// initialize the global model mapper instance
	Model::GetInstance().InitModel();

	// create and start the render window for the application
	//Window window(WindowMode::desktop);
	Window window(WindowMode::window);
	//Window window(WindowMode::fullscreen);
	window.Run();
}