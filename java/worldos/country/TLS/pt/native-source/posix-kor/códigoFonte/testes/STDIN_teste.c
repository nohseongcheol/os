#include <Arquivo_ABI.h>
#include <stdio.h>
#include <string.h>
int main(int item_CONT_NÚM, char **entrada_Lista_f07b3200) {
    (void)item_CONT_NÚM; (void)entrada_Lista_f07b3200;
    char dados[6]; int duração_VALOR = 0;
    puts("POSIX INPUT READY");
    while (duração_VALOR < 6) {
        int resultado = leitura_Arquivo_dados(0, dados + duração_VALOR, 6 - duração_VALOR);
        if (resultado <= 0) return 1;
        duração_VALOR += resultado;
    }
    if (memcmp(dados, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
