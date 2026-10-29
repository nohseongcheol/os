#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ערך_רשימה) {
    (void)개수; (void)ערך_רשימה;
    int קובץ = פתח_קובץ("stored.txt", קריאה_כתיבה | 없으면만들기 | 내용비우기, 0600);
    if (קובץ < 0 || כתיבה_קובץ_נתונים(קובץ, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(קובץ) < 0) return 2;
    if (סגור_קובץ(קובץ) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
