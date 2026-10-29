#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **аргумент_Тізім) {
    if (인수개수 < 1 || !аргумент_Тізім[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = ашу_файл("인사.txt", оқу_жазу | 없으면만들기 | қысқарту_Мазмұны, 0600);
    if (문서 < 0) return 1;
    입출력결과형 ұзындық_мән = жазу_файл_деректер(문서, 인사말, sizeof(인사말) - 1);
    Жабу_файл(문서);
    жазу_файл_деректер(1, 인사말, sizeof(인사말) - 1);
    return ұзындық_мән == sizeof(인사말) - 1 ? 0 : 3;
}
