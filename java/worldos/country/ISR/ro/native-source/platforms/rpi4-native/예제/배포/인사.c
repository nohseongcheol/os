#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_Listă) {
    if (인수개수 < 1 || !argument_Listă[0]) return 2;
    const char 인사말[] = "propriu 커널의 C와 Română POSIX\n";
    int 문서 = crea_Fișier("인사.txt", citire_scriere | 없으면만들기 | trunchia_TOC, 0600);
    if (문서 < 0) return 1;
    입출력결과형 lungime_VALUE = scriere_Fișier_date(문서, 인사말, sizeof(인사말) - 1);
    închide_Fișier(문서);
    scriere_Fișier_date(1, 인사말, sizeof(인사말) - 1);
    return lungime_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
