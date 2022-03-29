#include <iostream>
#include <vector>
#include <string>
#include <filesystem>
#include <sys/stat.h>

using std::cout; using std::cin;
using std::endl; using std::string;
using std::vector;
using std::filesystem::directory_iterator;


bool IsPathExist(const string &s)
{
    struct stat buffer;
    return (stat (s.c_str(), &buffer) == 0);
}

void tokenize(std::string const &str, const char delim,
              std::vector<std::string> &out)
{
    size_t start;
    size_t end = 0;

    while ((start = str.find_first_not_of(delim, end)) != std::string::npos)
    {
        end = str.find(delim, start);
        out.push_back(str.substr(start, end - start));
    }
}

void get_file_name(string sub_path){
    string subsub_path;
    sub_path += "/lidar/";
    for (const auto & subfile : directory_iterator(sub_path)){
    subsub_path = subfile.path();
    // cout << "all files:"<< subsub_path << endl;
    vector<string> out;
        tokenize(subsub_path,'/',out);
        for (auto &s: out){
            if (s.substr(0,5) == "Tesla"){
                cout << "correct: " << subsub_path << endl;
            }
        }
    }
}

void check_mkdir(string dir_name){
    if (!IsPathExist(dir_name)){
        string command;
        command = "mkdir -p " + dir_name;
        system(command.c_str());
    }
}

int main() {
   // string path = "./";
    /*
    for (const auto & file : directory_iterator(path))
        cout << file.path() << endl;
    return EXIT_SUCCESS;
     */
    /*
    string folder_path = "ws/hello";
    string command;
    command = "mkdir -p " + folder_path;
    system(command.c_str());
    return 0;*/
    /*
     目前解决这个问题了，因为想尝试removert这个工程，所以编译得用到C++17 gcc得8以上的版本

    我的环境是Ubuntu18.04 ros melodic

    系统默认的gcc是7.5

    首先安装 gcc-8 和g++8

    sudo apt-get install gcc-8 g++8

    然后编译的时候用下面的指令就行：

    catkin_make -DCMAKE_C_COMPILER=gcc-8 -DCMAKE_CXX_COMPILER=g++-8
     */
    /*
    string path = "Day11";
    path = path + "/lidar/";
    cout << path << endl;*/


    string path = "/home/zhaoliang/Data_ZZL/mobility_lab/CAV_project/2nd deployment/";
    string sub_path;
    string subsub_path;
    string save_folder_name = "output_data";
    string sub_folder_name;
    check_mkdir(save_folder_name);

    for (const auto & file : directory_iterator(path)){
        sub_path = file.path();

        vector<string> out;
        tokenize(sub_path,'/',out);
        for (auto &s: out){
            if (s.substr(0,3) == "Day"){
                cout << "Folder_day:"<< s << endl;
                sub_folder_name = save_folder_name + "/";
                sub_folder_name += s;
                // cout << "Folder name:"<< sub_folder_name << endl;
                check_mkdir(sub_folder_name);
                // cout << "The correct answer:" << sub_path << endl;
                get_file_name(sub_path);
            }
        }
    // cout << sub_path[] << endl;
    }


    return EXIT_SUCCESS;

}
