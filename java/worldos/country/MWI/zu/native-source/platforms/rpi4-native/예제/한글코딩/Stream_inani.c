#include "통신규약.h"

int qala_umsebenzisi_i_app(int 인수) {
    (void)인수;
    struct 인터넷통신주소 ikheli = {0};
    ikheli.ikheli_Umndeni = I_cloud_Umndeni;
    ikheli.접속번호 = 망차례짧은수(9260);
    ikheli.ikheli_le_inthanethi.ikheli_inani = iNethiwekhi_inamba(되돌림주소);
    int Iseva_inani = 통신종단점만들기(I_cloud_Umndeni, Stream_iNethiwekhi, 흐름전송규약);
    if (Iseva_inani < 0 || i_BIND_ikheli(Iseva_inani, (struct 통신주소 *)&ikheli, sizeof(ikheli)) < 0 ||
        통신연결기다리기(Iseva_inani, 4) < 0) return 1;
    if (yamukela_uxhumano_lwenethiwekhi(Iseva_inani, 0, 0) != -1 || 오류번호 != 11) return 2;
    int isivakashi_inani = 통신종단점만들기(I_cloud_Umndeni, Stream_iNethiwekhi, 흐름전송규약);
    if (isivakashi_inani < 0 || xhuma_iNethiwekhi(isivakashi_inani, (struct 통신주소 *)&ikheli, sizeof(ikheli)) < 0) return 3;
    int Xhumanisa = yamukela_uxhumano_lwenethiwekhi(Iseva_inani, 0, 0);
    if (Xhumanisa < 0) return 4;
    unsigned char 보낼것[1500], 받은것[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int ubude_inani = bhala_ifayela_imininingwane(isivakashi_inani, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (ubude_inani <= 0) return 5;
        보낸수 += ubude_inani;
    }
    if (bhala_ifayela_imininingwane(isivakashi_inani, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Impindamuva_inani EOF가 된다. */
    vala_ifayela(isivakashi_inani);
    int 받은수 = 0;
    while (받은수 < 보낸수) {
        int ubude_inani = 파일자료읽기(Xhumanisa, 받은것 + 받은수, sizeof(받은것) - 받은수);
        if (ubude_inani <= 0) return 7;
        받은수 += ubude_inani;
    }
    for (int 수 = 0; 수 < 받은수; 수++) if (받은것[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Xhumanisa, 받은것, 1) != 0) return 9;
    if (bhala_ifayela_imininingwane(Xhumanisa, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    vala_ifayela(Xhumanisa); vala_ifayela(Iseva_inani);
    const char 결과[] = "C posix-kor 연결형 통신 PASS\n";
    bhala_ifayela_imininingwane(1, 결과, sizeof(결과) - 1);
    return 0;
}
