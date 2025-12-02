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
