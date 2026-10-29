#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argumento_list) {
    if (인수개수 < 1 || !argumento_list[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = buksan_file("인사.txt", nababasa_nasusulatan | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 haba_VALUE = sumulat_file_data(문서, 인사말, sizeof(인사말) - 1);
    isara_file(문서);
    sumulat_file_data(1, 인사말, sizeof(인사말) - 1);
    return haba_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
