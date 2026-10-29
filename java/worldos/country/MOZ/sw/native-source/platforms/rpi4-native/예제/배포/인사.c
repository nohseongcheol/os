#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **hoja_Orodha) {
    if (인수개수 < 1 || !hoja_Orodha[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = unda_faili("인사.txt", soma_andika | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 urefu_thamani = andika_faili_data(문서, 인사말, sizeof(인사말) - 1);
    funga_faili(문서);
    andika_faili_data(1, 인사말, sizeof(인사말) - 1);
    return urefu_thamani == sizeof(인사말) - 1 ? 0 : 3;
}
