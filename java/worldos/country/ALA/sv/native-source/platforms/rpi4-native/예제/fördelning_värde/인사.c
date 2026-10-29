#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_ange) {
    if (인수개수 < 1 || !argument_ange[0]) return 2;
    const char 인사말[] = "eget 커널의 C와 Svenska POSIX\n";
    int 문서 = skapa_fil("인사.txt", läsa_skriva | 없으면만들기 | trimma_Innehåll, 0600);
    if (문서 < 0) return 1;
    입출력결과형 längd_värde = skriva_fil_data(문서, 인사말, sizeof(인사말) - 1);
    Stäng_fil(문서);
    skriva_fil_data(1, 인사말, sizeof(인사말) - 1);
    return längd_värde == sizeof(인사말) - 1 ? 0 : 3;
}
