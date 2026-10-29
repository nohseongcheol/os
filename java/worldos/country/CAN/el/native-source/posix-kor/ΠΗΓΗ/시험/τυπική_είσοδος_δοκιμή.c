#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **καταχώρηση_Λίστα) {
    (void)개수; (void)καταχώρηση_Λίστα;
    char δεδομένα[6]; int διάρκεια_τιμή = 0;
    puts("POSIX INPUT READY");
    while (διάρκεια_τιμή < 6) {
        int μέτρηση = 파일자료읽기(0, δεδομένα + διάρκεια_τιμή, 6 - διάρκεια_τιμή);
        if (μέτρηση <= 0) return 1;
        διάρκεια_τιμή += μέτρηση;
    }
    if (memcmp(δεδομένα, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
