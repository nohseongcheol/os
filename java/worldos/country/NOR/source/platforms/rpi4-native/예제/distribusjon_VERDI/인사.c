#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_Liste) {
    if (인수개수 < 1 || !argument_Liste[0]) return 2;
    const char 인사말[] = "eget 커널의 C와 norsk POSIX\n";
    int 문서 = åpen_Fil("인사.txt", lese_og_skrive | 없으면만들기 | avkorte_Innhold, 0600);
    if (문서 < 0) return 1;
    입출력결과형 lengde_VERDI = skrive_Fil_data(문서, 인사말, sizeof(인사말) - 1);
    Lukk_Fil(문서);
    skrive_Fil_data(1, 인사말, sizeof(인사말) - 1);
    return lengde_VERDI == sizeof(인사말) - 1 ? 0 : 3;
}
