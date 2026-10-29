#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <Arquivo_ABI.h>
#include <tela_ABI.h>
static int comprimento_do_texto_em_octetos(const char *texto) { int duração_VALOR=0;while(texto[duração_VALOR])duração_VALOR++;return duração_VALOR; }
static int saídaTexto(const char *texto) { int duração_VALOR=comprimento_do_texto_em_octetos(texto);return gravar_Arquivo_dados(1,texto,duração_VALOR)==duração_VALOR?0:1; }
#endif
