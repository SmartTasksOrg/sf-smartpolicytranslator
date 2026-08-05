#include "SptClient.hpp"
#include <filesystem>
#include <fstream>
#include <iostream>
namespace fs = std::filesystem;
int main(int argc, char** argv) {
    std::string ds = argv[1], out = argv[2];
    fs::create_directories(out);
    smarttasks::SptClient spt(std::getenv("SPT_URL") ? std::getenv("SPT_URL") : "http://localhost:8000");
    for (auto& e : fs::directory_iterator(ds)) {
        if (e.path().extension() != ".txt") continue;
        std::ifstream in(e.path()); std::string text((std::istreambuf_iterator<char>(in)), {});
        std::string json = spt.translate(text);
        std::string name = e.path().stem().string();
        std::ofstream(out + "/" + name + ".policy.json") << json;
        std::cout << "  " << name << "\n";
    }
}
