#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **દલીલ_સૂચી) {
    if (인수개수 < 1 || !દલીલ_સૂચી[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 ગુજરાતી POSIX\n";
    int 문서 = બનાવો_ફાઇલ("인사.txt", વાંચન_લેખન | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 લંબાઈ_મૂલ્ય = લખો_ફાઇલ_ડેટા(문서, 인사말, sizeof(인사말) - 1);
    બંધ_કરો_ફાઇલ(문서);
    લખો_ફાઇલ_ડેટા(1, 인사말, sizeof(인사말) - 1);
    return લંબાઈ_મૂલ્ય == sizeof(인사말) - 1 ? 0 : 3;
}
