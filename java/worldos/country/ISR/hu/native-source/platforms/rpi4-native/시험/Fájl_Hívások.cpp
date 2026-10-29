#include "../명명/기계연결이름.h"
#include "파일규약.h"
// 표준 C++ kódtár 없는 freestanding C++11 app_f5044b9b. 커널에 statikus_ÉRTÉK 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char Tartalom_ÉRTÉK[] = "C++ → Java kernel_ÉRTÉK · 한글 😀";
    unsigned char 읽은값[sizeof(Tartalom_ÉRTÉK)] = {};
    int Fájl = készít_Fájl("시험.txt", 읽고쓰기 | 없으면만들기 | vág_Tartalom, 0600);
    if (Fájl < 0) return 1;
    if (ír_Fájl_adat(Fájl, Tartalom_ÉRTÉK, sizeof(Tartalom_ÉRTÉK)) != sizeof(Tartalom_ÉRTÉK)) return 2;
    if (keres_Fájl(Fájl, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(Fájl, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(Tartalom_ÉRTÉK); 순번++) if (읽은값[순번] != (unsigned char)Tartalom_ÉRTÉK[순번]) return 5;
    if (파일자료읽기(Fájl, 읽은값, 1) != 0) return 6;
    if (véglegesít_Files(Fájl) != -1 || hibaszám != 38) return 7;
    if (bezár_Fájl(Fájl) || bezár_Fájl(Fájl) != -1 || hibaszám != 9) return 8;
    Fájl = készít_Fájl("시험.txt", írásvédett_ÉRTÉK);
    if (Fájl < 0 || ír_Fájl_adat(Fájl, Tartalom_ÉRTÉK, 1) != -1 || hibaszám != 9) return 9;
    if (bezár_Fájl(Fájl)) return 10;
    Fájl = készít_Fájl("시험.txt", 읽고쓰기 | 끝에이어쓰기);
    if (Fájl < 0 || keres_Fájl(Fájl, 0, 처음기준) != 0 || ír_Fájl_adat(Fájl, "!", 1) != 1 || fájlméret(Fájl) != sizeof(Tartalom_ÉRTÉK) + 1) return 11;
    if (halmaz_Fájl_hossz(Fájl, 2) || keres_Fájl(Fájl, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (ír_Fájl_adat(Fájl, "x", 1) != 1 || fájlméret(Fájl) != 3 || bezár_Fájl(Fájl)) return 13;
    Fájl = készít_Fájl("구멍.bin", 읽고쓰기 | 없으면만들기 | vág_Tartalom, 0600);
    if (Fájl < 0 || keres_Fájl(Fájl, 3, 처음기준) != 3 || ír_Fájl_adat(Fájl, "z", 1) != 1) return 14;
    if (keres_Fájl(Fájl, 0, 처음기준) != 0 || 파일자료읽기(Fájl, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (eltávolít_Fájl_bejegyzés_név("구멍.bin") || fájlméret(Fájl) != 4 || bezár_Fájl(Fájl)) return 16;
    if (készít_Fájl("구멍.bin", írásvédett_ÉRTÉK) != -1 || hibaszám != 2) return 17;
    if (készít_Fájl("시험.txt", 읽고쓰기 | 새파일만들기, 0600) != -1 || hibaszám != 17) return 18;
    if (készít_Fájl("../금지", írásvédett_ÉRTÉK) != -1) return 19;
    return 0;
}
