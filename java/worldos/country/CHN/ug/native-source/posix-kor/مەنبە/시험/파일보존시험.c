#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **كىرگۈزۈش_تىزىم) {
    (void)개수; (void)كىرگۈزۈش_تىزىم;
    int ھۆججەت = قۇرۇش_ھۆججەت("stored.txt", ئوقۇش_يېزىش | 없으면만들기 | 내용비우기, 0600);
    if (ھۆججەت < 0 || يازماق_ھۆججەت_مەلۇمات(ھۆججەت, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(ھۆججەت) < 0) return 2;
    if (ئاياغ_ھۆججەت(ھۆججەت) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
