#include <iostream>
#include <string>
using namespace std;

string Encrypt(string text, int key) {
    string result ="";
    for (char c : text) {
        if (isalpha(c)) {
            char baseC = isupper(c) ? 'A' : 'a';
            char encr = (c - baseC + key) % 26 + baseC;
            result += encr;
        } else {
            result += c;
        }
    }
    return result;
}

string Decrypt(string text, int key) {
    string result = "";
    for (char c : text) {
        if (isalpha(c)) {
            char baseC = isupper(c) ? 'A' : 'a';
            char decr = (c - baseC - key + 26) % 26 + baseC;
            result += decr;
        } else {
            result += c;
        }
    }
    return result;
}

int main() {
    string text;
    int key, menu;
    cout<<"Nhap chuoi: ";
    getline(cin, text);
    cout<<"Nhap khoa: ";
    cin>>key;
    cout<<"1. Ma hoa"<<endl;
    cout<<"2. Giai ma"<<endl;
    cout<<"Chon: ";
    cin>>menu;
    
    if (menu == 1) {
        string enc = Encrypt(text, key);
        cout<<"Ciphertext: "<<enc;
    }
    else if (menu == 2) {
        string dec = Decrypt(text, key);
        cout<<"Plain text: "<<dec;
    } else {
        cout<<"Khong hop le"<<endl;
    }
    return 0;
}