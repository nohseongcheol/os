#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "rangkaian_tindan.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../jauh_VALUE/jauh_VALUE.h"
#include "berwayar_rangkaian.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define mesin_daftar(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif hubungan_peranti;
static int 준비됨, undian;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_bait_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_bidang, 수신창구, teknologi_maklumat_belum_selesai, 연결됨, fail_tamat, RALAT;
    struct tcp_pcb *hubungan_kawalan;
    struct udp_pcb *전문제어;
    unsigned hadapan_pemasukan, pemasukan_COUNT;
    unsigned char data[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], rakan_e_mel;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *dapatkan_VALUE(int fail_pemegang) { return fail_pemegang >= 0 && fail_pemegang < 32 && 통신끝점들[fail_pemegang].TYPE_bidang ? &통신끝점들[fail_pemegang] : 0; }
static int 예약하기(int TYPE_bidang) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_bidang) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_bidang = TYPE_bidang; 통신끝점들[순번].teknologi_maklumat_belum_selesai = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned titik_kod) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = titik_kod; }
static err_t 출력결과(struct netif *item_COUNT, struct pbuf *data_jawatan, const ip4_addr_t *e_mel) {
    (void)item_COUNT; (void)e_mel;
    if (data_jawatan->tot_len > 1500 || 송신개수 + 2 * data_jawatan->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Seterusnya_Ofset = data_jawatan; Seterusnya_Ofset; Seterusnya_Ofset = Seterusnya_Ofset->next) for (unsigned 순번 = 0; 순번 < Seterusnya_Ofset->len; 순번++) {
        unsigned titik_kod = ((unsigned char *)Seterusnya_Ofset->payload)[순번];
        if (titik_kod == 192 || titik_kod == 219) { 내보내기(219); 내보내기(titik_kod == 192 ? 220 : 221); } else 내보내기(titik_kod);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += data_jawatan->tot_len; return ERR_OK;
}
static err_t Sediakan_masa_jalan_bahasa_biasa(struct netif *item_COUNT) { item_COUNT->name[0] = 's'; item_COUNT->name[1] = 'l'; item_COUNT->mtu = 1500; item_COUNT->output = 출력결과; return ERR_OK; }
void Sediakan_rangkaian(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    mesin_daftar(보조장치 + 4) |= 1; mesin_daftar(보조장치 + 0x60) = 0; mesin_daftar(보조장치 + 0x44) = 0;
    mesin_daftar(보조장치 + 0x48) = 0xc6; mesin_daftar(보조장치 + 0x4c) = 3; mesin_daftar(보조장치 + 0x68) = 270; mesin_daftar(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t alamat_Internet, bitmask, get_laluan_e_mel;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&alamat_Internet, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bitmask, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&get_laluan_e_mel, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&hubungan_peranti, &alamat_Internet, &bitmask, &get_laluan_e_mel, 0, 유선사용?Sediakan_berwayar_rangkaian:Sediakan_masa_jalan_bahasa_biasa, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&hubungan_peranti); netif_set_up(&hubungan_peranti);if(!유선사용)netif_set_link_up(&hubungan_peranti); 준비됨 = 1;
    Sediakan_jauh();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *penghantaran_kawalan_blok, struct pbuf *data_jawatan, err_t RALAT) {
    통신끝점 *rentetan_data = 부가인수; (void)penghantaran_kawalan_blok; (void)RALAT;
    if (!data_jawatan) { rentetan_data->fail_tamat = 1; return ERR_OK; }
    if (data_jawatan->tot_len > sizeof(rentetan_data->data) - rentetan_data->pemasukan_COUNT) return ERR_MEM;
    unsigned 현재위치 = (rentetan_data->hadapan_pemasukan + rentetan_data->pemasukan_COUNT) % sizeof(rentetan_data->data);
    for (struct pbuf *Seterusnya_Ofset = data_jawatan; Seterusnya_Ofset; Seterusnya_Ofset = Seterusnya_Ofset->next) for (unsigned 순번 = 0; 순번 < Seterusnya_Ofset->len; 순번++) {
        rentetan_data->data[현재위치] = ((unsigned char *)Seterusnya_Ofset->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(rentetan_data->data);
    }
    rentetan_data->pemasukan_COUNT += data_jawatan->tot_len; pbuf_free(data_jawatan); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t RALAT) { 통신끝점 *rentetan_data = 부가인수; rentetan_data->hubungan_kawalan = 0; rentetan_data->RALAT = 오류번호(RALAT); }
static void 되부름목록(통신끝점 *rentetan_data) { tcp_arg(rentetan_data->hubungan_kawalan, rentetan_data); tcp_recv(rentetan_data->hubungan_kawalan, 수신됨); tcp_err(rentetan_data->hubungan_kawalan, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *penghantaran_kawalan_blok, err_t RALAT) {
    통신끝점 *rentetan_data = 부가인수; (void)penghantaran_kawalan_blok; if (RALAT) rentetan_data->RALAT = 오류번호(RALAT); else rentetan_data->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *penghantaran_kawalan_blok, err_t RALAT) {
    통신끝점 *부모항목 = 부가인수; if (RALAT) return RALAT;
    int fail_pemegang = 예약하기(1); if (fail_pemegang < 0) return ERR_MEM;
    통신끝점 *rentetan_data = &통신끝점들[fail_pemegang]; rentetan_data->hubungan_kawalan = penghantaran_kawalan_blok; rentetan_data->연결됨 = 1; rentetan_data->teknologi_maklumat_belum_selesai = (int)(부모항목 - 통신끝점들);
    rentetan_data->rakan_e_mel = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&penghantaran_kawalan_blok->remote_ip))); rentetan_data->상대창구번호 = penghantaran_kawalan_blok->remote_port;
    되부름목록(rentetan_data); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *penghantaran_kawalan_blok, struct pbuf *data_jawatan, const ip_addr_t *e_mel, u16_t nombor_port) {
    통신끝점 *rentetan_data = 부가인수; (void)penghantaran_kawalan_blok;
    if (rentetan_data->pemasukan_COUNT < 4 && data_jawatan->tot_len <= 512) {
        unsigned jawatan_INDEX = (rentetan_data->hadapan_pemasukan + rentetan_data->pemasukan_COUNT) % 4;
        pbuf_copy_partial(data_jawatan, rentetan_data->data + jawatan_INDEX * 512, data_jawatan->tot_len, 0);
        rentetan_data->길이목록[jawatan_INDEX] = data_jawatan->tot_len; rentetan_data->접속번호들[jawatan_INDEX] = nombor_port;
        rentetan_data->주소목록[jawatan_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(e_mel))); rentetan_data->pemasukan_COUNT++;
    }
    pbuf_free(data_jawatan);
}
int 통신끝점만들기(int TYPE_bidang) {
    if (!준비됨) return -100;
    if (TYPE_bidang != 1 && TYPE_bidang != 2) return -93;
    int fail_pemegang = 예약하기(TYPE_bidang); if (fail_pemegang < 0) return fail_pemegang;
    통신끝점 *rentetan_data = &통신끝점들[fail_pemegang];
    if (TYPE_bidang == 1) { rentetan_data->hubungan_kawalan = tcp_new(); if (rentetan_data->hubungan_kawalan) 되부름목록(rentetan_data); }
    else { rentetan_data->전문제어 = udp_new(); if (rentetan_data->전문제어) udp_recv(rentetan_data->전문제어, 전문, rentetan_data); }
    if (!rentetan_data->hubungan_kawalan && !rentetan_data->전문제어) { rentetan_data->TYPE_bidang = 0; return -12; } return fail_pemegang;
}
int 망주소묶기(int fail_pemegang, uint32_t e_mel, unsigned nombor_port) {
    통신끝점 *rentetan_data = dapatkan_VALUE(fail_pemegang); if (!rentetan_data) return -9;
    if (nombor_port > 65535 || (e_mel && e_mel != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&hubungan_peranti))) && e_mel != 0x7f000001)) return -99;
    ip_addr_t alamat_Internet; ip_addr_set_ip4_u32(&alamat_Internet, lwip_htonl(e_mel));
    err_t 보조항목 = rentetan_data->TYPE_bidang == 1 ? tcp_bind(rentetan_data->hubungan_kawalan, &alamat_Internet, nombor_port) : udp_bind(rentetan_data->전문제어, &alamat_Internet, nombor_port); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int fail_pemegang) { 통신끝점 *rentetan_data = dapatkan_VALUE(fail_pemegang); if (rentetan_data && rentetan_data->hubungan_kawalan) ip_set_option(rentetan_data->hubungan_kawalan, SOF_REUSEADDR); }
int 연결기다리기(int fail_pemegang) {
    통신끝점 *rentetan_data = dapatkan_VALUE(fail_pemegang); if (!rentetan_data || rentetan_data->TYPE_bidang != 1) return -9;
    if (rentetan_data->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *penghantaran_kawalan_blok = tcp_listen_with_backlog_and_err(rentetan_data->hubungan_kawalan, 4, &보조항목);
    if (!penghantaran_kawalan_blok) return 오류번호(보조항목); rentetan_data->hubungan_kawalan = penghantaran_kawalan_blok; rentetan_data->수신창구 = 1; tcp_arg(penghantaran_kawalan_blok, rentetan_data); tcp_accept(penghantaran_kawalan_blok, 연결받음); return 0;
}
int 망연결하기(int fail_pemegang, uint32_t e_mel, unsigned nombor_port) {
    통신끝점 *rentetan_data = dapatkan_VALUE(fail_pemegang); if (!rentetan_data || rentetan_data->TYPE_bidang != 1) return -9;
    if (rentetan_data->RALAT) return rentetan_data->RALAT;
    if (rentetan_data->연결됨) return 0;
    if (rentetan_data->상대창구번호) return -115;
    if (!nombor_port || nombor_port > 65535 || !e_mel) return -22;
    ip_addr_t alamat_Internet; ip_addr_set_ip4_u32(&alamat_Internet, lwip_htonl(e_mel));
    rentetan_data->rakan_e_mel = e_mel; rentetan_data->상대창구번호 = nombor_port;
    err_t 보조항목 = tcp_connect(rentetan_data->hubungan_kawalan, &alamat_Internet, nombor_port, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int fail_pemegang) {
    통신끝점 *rentetan_data = dapatkan_VALUE(fail_pemegang); if (!rentetan_data || !rentetan_data->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_bidang == 1 && 통신끝점들[순번].teknologi_maklumat_belum_selesai == fail_pemegang) { 통신끝점들[순번].teknologi_maklumat_belum_selesai = -1; return 순번; }
    return -11;
}
int 통신읽기(int fail_pemegang, void *data, unsigned item_COUNT) {
    통신끝점 *rentetan_data = dapatkan_VALUE(fail_pemegang); if (!rentetan_data || rentetan_data->TYPE_bidang != 1) return -9;
    if (!item_COUNT) return 0; if (!rentetan_data->pemasukan_COUNT) return rentetan_data->RALAT ? rentetan_data->RALAT : rentetan_data->fail_tamat ? 0 : -11;
    if (item_COUNT > rentetan_data->pemasukan_COUNT) item_COUNT = rentetan_data->pemasukan_COUNT;
    for (unsigned 순번 = 0; 순번 < item_COUNT; 순번++) { ((unsigned char *)data)[순번] = rentetan_data->data[rentetan_data->hadapan_pemasukan]; rentetan_data->hadapan_pemasukan = (rentetan_data->hadapan_pemasukan + 1) % sizeof(rentetan_data->data); }
    rentetan_data->pemasukan_COUNT -= item_COUNT; if (rentetan_data->hubungan_kawalan) tcp_recved(rentetan_data->hubungan_kawalan, item_COUNT); return item_COUNT;
}
int 통신쓰기(int fail_pemegang, const void *data, unsigned item_COUNT) {
    통신끝점 *rentetan_data = dapatkan_VALUE(fail_pemegang); if (!rentetan_data || rentetan_data->TYPE_bidang != 1) return -9;
    if (rentetan_data->RALAT) return rentetan_data->RALAT; if (!rentetan_data->hubungan_kawalan || !rentetan_data->연결됨) return -107;
    if (!item_COUNT) return 0; if (item_COUNT > tcp_sndbuf(rentetan_data->hubungan_kawalan)) item_COUNT = tcp_sndbuf(rentetan_data->hubungan_kawalan);
    if (!item_COUNT) return -11; if (item_COUNT > 1024) item_COUNT = 1024;
    err_t 보조항목 = tcp_write(rentetan_data->hubungan_kawalan, data, item_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(rentetan_data->hubungan_kawalan); return item_COUNT;
}
int 전문보내기(int fail_pemegang, const void *data, unsigned item_COUNT, uint32_t e_mel, unsigned nombor_port) {
    통신끝점 *rentetan_data = dapatkan_VALUE(fail_pemegang); if (!rentetan_data || rentetan_data->TYPE_bidang != 2) return -9;
    if (item_COUNT > 512) return -90; if (!nombor_port || nombor_port > 65535) return -22;
    struct pbuf *data_jawatan = pbuf_alloc(PBUF_TRANSPORT, item_COUNT, PBUF_RAM); if (!data_jawatan) return -11;
    pbuf_take(data_jawatan, data, item_COUNT); ip_addr_t alamat_Internet; ip_addr_set_ip4_u32(&alamat_Internet, lwip_htonl(e_mel));
    err_t 보조항목 = udp_sendto(rentetan_data->전문제어, data_jawatan, &alamat_Internet, nombor_port); pbuf_free(data_jawatan); return 보조항목 ? 오류번호(보조항목) : (int)item_COUNT;
}
int 전문받기(int fail_pemegang, void *data, unsigned item_COUNT) {
    통신끝점 *rentetan_data = dapatkan_VALUE(fail_pemegang); if (!rentetan_data || rentetan_data->TYPE_bidang != 2) return -9;
    if (!rentetan_data->pemasukan_COUNT) return -11; unsigned 현재위치 = rentetan_data->hadapan_pemasukan;
    if (item_COUNT > rentetan_data->길이목록[현재위치]) item_COUNT = rentetan_data->길이목록[현재위치]; memcpy(data, rentetan_data->data + 현재위치 * 512, item_COUNT);
    rentetan_data->상대창구번호 = rentetan_data->접속번호들[현재위치]; rentetan_data->rakan_e_mel = rentetan_data->주소목록[현재위치]; rentetan_data->hadapan_pemasukan = (현재위치 + 1) % 4; rentetan_data->pemasukan_COUNT--; return item_COUNT;
}
unsigned rangkaian_nombor_port(int fail_pemegang) { 통신끝점 *rentetan_data = dapatkan_VALUE(fail_pemegang); return !rentetan_data ? 0 : rentetan_data->hubungan_kawalan ? rentetan_data->hubungan_kawalan->local_port : rentetan_data->전문제어 ? rentetan_data->전문제어->local_port : 0; }
unsigned rakan_nombor_port(int fail_pemegang) { 통신끝점 *rentetan_data = dapatkan_VALUE(fail_pemegang); return rentetan_data ? rentetan_data->상대창구번호 : 0; }
uint32_t 상대통신주소(int fail_pemegang) { 통신끝점 *rentetan_data = dapatkan_VALUE(fail_pemegang); return rentetan_data ? rentetan_data->rakan_e_mel : 0; }
void Tutup_rangkaian(int fail_pemegang) {
    통신끝점 *rentetan_data = dapatkan_VALUE(fail_pemegang); if (!rentetan_data) return;
    if (rentetan_data->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_bidang && 통신끝점들[순번].teknologi_maklumat_belum_selesai == fail_pemegang) Tutup_rangkaian(순번);
    if (rentetan_data->hubungan_kawalan) {
        tcp_arg(rentetan_data->hubungan_kawalan, 0); if (rentetan_data->수신창구) tcp_accept(rentetan_data->hubungan_kawalan, 0); else { tcp_recv(rentetan_data->hubungan_kawalan, 0); tcp_err(rentetan_data->hubungan_kawalan, 0); }
        if (tcp_close(rentetan_data->hubungan_kawalan) != ERR_OK) tcp_abort(rentetan_data->hubungan_kawalan);
    }
    if (rentetan_data->전문제어) udp_remove(rentetan_data->전문제어); rentetan_data->TYPE_bidang = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || undian) return; undian = 1;
    if(유선사용)유선망살피기(&hubungan_peranti);
    for (unsigned belanjawan_diperuntukkan = 0; !유선사용 && belanjawan_diperuntukkan < 4096 && (mesin_daftar(보조장치 + 0x54) & 1); belanjawan_diperuntukkan++) {
        unsigned titik_kod = mesin_daftar(보조장치 + 0x40) & 255;
        if (titik_kod == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *data_jawatan = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (data_jawatan) { 받은전문수++; RECEIVED_bait_COUNT += 수신사용량; pbuf_take(data_jawatan, 수신자료, 수신사용량); if (hubungan_peranti.input(data_jawatan, &hubungan_peranti) != ERR_OK) { 버린전문수++; pbuf_free(data_jawatan); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (titik_kod == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (titik_kod != 220 && titik_kod != 221) 수신오류 = 1; titik_kod = titik_kod == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = titik_kod; else 수신오류 = 1;
        }
    }
    netif_poll(&hubungan_peranti); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned belanjawan_diperuntukkan = 0; belanjawan_diperuntukkan < 4096 && 송신개수 && (mesin_daftar(보조장치 + 0x54) & 0x20); belanjawan_diperuntukkan++) {
        mesin_daftar(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    undian = 0;
}

/* Tetapan·조회는 lwIP의 sebenar_data 인터페이스와 tamat_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned pemasukan_VALUE, unsigned INDEX) {
    if(pemasukan_VALUE==20)return 유선사용;
    if(pemasukan_VALUE==21)return 준비됨&&netif_is_link_up(&hubungan_peranti);
    if(pemasukan_VALUE==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&pemasukan_VALUE>=4&&pemasukan_VALUE<=8)return 유선망집계(pemasukan_VALUE-4);
    if (pemasukan_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&hubungan_peranti)));
    if (pemasukan_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&hubungan_peranti)));
    if (pemasukan_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&hubungan_peranti)));
    if (pemasukan_VALUE == 3) return netif_is_up(&hubungan_peranti) != 0;
    if (pemasukan_VALUE == 4) return 받은전문수;
    if (pemasukan_VALUE == 5) return 보낸전문수;
    if (pemasukan_VALUE == 6) return RECEIVED_bait_COUNT;
    if (pemasukan_VALUE == 7) return 보낸바이트수;
    if (pemasukan_VALUE == 8) return 버린전문수;
    if (pemasukan_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *tamat_p = &통신끝점들[INDEX];
    if (pemasukan_VALUE == 10) return tamat_p->TYPE_bidang;
    if (!tamat_p->TYPE_bidang) return 0;
    if (pemasukan_VALUE == 11) return rangkaian_nombor_port(INDEX);
    if (pemasukan_VALUE == 12) return tamat_p->rakan_e_mel;
    if (pemasukan_VALUE == 13) return tamat_p->상대창구번호;
    if (pemasukan_VALUE == 14) return tamat_p->수신창구 ? 1 : tamat_p->fail_tamat ? 3 : tamat_p->RALAT ? 4 : tamat_p->연결됨 ? 2 : 0;
    if (pemasukan_VALUE == 15) return tamat_p->pemasukan_COUNT;
    if (pemasukan_VALUE == 16) {
        const ip_addr_t *e_mel = tamat_p->TYPE_bidang == 1 && tamat_p->hubungan_kawalan ? &tamat_p->hubungan_kawalan->local_ip :
            tamat_p->TYPE_bidang == 2 && tamat_p->전문제어 ? &tamat_p->전문제어->local_ip : 0;
        return e_mel ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(e_mel))) : 0;
    }
    return 0;
}

int konfigurasi_rangkaian(unsigned Aksi, uint32_t e_mel, uint32_t topeng_VALUE, uint32_t get_laluan_VALUE) {
    if (!준비됨) return -100;
    if (Aksi == 1) { netif_set_up(&hubungan_peranti); return 0; }
    if (Aksi == 2) { netif_set_down(&hubungan_peranti); return 0; }
    if (Aksi != 0) return -22;
    /* 유니캐스트 IPv4, 연속 topeng_VALUE, 같은 망의 선택적 nilai_lalai get_laluan_VALUE. */
    uint32_t 뒤집은가림 = ~topeng_VALUE;
    if (!topeng_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !e_mel || (e_mel >> 24) == 127 ||
        (e_mel >> 24) == 0 || (e_mel >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(e_mel & 뒤집은가림) || (e_mel & 뒤집은가림) == 뒤집은가림)) ||
        (get_laluan_VALUE && ((get_laluan_VALUE & topeng_VALUE) != (e_mel & topeng_VALUE) || get_laluan_VALUE == e_mel || (get_laluan_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(get_laluan_VALUE & 뒤집은가림) || (get_laluan_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 e_mel 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_bidang &&
        !(통신끝점들[INDEX].수신창구 && 통신끝점들[INDEX].hubungan_kawalan && ip_addr_isany(&통신끝점들[INDEX].hubungan_kawalan->local_ip))) return -16;
    if(유선사용)dhcp_stop(&hubungan_peranti);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(e_mel)); ip4_addr_set_u32(&새가림, lwip_htonl(topeng_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(get_laluan_VALUE));
    netif_set_addr(&hubungan_peranti, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *respons_peserta;
static uint32_t ujian_e_mel, ujian_TIME, respons_TIME;
static unsigned ujian_jujukan, 시험식별자, respons_jujukan;
static int respons_status;
static u8_t 응답받음(void *인수, struct raw_pcb *tamat_p, struct pbuf *data, const ip_addr_t *e_mel) {
    (void)인수; (void)tamat_p;
    unsigned char 머리[20], balas[16];
    if (respons_status != -11 || data->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(e_mel))) != ujian_e_mel || pbuf_copy_partial(data, 머리, 20, 0) != 20) return 0;
    unsigned Pengepala_saiz = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Pengepala_saiz < 20 || data->tot_len < Pengepala_saiz + 16 ||
        pbuf_copy_partial(data, balas, 16, Pengepala_saiz) != 16 || balas[0] || balas[1] ||
        (((unsigned)balas[4] << 8) | balas[5]) != 시험식별자 ||
        (((unsigned)balas[6] << 8) | balas[7]) != ujian_jujukan ||
        balas[8] != 'J' || balas[9] != 'K' || balas[10] != 'O' || balas[11] != 'S' ||
        (((uint32_t)balas[12] << 24) | ((uint32_t)balas[13] << 16) | ((uint32_t)balas[14] << 8) | balas[15]) != ujian_TIME) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(data, Pengepala_saiz)) return 0;
    if (inet_chksum_pbuf(data)) { pbuf_add_header(data, Pengepala_saiz); return 0; }
    respons_TIME = (uint32_t)보드밀리초() - ujian_TIME; respons_jujukan = 머리[8]; respons_status = 0;
    pbuf_free(data); return 1;
}
int Mula_respons_ujian(uint32_t e_mel, unsigned tertib_VALUE) {
    if (!준비됨 || !netif_is_up(&hubungan_peranti)) return -100;
    if (!e_mel || (e_mel >> 28) >= 14 || e_mel == 0xffffffffu) return -22;
    if (!respons_peserta) { respons_peserta = raw_new(IP_PROTO_ICMP); if (!respons_peserta) return -12; raw_recv(respons_peserta, 응답받음, 0); }
    ujian_e_mel = e_mel; ujian_jujukan = tertib_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    ujian_TIME = 보드밀리초(); respons_status = -11; respons_TIME = respons_jujukan = 0;
    unsigned char data[32] = {8,0,0,0};
    data[4] = 시험식별자 >> 8; data[5] = 시험식별자; data[6] = ujian_jujukan >> 8; data[7] = ujian_jujukan;
    data[8]='J'; data[9]='K'; data[10]='O'; data[11]='S';
    data[12]=ujian_TIME >> 24; data[13]=ujian_TIME >> 16; data[14]=ujian_TIME >> 8; data[15]=ujian_TIME;
    for (unsigned jawatan_INDEX = 16; jawatan_INDEX < sizeof(data); jawatan_INDEX++) data[jawatan_INDEX] = jawatan_INDEX;
    uint16_t pengesahan_hasil_tambah_semak = inet_chksum(data, sizeof(data)); memcpy(data + 2, &pengesahan_hasil_tambah_semak, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(data), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, data, sizeof(data)); ip_addr_t destinasi_peserta; ip_addr_set_ip4_u32(&destinasi_peserta, lwip_htonl(e_mel));
    err_t 처리값 = raw_sendto(respons_peserta, 전문, &destinasi_peserta); pbuf_free(전문);
    if (처리값) respons_status = 오류번호(처리값);
    return 처리값 ? respons_status : 0;
}
int 응답시험읽기(unsigned pemasukan_VALUE) {
    통신망살피기();
    return pemasukan_VALUE == 0 ? respons_status : pemasukan_VALUE == 1 ? (int)respons_TIME : pemasukan_VALUE == 2 ? (int)respons_jujukan : -22;
}
