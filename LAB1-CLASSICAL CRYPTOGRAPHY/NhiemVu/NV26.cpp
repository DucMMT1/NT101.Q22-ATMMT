#include <iostream>
#include <string>
#include <vector>
#include <cctype>
#include <algorithm>
#include <map>
#include <set>
#include <numeric>
#include <cmath>
#include <iomanip>

using namespace std;

const vector<double> ENG_FREQ = {
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074
};

string cleanText(const string& text) {
    string result;
    for (char ch : text) {
        if (isalpha(ch)) {
            result.push_back(toupper(ch));
        }
    }
    return result;
}

double ioc(const string& s) {
    int n = s.size();
    if (n <= 1) return 0.0;
    vector<int> counts(26, 0);
    for (char ch : s) {
        counts[ch - 'A']++;
    }
    double sum = 0.0;
    for (int c : counts) {
        sum += c * (c - 1);
    }
    return sum / (n * (n - 1));
}

vector<int> kasiskiKeyLengths(const string& cipher, int maxLen = 20) {
    const int MIN_REPEAT = 3;      
    const int MIN_DISTANCE = 3;     
    const int MIN_OCCURRENCES = 2;  

    map<string, vector<int>> positions;
    for (size_t i = 0; i + MIN_REPEAT <= cipher.size(); ++i) {
        string sub = cipher.substr(i, MIN_REPEAT);
        positions[sub].push_back(i);
    }

    set<int> distances;
    for (const auto& p : positions) {
        const auto& vec = p.second;
        if (vec.size() < MIN_OCCURRENCES) continue;
        for (size_t i = 0; i < vec.size(); ++i) {
            for (size_t j = i + 1; j < vec.size(); ++j) {
                int dist = vec[j] - vec[i];
                if (dist >= MIN_DISTANCE) {
                    distances.insert(dist);
                }
            }
        }
    }

    vector<int> candidates;
    for (int len = 2; len <= maxLen; ++len) {
        bool isDivisor = true;
        for (int d : distances) {
            if (d % len != 0) {
                isDivisor = false;
                break;
            }
        }
        if (distances.empty()) {
            candidates.clear();
            break;
        }
        if (isDivisor) {
            candidates.push_back(len);
        }
    }

    if (candidates.empty()) {
        for (int len = 2; len <= maxLen; ++len) candidates.push_back(len);
    }
    return candidates;
}

int selectBestKeyLength(const string& cipher, const vector<int>& candidates) {
    int bestLen = 2;
    double bestIoc = 0.0;
    cout << "=== Evaluating key lengths with IoC ===\n";
    for (int len : candidates) {
        double avgIoc = 0.0;
        int colCount = 0;
        for (int i = 0; i < len; ++i) {
            string col;
            for (size_t j = i; j < cipher.size(); j += len) {
                col.push_back(cipher[j]);
            }
            if (col.size() > 1) {
                avgIoc += ioc(col);
                colCount++;
            }
        }
        avgIoc /= colCount;
        cout << "Length " << setw(2) << len << " : average IoC = " << fixed << setprecision(4) << avgIoc << endl;
        double diff = fabs(avgIoc - 0.065);
        if (fabs(avgIoc - 0.065) < fabs(bestIoc - 0.065) || bestIoc == 0.0) {
            bestIoc = avgIoc;
            bestLen = len;
        }
    }
    cout << "-> Best key length: " << bestLen << " (IoC = " << bestIoc << ")\n\n";
    return bestLen;
}

string findKey(const string& cipher, int keyLen) {
    string key(keyLen, 'A');
    vector<vector<char>> columns(keyLen);
    for (size_t i = 0; i < cipher.size(); ++i) {
        columns[i % keyLen].push_back(cipher[i]);
    }

    cout << "=== Key recovery (chi-squared test) ===\n";
    for (int col = 0; col < keyLen; ++col) {
        vector<int> counts(26, 0);
        for (char ch : columns[col]) {
            counts[ch - 'A']++;
        }
        double bestChi2 = 1e9;
        int bestShift = 0;
        for (int shift = 0; shift < 26; ++shift) {
            double chi2 = 0.0;
            int total = columns[col].size();
            for (int i = 0; i < 26; ++i) {
                int observed = counts[(i + shift) % 26];
                double expected = total * ENG_FREQ[i];
                if (expected > 0) {
                    chi2 += (observed - expected) * (observed - expected) / expected;
                }
            }
            if (chi2 < bestChi2) {
                bestChi2 = chi2;
                bestShift = shift;
            }
        }
        key[col] = 'A' + bestShift;
        cout << "Column " << setw(2) << col << " : best shift = " << bestShift 
             << " -> key char = " << key[col] << " (chi² = " << fixed << setprecision(2) << bestChi2 << ")\n";
    }
    cout << "\nRecovered key: " << key << "\n\n";
    return key;
}

string decrypt(const string& cipher, const string& key) {
    string plain;
    for (size_t i = 0; i < cipher.size(); ++i) {
        int c = cipher[i] - 'A';
        int k = key[i % key.size()] - 'A';
        int p = (c - k + 26) % 26;
        plain.push_back('A' + p);
    }
    return plain;
}

int main() {
    string ciphertext;
    string line;
    while (getline(cin, line)) {
        ciphertext += line;
    }

    string cleaned = cleanText(ciphertext);
    if (cleaned.empty()) {
        cerr << "Error: no alphabetic characters found.\n";
        return 1;
    }

    cout << "Ciphertext length (letters only): " << cleaned.size() << "\n\n";

    vector<int> candidates = kasiskiKeyLengths(cleaned);
    int keyLen = selectBestKeyLength(cleaned, candidates);

    string key = findKey(cleaned, keyLen);

    string plain = decrypt(cleaned, key);

    string lowerPlain;
    for (char ch : plain) lowerPlain.push_back(tolower(ch));
    cout << "=== Decrypted plaintext ===\n";
    cout << lowerPlain << "\n\n";

    cout << "Key used: " << key << "\n";

    return 0;
}