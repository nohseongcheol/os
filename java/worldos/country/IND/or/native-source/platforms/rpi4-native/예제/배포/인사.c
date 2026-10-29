#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **ଯୁକ୍ତି_ତାଲିକା) {
    if (인수개수 < 1 || !ଯୁକ୍ତି_ତାଲିକା[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = ଖୋଲିବା_ଫାଇଲ୍("인사.txt", ପଢିବା_ଲେଖିବା | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = ଲିଖନ_ଫାଇଲ୍_ଡାଟା(문서, 인사말, sizeof(인사말) - 1);
    ବନ୍ଦ_ଫାଇଲ୍(문서);
    ଲିଖନ_ଫାଇଲ୍_ଡାଟା(1, 인사말, sizeof(인사말) - 1);
    return ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ == sizeof(인사말) - 1 ? 0 : 3;
}
