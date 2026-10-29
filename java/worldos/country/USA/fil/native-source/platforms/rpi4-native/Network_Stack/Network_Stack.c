#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Network_Stack.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../malayuan_VALUE/malayuan_VALUE.h"
#include "naka_wire_Network.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define machine_magrehistro(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif koneksyon_device;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_byte_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_kategorya, 수신창구, information_technology_pending, 연결됨, file_tapusin, error;
    struct tcp_pcb *koneksyon_control;
    struct udp_pcb *전문제어;
    unsigned nasa_harap_pagpasok, pagpasok_COUNT;
    unsigned char data[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], peer_email;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *get_VALUE(int file_hawakán) { return file_hawakán >= 0 && file_hawakán < 32 && 통신끝점들[file_hawakán].TYPE_kategorya ? &통신끝점들[file_hawakán] : 0; }
static int 예약하기(int TYPE_kategorya) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_kategorya) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_kategorya = TYPE_kategorya; 통신끝점들[순번].information_technology_pending = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned character_code) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = character_code; }
static err_t 출력결과(struct netif *item_COUNT, struct pbuf *data_posisyon, const ip4_addr_t *email) {
    (void)item_COUNT; (void)email;
    if (data_posisyon->tot_len > 1500 || 송신개수 + 2 * data_posisyon->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Susunod_OFFSET = data_posisyon; Susunod_OFFSET; Susunod_OFFSET = Susunod_OFFSET->next) for (unsigned 순번 = 0; 순번 < Susunod_OFFSET->len; 순번++) {
        unsigned character_code = ((unsigned char *)Susunod_OFFSET->payload)[순번];
        if (character_code == 192 || character_code == 219) { 내보내기(219); 내보내기(character_code == 192 ? 220 : 221); } else 내보내기(character_code);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += data_posisyon->tot_len; return ERR_OK;
}
static err_t Ihanda_common_language_runtime(struct netif *item_COUNT) { item_COUNT->name[0] = 's'; item_COUNT->name[1] = 'l'; item_COUNT->mtu = 1500; item_COUNT->output = 출력결과; return ERR_OK; }
void Ihanda_Network(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    machine_magrehistro(보조장치 + 4) |= 1; machine_magrehistro(보조장치 + 0x60) = 0; machine_magrehistro(보조장치 + 0x44) = 0;
    machine_magrehistro(보조장치 + 0x48) = 0xc6; machine_magrehistro(보조장치 + 0x4c) = 3; machine_magrehistro(보조장치 + 0x68) = 270; machine_magrehistro(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Internet_address, bit_mask, entrada_email;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&Internet_address, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_mask, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&entrada_email, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&koneksyon_device, &Internet_address, &bit_mask, &entrada_email, 0, 유선사용?Ihanda_naka_wire_Network:Ihanda_common_language_runtime, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&koneksyon_device); netif_set_up(&koneksyon_device);if(!유선사용)netif_set_link_up(&koneksyon_device); 준비됨 = 1;
    Ihanda_malayuan();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *pagpapadala_control_i_block, struct pbuf *data_posisyon, err_t error) {
    통신끝점 *string_data = 부가인수; (void)pagpapadala_control_i_block; (void)error;
    if (!data_posisyon) { string_data->file_tapusin = 1; return ERR_OK; }
    if (data_posisyon->tot_len > sizeof(string_data->data) - string_data->pagpasok_COUNT) return ERR_MEM;
    unsigned 현재위치 = (string_data->nasa_harap_pagpasok + string_data->pagpasok_COUNT) % sizeof(string_data->data);
    for (struct pbuf *Susunod_OFFSET = data_posisyon; Susunod_OFFSET; Susunod_OFFSET = Susunod_OFFSET->next) for (unsigned 순번 = 0; 순번 < Susunod_OFFSET->len; 순번++) {
        string_data->data[현재위치] = ((unsigned char *)Susunod_OFFSET->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(string_data->data);
    }
    string_data->pagpasok_COUNT += data_posisyon->tot_len; pbuf_free(data_posisyon); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t error) { 통신끝점 *string_data = 부가인수; string_data->koneksyon_control = 0; string_data->error = 오류번호(error); }
static void 되부름목록(통신끝점 *string_data) { tcp_arg(string_data->koneksyon_control, string_data); tcp_recv(string_data->koneksyon_control, 수신됨); tcp_err(string_data->koneksyon_control, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *pagpapadala_control_i_block, err_t error) {
    통신끝점 *string_data = 부가인수; (void)pagpapadala_control_i_block; if (error) string_data->error = 오류번호(error); else string_data->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *pagpapadala_control_i_block, err_t error) {
    통신끝점 *부모항목 = 부가인수; if (error) return error;
    int file_hawakán = 예약하기(1); if (file_hawakán < 0) return ERR_MEM;
    통신끝점 *string_data = &통신끝점들[file_hawakán]; string_data->koneksyon_control = pagpapadala_control_i_block; string_data->연결됨 = 1; string_data->information_technology_pending = (int)(부모항목 - 통신끝점들);
    string_data->peer_email = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&pagpapadala_control_i_block->remote_ip))); string_data->상대창구번호 = pagpapadala_control_i_block->remote_port;
    되부름목록(string_data); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *pagpapadala_control_i_block, struct pbuf *data_posisyon, const ip_addr_t *email, u16_t numero_ng_port) {
    통신끝점 *string_data = 부가인수; (void)pagpapadala_control_i_block;
    if (string_data->pagpasok_COUNT < 4 && data_posisyon->tot_len <= 512) {
        unsigned posisyon_INDEX = (string_data->nasa_harap_pagpasok + string_data->pagpasok_COUNT) % 4;
        pbuf_copy_partial(data_posisyon, string_data->data + posisyon_INDEX * 512, data_posisyon->tot_len, 0);
        string_data->길이목록[posisyon_INDEX] = data_posisyon->tot_len; string_data->접속번호들[posisyon_INDEX] = numero_ng_port;
        string_data->주소목록[posisyon_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(email))); string_data->pagpasok_COUNT++;
    }
    pbuf_free(data_posisyon);
}
int 통신끝점만들기(int TYPE_kategorya) {
    if (!준비됨) return -100;
    if (TYPE_kategorya != 1 && TYPE_kategorya != 2) return -93;
    int file_hawakán = 예약하기(TYPE_kategorya); if (file_hawakán < 0) return file_hawakán;
    통신끝점 *string_data = &통신끝점들[file_hawakán];
    if (TYPE_kategorya == 1) { string_data->koneksyon_control = tcp_new(); if (string_data->koneksyon_control) 되부름목록(string_data); }
    else { string_data->전문제어 = udp_new(); if (string_data->전문제어) udp_recv(string_data->전문제어, 전문, string_data); }
    if (!string_data->koneksyon_control && !string_data->전문제어) { string_data->TYPE_kategorya = 0; return -12; } return file_hawakán;
}
int 망주소묶기(int file_hawakán, uint32_t email, unsigned numero_ng_port) {
    통신끝점 *string_data = get_VALUE(file_hawakán); if (!string_data) return -9;
    if (numero_ng_port > 65535 || (email && email != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&koneksyon_device))) && email != 0x7f000001)) return -99;
    ip_addr_t Internet_address; ip_addr_set_ip4_u32(&Internet_address, lwip_htonl(email));
    err_t 보조항목 = string_data->TYPE_kategorya == 1 ? tcp_bind(string_data->koneksyon_control, &Internet_address, numero_ng_port) : udp_bind(string_data->전문제어, &Internet_address, numero_ng_port); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int file_hawakán) { 통신끝점 *string_data = get_VALUE(file_hawakán); if (string_data && string_data->koneksyon_control) ip_set_option(string_data->koneksyon_control, SOF_REUSEADDR); }
int 연결기다리기(int file_hawakán) {
    통신끝점 *string_data = get_VALUE(file_hawakán); if (!string_data || string_data->TYPE_kategorya != 1) return -9;
    if (string_data->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *pagpapadala_control_i_block = tcp_listen_with_backlog_and_err(string_data->koneksyon_control, 4, &보조항목);
    if (!pagpapadala_control_i_block) return 오류번호(보조항목); string_data->koneksyon_control = pagpapadala_control_i_block; string_data->수신창구 = 1; tcp_arg(pagpapadala_control_i_block, string_data); tcp_accept(pagpapadala_control_i_block, 연결받음); return 0;
}
int 망연결하기(int file_hawakán, uint32_t email, unsigned numero_ng_port) {
    통신끝점 *string_data = get_VALUE(file_hawakán); if (!string_data || string_data->TYPE_kategorya != 1) return -9;
    if (string_data->error) return string_data->error;
    if (string_data->연결됨) return 0;
    if (string_data->상대창구번호) return -115;
    if (!numero_ng_port || numero_ng_port > 65535 || !email) return -22;
    ip_addr_t Internet_address; ip_addr_set_ip4_u32(&Internet_address, lwip_htonl(email));
    string_data->peer_email = email; string_data->상대창구번호 = numero_ng_port;
    err_t 보조항목 = tcp_connect(string_data->koneksyon_control, &Internet_address, numero_ng_port, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int file_hawakán) {
    통신끝점 *string_data = get_VALUE(file_hawakán); if (!string_data || !string_data->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_kategorya == 1 && 통신끝점들[순번].information_technology_pending == file_hawakán) { 통신끝점들[순번].information_technology_pending = -1; return 순번; }
    return -11;
}
int 통신읽기(int file_hawakán, void *data, unsigned item_COUNT) {
    통신끝점 *string_data = get_VALUE(file_hawakán); if (!string_data || string_data->TYPE_kategorya != 1) return -9;
    if (!item_COUNT) return 0; if (!string_data->pagpasok_COUNT) return string_data->error ? string_data->error : string_data->file_tapusin ? 0 : -11;
    if (item_COUNT > string_data->pagpasok_COUNT) item_COUNT = string_data->pagpasok_COUNT;
    for (unsigned 순번 = 0; 순번 < item_COUNT; 순번++) { ((unsigned char *)data)[순번] = string_data->data[string_data->nasa_harap_pagpasok]; string_data->nasa_harap_pagpasok = (string_data->nasa_harap_pagpasok + 1) % sizeof(string_data->data); }
    string_data->pagpasok_COUNT -= item_COUNT; if (string_data->koneksyon_control) tcp_recved(string_data->koneksyon_control, item_COUNT); return item_COUNT;
}
int 통신쓰기(int file_hawakán, const void *data, unsigned item_COUNT) {
    통신끝점 *string_data = get_VALUE(file_hawakán); if (!string_data || string_data->TYPE_kategorya != 1) return -9;
    if (string_data->error) return string_data->error; if (!string_data->koneksyon_control || !string_data->연결됨) return -107;
    if (!item_COUNT) return 0; if (item_COUNT > tcp_sndbuf(string_data->koneksyon_control)) item_COUNT = tcp_sndbuf(string_data->koneksyon_control);
    if (!item_COUNT) return -11; if (item_COUNT > 1024) item_COUNT = 1024;
    err_t 보조항목 = tcp_write(string_data->koneksyon_control, data, item_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(string_data->koneksyon_control); return item_COUNT;
}
int 전문보내기(int file_hawakán, const void *data, unsigned item_COUNT, uint32_t email, unsigned numero_ng_port) {
    통신끝점 *string_data = get_VALUE(file_hawakán); if (!string_data || string_data->TYPE_kategorya != 2) return -9;
    if (item_COUNT > 512) return -90; if (!numero_ng_port || numero_ng_port > 65535) return -22;
    struct pbuf *data_posisyon = pbuf_alloc(PBUF_TRANSPORT, item_COUNT, PBUF_RAM); if (!data_posisyon) return -11;
    pbuf_take(data_posisyon, data, item_COUNT); ip_addr_t Internet_address; ip_addr_set_ip4_u32(&Internet_address, lwip_htonl(email));
    err_t 보조항목 = udp_sendto(string_data->전문제어, data_posisyon, &Internet_address, numero_ng_port); pbuf_free(data_posisyon); return 보조항목 ? 오류번호(보조항목) : (int)item_COUNT;
}
int 전문받기(int file_hawakán, void *data, unsigned item_COUNT) {
    통신끝점 *string_data = get_VALUE(file_hawakán); if (!string_data || string_data->TYPE_kategorya != 2) return -9;
    if (!string_data->pagpasok_COUNT) return -11; unsigned 현재위치 = string_data->nasa_harap_pagpasok;
    if (item_COUNT > string_data->길이목록[현재위치]) item_COUNT = string_data->길이목록[현재위치]; memcpy(data, string_data->data + 현재위치 * 512, item_COUNT);
    string_data->상대창구번호 = string_data->접속번호들[현재위치]; string_data->peer_email = string_data->주소목록[현재위치]; string_data->nasa_harap_pagpasok = (현재위치 + 1) % 4; string_data->pagpasok_COUNT--; return item_COUNT;
}
unsigned Network_numero_ng_port(int file_hawakán) { 통신끝점 *string_data = get_VALUE(file_hawakán); return !string_data ? 0 : string_data->koneksyon_control ? string_data->koneksyon_control->local_port : string_data->전문제어 ? string_data->전문제어->local_port : 0; }
unsigned peer_numero_ng_port(int file_hawakán) { 통신끝점 *string_data = get_VALUE(file_hawakán); return string_data ? string_data->상대창구번호 : 0; }
uint32_t 상대통신주소(int file_hawakán) { 통신끝점 *string_data = get_VALUE(file_hawakán); return string_data ? string_data->peer_email : 0; }
void isara_Network(int file_hawakán) {
    통신끝점 *string_data = get_VALUE(file_hawakán); if (!string_data) return;
    if (string_data->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_kategorya && 통신끝점들[순번].information_technology_pending == file_hawakán) isara_Network(순번);
    if (string_data->koneksyon_control) {
        tcp_arg(string_data->koneksyon_control, 0); if (string_data->수신창구) tcp_accept(string_data->koneksyon_control, 0); else { tcp_recv(string_data->koneksyon_control, 0); tcp_err(string_data->koneksyon_control, 0); }
        if (tcp_close(string_data->koneksyon_control) != ERR_OK) tcp_abort(string_data->koneksyon_control);
    }
    if (string_data->전문제어) udp_remove(string_data->전문제어); string_data->TYPE_kategorya = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&koneksyon_device);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (machine_magrehistro(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned character_code = machine_magrehistro(보조장치 + 0x40) & 255;
        if (character_code == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *data_posisyon = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (data_posisyon) { 받은전문수++; RECEIVED_byte_COUNT += 수신사용량; pbuf_take(data_posisyon, 수신자료, 수신사용량); if (koneksyon_device.input(data_posisyon, &koneksyon_device) != ERR_OK) { 버린전문수++; pbuf_free(data_posisyon); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (character_code == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (character_code != 220 && character_code != 221) 수신오류 = 1; character_code = character_code == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = character_code; else 수신오류 = 1;
        }
    }
    netif_poll(&koneksyon_device); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (machine_magrehistro(보조장치 + 0x54) & 0x20); 처리한도++) {
        machine_magrehistro(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Mga_Setting·조회는 lwIP의 totoo_data 인터페이스와 tapusin_point 표를 사용한다. */
uint32_t 망상태읽기(unsigned pagpasok_VALUE, unsigned INDEX) {
    if(pagpasok_VALUE==20)return 유선사용;
    if(pagpasok_VALUE==21)return 준비됨&&netif_is_link_up(&koneksyon_device);
    if(pagpasok_VALUE==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&pagpasok_VALUE>=4&&pagpasok_VALUE<=8)return 유선망집계(pagpasok_VALUE-4);
    if (pagpasok_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&koneksyon_device)));
    if (pagpasok_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&koneksyon_device)));
    if (pagpasok_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&koneksyon_device)));
    if (pagpasok_VALUE == 3) return netif_is_up(&koneksyon_device) != 0;
    if (pagpasok_VALUE == 4) return 받은전문수;
    if (pagpasok_VALUE == 5) return 보낸전문수;
    if (pagpasok_VALUE == 6) return RECEIVED_byte_COUNT;
    if (pagpasok_VALUE == 7) return 보낸바이트수;
    if (pagpasok_VALUE == 8) return 버린전문수;
    if (pagpasok_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *tapusin_point = &통신끝점들[INDEX];
    if (pagpasok_VALUE == 10) return tapusin_point->TYPE_kategorya;
    if (!tapusin_point->TYPE_kategorya) return 0;
    if (pagpasok_VALUE == 11) return Network_numero_ng_port(INDEX);
    if (pagpasok_VALUE == 12) return tapusin_point->peer_email;
    if (pagpasok_VALUE == 13) return tapusin_point->상대창구번호;
    if (pagpasok_VALUE == 14) return tapusin_point->수신창구 ? 1 : tapusin_point->file_tapusin ? 3 : tapusin_point->error ? 4 : tapusin_point->연결됨 ? 2 : 0;
    if (pagpasok_VALUE == 15) return tapusin_point->pagpasok_COUNT;
    if (pagpasok_VALUE == 16) {
        const ip_addr_t *email = tapusin_point->TYPE_kategorya == 1 && tapusin_point->koneksyon_control ? &tapusin_point->koneksyon_control->local_ip :
            tapusin_point->TYPE_kategorya == 2 && tapusin_point->전문제어 ? &tapusin_point->전문제어->local_ip : 0;
        return email ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(email))) : 0;
    }
    return 0;
}

int magkompigura_Network(unsigned aksyon, uint32_t email, uint32_t mask_VALUE, uint32_t entrada_VALUE) {
    if (!준비됨) return -100;
    if (aksyon == 1) { netif_set_up(&koneksyon_device); return 0; }
    if (aksyon == 2) { netif_set_down(&koneksyon_device); return 0; }
    if (aksyon != 0) return -22;
    /* 유니캐스트 IPv4, 연속 mask_VALUE, 같은 망의 선택적 value_ng_default entrada_VALUE. */
    uint32_t 뒤집은가림 = ~mask_VALUE;
    if (!mask_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !email || (email >> 24) == 127 ||
        (email >> 24) == 0 || (email >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(email & 뒤집은가림) || (email & 뒤집은가림) == 뒤집은가림)) ||
        (entrada_VALUE && ((entrada_VALUE & mask_VALUE) != (email & mask_VALUE) || entrada_VALUE == email || (entrada_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(entrada_VALUE & 뒤집은가림) || (entrada_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 email 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_kategorya &&
        !(통신끝점들[INDEX].수신창구 && 통신끝점들[INDEX].koneksyon_control && ip_addr_isany(&통신끝점들[INDEX].koneksyon_control->local_ip))) return -16;
    if(유선사용)dhcp_stop(&koneksyon_device);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(email)); ip4_addr_set_u32(&새가림, lwip_htonl(mask_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(entrada_VALUE));
    netif_set_addr(&koneksyon_device, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *tapusin_point, struct pbuf *data, const ip_addr_t *email) {
    (void)인수; (void)tapusin_point;
    unsigned char 머리[20], tumugon[16];
    if (응답상태 != -11 || data->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(email))) != 시험주소 || pbuf_copy_partial(data, 머리, 20, 0) != 20) return 0;
    unsigned Header_sukat = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Header_sukat < 20 || data->tot_len < Header_sukat + 16 ||
        pbuf_copy_partial(data, tumugon, 16, Header_sukat) != 16 || tumugon[0] || tumugon[1] ||
        (((unsigned)tumugon[4] << 8) | tumugon[5]) != 시험식별자 ||
        (((unsigned)tumugon[6] << 8) | tumugon[7]) != 시험순서 ||
        tumugon[8] != 'J' || tumugon[9] != 'K' || tumugon[10] != 'O' || tumugon[11] != 'S' ||
        (((uint32_t)tumugon[12] << 24) | ((uint32_t)tumugon[13] << 16) | ((uint32_t)tumugon[14] << 8) | tumugon[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(data, Header_sukat)) return 0;
    if (inet_chksum_pbuf(data)) { pbuf_add_header(data, Header_sukat); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(data); return 1;
}
int 응답시험시작(uint32_t email, unsigned pagkakasunud_sunod_VALUE) {
    if (!준비됨 || !netif_is_up(&koneksyon_device)) return -100;
    if (!email || (email >> 28) >= 14 || email == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = email; 시험순서 = pagkakasunud_sunod_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char data[32] = {8,0,0,0};
    data[4] = 시험식별자 >> 8; data[5] = 시험식별자; data[6] = 시험순서 >> 8; data[7] = 시험순서;
    data[8]='J'; data[9]='K'; data[10]='O'; data[11]='S';
    data[12]=시험시각 >> 24; data[13]=시험시각 >> 16; data[14]=시험시각 >> 8; data[15]=시험시각;
    for (unsigned posisyon_INDEX = 16; posisyon_INDEX < sizeof(data); posisyon_INDEX++) data[posisyon_INDEX] = posisyon_INDEX;
    uint16_t beripikasyon_checksum = inet_chksum(data, sizeof(data)); memcpy(data + 2, &beripikasyon_checksum, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(data), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, data, sizeof(data)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(email));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned pagpasok_VALUE) {
    통신망살피기();
    return pagpasok_VALUE == 0 ? 응답상태 : pagpasok_VALUE == 1 ? (int)응답시간 : pagpasok_VALUE == 2 ? (int)응답차례 : -22;
}
