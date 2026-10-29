#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ምዝግብ_ዝርዝር) {
    (void)개수; (void)ምዝግብ_ዝርዝር;
    int ፋይል = ክፈት_ፋይል("stored.txt", ተነባቢ_የሚጻፍበት | 없으면만들기 | 내용비우기, 0600);
    if (ፋይል < 0 || ጻፍ_ፋይል_ውሂብ(ፋይል, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(ፋይል) < 0) return 2;
    if (ዝጋ_ፋይል(ፋይል) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
