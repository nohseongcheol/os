#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_Seznam) {
    if (인수개수 < 1 || !argument_Seznam[0]) return 2;
    const char 인사말[] = "lastno 커널의 C와 slovenščina POSIX\n";
    int 문서 = odprto_Datoteka("인사.txt", branje_pisanje | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 길이 = pisati_Datoteka_podatki(문서, 인사말, sizeof(인사말) - 1);
    Zapri_Datoteka(문서);
    pisati_Datoteka_podatki(1, 인사말, sizeof(인사말) - 1);
    return 길이 == sizeof(인사말) - 1 ? 0 : 3;
}
