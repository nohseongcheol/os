#include "rede_ABI.h"

int START_usuário_app(int argumentos) {
    (void)argumentos;
    struct malha_soquete_email Endereço = {0};
    Endereço.email_Família = malha_Família;
    Endereço.número_da_porta = 망차례짧은수(9260);
    Endereço.endereço_na_Internet.email_VALOR = rede_inteiro(endereço_de_loopback);
    int servidor_VALOR = Criar_empresa(malha_Família, fluxo_rede, fluxo_protocolo_de_transporte);
    if (servidor_VALOR < 0 || BIND_email(servidor_VALOR, (struct soquete_email *)&Endereço, sizeof(Endereço)) < 0 ||
        통신연결기다리기(servidor_VALOR, 4) < 0) return 1;
    if (aceitar_conexão_de_rede(servidor_VALOR, 0, 0) != -1 || número_do_erro != 11) return 2;
    int convidado_VALOR = Criar_empresa(malha_Família, fluxo_rede, fluxo_protocolo_de_transporte);
    if (convidado_VALOR < 0 || Conexão_rede(convidado_VALOR, (struct soquete_email *)&Endereço, sizeof(Endereço)) < 0) return 3;
    int Ligar = aceitar_conexão_de_rede(servidor_VALOR, 0, 0);
    if (Ligar < 0) return 4;
    unsigned char 보낼것[1500], RECEBER_item[1500];
    for (int número = 0; número < 1500; número++) 보낼것[número] = (unsigned char)número;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int duração_VALOR = gravar_Arquivo_dados(convidado_VALOR, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (duração_VALOR <= 0) return 5;
        보낸수 += duração_VALOR;
    }
    if (gravar_Arquivo_dados(convidado_VALOR, 보낼것, 1) != -1 || número_do_erro != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 BACK_VALOR EOF가 된다. */
    Close_Arquivo(convidado_VALOR);
    int RECEBER_CONT_NÚM = 0;
    while (RECEBER_CONT_NÚM < 보낸수) {
        int duração_VALOR = leitura_Arquivo_dados(Ligar, RECEBER_item + RECEBER_CONT_NÚM, sizeof(RECEBER_item) - RECEBER_CONT_NÚM);
        if (duração_VALOR <= 0) return 7;
        RECEBER_CONT_NÚM += duração_VALOR;
    }
    for (int número = 0; número < RECEBER_CONT_NÚM; número++) if (RECEBER_item[número] != 보낼것[número]) return 8;
    if (leitura_Arquivo_dados(Ligar, RECEBER_item, 1) != 0) return 9;
    if (gravar_Arquivo_dados(Ligar, 보낼것, 1) != -1 || número_do_erro != 32) return 10;
    Close_Arquivo(Ligar); Close_Arquivo(servidor_VALOR);
    const char resultado[] = "C posix-kor 연결형 comunicação PASS\n";
    gravar_Arquivo_dados(1, resultado, sizeof(resultado) - 1);
    return 0;
}
