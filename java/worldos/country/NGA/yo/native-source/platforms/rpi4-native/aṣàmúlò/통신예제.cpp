#include "통신규약.h"
static 인터넷통신주소 àdírẹ́ẹ̀sì(unsigned ojú_iye) {
    인터넷통신주소 iye = {}; iye.àdírẹ́ẹ̀sì_Ẹbí = Íntánẹ́ẹ̀tì_Ẹbí;
    iye.접속번호 = 망차례짧은수(ojú_iye); iye.àdíréẹ̀sì_íntánẹ́ẹ̀tì.àdírẹ́ẹ̀sì_iye = Alásopọ̀_nọ́ńbà_odindi(되돌림주소); return iye;
}
extern "C" int bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò(int) {
    int 보내는곳 = 통신종단점만들기(Íntánẹ́ẹ̀tì_Ẹbí, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(Íntánẹ́ẹ̀tì_Ẹbí, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = àdírẹ́ẹ̀sì(7777), 출발 = àdírẹ́ẹ̀sì(7778), 보낸주소 = {};
    통신주소길이형 àdírẹ́ẹ̀sì_gígùn = sizeof(보낸주소);
    if (BIND_àdírẹ́ẹ̀sì(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BIND_àdírẹ́ẹ̀sì(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (BIND_àdírẹ́ẹ̀sì(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Àkóónú_iye[] = "한글 UDP loopback 😀";
    char 받은값[64] = {};
    if (자료전문보내기(보내는곳, Àkóónú_iye, sizeof(Àkóónú_iye), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Àkóónú_iye)) return 5;
    if (자료전문받기(받는곳, (void *)Àkóónú_iye, sizeof(Àkóónú_iye), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, (통신주소 *)&보낸주소, &àdírẹ́ẹ̀sì_gígùn) != sizeof(Àkóónú_iye)) return 7;
    if (àdírẹ́ẹ̀sì_gígùn != sizeof(보낸주소) || 장치차례짧은수(보낸주소.접속번호) != 7778 || ohun_èlò_ìtodátà_nọ́ńbà_odindi(보낸주소.àdíréẹ̀sì_íntánẹ́ẹ̀tì.àdírẹ́ẹ̀sì_iye) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Àkóónú_iye); 순번++) if (받은값[순번] != Àkóónú_iye[순번]) return 9;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, 받은값, sizeof(Àkóónú_iye), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Àkóónú_iye)) return 11;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Àkóónú_iye, sizeof(Àkóónú_iye), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Àkóónú_iye)) return 14;
    if (자료전문보내기(보내는곳, Àkóónú_iye, sizeof(Àkóónú_iye), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != sizeof(Àkóónú_iye)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.àdíréẹ̀sì_íntánẹ́ẹ̀tì.àdírẹ́ẹ̀sì_iye = Alásopọ̀_nọ́ńbà_odindi(0x08080808);
    if (자료전문보내기(보내는곳, Àkóónú_iye, sizeof(Àkóónú_iye), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(Íntánẹ́ẹ̀tì_Ẹbí, Stream_Alásopọ̀, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    àdírẹ́ẹ̀sì_gígùn = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &àdírẹ́ẹ̀sì_gígùn) || 장치차례짧은수(보낸주소.접속번호) != 7777) return 19;
    if (pa_dé_fáìlì(받는곳) || pa_dé_fáìlì(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: jáde_àtòjọ_ètò 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    kọ_fáìlì_détà(1, 완료, sizeof(완료) - 1);
    return 0;
}
