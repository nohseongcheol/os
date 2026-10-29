#include "rete_ABI.h"
static cloud_socket_e_mail e_mail(unsigned porta_VALORE) {
    cloud_socket_e_mail VALORE = {}; VALORE.e_mail_serie = cloud_serie;
    VALORE.numero_di_porta = 망차례짧은수(porta_VALORE); VALORE.indirizzo_Internet.e_mail_VALORE = rete_intero(indirizzo_di_loopback); return VALORE;
}
extern "C" int START_USER_app(int) {
    int 보내는곳 = Crea_endpoint(cloud_serie, socket_di_datagramma, 0);
    int 받는곳 = Crea_endpoint(cloud_serie, socket_di_datagramma, datagramma_protocollo);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    cloud_socket_e_mail 도착 = e_mail(7777), 출발 = e_mail(7778), 보낸주소 = {};
    socket_e_mail_durata_TIPO e_mail_durata = sizeof(보낸주소);
    if (BIND_e_mail(받는곳, (socket_e_mail *)&도착, sizeof(도착))) return 2;
    if (BIND_e_mail(보내는곳, (socket_e_mail *)&도착, sizeof(도착)) != -1 || numero_errore != 98) return 3;
    if (BIND_e_mail(보내는곳, (socket_e_mail *)&출발, sizeof(출발))) return 4;
    static const char Contenuto_VALORE[] = "한글 UDP loopback 😀";
    char RICEV_SCAD_VALORE[64] = {};
    if (inviare_datagramma_dati(보내는곳, Contenuto_VALORE, sizeof(Contenuto_VALORE), 0, (socket_e_mail *)&도착, sizeof(도착)) != sizeof(Contenuto_VALORE)) return 5;
    if (ricevere_datagramma_dati(받는곳, (void *)Contenuto_VALORE, sizeof(Contenuto_VALORE), 0, 0, 0) != -1 || numero_errore != 14) return 6;
    if (ricevere_datagramma_dati(받는곳, RICEV_SCAD_VALORE, sizeof(RICEV_SCAD_VALORE), 0, (socket_e_mail *)&보낸주소, &e_mail_durata) != sizeof(Contenuto_VALORE)) return 7;
    if (e_mail_durata != sizeof(보낸주소) || 장치차례짧은수(보낸주소.numero_di_porta) != 7778 || cellulare_ordine_intero(보낸주소.indirizzo_Internet.e_mail_VALORE) != indirizzo_di_loopback) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Contenuto_VALORE); 순번++) if (RICEV_SCAD_VALORE[순번] != Contenuto_VALORE[순번]) return 9;
    if (ricevere_datagramma_dati(받는곳, RICEV_SCAD_VALORE, sizeof(RICEV_SCAD_VALORE), 0, 0, 0) != -1 || numero_errore != 11) return 10;
    if (inviare_datagramma_dati(받는곳, RICEV_SCAD_VALORE, sizeof(Contenuto_VALORE), 0, (socket_e_mail *)&보낸주소, sizeof(보낸주소)) != sizeof(Contenuto_VALORE)) return 11;
    if (ricevere_datagramma_dati(보내는곳, RICEV_SCAD_VALORE, 4, 0, 0, 0) != 4) return 12;
    if (ricevere_datagramma_dati(보내는곳, RICEV_SCAD_VALORE, 4, 0, 0, 0) != -1 || numero_errore != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (inviare_datagramma_dati(보내는곳, Contenuto_VALORE, sizeof(Contenuto_VALORE), 0, (socket_e_mail *)&도착, sizeof(도착)) != sizeof(Contenuto_VALORE)) return 14;
    if (inviare_datagramma_dati(보내는곳, Contenuto_VALORE, sizeof(Contenuto_VALORE), 0, (socket_e_mail *)&도착, sizeof(도착)) != -1 || numero_errore != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (ricevere_datagramma_dati(받는곳, RICEV_SCAD_VALORE, sizeof(RICEV_SCAD_VALORE), 0, 0, 0) != sizeof(Contenuto_VALORE)) return 16;
    if (inviare_datagramma_dati(보내는곳, 0, 0, 0, (socket_e_mail *)&도착, sizeof(도착)) != 0 ||
        ricevere_datagramma_dati(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.indirizzo_Internet.e_mail_VALORE = rete_intero(0x08080808);
    if (inviare_datagramma_dati(보내는곳, Contenuto_VALORE, sizeof(Contenuto_VALORE), 0, (socket_e_mail *)&도착, sizeof(도착)) != -1 || numero_errore != 101) return 17;
    if (Crea_endpoint(cloud_serie, Stream_rete, datagramma_protocollo) != -1 || numero_errore != 93) return 18;
    e_mail_durata = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (socket_e_mail *)&보낸주소, &e_mail_durata) || 장치차례짧은수(보낸주소.numero_di_porta) != 7777) return 19;
    if (Chiudi_File(받는곳) || Chiudi_File(받는곳) != -1 || numero_errore != 9) return 20;
    // 보내는곳은 열어 둔다: Esci_app 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    scrivere_File_dati(1, 완료, sizeof(완료) - 1);
    return 0;
}
