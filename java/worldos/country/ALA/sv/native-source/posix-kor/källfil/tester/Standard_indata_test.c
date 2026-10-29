#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int objekt_ANTAL, char **post_ange) {
    (void)objekt_ANTAL; (void)post_ange;
    char data[6]; int längd_värde = 0;
    puts("POSIX INPUT READY");
    while (längd_värde < 6) {
        int RESULTAT = läsa_fil_data(0, data + längd_värde, 6 - längd_värde);
        if (RESULTAT <= 0) return 1;
        längd_värde += RESULTAT;
    }
    if (memcmp(data, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
