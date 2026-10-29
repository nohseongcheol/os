#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **تێنووسین_لیست) {
    (void)개수; (void)تێنووسین_لیست;
    int فایل = کردنەوە_فایل("stored.txt", خوێندن_نووسین | 없으면만들기 | 내용비우기, 0600);
    if (فایل < 0 || ڕایت_کردن_فایل_دەیتا(فایل, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(فایل) < 0) return 2;
    if (داخستن_فایل(فایل) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
