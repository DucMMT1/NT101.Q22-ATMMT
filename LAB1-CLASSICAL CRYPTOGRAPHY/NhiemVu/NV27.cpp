#include <iostream>
#include <vector>
#include <string>

using namespace std;

/*
 Ý tưởng:
 - Viết các ký tự theo dạng zíc-zắc trên nhiều dòng (rails)
 - Sau đó đọc từng dòng từ trên xuống để tạo ciphertext
*/
string railFenceEncrypt(const string& input, int key) {
    // Trường hợp đặc biệt: key không hợp lệ
    if (key <= 1) return input;

    // Tạo các dòng rào
    vector<string> rails(key);

    int currentRow = 0;
    bool goingDown = false; // hướng di chuyển

    for (char ch : input) {
        // (Tùy chọn) bỏ khoảng trắng
        if (ch == ' ') continue;

        // Thêm ký tự vào dòng hiện tại
        rails[currentRow] += ch;

        // Nếu chạm biên thì đổi hướng
        if (currentRow == 0 || currentRow == key - 1) {
            goingDown = !goingDown;
        }

        // Di chuyển lên/xuống
        currentRow += (goingDown ? 1 : -1);
    }

    // Ghép các dòng lại thành kết quả
    string cipher = "";
    for (const string& row : rails) {
        cipher += row;
    }

    return cipher;
}

/*
 Các bước:
 1. Đánh dấu vị trí zigzag
 2. Điền ký tự cipher vào đúng vị trí
 3. Đọc lại theo zigzag để ra plaintext
*/
string railFenceDecrypt(const string& cipher, int key) {
    if (key <= 1) return cipher;

    int len = cipher.length();

    // Tạo ma trận rỗng
    vector<vector<char>> matrix(key, vector<char>(len, '\n'));

    // BƯỚC 1: ĐÁNH DẤU ZIGZAG
    int row = 0, col = 0;
    bool goingDown = false;

    for (int i = 0; i < len; i++) {
        matrix[row][col++] = '*';

        if (row == 0 || row == key - 1) {
            goingDown = !goingDown;
        }

        row += (goingDown ? 1 : -1);
    }

    // BƯỚC 2: ĐIỀN CIPHER VÀO
    int index = 0;
    for (int i = 0; i < key; i++) {
        for (int j = 0; j < len; j++) {
            if (matrix[i][j] == '*' && index < len) {
                matrix[i][j] = cipher[index++];
            }
        }
    }

    // BƯỚC 3: ĐỌC LẠI ZIGZAG
    string result = "";
    row = 0; col = 0;
    goingDown = false;

    for (int i = 0; i < len; i++) {
        result += matrix[row][col++];

        if (row == 0 || row == key - 1) {
            goingDown = !goingDown;
        }

        row += (goingDown ? 1 : -1);
    }

    return result;
}

int main() {
    int choice, key;
    string text;

    cout << "===== RAIL FENCE CIPHER =====\n";
    cout << "1. Ma hoa\n";
    cout << "2. Giai ma\n";
    cout << "Lua chon: ";
    cin >> choice;

    cout << "Nhap key (>=2): ";
    cin >> key;
    cin.ignore();

    cout << "Nhap van ban: ";
    getline(cin, text);

    if (choice == 1) {
        string encrypted = railFenceEncrypt(text, key);
        cout << "\nCiphertext: " << encrypted << endl;
    }
    else if (choice == 2) {
        string decrypted = railFenceDecrypt(text, key);
        cout << "\nPlaintext: " << decrypted << endl;
    }
    else {
        cout << "Lua chon khong hop le!\n";
    }

    return 0;
}
