#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int element_COUNT, char **vnos_Seznam) {
    (void)element_COUNT; (void)vnos_Seznam;
    char podatki[6]; int 길이 = 0;
    puts("POSIX INPUT READY");
    while (길이 < 6) {
        int REZULTAT = 파일자료읽기(0, podatki + 길이, 6 - 길이);
        if (REZULTAT <= 0) return 1;
        길이 += REZULTAT;
    }
    if (memcmp(podatki, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
