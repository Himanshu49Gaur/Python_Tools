#include <iostream>
#include <string>

using namespace std;

string input;
int pos = 0;
char lookahead;

// Function Prototypes
void E();
void E_prime();
void T();
void match(char t);

void error() {
    cout << "Syntax Error!" << endl;
    exit(1);
}

void match(char t) {
    if (lookahead == t) {
        pos++;
        if (pos < input.length()) lookahead = input[pos];
        else lookahead = '$'; // End of string
    } else {
        error();
    }
}

// Rule: E -> T E'
void E() {
    cout << "Parsing E -> T E'" << endl;
    T();
    E_prime();
}


