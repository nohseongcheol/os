#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **arg_Rhestr) {
    if (인수개수 < 1 || !arg_Rhestr[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 Cymraeg POSIX\n";
    int 문서 = agor_ffeil("인사.txt", darllen_ysgrifennu | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 hyd_VALUE = ysgrifennu_ffeil_data(문서, 인사말, sizeof(인사말) - 1);
    cau_ffeil(문서);
    ysgrifennu_ffeil_data(1, 인사말, sizeof(인사말) - 1);
    return hyd_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
