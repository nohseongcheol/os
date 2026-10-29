#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **frumbreyta_Listi) {
    if (인수개수 < 1 || !frumbreyta_Listi[0]) return 2;
    const char 인사말[] = "eigin 커널의 C와 Íslenska POSIX\n";
    int 문서 = opið_skrá("인사.txt", les_skrifheimild | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 lengd_VALUE = skrifa_skrá_gögn(문서, 인사말, sizeof(인사말) - 1);
    loka_skrá(문서);
    skrifa_skrá_gögn(1, 인사말, sizeof(인사말) - 1);
    return lengd_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
