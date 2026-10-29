#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_durada(const char *SMS) { int durada_VALOR=0;while(SMS[durada_VALOR])durada_VALOR++;return durada_VALOR; }
static int Sortida(const char *SMS) { int durada_VALOR=SMS_durada(SMS);return escriure_arxiu_dades(1,SMS,durada_VALOR)==durada_VALOR?0:1; }
#endif
