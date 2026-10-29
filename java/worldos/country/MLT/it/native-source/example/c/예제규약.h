#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <File_ABI.h>
#include <schermata_ABI.h>
static int lunghezza_del_testo_in_ottetti(const char *testo) { int durata_VALORE=0;while(testo[durata_VALORE])durata_VALORE++;return durata_VALORE; }
static int uscitaTesto(const char *testo) { int durata_VALORE=lunghezza_del_testo_in_ottetti(testo);return scrivere_File_dati(1,testo,durata_VALORE)==durata_VALORE?0:1; }
#endif
