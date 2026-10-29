#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ምእታው_ዝርዝር) {
    (void)개수; (void)ምእታው_ዝርዝር;
    int ፋይል = ክፈት_ፋይል("stored.txt", ኣንብብ_ጽሓፍ | 없으면만들기 | 내용비우기, 0600);
    if (ፋይል < 0 || ጸሓፍ_ፋይል_ሓበሬታ(ፋይል, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(ፋይል) < 0) return 2;
    if (ዕጸው_ፋይል(ፋይል) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
