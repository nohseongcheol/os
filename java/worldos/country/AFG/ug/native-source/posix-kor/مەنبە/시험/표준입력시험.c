#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **كىرگۈزۈش_تىزىم) {
    (void)개수; (void)كىرگۈزۈش_تىزىم;
    char مەلۇمات[6]; int ئۇزۇنلۇق_قىممىتى = 0;
    puts("POSIX INPUT READY");
    while (ئۇزۇنلۇق_قىممىتى < 6) {
        int ئۆلچەم = 파일자료읽기(0, مەلۇمات + ئۇزۇنلۇق_قىممىتى, 6 - ئۇزۇنلۇق_قىممىتى);
        if (ئۆلچەم <= 0) return 1;
        ئۇزۇنلۇق_قىممىتى += ئۆلچەم;
    }
    if (memcmp(مەلۇمات, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
