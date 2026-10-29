#include "통신규약.h"

int Itangira_ukoresha_porogaramu(int 인수) {
    (void)인수;
    struct 인터넷통신주소 aderesi = {0};
    aderesi.aderesi_Umuryango = karawudi_Umuryango;
    aderesi.접속번호 = 망차례짧은수(9260);
    aderesi.Aderesi_ya_Interineti.aderesi_agaciro = Urusobemiyoboro_umubare_wuzuye(되돌림주소);
    int seriveri_agaciro = 통신종단점만들기(karawudi_Umuryango, Stream_Urusobemiyoboro, 흐름전송규약);
    if (seriveri_agaciro < 0 || BIND_aderesi(seriveri_agaciro, (struct 통신주소 *)&aderesi, sizeof(aderesi)) < 0 ||
        통신연결기다리기(seriveri_agaciro, 4) < 0) return 1;
    if (kwemera_ukwihuza_ku_rusobemiyoboro(seriveri_agaciro, 0, 0) != -1 || 오류번호 != 11) return 2;
    int 손님 = 통신종단점만들기(karawudi_Umuryango, Stream_Urusobemiyoboro, 흐름전송규약);
    if (손님 < 0 || Guhuza_Urusobemiyoboro(손님, (struct 통신주소 *)&aderesi, sizeof(aderesi)) < 0) return 3;
    int Guhuza = kwemera_ukwihuza_ku_rusobemiyoboro(seriveri_agaciro, 0, 0);
    if (Guhuza < 0) return 4;
    unsigned char 보낼것[1500], 받은것[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int uburebure_agaciro = kwandika_dosiye_amakurushingiro(손님, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (uburebure_agaciro <= 0) return 5;
        보낸수 += uburebure_agaciro;
    }
    if (kwandika_dosiye_amakurushingiro(손님, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Ikibanza_agaciro EOF가 된다. */
    gufunga_dosiye(손님);
    int 받은수 = 0;
    while (받은수 < 보낸수) {
        int uburebure_agaciro = 파일자료읽기(Guhuza, 받은것 + 받은수, sizeof(받은것) - 받은수);
        if (uburebure_agaciro <= 0) return 7;
        받은수 += uburebure_agaciro;
    }
    for (int 수 = 0; 수 < 받은수; 수++) if (받은것[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Guhuza, 받은것, 1) != 0) return 9;
    if (kwandika_dosiye_amakurushingiro(Guhuza, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    gufunga_dosiye(Guhuza); gufunga_dosiye(seriveri_agaciro);
    const char 결과[] = "C posix-kor 연결형 통신 PASS\n";
    kwandika_dosiye_amakurushingiro(1, 결과, sizeof(결과) - 1);
    return 0;
}
