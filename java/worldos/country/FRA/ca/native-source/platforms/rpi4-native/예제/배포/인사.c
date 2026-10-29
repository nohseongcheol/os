#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **arg_Llista) {
    if (인수개수 < 1 || !arg_Llista[0]) return 2;
    const char 인사말[] = "propi 커널의 C와 Català POSIX\n";
    int 문서 = crear_arxiu("인사.txt", lectura_escriptura | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 durada_VALOR = escriure_arxiu_dades(문서, 인사말, sizeof(인사말) - 1);
    Tanca_arxiu(문서);
    escriure_arxiu_dades(1, 인사말, sizeof(인사말) - 1);
    return durada_VALOR == sizeof(인사말) - 1 ? 0 : 3;
}
