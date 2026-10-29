#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **පිවිසුම_ලැයිස්තුව) {
    (void)개수; (void)පිවිසුම_ලැයිස්තුව;
    int ගොනු = සාදන්න_ගොනුව("stored.txt", කියවීම්_ලිවීම් | 없으면만들기 | 내용비우기, 0600);
    if (ගොනු < 0 || ලියන්න_ගොනුව_දත්ත(ගොනු, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(ගොනු) < 0) return 2;
    if (වසන්න_ගොනුව(ගොනු) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
