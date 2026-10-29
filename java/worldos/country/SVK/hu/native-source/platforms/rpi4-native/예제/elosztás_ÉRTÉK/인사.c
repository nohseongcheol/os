#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argumentum_Lista) {
    if (인수개수 < 1 || !argumentum_Lista[0]) return 2;
    const char 인사말[] = "saját 커널의 C와 magyar POSIX\n";
    int 문서 = készít_Fájl("인사.txt", 읽고쓰기 | 없으면만들기 | vág_Tartalom, 0600);
    if (문서 < 0) return 1;
    입출력결과형 hossz_ÉRTÉK = ír_Fájl_adat(문서, 인사말, sizeof(인사말) - 1);
    bezár_Fájl(문서);
    ír_Fájl_adat(1, 인사말, sizeof(인사말) - 1);
    return hossz_ÉRTÉK == sizeof(인사말) - 1 ? 0 : 3;
}
