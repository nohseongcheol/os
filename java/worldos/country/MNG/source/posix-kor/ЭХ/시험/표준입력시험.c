#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **оролт_Жагсаалт) {
    (void)개수; (void)оролт_Жагсаалт;
    char өгөгдөл[6]; int урт_утга = 0;
    puts("POSIX INPUT READY");
    while (урт_утга < 6) {
        int 결과 = 파일자료읽기(0, өгөгдөл + урт_утга, 6 - урт_утга);
        if (결과 <= 0) return 1;
        урт_утга += 결과;
    }
    if (memcmp(өгөгдөл, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
