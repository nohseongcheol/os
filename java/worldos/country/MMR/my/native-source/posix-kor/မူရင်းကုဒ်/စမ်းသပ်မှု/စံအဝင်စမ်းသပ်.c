#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int အရေအတွက်, char **အချက်စာရင်း) {
    (void)အရေအတွက်; (void)အချက်စာရင်း;
    char ဒေတာ[6]; int အလျား = 0;
    puts("POSIX INPUT READY");
    while (အလျား < 6) {
        int ရလဒ် = ဖိုင်ဒေတာဖတ်(0, ဒေတာ + အလျား, 6 - အလျား);
        if (ရလဒ် <= 0) return 1;
        အလျား += ရလဒ်;
    }
    if (memcmp(ဒေတာ, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
