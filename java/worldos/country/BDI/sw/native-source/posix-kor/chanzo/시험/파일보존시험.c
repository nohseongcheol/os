#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ingizo_Orodha) {
    (void)개수; (void)ingizo_Orodha;
    int faili = unda_faili("stored.txt", soma_andika | 없으면만들기 | 내용비우기, 0600);
    if (faili < 0 || andika_faili_data(faili, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(faili) < 0) return 2;
    if (funga_faili(faili) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
