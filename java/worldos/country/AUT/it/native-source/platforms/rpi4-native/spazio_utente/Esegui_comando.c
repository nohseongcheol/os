#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*inizializzatore_metodo)(void);
extern inizializzatore_metodo __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_USER_app(int);
int USER_START(int 전달값) {
    for (inizializzatore_metodo *dati_funzione = __init_array_start; dati_funzione < __init_array_end; dati_funzione++) (*dati_funzione)();
    int risultato = START_USER_app(전달값);
    for (inizializzatore_metodo *dati_funzione = __fini_array_end; dati_funzione != __fini_array_start;) (*--dati_funzione)();
    return risultato;
}
void *memset(void *dati_funzione, int VALORE, size_t voce_CONTA_NUMERI) { unsigned char *meta_dati = dati_funzione; while (voce_CONTA_NUMERI--) *meta_dati++ = VALORE; return dati_funzione; }
void *memcpy(void *meta_dati, const void *stringa_dati, size_t voce_CONTA_NUMERI) { unsigned char *첫째값 = meta_dati; const unsigned char *SECONDO_VALORE = stringa_dati; while (voce_CONTA_NUMERI--) *첫째값++ = *SECONDO_VALORE++; return meta_dati; }
