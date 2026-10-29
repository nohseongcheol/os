#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **մուտքագրում_Ցուցակ) {
    (void)개수; (void)մուտքագրում_Ցուցակ;
    char տվյալ[6]; int տեւողություն_արժեք = 0;
    puts("POSIX INPUT READY");
    while (տեւողություն_արժեք < 6) {
        int չափ = 파일자료읽기(0, տվյալ + տեւողություն_արժեք, 6 - տեւողություն_արժեք);
        if (չափ <= 0) return 1;
        տեւողություն_արժեք += չափ;
    }
    if (memcmp(տվյալ, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
