#include "통신규약.h"

int Başla_istifadəçi_proqram(int 인수) {
    (void)인수;
    struct 인터넷통신주소 ünvan = {0};
    ünvan.ünvan_Ailə = bulud_Ailə;
    ünvan.접속번호 = 망차례짧은수(9260);
    ünvan.İnternet_ünvanı.ünvan_VALUE = Şəbəkə_tam_ədəd(qapalı_ünvan);
    int server_VALUE = 통신종단점만들기(bulud_Ailə, axın_Şəbəkə, 흐름전송규약);
    if (server_VALUE < 0 || BIND_ünvan(server_VALUE, (struct 통신주소 *)&ünvan, sizeof(ünvan)) < 0 ||
        통신연결기다리기(server_VALUE, 4) < 0) return 1;
    if (qəbul_et_şəbəkə_bağlantısı(server_VALUE, 0, 0) != -1 || 오류번호 != 11) return 2;
    int qonaq_VALUE = 통신종단점만들기(bulud_Ailə, axın_Şəbəkə, 흐름전송규약);
    if (qonaq_VALUE < 0 || QOŞUN_Şəbəkə(qonaq_VALUE, (struct 통신주소 *)&ünvan, sizeof(ünvan)) < 0) return 3;
    int Bağlan = qəbul_et_şəbəkə_bağlantısı(server_VALUE, 0, 0);
    if (Bağlan < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_element[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int uzunluq_VALUE = yazmaq_fayl_verilənlər(qonaq_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (uzunluq_VALUE <= 0) return 5;
        보낸수 += uzunluq_VALUE;
    }
    if (yazmaq_fayl_verilənlər(qonaq_VALUE, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 GERİ_VALUE EOF가 된다. */
    bağlamaq_fayl(qonaq_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int uzunluq_VALUE = 파일자료읽기(Bağlan, RECEIVED_element + RECEIVED_COUNT, sizeof(RECEIVED_element) - RECEIVED_COUNT);
        if (uzunluq_VALUE <= 0) return 7;
        RECEIVED_COUNT += uzunluq_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_element[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Bağlan, RECEIVED_element, 1) != 0) return 9;
    if (yazmaq_fayl_verilənlər(Bağlan, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    bağlamaq_fayl(Bağlan); bağlamaq_fayl(server_VALUE);
    const char ölçü[] = "C posix-kor 연결형 통신 PASS\n";
    yazmaq_fayl_verilənlər(1, ölçü, sizeof(ölçü) - 1);
    return 0;
}
