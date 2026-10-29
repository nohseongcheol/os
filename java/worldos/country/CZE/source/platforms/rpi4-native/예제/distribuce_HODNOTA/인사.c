#include <Soubor_ABI.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_Seznam) {
    if (인수개수 < 1 || !argument_Seznam[0]) return 2;
    const char 인사말[] = "vlastní 커널의 C와 čeština POSIX\n";
    int 문서 = otevřít_Soubor("인사.txt", pro_čtení_i_zápis | 없으면만들기 | stříhat_Obsah, 0600);
    if (문서 < 0) return 1;
    입출력결과형 délka_HODNOTA = zápis_Soubor_data(문서, 인사말, sizeof(인사말) - 1);
    Zavřít_Soubor(문서);
    zápis_Soubor_data(1, 인사말, sizeof(인사말) - 1);
    return délka_HODNOTA == sizeof(인사말) - 1 ? 0 : 3;
}
