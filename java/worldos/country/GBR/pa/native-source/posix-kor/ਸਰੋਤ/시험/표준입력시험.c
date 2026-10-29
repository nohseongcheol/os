#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ਦਾਖਲਾ_ਸੂਚੀ) {
    (void)개수; (void)ਦਾਖਲਾ_ਸੂਚੀ;
    char ਸਮੱਗਰੀ[6]; int ਲੰਬਾਈ_ਕੀਮਤ = 0;
    puts("POSIX INPUT READY");
    while (ਲੰਬਾਈ_ਕੀਮਤ < 6) {
        int ਮਾਪ = 파일자료읽기(0, ਸਮੱਗਰੀ + ਲੰਬਾਈ_ਕੀਮਤ, 6 - ਲੰਬਾਈ_ਕੀਮਤ);
        if (ਮਾਪ <= 0) return 1;
        ਲੰਬਾਈ_ਕੀਮਤ += ਮਾਪ;
    }
    if (memcmp(ਸਮੱਗਰੀ, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
