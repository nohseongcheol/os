#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **аргумент_Исемлек) {
    if (인수개수 < 1 || !аргумент_Исемлек[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 Татарча POSIX\n";
    int 문서 = ачу_файл("인사.txt", укымалы_язмалы | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 озынлык_VALUE = язу_файл_мәгълүмат(문서, 인사말, sizeof(인사말) - 1);
    чик_файл(문서);
    язу_файл_мәгълүмат(1, 인사말, sizeof(인사말) - 1);
    return озынлык_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
