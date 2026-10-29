#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **i_agumenti_Uhlu) {
    if (인수개수 < 1 || !i_agumenti_Uhlu[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 Isi_Zulu POSIX\n";
    int 문서 = vula_ifayela("인사.txt", fundeka_bhaleka | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 ubude_inani = bhala_ifayela_imininingwane(문서, 인사말, sizeof(인사말) - 1);
    vala_ifayela(문서);
    bhala_ifayela_imininingwane(1, 인사말, sizeof(인사말) - 1);
    return ubude_inani == sizeof(인사말) - 1 ? 0 : 3;
}
