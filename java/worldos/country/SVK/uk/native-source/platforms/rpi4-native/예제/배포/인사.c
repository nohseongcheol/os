#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **аргумент_список) {
    if (인수개수 < 1 || !аргумент_список[0]) return 2;
    const char 인사말[] = "своє 커널의 C와 українська POSIX\n";
    int 문서 = відкрито_Файл("인사.txt", 읽고쓰기 | 없으면만들기 | скорочувати_Зміст, 0600);
    if (문서 < 0) return 1;
    입출력결과형 길이 = записування_Файл_дані(문서, 인사말, sizeof(인사말) - 1);
    Закрити_Файл(문서);
    записування_Файл_дані(1, 인사말, sizeof(인사말) - 1);
    return 길이 == sizeof(인사말) - 1 ? 0 : 3;
}
