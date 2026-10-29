#include <파일규약.h>
#include <stdio.h>
int main(int mír_COUNT, char **iontráil_Liosta) {
    (void)mír_COUNT; (void)iontráil_Liosta;
    int Comhad = oscail_comhad("stored.txt", inléite_inscríofa | 없으면만들기 | 내용비우기, 0600);
    if (Comhad < 0 || scríobh_comhad_sonraí(Comhad, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Comhad) < 0) return 2;
    if (dún_comhad(Comhad) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
