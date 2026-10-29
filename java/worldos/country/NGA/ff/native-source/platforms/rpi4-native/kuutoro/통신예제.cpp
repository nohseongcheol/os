#include "통신규약.h"
static 인터넷통신주소 ñiiɓirde(unsigned poor_njaru) {
    인터넷통신주소 njaru = {}; njaru.주소갈래 = 인터넷주소갈래;
    njaru.접속번호 = 망차례짧은수(poor_njaru); njaru.ñiiɓirde_enternet.ñiiɓirde_njaru = 망차례정수(되돌림주소); return njaru;
}
extern "C" int huɓɓude_kuutoro_tafirde(int) {
    int 보내는곳 = 통신종단점만들기(인터넷주소갈래, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(인터넷주소갈래, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = ñiiɓirde(7777), 출발 = ñiiɓirde(7778), 보낸주소 = {};
    통신주소길이형 ñiiɓirde_njuuteendi = sizeof(보낸주소);
    if (seŋondir_ñiiɓirde(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (seŋondir_ñiiɓirde(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (seŋondir_ñiiɓirde(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char loowdi_njaru[] = "한글 UDP loopback 😀";
    char 받은값[64] = {};
    if (자료전문보내기(보내는곳, loowdi_njaru, sizeof(loowdi_njaru), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(loowdi_njaru)) return 5;
    if (자료전문받기(받는곳, (void *)loowdi_njaru, sizeof(loowdi_njaru), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, (통신주소 *)&보낸주소, &ñiiɓirde_njuuteendi) != sizeof(loowdi_njaru)) return 7;
    if (ñiiɓirde_njuuteendi != sizeof(보낸주소) || 장치차례짧은수(보낸주소.접속번호) != 7778 || 장치차례정수(보낸주소.ñiiɓirde_enternet.ñiiɓirde_njaru) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(loowdi_njaru); 순번++) if (받은값[순번] != loowdi_njaru[순번]) return 9;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, 받은값, sizeof(loowdi_njaru), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(loowdi_njaru)) return 11;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, loowdi_njaru, sizeof(loowdi_njaru), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(loowdi_njaru)) return 14;
    if (자료전문보내기(보내는곳, loowdi_njaru, sizeof(loowdi_njaru), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != sizeof(loowdi_njaru)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.ñiiɓirde_enternet.ñiiɓirde_njaru = 망차례정수(0x08080808);
    if (자료전문보내기(보내는곳, loowdi_njaru, sizeof(loowdi_njaru), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(인터넷주소갈래, waraango_laylaytol, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    ñiiɓirde_njuuteendi = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &ñiiɓirde_njuuteendi) || 장치차례짧은수(보낸주소.접속번호) != 7777) return 19;
    if (uddude_fiilde(받는곳) || uddude_fiilde(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: yaltude_tafirde 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    winndude_fiilde_keɓe(1, 완료, sizeof(완료) - 1);
    return 0;
}
