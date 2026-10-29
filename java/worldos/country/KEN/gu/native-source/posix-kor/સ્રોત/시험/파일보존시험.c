#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **પ્રવેશ_સૂચી) {
    (void)개수; (void)પ્રવેશ_સૂચી;
    int ફાઈલ = બનાવો_ફાઇલ("stored.txt", વાંચન_લેખન | 없으면만들기 | 내용비우기, 0600);
    if (ફાઈલ < 0 || લખો_ફાઇલ_ડેટા(ફાઈલ, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(ફાઈલ) < 0) return 2;
    if (બંધ_કરો_ફાઇલ(ફાઈલ) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
