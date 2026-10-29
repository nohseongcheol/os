#include "통신규약.h"

int START_felhasználó_app(int Argumentumok) {
    (void)Argumentumok;
    struct háló_szoftvercsatorna_CÍM CÍM = {0};
    CÍM.CÍM_Család = háló_Család;
    CÍM.portszám = 망차례짧은수(9260);
    CÍM.internetcím.CÍM_ÉRTÉK = hálózat_egész_szám(visszacsatolási_cím);
    int kiszolgáló_ÉRTÉK = készít_végpont(háló_Család, Stream_hálózat, Stream_átviteli_protokoll);
    if (kiszolgáló_ÉRTÉK < 0 || BIND_CÍM(kiszolgáló_ÉRTÉK, (struct szoftvercsatorna_CÍM *)&CÍM, sizeof(CÍM)) < 0 ||
        통신연결기다리기(kiszolgáló_ÉRTÉK, 4) < 0) return 1;
    if (elfogad_hálózati_kapcsolat(kiszolgáló_ÉRTÉK, 0, 0) != -1 || hibaszám != 11) return 2;
    int vendég_ÉRTÉK = készít_végpont(háló_Család, Stream_hálózat, Stream_átviteli_protokoll);
    if (vendég_ÉRTÉK < 0 || KAPCSOLAT_hálózat(vendég_ÉRTÉK, (struct szoftvercsatorna_CÍM *)&CÍM, sizeof(CÍM)) < 0) return 3;
    int Kapcsolódás = elfogad_hálózati_kapcsolat(kiszolgáló_ÉRTÉK, 0, 0);
    if (Kapcsolódás < 0) return 4;
    unsigned char 보낼것[1500], KAPOTT_cikk[1500];
    for (int szám = 0; szám < 1500; szám++) 보낼것[szám] = (unsigned char)szám;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int hossz_ÉRTÉK = ír_Fájl_adat(vendég_ÉRTÉK, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (hossz_ÉRTÉK <= 0) return 5;
        보낸수 += hossz_ÉRTÉK;
    }
    if (ír_Fájl_adat(vendég_ÉRTÉK, 보낼것, 1) != -1 || hibaszám != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 BACK_ÉRTÉK EOF가 된다. */
    bezár_Fájl(vendég_ÉRTÉK);
    int KAPOTT_DARAB = 0;
    while (KAPOTT_DARAB < 보낸수) {
        int hossz_ÉRTÉK = 파일자료읽기(Kapcsolódás, KAPOTT_cikk + KAPOTT_DARAB, sizeof(KAPOTT_cikk) - KAPOTT_DARAB);
        if (hossz_ÉRTÉK <= 0) return 7;
        KAPOTT_DARAB += hossz_ÉRTÉK;
    }
    for (int szám = 0; szám < KAPOTT_DARAB; szám++) if (KAPOTT_cikk[szám] != 보낼것[szám]) return 8;
    if (파일자료읽기(Kapcsolódás, KAPOTT_cikk, 1) != 0) return 9;
    if (ír_Fájl_adat(Kapcsolódás, 보낼것, 1) != -1 || hibaszám != 32) return 10;
    bezár_Fájl(Kapcsolódás); bezár_Fájl(kiszolgáló_ÉRTÉK);
    const char KR[] = "C posix-kor 연결형 kommunikáció PASS\n";
    ír_Fájl_adat(1, KR, sizeof(KR) - 1);
    return 0;
}
