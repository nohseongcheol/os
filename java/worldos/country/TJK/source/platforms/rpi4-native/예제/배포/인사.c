#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **аргумент_Рӯйхат) {
    if (인수개수 < 1 || !аргумент_Рӯйхат[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = кушодан_файл("인사.txt", хондан_навиштан | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 дарозӣ_қимат = навиштан_файл_иттилоот(문서, 인사말, sizeof(인사말) - 1);
    пӯшидан_файл(문서);
    навиштан_файл_иттилоот(1, 인사말, sizeof(인사말) - 1);
    return дарозӣ_қимат == sizeof(인사말) - 1 ? 0 : 3;
}
