#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **аргумент_Списък) {
    if (인수개수 < 1 || !аргумент_Списък[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 Български POSIX\n";
    int 문서 = отварям_Файл("인사.txt", 읽고쓰기 | 없으면만들기 | съкращавам_Съдържание, 0600);
    if (문서 < 0) return 1;
    입출력결과형 길이 = записване_Файл_данни(문서, 인사말, sizeof(인사말) - 1);
    затварям_Файл(문서);
    записване_Файл_данни(1, 인사말, sizeof(인사말) - 1);
    return 길이 == sizeof(인사말) - 1 ? 0 : 3;
}
