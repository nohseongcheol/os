#include "통신규약.h"
static 인터넷통신주소 адреса(unsigned порта_VALUE) {
    인터넷통신주소 VALUE = {}; VALUE.адреса_семејни = облак_семејни;
    VALUE.број_на_порта = 망차례짧은수(порта_VALUE); VALUE.Интернет_адреса.адреса_VALUE = Мрежа_цел_број(адреса_на_неуспешен_обид_за_остварување_на_врска); return VALUE;
}
extern "C" int Start_корисник_програма(int) {
    int 보내는곳 = 통신종단점만들기(облак_семејни, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(облак_семејни, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = адреса(7777), 출발 = адреса(7778), 보낸주소 = {};
    통신주소길이형 адреса_должина = sizeof(보낸주소);
    if (БИНД_адреса(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (БИНД_адреса(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (БИНД_адреса(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Содржина_VALUE[] = "한글 UDP loopback 😀";
    char RECEIVED_VALUE[64] = {};
    if (자료전문보내기(보내는곳, Содржина_VALUE, sizeof(Содржина_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Содржина_VALUE)) return 5;
    if (자료전문받기(받는곳, (void *)Содржина_VALUE, sizeof(Содржина_VALUE), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, (통신주소 *)&보낸주소, &адреса_должина) != sizeof(Содржина_VALUE)) return 7;
    if (адреса_должина != sizeof(보낸주소) || 장치차례짧은수(보낸주소.број_на_порта) != 7778 || уред_редослед_цел_број(보낸주소.Интернет_адреса.адреса_VALUE) != адреса_на_неуспешен_обид_за_остварување_на_врска) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Содржина_VALUE); 순번++) if (RECEIVED_VALUE[순번] != Содржина_VALUE[순번]) return 9;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, RECEIVED_VALUE, sizeof(Содржина_VALUE), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Содржина_VALUE)) return 11;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Содржина_VALUE, sizeof(Содржина_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Содржина_VALUE)) return 14;
    if (자료전문보내기(보내는곳, Содржина_VALUE, sizeof(Содржина_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != sizeof(Содржина_VALUE)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.Интернет_адреса.адреса_VALUE = Мрежа_цел_број(0x08080808);
    if (자료전문보내기(보내는곳, Содржина_VALUE, sizeof(Содржина_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(облак_семејни, Stream_Мрежа, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    адреса_должина = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &адреса_должина) || 장치차례짧은수(보낸주소.број_на_порта) != 7777) return 19;
    if (затвори_датотека(받는곳) || затвори_датотека(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: Излез_програма 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    запиши_датотека_податоци(1, 완료, sizeof(완료) - 1);
    return 0;
}
