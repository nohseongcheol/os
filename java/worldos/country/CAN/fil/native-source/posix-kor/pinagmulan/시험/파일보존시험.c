#include <파일규약.h>
#include <stdio.h>
int main(int item_COUNT, char **pagpasok_list) {
    (void)item_COUNT; (void)pagpasok_list;
    int file = buksan_file("stored.txt", nababasa_nasusulatan | 없으면만들기 | 내용비우기, 0600);
    if (file < 0 || sumulat_file_data(file, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(file) < 0) return 2;
    if (isara_file(file) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
