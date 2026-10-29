#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **എന്_ട്രി_ലിസ്റ്റ്) {
    (void)개수; (void)എന്_ട്രി_ലിസ്റ്റ്;
    char ഡാറ്റാ[6]; int ദൈര്_ഘ്യം_മൂല്യം = 0;
    puts("POSIX INPUT READY");
    while (ദൈര്_ഘ്യം_മൂല്യം < 6) {
        int അളവ് = 파일자료읽기(0, ഡാറ്റാ + ദൈര്_ഘ്യം_മൂല്യം, 6 - ദൈര്_ഘ്യം_മൂല്യം);
        if (അളവ് <= 0) return 1;
        ദൈര്_ഘ്യം_മൂല്യം += അളവ്;
    }
    if (memcmp(ഡാറ്റാ, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
