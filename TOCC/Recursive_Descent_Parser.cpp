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

// Rule: E' -> + T E' | epsilon
void E_prime() {
    if (lookahead == '+') {
        cout << "Parsing E' -> + T E'" << endl;
        match('+');
        T();
        E_prime();
    } else {
        cout << "Parsing E' -> epsilon" << endl;
        // Do nothing (epsilon)
    }
}

// Rule: T -> id (we assume 'i' represents an identifier)
void T() {
    if (lookahead == 'i') {
        cout << "Parsing T -> id" << endl;
        match('i');
    } else {
        error();
    }
}


