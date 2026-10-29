#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **وسيطة_قائمة) {
    if (인수개수 < 1 || !وسيطة_قائمة[0]) return 2;
    const char 인사말[] = "ذاتي 커널의 C와 العربية POSIX\n";
    int 문서 = فتح_ملف("인사.txt", مقروء_مكتوب | 없으면만들기 | يقتطع_المحتويات, 0600);
    if (문서 < 0) return 1;
    입출력결과형 길이 = كتابة_ملف_بيانات(문서, 인사말, sizeof(인사말) - 1);
    يغلق_ملف(문서);
    كتابة_ملف_بيانات(1, 인사말, sizeof(인사말) - 1);
    return 길이 == sizeof(인사말) - 1 ? 0 : 3;
}
