#include "통신규약.h"

int Start_úsáideoir_clár(int Argóintí) {
    (void)Argóintí;
    struct 인터넷통신주소 ADDRESS = {0};
    ADDRESS.ADDRESS_Teaghlach = néal_Teaghlach;
    ADDRESS.uimhir_phoirt = 망차례짧은수(9260);
    ADDRESS.seoladh_Idirlín.ADDRESS_VALUE = Líonra_slánuimhir(seoladh_aislúbtha);
    int freastalaí_VALUE = 통신종단점만들기(néal_Teaghlach, sruth_Líonra, 흐름전송규약);
    if (freastalaí_VALUE < 0 || BIND_ADDRESS(freastalaí_VALUE, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0 ||
        통신연결기다리기(freastalaí_VALUE, 4) < 0) return 1;
    if (glac_le_nasc_líonra(freastalaí_VALUE, 0, 0) != -1 || 오류번호 != 11) return 2;
    int aoi_VALUE = 통신종단점만들기(néal_Teaghlach, sruth_Líonra, 흐름전송규약);
    if (aoi_VALUE < 0 || nasc_Líonra(aoi_VALUE, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0) return 3;
    int Nasc = glac_le_nasc_líonra(freastalaí_VALUE, 0, 0);
    if (Nasc < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_mír[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int fad_VALUE = scríobh_comhad_sonraí(aoi_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (fad_VALUE <= 0) return 5;
        보낸수 += fad_VALUE;
    }
    if (scríobh_comhad_sonraí(aoi_VALUE, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Siar_VALUE EOF가 된다. */
    dún_comhad(aoi_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int fad_VALUE = 파일자료읽기(Nasc, RECEIVED_mír + RECEIVED_COUNT, sizeof(RECEIVED_mír) - RECEIVED_COUNT);
        if (fad_VALUE <= 0) return 7;
        RECEIVED_COUNT += fad_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_mír[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Nasc, RECEIVED_mír, 1) != 0) return 9;
    if (scríobh_comhad_sonraí(Nasc, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    dún_comhad(Nasc); dún_comhad(freastalaí_VALUE);
    const char tomhas[] = "C posix-kor 연결형 통신 PASS\n";
    scríobh_comhad_sonraí(1, tomhas, sizeof(tomhas) - 1);
    return 0;
}
