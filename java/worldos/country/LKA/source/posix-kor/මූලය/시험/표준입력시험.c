#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **පිවිසුම_ලැයිස්තුව) {
    (void)개수; (void)පිවිසුම_ලැයිස්තුව;
    char දත්ත[6]; int දිග_අගය = 0;
    puts("POSIX INPUT READY");
    while (දිග_අගය < 6) {
        int 결과 = 파일자료읽기(0, දත්ත + දිග_අගය, 6 - දිග_අගය);
        if (결과 <= 0) return 1;
        දිග_අගය += 결과;
    }
    if (memcmp(දත්ත, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
