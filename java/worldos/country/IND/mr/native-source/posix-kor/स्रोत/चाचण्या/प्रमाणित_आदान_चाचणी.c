#include <संचिका_द्विमानजोडणी.h>
#include <stdio.h>
#include <string.h>
int main(int आयटम_संख्या, char **प्रविष्टी_यादी) {
    (void)आयटम_संख्या; (void)प्रविष्टी_यादी;
    char डेटा[6]; int लांबी_मूल्य = 0;
    puts("POSIX INPUT READY");
    while (लांबी_मूल्य < 6) {
        int मोजमाप = संचिका_डेटा_वाचा(0, डेटा + लांबी_मूल्य, 6 - लांबी_मूल्य);
        if (मोजमाप <= 0) return 1;
        लांबी_मूल्य += मोजमाप;
    }
    if (memcmp(डेटा, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
