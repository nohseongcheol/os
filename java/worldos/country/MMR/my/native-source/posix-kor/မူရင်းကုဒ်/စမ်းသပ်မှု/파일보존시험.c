#include <파일규약.h>
#include <stdio.h>
int main(int အရေအတွက်, char **အချက်စာရင်း) {
    (void)အရေအတွက်; (void)အချက်စာရင်း;
    int ဖိုင် = ဖိုင်ဖွင့်("stored.txt", ဖတ်ရေး | 없으면만들기 | 내용비우기, 0600);
    if (ဖိုင် < 0 || ဖိုင်ဒေတာရေး(ဖိုင်, "saved-from-C", 12) != 12) return 1;
    if (ဖိုင်သိုလှောင်အတည်ပြု(ဖိုင်) < 0) return 2;
    if (ဖိုင်ပိတ်(ဖိုင်) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
