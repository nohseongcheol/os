#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ଏଣ୍ଟ୍ରି_ତାଲିକା) {
    (void)개수; (void)ଏଣ୍ଟ୍ରି_ତାଲିକା;
    char ଡାଟା[6]; int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = 0;
    puts("POSIX INPUT READY");
    while (ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ < 6) {
        int ମାପ = 파일자료읽기(0, ଡାଟା + ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ, 6 - ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ);
        if (ମାପ <= 0) return 1;
        ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ += ମାପ;
    }
    if (memcmp(ଡାଟା, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
