#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **киргизме_жазуу_Тизме) {
    (void)개수; (void)киргизме_жазуу_Тизме;
    char берилмелер[6]; int узундук_маани = 0;
    puts("POSIX INPUT READY");
    while (узундук_маани < 6) {
        int 결과 = 파일자료읽기(0, берилмелер + узундук_маани, 6 - узундук_маани);
        if (결과 <= 0) return 1;
        узундук_маани += 결과;
    }
    if (memcmp(берилмелер, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
