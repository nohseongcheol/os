#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ನಮೂದು_ಪಟ್ಟಿ) {
    (void)개수; (void)ನಮೂದು_ಪಟ್ಟಿ;
    int ಕಡತ = ರಚಿಸು_ಫೈಲ್("stored.txt", ಓದು_ಬರೆ | 없으면만들기 | 내용비우기, 0600);
    if (ಕಡತ < 0 || ಬರೆ_ಫೈಲ್_ಡೇಟಾ(ಕಡತ, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(ಕಡತ) < 0) return 2;
    if (ಮುಚ್ಚು_ಫೈಲ್(ಕಡತ) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
