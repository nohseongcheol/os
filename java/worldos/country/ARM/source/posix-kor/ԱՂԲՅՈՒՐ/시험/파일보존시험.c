#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **մուտքագրում_Ցուցակ) {
    (void)개수; (void)մուտքագրում_Ցուցակ;
    int Ֆայլ = բացել_նիշք("stored.txt", կարդալ_գրել | 없으면만들기 | 내용비우기, 0600);
    if (Ֆայլ < 0 || գրել_նիշք_տվյալ(Ֆայլ, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Ֆայլ) < 0) return 2;
    if (փակել_նիշք(Ֆայլ) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
