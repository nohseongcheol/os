#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **hujja_Doggol) {
    if (인수개수 < 1 || !hujja_Doggol[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = udditde_fiilde("인사.txt", tar_winndu | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 njuuteendi_njaru = winndude_fiilde_keɓe(문서, 인사말, sizeof(인사말) - 1);
    uddude_fiilde(문서);
    winndude_fiilde_keɓe(1, 인사말, sizeof(인사말) - 1);
    return njuuteendi_njaru == sizeof(인사말) - 1 ? 0 : 3;
}
