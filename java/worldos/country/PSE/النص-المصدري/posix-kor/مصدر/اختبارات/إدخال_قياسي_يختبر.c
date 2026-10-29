#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **إدخال_قائمة_f07b3200) {
    (void)개수; (void)إدخال_قائمة_f07b3200;
    char بيانات[6]; int 길이 = 0;
    puts("POSIX INPUT READY");
    while (길이 < 6) {
        int نتيجة = يقرأ_ملف_بيانات(0, بيانات + 길이, 6 - 길이);
        if (نتيجة <= 0) return 1;
        길이 += نتيجة;
    }
    if (memcmp(بيانات, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
