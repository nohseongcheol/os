#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **دليل_فهرست) {
    if (인수개수 < 1 || !دليل_فهرست[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = ٺاھيو_فائل("인사.txt", پڙهڻ_لکڻ | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 لمبائي_قدر = لکو_فائل_ڪوائف(문서, 인사말, sizeof(인사말) - 1);
    بند_ڪرڻ_فائل(문서);
    لکو_فائل_ڪوائف(1, 인사말, sizeof(인사말) - 1);
    return لمبائي_قدر == sizeof(인사말) - 1 ? 0 : 3;
}
