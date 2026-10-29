#ifndef nativo_C_E_S_padrão_Cabeçalho
#define nativo_C_E_S_padrão_Cabeçalho
#include <stddef.h>
#include <stdarg.h>
typedef struct { int identificador_de_arquivo, erro, 사용량; } FILE;
extern FILE *stdout, *stderr;
#define EOF (-1)
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
FILE *fdopen(int, const char *);
int fclose(FILE *);
int fflush(FILE *);
size_t fwrite(const void *, size_t, size_t, FILE *);
int fputc(int, FILE *);
int fputs(const char *, FILE *);
int vfprintf(FILE *, const char *, va_list);
int fprintf(FILE *, const char *, ...);
int printf(const char *, ...);
int snprintf(char *, size_t, const char *, ...);
int vsnprintf(char *, size_t, const char *, va_list);
int sprintf(char *, const char *, ...);
#endif
