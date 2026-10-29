#include "통신규약.h"
static 인터넷통신주소 àdreèsì(unsigned pọọt_valuu) {
    인터넷통신주소 valuu = {}; valuu.àdreèsì_Ezinụlọ = urukpu_Ezinụlọ;
    valuu.접속번호 = 망차례짧은수(pọọt_valuu); valuu.adreesi_ịntaneèt.àdreèsì_valuu = Netwọọkụ_ọnụọgụ_nzùrùòkè(되돌림주소); return valuu;
}
extern "C" int Mbido_òjìàrụ_app(int) {
    int 보내는곳 = 통신종단점만들기(urukpu_Ezinụlọ, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(urukpu_Ezinụlọ, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = àdreèsì(7777), 출발 = àdreèsì(7778), 보낸주소 = {};
    통신주소길이형 àdreèsì_ogologo = sizeof(보낸주소);
    if (JIKỌNYE_àdreèsì(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (JIKỌNYE_àdreèsì(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (JIKỌNYE_àdreèsì(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char ndịnà_valuu[] = "한글 UDP loopback 😀";
    char 받은값[64] = {};
    if (자료전문보내기(보내는곳, ndịnà_valuu, sizeof(ndịnà_valuu), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(ndịnà_valuu)) return 5;
    if (자료전문받기(받는곳, (void *)ndịnà_valuu, sizeof(ndịnà_valuu), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, (통신주소 *)&보낸주소, &àdreèsì_ogologo) != sizeof(ndịnà_valuu)) return 7;
    if (àdreèsì_ogologo != sizeof(보낸주소) || 장치차례짧은수(보낸주소.접속번호) != 7778 || njìarụ_ùsòrò_ọnụọgụ_nzùrùòkè(보낸주소.adreesi_ịntaneèt.àdreèsì_valuu) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(ndịnà_valuu); 순번++) if (받은값[순번] != ndịnà_valuu[순번]) return 9;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, 받은값, sizeof(ndịnà_valuu), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(ndịnà_valuu)) return 11;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, ndịnà_valuu, sizeof(ndịnà_valuu), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(ndịnà_valuu)) return 14;
    if (자료전문보내기(보내는곳, ndịnà_valuu, sizeof(ndịnà_valuu), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != sizeof(ndịnà_valuu)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.adreesi_ịntaneèt.àdreèsì_valuu = Netwọọkụ_ọnụọgụ_nzùrùòkè(0x08080808);
    if (자료전문보내기(보내는곳, ndịnà_valuu, sizeof(ndịnà_valuu), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(urukpu_Ezinụlọ, agịrị_Netwọọkụ, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    àdreèsì_ogologo = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &àdreèsì_ogologo) || 장치차례짧은수(보낸주소.접속번호) != 7777) return 19;
    if (mmechi_ọbọakwụkwọ(받는곳) || mmechi_ọbọakwụkwọ(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: pụọ_app 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    dee_ọbọakwụkwọ_datà(1, 완료, sizeof(완료) - 1);
    return 0;
}
