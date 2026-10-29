#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Rede_Montón.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../remoto_VALOR/remoto_VALOR.h"
#include "con_fíos_Rede.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define máquina_rexistrarse(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif conexión_dispositivo;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECIBIDO_byte_CONTAR, 보낸바이트수, 버린전문수;
typedef struct {
    int TIPO_Categoría, 수신창구, Tecnoloxía_da_información_TI_pendente, 연결됨, Ficheiro_finalizar, ERRO;
    struct tcp_pcb *conexión_control;
    struct udp_pcb *전문제어;
    unsigned frontal_introdución, introdución_CONTAR;
    unsigned char datos[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], punto_ENDEREZO;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int número_de_erro(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *obter_VALOR(int Ficheiro_agarradoira) { return Ficheiro_agarradoira >= 0 && Ficheiro_agarradoira < 32 && 통신끝점들[Ficheiro_agarradoira].TIPO_Categoría ? &통신끝점들[Ficheiro_agarradoira] : 0; }
static int 예약하기(int TIPO_Categoría) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TIPO_Categoría) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TIPO_Categoría = TIPO_Categoría; 통신끝점들[순번].Tecnoloxía_da_información_TI_pendente = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned código_de_carácter) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = código_de_carácter; }
static err_t 출력결과(struct netif *elemento_CONTAR, struct pbuf *datos_cargo, const ip4_addr_t *ENDEREZO) {
    (void)elemento_CONTAR; (void)ENDEREZO;
    if (datos_cargo->tot_len > 1500 || 송신개수 + 2 * datos_cargo->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Seguinte_DESPRAZAMENTO = datos_cargo; Seguinte_DESPRAZAMENTO; Seguinte_DESPRAZAMENTO = Seguinte_DESPRAZAMENTO->next) for (unsigned 순번 = 0; 순번 < Seguinte_DESPRAZAMENTO->len; 순번++) {
        unsigned código_de_carácter = ((unsigned char *)Seguinte_DESPRAZAMENTO->payload)[순번];
        if (código_de_carácter == 192 || código_de_carácter == 219) { 내보내기(219); 내보내기(código_de_carácter == 192 ? 220 : 221); } else 내보내기(código_de_carácter);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += datos_cargo->tot_len; return ERR_OK;
}
static err_t 준비하기(struct netif *elemento_CONTAR) { elemento_CONTAR->name[0] = 's'; elemento_CONTAR->name[1] = 'l'; elemento_CONTAR->mtu = 1500; elemento_CONTAR->output = 출력결과; return ERR_OK; }
void 통신망준비(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    máquina_rexistrarse(보조장치 + 4) |= 1; máquina_rexistrarse(보조장치 + 0x60) = 0; máquina_rexistrarse(보조장치 + 0x44) = 0;
    máquina_rexistrarse(보조장치 + 0x48) = 0xc6; máquina_rexistrarse(보조장치 + 0x4c) = 3; máquina_rexistrarse(보조장치 + 0x68) = 270; máquina_rexistrarse(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t enderezo_de_internet, máscara_de_bits, pasarela_ENDEREZO;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&enderezo_de_internet, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&máscara_de_bits, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&pasarela_ENDEREZO, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&conexión_dispositivo, &enderezo_de_internet, &máscara_de_bits, &pasarela_ENDEREZO, 0, 유선사용?유선망준비:준비하기, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&conexión_dispositivo); netif_set_up(&conexión_dispositivo);if(!유선사용)netif_set_link_up(&conexión_dispositivo); 준비됨 = 1;
    원격준비();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *transmisión_control_bloquear, struct pbuf *datos_cargo, err_t ERRO) {
    통신끝점 *cadea_datos = 부가인수; (void)transmisión_control_bloquear; (void)ERRO;
    if (!datos_cargo) { cadea_datos->Ficheiro_finalizar = 1; return ERR_OK; }
    if (datos_cargo->tot_len > sizeof(cadea_datos->datos) - cadea_datos->introdución_CONTAR) return ERR_MEM;
    unsigned ao_corrente_cargo = (cadea_datos->frontal_introdución + cadea_datos->introdución_CONTAR) % sizeof(cadea_datos->datos);
    for (struct pbuf *Seguinte_DESPRAZAMENTO = datos_cargo; Seguinte_DESPRAZAMENTO; Seguinte_DESPRAZAMENTO = Seguinte_DESPRAZAMENTO->next) for (unsigned 순번 = 0; 순번 < Seguinte_DESPRAZAMENTO->len; 순번++) {
        cadea_datos->datos[ao_corrente_cargo] = ((unsigned char *)Seguinte_DESPRAZAMENTO->payload)[순번]; ao_corrente_cargo = (ao_corrente_cargo + 1) % sizeof(cadea_datos->datos);
    }
    cadea_datos->introdución_CONTAR += datos_cargo->tot_len; pbuf_free(datos_cargo); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t ERRO) { 통신끝점 *cadea_datos = 부가인수; cadea_datos->conexión_control = 0; cadea_datos->ERRO = número_de_erro(ERRO); }
static void 되부름목록(통신끝점 *cadea_datos) { tcp_arg(cadea_datos->conexión_control, cadea_datos); tcp_recv(cadea_datos->conexión_control, 수신됨); tcp_err(cadea_datos->conexión_control, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *transmisión_control_bloquear, err_t ERRO) {
    통신끝점 *cadea_datos = 부가인수; (void)transmisión_control_bloquear; if (ERRO) cadea_datos->ERRO = número_de_erro(ERRO); else cadea_datos->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *transmisión_control_bloquear, err_t ERRO) {
    통신끝점 *부모항목 = 부가인수; if (ERRO) return ERRO;
    int Ficheiro_agarradoira = 예약하기(1); if (Ficheiro_agarradoira < 0) return ERR_MEM;
    통신끝점 *cadea_datos = &통신끝점들[Ficheiro_agarradoira]; cadea_datos->conexión_control = transmisión_control_bloquear; cadea_datos->연결됨 = 1; cadea_datos->Tecnoloxía_da_información_TI_pendente = (int)(부모항목 - 통신끝점들);
    cadea_datos->punto_ENDEREZO = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&transmisión_control_bloquear->remote_ip))); cadea_datos->상대창구번호 = transmisión_control_bloquear->remote_port;
    되부름목록(cadea_datos); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *transmisión_control_bloquear, struct pbuf *datos_cargo, const ip_addr_t *ENDEREZO, u16_t número_do_porto) {
    통신끝점 *cadea_datos = 부가인수; (void)transmisión_control_bloquear;
    if (cadea_datos->introdución_CONTAR < 4 && datos_cargo->tot_len <= 512) {
        unsigned cargo_ÍNDICE = (cadea_datos->frontal_introdución + cadea_datos->introdución_CONTAR) % 4;
        pbuf_copy_partial(datos_cargo, cadea_datos->datos + cargo_ÍNDICE * 512, datos_cargo->tot_len, 0);
        cadea_datos->길이목록[cargo_ÍNDICE] = datos_cargo->tot_len; cadea_datos->접속번호들[cargo_ÍNDICE] = número_do_porto;
        cadea_datos->주소목록[cargo_ÍNDICE] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ENDEREZO))); cadea_datos->introdución_CONTAR++;
    }
    pbuf_free(datos_cargo);
}
int 통신끝점만들기(int TIPO_Categoría) {
    if (!준비됨) return -100;
    if (TIPO_Categoría != 1 && TIPO_Categoría != 2) return -93;
    int Ficheiro_agarradoira = 예약하기(TIPO_Categoría); if (Ficheiro_agarradoira < 0) return Ficheiro_agarradoira;
    통신끝점 *cadea_datos = &통신끝점들[Ficheiro_agarradoira];
    if (TIPO_Categoría == 1) { cadea_datos->conexión_control = tcp_new(); if (cadea_datos->conexión_control) 되부름목록(cadea_datos); }
    else { cadea_datos->전문제어 = udp_new(); if (cadea_datos->전문제어) udp_recv(cadea_datos->전문제어, 전문, cadea_datos); }
    if (!cadea_datos->conexión_control && !cadea_datos->전문제어) { cadea_datos->TIPO_Categoría = 0; return -12; } return Ficheiro_agarradoira;
}
int 망주소묶기(int Ficheiro_agarradoira, uint32_t ENDEREZO, unsigned número_do_porto) {
    통신끝점 *cadea_datos = obter_VALOR(Ficheiro_agarradoira); if (!cadea_datos) return -9;
    if (número_do_porto > 65535 || (ENDEREZO && ENDEREZO != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&conexión_dispositivo))) && ENDEREZO != 0x7f000001)) return -99;
    ip_addr_t enderezo_de_internet; ip_addr_set_ip4_u32(&enderezo_de_internet, lwip_htonl(ENDEREZO));
    err_t 보조항목 = cadea_datos->TIPO_Categoría == 1 ? tcp_bind(cadea_datos->conexión_control, &enderezo_de_internet, número_do_porto) : udp_bind(cadea_datos->전문제어, &enderezo_de_internet, número_do_porto); return 보조항목 ? número_de_erro(보조항목) : 0;
}
void 통신주소재사용(int Ficheiro_agarradoira) { 통신끝점 *cadea_datos = obter_VALOR(Ficheiro_agarradoira); if (cadea_datos && cadea_datos->conexión_control) ip_set_option(cadea_datos->conexión_control, SOF_REUSEADDR); }
int 연결기다리기(int Ficheiro_agarradoira) {
    통신끝점 *cadea_datos = obter_VALOR(Ficheiro_agarradoira); if (!cadea_datos || cadea_datos->TIPO_Categoría != 1) return -9;
    if (cadea_datos->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *transmisión_control_bloquear = tcp_listen_with_backlog_and_err(cadea_datos->conexión_control, 4, &보조항목);
    if (!transmisión_control_bloquear) return número_de_erro(보조항목); cadea_datos->conexión_control = transmisión_control_bloquear; cadea_datos->수신창구 = 1; tcp_arg(transmisión_control_bloquear, cadea_datos); tcp_accept(transmisión_control_bloquear, 연결받음); return 0;
}
int 망연결하기(int Ficheiro_agarradoira, uint32_t ENDEREZO, unsigned número_do_porto) {
    통신끝점 *cadea_datos = obter_VALOR(Ficheiro_agarradoira); if (!cadea_datos || cadea_datos->TIPO_Categoría != 1) return -9;
    if (cadea_datos->ERRO) return cadea_datos->ERRO;
    if (cadea_datos->연결됨) return 0;
    if (cadea_datos->상대창구번호) return -115;
    if (!número_do_porto || número_do_porto > 65535 || !ENDEREZO) return -22;
    ip_addr_t enderezo_de_internet; ip_addr_set_ip4_u32(&enderezo_de_internet, lwip_htonl(ENDEREZO));
    cadea_datos->punto_ENDEREZO = ENDEREZO; cadea_datos->상대창구번호 = número_do_porto;
    err_t 보조항목 = tcp_connect(cadea_datos->conexión_control, &enderezo_de_internet, número_do_porto, 연결됨); return 보조항목 ? número_de_erro(보조항목) : -115;
}
int 망연결받기(int Ficheiro_agarradoira) {
    통신끝점 *cadea_datos = obter_VALOR(Ficheiro_agarradoira); if (!cadea_datos || !cadea_datos->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TIPO_Categoría == 1 && 통신끝점들[순번].Tecnoloxía_da_información_TI_pendente == Ficheiro_agarradoira) { 통신끝점들[순번].Tecnoloxía_da_información_TI_pendente = -1; return 순번; }
    return -11;
}
int 통신읽기(int Ficheiro_agarradoira, void *datos, unsigned elemento_CONTAR) {
    통신끝점 *cadea_datos = obter_VALOR(Ficheiro_agarradoira); if (!cadea_datos || cadea_datos->TIPO_Categoría != 1) return -9;
    if (!elemento_CONTAR) return 0; if (!cadea_datos->introdución_CONTAR) return cadea_datos->ERRO ? cadea_datos->ERRO : cadea_datos->Ficheiro_finalizar ? 0 : -11;
    if (elemento_CONTAR > cadea_datos->introdución_CONTAR) elemento_CONTAR = cadea_datos->introdución_CONTAR;
    for (unsigned 순번 = 0; 순번 < elemento_CONTAR; 순번++) { ((unsigned char *)datos)[순번] = cadea_datos->datos[cadea_datos->frontal_introdución]; cadea_datos->frontal_introdución = (cadea_datos->frontal_introdución + 1) % sizeof(cadea_datos->datos); }
    cadea_datos->introdución_CONTAR -= elemento_CONTAR; if (cadea_datos->conexión_control) tcp_recved(cadea_datos->conexión_control, elemento_CONTAR); return elemento_CONTAR;
}
int 통신쓰기(int Ficheiro_agarradoira, const void *datos, unsigned elemento_CONTAR) {
    통신끝점 *cadea_datos = obter_VALOR(Ficheiro_agarradoira); if (!cadea_datos || cadea_datos->TIPO_Categoría != 1) return -9;
    if (cadea_datos->ERRO) return cadea_datos->ERRO; if (!cadea_datos->conexión_control || !cadea_datos->연결됨) return -107;
    if (!elemento_CONTAR) return 0; if (elemento_CONTAR > tcp_sndbuf(cadea_datos->conexión_control)) elemento_CONTAR = tcp_sndbuf(cadea_datos->conexión_control);
    if (!elemento_CONTAR) return -11; if (elemento_CONTAR > 1024) elemento_CONTAR = 1024;
    err_t 보조항목 = tcp_write(cadea_datos->conexión_control, datos, elemento_CONTAR, TCP_WRITE_FLAG_COPY); if (보조항목) return número_de_erro(보조항목);
    tcp_output(cadea_datos->conexión_control); return elemento_CONTAR;
}
int 전문보내기(int Ficheiro_agarradoira, const void *datos, unsigned elemento_CONTAR, uint32_t ENDEREZO, unsigned número_do_porto) {
    통신끝점 *cadea_datos = obter_VALOR(Ficheiro_agarradoira); if (!cadea_datos || cadea_datos->TIPO_Categoría != 2) return -9;
    if (elemento_CONTAR > 512) return -90; if (!número_do_porto || número_do_porto > 65535) return -22;
    struct pbuf *datos_cargo = pbuf_alloc(PBUF_TRANSPORT, elemento_CONTAR, PBUF_RAM); if (!datos_cargo) return -11;
    pbuf_take(datos_cargo, datos, elemento_CONTAR); ip_addr_t enderezo_de_internet; ip_addr_set_ip4_u32(&enderezo_de_internet, lwip_htonl(ENDEREZO));
    err_t 보조항목 = udp_sendto(cadea_datos->전문제어, datos_cargo, &enderezo_de_internet, número_do_porto); pbuf_free(datos_cargo); return 보조항목 ? número_de_erro(보조항목) : (int)elemento_CONTAR;
}
int 전문받기(int Ficheiro_agarradoira, void *datos, unsigned elemento_CONTAR) {
    통신끝점 *cadea_datos = obter_VALOR(Ficheiro_agarradoira); if (!cadea_datos || cadea_datos->TIPO_Categoría != 2) return -9;
    if (!cadea_datos->introdución_CONTAR) return -11; unsigned ao_corrente_cargo = cadea_datos->frontal_introdución;
    if (elemento_CONTAR > cadea_datos->길이목록[ao_corrente_cargo]) elemento_CONTAR = cadea_datos->길이목록[ao_corrente_cargo]; memcpy(datos, cadea_datos->datos + ao_corrente_cargo * 512, elemento_CONTAR);
    cadea_datos->상대창구번호 = cadea_datos->접속번호들[ao_corrente_cargo]; cadea_datos->punto_ENDEREZO = cadea_datos->주소목록[ao_corrente_cargo]; cadea_datos->frontal_introdución = (ao_corrente_cargo + 1) % 4; cadea_datos->introdución_CONTAR--; return elemento_CONTAR;
}
unsigned Rede_número_do_porto(int Ficheiro_agarradoira) { 통신끝점 *cadea_datos = obter_VALOR(Ficheiro_agarradoira); return !cadea_datos ? 0 : cadea_datos->conexión_control ? cadea_datos->conexión_control->local_port : cadea_datos->전문제어 ? cadea_datos->전문제어->local_port : 0; }
unsigned punto_número_do_porto(int Ficheiro_agarradoira) { 통신끝점 *cadea_datos = obter_VALOR(Ficheiro_agarradoira); return cadea_datos ? cadea_datos->상대창구번호 : 0; }
uint32_t 상대통신주소(int Ficheiro_agarradoira) { 통신끝점 *cadea_datos = obter_VALOR(Ficheiro_agarradoira); return cadea_datos ? cadea_datos->punto_ENDEREZO : 0; }
void peche_Rede(int Ficheiro_agarradoira) {
    통신끝점 *cadea_datos = obter_VALOR(Ficheiro_agarradoira); if (!cadea_datos) return;
    if (cadea_datos->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TIPO_Categoría && 통신끝점들[순번].Tecnoloxía_da_información_TI_pendente == Ficheiro_agarradoira) peche_Rede(순번);
    if (cadea_datos->conexión_control) {
        tcp_arg(cadea_datos->conexión_control, 0); if (cadea_datos->수신창구) tcp_accept(cadea_datos->conexión_control, 0); else { tcp_recv(cadea_datos->conexión_control, 0); tcp_err(cadea_datos->conexión_control, 0); }
        if (tcp_close(cadea_datos->conexión_control) != ERR_OK) tcp_abort(cadea_datos->conexión_control);
    }
    if (cadea_datos->전문제어) udp_remove(cadea_datos->전문제어); cadea_datos->TIPO_Categoría = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&conexión_dispositivo);
    for (unsigned orzamento_atribuído = 0; !유선사용 && orzamento_atribuído < 4096 && (máquina_rexistrarse(보조장치 + 0x54) & 1); orzamento_atribuído++) {
        unsigned código_de_carácter = máquina_rexistrarse(보조장치 + 0x40) & 255;
        if (código_de_carácter == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *datos_cargo = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (datos_cargo) { 받은전문수++; RECIBIDO_byte_CONTAR += 수신사용량; pbuf_take(datos_cargo, 수신자료, 수신사용량); if (conexión_dispositivo.input(datos_cargo, &conexión_dispositivo) != ERR_OK) { 버린전문수++; pbuf_free(datos_cargo); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (código_de_carácter == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (código_de_carácter != 220 && código_de_carácter != 221) 수신오류 = 1; código_de_carácter = código_de_carácter == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = código_de_carácter; else 수신오류 = 1;
        }
    }
    netif_poll(&conexión_dispositivo); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned orzamento_atribuído = 0; orzamento_atribuído < 4096 && 송신개수 && (máquina_rexistrarse(보조장치 + 0x54) & 0x20); orzamento_atribuído++) {
        máquina_rexistrarse(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Configuración·조회는 lwIP의 real_datos 인터페이스와 finalizar_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned introdución_VALOR, unsigned ÍNDICE) {
    if(introdución_VALOR==20)return 유선사용;
    if(introdución_VALOR==21)return 준비됨&&netif_is_link_up(&conexión_dispositivo);
    if(introdución_VALOR==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&introdución_VALOR>=4&&introdución_VALOR<=8)return 유선망집계(introdución_VALOR-4);
    if (introdución_VALOR == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&conexión_dispositivo)));
    if (introdución_VALOR == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&conexión_dispositivo)));
    if (introdución_VALOR == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&conexión_dispositivo)));
    if (introdución_VALOR == 3) return netif_is_up(&conexión_dispositivo) != 0;
    if (introdución_VALOR == 4) return 받은전문수;
    if (introdución_VALOR == 5) return 보낸전문수;
    if (introdución_VALOR == 6) return RECIBIDO_byte_CONTAR;
    if (introdución_VALOR == 7) return 보낸바이트수;
    if (introdución_VALOR == 8) return 버린전문수;
    if (introdución_VALOR == 9) return 송신개수;
    if (ÍNDICE >= 32) return 0;
    통신끝점 *finalizar_p = &통신끝점들[ÍNDICE];
    if (introdución_VALOR == 10) return finalizar_p->TIPO_Categoría;
    if (!finalizar_p->TIPO_Categoría) return 0;
    if (introdución_VALOR == 11) return Rede_número_do_porto(ÍNDICE);
    if (introdución_VALOR == 12) return finalizar_p->punto_ENDEREZO;
    if (introdución_VALOR == 13) return finalizar_p->상대창구번호;
    if (introdución_VALOR == 14) return finalizar_p->수신창구 ? 1 : finalizar_p->Ficheiro_finalizar ? 3 : finalizar_p->ERRO ? 4 : finalizar_p->연결됨 ? 2 : 0;
    if (introdución_VALOR == 15) return finalizar_p->introdución_CONTAR;
    if (introdución_VALOR == 16) {
        const ip_addr_t *ENDEREZO = finalizar_p->TIPO_Categoría == 1 && finalizar_p->conexión_control ? &finalizar_p->conexión_control->local_ip :
            finalizar_p->TIPO_Categoría == 2 && finalizar_p->전문제어 ? &finalizar_p->전문제어->local_ip : 0;
        return ENDEREZO ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ENDEREZO))) : 0;
    }
    return 0;
}

int configurar_Rede(unsigned Acción, uint32_t ENDEREZO, uint32_t máscara_VALOR, uint32_t pasarela_VALOR) {
    if (!준비됨) return -100;
    if (Acción == 1) { netif_set_up(&conexión_dispositivo); return 0; }
    if (Acción == 2) { netif_set_down(&conexión_dispositivo); return 0; }
    if (Acción != 0) return -22;
    /* 유니캐스트 IPv4, 연속 máscara_VALOR, 같은 망의 선택적 valor_predefinido pasarela_VALOR. */
    uint32_t 뒤집은가림 = ~máscara_VALOR;
    if (!máscara_VALOR || (뒤집은가림 & (뒤집은가림 + 1)) || !ENDEREZO || (ENDEREZO >> 24) == 127 ||
        (ENDEREZO >> 24) == 0 || (ENDEREZO >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(ENDEREZO & 뒤집은가림) || (ENDEREZO & 뒤집은가림) == 뒤집은가림)) ||
        (pasarela_VALOR && ((pasarela_VALOR & máscara_VALOR) != (ENDEREZO & máscara_VALOR) || pasarela_VALOR == ENDEREZO || (pasarela_VALOR >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(pasarela_VALOR & 뒤집은가림) || (pasarela_VALOR & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 ENDEREZO 변경으로 몰래 끊지 않는다. */
    for (unsigned ÍNDICE = 0; ÍNDICE < 32; ÍNDICE++) if (통신끝점들[ÍNDICE].TIPO_Categoría &&
        !(통신끝점들[ÍNDICE].수신창구 && 통신끝점들[ÍNDICE].conexión_control && ip_addr_isany(&통신끝점들[ÍNDICE].conexión_control->local_ip))) return -16;
    if(유선사용)dhcp_stop(&conexión_dispositivo);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(ENDEREZO)); ip4_addr_set_u32(&새가림, lwip_htonl(máscara_VALOR)); ip4_addr_set_u32(&새관문, lwip_htonl(pasarela_VALOR));
    netif_set_addr(&conexión_dispositivo, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *resposta_extremo;
static uint32_t 시험주소, 시험시각, resposta_hora;
static unsigned 시험순서, 시험식별자, resposta_SECUENCIA;
static int resposta_Estado;
static u8_t 응답받음(void *Argumentos, struct raw_pcb *finalizar_p, struct pbuf *datos, const ip_addr_t *ENDEREZO) {
    (void)Argumentos; (void)finalizar_p;
    unsigned char 머리[20], resposta[16];
    if (resposta_Estado != -11 || datos->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ENDEREZO))) != 시험주소 || pbuf_copy_partial(datos, 머리, 20, 0) != 20) return 0;
    unsigned 머리크기 = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || 머리크기 < 20 || datos->tot_len < 머리크기 + 16 ||
        pbuf_copy_partial(datos, resposta, 16, 머리크기) != 16 || resposta[0] || resposta[1] ||
        (((unsigned)resposta[4] << 8) | resposta[5]) != 시험식별자 ||
        (((unsigned)resposta[6] << 8) | resposta[7]) != 시험순서 ||
        resposta[8] != 'J' || resposta[9] != 'K' || resposta[10] != 'O' || resposta[11] != 'S' ||
        (((uint32_t)resposta[12] << 24) | ((uint32_t)resposta[13] << 16) | ((uint32_t)resposta[14] << 8) | resposta[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(datos, 머리크기)) return 0;
    if (inet_chksum_pbuf(datos)) { pbuf_add_header(datos, 머리크기); return 0; }
    resposta_hora = (uint32_t)보드밀리초() - 시험시각; resposta_SECUENCIA = 머리[8]; resposta_Estado = 0;
    pbuf_free(datos); return 1;
}
int 응답시험시작(uint32_t ENDEREZO, unsigned orde_VALOR) {
    if (!준비됨 || !netif_is_up(&conexión_dispositivo)) return -100;
    if (!ENDEREZO || (ENDEREZO >> 28) >= 14 || ENDEREZO == 0xffffffffu) return -22;
    if (!resposta_extremo) { resposta_extremo = raw_new(IP_PROTO_ICMP); if (!resposta_extremo) return -12; raw_recv(resposta_extremo, 응답받음, 0); }
    시험주소 = ENDEREZO; 시험순서 = orde_VALOR & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); resposta_Estado = -11; resposta_hora = resposta_SECUENCIA = 0;
    unsigned char datos[32] = {8,0,0,0};
    datos[4] = 시험식별자 >> 8; datos[5] = 시험식별자; datos[6] = 시험순서 >> 8; datos[7] = 시험순서;
    datos[8]='J'; datos[9]='K'; datos[10]='O'; datos[11]='S';
    datos[12]=시험시각 >> 24; datos[13]=시험시각 >> 16; datos[14]=시험시각 >> 8; datos[15]=시험시각;
    for (unsigned cargo_ÍNDICE = 16; cargo_ÍNDICE < sizeof(datos); cargo_ÍNDICE++) datos[cargo_ÍNDICE] = cargo_ÍNDICE;
    uint16_t verificación_suma_de_comprobación = inet_chksum(datos, sizeof(datos)); memcpy(datos + 2, &verificación_suma_de_comprobación, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(datos), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, datos, sizeof(datos)); ip_addr_t destino_extremo; ip_addr_set_ip4_u32(&destino_extremo, lwip_htonl(ENDEREZO));
    err_t 처리값 = raw_sendto(resposta_extremo, 전문, &destino_extremo); pbuf_free(전문);
    if (처리값) resposta_Estado = número_de_erro(처리값);
    return 처리값 ? resposta_Estado : 0;
}
int 응답시험읽기(unsigned introdución_VALOR) {
    통신망살피기();
    return introdución_VALOR == 0 ? resposta_Estado : introdución_VALOR == 1 ? (int)resposta_hora : introdución_VALOR == 2 ? (int)resposta_SECUENCIA : -22;
}
