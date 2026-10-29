#include "rete_ABI.h"

int START_USER_app(int argomenti) {
    (void)argomenti;
    struct cloud_socket_e_mail e_mail = {0};
    e_mail.e_mail_serie = cloud_serie;
    e_mail.numero_di_porta = 망차례짧은수(9260);
    e_mail.indirizzo_Internet.e_mail_VALORE = rete_intero(indirizzo_di_loopback);
    int server_VALORE = Crea_endpoint(cloud_serie, Stream_rete, Stream_protocollo_di_trasporto);
    if (server_VALORE < 0 || BIND_e_mail(server_VALORE, (struct socket_e_mail *)&e_mail, sizeof(e_mail)) < 0 ||
        통신연결기다리기(server_VALORE, 4) < 0) return 1;
    if (accettare_connessione_di_rete(server_VALORE, 0, 0) != -1 || numero_errore != 11) return 2;
    int guest_VALORE = Crea_endpoint(cloud_serie, Stream_rete, Stream_protocollo_di_trasporto);
    if (guest_VALORE < 0 || CONNETTI_rete(guest_VALORE, (struct socket_e_mail *)&e_mail, sizeof(e_mail)) < 0) return 3;
    int Connetti = accettare_connessione_di_rete(server_VALORE, 0, 0);
    if (Connetti < 0) return 4;
    unsigned char 보낼것[1500], RICEV_SCAD_articolo[1500];
    for (int numero = 0; numero < 1500; numero++) 보낼것[numero] = (unsigned char)numero;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int durata_VALORE = scrivere_File_dati(guest_VALORE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (durata_VALORE <= 0) return 5;
        보낸수 += durata_VALORE;
    }
    if (scrivere_File_dati(guest_VALORE, 보낼것, 1) != -1 || numero_errore != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 BACK_VALORE EOF가 된다. */
    Chiudi_File(guest_VALORE);
    int RICEV_SCAD_CONTA_NUMERI = 0;
    while (RICEV_SCAD_CONTA_NUMERI < 보낸수) {
        int durata_VALORE = 파일자료읽기(Connetti, RICEV_SCAD_articolo + RICEV_SCAD_CONTA_NUMERI, sizeof(RICEV_SCAD_articolo) - RICEV_SCAD_CONTA_NUMERI);
        if (durata_VALORE <= 0) return 7;
        RICEV_SCAD_CONTA_NUMERI += durata_VALORE;
    }
    for (int numero = 0; numero < RICEV_SCAD_CONTA_NUMERI; numero++) if (RICEV_SCAD_articolo[numero] != 보낼것[numero]) return 8;
    if (파일자료읽기(Connetti, RICEV_SCAD_articolo, 1) != 0) return 9;
    if (scrivere_File_dati(Connetti, 보낼것, 1) != -1 || numero_errore != 32) return 10;
    Chiudi_File(Connetti); Chiudi_File(server_VALORE);
    const char risultato[] = "C posix-kor 연결형 comunicazione PASS\n";
    scrivere_File_dati(1, risultato, sizeof(risultato) - 1);
    return 0;
}
