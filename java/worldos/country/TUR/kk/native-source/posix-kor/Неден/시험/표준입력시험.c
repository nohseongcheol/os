#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **енгізу_Тізім) {
    (void)개수; (void)енгізу_Тізім;
    char деректер[6]; int ұзындық_мән = 0;
    puts("POSIX INPUT READY");
    while (ұзындық_мән < 6) {
        int НӘТИЖЕ = 파일자료읽기(0, деректер + ұзындық_мән, 6 - ұзындық_мән);
        if (НӘТИЖЕ <= 0) return 1;
        ұзындық_мән += НӘТИЖЕ;
    }
    if (memcmp(деректер, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
