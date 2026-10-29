#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "rede_pilha.h"
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
#include "com_fio_rede.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define computador_registro(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif conexão_celular;
static int 준비됨, sondagem;
static int uso_com_fio_rede;
static unsigned receber_uso, 수신탈출, receber_erro;
static unsigned char receber_buffer_de_dados[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t RECEBER_datagrama_CONT_NÚM, 보낸전문수, RECEBER_byte_CONT_NÚM, 보낸바이트수, 버린전문수;
typedef struct {
    int TIPO_área, porta_de_recepção, TI_Pendente, 연결됨, Arquivo_encerrar, erro;
    struct tcp_pcb *conexão_visual;
    struct udp_pcb *datagrama_visual;
    unsigned câmera_frontal_entrada, entrada_CONT_NÚM_8f7753a1;
    unsigned char dados[4096];
    unsigned 길이목록[4], 접속번호들[4], par_empresa_número;
    uint32_t 주소목록[4], par_email;
} soquete_empresa_3db661a2;
static soquete_empresa_3db661a2 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int número_do_erro(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static soquete_empresa_3db661a2 *get_VALOR(int identificador_de_arquivo) { return identificador_de_arquivo >= 0 && identificador_de_arquivo < 32 && 통신끝점들[identificador_de_arquivo].TIPO_área ? &통신끝점들[identificador_de_arquivo] : 0; }
static int 예약하기(int TIPO_área) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TIPO_área) {
        memset(&통신끝점들[순번], 0, sizeof(soquete_empresa_3db661a2)); 통신끝점들[순번].TIPO_área = TIPO_área; 통신끝점들[순번].TI_Pendente = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned ponto_de_código) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = ponto_de_código; }
static err_t saída(struct netif *item_CONT_NÚM, struct pbuf *dados_cargo, const ip4_addr_t *Endereço) {
    (void)item_CONT_NÚM; (void)Endereço;
    if (dados_cargo->tot_len > 1500 || 송신개수 + 2 * dados_cargo->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Avançar_DESLOC = dados_cargo; Avançar_DESLOC; Avançar_DESLOC = Avançar_DESLOC->next) for (unsigned 순번 = 0; 순번 < Avançar_DESLOC->len; 순번++) {
        unsigned ponto_de_código = ((unsigned char *)Avançar_DESLOC->payload)[순번];
        if (ponto_de_código == 192 || ponto_de_código == 219) { 내보내기(219); 내보내기(ponto_de_código == 192 ? 220 : 221); } else 내보내기(ponto_de_código);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += dados_cargo->tot_len; return ERR_OK;
}
static err_t Preparar_CLR(struct netif *item_CONT_NÚM) { item_CONT_NÚM->name[0] = 's'; item_CONT_NÚM->name[1] = 'l'; item_CONT_NÚM->mtu = 1500; item_CONT_NÚM->output = saída; return ERR_OK; }
void Preparar_rede(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    computador_registro(보조장치 + 4) |= 1; computador_registro(보조장치 + 0x60) = 0; computador_registro(보조장치 + 0x44) = 0;
    computador_registro(보조장치 + 0x48) = 0xc6; computador_registro(보조장치 + 0x4c) = 3; computador_registro(보조장치 + 0x68) = 270; computador_registro(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t endereço_na_Internet, bitmask, endereço_do_gateway;
    uso_com_fio_rede=유선장치있음();
    ip4_addr_set_u32(&endereço_na_Internet, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bitmask, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&endereço_do_gateway, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&conexão_celular, &endereço_na_Internet, &bitmask, &endereço_do_gateway, 0, uso_com_fio_rede?Preparar_com_fio_rede:Preparar_CLR, uso_com_fio_rede?ethernet_input:ip4_input))return;
    netif_set_default(&conexão_celular); netif_set_up(&conexão_celular);if(!uso_com_fio_rede)netif_set_link_up(&conexão_celular); 준비됨 = 1;
    Preparar_remoto();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *transmissão_visual_bloco, struct pbuf *dados_cargo, err_t erro) {
    soquete_empresa_3db661a2 *cadeia_dados = 부가인수; (void)transmissão_visual_bloco; (void)erro;
    if (!dados_cargo) { cadeia_dados->Arquivo_encerrar = 1; return ERR_OK; }
    if (dados_cargo->tot_len > sizeof(cadeia_dados->dados) - cadeia_dados->entrada_CONT_NÚM_8f7753a1) return ERR_MEM;
    unsigned em_dia_cargo = (cadeia_dados->câmera_frontal_entrada + cadeia_dados->entrada_CONT_NÚM_8f7753a1) % sizeof(cadeia_dados->dados);
    for (struct pbuf *Avançar_DESLOC = dados_cargo; Avançar_DESLOC; Avançar_DESLOC = Avançar_DESLOC->next) for (unsigned 순번 = 0; 순번 < Avançar_DESLOC->len; 순번++) {
        cadeia_dados->dados[em_dia_cargo] = ((unsigned char *)Avançar_DESLOC->payload)[순번]; em_dia_cargo = (em_dia_cargo + 1) % sizeof(cadeia_dados->dados);
    }
    cadeia_dados->entrada_CONT_NÚM_8f7753a1 += dados_cargo->tot_len; pbuf_free(dados_cargo); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t erro) { soquete_empresa_3db661a2 *cadeia_dados = 부가인수; cadeia_dados->conexão_visual = 0; cadeia_dados->erro = número_do_erro(erro); }
static void 되부름목록(soquete_empresa_3db661a2 *cadeia_dados) { tcp_arg(cadeia_dados->conexão_visual, cadeia_dados); tcp_recv(cadeia_dados->conexão_visual, 수신됨); tcp_err(cadeia_dados->conexão_visual, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *transmissão_visual_bloco, err_t erro) {
    soquete_empresa_3db661a2 *cadeia_dados = 부가인수; (void)transmissão_visual_bloco; if (erro) cadeia_dados->erro = número_do_erro(erro); else cadeia_dados->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *transmissão_visual_bloco, err_t erro) {
    soquete_empresa_3db661a2 *pai = 부가인수; if (erro) return erro;
    int identificador_de_arquivo = 예약하기(1); if (identificador_de_arquivo < 0) return ERR_MEM;
    soquete_empresa_3db661a2 *cadeia_dados = &통신끝점들[identificador_de_arquivo]; cadeia_dados->conexão_visual = transmissão_visual_bloco; cadeia_dados->연결됨 = 1; cadeia_dados->TI_Pendente = (int)(pai - 통신끝점들);
    cadeia_dados->par_email = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&transmissão_visual_bloco->remote_ip))); cadeia_dados->par_empresa_número = transmissão_visual_bloco->remote_port;
    되부름목록(cadeia_dados); return ERR_OK;
}
static void datagrama(void *부가인수, struct udp_pcb *transmissão_visual_bloco, struct pbuf *dados_cargo, const ip_addr_t *Endereço, u16_t número_da_porta) {
    soquete_empresa_3db661a2 *cadeia_dados = 부가인수; (void)transmissão_visual_bloco;
    if (cadeia_dados->entrada_CONT_NÚM_8f7753a1 < 4 && dados_cargo->tot_len <= 512) {
        unsigned cargo_ÍNDICE = (cadeia_dados->câmera_frontal_entrada + cadeia_dados->entrada_CONT_NÚM_8f7753a1) % 4;
        pbuf_copy_partial(dados_cargo, cadeia_dados->dados + cargo_ÍNDICE * 512, dados_cargo->tot_len, 0);
        cadeia_dados->길이목록[cargo_ÍNDICE] = dados_cargo->tot_len; cadeia_dados->접속번호들[cargo_ÍNDICE] = número_da_porta;
        cadeia_dados->주소목록[cargo_ÍNDICE] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Endereço))); cadeia_dados->entrada_CONT_NÚM_8f7753a1++;
    }
    pbuf_free(dados_cargo);
}
int Criar_soquete_empresa(int TIPO_área) {
    if (!준비됨) return -100;
    if (TIPO_área != 1 && TIPO_área != 2) return -93;
    int identificador_de_arquivo = 예약하기(TIPO_área); if (identificador_de_arquivo < 0) return identificador_de_arquivo;
    soquete_empresa_3db661a2 *cadeia_dados = &통신끝점들[identificador_de_arquivo];
    if (TIPO_área == 1) { cadeia_dados->conexão_visual = tcp_new(); if (cadeia_dados->conexão_visual) 되부름목록(cadeia_dados); }
    else { cadeia_dados->datagrama_visual = udp_new(); if (cadeia_dados->datagrama_visual) udp_recv(cadeia_dados->datagrama_visual, datagrama, cadeia_dados); }
    if (!cadeia_dados->conexão_visual && !cadeia_dados->datagrama_visual) { cadeia_dados->TIPO_área = 0; return -12; } return identificador_de_arquivo;
}
int NET_BIND(int identificador_de_arquivo, uint32_t Endereço, unsigned número_da_porta) {
    soquete_empresa_3db661a2 *cadeia_dados = get_VALOR(identificador_de_arquivo); if (!cadeia_dados) return -9;
    if (número_da_porta > 65535 || (Endereço && Endereço != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&conexão_celular))) && Endereço != 0x7f000001)) return -99;
    ip_addr_t endereço_na_Internet; ip_addr_set_ip4_u32(&endereço_na_Internet, lwip_htonl(Endereço));
    err_t 보조항목 = cadeia_dados->TIPO_área == 1 ? tcp_bind(cadeia_dados->conexão_visual, &endereço_na_Internet, número_da_porta) : udp_bind(cadeia_dados->datagrama_visual, &endereço_na_Internet, número_da_porta); return 보조항목 ? número_do_erro(보조항목) : 0;
}
void 통신주소재사용(int identificador_de_arquivo) { soquete_empresa_3db661a2 *cadeia_dados = get_VALOR(identificador_de_arquivo); if (cadeia_dados && cadeia_dados->conexão_visual) ip_set_option(cadeia_dados->conexão_visual, SOF_REUSEADDR); }
int NET_escutar(int identificador_de_arquivo) {
    soquete_empresa_3db661a2 *cadeia_dados = get_VALOR(identificador_de_arquivo); if (!cadeia_dados || cadeia_dados->TIPO_área != 1) return -9;
    if (cadeia_dados->porta_de_recepção) return 0;
    err_t 보조항목; struct tcp_pcb *transmissão_visual_bloco = tcp_listen_with_backlog_and_err(cadeia_dados->conexão_visual, 4, &보조항목);
    if (!transmissão_visual_bloco) return número_do_erro(보조항목); cadeia_dados->conexão_visual = transmissão_visual_bloco; cadeia_dados->porta_de_recepção = 1; tcp_arg(transmissão_visual_bloco, cadeia_dados); tcp_accept(transmissão_visual_bloco, 연결받음); return 0;
}
int NET_Conexão(int identificador_de_arquivo, uint32_t Endereço, unsigned número_da_porta) {
    soquete_empresa_3db661a2 *cadeia_dados = get_VALOR(identificador_de_arquivo); if (!cadeia_dados || cadeia_dados->TIPO_área != 1) return -9;
    if (cadeia_dados->erro) return cadeia_dados->erro;
    if (cadeia_dados->연결됨) return 0;
    if (cadeia_dados->par_empresa_número) return -115;
    if (!número_da_porta || número_da_porta > 65535 || !Endereço) return -22;
    ip_addr_t endereço_na_Internet; ip_addr_set_ip4_u32(&endereço_na_Internet, lwip_htonl(Endereço));
    cadeia_dados->par_email = Endereço; cadeia_dados->par_empresa_número = número_da_porta;
    err_t 보조항목 = tcp_connect(cadeia_dados->conexão_visual, &endereço_na_Internet, número_da_porta, 연결됨); return 보조항목 ? número_do_erro(보조항목) : -115;
}
int NET_aceitar(int identificador_de_arquivo) {
    soquete_empresa_3db661a2 *cadeia_dados = get_VALOR(identificador_de_arquivo); if (!cadeia_dados || !cadeia_dados->porta_de_recepção) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TIPO_área == 1 && 통신끝점들[순번].TI_Pendente == identificador_de_arquivo) { 통신끝점들[순번].TI_Pendente = -1; return 순번; }
    return -11;
}
int NET_leitura(int identificador_de_arquivo, void *dados, unsigned item_CONT_NÚM) {
    soquete_empresa_3db661a2 *cadeia_dados = get_VALOR(identificador_de_arquivo); if (!cadeia_dados || cadeia_dados->TIPO_área != 1) return -9;
    if (!item_CONT_NÚM) return 0; if (!cadeia_dados->entrada_CONT_NÚM_8f7753a1) return cadeia_dados->erro ? cadeia_dados->erro : cadeia_dados->Arquivo_encerrar ? 0 : -11;
    if (item_CONT_NÚM > cadeia_dados->entrada_CONT_NÚM_8f7753a1) item_CONT_NÚM = cadeia_dados->entrada_CONT_NÚM_8f7753a1;
    for (unsigned 순번 = 0; 순번 < item_CONT_NÚM; 순번++) { ((unsigned char *)dados)[순번] = cadeia_dados->dados[cadeia_dados->câmera_frontal_entrada]; cadeia_dados->câmera_frontal_entrada = (cadeia_dados->câmera_frontal_entrada + 1) % sizeof(cadeia_dados->dados); }
    cadeia_dados->entrada_CONT_NÚM_8f7753a1 -= item_CONT_NÚM; if (cadeia_dados->conexão_visual) tcp_recved(cadeia_dados->conexão_visual, item_CONT_NÚM); return item_CONT_NÚM;
}
int NET_gravar(int identificador_de_arquivo, const void *dados, unsigned item_CONT_NÚM) {
    soquete_empresa_3db661a2 *cadeia_dados = get_VALOR(identificador_de_arquivo); if (!cadeia_dados || cadeia_dados->TIPO_área != 1) return -9;
    if (cadeia_dados->erro) return cadeia_dados->erro; if (!cadeia_dados->conexão_visual || !cadeia_dados->연결됨) return -107;
    if (!item_CONT_NÚM) return 0; if (item_CONT_NÚM > tcp_sndbuf(cadeia_dados->conexão_visual)) item_CONT_NÚM = tcp_sndbuf(cadeia_dados->conexão_visual);
    if (!item_CONT_NÚM) return -11; if (item_CONT_NÚM > 1024) item_CONT_NÚM = 1024;
    err_t 보조항목 = tcp_write(cadeia_dados->conexão_visual, dados, item_CONT_NÚM, TCP_WRITE_FLAG_COPY); if (보조항목) return número_do_erro(보조항목);
    tcp_output(cadeia_dados->conexão_visual); return item_CONT_NÚM;
}
int enviar_datagrama(int identificador_de_arquivo, const void *dados, unsigned item_CONT_NÚM, uint32_t Endereço, unsigned número_da_porta) {
    soquete_empresa_3db661a2 *cadeia_dados = get_VALOR(identificador_de_arquivo); if (!cadeia_dados || cadeia_dados->TIPO_área != 2) return -9;
    if (item_CONT_NÚM > 512) return -90; if (!número_da_porta || número_da_porta > 65535) return -22;
    struct pbuf *dados_cargo = pbuf_alloc(PBUF_TRANSPORT, item_CONT_NÚM, PBUF_RAM); if (!dados_cargo) return -11;
    pbuf_take(dados_cargo, dados, item_CONT_NÚM); ip_addr_t endereço_na_Internet; ip_addr_set_ip4_u32(&endereço_na_Internet, lwip_htonl(Endereço));
    err_t 보조항목 = udp_sendto(cadeia_dados->datagrama_visual, dados_cargo, &endereço_na_Internet, número_da_porta); pbuf_free(dados_cargo); return 보조항목 ? número_do_erro(보조항목) : (int)item_CONT_NÚM;
}
int receber_datagrama(int identificador_de_arquivo, void *dados, unsigned item_CONT_NÚM) {
    soquete_empresa_3db661a2 *cadeia_dados = get_VALOR(identificador_de_arquivo); if (!cadeia_dados || cadeia_dados->TIPO_área != 2) return -9;
    if (!cadeia_dados->entrada_CONT_NÚM_8f7753a1) return -11; unsigned em_dia_cargo = cadeia_dados->câmera_frontal_entrada;
    if (item_CONT_NÚM > cadeia_dados->길이목록[em_dia_cargo]) item_CONT_NÚM = cadeia_dados->길이목록[em_dia_cargo]; memcpy(dados, cadeia_dados->dados + em_dia_cargo * 512, item_CONT_NÚM);
    cadeia_dados->par_empresa_número = cadeia_dados->접속번호들[em_dia_cargo]; cadeia_dados->par_email = cadeia_dados->주소목록[em_dia_cargo]; cadeia_dados->câmera_frontal_entrada = (em_dia_cargo + 1) % 4; cadeia_dados->entrada_CONT_NÚM_8f7753a1--; return item_CONT_NÚM;
}
unsigned rede_número_da_porta(int identificador_de_arquivo) { soquete_empresa_3db661a2 *cadeia_dados = get_VALOR(identificador_de_arquivo); return !cadeia_dados ? 0 : cadeia_dados->conexão_visual ? cadeia_dados->conexão_visual->local_port : cadeia_dados->datagrama_visual ? cadeia_dados->datagrama_visual->local_port : 0; }
unsigned par_número_da_porta(int identificador_de_arquivo) { soquete_empresa_3db661a2 *cadeia_dados = get_VALOR(identificador_de_arquivo); return cadeia_dados ? cadeia_dados->par_empresa_número : 0; }
uint32_t NET_par_email(int identificador_de_arquivo) { soquete_empresa_3db661a2 *cadeia_dados = get_VALOR(identificador_de_arquivo); return cadeia_dados ? cadeia_dados->par_email : 0; }
void Close_rede(int identificador_de_arquivo) {
    soquete_empresa_3db661a2 *cadeia_dados = get_VALOR(identificador_de_arquivo); if (!cadeia_dados) return;
    if (cadeia_dados->porta_de_recepção) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TIPO_área && 통신끝점들[순번].TI_Pendente == identificador_de_arquivo) Close_rede(순번);
    if (cadeia_dados->conexão_visual) {
        tcp_arg(cadeia_dados->conexão_visual, 0); if (cadeia_dados->porta_de_recepção) tcp_accept(cadeia_dados->conexão_visual, 0); else { tcp_recv(cadeia_dados->conexão_visual, 0); tcp_err(cadeia_dados->conexão_visual, 0); }
        if (tcp_close(cadeia_dados->conexão_visual) != ERR_OK) tcp_abort(cadeia_dados->conexão_visual);
    }
    if (cadeia_dados->datagrama_visual) udp_remove(cadeia_dados->datagrama_visual); cadeia_dados->TIPO_área = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || sondagem) return; sondagem = 1;
    if(uso_com_fio_rede)유선망살피기(&conexão_celular);
    for (unsigned orçamento = 0; !uso_com_fio_rede && orçamento < 4096 && (computador_registro(보조장치 + 0x54) & 1); orçamento++) {
        unsigned ponto_de_código = computador_registro(보조장치 + 0x40) & 255;
        if (ponto_de_código == 192) {
            if (receber_uso && !receber_erro && !수신탈출) {
                struct pbuf *dados_cargo = pbuf_alloc(PBUF_RAW, receber_uso, PBUF_POOL);
                if (dados_cargo) { RECEBER_datagrama_CONT_NÚM++; RECEBER_byte_CONT_NÚM += receber_uso; pbuf_take(dados_cargo, receber_buffer_de_dados, receber_uso); if (conexão_celular.input(dados_cargo, &conexão_celular) != ERR_OK) { 버린전문수++; pbuf_free(dados_cargo); } }
                else 버린전문수++;
            }
            else if (receber_uso) 버린전문수++;
            receber_uso = receber_erro = 수신탈출 = 0;
        } else if (ponto_de_código == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (ponto_de_código != 220 && ponto_de_código != 221) receber_erro = 1; ponto_de_código = ponto_de_código == 220 ? 192 : 219; 수신탈출 = 0; }
            if (receber_uso < sizeof(receber_buffer_de_dados)) receber_buffer_de_dados[receber_uso++] = ponto_de_código; else receber_erro = 1;
        }
    }
    netif_poll(&conexão_celular); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned orçamento = 0; orçamento < 4096 && 송신개수 && (computador_registro(보조장치 + 0x54) & 0x20); orçamento++) {
        computador_registro(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    sondagem = 0;
}

/* Definições·조회는 lwIP의 real_dados 인터페이스와 encerrar_ponto 표를 사용한다. */
uint32_t leitura_rede_Status(unsigned entrada_VALOR_962f286b, unsigned ÍNDICE) {
    if(entrada_VALOR_962f286b==20)return uso_com_fio_rede;
    if(entrada_VALOR_962f286b==21)return 준비됨&&netif_is_link_up(&conexão_celular);
    if(entrada_VALOR_962f286b==22)return uso_com_fio_rede?com_fio_rede_Estatísticas(5):0;
    if (!준비됨) return 0;
    if(uso_com_fio_rede&&entrada_VALOR_962f286b>=4&&entrada_VALOR_962f286b<=8)return com_fio_rede_Estatísticas(entrada_VALOR_962f286b-4);
    if (entrada_VALOR_962f286b == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&conexão_celular)));
    if (entrada_VALOR_962f286b == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&conexão_celular)));
    if (entrada_VALOR_962f286b == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&conexão_celular)));
    if (entrada_VALOR_962f286b == 3) return netif_is_up(&conexão_celular) != 0;
    if (entrada_VALOR_962f286b == 4) return RECEBER_datagrama_CONT_NÚM;
    if (entrada_VALOR_962f286b == 5) return 보낸전문수;
    if (entrada_VALOR_962f286b == 6) return RECEBER_byte_CONT_NÚM;
    if (entrada_VALOR_962f286b == 7) return 보낸바이트수;
    if (entrada_VALOR_962f286b == 8) return 버린전문수;
    if (entrada_VALOR_962f286b == 9) return 송신개수;
    if (ÍNDICE >= 32) return 0;
    soquete_empresa_3db661a2 *encerrar_ponto = &통신끝점들[ÍNDICE];
    if (entrada_VALOR_962f286b == 10) return encerrar_ponto->TIPO_área;
    if (!encerrar_ponto->TIPO_área) return 0;
    if (entrada_VALOR_962f286b == 11) return rede_número_da_porta(ÍNDICE);
    if (entrada_VALOR_962f286b == 12) return encerrar_ponto->par_email;
    if (entrada_VALOR_962f286b == 13) return encerrar_ponto->par_empresa_número;
    if (entrada_VALOR_962f286b == 14) return encerrar_ponto->porta_de_recepção ? 1 : encerrar_ponto->Arquivo_encerrar ? 3 : encerrar_ponto->erro ? 4 : encerrar_ponto->연결됨 ? 2 : 0;
    if (entrada_VALOR_962f286b == 15) return encerrar_ponto->entrada_CONT_NÚM_8f7753a1;
    if (entrada_VALOR_962f286b == 16) {
        const ip_addr_t *Endereço = encerrar_ponto->TIPO_área == 1 && encerrar_ponto->conexão_visual ? &encerrar_ponto->conexão_visual->local_ip :
            encerrar_ponto->TIPO_área == 2 && encerrar_ponto->datagrama_visual ? &encerrar_ponto->datagrama_visual->local_ip : 0;
        return Endereço ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Endereço))) : 0;
    }
    return 0;
}

int configurar_rede(unsigned Acção, uint32_t Endereço, uint32_t máscara_VALOR, uint32_t gateway_VALOR) {
    if (!준비됨) return -100;
    if (Acção == 1) { netif_set_up(&conexão_celular); return 0; }
    if (Acção == 2) { netif_set_down(&conexão_celular); return 0; }
    if (Acção != 0) return -22;
    /* 유니캐스트 IPv4, 연속 máscara_VALOR, 같은 망의 선택적 valor_padrão gateway_VALOR. */
    uint32_t 뒤집은가림 = ~máscara_VALOR;
    if (!máscara_VALOR || (뒤집은가림 & (뒤집은가림 + 1)) || !Endereço || (Endereço >> 24) == 127 ||
        (Endereço >> 24) == 0 || (Endereço >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(Endereço & 뒤집은가림) || (Endereço & 뒤집은가림) == 뒤집은가림)) ||
        (gateway_VALOR && ((gateway_VALOR & máscara_VALOR) != (Endereço & máscara_VALOR) || gateway_VALOR == Endereço || (gateway_VALOR >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(gateway_VALOR & 뒤집은가림) || (gateway_VALOR & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 Endereço 변경으로 몰래 끊지 않는다. */
    for (unsigned ÍNDICE = 0; ÍNDICE < 32; ÍNDICE++) if (통신끝점들[ÍNDICE].TIPO_área &&
        !(통신끝점들[ÍNDICE].porta_de_recepção && 통신끝점들[ÍNDICE].conexão_visual && ip_addr_isany(&통신끝점들[ÍNDICE].conexão_visual->local_ip))) return -16;
    if(uso_com_fio_rede)dhcp_stop(&conexão_celular);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(Endereço)); ip4_addr_set_u32(&새가림, lwip_htonl(máscara_VALOR)); ip4_addr_set_u32(&새관문, lwip_htonl(gateway_VALOR));
    netif_set_addr(&conexão_celular, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *réplica_empresa;
static uint32_t teste_email, teste_time, tempo_de_resposta;
static unsigned teste_SEQUÊNCIA, teste_identificador, réplica_SEQUÊNCIA;
static int réplica_Estado;
static u8_t 응답받음(void *argumentos, struct raw_pcb *encerrar_ponto, struct pbuf *dados, const ip_addr_t *Endereço) {
    (void)argumentos; (void)encerrar_ponto;
    unsigned char HEAD_VALOR[20], resposta[16];
    if (réplica_Estado != -11 || dados->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Endereço))) != teste_email || pbuf_copy_partial(dados, HEAD_VALOR, 20, 0) != 20) return 0;
    unsigned Cabeçalho_dimensionar = (HEAD_VALOR[0] & 15) * 4;
    if ((HEAD_VALOR[0] >> 4) != 4 || Cabeçalho_dimensionar < 20 || dados->tot_len < Cabeçalho_dimensionar + 16 ||
        pbuf_copy_partial(dados, resposta, 16, Cabeçalho_dimensionar) != 16 || resposta[0] || resposta[1] ||
        (((unsigned)resposta[4] << 8) | resposta[5]) != teste_identificador ||
        (((unsigned)resposta[6] << 8) | resposta[7]) != teste_SEQUÊNCIA ||
        resposta[8] != 'J' || resposta[9] != 'K' || resposta[10] != 'O' || resposta[11] != 'S' ||
        (((uint32_t)resposta[12] << 24) | ((uint32_t)resposta[13] << 16) | ((uint32_t)resposta[14] << 8) | resposta[15]) != teste_time) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(dados, Cabeçalho_dimensionar)) return 0;
    if (inet_chksum_pbuf(dados)) { pbuf_add_header(dados, Cabeçalho_dimensionar); return 0; }
    tempo_de_resposta = (uint32_t)보드밀리초() - teste_time; réplica_SEQUÊNCIA = HEAD_VALOR[8]; réplica_Estado = 0;
    pbuf_free(dados); return 1;
}
int START_réplica_teste(uint32_t Endereço, unsigned ordem_VALOR) {
    if (!준비됨 || !netif_is_up(&conexão_celular)) return -100;
    if (!Endereço || (Endereço >> 28) >= 14 || Endereço == 0xffffffffu) return -22;
    if (!réplica_empresa) { réplica_empresa = raw_new(IP_PROTO_ICMP); if (!réplica_empresa) return -12; raw_recv(réplica_empresa, 응답받음, 0); }
    teste_email = Endereço; teste_SEQUÊNCIA = ordem_VALOR & 65535; teste_identificador = (teste_identificador + 1) & 65535;
    teste_time = 보드밀리초(); réplica_Estado = -11; tempo_de_resposta = réplica_SEQUÊNCIA = 0;
    unsigned char dados[32] = {8,0,0,0};
    dados[4] = teste_identificador >> 8; dados[5] = teste_identificador; dados[6] = teste_SEQUÊNCIA >> 8; dados[7] = teste_SEQUÊNCIA;
    dados[8]='J'; dados[9]='K'; dados[10]='O'; dados[11]='S';
    dados[12]=teste_time >> 24; dados[13]=teste_time >> 16; dados[14]=teste_time >> 8; dados[15]=teste_time;
    for (unsigned cargo_ÍNDICE = 16; cargo_ÍNDICE < sizeof(dados); cargo_ÍNDICE++) dados[cargo_ÍNDICE] = cargo_ÍNDICE;
    uint16_t verificação_soma_de_verificação = inet_chksum(dados, sizeof(dados)); memcpy(dados + 2, &verificação_soma_de_verificação, 2);
    struct pbuf *datagrama = pbuf_alloc(PBUF_IP, sizeof(dados), PBUF_RAM); if (!datagrama) return -12;
    pbuf_take(datagrama, dados, sizeof(dados)); ip_addr_t destino_empresa; ip_addr_set_ip4_u32(&destino_empresa, lwip_htonl(Endereço));
    err_t 처리값 = raw_sendto(réplica_empresa, datagrama, &destino_empresa); pbuf_free(datagrama);
    if (처리값) réplica_Estado = número_do_erro(처리값);
    return 처리값 ? réplica_Estado : 0;
}
int leitura_réplica_teste(unsigned entrada_VALOR_962f286b) {
    통신망살피기();
    return entrada_VALOR_962f286b == 0 ? réplica_Estado : entrada_VALOR_962f286b == 1 ? (int)tempo_de_resposta : entrada_VALOR_962f286b == 2 ? (int)réplica_SEQUÊNCIA : -22;
}
