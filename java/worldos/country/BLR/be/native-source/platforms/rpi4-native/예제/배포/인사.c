#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **аргумент_Спіс) {
    if (인수개수 < 1 || !аргумент_Спіс[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = адкрыць_файл("인사.txt", для_чытання_для_запісу | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 даўжыня_значэнне = напісаць_файл_дадзеныя(문서, 인사말, sizeof(인사말) - 1);
    закрыць_файл(문서);
    напісаць_файл_дадзеныя(1, 인사말, sizeof(인사말) - 1);
    return даўжыня_значэнне == sizeof(인사말) - 1 ? 0 : 3;
}
