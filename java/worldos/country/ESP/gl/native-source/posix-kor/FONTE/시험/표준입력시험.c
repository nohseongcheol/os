#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int elemento_CONTAR, char **introdución_Lista) {
    (void)elemento_CONTAR; (void)introdución_Lista;
    char datos[6]; int duración_VALOR = 0;
    puts("POSIX INPUT READY");
    while (duración_VALOR < 6) {
        int RESULTANTE = 파일자료읽기(0, datos + duración_VALOR, 6 - duración_VALOR);
        if (RESULTANTE <= 0) return 1;
        duración_VALOR += RESULTANTE;
    }
    if (memcmp(datos, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
