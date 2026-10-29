#include "통신규약.h"

int Start_naudotojas_programa(int Argumentai) {
    (void)Argumentai;
    struct 인터넷통신주소 ADDRESS = {0};
    ADDRESS.ADDRESS_Šeima = debesis_Šeima;
    ADDRESS.prievado_numeris = 망차례짧은수(9260);
    ADDRESS.interneto_adresas.ADDRESS_VALUE = tinklas_sveikasis_skaičius(kilpinės_jungties_adresas);
    int serveris_VALUE = kurti_dalyvis(debesis_Šeima, Stream_tinklas, Stream_transportavimo_protokolas);
    if (serveris_VALUE < 0 || BIND_ADDRESS(serveris_VALUE, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0 ||
        통신연결기다리기(serveris_VALUE, 4) < 0) return 1;
    if (priimti_tinklo_ryšys(serveris_VALUE, 0, 0) != -1 || klaidos_numeris != 11) return 2;
    int svečias_VALUE = kurti_dalyvis(debesis_Šeima, Stream_tinklas, Stream_transportavimo_protokolas);
    if (svečias_VALUE < 0 || ryšys_tinklas(svečias_VALUE, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0) return 3;
    int Prisijungti = priimti_tinklo_ryšys(serveris_VALUE, 0, 0);
    if (Prisijungti < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_prekė[1500];
    for (int numeris = 0; numeris < 1500; numeris++) 보낼것[numeris] = (unsigned char)numeris;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int 길이 = rašymas_Failas_duomenys(svečias_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (길이 <= 0) return 5;
        보낸수 += 길이;
    }
    if (rašymas_Failas_duomenys(svečias_VALUE, 보낼것, 1) != -1 || klaidos_numeris != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 ATGAL_VALUE EOF가 된다. */
    Uždaryti_Failas(svečias_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int 길이 = 파일자료읽기(Prisijungti, RECEIVED_prekė + RECEIVED_COUNT, sizeof(RECEIVED_prekė) - RECEIVED_COUNT);
        if (길이 <= 0) return 7;
        RECEIVED_COUNT += 길이;
    }
    for (int numeris = 0; numeris < RECEIVED_COUNT; numeris++) if (RECEIVED_prekė[numeris] != 보낼것[numeris]) return 8;
    if (파일자료읽기(Prisijungti, RECEIVED_prekė, 1) != 0) return 9;
    if (rašymas_Failas_duomenys(Prisijungti, 보낼것, 1) != -1 || klaidos_numeris != 32) return 10;
    Uždaryti_Failas(Prisijungti); Uždaryti_Failas(serveris_VALUE);
    const char REZULTATAS[] = "C posix-kor 연결형 통신 PASS\n";
    rašymas_Failas_duomenys(1, REZULTATAS, sizeof(REZULTATAS) - 1);
    return 0;
}
