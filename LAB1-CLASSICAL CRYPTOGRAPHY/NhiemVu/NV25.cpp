#include <iostream>
#include <string>
#include <cctype>
using namespace std;

string caps(string key) {
    for (char &c : key) {
        c = toupper(c);
    }
    return key;
}

string Encrypt(string text, string key) {
    string result = "";
    int klength = key.length();
    int k = 0;

    for (int i = 0; i < text.length(); i++) {
        char c = text[i];
        if (isalpha(c)) {
            char baseC = isupper(c) ? 'A' : 'a';
            int shift = key[k%klength] - 'A';
            char encr = (c - baseC + shift) % 26 + baseC;
            result += encr;
            k++;
        } else {
            result += c;
        }
    }
    return result;
}

string Decrypt(string text, string key) {
    string result = "";
    int klength = key.length();
    int k = 0;
    for (int i = 0; i < text.length(); i++) {
        char c = text[i];
        if (isalpha(c)) {
            char baseC = isupper(c) ? 'A' : 'a';
            int shift = key[k%klength] - 'A';
            char decr = (c - baseC - shift + 26) % 26 + baseC;
            result += decr;
            k++;
        } else {
            result += c;
        }
    }
    return result;
}

int main() {
    string text, key;
    int menu;
    cout<<"Nhap chuoi: ";
    getline(cin, text);
    cout<<"Nhap khoa: ";
    cin>>key;
    key = caps(key);

    cout<<"1. Ma hoa"<<endl;
    cout<<"2. Giai ma"<<endl;
    cout<<"Chon: ";
    cin>>menu;

    if (menu == 1) {
        string enc = Encrypt(text, key);
        cout<<"Ciphertext: "<<enc;
    } else if (menu == 2){
        string dec = Decrypt(text, key);
        cout<<"Plaintext: "<<dec;
    }
    return 0;
}