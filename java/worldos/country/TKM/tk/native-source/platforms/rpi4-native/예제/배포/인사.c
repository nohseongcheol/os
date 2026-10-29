#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_Sanaw) {
    if (인수개수 < 1 || !argument_Sanaw[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = aç_faýl("인사.txt", okalýan_ýazylýan | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 dowamlylyk_baha = ýaz_faýl_maglumat(문서, 인사말, sizeof(인사말) - 1);
    ýap_faýl(문서);
    ýaz_faýl_maglumat(1, 인사말, sizeof(인사말) - 1);
    return dowamlylyk_baha == sizeof(인사말) - 1 ? 0 : 3;
}
