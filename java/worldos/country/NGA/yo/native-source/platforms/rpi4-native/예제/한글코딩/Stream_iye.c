#include "통신규약.h"

int bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò(int 인수) {
    (void)인수;
    struct 인터넷통신주소 àdírẹ́ẹ̀sì = {0};
    àdírẹ́ẹ̀sì.àdírẹ́ẹ̀sì_Ẹbí = Íntánẹ́ẹ̀tì_Ẹbí;
    àdírẹ́ẹ̀sì.접속번호 = 망차례짧은수(9260);
    àdírẹ́ẹ̀sì.àdíréẹ̀sì_íntánẹ́ẹ̀tì.àdírẹ́ẹ̀sì_iye = Alásopọ̀_nọ́ńbà_odindi(되돌림주소);
    int apèsè_iye = 통신종단점만들기(Íntánẹ́ẹ̀tì_Ẹbí, Stream_Alásopọ̀, 흐름전송규약);
    if (apèsè_iye < 0 || BIND_àdírẹ́ẹ̀sì(apèsè_iye, (struct 통신주소 *)&àdírẹ́ẹ̀sì, sizeof(àdírẹ́ẹ̀sì)) < 0 ||
        통신연결기다리기(apèsè_iye, 4) < 0) return 1;
    if (gbà_ìsopọ̀_alásopọ̀(apèsè_iye, 0, 0) != -1 || 오류번호 != 11) return 2;
    int àlejò_iye = 통신종단점만들기(Íntánẹ́ẹ̀tì_Ẹbí, Stream_Alásopọ̀, 흐름전송규약);
    if (àlejò_iye < 0 || SOMỌ́_Alásopọ̀(àlejò_iye, (struct 통신주소 *)&àdírẹ́ẹ̀sì, sizeof(àdírẹ́ẹ̀sì)) < 0) return 3;
    int Darapọ̀ = gbà_ìsopọ̀_alásopọ̀(apèsè_iye, 0, 0);
    if (Darapọ̀ < 0) return 4;
    unsigned char 보낼것[1500], 받은것[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int gígùn_iye = kọ_fáìlì_détà(àlejò_iye, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (gígùn_iye <= 0) return 5;
        보낸수 += gígùn_iye;
    }
    if (kọ_fáìlì_détà(àlejò_iye, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Padà_sẹ́yìn_iye EOF가 된다. */
    pa_dé_fáìlì(àlejò_iye);
    int 받은수 = 0;
    while (받은수 < 보낸수) {
        int gígùn_iye = 파일자료읽기(Darapọ̀, 받은것 + 받은수, sizeof(받은것) - 받은수);
        if (gígùn_iye <= 0) return 7;
        받은수 += gígùn_iye;
    }
    for (int 수 = 0; 수 < 받은수; 수++) if (받은것[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Darapọ̀, 받은것, 1) != 0) return 9;
    if (kọ_fáìlì_détà(Darapọ̀, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    pa_dé_fáìlì(Darapọ̀); pa_dé_fáìlì(apèsè_iye);
    const char 결과[] = "C posix-kor 연결형 통신 PASS\n";
    kọ_fáìlì_détà(1, 결과, sizeof(결과) - 1);
    return 0;
}
