#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_Liste) {
    if (인수개수 < 1 || !argument_Liste[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = opne_fil("인사.txt", lese_og_skrivetilgang | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 lengd_VALUE = skrive_fil_data(문서, 인사말, sizeof(인사말) - 1);
    Lukk_fil(문서);
    skrive_fil_data(1, 인사말, sizeof(인사말) - 1);
    return lengd_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
