#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argumen_Senarai) {
    if (인수개수 < 1 || !argumen_Senarai[0]) return 2;
    const char 인사말[] = "Asli 커널의 C와 Melayu POSIX\n";
    int 문서 = buka_fail("인사.txt", baca_tulis | 없으면만들기 | potong_TOC, 0600);
    if (문서 < 0) return 1;
    입출력결과형 kepanjangan_VALUE = tulis_fail_data(문서, 인사말, sizeof(인사말) - 1);
    Tutup_fail(문서);
    tulis_fail_data(1, 인사말, sizeof(인사말) - 1);
    return kepanjangan_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
