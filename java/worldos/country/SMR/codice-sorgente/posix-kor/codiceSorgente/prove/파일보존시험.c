#include <File_ABI.h>
#include <stdio.h>
int main(int articolo_CONTA_NUMERI, char **voce_elenco) {
    (void)articolo_CONTA_NUMERI; (void)voce_elenco;
    int file = aperto_File("stored.txt", in_lettura_scrittura | 없으면만들기 | tagliare_Sommario, 0600);
    if (file < 0 || scrivere_File_dati(file, "saved-from-C", 12) != 12) return 1;
    if (commit_File(file) < 0) return 2;
    if (Chiudi_File(file) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
