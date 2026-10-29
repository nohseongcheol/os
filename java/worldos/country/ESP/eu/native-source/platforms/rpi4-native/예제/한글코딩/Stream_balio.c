#include "통신규약.h"

int HASI_erabiltzaile_aplik(int Argumentuak) {
    (void)Argumentuak;
    struct 인터넷통신주소 helbide = {0};
    helbide.helbide_sorta = hodei_sorta;
    helbide.ataka_zenbaki = 망차례짧은수(9260);
    helbide.Internet_helbide.helbide_balio = sare_osoko_zenbaki(되돌림주소);
    int zerbitzari_balio = sortu_amaiera_puntu(hodei_sorta, Stream_sare, Stream_garraio_protokolo);
    if (zerbitzari_balio < 0 || lotu_helbide(zerbitzari_balio, (struct 통신주소 *)&helbide, sizeof(helbide)) < 0 ||
        통신연결기다리기(zerbitzari_balio, 4) < 0) return 1;
    if (onartu_sare_konexio(zerbitzari_balio, 0, 0) != -1 || errorearen_zenbaki != 11) return 2;
    int gonbidatu_balio = sortu_amaiera_puntu(hodei_sorta, Stream_sare, Stream_garraio_protokolo);
    if (gonbidatu_balio < 0 || KONEKTATU_sare(gonbidatu_balio, (struct 통신주소 *)&helbide, sizeof(helbide)) < 0) return 3;
    int Konektatu = onartu_sare_konexio(zerbitzari_balio, 0, 0);
    if (Konektatu < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_elementu[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int luzera_balio = idatzi_fitxategi_datuak(gonbidatu_balio, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (luzera_balio <= 0) return 5;
        보낸수 += luzera_balio;
    }
    if (idatzi_fitxategi_datuak(gonbidatu_balio, 보낼것, 1) != -1 || errorearen_zenbaki != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 ATZERA_balio EOF가 된다. */
    itxi_fitxategi(gonbidatu_balio);
    int RECEIVED_ZENBATU = 0;
    while (RECEIVED_ZENBATU < 보낸수) {
        int luzera_balio = 파일자료읽기(Konektatu, RECEIVED_elementu + RECEIVED_ZENBATU, sizeof(RECEIVED_elementu) - RECEIVED_ZENBATU);
        if (luzera_balio <= 0) return 7;
        RECEIVED_ZENBATU += luzera_balio;
    }
    for (int 수 = 0; 수 < RECEIVED_ZENBATU; 수++) if (RECEIVED_elementu[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Konektatu, RECEIVED_elementu, 1) != 0) return 9;
    if (idatzi_fitxategi_datuak(Konektatu, 보낼것, 1) != -1 || errorearen_zenbaki != 32) return 10;
    itxi_fitxategi(Konektatu); itxi_fitxategi(zerbitzari_balio);
    const char EMAITZA[] = "C posix-kor 연결형 통신 PASS\n";
    idatzi_fitxategi_datuak(1, EMAITZA, sizeof(EMAITZA) - 1);
    return 0;
}
