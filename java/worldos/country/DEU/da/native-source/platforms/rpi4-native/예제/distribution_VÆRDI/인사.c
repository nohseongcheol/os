#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_Liste) {
    if (인수개수 < 1 || !argument_Liste[0]) return 2;
    const char 인사말[] = "eget 커널의 C와 Dansk POSIX\n";
    int 문서 = åben_fil("인사.txt", læse_skrive | 없으면만들기 | afkorte_Indhold, 0600);
    if (문서 < 0) return 1;
    입출력결과형 varighed_VÆRDI = skrive_fil_data(문서, 인사말, sizeof(인사말) - 1);
    Luk_fil(문서);
    skrive_fil_data(1, 인사말, sizeof(인사말) - 1);
    return varighed_VÆRDI == sizeof(인사말) - 1 ? 0 : 3;
}
