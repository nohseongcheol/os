#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int mír_COUNT, char **iontráil_Liosta) {
    (void)mír_COUNT; (void)iontráil_Liosta;
    char sonraí[6]; int fad_VALUE = 0;
    puts("POSIX INPUT READY");
    while (fad_VALUE < 6) {
        int tomhas = 파일자료읽기(0, sonraí + fad_VALUE, 6 - fad_VALUE);
        if (tomhas <= 0) return 1;
        fad_VALUE += tomhas;
    }
    if (memcmp(sonraí, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
