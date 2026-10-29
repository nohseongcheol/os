#include "통신규약.h"

int Start_foydalanuvchi_ilova(int 인수) {
    (void)인수;
    struct 인터넷통신주소 manzil = {0};
    manzil.manzil_Oila = bulut_Oila;
    manzil.접속번호 = 망차례짧은수(9260);
    manzil.Internetdagi_manzil.manzil_VALUE = Tarmoq_butun_son(되돌림주소);
    int server_VALUE = 통신종단점만들기(bulut_Oila, oqim_Tarmoq, 흐름전송규약);
    if (server_VALUE < 0 || BOG_LAMOQ_manzil(server_VALUE, (struct 통신주소 *)&manzil, sizeof(manzil)) < 0 ||
        통신연결기다리기(server_VALUE, 4) < 0) return 1;
    if (qabul_qilish_tarmoq_ulanishi(server_VALUE, 0, 0) != -1 || 오류번호 != 11) return 2;
    int mehmon_VALUE = 통신종단점만들기(bulut_Oila, oqim_Tarmoq, 흐름전송규약);
    if (mehmon_VALUE < 0 || ulash_Tarmoq(mehmon_VALUE, (struct 통신주소 *)&manzil, sizeof(manzil)) < 0) return 3;
    int Ulanish = qabul_qilish_tarmoq_ulanishi(server_VALUE, 0, 0);
    if (Ulanish < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_element[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int uzunlik_VALUE = yozmoq_fayl_ma_lumotlar(mehmon_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (uzunlik_VALUE <= 0) return 5;
        보낸수 += uzunlik_VALUE;
    }
    if (yozmoq_fayl_ma_lumotlar(mehmon_VALUE, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Orqaga_VALUE EOF가 된다. */
    yopmoq_fayl(mehmon_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int uzunlik_VALUE = 파일자료읽기(Ulanish, RECEIVED_element + RECEIVED_COUNT, sizeof(RECEIVED_element) - RECEIVED_COUNT);
        if (uzunlik_VALUE <= 0) return 7;
        RECEIVED_COUNT += uzunlik_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_element[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Ulanish, RECEIVED_element, 1) != 0) return 9;
    if (yozmoq_fayl_ma_lumotlar(Ulanish, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    yopmoq_fayl(Ulanish); yopmoq_fayl(server_VALUE);
    const char o_lchov[] = "C posix-kor 연결형 통신 PASS\n";
    yozmoq_fayl_ma_lumotlar(1, o_lchov, sizeof(o_lchov) - 1);
    return 0;
}
