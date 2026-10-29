#include <파일규약.h>
#include <stdio.h>
int main(int element_COMPT, char **introducció_Llista) {
    (void)element_COMPT; (void)introducció_Llista;
    int Fitxer = crear_arxiu("stored.txt", lectura_escriptura | 없으면만들기 | 내용비우기, 0600);
    if (Fitxer < 0 || escriure_arxiu_dades(Fitxer, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Fitxer) < 0) return 2;
    if (Tanca_arxiu(Fitxer) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
