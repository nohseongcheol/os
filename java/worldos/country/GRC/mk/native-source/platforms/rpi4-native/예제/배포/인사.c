#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **аргумент_Список) {
    if (인수개수 < 1 || !аргумент_Список[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 Македонски POSIX\n";
    int 문서 = отвори_датотека("인사.txt", чита_пишува | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 должина_VALUE = запиши_датотека_податоци(문서, 인사말, sizeof(인사말) - 1);
    затвори_датотека(문서);
    запиши_датотека_податоци(1, 인사말, sizeof(인사말) - 1);
    return должина_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
