#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **Thulaganyo_lenaane) {
    if (인수개수 < 1 || !Thulaganyo_lenaane[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = bula_faele("인사.txt", buisa_kwala | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 boleele_Boleng = kwala_faele_tshedimosetso(문서, 인사말, sizeof(인사말) - 1);
    tswala_faele(문서);
    kwala_faele_tshedimosetso(1, 인사말, sizeof(인사말) - 1);
    return boleele_Boleng == sizeof(인사말) - 1 ? 0 : 3;
}
