#include <파일규약.h>
#include <stdio.h>
int main(int vara_COUNT, char **færsla_Listi) {
    (void)vara_COUNT; (void)færsla_Listi;
    int Skrá = opið_skrá("stored.txt", les_skrifheimild | 없으면만들기 | 내용비우기, 0600);
    if (Skrá < 0 || skrifa_skrá_gögn(Skrá, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Skrá) < 0) return 2;
    if (loka_skrá(Skrá) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
