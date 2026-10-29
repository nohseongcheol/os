#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **аргумент_Листа) {
    if (인수개수 < 1 || !аргумент_Листа[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = креирати_фајл("인사.txt", за_читање_писање | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 дужина_вриједност = писати_фајл_подаци(문서, 인사말, sizeof(인사말) - 1);
    затварање_фајл(문서);
    писати_фајл_подаци(1, 인사말, sizeof(인사말) - 1);
    return дужина_вриједност == sizeof(인사말) - 1 ? 0 : 3;
}
