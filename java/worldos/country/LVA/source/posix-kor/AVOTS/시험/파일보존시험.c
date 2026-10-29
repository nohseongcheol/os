#include <파일규약.h>
#include <stdio.h>
int main(int krājums_COUNT, char **ievade_Saraksts) {
    (void)krājums_COUNT; (void)ievade_Saraksts;
    int Fails = atvērt_Fails("stored.txt", 읽고쓰기 | 없으면만들기 | apraut_Satura_rādītājs, 0600);
    if (Fails < 0 || rakstīšana_Fails_dati(Fails, "saved-from-C", 12) != 12) return 1;
    if (izpilde_failu_krātuve(Fails) < 0) return 2;
    if (Aizvērt_Fails(Fails) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
