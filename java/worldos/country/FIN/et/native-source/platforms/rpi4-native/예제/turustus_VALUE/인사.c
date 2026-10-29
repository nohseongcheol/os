#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_Loend) {
    if (인수개수 < 1 || !argument_Loend[0]) return 2;
    const char 인사말[] = "oma 커널의 C와 Eesti POSIX\n";
    int 문서 = avama_Fail("인사.txt", 읽고쓰기 | 없으면만들기 | lühendama_Sisu, 0600);
    if (문서 < 0) return 1;
    입출력결과형 길이 = kirjutamine_Fail_andmed(문서, 인사말, sizeof(인사말) - 1);
    Sule_Fail(문서);
    kirjutamine_Fail_andmed(1, 인사말, sizeof(인사말) - 1);
    return 길이 == sizeof(인사말) - 1 ? 0 : 3;
}
