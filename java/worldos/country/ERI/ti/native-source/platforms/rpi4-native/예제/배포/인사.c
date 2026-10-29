#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **ሓባሪ_ቁጽሪ_ዝርዝር) {
    if (인수개수 < 1 || !ሓባሪ_ቁጽሪ_ዝርዝር[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 ትግርኛ POSIX\n";
    int 문서 = ክፈት_ፋይል("인사.txt", ኣንብብ_ጽሓፍ | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 ንውሓት_ዋጋ = ጸሓፍ_ፋይል_ሓበሬታ(문서, 인사말, sizeof(인사말) - 1);
    ዕጸው_ፋይል(문서);
    ጸሓፍ_ፋይል_ሓበሬታ(1, 인사말, sizeof(인사말) - 1);
    return ንውሓት_ዋጋ == sizeof(인사말) - 1 ? 0 : 3;
}
