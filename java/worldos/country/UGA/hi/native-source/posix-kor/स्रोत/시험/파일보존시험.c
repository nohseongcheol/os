#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **एन्ट्री_सूची) {
    (void)개수; (void)एन्ट्री_सूची;
    int संचिका = जारी_फ़ाइल("stored.txt", पठन_लेखन | 없으면만들기 | कम_करें_सामग्री, 0600);
    if (संचिका < 0 || लिखना_फ़ाइल_डेटा(संचिका, "saved-from-C", 12) != 12) return 1;
    if (कमिट_फ़ाइल_संग्रहण(संचिका) < 0) return 2;
    if (बंद_फ़ाइल(संचिका) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
