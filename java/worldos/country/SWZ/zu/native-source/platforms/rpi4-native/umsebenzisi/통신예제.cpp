#include "통신규약.h"
static 인터넷통신주소 ikheli(unsigned intuba_inani) {
    인터넷통신주소 inani = {}; inani.ikheli_Umndeni = I_cloud_Umndeni;
    inani.접속번호 = 망차례짧은수(intuba_inani); inani.ikheli_le_inthanethi.ikheli_inani = iNethiwekhi_inamba(되돌림주소); return inani;
}
extern "C" int qala_umsebenzisi_i_app(int) {
    int 보내는곳 = 통신종단점만들기(I_cloud_Umndeni, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(I_cloud_Umndeni, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = ikheli(7777), 출발 = ikheli(7778), 보낸주소 = {};
    통신주소길이형 ikheli_ubude = sizeof(보낸주소);
    if (i_BIND_ikheli(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (i_BIND_ikheli(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (i_BIND_ikheli(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Okuqukethwe_inani[] = "한글 UDP loopback 😀";
    char 받은값[64] = {};
    if (자료전문보내기(보내는곳, Okuqukethwe_inani, sizeof(Okuqukethwe_inani), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Okuqukethwe_inani)) return 5;
    if (자료전문받기(받는곳, (void *)Okuqukethwe_inani, sizeof(Okuqukethwe_inani), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, (통신주소 *)&보낸주소, &ikheli_ubude) != sizeof(Okuqukethwe_inani)) return 7;
    if (ikheli_ubude != sizeof(보낸주소) || 장치차례짧은수(보낸주소.접속번호) != 7778 || idivayisi_ukuhleleka_inamba(보낸주소.ikheli_le_inthanethi.ikheli_inani) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Okuqukethwe_inani); 순번++) if (받은값[순번] != Okuqukethwe_inani[순번]) return 9;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, 받은값, sizeof(Okuqukethwe_inani), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Okuqukethwe_inani)) return 11;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Okuqukethwe_inani, sizeof(Okuqukethwe_inani), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Okuqukethwe_inani)) return 14;
    if (자료전문보내기(보내는곳, Okuqukethwe_inani, sizeof(Okuqukethwe_inani), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != sizeof(Okuqukethwe_inani)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.ikheli_le_inthanethi.ikheli_inani = iNethiwekhi_inamba(0x08080808);
    if (자료전문보내기(보내는곳, Okuqukethwe_inani, sizeof(Okuqukethwe_inani), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(I_cloud_Umndeni, Stream_iNethiwekhi, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    ikheli_ubude = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &ikheli_ubude) || 장치차례짧은수(보낸주소.접속번호) != 7777) return 19;
    if (vala_ifayela(받는곳) || vala_ifayela(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: phuma_i_app 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    bhala_ifayela_imininingwane(1, 완료, sizeof(완료) - 1);
    return 0;
}
