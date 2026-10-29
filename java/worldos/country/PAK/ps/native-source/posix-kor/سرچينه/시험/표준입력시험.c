#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **목록) {
    (void)개수; (void)목록;
    char اومتوک[6]; int اوږدوالى_ارزښت = 0;
    puts("POSIX INPUT READY");
    while (اوږدوالى_ارزښت < 6) {
        int 결과 = 파일자료읽기(0, اومتوک + اوږدوالى_ارزښت, 6 - اوږدوالى_ارزښت);
        if (결과 <= 0) return 1;
        اوږدوالى_ارزښت += 결과;
    }
    if (memcmp(اومتوک, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
