#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **تێنووسین_لیست) {
    (void)개수; (void)تێنووسین_لیست;
    char دەیتا[6]; int درێژی_نرخ = 0;
    puts("POSIX INPUT READY");
    while (درێژی_نرخ < 6) {
        int 결과 = 파일자료읽기(0, دەیتا + درێژی_نرخ, 6 - درێژی_نرخ);
        if (결과 <= 0) return 1;
        درێژی_نرخ += 결과;
    }
    if (memcmp(دەیتا, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
