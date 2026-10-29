#include "통신규약.h"
static pilvi_vastake_OSOITE OSOITE(unsigned portti_ARVO) {
    pilvi_vastake_OSOITE ARVO = {}; ARVO.OSOITE_Perhe = pilvi_Perhe;
    ARVO.portin_numero = 망차례짧은수(portti_ARVO); ARVO.Internet_osoite.OSOITE_ARVO = verkko_kokonaisluku(silmukkaosoite); return ARVO;
}
extern "C" int alku_käyttäjä_ohjelma(int) {
    int 보내는곳 = Luo_päätepiste(pilvi_Perhe, datagrammivastake, 0);
    int 받는곳 = Luo_päätepiste(pilvi_Perhe, datagrammivastake, datagrammi_protokolla);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    pilvi_vastake_OSOITE 도착 = OSOITE(7777), 출발 = OSOITE(7778), 보낸주소 = {};
    vastake_OSOITE_kesto_TYYPPI OSOITE_kesto = sizeof(보낸주소);
    if (BIND_OSOITE(받는곳, (vastake_OSOITE *)&도착, sizeof(도착))) return 2;
    if (BIND_OSOITE(보내는곳, (vastake_OSOITE *)&도착, sizeof(도착)) != -1 || virhenumero != 98) return 3;
    if (BIND_OSOITE(보내는곳, (vastake_OSOITE *)&출발, sizeof(출발))) return 4;
    static const char Sisältö_ARVO[] = "한글 UDP loopback 😀";
    char SAATU_HINTA_ARVO[64] = {};
    if (lähettää_datagrammi_data(보내는곳, Sisältö_ARVO, sizeof(Sisältö_ARVO), 0, (vastake_OSOITE *)&도착, sizeof(도착)) != sizeof(Sisältö_ARVO)) return 5;
    if (saada_datagrammi_data(받는곳, (void *)Sisältö_ARVO, sizeof(Sisältö_ARVO), 0, 0, 0) != -1 || virhenumero != 14) return 6;
    if (saada_datagrammi_data(받는곳, SAATU_HINTA_ARVO, sizeof(SAATU_HINTA_ARVO), 0, (vastake_OSOITE *)&보낸주소, &OSOITE_kesto) != sizeof(Sisältö_ARVO)) return 7;
    if (OSOITE_kesto != sizeof(보낸주소) || 장치차례짧은수(보낸주소.portin_numero) != 7778 || laite_tilata_kokonaisluku(보낸주소.Internet_osoite.OSOITE_ARVO) != silmukkaosoite) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Sisältö_ARVO); 순번++) if (SAATU_HINTA_ARVO[순번] != Sisältö_ARVO[순번]) return 9;
    if (saada_datagrammi_data(받는곳, SAATU_HINTA_ARVO, sizeof(SAATU_HINTA_ARVO), 0, 0, 0) != -1 || virhenumero != 11) return 10;
    if (lähettää_datagrammi_data(받는곳, SAATU_HINTA_ARVO, sizeof(Sisältö_ARVO), 0, (vastake_OSOITE *)&보낸주소, sizeof(보낸주소)) != sizeof(Sisältö_ARVO)) return 11;
    if (saada_datagrammi_data(보내는곳, SAATU_HINTA_ARVO, 4, 0, 0, 0) != 4) return 12;
    if (saada_datagrammi_data(보내는곳, SAATU_HINTA_ARVO, 4, 0, 0, 0) != -1 || virhenumero != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (lähettää_datagrammi_data(보내는곳, Sisältö_ARVO, sizeof(Sisältö_ARVO), 0, (vastake_OSOITE *)&도착, sizeof(도착)) != sizeof(Sisältö_ARVO)) return 14;
    if (lähettää_datagrammi_data(보내는곳, Sisältö_ARVO, sizeof(Sisältö_ARVO), 0, (vastake_OSOITE *)&도착, sizeof(도착)) != -1 || virhenumero != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (saada_datagrammi_data(받는곳, SAATU_HINTA_ARVO, sizeof(SAATU_HINTA_ARVO), 0, 0, 0) != sizeof(Sisältö_ARVO)) return 16;
    if (lähettää_datagrammi_data(보내는곳, 0, 0, 0, (vastake_OSOITE *)&도착, sizeof(도착)) != 0 ||
        saada_datagrammi_data(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.Internet_osoite.OSOITE_ARVO = verkko_kokonaisluku(0x08080808);
    if (lähettää_datagrammi_data(보내는곳, Sisältö_ARVO, sizeof(Sisältö_ARVO), 0, (vastake_OSOITE *)&도착, sizeof(도착)) != -1 || virhenumero != 101) return 17;
    if (Luo_päätepiste(pilvi_Perhe, virta_verkko, datagrammi_protokolla) != -1 || virhenumero != 93) return 18;
    OSOITE_kesto = sizeof(보낸주소);
    if (lukea_vastake_OSOITE(받는곳, (vastake_OSOITE *)&보낸주소, &OSOITE_kesto) || 장치차례짧은수(보낸주소.portin_numero) != 7777) return 19;
    if (Sulje_Tiedosto(받는곳) || Sulje_Tiedosto(받는곳) != -1 || virhenumero != 9) return 20;
    // 보내는곳은 열어 둔다: Lopeta_ohjelma 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    kirjoitus_Tiedosto_data(1, 완료, sizeof(완료) - 1);
    return 0;
}
