#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "jaringan_tumpuk.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../jarak_jauh_VALUE/jarak_jauh_VALUE.h"
#include "terkabel_jaringan.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define mesin_daftar(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif koneksi_Ponsel;
static int 준비됨, 살피는중;
static int gunakan_terkabel_jaringan;
static unsigned 수신사용량, 수신탈출, terima_kesalahan;
static unsigned char Data_Penerimaan_buffer[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_byte_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_area, terima_port, teknologi_informasi_sedang_diproses, 연결됨, file_mengakhiri, galat;
    struct tcp_pcb *koneksi_kontrol;
    struct udp_pcb *전문제어;
    unsigned depan_entri, entri_COUNT;
    unsigned char data[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], serekan_surel;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int nomor_kesalahan(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *dapatkan_VALUE(int file_handel) { return file_handel >= 0 && file_handel < 32 && 통신끝점들[file_handel].TYPE_area ? &통신끝점들[file_handel] : 0; }
static int 예약하기(int TYPE_area) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_area) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_area = TYPE_area; 통신끝점들[순번].teknologi_informasi_sedang_diproses = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned kode_karakter) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = kode_karakter; }
static err_t 출력결과(struct netif *item_COUNT, struct pbuf *data_posisi, const ip4_addr_t *surel) {
    (void)item_COUNT; (void)surel;
    if (data_posisi->tot_len > 1500 || 송신개수 + 2 * data_posisi->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Berikutnya_OFFSET = data_posisi; Berikutnya_OFFSET; Berikutnya_OFFSET = Berikutnya_OFFSET->next) for (unsigned 순번 = 0; 순번 < Berikutnya_OFFSET->len; 순번++) {
        unsigned kode_karakter = ((unsigned char *)Berikutnya_OFFSET->payload)[순번];
        if (kode_karakter == 192 || kode_karakter == 219) { 내보내기(219); 내보내기(kode_karakter == 192 ? 220 : 221); } else 내보내기(kode_karakter);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += data_posisi->tot_len; return ERR_OK;
}
static err_t Siapkan_runtime_bahasa_umum(struct netif *item_COUNT) { item_COUNT->name[0] = 's'; item_COUNT->name[1] = 'l'; item_COUNT->mtu = 1500; item_COUNT->output = 출력결과; return ERR_OK; }
void Siapkan_jaringan(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    mesin_daftar(보조장치 + 4) |= 1; mesin_daftar(보조장치 + 0x60) = 0; mesin_daftar(보조장치 + 0x44) = 0;
    mesin_daftar(보조장치 + 0x48) = 0xc6; mesin_daftar(보조장치 + 0x4c) = 3; mesin_daftar(보조장치 + 0x68) = 270; mesin_daftar(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Alamat_internet, bitmask, gateway_surel;
    gunakan_terkabel_jaringan=유선장치있음();
    ip4_addr_set_u32(&Alamat_internet, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bitmask, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&gateway_surel, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&koneksi_Ponsel, &Alamat_internet, &bitmask, &gateway_surel, 0, gunakan_terkabel_jaringan?Siapkan_terkabel_jaringan:Siapkan_runtime_bahasa_umum, gunakan_terkabel_jaringan?ethernet_input:ip4_input))return;
    netif_set_default(&koneksi_Ponsel); netif_set_up(&koneksi_Ponsel);if(!gunakan_terkabel_jaringan)netif_set_link_up(&koneksi_Ponsel); 준비됨 = 1;
    Siapkan_jarak_jauh();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *transmisi_kontrol_blok, struct pbuf *data_posisi, err_t galat) {
    통신끝점 *string_data = 부가인수; (void)transmisi_kontrol_blok; (void)galat;
    if (!data_posisi) { string_data->file_mengakhiri = 1; return ERR_OK; }
    if (data_posisi->tot_len > sizeof(string_data->data) - string_data->entri_COUNT) return ERR_MEM;
    unsigned saat_ini_posisi = (string_data->depan_entri + string_data->entri_COUNT) % sizeof(string_data->data);
    for (struct pbuf *Berikutnya_OFFSET = data_posisi; Berikutnya_OFFSET; Berikutnya_OFFSET = Berikutnya_OFFSET->next) for (unsigned 순번 = 0; 순번 < Berikutnya_OFFSET->len; 순번++) {
        string_data->data[saat_ini_posisi] = ((unsigned char *)Berikutnya_OFFSET->payload)[순번]; saat_ini_posisi = (saat_ini_posisi + 1) % sizeof(string_data->data);
    }
    string_data->entri_COUNT += data_posisi->tot_len; pbuf_free(data_posisi); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t galat) { 통신끝점 *string_data = 부가인수; string_data->koneksi_kontrol = 0; string_data->galat = nomor_kesalahan(galat); }
static void 되부름목록(통신끝점 *string_data) { tcp_arg(string_data->koneksi_kontrol, string_data); tcp_recv(string_data->koneksi_kontrol, 수신됨); tcp_err(string_data->koneksi_kontrol, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *transmisi_kontrol_blok, err_t galat) {
    통신끝점 *string_data = 부가인수; (void)transmisi_kontrol_blok; if (galat) string_data->galat = nomor_kesalahan(galat); else string_data->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *transmisi_kontrol_blok, err_t galat) {
    통신끝점 *induk = 부가인수; if (galat) return galat;
    int file_handel = 예약하기(1); if (file_handel < 0) return ERR_MEM;
    통신끝점 *string_data = &통신끝점들[file_handel]; string_data->koneksi_kontrol = transmisi_kontrol_blok; string_data->연결됨 = 1; string_data->teknologi_informasi_sedang_diproses = (int)(induk - 통신끝점들);
    string_data->serekan_surel = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&transmisi_kontrol_blok->remote_ip))); string_data->상대창구번호 = transmisi_kontrol_blok->remote_port;
    되부름목록(string_data); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *transmisi_kontrol_blok, struct pbuf *data_posisi, const ip_addr_t *surel, u16_t nomor_port) {
    통신끝점 *string_data = 부가인수; (void)transmisi_kontrol_blok;
    if (string_data->entri_COUNT < 4 && data_posisi->tot_len <= 512) {
        unsigned posisi_INDEX = (string_data->depan_entri + string_data->entri_COUNT) % 4;
        pbuf_copy_partial(data_posisi, string_data->data + posisi_INDEX * 512, data_posisi->tot_len, 0);
        string_data->길이목록[posisi_INDEX] = data_posisi->tot_len; string_data->접속번호들[posisi_INDEX] = nomor_port;
        string_data->주소목록[posisi_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(surel))); string_data->entri_COUNT++;
    }
    pbuf_free(data_posisi);
}
int 통신끝점만들기(int TYPE_area) {
    if (!준비됨) return -100;
    if (TYPE_area != 1 && TYPE_area != 2) return -93;
    int file_handel = 예약하기(TYPE_area); if (file_handel < 0) return file_handel;
    통신끝점 *string_data = &통신끝점들[file_handel];
    if (TYPE_area == 1) { string_data->koneksi_kontrol = tcp_new(); if (string_data->koneksi_kontrol) 되부름목록(string_data); }
    else { string_data->전문제어 = udp_new(); if (string_data->전문제어) udp_recv(string_data->전문제어, 전문, string_data); }
    if (!string_data->koneksi_kontrol && !string_data->전문제어) { string_data->TYPE_area = 0; return -12; } return file_handel;
}
int 망주소묶기(int file_handel, uint32_t surel, unsigned nomor_port) {
    통신끝점 *string_data = dapatkan_VALUE(file_handel); if (!string_data) return -9;
    if (nomor_port > 65535 || (surel && surel != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&koneksi_Ponsel))) && surel != 0x7f000001)) return -99;
    ip_addr_t Alamat_internet; ip_addr_set_ip4_u32(&Alamat_internet, lwip_htonl(surel));
    err_t 보조항목 = string_data->TYPE_area == 1 ? tcp_bind(string_data->koneksi_kontrol, &Alamat_internet, nomor_port) : udp_bind(string_data->전문제어, &Alamat_internet, nomor_port); return 보조항목 ? nomor_kesalahan(보조항목) : 0;
}
void 통신주소재사용(int file_handel) { 통신끝점 *string_data = dapatkan_VALUE(file_handel); if (string_data && string_data->koneksi_kontrol) ip_set_option(string_data->koneksi_kontrol, SOF_REUSEADDR); }
int 연결기다리기(int file_handel) {
    통신끝점 *string_data = dapatkan_VALUE(file_handel); if (!string_data || string_data->TYPE_area != 1) return -9;
    if (string_data->terima_port) return 0;
    err_t 보조항목; struct tcp_pcb *transmisi_kontrol_blok = tcp_listen_with_backlog_and_err(string_data->koneksi_kontrol, 4, &보조항목);
    if (!transmisi_kontrol_blok) return nomor_kesalahan(보조항목); string_data->koneksi_kontrol = transmisi_kontrol_blok; string_data->terima_port = 1; tcp_arg(transmisi_kontrol_blok, string_data); tcp_accept(transmisi_kontrol_blok, 연결받음); return 0;
}
int 망연결하기(int file_handel, uint32_t surel, unsigned nomor_port) {
    통신끝점 *string_data = dapatkan_VALUE(file_handel); if (!string_data || string_data->TYPE_area != 1) return -9;
    if (string_data->galat) return string_data->galat;
    if (string_data->연결됨) return 0;
    if (string_data->상대창구번호) return -115;
    if (!nomor_port || nomor_port > 65535 || !surel) return -22;
    ip_addr_t Alamat_internet; ip_addr_set_ip4_u32(&Alamat_internet, lwip_htonl(surel));
    string_data->serekan_surel = surel; string_data->상대창구번호 = nomor_port;
    err_t 보조항목 = tcp_connect(string_data->koneksi_kontrol, &Alamat_internet, nomor_port, 연결됨); return 보조항목 ? nomor_kesalahan(보조항목) : -115;
}
int 망연결받기(int file_handel) {
    통신끝점 *string_data = dapatkan_VALUE(file_handel); if (!string_data || !string_data->terima_port) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_area == 1 && 통신끝점들[순번].teknologi_informasi_sedang_diproses == file_handel) { 통신끝점들[순번].teknologi_informasi_sedang_diproses = -1; return 순번; }
    return -11;
}
int 통신읽기(int file_handel, void *data, unsigned item_COUNT) {
    통신끝점 *string_data = dapatkan_VALUE(file_handel); if (!string_data || string_data->TYPE_area != 1) return -9;
    if (!item_COUNT) return 0; if (!string_data->entri_COUNT) return string_data->galat ? string_data->galat : string_data->file_mengakhiri ? 0 : -11;
    if (item_COUNT > string_data->entri_COUNT) item_COUNT = string_data->entri_COUNT;
    for (unsigned 순번 = 0; 순번 < item_COUNT; 순번++) { ((unsigned char *)data)[순번] = string_data->data[string_data->depan_entri]; string_data->depan_entri = (string_data->depan_entri + 1) % sizeof(string_data->data); }
    string_data->entri_COUNT -= item_COUNT; if (string_data->koneksi_kontrol) tcp_recved(string_data->koneksi_kontrol, item_COUNT); return item_COUNT;
}
int 통신쓰기(int file_handel, const void *data, unsigned item_COUNT) {
    통신끝점 *string_data = dapatkan_VALUE(file_handel); if (!string_data || string_data->TYPE_area != 1) return -9;
    if (string_data->galat) return string_data->galat; if (!string_data->koneksi_kontrol || !string_data->연결됨) return -107;
    if (!item_COUNT) return 0; if (item_COUNT > tcp_sndbuf(string_data->koneksi_kontrol)) item_COUNT = tcp_sndbuf(string_data->koneksi_kontrol);
    if (!item_COUNT) return -11; if (item_COUNT > 1024) item_COUNT = 1024;
    err_t 보조항목 = tcp_write(string_data->koneksi_kontrol, data, item_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return nomor_kesalahan(보조항목);
    tcp_output(string_data->koneksi_kontrol); return item_COUNT;
}
int 전문보내기(int file_handel, const void *data, unsigned item_COUNT, uint32_t surel, unsigned nomor_port) {
    통신끝점 *string_data = dapatkan_VALUE(file_handel); if (!string_data || string_data->TYPE_area != 2) return -9;
    if (item_COUNT > 512) return -90; if (!nomor_port || nomor_port > 65535) return -22;
    struct pbuf *data_posisi = pbuf_alloc(PBUF_TRANSPORT, item_COUNT, PBUF_RAM); if (!data_posisi) return -11;
    pbuf_take(data_posisi, data, item_COUNT); ip_addr_t Alamat_internet; ip_addr_set_ip4_u32(&Alamat_internet, lwip_htonl(surel));
    err_t 보조항목 = udp_sendto(string_data->전문제어, data_posisi, &Alamat_internet, nomor_port); pbuf_free(data_posisi); return 보조항목 ? nomor_kesalahan(보조항목) : (int)item_COUNT;
}
int 전문받기(int file_handel, void *data, unsigned item_COUNT) {
    통신끝점 *string_data = dapatkan_VALUE(file_handel); if (!string_data || string_data->TYPE_area != 2) return -9;
    if (!string_data->entri_COUNT) return -11; unsigned saat_ini_posisi = string_data->depan_entri;
    if (item_COUNT > string_data->길이목록[saat_ini_posisi]) item_COUNT = string_data->길이목록[saat_ini_posisi]; memcpy(data, string_data->data + saat_ini_posisi * 512, item_COUNT);
    string_data->상대창구번호 = string_data->접속번호들[saat_ini_posisi]; string_data->serekan_surel = string_data->주소목록[saat_ini_posisi]; string_data->depan_entri = (saat_ini_posisi + 1) % 4; string_data->entri_COUNT--; return item_COUNT;
}
unsigned jaringan_nomor_port(int file_handel) { 통신끝점 *string_data = dapatkan_VALUE(file_handel); return !string_data ? 0 : string_data->koneksi_kontrol ? string_data->koneksi_kontrol->local_port : string_data->전문제어 ? string_data->전문제어->local_port : 0; }
unsigned serekan_nomor_port(int file_handel) { 통신끝점 *string_data = dapatkan_VALUE(file_handel); return string_data ? string_data->상대창구번호 : 0; }
uint32_t 상대통신주소(int file_handel) { 통신끝점 *string_data = dapatkan_VALUE(file_handel); return string_data ? string_data->serekan_surel : 0; }
void Tutup_jaringan(int file_handel) {
    통신끝점 *string_data = dapatkan_VALUE(file_handel); if (!string_data) return;
    if (string_data->terima_port) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_area && 통신끝점들[순번].teknologi_informasi_sedang_diproses == file_handel) Tutup_jaringan(순번);
    if (string_data->koneksi_kontrol) {
        tcp_arg(string_data->koneksi_kontrol, 0); if (string_data->terima_port) tcp_accept(string_data->koneksi_kontrol, 0); else { tcp_recv(string_data->koneksi_kontrol, 0); tcp_err(string_data->koneksi_kontrol, 0); }
        if (tcp_close(string_data->koneksi_kontrol) != ERR_OK) tcp_abort(string_data->koneksi_kontrol);
    }
    if (string_data->전문제어) udp_remove(string_data->전문제어); string_data->TYPE_area = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(gunakan_terkabel_jaringan)유선망살피기(&koneksi_Ponsel);
    for (unsigned anggaran = 0; !gunakan_terkabel_jaringan && anggaran < 4096 && (mesin_daftar(보조장치 + 0x54) & 1); anggaran++) {
        unsigned kode_karakter = mesin_daftar(보조장치 + 0x40) & 255;
        if (kode_karakter == 192) {
            if (수신사용량 && !terima_kesalahan && !수신탈출) {
                struct pbuf *data_posisi = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (data_posisi) { 받은전문수++; RECEIVED_byte_COUNT += 수신사용량; pbuf_take(data_posisi, Data_Penerimaan_buffer, 수신사용량); if (koneksi_Ponsel.input(data_posisi, &koneksi_Ponsel) != ERR_OK) { 버린전문수++; pbuf_free(data_posisi); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = terima_kesalahan = 수신탈출 = 0;
        } else if (kode_karakter == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (kode_karakter != 220 && kode_karakter != 221) terima_kesalahan = 1; kode_karakter = kode_karakter == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(Data_Penerimaan_buffer)) Data_Penerimaan_buffer[수신사용량++] = kode_karakter; else terima_kesalahan = 1;
        }
    }
    netif_poll(&koneksi_Ponsel); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned anggaran = 0; anggaran < 4096 && 송신개수 && (mesin_daftar(보조장치 + 0x54) & 0x20); anggaran++) {
        mesin_daftar(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Konfigurasi·조회는 lwIP의 aktual_data 인터페이스와 mengakhiri_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned entri_VALUE, unsigned INDEX) {
    if(entri_VALUE==20)return gunakan_terkabel_jaringan;
    if(entri_VALUE==21)return 준비됨&&netif_is_link_up(&koneksi_Ponsel);
    if(entri_VALUE==22)return gunakan_terkabel_jaringan?유선망집계(5):0;
    if (!준비됨) return 0;
    if(gunakan_terkabel_jaringan&&entri_VALUE>=4&&entri_VALUE<=8)return 유선망집계(entri_VALUE-4);
    if (entri_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&koneksi_Ponsel)));
    if (entri_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&koneksi_Ponsel)));
    if (entri_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&koneksi_Ponsel)));
    if (entri_VALUE == 3) return netif_is_up(&koneksi_Ponsel) != 0;
    if (entri_VALUE == 4) return 받은전문수;
    if (entri_VALUE == 5) return 보낸전문수;
    if (entri_VALUE == 6) return RECEIVED_byte_COUNT;
    if (entri_VALUE == 7) return 보낸바이트수;
    if (entri_VALUE == 8) return 버린전문수;
    if (entri_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *mengakhiri_p = &통신끝점들[INDEX];
    if (entri_VALUE == 10) return mengakhiri_p->TYPE_area;
    if (!mengakhiri_p->TYPE_area) return 0;
    if (entri_VALUE == 11) return jaringan_nomor_port(INDEX);
    if (entri_VALUE == 12) return mengakhiri_p->serekan_surel;
    if (entri_VALUE == 13) return mengakhiri_p->상대창구번호;
    if (entri_VALUE == 14) return mengakhiri_p->terima_port ? 1 : mengakhiri_p->file_mengakhiri ? 3 : mengakhiri_p->galat ? 4 : mengakhiri_p->연결됨 ? 2 : 0;
    if (entri_VALUE == 15) return mengakhiri_p->entri_COUNT;
    if (entri_VALUE == 16) {
        const ip_addr_t *surel = mengakhiri_p->TYPE_area == 1 && mengakhiri_p->koneksi_kontrol ? &mengakhiri_p->koneksi_kontrol->local_ip :
            mengakhiri_p->TYPE_area == 2 && mengakhiri_p->전문제어 ? &mengakhiri_p->전문제어->local_ip : 0;
        return surel ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(surel))) : 0;
    }
    return 0;
}

int konfigurasikan_jaringan(unsigned Aksi, uint32_t surel, uint32_t masker_VALUE, uint32_t gateway_VALUE) {
    if (!준비됨) return -100;
    if (Aksi == 1) { netif_set_up(&koneksi_Ponsel); return 0; }
    if (Aksi == 2) { netif_set_down(&koneksi_Ponsel); return 0; }
    if (Aksi != 0) return -22;
    /* 유니캐스트 IPv4, 연속 masker_VALUE, 같은 망의 선택적 nilai_default gateway_VALUE. */
    uint32_t 뒤집은가림 = ~masker_VALUE;
    if (!masker_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !surel || (surel >> 24) == 127 ||
        (surel >> 24) == 0 || (surel >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(surel & 뒤집은가림) || (surel & 뒤집은가림) == 뒤집은가림)) ||
        (gateway_VALUE && ((gateway_VALUE & masker_VALUE) != (surel & masker_VALUE) || gateway_VALUE == surel || (gateway_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(gateway_VALUE & 뒤집은가림) || (gateway_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 surel 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_area &&
        !(통신끝점들[INDEX].terima_port && 통신끝점들[INDEX].koneksi_kontrol && ip_addr_isany(&통신끝점들[INDEX].koneksi_kontrol->local_ip))) return -16;
    if(gunakan_terkabel_jaringan)dhcp_stop(&koneksi_Ponsel);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(surel)); ip4_addr_set_u32(&새가림, lwip_htonl(masker_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(gateway_VALUE));
    netif_set_addr(&koneksi_Ponsel, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *respons_peserta;
static uint32_t 시험주소, 시험시각, respons_TIME;
static unsigned 시험순서, 시험식별자, respons_urutan;
static int respons_Status;
static u8_t 응답받음(void *argumen, struct raw_pcb *mengakhiri_p, struct pbuf *data, const ip_addr_t *surel) {
    (void)argumen; (void)mengakhiri_p;
    unsigned char kepala_VALUE[20], balas[16];
    if (respons_Status != -11 || data->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(surel))) != 시험주소 || pbuf_copy_partial(data, kepala_VALUE, 20, 0) != 20) return 0;
    unsigned judul_ukuran = (kepala_VALUE[0] & 15) * 4;
    if ((kepala_VALUE[0] >> 4) != 4 || judul_ukuran < 20 || data->tot_len < judul_ukuran + 16 ||
        pbuf_copy_partial(data, balas, 16, judul_ukuran) != 16 || balas[0] || balas[1] ||
        (((unsigned)balas[4] << 8) | balas[5]) != 시험식별자 ||
        (((unsigned)balas[6] << 8) | balas[7]) != 시험순서 ||
        balas[8] != 'J' || balas[9] != 'K' || balas[10] != 'O' || balas[11] != 'S' ||
        (((uint32_t)balas[12] << 24) | ((uint32_t)balas[13] << 16) | ((uint32_t)balas[14] << 8) | balas[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(data, judul_ukuran)) return 0;
    if (inet_chksum_pbuf(data)) { pbuf_add_header(data, judul_ukuran); return 0; }
    respons_TIME = (uint32_t)보드밀리초() - 시험시각; respons_urutan = kepala_VALUE[8]; respons_Status = 0;
    pbuf_free(data); return 1;
}
int 응답시험시작(uint32_t surel, unsigned urutan_VALUE) {
    if (!준비됨 || !netif_is_up(&koneksi_Ponsel)) return -100;
    if (!surel || (surel >> 28) >= 14 || surel == 0xffffffffu) return -22;
    if (!respons_peserta) { respons_peserta = raw_new(IP_PROTO_ICMP); if (!respons_peserta) return -12; raw_recv(respons_peserta, 응답받음, 0); }
    시험주소 = surel; 시험순서 = urutan_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); respons_Status = -11; respons_TIME = respons_urutan = 0;
    unsigned char data[32] = {8,0,0,0};
    data[4] = 시험식별자 >> 8; data[5] = 시험식별자; data[6] = 시험순서 >> 8; data[7] = 시험순서;
    data[8]='J'; data[9]='K'; data[10]='O'; data[11]='S';
    data[12]=시험시각 >> 24; data[13]=시험시각 >> 16; data[14]=시험시각 >> 8; data[15]=시험시각;
    for (unsigned posisi_INDEX = 16; posisi_INDEX < sizeof(data); posisi_INDEX++) data[posisi_INDEX] = posisi_INDEX;
    uint16_t verifikasi_checksum = inet_chksum(data, sizeof(data)); memcpy(data + 2, &verifikasi_checksum, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(data), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, data, sizeof(data)); ip_addr_t tujuan_peserta; ip_addr_set_ip4_u32(&tujuan_peserta, lwip_htonl(surel));
    err_t 처리값 = raw_sendto(respons_peserta, 전문, &tujuan_peserta); pbuf_free(전문);
    if (처리값) respons_Status = nomor_kesalahan(처리값);
    return 처리값 ? respons_Status : 0;
}
int 응답시험읽기(unsigned entri_VALUE) {
    통신망살피기();
    return entri_VALUE == 0 ? respons_Status : entri_VALUE == 1 ? (int)respons_TIME : entri_VALUE == 2 ? (int)respons_urutan : -22;
}
