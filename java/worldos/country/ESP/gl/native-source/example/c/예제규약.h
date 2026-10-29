#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_duración(const char *Texto) { int duración_VALOR=0;while(Texto[duración_VALOR])duración_VALOR++;return duración_VALOR; }
static int Saída(const char *Texto) { int duración_VALOR=SMS_duración(Texto);return escribir_Ficheiro_datos(1,Texto,duración_VALOR)==duración_VALOR?0:1; }
#endif
