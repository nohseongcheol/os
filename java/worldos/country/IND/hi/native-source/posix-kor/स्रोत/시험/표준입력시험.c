#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **एन्ट्री_सूची) {
    (void)개수; (void)एन्ट्री_सूची;
    char आँकड़े[6]; int 길이 = 0;
    puts("POSIX INPUT READY");
    while (길이 < 6) {
        int परिणाम = पढें_फ़ाइल_डेटा(0, आँकड़े + 길이, 6 - 길이);
        if (परिणाम <= 0) return 1;
        길이 += परिणाम;
    }
    if (memcmp(आँकड़े, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
