#include "통신규약.h"
static 인터넷통신주소 ünvan(unsigned port_VALUE) {
    인터넷통신주소 VALUE = {}; VALUE.ünvan_Ailə = bulud_Ailə;
    VALUE.접속번호 = 망차례짧은수(port_VALUE); VALUE.İnternet_ünvanı.ünvan_VALUE = Şəbəkə_tam_ədəd(qapalı_ünvan); return VALUE;
}
extern "C" int Başla_istifadəçi_proqram(int) {
    int 보내는곳 = 통신종단점만들기(bulud_Ailə, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(bulud_Ailə, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = ünvan(7777), 출발 = ünvan(7778), 보낸주소 = {};
    통신주소길이형 ünvan_uzunluq = sizeof(보낸주소);
    if (BIND_ünvan(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BIND_ünvan(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (BIND_ünvan(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Məzmun_VALUE[] = "한글 UDP loopback 😀";
    char RECEIVED_VALUE[64] = {};
    if (자료전문보내기(보내는곳, Məzmun_VALUE, sizeof(Məzmun_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Məzmun_VALUE)) return 5;
    if (자료전문받기(받는곳, (void *)Məzmun_VALUE, sizeof(Məzmun_VALUE), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, (통신주소 *)&보낸주소, &ünvan_uzunluq) != sizeof(Məzmun_VALUE)) return 7;
    if (ünvan_uzunluq != sizeof(보낸주소) || 장치차례짧은수(보낸주소.접속번호) != 7778 || cihaz_ardıcıllıq_tam_ədəd(보낸주소.İnternet_ünvanı.ünvan_VALUE) != qapalı_ünvan) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Məzmun_VALUE); 순번++) if (RECEIVED_VALUE[순번] != Məzmun_VALUE[순번]) return 9;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, RECEIVED_VALUE, sizeof(Məzmun_VALUE), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Məzmun_VALUE)) return 11;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Məzmun_VALUE, sizeof(Məzmun_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Məzmun_VALUE)) return 14;
    if (자료전문보내기(보내는곳, Məzmun_VALUE, sizeof(Məzmun_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != sizeof(Məzmun_VALUE)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.İnternet_ünvanı.ünvan_VALUE = Şəbəkə_tam_ədəd(0x08080808);
    if (자료전문보내기(보내는곳, Məzmun_VALUE, sizeof(Məzmun_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(bulud_Ailə, axın_Şəbəkə, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    ünvan_uzunluq = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &ünvan_uzunluq) || 장치차례짧은수(보낸주소.접속번호) != 7777) return 19;
    if (bağlamaq_fayl(받는곳) || bağlamaq_fayl(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: Çıxış_proqram 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    yazmaq_fayl_verilənlər(1, 완료, sizeof(완료) - 1);
    return 0;
}
