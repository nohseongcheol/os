#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ورودی_لیست) {
    (void)개수; (void)ورودی_لیست;
    int پرونده = ایجاد_فایل("stored.txt", خواندن_نوشتن | 없으면만들기 | 내용비우기, 0600);
    if (پرونده < 0 || نوشتن_فایل_داده_ها(پرونده, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(پرونده) < 0) return 2;
    if (بستن_فایل(پرونده) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
