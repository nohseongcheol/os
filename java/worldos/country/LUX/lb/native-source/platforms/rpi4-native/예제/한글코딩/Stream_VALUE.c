#include "통신규약.h"

int Start_Benotzer_App(int 인수) {
    (void)인수;
    struct 인터넷통신주소 Adress = {0};
    Adress.Adress_Famill = Cloud_Famill;
    Adress.접속번호 = 망차례짧은수(9260);
    Adress.Internetsadress.Adress_VALUE = Reseau_Ganzzuel(되돌림주소);
    int Server_VALUE = 통신종단점만들기(Cloud_Famill, Stream_Reseau, 흐름전송규약);
    if (Server_VALUE < 0 || BANNEN_Adress(Server_VALUE, (struct 통신주소 *)&Adress, sizeof(Adress)) < 0 ||
        통신연결기다리기(Server_VALUE, 4) < 0) return 1;
    if (acceptéieren_Netzwierksverbindung(Server_VALUE, 0, 0) != -1 || 오류번호 != 11) return 2;
    int Gaascht_VALUE = 통신종단점만들기(Cloud_Famill, Stream_Reseau, 흐름전송규약);
    if (Gaascht_VALUE < 0 || Verbannen_Reseau(Gaascht_VALUE, (struct 통신주소 *)&Adress, sizeof(Adress)) < 0) return 3;
    int Verbannen = acceptéieren_Netzwierksverbindung(Server_VALUE, 0, 0);
    if (Verbannen < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_Element[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int Längt_VALUE = schreiwen_Fichier_Daten(Gaascht_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (Längt_VALUE <= 0) return 5;
        보낸수 += Längt_VALUE;
    }
    if (schreiwen_Fichier_Daten(Gaascht_VALUE, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Zeréck_VALUE EOF가 된다. */
    Clôture_Fichier(Gaascht_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int Längt_VALUE = 파일자료읽기(Verbannen, RECEIVED_Element + RECEIVED_COUNT, sizeof(RECEIVED_Element) - RECEIVED_COUNT);
        if (Längt_VALUE <= 0) return 7;
        RECEIVED_COUNT += Längt_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_Element[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Verbannen, RECEIVED_Element, 1) != 0) return 9;
    if (schreiwen_Fichier_Daten(Verbannen, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    Clôture_Fichier(Verbannen); Clôture_Fichier(Server_VALUE);
    const char Mooss[] = "C posix-kor 연결형 통신 PASS\n";
    schreiwen_Fichier_Daten(1, Mooss, sizeof(Mooss) - 1);
    return 0;
}
