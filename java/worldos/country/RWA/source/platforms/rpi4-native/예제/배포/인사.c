#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **ingingo_Urutonde) {
    if (인수개수 < 1 || !ingingo_Urutonde[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 Ikinyarwanda POSIX\n";
    int 문서 = kurema_dosiye("인사.txt", gusoma_kwandika | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 uburebure_agaciro = kwandika_dosiye_amakurushingiro(문서, 인사말, sizeof(인사말) - 1);
    gufunga_dosiye(문서);
    kwandika_dosiye_amakurushingiro(1, 인사말, sizeof(인사말) - 1);
    return uburebure_agaciro == sizeof(인사말) - 1 ? 0 : 3;
}
