#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **შენატანი_სია) {
    (void)개수; (void)შენატანი_სია;
    char მონაცემები[6]; int სიგრძე_მნიშვნელობა = 0;
    puts("POSIX INPUT READY");
    while (სიგრძე_მნიშვნელობა < 6) {
        int გაზომვა = 파일자료읽기(0, მონაცემები + სიგრძე_მნიშვნელობა, 6 - სიგრძე_მნიშვნელობა);
        if (გაზომვა <= 0) return 1;
        სიგრძე_მნიშვნელობა += გაზომვა;
    }
    if (memcmp(მონაცემები, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
