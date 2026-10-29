#include "통신규약.h"

int Anza_mtumiaji_programu(int 인수) {
    (void)인수;
    struct 인터넷통신주소 anwani = {0};
    anwani.anwani_Familia = wingu_Familia;
    anwani.namba_ya_kituo = 망차례짧은수(9260);
    anwani.Anwani_tovuti.anwani_thamani = Mtandao_namba_kamili(되돌림주소);
    int seva_thamani = 통신종단점만들기(wingu_Familia, Stream_Mtandao, 흐름전송규약);
    if (seva_thamani < 0 || FUNGA_anwani(seva_thamani, (struct 통신주소 *)&anwani, sizeof(anwani)) < 0 ||
        통신연결기다리기(seva_thamani, 4) < 0) return 1;
    if (kubali_muunganisho_wa_mtandao(seva_thamani, 0, 0) != -1 || 오류번호 != 11) return 2;
    int mgeni_thamani = 통신종단점만들기(wingu_Familia, Stream_Mtandao, 흐름전송규약);
    if (mgeni_thamani < 0 || UNGANISHA_Mtandao(mgeni_thamani, (struct 통신주소 *)&anwani, sizeof(anwani)) < 0) return 3;
    int UNGANISHA = kubali_muunganisho_wa_mtandao(seva_thamani, 0, 0);
    if (UNGANISHA < 0) return 4;
    unsigned char 보낼것[1500], 받은것[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int urefu_thamani = andika_faili_data(mgeni_thamani, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (urefu_thamani <= 0) return 5;
        보낸수 += urefu_thamani;
    }
    if (andika_faili_data(mgeni_thamani, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Nyuma_thamani EOF가 된다. */
    funga_faili(mgeni_thamani);
    int 받은수 = 0;
    while (받은수 < 보낸수) {
        int urefu_thamani = 파일자료읽기(UNGANISHA, 받은것 + 받은수, sizeof(받은것) - 받은수);
        if (urefu_thamani <= 0) return 7;
        받은수 += urefu_thamani;
    }
    for (int 수 = 0; 수 < 받은수; 수++) if (받은것[수] != 보낼것[수]) return 8;
    if (파일자료읽기(UNGANISHA, 받은것, 1) != 0) return 9;
    if (andika_faili_data(UNGANISHA, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    funga_faili(UNGANISHA); funga_faili(seva_thamani);
    const char 결과[] = "C posix-kor 연결형 통신 PASS\n";
    andika_faili_data(1, 결과, sizeof(결과) - 1);
    return 0;
}
