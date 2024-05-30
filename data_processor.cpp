#include <iostream>
#include <vector>
#include <algorithm>
#include <sstream>

class DataProcessor {
public:
    static double calculateAverage(const std::vector<double>& data) {
        if (data.empty()) {
            return 0.0;
        }
        double sum = 0.0;
        for (double value : data) {
            sum += value;
        }
        return sum / data.size();
    }

    static double findMax(const std::vector<double>& data) {
        if (data.empty()) {
            return 0.0;
        }
        return *std::max_element(data.begin(), data.end());
    }

    static double findMin(const std::vector<double>& data) {
        if (data.empty()) {
            return 0.0;
        }
        return *std::min_element(data.begin(), data.end());
    }
};

// Function to convert command-line arguments to a vector of doubles
std::vector<double> parseArguments(int argc, char* argv[]) {
    std::vector<double> data;
    for (int i = 1; i < argc; ++i) {
        double value;
        std::istringstream iss(argv[i]);
        if (iss >> value) {
            data.push_back(value);
        }
    }
    return data;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Please provide data values as command-line arguments." << std::endl;
        return 1;
    }

    std::vector<double> data = parseArguments(argc, argv);
    
    double avg = DataProcessor::calculateAverage(data);
    double max = DataProcessor::findMax(data);
    double min = DataProcessor::findMin(data);

    std::cout << "Average: " << avg << std::endl;
    std::cout << "Max: " << max << std::endl;
    std::cout << "Min: " << min << std::endl;

    return 0;

}
