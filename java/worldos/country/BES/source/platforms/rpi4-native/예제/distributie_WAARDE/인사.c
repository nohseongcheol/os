#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_Lijst) {
    if (인수개수 < 1 || !argument_Lijst[0]) return 2;
    const char 인사말[] = "Eigen 커널의 C와 Nederlands POSIX\n";
    int Guides = open_Bestand("인사.txt", lezen_schrijven | 없으면만들기 | afkappen_Inhoud, 0600);
    if (Guides < 0) return 1;
    입출력결과형 tijdsduur_WAARDE = schrijven_Bestand_gegevens(Guides, 인사말, sizeof(인사말) - 1);
    Sluiten_Bestand(Guides);
    schrijven_Bestand_gegevens(1, 인사말, sizeof(인사말) - 1);
    return tijdsduur_WAARDE == sizeof(인사말) - 1 ? 0 : 3;
}
