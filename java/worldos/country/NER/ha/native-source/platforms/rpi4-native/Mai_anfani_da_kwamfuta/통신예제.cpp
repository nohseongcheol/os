#include "통신규약.h"
static 인터넷통신주소 imel(unsigned fot_Daraja) {
    인터넷통신주소 Daraja = {}; Daraja.imel_Iyali = Intanet_Iyali;
    Daraja.lambar_kafa = 망차례짧은수(fot_Daraja); Daraja.Adireshin_yanar_gizo.imel_Daraja = Hanyar_sadarwa_Lamba_mara(되돌림주소); return Daraja;
}
extern "C" int Fara_Mai_anfani_da_kwamfuta_Shiri(int) {
    int 보내는곳 = 통신종단점만들기(Intanet_Iyali, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(Intanet_Iyali, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = imel(7777), 출발 = imel(7778), 보낸주소 = {};
    통신주소길이형 imel_Tsawo = sizeof(보낸주소);
    if (BIND_imel(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BIND_imel(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (BIND_imel(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char kunshiya_Daraja[] = "한글 UDP loopback 😀";
    char 받은값[64] = {};
    if (자료전문보내기(보내는곳, kunshiya_Daraja, sizeof(kunshiya_Daraja), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(kunshiya_Daraja)) return 5;
    if (자료전문받기(받는곳, (void *)kunshiya_Daraja, sizeof(kunshiya_Daraja), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, (통신주소 *)&보낸주소, &imel_Tsawo) != sizeof(kunshiya_Daraja)) return 7;
    if (imel_Tsawo != sizeof(보낸주소) || 장치차례짧은수(보낸주소.lambar_kafa) != 7778 || na_ura_Hanyar_jejjerawa_Lamba_mara(보낸주소.Adireshin_yanar_gizo.imel_Daraja) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(kunshiya_Daraja); 순번++) if (받은값[순번] != kunshiya_Daraja[순번]) return 9;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, 받은값, sizeof(kunshiya_Daraja), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(kunshiya_Daraja)) return 11;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, kunshiya_Daraja, sizeof(kunshiya_Daraja), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(kunshiya_Daraja)) return 14;
    if (자료전문보내기(보내는곳, kunshiya_Daraja, sizeof(kunshiya_Daraja), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != sizeof(kunshiya_Daraja)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.Adireshin_yanar_gizo.imel_Daraja = Hanyar_sadarwa_Lamba_mara(0x08080808);
    if (자료전문보내기(보내는곳, kunshiya_Daraja, sizeof(kunshiya_Daraja), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(Intanet_Iyali, watsuwa_Hanyar_sadarwa, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    imel_Tsawo = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &imel_Tsawo) || 장치차례짧은수(보낸주소.lambar_kafa) != 7777) return 19;
    if (Rufe_Fayil(받는곳) || Rufe_Fayil(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: Mafita_Shiri 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    Rubuta_Fayil_Tarin_bayani(1, 완료, sizeof(완료) - 1);
    return 0;
}
