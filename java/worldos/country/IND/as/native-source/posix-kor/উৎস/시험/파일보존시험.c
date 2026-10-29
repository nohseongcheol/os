#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **প্রবিষ্ট_সূচী) {
    (void)개수; (void)প্রবিষ্ট_সূচী;
    int নথিপত্ৰ = খোলক_ফাইল("stored.txt", পঢ়িব_লিখিব_পৰা | 없으면만들기 | 내용비우기, 0600);
    if (নথিপত্ৰ < 0 || লিখক_ফাইল_ডাটা(নথিপত্ৰ, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(নথিপত্ৰ) < 0) return 2;
    if (বন্ধ_কৰক_ফাইল(নথিপত্ৰ) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
