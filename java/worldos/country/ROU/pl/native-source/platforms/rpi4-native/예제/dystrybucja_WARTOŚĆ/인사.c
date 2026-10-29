#include <Plik_ABI.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_Lista) {
    if (인수개수 < 1 || !argument_Lista[0]) return 2;
    const char 인사말[] = "własny 커널의 C와 polski POSIX\n";
    int 문서 = otwarty_Plik("인사.txt", R_W | 없으면만들기 | obcinać_Spis_treści, 0600);
    if (문서 < 0) return 1;
    입출력결과형 długość_WARTOŚĆ = zapis_Plik_dane(문서, 인사말, sizeof(인사말) - 1);
    Zamknij_Plik(문서);
    zapis_Plik_dane(1, 인사말, sizeof(인사말) - 1);
    return długość_WARTOŚĆ == sizeof(인사말) - 1 ? 0 : 3;
}
