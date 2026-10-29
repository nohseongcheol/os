#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **καταχώρηση_Λίστα) {
    (void)개수; (void)καταχώρηση_Λίστα;
    int Αρχείο = ανοίγω_Αρχείο("stored.txt", 읽고쓰기 | 없으면만들기 | περικοπή_Περιεχόμενα, 0600);
    if (Αρχείο < 0 || εγγράφω_Αρχείο_δεδομένα(Αρχείο, "saved-from-C", 12) != 12) return 1;
    if (δέσμευση_Αρχεία(Αρχείο) < 0) return 2;
    if (κλείνω_Αρχείο(Αρχείο) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
