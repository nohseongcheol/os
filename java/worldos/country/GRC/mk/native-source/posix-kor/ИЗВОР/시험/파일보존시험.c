#include <파일규약.h>
#include <stdio.h>
int main(int ставка_COUNT, char **внес_Список) {
    (void)ставка_COUNT; (void)внес_Список;
    int Датотека = отвори_датотека("stored.txt", чита_пишува | 없으면만들기 | 내용비우기, 0600);
    if (Датотека < 0 || запиши_датотека_податоци(Датотека, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Датотека) < 0) return 2;
    if (затвори_датотека(Датотека) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
