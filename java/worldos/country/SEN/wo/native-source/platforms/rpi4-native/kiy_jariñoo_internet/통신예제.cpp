#include "통신규약.h"
static 인터넷통신주소 dëkkuwaay(unsigned jël_xëyma) {
    인터넷통신주소 xëyma = {}; xëyma.dëkkuwaay_Njaboot = net_Njaboot;
    xëyma.접속번호 = 망차례짧은수(jël_xëyma); xëyma.dëkkuwaayu_Internet.dëkkuwaay_xëyma = mbaal_lëmm(되돌림주소); return xëyma;
}
extern "C" int Door_kiy_jariñoo_internet_jëfekaay(int) {
    int 보내는곳 = 통신종단점만들기(net_Njaboot, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(net_Njaboot, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = dëkkuwaay(7777), 출발 = dëkkuwaay(7778), 보낸주소 = {};
    통신주소길이형 dëkkuwaay_diir = sizeof(보낸주소);
    if (BIND_dëkkuwaay(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BIND_dëkkuwaay(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (BIND_dëkkuwaay(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Këmb_xëyma[] = "한글 UDP loopback 😀";
    char 받은값[64] = {};
    if (자료전문보내기(보내는곳, Këmb_xëyma, sizeof(Këmb_xëyma), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Këmb_xëyma)) return 5;
    if (자료전문받기(받는곳, (void *)Këmb_xëyma, sizeof(Këmb_xëyma), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, (통신주소 *)&보낸주소, &dëkkuwaay_diir) != sizeof(Këmb_xëyma)) return 7;
    if (dëkkuwaay_diir != sizeof(보낸주소) || 장치차례짧은수(보낸주소.접속번호) != 7778 || toftal_toftale_lëmm(보낸주소.dëkkuwaayu_Internet.dëkkuwaay_xëyma) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Këmb_xëyma); 순번++) if (받은값[순번] != Këmb_xëyma[순번]) return 9;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, 받은값, sizeof(Këmb_xëyma), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Këmb_xëyma)) return 11;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Këmb_xëyma, sizeof(Këmb_xëyma), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Këmb_xëyma)) return 14;
    if (자료전문보내기(보내는곳, Këmb_xëyma, sizeof(Këmb_xëyma), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != sizeof(Këmb_xëyma)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.dëkkuwaayu_Internet.dëkkuwaay_xëyma = mbaal_lëmm(0x08080808);
    if (자료전문보내기(보내는곳, Këmb_xëyma, sizeof(Këmb_xëyma), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(net_Njaboot, dawal_mbaal, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    dëkkuwaay_diir = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &dëkkuwaay_diir) || 장치차례짧은수(보낸주소.접속번호) != 7777) return 19;
    if (Tej_bara_denc(받는곳) || Tej_bara_denc(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: Génn_jëfekaay 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    biir_bara_denc_mbir(1, 완료, sizeof(완료) - 1);
    return 0;
}
