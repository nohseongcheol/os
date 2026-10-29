#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **შენატანი_სია) {
    (void)개수; (void)შენატანი_სია;
    int ფაილი = გახსნა_ფაილი("stored.txt", ჩაწერა_წაკითხვა | 없으면만들기 | 내용비우기, 0600);
    if (ფაილი < 0 || ჩაწერა_ფაილი_მონაცემები(ფაილი, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(ფაილი) < 0) return 2;
    if (დახურვა_ფაილი(ფაილი) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
