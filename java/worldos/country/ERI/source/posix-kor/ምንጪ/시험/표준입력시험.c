#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ምእታው_ዝርዝር) {
    (void)개수; (void)ምእታው_ዝርዝር;
    char ሓበሬታ[6]; int ንውሓት_ዋጋ = 0;
    puts("POSIX INPUT READY");
    while (ንውሓት_ዋጋ < 6) {
        int 결과 = 파일자료읽기(0, ሓበሬታ + ንውሓት_ዋጋ, 6 - ንውሓት_ዋጋ);
        if (결과 <= 0) return 1;
        ንውሓት_ዋጋ += 결과;
    }
    if (memcmp(ሓበሬታ, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
