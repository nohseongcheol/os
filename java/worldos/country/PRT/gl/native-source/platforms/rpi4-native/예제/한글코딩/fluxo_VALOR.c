#include "통신규약.h"

int START_usuario_apl(int Argumentos) {
    (void)Argumentos;
    struct 인터넷통신주소 ENDEREZO = {0};
    ENDEREZO.ENDEREZO_Familia = nube_Familia;
    ENDEREZO.número_do_porto = 망차례짧은수(9260);
    ENDEREZO.enderezo_de_internet.ENDEREZO_VALOR = Rede_número_enteiro(되돌림주소);
    int servidor_VALOR = crear_extremo(nube_Familia, fluxo_Rede, fluxo_protocolo_de_transporte);
    if (servidor_VALOR < 0 || ligar_ENDEREZO(servidor_VALOR, (struct 통신주소 *)&ENDEREZO, sizeof(ENDEREZO)) < 0 ||
        통신연결기다리기(servidor_VALOR, 4) < 0) return 1;
    if (aceptar_conexión_de_rede(servidor_VALOR, 0, 0) != -1 || número_de_erro != 11) return 2;
    int convidado_VALOR = crear_extremo(nube_Familia, fluxo_Rede, fluxo_protocolo_de_transporte);
    if (convidado_VALOR < 0 || CONECTAR_Rede(convidado_VALOR, (struct 통신주소 *)&ENDEREZO, sizeof(ENDEREZO)) < 0) return 3;
    int Conectar = aceptar_conexión_de_rede(servidor_VALOR, 0, 0);
    if (Conectar < 0) return 4;
    unsigned char 보낼것[1500], RECIBIDO_elemento[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int duración_VALOR = escribir_Ficheiro_datos(convidado_VALOR, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (duración_VALOR <= 0) return 5;
        보낸수 += duración_VALOR;
    }
    if (escribir_Ficheiro_datos(convidado_VALOR, 보낼것, 1) != -1 || número_de_erro != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 ATRÁS_VALOR EOF가 된다. */
    peche_Ficheiro(convidado_VALOR);
    int RECIBIDO_CONTAR = 0;
    while (RECIBIDO_CONTAR < 보낸수) {
        int duración_VALOR = 파일자료읽기(Conectar, RECIBIDO_elemento + RECIBIDO_CONTAR, sizeof(RECIBIDO_elemento) - RECIBIDO_CONTAR);
        if (duración_VALOR <= 0) return 7;
        RECIBIDO_CONTAR += duración_VALOR;
    }
    for (int 수 = 0; 수 < RECIBIDO_CONTAR; 수++) if (RECIBIDO_elemento[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Conectar, RECIBIDO_elemento, 1) != 0) return 9;
    if (escribir_Ficheiro_datos(Conectar, 보낼것, 1) != -1 || número_de_erro != 32) return 10;
    peche_Ficheiro(Conectar); peche_Ficheiro(servidor_VALOR);
    const char RESULTANTE[] = "C posix-kor 연결형 통신 PASS\n";
    escribir_Ficheiro_datos(1, RESULTANTE, sizeof(RESULTANTE) - 1);
    return 0;
}
