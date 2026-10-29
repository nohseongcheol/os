#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **اندراج_فہرست) {
    (void)개수; (void)اندراج_فہرست;
    int فائل_کا_نام = بنائیں_فائل("stored.txt", مطالعہ_تحریری | 없으면만들기 | 내용비우기, 0600);
    if (فائل_کا_نام < 0 || لکھیں_فائل_کوائف(فائل_کا_نام, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(فائل_کا_نام) < 0) return 2;
    if (بند_فائل(فائل_کا_نام) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
