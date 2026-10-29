#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ভুক্তি_তালিকা) {
    (void)개수; (void)ভুক্তি_তালিকা;
    int নথির_নাম = খোলা_ফাইল("stored.txt", পঠন_লিখন | 없으면만들기 | 내용비우기, 0600);
    if (নথির_নাম < 0 || লেখা_ফাইল_ডাটা(নথির_নাম, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(নথির_নাম) < 0) return 2;
    if (বন্ধ_ফাইল(নথির_নাম) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
