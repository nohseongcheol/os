#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **Tegtal_lim) {
    if (인수개수 < 1 || !Tegtal_lim[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = sos_bara_denc("인사.txt", jàng_bind | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 diir_xëyma = biir_bara_denc_mbir(문서, 인사말, sizeof(인사말) - 1);
    Tej_bara_denc(문서);
    biir_bara_denc_mbir(1, 인사말, sizeof(인사말) - 1);
    return diir_xëyma == sizeof(인사말) - 1 ? 0 : 3;
}
