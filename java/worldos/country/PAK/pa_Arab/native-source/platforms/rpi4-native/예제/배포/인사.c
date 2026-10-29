#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **دلیل_فرست) {
    if (인수개수 < 1 || !دلیل_فرست[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = بنڑاؤ_فائل("인사.txt", پڑھو_لکھو | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 لمبائی_قدر = لکھو_فائل_کوائف(문서, 인사말, sizeof(인사말) - 1);
    بند_کرو_فائل(문서);
    لکھو_فائل_کوائف(1, 인사말, sizeof(인사말) - 1);
    return لمبائی_قدر == sizeof(인사말) - 1 ? 0 : 3;
}
