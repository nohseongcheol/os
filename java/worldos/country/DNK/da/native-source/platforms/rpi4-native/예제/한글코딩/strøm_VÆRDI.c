#include "통신규약.h"

int START_bruger_app(int Argumenter) {
    (void)Argumenter;
    struct net_socket_mail mail = {0};
    mail.mail_serie = net_serie;
    mail.portnummer = 망차례짧은수(9260);
    mail.internetadresse.mail_VÆRDI = netværk_heltal(tilbagekoblingsadresse);
    int server_VÆRDI = åbne_slutpunkt(net_serie, strøm_netværk, strøm_transportprotokol);
    if (server_VÆRDI < 0 || BIND_mail(server_VÆRDI, (struct socket_mail *)&mail, sizeof(mail)) < 0 ||
        통신연결기다리기(server_VÆRDI, 4) < 0) return 1;
    if (acceptere_netværksforbindelse(server_VÆRDI, 0, 0) != -1 || fejlnummer != 11) return 2;
    int gæst_VÆRDI = åbne_slutpunkt(net_serie, strøm_netværk, strøm_transportprotokol);
    if (gæst_VÆRDI < 0 || Forbind_netværk(gæst_VÆRDI, (struct socket_mail *)&mail, sizeof(mail)) < 0) return 3;
    int Tilslut = acceptere_netværksforbindelse(server_VÆRDI, 0, 0);
    if (Tilslut < 0) return 4;
    unsigned char 보낼것[1500], MODTAGET_VED_UDLØB_vare[1500];
    for (int tal = 0; tal < 1500; tal++) 보낼것[tal] = (unsigned char)tal;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int varighed_VÆRDI = skrive_fil_data(gæst_VÆRDI, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (varighed_VÆRDI <= 0) return 5;
        보낸수 += varighed_VÆRDI;
    }
    if (skrive_fil_data(gæst_VÆRDI, 보낼것, 1) != -1 || fejlnummer != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 BACK_VÆRDI EOF가 된다. */
    Luk_fil(gæst_VÆRDI);
    int MODTAGET_VED_UDLØB_TÆL = 0;
    while (MODTAGET_VED_UDLØB_TÆL < 보낸수) {
        int varighed_VÆRDI = 파일자료읽기(Tilslut, MODTAGET_VED_UDLØB_vare + MODTAGET_VED_UDLØB_TÆL, sizeof(MODTAGET_VED_UDLØB_vare) - MODTAGET_VED_UDLØB_TÆL);
        if (varighed_VÆRDI <= 0) return 7;
        MODTAGET_VED_UDLØB_TÆL += varighed_VÆRDI;
    }
    for (int tal = 0; tal < MODTAGET_VED_UDLØB_TÆL; tal++) if (MODTAGET_VED_UDLØB_vare[tal] != 보낼것[tal]) return 8;
    if (파일자료읽기(Tilslut, MODTAGET_VED_UDLØB_vare, 1) != 0) return 9;
    if (skrive_fil_data(Tilslut, 보낼것, 1) != -1 || fejlnummer != 32) return 10;
    Luk_fil(Tilslut); Luk_fil(server_VÆRDI);
    const char KR[] = "C posix-kor 연결형 통신 PASS\n";
    skrive_fil_data(1, KR, sizeof(KR) - 1);
    return 0;
}
