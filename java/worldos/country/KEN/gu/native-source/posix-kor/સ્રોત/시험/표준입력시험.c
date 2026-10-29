#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **પ્રવેશ_સૂચી) {
    (void)개수; (void)પ્રવેશ_સૂચી;
    char ડેટા[6]; int લંબાઈ_મૂલ્ય = 0;
    puts("POSIX INPUT READY");
    while (લંબાઈ_મૂલ્ય < 6) {
        int પરિમાણ = 파일자료읽기(0, ડેટા + લંબાઈ_મૂલ્ય, 6 - લંબાઈ_મૂલ્ય);
        if (પરિમાણ <= 0) return 1;
        લંબાઈ_મૂલ્ય += પરિમાણ;
    }
    if (memcmp(ડેટા, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
