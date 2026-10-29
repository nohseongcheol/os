#include "통신규약.h"
static 인터넷통신주소 ADDRESS(unsigned kawe_uara) {
    인터넷통신주소 uara = {}; uara.ADDRESS_Whānau = kapua_Whānau;
    uara.접속번호 = 망차례짧은수(kawe_uara); uara.Wāhitau_ipurangi.ADDRESS_uara = whatunga_tau_tōpū(되돌림주소); return uara;
}
extern "C" int Start_kaiwhakamahi_kaupapa(int) {
    int 보내는곳 = 통신종단점만들기(kapua_Whānau, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(kapua_Whānau, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = ADDRESS(7777), 출발 = ADDRESS(7778), 보낸주소 = {};
    통신주소길이형 ADDRESS_roa = sizeof(보낸주소);
    if (BIND_ADDRESS(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BIND_ADDRESS(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (BIND_ADDRESS(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Ihirangi_uara[] = "한글 UDP loopback 😀";
    char RECEIVED_uara[64] = {};
    if (자료전문보내기(보내는곳, Ihirangi_uara, sizeof(Ihirangi_uara), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Ihirangi_uara)) return 5;
    if (자료전문받기(받는곳, (void *)Ihirangi_uara, sizeof(Ihirangi_uara), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, RECEIVED_uara, sizeof(RECEIVED_uara), 0, (통신주소 *)&보낸주소, &ADDRESS_roa) != sizeof(Ihirangi_uara)) return 7;
    if (ADDRESS_roa != sizeof(보낸주소) || 장치차례짧은수(보낸주소.접속번호) != 7778 || pūkoro_whakaraupapa_tau_tōpū(보낸주소.Wāhitau_ipurangi.ADDRESS_uara) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Ihirangi_uara); 순번++) if (RECEIVED_uara[순번] != Ihirangi_uara[순번]) return 9;
    if (자료전문받기(받는곳, RECEIVED_uara, sizeof(RECEIVED_uara), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, RECEIVED_uara, sizeof(Ihirangi_uara), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Ihirangi_uara)) return 11;
    if (자료전문받기(보내는곳, RECEIVED_uara, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, RECEIVED_uara, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Ihirangi_uara, sizeof(Ihirangi_uara), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Ihirangi_uara)) return 14;
    if (자료전문보내기(보내는곳, Ihirangi_uara, sizeof(Ihirangi_uara), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, RECEIVED_uara, sizeof(RECEIVED_uara), 0, 0, 0) != sizeof(Ihirangi_uara)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.Wāhitau_ipurangi.ADDRESS_uara = whatunga_tau_tōpū(0x08080808);
    if (자료전문보내기(보내는곳, Ihirangi_uara, sizeof(Ihirangi_uara), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(kapua_Whānau, roma_whatunga, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    ADDRESS_roa = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &ADDRESS_roa) || 장치차례짧은수(보낸주소.접속번호) != 7777) return 19;
    if (kati_kōnae(받는곳) || kati_kōnae(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: Putaatu_kaupapa 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    tuhi_kōnae_raraunga(1, 완료, sizeof(완료) - 1);
    return 0;
}
