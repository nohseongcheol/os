#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ನಮೂದು_ಪಟ್ಟಿ) {
    (void)개수; (void)ನಮೂದು_ಪಟ್ಟಿ;
    char ಡೇಟಾ[6]; int ಉದ್ದ_ಮೌಲ್ಯ = 0;
    puts("POSIX INPUT READY");
    while (ಉದ್ದ_ಮೌಲ್ಯ < 6) {
        int ಮಾಪನ = 파일자료읽기(0, ಡೇಟಾ + ಉದ್ದ_ಮೌಲ್ಯ, 6 - ಉದ್ದ_ಮೌಲ್ಯ);
        if (ಮಾಪನ <= 0) return 1;
        ಉದ್ದ_ಮೌಲ್ಯ += ಮಾಪನ;
    }
    if (memcmp(ಡೇಟಾ, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
