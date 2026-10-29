#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ଏଣ୍ଟ୍ରି_ତାଲିକା) {
    (void)개수; (void)ଏଣ୍ଟ୍ରି_ତାଲିକା;
    int ଫାଇଲ = ଖୋଲିବା_ଫାଇଲ୍("stored.txt", ପଢିବା_ଲେଖିବା | 없으면만들기 | 내용비우기, 0600);
    if (ଫାଇଲ < 0 || ଲିଖନ_ଫାଇଲ୍_ଡାଟା(ଫାଇଲ, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(ଫାଇଲ) < 0) return 2;
    if (ବନ୍ଦ_ଫାଇଲ୍(ଫାଇଲ) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
