#include <파일규약.h>
#include <stdio.h>
int main(int kaup_COUNT, char **kirje_Loend) {
    (void)kaup_COUNT; (void)kirje_Loend;
    int Fail = avama_Fail("stored.txt", 읽고쓰기 | 없으면만들기 | lühendama_Sisu, 0600);
    if (Fail < 0 || kirjutamine_Fail_andmed(Fail, "saved-from-C", 12) != 12) return 1;
    if (kinnitamine_failisalvestusruum(Fail) < 0) return 2;
    if (Sule_Fail(Fail) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
