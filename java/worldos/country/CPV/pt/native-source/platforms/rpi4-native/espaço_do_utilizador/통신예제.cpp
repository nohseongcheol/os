#include "rede_ABI.h"
static malha_soquete_email Endereço(unsigned porta_VALOR) {
    malha_soquete_email VALOR = {}; VALOR.email_Família = malha_Família;
    VALOR.número_da_porta = 망차례짧은수(porta_VALOR); VALOR.endereço_na_Internet.email_VALOR = rede_inteiro(endereço_de_loopback); return VALOR;
}
extern "C" int START_usuário_app(int) {
    int 보내는곳 = Criar_empresa(malha_Família, datagrama_soquete, 0);
    int 받는곳 = Criar_empresa(malha_Família, datagrama_soquete, datagrama_protocolo);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    malha_soquete_email 도착 = Endereço(7777), 출발 = Endereço(7778), 보낸주소 = {};
    soquete_email_duração_TIPO email_duração = sizeof(보낸주소);
    if (BIND_email(받는곳, (soquete_email *)&도착, sizeof(도착))) return 2;
    if (BIND_email(보내는곳, (soquete_email *)&도착, sizeof(도착)) != -1 || número_do_erro != 98) return 3;
    if (BIND_email(보내는곳, (soquete_email *)&출발, sizeof(출발))) return 4;
    static const char Conteúdo_VALOR[] = "한글 UDP loopback 😀";
    char RECEBER_VALOR[64] = {};
    if (enviar_datagrama_dados(보내는곳, Conteúdo_VALOR, sizeof(Conteúdo_VALOR), 0, (soquete_email *)&도착, sizeof(도착)) != sizeof(Conteúdo_VALOR)) return 5;
    if (receber_datagrama_dados(받는곳, (void *)Conteúdo_VALOR, sizeof(Conteúdo_VALOR), 0, 0, 0) != -1 || número_do_erro != 14) return 6;
    if (receber_datagrama_dados(받는곳, RECEBER_VALOR, sizeof(RECEBER_VALOR), 0, (soquete_email *)&보낸주소, &email_duração) != sizeof(Conteúdo_VALOR)) return 7;
    if (email_duração != sizeof(보낸주소) || 장치차례짧은수(보낸주소.número_da_porta) != 7778 || celular_ordem_inteiro(보낸주소.endereço_na_Internet.email_VALOR) != endereço_de_loopback) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Conteúdo_VALOR); 순번++) if (RECEBER_VALOR[순번] != Conteúdo_VALOR[순번]) return 9;
    if (receber_datagrama_dados(받는곳, RECEBER_VALOR, sizeof(RECEBER_VALOR), 0, 0, 0) != -1 || número_do_erro != 11) return 10;
    if (enviar_datagrama_dados(받는곳, RECEBER_VALOR, sizeof(Conteúdo_VALOR), 0, (soquete_email *)&보낸주소, sizeof(보낸주소)) != sizeof(Conteúdo_VALOR)) return 11;
    if (receber_datagrama_dados(보내는곳, RECEBER_VALOR, 4, 0, 0, 0) != 4) return 12;
    if (receber_datagrama_dados(보내는곳, RECEBER_VALOR, 4, 0, 0, 0) != -1 || número_do_erro != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (enviar_datagrama_dados(보내는곳, Conteúdo_VALOR, sizeof(Conteúdo_VALOR), 0, (soquete_email *)&도착, sizeof(도착)) != sizeof(Conteúdo_VALOR)) return 14;
    if (enviar_datagrama_dados(보내는곳, Conteúdo_VALOR, sizeof(Conteúdo_VALOR), 0, (soquete_email *)&도착, sizeof(도착)) != -1 || número_do_erro != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (receber_datagrama_dados(받는곳, RECEBER_VALOR, sizeof(RECEBER_VALOR), 0, 0, 0) != sizeof(Conteúdo_VALOR)) return 16;
    if (enviar_datagrama_dados(보내는곳, 0, 0, 0, (soquete_email *)&도착, sizeof(도착)) != 0 ||
        receber_datagrama_dados(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.endereço_na_Internet.email_VALOR = rede_inteiro(0x08080808);
    if (enviar_datagrama_dados(보내는곳, Conteúdo_VALOR, sizeof(Conteúdo_VALOR), 0, (soquete_email *)&도착, sizeof(도착)) != -1 || número_do_erro != 101) return 17;
    if (Criar_empresa(malha_Família, fluxo_rede, datagrama_protocolo) != -1 || número_do_erro != 93) return 18;
    email_duração = sizeof(보낸주소);
    if (leitura_soquete_email(받는곳, (soquete_email *)&보낸주소, &email_duração) || 장치차례짧은수(보낸주소.número_da_porta) != 7777) return 19;
    if (Close_Arquivo(받는곳) || Close_Arquivo(받는곳) != -1 || número_do_erro != 9) return 20;
    // 보내는곳은 열어 둔다: sair_app 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    gravar_Arquivo_dados(1, 완료, sizeof(완료) - 1);
    return 0;
}
