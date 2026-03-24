#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

// Hàm tạo ma trận 5x5 từ khóa
string generateMatrix(string key) {
    string matrix = "";
    string alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"; // Bỏ chữ J (gộp vào I)

    // Xử lý từ khóa: Viết hoa, đổi J thành I, lọc trùng
    for (char c : key) {
        if (isalpha(c)) {
            char upperC = toupper(c);
            if (upperC == 'J') upperC = 'I';
            if (matrix.find(upperC) == string::npos) matrix += upperC;
        }
    }
    // Điền nốt bảng chữ cái
    for (char c : alphabet) {
        if (matrix.find(c) == string::npos) matrix += c;
    }
    return matrix;
}

// Hàm in ma trận
void printMatrix(string matrix) {
    cout << "\n--- MA TRAN PLAYFAIR ---" << endl;
    for (int i = 0; i < 25; i++) {
        cout << matrix[i] << " ";
        if ((i + 1) % 5 == 0) cout << endl;
    }
    cout << endl;
}

// Hàm chuẩn bị văn bản (Chia cặp, chèn X nếu trùng)
string prepareText(string text, bool isEncrypt) {
    string cleanText = "";
    for (char c : text) {
        if (isalpha(c)) {
            char upperC = toupper(c);
            if (upperC == 'J') upperC = 'I';
            cleanText += upperC;
        }
    }

    if (isEncrypt) {
        string prepared = "";
        for (size_t i = 0; i < cleanText.length(); i++) {
            prepared += cleanText[i];
            if (i + 1 < cleanText.length() && cleanText[i] == cleanText[i+1]) {
                prepared += 'X';
            }
        }
        if (prepared.length() % 2 != 0) prepared += 'X';
        return prepared;
    }
    if (cleanText.length() % 2 != 0) cleanText += 'X';

    return cleanText;
}

// Hàm xử lý mã hóa/giải mã
string playfairCrypt(string text, string matrix, bool isEncrypt) {
    string result = "";
    // Dịch phải/xuống (+1), Dịch trái/lên (-1 tương đương +4 trong modulo 5)
    int shift = isEncrypt ? 1 : 4;

    for (size_t i = 0; i < text.length(); i += 2) {
        char a = text[i];
        char b = text[i+1];

        int posA = matrix.find(a);
        int posB = matrix.find(b);

        int rowA = posA / 5, colA = posA % 5;
        int rowB = posB / 5, colB = posB % 5;

        if (rowA == rowB) { // Cùng hàng
            result += matrix[rowA * 5 + (colA + shift) % 5];
            result += matrix[rowB * 5 + (colB + shift) % 5];
        }
        else if (colA == colB) { // Cùng cột
            result += matrix[((rowA + shift) % 5) * 5 + colA];
            result += matrix[((rowB + shift) % 5) * 5 + colB];
        }
        else { // Khác hàng, khác cột
            result += matrix[rowA * 5 + colB];
            result += matrix[rowB * 5 + colA];
        }
    }
    return result;
}

int main() {
    string key, text;
    int choice;

    cout << "Nhap khoa: ";
    getline(cin, key);

    string matrix = generateMatrix(key);
    printMatrix(matrix);

    cout << "1. Ma hoa\n2. Giai ma\nChon: ";
    cin >> choice;
    cin.ignore(); // Xóa bộ đệm sau khi nhập số

    cout << "Nhap chuoi: \n";
    string tempLine;
    text = ""; // Đảm bảo chuỗi text rỗng trước khi nhập
    while (getline(cin, tempLine)) {
        if (tempLine.empty()) {
            break; // Nếu gặp một dòng trống (nhấn Enter 2 lần), sẽ thoát nhập
        }
        text += tempLine; // Nối các dòng lại với nhau thành 1 chuỗi dài
    }

    bool isEncrypt = (choice == 1);
    string prepared = prepareText(text, isEncrypt);
    string result = playfairCrypt(prepared, matrix, isEncrypt);

    if (isEncrypt) cout << "Ciphertext: " << result << endl;
    else cout << "Plaintext: " << result << endl;

    return 0;
}
