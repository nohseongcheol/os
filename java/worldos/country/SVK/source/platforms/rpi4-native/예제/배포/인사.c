#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_Zoznam) {
    if (인수개수 < 1 || !argument_Zoznam[0]) return 2;
    const char 인사말[] = "vlastné 커널의 C와 Slovenský POSIX\n";
    int 문서 = otvoriť_Súbor("인사.txt", na_čítanie_a_zapisovanie | 없으면만들기 | skrátiť_Obsah, 0600);
    if (문서 < 0) return 1;
    입출력결과형 dĺžka_VALUE = zapísať_Súbor_údaje(문서, 인사말, sizeof(인사말) - 1);
    Zavrieť_Súbor(문서);
    zapísať_Súbor_údaje(1, 인사말, sizeof(인사말) - 1);
    return dĺžka_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
