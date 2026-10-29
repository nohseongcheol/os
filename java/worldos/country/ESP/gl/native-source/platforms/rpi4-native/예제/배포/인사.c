#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argumento_Lista) {
    if (인수개수 < 1 || !argumento_Lista[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 Galego POSIX\n";
    int 문서 = abrir_Ficheiro("인사.txt", de_lectura_e_escrita | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 duración_VALOR = escribir_Ficheiro_datos(문서, 인사말, sizeof(인사말) - 1);
    peche_Ficheiro(문서);
    escribir_Ficheiro_datos(1, 인사말, sizeof(인사말) - 1);
    return duración_VALOR == sizeof(인사말) - 1 ? 0 : 3;
}
