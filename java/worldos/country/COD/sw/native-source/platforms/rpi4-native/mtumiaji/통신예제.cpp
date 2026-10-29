#include "통신규약.h"
static 인터넷통신주소 anwani(unsigned kituo_thamani) {
    인터넷통신주소 thamani = {}; thamani.anwani_Familia = wingu_Familia;
    thamani.namba_ya_kituo = 망차례짧은수(kituo_thamani); thamani.Anwani_tovuti.anwani_thamani = Mtandao_namba_kamili(되돌림주소); return thamani;
}
extern "C" int Anza_mtumiaji_programu(int) {
    int 보내는곳 = 통신종단점만들기(wingu_Familia, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(wingu_Familia, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = anwani(7777), 출발 = anwani(7778), 보낸주소 = {};
    통신주소길이형 anwani_urefu = sizeof(보낸주소);
    if (FUNGA_anwani(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (FUNGA_anwani(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (FUNGA_anwani(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char maudhui_thamani[] = "한글 UDP loopback 😀";
    char 받은값[64] = {};
    if (자료전문보내기(보내는곳, maudhui_thamani, sizeof(maudhui_thamani), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(maudhui_thamani)) return 5;
    if (자료전문받기(받는곳, (void *)maudhui_thamani, sizeof(maudhui_thamani), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, (통신주소 *)&보낸주소, &anwani_urefu) != sizeof(maudhui_thamani)) return 7;
    if (anwani_urefu != sizeof(보낸주소) || 장치차례짧은수(보낸주소.namba_ya_kituo) != 7778 || kifaa_mpangilio_namba_kamili(보낸주소.Anwani_tovuti.anwani_thamani) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(maudhui_thamani); 순번++) if (받은값[순번] != maudhui_thamani[순번]) return 9;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, 받은값, sizeof(maudhui_thamani), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(maudhui_thamani)) return 11;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, maudhui_thamani, sizeof(maudhui_thamani), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(maudhui_thamani)) return 14;
    if (자료전문보내기(보내는곳, maudhui_thamani, sizeof(maudhui_thamani), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != sizeof(maudhui_thamani)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.Anwani_tovuti.anwani_thamani = Mtandao_namba_kamili(0x08080808);
    if (자료전문보내기(보내는곳, maudhui_thamani, sizeof(maudhui_thamani), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(wingu_Familia, Stream_Mtandao, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    anwani_urefu = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &anwani_urefu) || 장치차례짧은수(보낸주소.namba_ya_kituo) != 7777) return 19;
    if (funga_faili(받는곳) || funga_faili(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: toka_programu 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    andika_faili_data(1, 완료, sizeof(완료) - 1);
    return 0;
}
