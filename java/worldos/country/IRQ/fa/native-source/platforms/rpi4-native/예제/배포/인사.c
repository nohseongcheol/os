#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **آرگومان_لیست) {
    if (인수개수 < 1 || !آرگومان_لیست[0]) return 2;
    const char 인사말[] = "بومی 커널의 C와 فارسی POSIX\n";
    int 문서 = ایجاد_فایل("인사.txt", خواندن_نوشتن | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 طول_مقدار = نوشتن_فایل_داده_ها(문서, 인사말, sizeof(인사말) - 1);
    بستن_فایل(문서);
    نوشتن_فایل_داده_ها(1, 인사말, sizeof(인사말) - 1);
    return طول_مقدار == sizeof(인사말) - 1 ? 0 : 3;
}
