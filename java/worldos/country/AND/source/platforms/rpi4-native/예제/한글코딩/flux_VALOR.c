#include "통신규약.h"

int Inici_usuari_programa(int 인수) {
    (void)인수;
    struct 인터넷통신주소 Adreça = {0};
    Adreça.ADREÇA_Família = núvol_Família;
    Adreça.número_de_port = 망차례짧은수(9260);
    Adreça.adreça_d_Internet.ADREÇA_VALOR = 망차례정수(되돌림주소);
    int servidor_VALOR = Crear_extrem(núvol_Família, flux_xarxa, flux_protocol_de_transport);
    if (servidor_VALOR < 0 || enllaçar_ADREÇA(servidor_VALOR, (struct 통신주소 *)&Adreça, sizeof(Adreça)) < 0 ||
        통신연결기다리기(servidor_VALOR, 4) < 0) return 1;
    if (acceptar_connexió_de_xarxa(servidor_VALOR, 0, 0) != -1 || número_d_error != 11) return 2;
    int convidat_VALOR = Crear_extrem(núvol_Família, flux_xarxa, flux_protocol_de_transport);
    if (convidat_VALOR < 0 || CONNECTA_xarxa(convidat_VALOR, (struct 통신주소 *)&Adreça, sizeof(Adreça)) < 0) return 3;
    int Connecta = acceptar_connexió_de_xarxa(servidor_VALOR, 0, 0);
    if (Connecta < 0) return 4;
    unsigned char 보낼것[1500], CANTIDAD_RECIBIDA_element[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int durada_VALOR = escriure_arxiu_dades(convidat_VALOR, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (durada_VALOR <= 0) return 5;
        보낸수 += durada_VALOR;
    }
    if (escriure_arxiu_dades(convidat_VALOR, 보낼것, 1) != -1 || número_d_error != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 ENRERE_VALOR EOF가 된다. */
    Tanca_arxiu(convidat_VALOR);
    int CANTIDAD_RECIBIDA_COMPT = 0;
    while (CANTIDAD_RECIBIDA_COMPT < 보낸수) {
        int durada_VALOR = tancar_arxiu_dades(Connecta, CANTIDAD_RECIBIDA_element + CANTIDAD_RECIBIDA_COMPT, sizeof(CANTIDAD_RECIBIDA_element) - CANTIDAD_RECIBIDA_COMPT);
        if (durada_VALOR <= 0) return 7;
        CANTIDAD_RECIBIDA_COMPT += durada_VALOR;
    }
    for (int 수 = 0; 수 < CANTIDAD_RECIBIDA_COMPT; 수++) if (CANTIDAD_RECIBIDA_element[수] != 보낼것[수]) return 8;
    if (tancar_arxiu_dades(Connecta, CANTIDAD_RECIBIDA_element, 1) != 0) return 9;
    if (escriure_arxiu_dades(Connecta, 보낼것, 1) != -1 || número_d_error != 32) return 10;
    Tanca_arxiu(Connecta); Tanca_arxiu(servidor_VALOR);
    const char RESULTAT[] = "C posix-kor 연결형 통신 PASS\n";
    escriure_arxiu_dades(1, RESULTAT, sizeof(RESULTAT) - 1);
    return 0;
}
