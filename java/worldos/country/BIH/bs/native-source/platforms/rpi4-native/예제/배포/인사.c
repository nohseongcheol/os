#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_spisak) {
    if (인수개수 < 1 || !argument_spisak[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = kreirati_fajl("인사.txt", i_za_čitanje_i_za_pisanje | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 dužina_VALUE = pisati_fajl_podaci(문서, 인사말, sizeof(인사말) - 1);
    zatvoriti_fajl(문서);
    pisati_fajl_podaci(1, 인사말, sizeof(인사말) - 1);
    return dužina_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
