#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_Lista) {
    if (인수개수 < 1 || !argument_Lista[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 Malti POSIX\n";
    int 문서 = fetaħ_fajl("인사.txt", qari_kitba | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 tul_VALUE = kiteb_fajl_data(문서, 인사말, sizeof(인사말) - 1);
    agħlaq_fajl(문서);
    kiteb_fajl_data(1, 인사말, sizeof(인사말) - 1);
    return tul_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
