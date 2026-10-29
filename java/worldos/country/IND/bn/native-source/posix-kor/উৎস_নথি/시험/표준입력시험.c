#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ভুক্তি_তালিকা) {
    (void)개수; (void)ভুক্তি_তালিকা;
    char ডাটা[6]; int দৈর্ঘ্য_মান = 0;
    puts("POSIX INPUT READY");
    while (দৈর্ঘ্য_মান < 6) {
        int পরিমাপ = 파일자료읽기(0, ডাটা + দৈর্ঘ্য_মান, 6 - দৈর্ঘ্য_মান);
        if (পরিমাপ <= 0) return 1;
        দৈর্ঘ্য_মান += পরিমাপ;
    }
    if (memcmp(ডাটা, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
