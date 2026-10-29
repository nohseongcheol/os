#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **agụment_ndepụta) {
    if (인수개수 < 1 || !agụment_ndepụta[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = mepee_ọbọakwụkwọ("인사.txt", gụọ_dèe | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 ogologo_valuu = dee_ọbọakwụkwọ_datà(문서, 인사말, sizeof(인사말) - 1);
    mmechi_ọbọakwụkwọ(문서);
    dee_ọbọakwụkwọ_datà(1, 인사말, sizeof(인사말) - 1);
    return ogologo_valuu == sizeof(인사말) - 1 ? 0 : 3;
}
