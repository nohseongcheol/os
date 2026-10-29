#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argumentti_luettelo) {
    if (인수개수 < 1 || !argumentti_luettelo[0]) return 2;
    const char 인사말[] = "oma 커널의 C와 suomi POSIX\n";
    int 문서 = avata_Tiedosto("인사.txt", luku_ja_kirjoitus | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 kesto_ARVO = kirjoitus_Tiedosto_data(문서, 인사말, sizeof(인사말) - 1);
    Sulje_Tiedosto(문서);
    kirjoitus_Tiedosto_data(1, 인사말, sizeof(인사말) - 1);
    return kesto_ARVO == sizeof(인사말) - 1 ? 0 : 3;
}
