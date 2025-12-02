#include <stdio.h>
#include <ctype.h>
#include <string.h>

// Token Types
typedef enum { TOKEN_INT, TOKEN_ID, TOKEN_OP, TOKEN_EOF } TokenType;

typedef struct {
    TokenType type;
    char value[100];
} Token;

void get_next_token(char **input) {
    char *ptr = *input;
    
    // Skip whitespace
    while (*ptr == ' ' || *ptr == '\n') ptr++;
    
    if (*ptr == '\0') {
        printf("Token: EOF\n");
        return;
    }

    if (isdigit(*ptr)) {
        // Scan Integer
        char buffer[100];
        int i = 0;
        while (isdigit(*ptr)) {
            buffer[i++] = *ptr++;
        }
        buffer[i] = '\0';
        printf("Token: INTEGER (%s)\n", buffer);
    } 
    else if (isalpha(*ptr)) {
        // Scan Identifier
        char buffer[100];
        int i = 0;
        while (isalnum(*ptr)) {
            buffer[i++] = *ptr++;
        }
        buffer[i] = '\0';
        printf("Token: IDENTIFIER (%s)\n", buffer);
    } 
    else {
        // Scan Operator
        printf("Token: OPERATOR (%c)\n", *ptr);
        ptr++;
    }
    
    *input = ptr; // Update the pointer
}

int main() {
    char input[] = "sum = a + 50";
    char *ptr = input;
    
    printf("Analyzing: \"%s\"\n", input);
    printf("--------------------------\n");
    
    while (*ptr != '\0') {
        get_next_token(&ptr);
    }
    
    return 0;
}

