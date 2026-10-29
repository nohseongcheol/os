#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **உள்ளீடு_பட்டியல்) {
    (void)개수; (void)உள்ளீடு_பட்டியல்;
    char தரவு[6]; int நீளம்_மதிப்பு = 0;
    puts("POSIX INPUT READY");
    while (நீளம்_மதிப்பு < 6) {
        int அளவிடக்கூடியது = 파일자료읽기(0, தரவு + நீளம்_மதிப்பு, 6 - நீளம்_மதிப்பு);
        if (அளவிடக்கூடியது <= 0) return 1;
        நீளம்_மதிப்பு += அளவிடக்கூடியது;
    }
    if (memcmp(தரவு, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
