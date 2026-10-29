#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "rete_Pila.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../remoto_VALORE/remoto_VALORE.h"
#include "cablato_rete.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define computer_registro(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif connessione_cellulare;
static int 준비됨, polling;
static int usare_cablato_rete;
static unsigned ricevere_utilizzo, 수신탈출, ricevere_errore;
static unsigned char ricevere_buffer_dei_dati[1600];
static unsigned char trasmettere_dati[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t RICEV_SCAD_datagramma_CONTA_NUMERI, 보낸전문수, RICEV_SCAD_byte_CONTA_NUMERI, 보낸바이트수, 버린전문수;
typedef struct {
    int TIPO_area, porta_di_ricezione, reparto_IT_In_sospeso, 연결됨, File_chiudere, errore;
    struct tcp_pcb *connessione_controllo;
    struct udp_pcb *datagramma_controllo;
    unsigned frontale_voce, voce_CONTA_NUMERI;
    unsigned char dati[4096];
    unsigned 길이목록[4], 접속번호들[4], peer_endpoint_numero;
    uint32_t 주소목록[4], peer_e_mail;
} socket_endpoint_3db661a2;
static socket_endpoint_3db661a2 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int numero_errore(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static socket_endpoint_3db661a2 *get_VALORE(int handle_di_file) { return handle_di_file >= 0 && handle_di_file < 32 && 통신끝점들[handle_di_file].TIPO_area ? &통신끝점들[handle_di_file] : 0; }
static int 예약하기(int TIPO_area) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TIPO_area) {
        memset(&통신끝점들[순번], 0, sizeof(socket_endpoint_3db661a2)); 통신끝점들[순번].TIPO_area = TIPO_area; 통신끝점들[순번].reparto_IT_In_sospeso = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned punto_di_codice) { trasmettere_dati[(송신앞자리 + 송신개수++) % sizeof(trasmettere_dati)] = punto_di_codice; }
static err_t output(struct netif *articolo_CONTA_NUMERI, struct pbuf *dati_funzione, const ip4_addr_t *e_mail) {
    (void)articolo_CONTA_NUMERI; (void)e_mail;
    if (dati_funzione->tot_len > 1500 || 송신개수 + 2 * dati_funzione->tot_len + 2 > sizeof(trasmettere_dati)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Avanti_SCARTO = dati_funzione; Avanti_SCARTO; Avanti_SCARTO = Avanti_SCARTO->next) for (unsigned 순번 = 0; 순번 < Avanti_SCARTO->len; 순번++) {
        unsigned punto_di_codice = ((unsigned char *)Avanti_SCARTO->payload)[순번];
        if (punto_di_codice == 192 || punto_di_codice == 219) { 내보내기(219); 내보내기(punto_di_codice == 192 ? 220 : 221); } else 내보내기(punto_di_codice);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += dati_funzione->tot_len; return ERR_OK;
}
static err_t Prepara_CLR(struct netif *articolo_CONTA_NUMERI) { articolo_CONTA_NUMERI->name[0] = 's'; articolo_CONTA_NUMERI->name[1] = 'l'; articolo_CONTA_NUMERI->mtu = 1500; articolo_CONTA_NUMERI->output = output; return ERR_OK; }
void Prepara_rete(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    computer_registro(보조장치 + 4) |= 1; computer_registro(보조장치 + 0x60) = 0; computer_registro(보조장치 + 0x44) = 0;
    computer_registro(보조장치 + 0x48) = 0xc6; computer_registro(보조장치 + 0x4c) = 3; computer_registro(보조장치 + 0x68) = 270; computer_registro(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t indirizzo_Internet, maschera_di_bit, indirizzo_del_gateway;
    usare_cablato_rete=유선장치있음();
    ip4_addr_set_u32(&indirizzo_Internet, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&maschera_di_bit, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&indirizzo_del_gateway, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&connessione_cellulare, &indirizzo_Internet, &maschera_di_bit, &indirizzo_del_gateway, 0, usare_cablato_rete?Prepara_cablato_rete:Prepara_CLR, usare_cablato_rete?ethernet_input:ip4_input))return;
    netif_set_default(&connessione_cellulare); netif_set_up(&connessione_cellulare);if(!usare_cablato_rete)netif_set_link_up(&connessione_cellulare); 준비됨 = 1;
    Prepara_remoto();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *trasmissione_controllo_Blocca, struct pbuf *dati_funzione, err_t errore) {
    socket_endpoint_3db661a2 *stringa_dati = 부가인수; (void)trasmissione_controllo_Blocca; (void)errore;
    if (!dati_funzione) { stringa_dati->File_chiudere = 1; return ERR_OK; }
    if (dati_funzione->tot_len > sizeof(stringa_dati->dati) - stringa_dati->voce_CONTA_NUMERI) return ERR_MEM;
    unsigned Regolari_funzione = (stringa_dati->frontale_voce + stringa_dati->voce_CONTA_NUMERI) % sizeof(stringa_dati->dati);
    for (struct pbuf *Avanti_SCARTO = dati_funzione; Avanti_SCARTO; Avanti_SCARTO = Avanti_SCARTO->next) for (unsigned 순번 = 0; 순번 < Avanti_SCARTO->len; 순번++) {
        stringa_dati->dati[Regolari_funzione] = ((unsigned char *)Avanti_SCARTO->payload)[순번]; Regolari_funzione = (Regolari_funzione + 1) % sizeof(stringa_dati->dati);
    }
    stringa_dati->voce_CONTA_NUMERI += dati_funzione->tot_len; pbuf_free(dati_funzione); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t errore) { socket_endpoint_3db661a2 *stringa_dati = 부가인수; stringa_dati->connessione_controllo = 0; stringa_dati->errore = numero_errore(errore); }
static void 되부름목록(socket_endpoint_3db661a2 *stringa_dati) { tcp_arg(stringa_dati->connessione_controllo, stringa_dati); tcp_recv(stringa_dati->connessione_controllo, 수신됨); tcp_err(stringa_dati->connessione_controllo, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *trasmissione_controllo_Blocca, err_t errore) {
    socket_endpoint_3db661a2 *stringa_dati = 부가인수; (void)trasmissione_controllo_Blocca; if (errore) stringa_dati->errore = numero_errore(errore); else stringa_dati->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *trasmissione_controllo_Blocca, err_t errore) {
    socket_endpoint_3db661a2 *padre = 부가인수; if (errore) return errore;
    int handle_di_file = 예약하기(1); if (handle_di_file < 0) return ERR_MEM;
    socket_endpoint_3db661a2 *stringa_dati = &통신끝점들[handle_di_file]; stringa_dati->connessione_controllo = trasmissione_controllo_Blocca; stringa_dati->연결됨 = 1; stringa_dati->reparto_IT_In_sospeso = (int)(padre - 통신끝점들);
    stringa_dati->peer_e_mail = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&trasmissione_controllo_Blocca->remote_ip))); stringa_dati->peer_endpoint_numero = trasmissione_controllo_Blocca->remote_port;
    되부름목록(stringa_dati); return ERR_OK;
}
static void datagramma(void *부가인수, struct udp_pcb *trasmissione_controllo_Blocca, struct pbuf *dati_funzione, const ip_addr_t *e_mail, u16_t numero_di_porta) {
    socket_endpoint_3db661a2 *stringa_dati = 부가인수; (void)trasmissione_controllo_Blocca;
    if (stringa_dati->voce_CONTA_NUMERI < 4 && dati_funzione->tot_len <= 512) {
        unsigned funzione_INDICE = (stringa_dati->frontale_voce + stringa_dati->voce_CONTA_NUMERI) % 4;
        pbuf_copy_partial(dati_funzione, stringa_dati->dati + funzione_INDICE * 512, dati_funzione->tot_len, 0);
        stringa_dati->길이목록[funzione_INDICE] = dati_funzione->tot_len; stringa_dati->접속번호들[funzione_INDICE] = numero_di_porta;
        stringa_dati->주소목록[funzione_INDICE] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(e_mail))); stringa_dati->voce_CONTA_NUMERI++;
    }
    pbuf_free(dati_funzione);
}
int Crea_socket_endpoint(int TIPO_area) {
    if (!준비됨) return -100;
    if (TIPO_area != 1 && TIPO_area != 2) return -93;
    int handle_di_file = 예약하기(TIPO_area); if (handle_di_file < 0) return handle_di_file;
    socket_endpoint_3db661a2 *stringa_dati = &통신끝점들[handle_di_file];
    if (TIPO_area == 1) { stringa_dati->connessione_controllo = tcp_new(); if (stringa_dati->connessione_controllo) 되부름목록(stringa_dati); }
    else { stringa_dati->datagramma_controllo = udp_new(); if (stringa_dati->datagramma_controllo) udp_recv(stringa_dati->datagramma_controllo, datagramma, stringa_dati); }
    if (!stringa_dati->connessione_controllo && !stringa_dati->datagramma_controllo) { stringa_dati->TIPO_area = 0; return -12; } return handle_di_file;
}
int NET_BIND(int handle_di_file, uint32_t e_mail, unsigned numero_di_porta) {
    socket_endpoint_3db661a2 *stringa_dati = get_VALORE(handle_di_file); if (!stringa_dati) return -9;
    if (numero_di_porta > 65535 || (e_mail && e_mail != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&connessione_cellulare))) && e_mail != 0x7f000001)) return -99;
    ip_addr_t indirizzo_Internet; ip_addr_set_ip4_u32(&indirizzo_Internet, lwip_htonl(e_mail));
    err_t 보조항목 = stringa_dati->TIPO_area == 1 ? tcp_bind(stringa_dati->connessione_controllo, &indirizzo_Internet, numero_di_porta) : udp_bind(stringa_dati->datagramma_controllo, &indirizzo_Internet, numero_di_porta); return 보조항목 ? numero_errore(보조항목) : 0;
}
void 통신주소재사용(int handle_di_file) { socket_endpoint_3db661a2 *stringa_dati = get_VALORE(handle_di_file); if (stringa_dati && stringa_dati->connessione_controllo) ip_set_option(stringa_dati->connessione_controllo, SOF_REUSEADDR); }
int NET_essere_in_ascolto(int handle_di_file) {
    socket_endpoint_3db661a2 *stringa_dati = get_VALORE(handle_di_file); if (!stringa_dati || stringa_dati->TIPO_area != 1) return -9;
    if (stringa_dati->porta_di_ricezione) return 0;
    err_t 보조항목; struct tcp_pcb *trasmissione_controllo_Blocca = tcp_listen_with_backlog_and_err(stringa_dati->connessione_controllo, 4, &보조항목);
    if (!trasmissione_controllo_Blocca) return numero_errore(보조항목); stringa_dati->connessione_controllo = trasmissione_controllo_Blocca; stringa_dati->porta_di_ricezione = 1; tcp_arg(trasmissione_controllo_Blocca, stringa_dati); tcp_accept(trasmissione_controllo_Blocca, 연결받음); return 0;
}
int NET_CONNETTI(int handle_di_file, uint32_t e_mail, unsigned numero_di_porta) {
    socket_endpoint_3db661a2 *stringa_dati = get_VALORE(handle_di_file); if (!stringa_dati || stringa_dati->TIPO_area != 1) return -9;
    if (stringa_dati->errore) return stringa_dati->errore;
    if (stringa_dati->연결됨) return 0;
    if (stringa_dati->peer_endpoint_numero) return -115;
    if (!numero_di_porta || numero_di_porta > 65535 || !e_mail) return -22;
    ip_addr_t indirizzo_Internet; ip_addr_set_ip4_u32(&indirizzo_Internet, lwip_htonl(e_mail));
    stringa_dati->peer_e_mail = e_mail; stringa_dati->peer_endpoint_numero = numero_di_porta;
    err_t 보조항목 = tcp_connect(stringa_dati->connessione_controllo, &indirizzo_Internet, numero_di_porta, 연결됨); return 보조항목 ? numero_errore(보조항목) : -115;
}
int NET_accettare(int handle_di_file) {
    socket_endpoint_3db661a2 *stringa_dati = get_VALORE(handle_di_file); if (!stringa_dati || !stringa_dati->porta_di_ricezione) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TIPO_area == 1 && 통신끝점들[순번].reparto_IT_In_sospeso == handle_di_file) { 통신끝점들[순번].reparto_IT_In_sospeso = -1; return 순번; }
    return -11;
}
int 통신읽기(int handle_di_file, void *dati, unsigned articolo_CONTA_NUMERI) {
    socket_endpoint_3db661a2 *stringa_dati = get_VALORE(handle_di_file); if (!stringa_dati || stringa_dati->TIPO_area != 1) return -9;
    if (!articolo_CONTA_NUMERI) return 0; if (!stringa_dati->voce_CONTA_NUMERI) return stringa_dati->errore ? stringa_dati->errore : stringa_dati->File_chiudere ? 0 : -11;
    if (articolo_CONTA_NUMERI > stringa_dati->voce_CONTA_NUMERI) articolo_CONTA_NUMERI = stringa_dati->voce_CONTA_NUMERI;
    for (unsigned 순번 = 0; 순번 < articolo_CONTA_NUMERI; 순번++) { ((unsigned char *)dati)[순번] = stringa_dati->dati[stringa_dati->frontale_voce]; stringa_dati->frontale_voce = (stringa_dati->frontale_voce + 1) % sizeof(stringa_dati->dati); }
    stringa_dati->voce_CONTA_NUMERI -= articolo_CONTA_NUMERI; if (stringa_dati->connessione_controllo) tcp_recved(stringa_dati->connessione_controllo, articolo_CONTA_NUMERI); return articolo_CONTA_NUMERI;
}
int NET_scrivere(int handle_di_file, const void *dati, unsigned articolo_CONTA_NUMERI) {
    socket_endpoint_3db661a2 *stringa_dati = get_VALORE(handle_di_file); if (!stringa_dati || stringa_dati->TIPO_area != 1) return -9;
    if (stringa_dati->errore) return stringa_dati->errore; if (!stringa_dati->connessione_controllo || !stringa_dati->연결됨) return -107;
    if (!articolo_CONTA_NUMERI) return 0; if (articolo_CONTA_NUMERI > tcp_sndbuf(stringa_dati->connessione_controllo)) articolo_CONTA_NUMERI = tcp_sndbuf(stringa_dati->connessione_controllo);
    if (!articolo_CONTA_NUMERI) return -11; if (articolo_CONTA_NUMERI > 1024) articolo_CONTA_NUMERI = 1024;
    err_t 보조항목 = tcp_write(stringa_dati->connessione_controllo, dati, articolo_CONTA_NUMERI, TCP_WRITE_FLAG_COPY); if (보조항목) return numero_errore(보조항목);
    tcp_output(stringa_dati->connessione_controllo); return articolo_CONTA_NUMERI;
}
int inviare_datagramma(int handle_di_file, const void *dati, unsigned articolo_CONTA_NUMERI, uint32_t e_mail, unsigned numero_di_porta) {
    socket_endpoint_3db661a2 *stringa_dati = get_VALORE(handle_di_file); if (!stringa_dati || stringa_dati->TIPO_area != 2) return -9;
    if (articolo_CONTA_NUMERI > 512) return -90; if (!numero_di_porta || numero_di_porta > 65535) return -22;
    struct pbuf *dati_funzione = pbuf_alloc(PBUF_TRANSPORT, articolo_CONTA_NUMERI, PBUF_RAM); if (!dati_funzione) return -11;
    pbuf_take(dati_funzione, dati, articolo_CONTA_NUMERI); ip_addr_t indirizzo_Internet; ip_addr_set_ip4_u32(&indirizzo_Internet, lwip_htonl(e_mail));
    err_t 보조항목 = udp_sendto(stringa_dati->datagramma_controllo, dati_funzione, &indirizzo_Internet, numero_di_porta); pbuf_free(dati_funzione); return 보조항목 ? numero_errore(보조항목) : (int)articolo_CONTA_NUMERI;
}
int ricevere_datagramma(int handle_di_file, void *dati, unsigned articolo_CONTA_NUMERI) {
    socket_endpoint_3db661a2 *stringa_dati = get_VALORE(handle_di_file); if (!stringa_dati || stringa_dati->TIPO_area != 2) return -9;
    if (!stringa_dati->voce_CONTA_NUMERI) return -11; unsigned Regolari_funzione = stringa_dati->frontale_voce;
    if (articolo_CONTA_NUMERI > stringa_dati->길이목록[Regolari_funzione]) articolo_CONTA_NUMERI = stringa_dati->길이목록[Regolari_funzione]; memcpy(dati, stringa_dati->dati + Regolari_funzione * 512, articolo_CONTA_NUMERI);
    stringa_dati->peer_endpoint_numero = stringa_dati->접속번호들[Regolari_funzione]; stringa_dati->peer_e_mail = stringa_dati->주소목록[Regolari_funzione]; stringa_dati->frontale_voce = (Regolari_funzione + 1) % 4; stringa_dati->voce_CONTA_NUMERI--; return articolo_CONTA_NUMERI;
}
unsigned rete_numero_di_porta(int handle_di_file) { socket_endpoint_3db661a2 *stringa_dati = get_VALORE(handle_di_file); return !stringa_dati ? 0 : stringa_dati->connessione_controllo ? stringa_dati->connessione_controllo->local_port : stringa_dati->datagramma_controllo ? stringa_dati->datagramma_controllo->local_port : 0; }
unsigned peer_numero_di_porta(int handle_di_file) { socket_endpoint_3db661a2 *stringa_dati = get_VALORE(handle_di_file); return stringa_dati ? stringa_dati->peer_endpoint_numero : 0; }
uint32_t NET_peer_e_mail(int handle_di_file) { socket_endpoint_3db661a2 *stringa_dati = get_VALORE(handle_di_file); return stringa_dati ? stringa_dati->peer_e_mail : 0; }
void Chiudi_rete(int handle_di_file) {
    socket_endpoint_3db661a2 *stringa_dati = get_VALORE(handle_di_file); if (!stringa_dati) return;
    if (stringa_dati->porta_di_ricezione) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TIPO_area && 통신끝점들[순번].reparto_IT_In_sospeso == handle_di_file) Chiudi_rete(순번);
    if (stringa_dati->connessione_controllo) {
        tcp_arg(stringa_dati->connessione_controllo, 0); if (stringa_dati->porta_di_ricezione) tcp_accept(stringa_dati->connessione_controllo, 0); else { tcp_recv(stringa_dati->connessione_controllo, 0); tcp_err(stringa_dati->connessione_controllo, 0); }
        if (tcp_close(stringa_dati->connessione_controllo) != ERR_OK) tcp_abort(stringa_dati->connessione_controllo);
    }
    if (stringa_dati->datagramma_controllo) udp_remove(stringa_dati->datagramma_controllo); stringa_dati->TIPO_area = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || polling) return; polling = 1;
    if(usare_cablato_rete)유선망살피기(&connessione_cellulare);
    for (unsigned budget = 0; !usare_cablato_rete && budget < 4096 && (computer_registro(보조장치 + 0x54) & 1); budget++) {
        unsigned punto_di_codice = computer_registro(보조장치 + 0x40) & 255;
        if (punto_di_codice == 192) {
            if (ricevere_utilizzo && !ricevere_errore && !수신탈출) {
                struct pbuf *dati_funzione = pbuf_alloc(PBUF_RAW, ricevere_utilizzo, PBUF_POOL);
                if (dati_funzione) { RICEV_SCAD_datagramma_CONTA_NUMERI++; RICEV_SCAD_byte_CONTA_NUMERI += ricevere_utilizzo; pbuf_take(dati_funzione, ricevere_buffer_dei_dati, ricevere_utilizzo); if (connessione_cellulare.input(dati_funzione, &connessione_cellulare) != ERR_OK) { 버린전문수++; pbuf_free(dati_funzione); } }
                else 버린전문수++;
            }
            else if (ricevere_utilizzo) 버린전문수++;
            ricevere_utilizzo = ricevere_errore = 수신탈출 = 0;
        } else if (punto_di_codice == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (punto_di_codice != 220 && punto_di_codice != 221) ricevere_errore = 1; punto_di_codice = punto_di_codice == 220 ? 192 : 219; 수신탈출 = 0; }
            if (ricevere_utilizzo < sizeof(ricevere_buffer_dei_dati)) ricevere_buffer_dei_dati[ricevere_utilizzo++] = punto_di_codice; else ricevere_errore = 1;
        }
    }
    netif_poll(&connessione_cellulare); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned budget = 0; budget < 4096 && 송신개수 && (computer_registro(보조장치 + 0x54) & 0x20); budget++) {
        computer_registro(보조장치 + 0x40) = trasmettere_dati[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(trasmettere_dati); 송신개수--;
    }
    polling = 0;
}

/* Impostazioni·조회는 lwIP의 effettivo_dati 인터페이스와 chiudere_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned voce_VALORE, unsigned INDICE) {
    if(voce_VALORE==20)return usare_cablato_rete;
    if(voce_VALORE==21)return 준비됨&&netif_is_link_up(&connessione_cellulare);
    if(voce_VALORE==22)return usare_cablato_rete?cablato_rete_Statistiche(5):0;
    if (!준비됨) return 0;
    if(usare_cablato_rete&&voce_VALORE>=4&&voce_VALORE<=8)return cablato_rete_Statistiche(voce_VALORE-4);
    if (voce_VALORE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&connessione_cellulare)));
    if (voce_VALORE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&connessione_cellulare)));
    if (voce_VALORE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&connessione_cellulare)));
    if (voce_VALORE == 3) return netif_is_up(&connessione_cellulare) != 0;
    if (voce_VALORE == 4) return RICEV_SCAD_datagramma_CONTA_NUMERI;
    if (voce_VALORE == 5) return 보낸전문수;
    if (voce_VALORE == 6) return RICEV_SCAD_byte_CONTA_NUMERI;
    if (voce_VALORE == 7) return 보낸바이트수;
    if (voce_VALORE == 8) return 버린전문수;
    if (voce_VALORE == 9) return 송신개수;
    if (INDICE >= 32) return 0;
    socket_endpoint_3db661a2 *chiudere_p = &통신끝점들[INDICE];
    if (voce_VALORE == 10) return chiudere_p->TIPO_area;
    if (!chiudere_p->TIPO_area) return 0;
    if (voce_VALORE == 11) return rete_numero_di_porta(INDICE);
    if (voce_VALORE == 12) return chiudere_p->peer_e_mail;
    if (voce_VALORE == 13) return chiudere_p->peer_endpoint_numero;
    if (voce_VALORE == 14) return chiudere_p->porta_di_ricezione ? 1 : chiudere_p->File_chiudere ? 3 : chiudere_p->errore ? 4 : chiudere_p->연결됨 ? 2 : 0;
    if (voce_VALORE == 15) return chiudere_p->voce_CONTA_NUMERI;
    if (voce_VALORE == 16) {
        const ip_addr_t *e_mail = chiudere_p->TIPO_area == 1 && chiudere_p->connessione_controllo ? &chiudere_p->connessione_controllo->local_ip :
            chiudere_p->TIPO_area == 2 && chiudere_p->datagramma_controllo ? &chiudere_p->datagramma_controllo->local_ip : 0;
        return e_mail ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(e_mail))) : 0;
    }
    return 0;
}

int configurare_rete(unsigned Azione, uint32_t e_mail, uint32_t maschera_VALORE, uint32_t gateway_VALORE) {
    if (!준비됨) return -100;
    if (Azione == 1) { netif_set_up(&connessione_cellulare); return 0; }
    if (Azione == 2) { netif_set_down(&connessione_cellulare); return 0; }
    if (Azione != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maschera_VALORE, 같은 망의 선택적 valore_predefinito gateway_VALORE. */
    uint32_t 뒤집은가림 = ~maschera_VALORE;
    if (!maschera_VALORE || (뒤집은가림 & (뒤집은가림 + 1)) || !e_mail || (e_mail >> 24) == 127 ||
        (e_mail >> 24) == 0 || (e_mail >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(e_mail & 뒤집은가림) || (e_mail & 뒤집은가림) == 뒤집은가림)) ||
        (gateway_VALORE && ((gateway_VALORE & maschera_VALORE) != (e_mail & maschera_VALORE) || gateway_VALORE == e_mail || (gateway_VALORE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(gateway_VALORE & 뒤집은가림) || (gateway_VALORE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 e_mail 변경으로 몰래 끊지 않는다. */
    for (unsigned INDICE = 0; INDICE < 32; INDICE++) if (통신끝점들[INDICE].TIPO_area &&
        !(통신끝점들[INDICE].porta_di_ricezione && 통신끝점들[INDICE].connessione_controllo && ip_addr_isany(&통신끝점들[INDICE].connessione_controllo->local_ip))) return -16;
    if(usare_cablato_rete)dhcp_stop(&connessione_cellulare);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(e_mail)); ip4_addr_set_u32(&새가림, lwip_htonl(maschera_VALORE)); ip4_addr_set_u32(&새관문, lwip_htonl(gateway_VALORE));
    netif_set_addr(&connessione_cellulare, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *risposta_endpoint;
static uint32_t test_e_mail, test_time, tempo_di_risposta;
static unsigned test_SEQUENZA, test_identificatore, risposta_SEQUENZA;
static int risposta_Stato;
static u8_t 응답받음(void *argomenti, struct raw_pcb *chiudere_p, struct pbuf *dati, const ip_addr_t *e_mail) {
    (void)argomenti; (void)chiudere_p;
    unsigned char intestazione_VALORE[20], replica[16];
    if (risposta_Stato != -11 || dati->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(e_mail))) != test_e_mail || pbuf_copy_partial(dati, intestazione_VALORE, 20, 0) != 20) return 0;
    unsigned Intestazione_ridimensionare = (intestazione_VALORE[0] & 15) * 4;
    if ((intestazione_VALORE[0] >> 4) != 4 || Intestazione_ridimensionare < 20 || dati->tot_len < Intestazione_ridimensionare + 16 ||
        pbuf_copy_partial(dati, replica, 16, Intestazione_ridimensionare) != 16 || replica[0] || replica[1] ||
        (((unsigned)replica[4] << 8) | replica[5]) != test_identificatore ||
        (((unsigned)replica[6] << 8) | replica[7]) != test_SEQUENZA ||
        replica[8] != 'J' || replica[9] != 'K' || replica[10] != 'O' || replica[11] != 'S' ||
        (((uint32_t)replica[12] << 24) | ((uint32_t)replica[13] << 16) | ((uint32_t)replica[14] << 8) | replica[15]) != test_time) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(dati, Intestazione_ridimensionare)) return 0;
    if (inet_chksum_pbuf(dati)) { pbuf_add_header(dati, Intestazione_ridimensionare); return 0; }
    tempo_di_risposta = (uint32_t)보드밀리초() - test_time; risposta_SEQUENZA = intestazione_VALORE[8]; risposta_Stato = 0;
    pbuf_free(dati); return 1;
}
int START_risposta_test(uint32_t e_mail, unsigned ordine_VALORE) {
    if (!준비됨 || !netif_is_up(&connessione_cellulare)) return -100;
    if (!e_mail || (e_mail >> 28) >= 14 || e_mail == 0xffffffffu) return -22;
    if (!risposta_endpoint) { risposta_endpoint = raw_new(IP_PROTO_ICMP); if (!risposta_endpoint) return -12; raw_recv(risposta_endpoint, 응답받음, 0); }
    test_e_mail = e_mail; test_SEQUENZA = ordine_VALORE & 65535; test_identificatore = (test_identificatore + 1) & 65535;
    test_time = 보드밀리초(); risposta_Stato = -11; tempo_di_risposta = risposta_SEQUENZA = 0;
    unsigned char dati[32] = {8,0,0,0};
    dati[4] = test_identificatore >> 8; dati[5] = test_identificatore; dati[6] = test_SEQUENZA >> 8; dati[7] = test_SEQUENZA;
    dati[8]='J'; dati[9]='K'; dati[10]='O'; dati[11]='S';
    dati[12]=test_time >> 24; dati[13]=test_time >> 16; dati[14]=test_time >> 8; dati[15]=test_time;
    for (unsigned funzione_INDICE = 16; funzione_INDICE < sizeof(dati); funzione_INDICE++) dati[funzione_INDICE] = funzione_INDICE;
    uint16_t verifica_checksum = inet_chksum(dati, sizeof(dati)); memcpy(dati + 2, &verifica_checksum, 2);
    struct pbuf *datagramma = pbuf_alloc(PBUF_IP, sizeof(dati), PBUF_RAM); if (!datagramma) return -12;
    pbuf_take(datagramma, dati, sizeof(dati)); ip_addr_t meta_endpoint; ip_addr_set_ip4_u32(&meta_endpoint, lwip_htonl(e_mail));
    err_t 처리값 = raw_sendto(risposta_endpoint, datagramma, &meta_endpoint); pbuf_free(datagramma);
    if (처리값) risposta_Stato = numero_errore(처리값);
    return 처리값 ? risposta_Stato : 0;
}
int 응답시험읽기(unsigned voce_VALORE) {
    통신망살피기();
    return voce_VALORE == 0 ? risposta_Stato : voce_VALORE == 1 ? (int)tempo_di_risposta : voce_VALORE == 2 ? (int)risposta_SEQUENZA : -22;
}
