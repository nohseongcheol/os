#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ndebà_ndepụta) {
    (void)개수; (void)ndebà_ndepụta;
    int Faịlụ = mepee_ọbọakwụkwọ("stored.txt", gụọ_dèe | 없으면만들기 | 내용비우기, 0600);
    if (Faịlụ < 0 || dee_ọbọakwụkwọ_datà(Faịlụ, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Faịlụ) < 0) return 2;
    if (mmechi_ọbọakwụkwọ(Faịlụ) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
