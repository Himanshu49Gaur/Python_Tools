#include <stdio.h>
#include <ctype.h>
#include <string.h>

// Token Types
typedef enum { TOKEN_INT, TOKEN_ID, TOKEN_OP, TOKEN_EOF } TokenType;
