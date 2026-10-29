#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argumen_Daftar) {
    if (인수개수 < 1 || !argumen_Daftar[0]) return 2;
    const char 인사말[] = "Asli 커널의 C와 Indonesia POSIX\n";
    int 문서 = buat_file("인사.txt", baca_tulis | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 panjang_VALUE = tulis_file_data(문서, 인사말, sizeof(인사말) - 1);
    Tutup_file(문서);
    tulis_file_data(1, 인사말, sizeof(인사말) - 1);
    return panjang_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
