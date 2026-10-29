#include "통신규약.h"
static 인터넷통신주소 Adress(unsigned Port_VALUE) {
    인터넷통신주소 VALUE = {}; VALUE.Adress_Famill = Cloud_Famill;
    VALUE.접속번호 = 망차례짧은수(Port_VALUE); VALUE.Internetsadress.Adress_VALUE = Reseau_Ganzzuel(되돌림주소); return VALUE;
}
extern "C" int Start_Benotzer_App(int) {
    int 보내는곳 = 통신종단점만들기(Cloud_Famill, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(Cloud_Famill, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = Adress(7777), 출발 = Adress(7778), 보낸주소 = {};
    통신주소길이형 Adress_Längt = sizeof(보낸주소);
    if (BANNEN_Adress(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BANNEN_Adress(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (BANNEN_Adress(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Inhalt_VALUE[] = "한글 UDP loopback 😀";
    char RECEIVED_VALUE[64] = {};
    if (자료전문보내기(보내는곳, Inhalt_VALUE, sizeof(Inhalt_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Inhalt_VALUE)) return 5;
    if (자료전문받기(받는곳, (void *)Inhalt_VALUE, sizeof(Inhalt_VALUE), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, (통신주소 *)&보낸주소, &Adress_Längt) != sizeof(Inhalt_VALUE)) return 7;
    if (Adress_Längt != sizeof(보낸주소) || 장치차례짧은수(보낸주소.접속번호) != 7778 || Mobil_Reiefolleg_Ganzzuel(보낸주소.Internetsadress.Adress_VALUE) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Inhalt_VALUE); 순번++) if (RECEIVED_VALUE[순번] != Inhalt_VALUE[순번]) return 9;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, RECEIVED_VALUE, sizeof(Inhalt_VALUE), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Inhalt_VALUE)) return 11;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Inhalt_VALUE, sizeof(Inhalt_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Inhalt_VALUE)) return 14;
    if (자료전문보내기(보내는곳, Inhalt_VALUE, sizeof(Inhalt_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != sizeof(Inhalt_VALUE)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.Internetsadress.Adress_VALUE = Reseau_Ganzzuel(0x08080808);
    if (자료전문보내기(보내는곳, Inhalt_VALUE, sizeof(Inhalt_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(Cloud_Famill, Stream_Reseau, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    Adress_Längt = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &Adress_Längt) || 장치차례짧은수(보낸주소.접속번호) != 7777) return 19;
    if (Clôture_Fichier(받는곳) || Clôture_Fichier(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: Schluss_App 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    schreiwen_Fichier_Daten(1, 완료, sizeof(완료) - 1);
    return 0;
}
