#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_Popis) {
    if (인수개수 < 1 || !argument_Popis[0]) return 2;
    const char 인사말[] = "vlastiti 커널의 C와 hrvatski POSIX\n";
    int 문서 = otvoreno_Datoteka("인사.txt", 읽고쓰기 | 없으면만들기 | skratiti_Sadržaj, 0600);
    if (문서 < 0) return 1;
    입출력결과형 길이 = zapisivanje_Datoteka_podaci(문서, 인사말, sizeof(인사말) - 1);
    Zatvori_Datoteka(문서);
    zapisivanje_Datoteka_podaci(1, 인사말, sizeof(인사말) - 1);
    return 길이 == sizeof(인사말) - 1 ? 0 : 3;
}
