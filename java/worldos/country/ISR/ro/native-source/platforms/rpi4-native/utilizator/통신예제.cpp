#include "통신규약.h"
static 인터넷통신주소 adresa(unsigned muta_VALUE) {
    인터넷통신주소 VALUE = {}; VALUE.adresa_Familie = cloud_Familie;
    VALUE.număr_port = 망차례짧은수(muta_VALUE); VALUE.adresă_internet.adresa_VALUE = rețea_întreg(adresă_de_întoarcere_în_buclă); return VALUE;
}
extern "C" int buta_utilizator_program(int) {
    int 보내는곳 = crea_participant(cloud_Familie, racord_diagramă_informații, 0);
    int 받는곳 = crea_participant(cloud_Familie, racord_diagramă_informații, diagramă_informații_protocol);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = adresa(7777), 출발 = adresa(7778), 보낸주소 = {};
    통신주소길이형 adresa_lungime = sizeof(보낸주소);
    if (BIND_adresa(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BIND_adresa(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || număr_de_eroare != 98) return 3;
    if (BIND_adresa(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Conținut_VALUE[] = "한글 UDP loopback 😀";
    char RECEIVED_VALUE[64] = {};
    if (trimite_diagramă_informații_date(보내는곳, Conținut_VALUE, sizeof(Conținut_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Conținut_VALUE)) return 5;
    if (primi_diagramă_informații_date(받는곳, (void *)Conținut_VALUE, sizeof(Conținut_VALUE), 0, 0, 0) != -1 || număr_de_eroare != 14) return 6;
    if (primi_diagramă_informații_date(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, (통신주소 *)&보낸주소, &adresa_lungime) != sizeof(Conținut_VALUE)) return 7;
    if (adresa_lungime != sizeof(보낸주소) || 장치차례짧은수(보낸주소.număr_port) != 7778 || mobil_ordine_întreg(보낸주소.adresă_internet.adresa_VALUE) != adresă_de_întoarcere_în_buclă) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Conținut_VALUE); 순번++) if (RECEIVED_VALUE[순번] != Conținut_VALUE[순번]) return 9;
    if (primi_diagramă_informații_date(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != -1 || număr_de_eroare != 11) return 10;
    if (trimite_diagramă_informații_date(받는곳, RECEIVED_VALUE, sizeof(Conținut_VALUE), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Conținut_VALUE)) return 11;
    if (primi_diagramă_informații_date(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != 4) return 12;
    if (primi_diagramă_informații_date(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != -1 || număr_de_eroare != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (trimite_diagramă_informații_date(보내는곳, Conținut_VALUE, sizeof(Conținut_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Conținut_VALUE)) return 14;
    if (trimite_diagramă_informații_date(보내는곳, Conținut_VALUE, sizeof(Conținut_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || număr_de_eroare != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (primi_diagramă_informații_date(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != sizeof(Conținut_VALUE)) return 16;
    if (trimite_diagramă_informații_date(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        primi_diagramă_informații_date(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.adresă_internet.adresa_VALUE = rețea_întreg(0x08080808);
    if (trimite_diagramă_informații_date(보내는곳, Conținut_VALUE, sizeof(Conținut_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || număr_de_eroare != 101) return 17;
    if (crea_participant(cloud_Familie, flux_rețea, diagramă_informații_protocol) != -1 || număr_de_eroare != 93) return 18;
    adresa_lungime = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &adresa_lungime) || 장치차례짧은수(보낸주소.număr_port) != 7777) return 19;
    if (închide_Fișier(받는곳) || închide_Fișier(받는곳) != -1 || număr_de_eroare != 9) return 20;
    // 보내는곳은 열어 둔다: ieși_program 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    scriere_Fișier_date(1, 완료, sizeof(완료) - 1);
    return 0;
}
