#include "통신규약.h"
static 인터넷통신주소 turaarut(unsigned kapputigaq_atuutilik) {
    인터넷통신주소 atuutilik = {}; atuutilik.turaarut_illumiuqatigiit = cloud_illumiuqatigiit;
    atuutilik.접속번호 = 망차례짧은수(kapputigaq_atuutilik); atuutilik.Ikiaqqivikkut_turaarut.turaarut_atuutilik = Kasuqatigiitsimajut_naasaut(되돌림주소); return atuutilik;
}
extern "C" int pigiarli_atuqtuq_pilirijjut(int) {
    int 보내는곳 = 통신종단점만들기(cloud_illumiuqatigiit, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(cloud_illumiuqatigiit, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = turaarut(7777), 출발 = turaarut(7778), 보낸주소 = {};
    통신주소길이형 turaarut_takininga = sizeof(보낸주소);
    if (unittilli_turaarut(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (unittilli_turaarut(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (unittilli_turaarut(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Ilulingit_atuutilik[] = "한글 UDP loopback 😀";
    char 받은값[64] = {};
    if (자료전문보내기(보내는곳, Ilulingit_atuutilik, sizeof(Ilulingit_atuutilik), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Ilulingit_atuutilik)) return 5;
    if (자료전문받기(받는곳, (void *)Ilulingit_atuutilik, sizeof(Ilulingit_atuutilik), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, (통신주소 *)&보낸주소, &turaarut_takininga) != sizeof(Ilulingit_atuutilik)) return 7;
    if (turaarut_takininga != sizeof(보낸주소) || 장치차례짧은수(보낸주소.접속번호) != 7778 || sunakkutaaq_agguijjut_naasaut(보낸주소.Ikiaqqivikkut_turaarut.turaarut_atuutilik) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Ilulingit_atuutilik); 순번++) if (받은값[순번] != Ilulingit_atuutilik[순번]) return 9;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, 받은값, sizeof(Ilulingit_atuutilik), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Ilulingit_atuutilik)) return 11;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Ilulingit_atuutilik, sizeof(Ilulingit_atuutilik), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Ilulingit_atuutilik)) return 14;
    if (자료전문보내기(보내는곳, Ilulingit_atuutilik, sizeof(Ilulingit_atuutilik), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != sizeof(Ilulingit_atuutilik)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.Ikiaqqivikkut_turaarut.turaarut_atuutilik = Kasuqatigiitsimajut_naasaut(0x08080808);
    if (자료전문보내기(보내는곳, Ilulingit_atuutilik, sizeof(Ilulingit_atuutilik), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(cloud_illumiuqatigiit, ingirrania_aulataup_Kasuqatigiitsimajut, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    turaarut_takininga = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &turaarut_takininga) || 장치차례짧은수(보낸주소.접속번호) != 7777) return 19;
    if (matuli_ini(받는곳) || matuli_ini(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: taima_pilirijjut 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    titiraq_ini_titiqqat(1, 완료, sizeof(완료) - 1);
    return 0;
}
