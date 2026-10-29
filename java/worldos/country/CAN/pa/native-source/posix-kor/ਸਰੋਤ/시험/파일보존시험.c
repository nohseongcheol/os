#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ਦਾਖਲਾ_ਸੂਚੀ) {
    (void)개수; (void)ਦਾਖਲਾ_ਸੂਚੀ;
    int ਫਾਇਲ = ਖੋਲੋ_ਲਿਖਤ_ਪੱਤਰ("stored.txt", ਪੜ੍ਹਨ_ਲਿਖਣ | 없으면만들기 | 내용비우기, 0600);
    if (ਫਾਇਲ < 0 || ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ_ਸਮੱਗਰੀ(ਫਾਇਲ, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(ਫਾਇਲ) < 0) return 2;
    if (ਬੰਦ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ(ਫਾਇਲ) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
