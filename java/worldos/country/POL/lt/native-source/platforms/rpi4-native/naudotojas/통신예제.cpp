#include "통신규약.h"
static 인터넷통신주소 ADDRESS(unsigned jungtis_VALUE) {
    인터넷통신주소 VALUE = {}; VALUE.ADDRESS_Šeima = debesis_Šeima;
    VALUE.prievado_numeris = 망차례짧은수(jungtis_VALUE); VALUE.interneto_adresas.ADDRESS_VALUE = tinklas_sveikasis_skaičius(kilpinės_jungties_adresas); return VALUE;
}
extern "C" int Start_naudotojas_programa(int) {
    int 보내는곳 = kurti_dalyvis(debesis_Šeima, paketų_maršruto_schemos_jungtis, 0);
    int 받는곳 = kurti_dalyvis(debesis_Šeima, paketų_maršruto_schemos_jungtis, paketų_kelio_schema_protokolas);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = ADDRESS(7777), 출발 = ADDRESS(7778), 보낸주소 = {};
    통신주소길이형 주소길이 = sizeof(보낸주소);
    if (BIND_ADDRESS(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BIND_ADDRESS(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || klaidos_numeris != 98) return 3;
    if (BIND_ADDRESS(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Turinys_VALUE[] = "한글 UDP loopback 😀";
    char RECEIVED_VALUE[64] = {};
    if (siųsti_paketų_kelio_schema_duomenys(보내는곳, Turinys_VALUE, sizeof(Turinys_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Turinys_VALUE)) return 5;
    if (gauti_paketų_kelio_schema_duomenys(받는곳, (void *)Turinys_VALUE, sizeof(Turinys_VALUE), 0, 0, 0) != -1 || klaidos_numeris != 14) return 6;
    if (gauti_paketų_kelio_schema_duomenys(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, (통신주소 *)&보낸주소, &주소길이) != sizeof(Turinys_VALUE)) return 7;
    if (주소길이 != sizeof(보낸주소) || 장치차례짧은수(보낸주소.prievado_numeris) != 7778 || įrenginys_tvarka_sveikasis_skaičius(보낸주소.interneto_adresas.ADDRESS_VALUE) != kilpinės_jungties_adresas) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Turinys_VALUE); 순번++) if (RECEIVED_VALUE[순번] != Turinys_VALUE[순번]) return 9;
    if (gauti_paketų_kelio_schema_duomenys(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != -1 || klaidos_numeris != 11) return 10;
    if (siųsti_paketų_kelio_schema_duomenys(받는곳, RECEIVED_VALUE, sizeof(Turinys_VALUE), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Turinys_VALUE)) return 11;
    if (gauti_paketų_kelio_schema_duomenys(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != 4) return 12;
    if (gauti_paketų_kelio_schema_duomenys(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != -1 || klaidos_numeris != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (siųsti_paketų_kelio_schema_duomenys(보내는곳, Turinys_VALUE, sizeof(Turinys_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Turinys_VALUE)) return 14;
    if (siųsti_paketų_kelio_schema_duomenys(보내는곳, Turinys_VALUE, sizeof(Turinys_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || klaidos_numeris != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (gauti_paketų_kelio_schema_duomenys(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != sizeof(Turinys_VALUE)) return 16;
    if (siųsti_paketų_kelio_schema_duomenys(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        gauti_paketų_kelio_schema_duomenys(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.interneto_adresas.ADDRESS_VALUE = tinklas_sveikasis_skaičius(0x08080808);
    if (siųsti_paketų_kelio_schema_duomenys(보내는곳, Turinys_VALUE, sizeof(Turinys_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || klaidos_numeris != 101) return 17;
    if (kurti_dalyvis(debesis_Šeima, Stream_tinklas, paketų_kelio_schema_protokolas) != -1 || klaidos_numeris != 93) return 18;
    주소길이 = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &주소길이) || 장치차례짧은수(보낸주소.prievado_numeris) != 7777) return 19;
    if (Uždaryti_Failas(받는곳) || Uždaryti_Failas(받는곳) != -1 || klaidos_numeris != 9) return 20;
    // 보내는곳은 열어 둔다: Baigti_programa_086bb533 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    rašymas_Failas_duomenys(1, 완료, sizeof(완료) - 1);
    return 0;
}
