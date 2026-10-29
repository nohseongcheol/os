#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ምዝግብ_ዝርዝር) {
    (void)개수; (void)ምዝግብ_ዝርዝር;
    char ውሂብ[6]; int ርዝመት_እሴት = 0;
    puts("POSIX INPUT READY");
    while (ርዝመት_እሴት < 6) {
        int ልኬት = 파일자료읽기(0, ውሂብ + ርዝመት_እሴት, 6 - ርዝመት_እሴት);
        if (ልኬት <= 0) return 1;
        ርዝመት_እሴት += ልኬት;
    }
    if (memcmp(ውሂብ, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
