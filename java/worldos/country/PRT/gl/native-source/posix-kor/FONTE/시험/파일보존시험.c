#include <파일규약.h>
#include <stdio.h>
int main(int elemento_CONTAR, char **introdución_Lista) {
    (void)elemento_CONTAR; (void)introdución_Lista;
    int Ficheiro = abrir_Ficheiro("stored.txt", de_lectura_e_escrita | 없으면만들기 | 내용비우기, 0600);
    if (Ficheiro < 0 || escribir_Ficheiro_datos(Ficheiro, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Ficheiro) < 0) return 2;
    if (peche_Ficheiro(Ficheiro) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
