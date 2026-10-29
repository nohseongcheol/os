#include "통신규약.h"
static 인터넷통신주소 idilesi(unsigned iphothi_ixabiso) {
    인터넷통신주소 ixabiso = {}; ixabiso.idilesi_Usapho = ilifu_Usapho;
    ixabiso.접속번호 = 망차례짧은수(iphothi_ixabiso); ixabiso.idilesi_yeintanethi.idilesi_ixabiso = Inethiwekhi_inani_elipheleleyo(되돌림주소); return ixabiso;
}
extern "C" int qala_umsebenzisi_inkqubo(int) {
    int 보내는곳 = 통신종단점만들기(ilifu_Usapho, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(ilifu_Usapho, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = idilesi(7777), 출발 = idilesi(7778), 보낸주소 = {};
    통신주소길이형 idilesi_ubude = sizeof(보낸주소);
    if (BOPHELELA_idilesi(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BOPHELELA_idilesi(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (BOPHELELA_idilesi(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Isiqulatho_ixabiso[] = "한글 UDP loopback 😀";
    char 받은값[64] = {};
    if (자료전문보내기(보내는곳, Isiqulatho_ixabiso, sizeof(Isiqulatho_ixabiso), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Isiqulatho_ixabiso)) return 5;
    if (자료전문받기(받는곳, (void *)Isiqulatho_ixabiso, sizeof(Isiqulatho_ixabiso), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, (통신주소 *)&보낸주소, &idilesi_ubude) != sizeof(Isiqulatho_ixabiso)) return 7;
    if (idilesi_ubude != sizeof(보낸주소) || 장치차례짧은수(보낸주소.접속번호) != 7778 || isixhobo_ulandelelwano_inani_elipheleleyo(보낸주소.idilesi_yeintanethi.idilesi_ixabiso) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Isiqulatho_ixabiso); 순번++) if (받은값[순번] != Isiqulatho_ixabiso[순번]) return 9;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, 받은값, sizeof(Isiqulatho_ixabiso), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Isiqulatho_ixabiso)) return 11;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Isiqulatho_ixabiso, sizeof(Isiqulatho_ixabiso), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Isiqulatho_ixabiso)) return 14;
    if (자료전문보내기(보내는곳, Isiqulatho_ixabiso, sizeof(Isiqulatho_ixabiso), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != sizeof(Isiqulatho_ixabiso)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.idilesi_yeintanethi.idilesi_ixabiso = Inethiwekhi_inani_elipheleleyo(0x08080808);
    if (자료전문보내기(보내는곳, Isiqulatho_ixabiso, sizeof(Isiqulatho_ixabiso), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(ilifu_Usapho, Stream_Inethiwekhi, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    idilesi_ubude = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &idilesi_ubude) || 장치차례짧은수(보낸주소.접속번호) != 7777) return 19;
    if (vala_ifayile(받는곳) || vala_ifayile(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: phuma_inkqubo 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    bhala_ifayile_iingcombolo(1, 완료, sizeof(완료) - 1);
    return 0;
}
