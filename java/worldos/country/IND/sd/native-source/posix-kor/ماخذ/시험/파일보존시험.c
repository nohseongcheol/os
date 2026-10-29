#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **داخلا_فهرست) {
    (void)개수; (void)داخلا_فهرست;
    int فائل = ٺاھيو_فائل("stored.txt", پڙهڻ_لکڻ | 없으면만들기 | 내용비우기, 0600);
    if (فائل < 0 || لکو_فائل_ڪوائف(فائل, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(فائل) < 0) return 2;
    if (بند_ڪرڻ_فائل(فائل) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
