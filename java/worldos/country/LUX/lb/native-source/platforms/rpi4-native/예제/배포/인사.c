#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **Argument_Lëscht) {
    if (인수개수 < 1 || !Argument_Lëscht[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = ariichten_Fichier("인사.txt", lies_schreiffäeg | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 Längt_VALUE = schreiwen_Fichier_Daten(문서, 인사말, sizeof(인사말) - 1);
    Clôture_Fichier(문서);
    schreiwen_Fichier_Daten(1, 인사말, sizeof(인사말) - 1);
    return Längt_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
