#include <File_ABI.h>
#include <stdio.h>
#include <string.h>
int main(int articolo_CONTA_NUMERI, char **voce_elenco) {
    (void)articolo_CONTA_NUMERI; (void)voce_elenco;
    char dati[6]; int durata_VALORE = 0;
    puts("POSIX INPUT READY");
    while (durata_VALORE < 6) {
        int risultato = 파일자료읽기(0, dati + durata_VALORE, 6 - durata_VALORE);
        if (risultato <= 0) return 1;
        durata_VALORE += risultato;
    }
    if (memcmp(dati, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
