#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **എന്_ട്രി_ലിസ്റ്റ്) {
    (void)개수; (void)എന്_ട്രി_ലിസ്റ്റ്;
    int ഫയല് = തുറക്കുക_ഫയല്("stored.txt", വായനാ_റൈറ്റ് | 없으면만들기 | 내용비우기, 0600);
    if (ഫയല് < 0 || റൈറ്റ്_ചെയ്യുക_ഫയല്_ഡാറ്റാ(ഫയല്, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(ഫയല്) < 0) return 2;
    if (അടയ്ക്കുക_ഫയല്(ഫയല്) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
