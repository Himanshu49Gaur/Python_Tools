#include <stdio.h>
#include <ctype.h>
#include <string.h>

// Token Types
typedef enum { TOKEN_INT, TOKEN_ID, TOKEN_OP, TOKEN_EOF } TokenType;

typedef struct {
    TokenType type;
    char value[100];
} Token;
