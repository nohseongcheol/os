#include "통신규약.h"
static háló_szoftvercsatorna_CÍM CÍM(unsigned port_ÉRTÉK) {
    háló_szoftvercsatorna_CÍM ÉRTÉK = {}; ÉRTÉK.CÍM_Család = háló_Család;
    ÉRTÉK.portszám = 망차례짧은수(port_ÉRTÉK); ÉRTÉK.internetcím.CÍM_ÉRTÉK = hálózat_egész_szám(visszacsatolási_cím); return ÉRTÉK;
}
extern "C" int START_felhasználó_app(int) {
    int 보내는곳 = készít_végpont(háló_Család, datagram_szoftvercsatorna, 0);
    int 받는곳 = készít_végpont(háló_Család, datagram_szoftvercsatorna, datagram_protokoll);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    háló_szoftvercsatorna_CÍM 도착 = CÍM(7777), 출발 = CÍM(7778), 보낸주소 = {};
    szoftvercsatorna_CÍM_hossz_beír CÍM_hossz = sizeof(보낸주소);
    if (BIND_CÍM(받는곳, (szoftvercsatorna_CÍM *)&도착, sizeof(도착))) return 2;
    if (BIND_CÍM(보내는곳, (szoftvercsatorna_CÍM *)&도착, sizeof(도착)) != -1 || hibaszám != 98) return 3;
    if (BIND_CÍM(보내는곳, (szoftvercsatorna_CÍM *)&출발, sizeof(출발))) return 4;
    static const char Tartalom_ÉRTÉK[] = "한글 UDP loopback 😀";
    char KAPOTT_ÉRTÉK[64] = {};
    if (küld_datagram_adat(보내는곳, Tartalom_ÉRTÉK, sizeof(Tartalom_ÉRTÉK), 0, (szoftvercsatorna_CÍM *)&도착, sizeof(도착)) != sizeof(Tartalom_ÉRTÉK)) return 5;
    if (fogad_datagram_adat(받는곳, (void *)Tartalom_ÉRTÉK, sizeof(Tartalom_ÉRTÉK), 0, 0, 0) != -1 || hibaszám != 14) return 6;
    if (fogad_datagram_adat(받는곳, KAPOTT_ÉRTÉK, sizeof(KAPOTT_ÉRTÉK), 0, (szoftvercsatorna_CÍM *)&보낸주소, &CÍM_hossz) != sizeof(Tartalom_ÉRTÉK)) return 7;
    if (CÍM_hossz != sizeof(보낸주소) || 장치차례짧은수(보낸주소.portszám) != 7778 || mobil_rendel_egész_szám(보낸주소.internetcím.CÍM_ÉRTÉK) != visszacsatolási_cím) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Tartalom_ÉRTÉK); 순번++) if (KAPOTT_ÉRTÉK[순번] != Tartalom_ÉRTÉK[순번]) return 9;
    if (fogad_datagram_adat(받는곳, KAPOTT_ÉRTÉK, sizeof(KAPOTT_ÉRTÉK), 0, 0, 0) != -1 || hibaszám != 11) return 10;
    if (küld_datagram_adat(받는곳, KAPOTT_ÉRTÉK, sizeof(Tartalom_ÉRTÉK), 0, (szoftvercsatorna_CÍM *)&보낸주소, sizeof(보낸주소)) != sizeof(Tartalom_ÉRTÉK)) return 11;
    if (fogad_datagram_adat(보내는곳, KAPOTT_ÉRTÉK, 4, 0, 0, 0) != 4) return 12;
    if (fogad_datagram_adat(보내는곳, KAPOTT_ÉRTÉK, 4, 0, 0, 0) != -1 || hibaszám != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (küld_datagram_adat(보내는곳, Tartalom_ÉRTÉK, sizeof(Tartalom_ÉRTÉK), 0, (szoftvercsatorna_CÍM *)&도착, sizeof(도착)) != sizeof(Tartalom_ÉRTÉK)) return 14;
    if (küld_datagram_adat(보내는곳, Tartalom_ÉRTÉK, sizeof(Tartalom_ÉRTÉK), 0, (szoftvercsatorna_CÍM *)&도착, sizeof(도착)) != -1 || hibaszám != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (fogad_datagram_adat(받는곳, KAPOTT_ÉRTÉK, sizeof(KAPOTT_ÉRTÉK), 0, 0, 0) != sizeof(Tartalom_ÉRTÉK)) return 16;
    if (küld_datagram_adat(보내는곳, 0, 0, 0, (szoftvercsatorna_CÍM *)&도착, sizeof(도착)) != 0 ||
        fogad_datagram_adat(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.internetcím.CÍM_ÉRTÉK = hálózat_egész_szám(0x08080808);
    if (küld_datagram_adat(보내는곳, Tartalom_ÉRTÉK, sizeof(Tartalom_ÉRTÉK), 0, (szoftvercsatorna_CÍM *)&도착, sizeof(도착)) != -1 || hibaszám != 101) return 17;
    if (készít_végpont(háló_Család, Stream_hálózat, datagram_protokoll) != -1 || hibaszám != 93) return 18;
    CÍM_hossz = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (szoftvercsatorna_CÍM *)&보낸주소, &CÍM_hossz) || 장치차례짧은수(보낸주소.portszám) != 7777) return 19;
    if (bezár_Fájl(받는곳) || bezár_Fájl(받는곳) != -1 || hibaszám != 9) return 20;
    // 보내는곳은 열어 둔다: kilép_app 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    ír_Fájl_adat(1, 완료, sizeof(완료) - 1);
    return 0;
}
