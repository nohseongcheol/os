#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **аргумент_Жагсаалт) {
    if (인수개수 < 1 || !аргумент_Жагсаалт[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 Монгол POSIX\n";
    int 문서 = нээх_файл("인사.txt", унших_бичих | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 урт_утга = бичих_файл_өгөгдөл(문서, 인사말, sizeof(인사말) - 1);
    хаах_файл(문서);
    бичих_файл_өгөгдөл(1, 인사말, sizeof(인사말) - 1);
    return урт_утга == sizeof(인사말) - 1 ? 0 : 3;
}
