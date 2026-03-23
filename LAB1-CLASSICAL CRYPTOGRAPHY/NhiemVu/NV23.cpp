#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <ctime>

using namespace std;

// Bảng điểm cho các trigram phổ biến trong tiếng Anh
map<string, double> trigrams = {
    {"THE", 100}, {"AND", 90}, {"ING", 85}, {"ENT", 80}, {"ION", 75},
    {"HER", 70}, {"FOR", 70}, {"THA", 65}, {"NTH", 65}, {"WAS", 60},
    {"ETH", 55}, {"TIO", 55}, {"ATI", 50}, {"ERS", 50}, {"ATE", 45}
};

// Hàm giải mã bằng khóa hoán vị (substitution cipher)
string decrypt(const string &text, const string &key) {
    string res = text;
    for (char &c : res) {
        if (isalpha(c)) {
            bool isUpper = isupper(c);
            c = isUpper ? key[toupper(c) - 'A'] : tolower(key[toupper(c) - 'A']);
        }
    }
    return res;
}

//Hàm tính điểm
double fitness(const string &text) {
    string s;
    for (char c : text) if (isalpha(c)) s += toupper(c);

    double score = 0;
    
    // Duyệt từng trigram (3 ký tự liên tiếp)
    for (int i = 0; i + 2 < s.size(); i++) {
        string tri = s.substr(i, 3);
        
        // Nếu trigram có trong bảng thì cộng điểm
        if (trigrams.count(tri)) score += trigrams[tri];
    }
    return score;
}

// Thuật toán Hill Climbing để tìm key tốt
string hillClimb(const string &cipher) {
    // Tạo key ngẫu nhiên ban đầu
    string key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    random_shuffle(key.begin(), key.end());

    double bestScore = fitness(decrypt(cipher, key));
    int stuck = 0;// đếm số lần không cải thiện

     // Lặp cho đến khi bị "kẹt"
    while (stuck < 1000) {
        string newKey = key;

        // Hoán đổi ngẫu nhiên 2 ký tự trong key
        swap(newKey[rand() % 26], newKey[rand() % 26]);

        double newScore = fitness(decrypt(cipher, newKey));

        if (newScore > bestScore) {
            key = newKey;
            bestScore = newScore;
            stuck = 0;
        } else {
            stuck++;
        }
    }

    return key;
}

int main() {
    srand(time(0));

    string cipher;
    cout << "Nhap ciphertext (ket thuc bang dong trong):\n";

    string line;
    while (true) {
        getline(cin, line);
        if (line.empty()) break;  // dòng trống để kết thúc
        cipher += line + "\n";
    }

    string bestKeyGlobal;
    double bestScoreGlobal = -1e9;

    for (int i = 0; i < 10; i++) {
        string key = hillClimb(cipher);
        double score = fitness(decrypt(cipher, key));

        cout << "Lan " << i + 1 << " - Score: " << score << endl; // debug

        if (score > bestScoreGlobal) {
            bestScoreGlobal = score;
            bestKeyGlobal = key;
        }
    }

    cout << "\n Ket qua: \n";
    cout << decrypt(cipher, bestKeyGlobal) << endl;

    system("pause");
    return 0;
}
