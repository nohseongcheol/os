#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argamaid_Liosta) {
    if (인수개수 < 1 || !argamaid_Liosta[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = fosgail_faidhle("인사.txt", so_leughte_so_sgrìobhte | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 faid_VALUE = sgrìobh_faidhle_dàta(문서, 인사말, sizeof(인사말) - 1);
    dùin_faidhle(문서);
    sgrìobh_faidhle_dàta(1, 인사말, sizeof(인사말) - 1);
    return faid_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
