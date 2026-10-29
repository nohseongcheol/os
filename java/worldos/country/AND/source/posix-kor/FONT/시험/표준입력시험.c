#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int element_COMPT, char **introducció_Llista) {
    (void)element_COMPT; (void)introducció_Llista;
    char dades[6]; int durada_VALOR = 0;
    puts("POSIX INPUT READY");
    while (durada_VALOR < 6) {
        int RESULTAT = tancar_arxiu_dades(0, dades + durada_VALOR, 6 - durada_VALOR);
        if (RESULTAT <= 0) return 1;
        durada_VALOR += RESULTAT;
    }
    if (memcmp(dades, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
