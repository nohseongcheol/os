#include "통신규약.h"

int alku_käyttäjä_ohjelma(int argumentit) {
    (void)argumentit;
    struct pilvi_vastake_OSOITE OSOITE = {0};
    OSOITE.OSOITE_Perhe = pilvi_Perhe;
    OSOITE.portin_numero = 망차례짧은수(9260);
    OSOITE.Internet_osoite.OSOITE_ARVO = verkko_kokonaisluku(silmukkaosoite);
    int palvelin_ARVO = Luo_päätepiste(pilvi_Perhe, virta_verkko, virta_kuljetusprotokolla);
    if (palvelin_ARVO < 0 || BIND_OSOITE(palvelin_ARVO, (struct vastake_OSOITE *)&OSOITE, sizeof(OSOITE)) < 0 ||
        통신연결기다리기(palvelin_ARVO, 4) < 0) return 1;
    if (hyväksyä_verkkoyhteys(palvelin_ARVO, 0, 0) != -1 || virhenumero != 11) return 2;
    int vieras_ARVO = Luo_päätepiste(pilvi_Perhe, virta_verkko, virta_kuljetusprotokolla);
    if (vieras_ARVO < 0 || YHDISTÄ_verkko(vieras_ARVO, (struct vastake_OSOITE *)&OSOITE, sizeof(OSOITE)) < 0) return 3;
    int Yhdistä = hyväksyä_verkkoyhteys(palvelin_ARVO, 0, 0);
    if (Yhdistä < 0) return 4;
    unsigned char 보낼것[1500], SAATU_HINTA_kohde[1500];
    for (int numero = 0; numero < 1500; numero++) 보낼것[numero] = (unsigned char)numero;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int kesto_ARVO = kirjoitus_Tiedosto_data(vieras_ARVO, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (kesto_ARVO <= 0) return 5;
        보낸수 += kesto_ARVO;
    }
    if (kirjoitus_Tiedosto_data(vieras_ARVO, 보낼것, 1) != -1 || virhenumero != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 BACK_ARVO EOF가 된다. */
    Sulje_Tiedosto(vieras_ARVO);
    int SAATU_HINTA_LASKE = 0;
    while (SAATU_HINTA_LASKE < 보낸수) {
        int kesto_ARVO = lukea_Tiedosto_data(Yhdistä, SAATU_HINTA_kohde + SAATU_HINTA_LASKE, sizeof(SAATU_HINTA_kohde) - SAATU_HINTA_LASKE);
        if (kesto_ARVO <= 0) return 7;
        SAATU_HINTA_LASKE += kesto_ARVO;
    }
    for (int numero = 0; numero < SAATU_HINTA_LASKE; numero++) if (SAATU_HINTA_kohde[numero] != 보낼것[numero]) return 8;
    if (lukea_Tiedosto_data(Yhdistä, SAATU_HINTA_kohde, 1) != 0) return 9;
    if (kirjoitus_Tiedosto_data(Yhdistä, 보낼것, 1) != -1 || virhenumero != 32) return 10;
    Sulje_Tiedosto(Yhdistä); Sulje_Tiedosto(palvelin_ARVO);
    const char TULOS[] = "C posix-kor 연결형 통신 PASS\n";
    kirjoitus_Tiedosto_data(1, TULOS, sizeof(TULOS) - 1);
    return 0;
}
