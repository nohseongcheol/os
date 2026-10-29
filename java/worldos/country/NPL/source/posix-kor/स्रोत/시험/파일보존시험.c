#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **प्रविष्टि_सूची) {
    (void)개수; (void)प्रविष्टि_सूची;
    int फाइल = सिर्जना_फाइल("stored.txt", पढ्न_लेख्_न | 없으면만들기 | 내용비우기, 0600);
    if (फाइल < 0 || लेख्नुहोस्_फाइल_लगत(फाइल, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(फाइल) < 0) return 2;
    if (बन्द_गर्नुहोस्_फाइल(फाइल) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
