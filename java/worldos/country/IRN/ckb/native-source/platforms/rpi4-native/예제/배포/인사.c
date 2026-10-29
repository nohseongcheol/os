#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **ئارگیومێنت_لیست) {
    if (인수개수 < 1 || !ئارگیومێنت_لیست[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = کردنەوە_فایل("인사.txt", خوێندن_نووسین | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 درێژی_نرخ = ڕایت_کردن_فایل_دەیتا(문서, 인사말, sizeof(인사말) - 1);
    داخستن_فایل(문서);
    ڕایت_کردن_فایل_دەیتا(1, 인사말, sizeof(인사말) - 1);
    return درێژی_نرخ == sizeof(인사말) - 1 ? 0 : 3;
}
