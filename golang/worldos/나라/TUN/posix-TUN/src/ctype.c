#include <ctype.h>

/* Single-byte C/POSIX locale; these are not Unicode character classifiers. */
int isupper(int character) { return character >= 'A' && character <= 'Z'; }
int islower(int character) { return character >= 'a' && character <= 'z'; }
int isalpha(int character) { return isupper(character) || islower(character); }
int isdigit(int character) { return character >= '0' && character <= '9'; }
int isalnum(int character) { return isalpha(character) || isdigit(character); }
int isblank(int character) { return character == ' ' || character == '\t'; }
int isspace(int character) { return character == ' ' || (character >= '\t' && character <= '\r'); }
int iscntrl(int character) { return (character >= 0 && character < 32) || character == 127; }
int isprint(int character) { return character >= 32 && character <= 126; }
int isgraph(int character) { return character >= 33 && character <= 126; }
int ispunct(int character) { return isgraph(character) && !isalnum(character); }
int isxdigit(int character) { return isdigit(character) || (character >= 'a' && character <= 'f') || (character >= 'A' && character <= 'F'); }
int tolower(int character) { return isupper(character) ? character + ('a' - 'A') : character; }
int toupper(int character) { return islower(character) ? character - ('a' - 'A') : character; }
