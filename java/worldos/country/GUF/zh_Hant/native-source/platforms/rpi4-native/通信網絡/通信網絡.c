#include "../命名/計算機連接名稱列.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "通信網絡.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../遠程值/遠程值.h"
#include "有線網路.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define 計算機寄存器(首位值) (*(volatile uint32_t *)(uintptr_t)(首位值))
#define 輔助設備 0xfe215000ul
extern uintptr_t 板經過毫秒(void);
static struct netif 連接狀態設備;
static int 是否已準備, 輪詢;
static int 使用有線網路;
static unsigned 接收用量, 接收轉義, 接收錯誤;
static unsigned char 接收資料緩衝區[1600];
static unsigned char 傳輸資料[32768];
static unsigned 發送側頭, 發送側個數;
static uint32_t 已接收數據報個數, 已發送數據報個數, 已接收位元組個數, 已發送位元組個數, 已丟棄數數據報個數;
typedef struct {
    int 類型分類, 接收埠, 是否待處理, 已連接, 檔案結束, 錯誤;
    struct tcp_pcb *連接狀態控制;
    struct udp_pcb *數據報控制;
    unsigned 前端條目, 條目個數;
    unsigned char 資料[4096];
    unsigned 長度列[4], 埠列[4], 對端端點編號;
    uint32_t 地址列[4], 對端地址;
} 通信終點;
static 通信終點 通訊端端點列[32];
u32_t sys_now(void) { return (u32_t)板經過毫秒(); }
static int 錯誤編號(err_t 輔助條目) {
    return 輔助條目 == ERR_MEM || 輔助條目 == ERR_BUF || 輔助條目 == ERR_WOULDBLOCK ? -11 : 輔助條目 == ERR_USE ? -98 :
        輔助條目 == ERR_RTE ? -101 : 輔助條目 == ERR_RST ? -104 : 輔助條目 == ERR_CONN ? -107 : 輔助條目 == ERR_TIMEOUT ? -110 : -5;
}
static 通信終點 *獲取值(int 檔案句柄) { return 檔案句柄 >= 0 && 檔案句柄 < 32 && 通訊端端點列[檔案句柄].類型分類 ? &通訊端端點列[檔案句柄] : 0; }
static int 預留(int 類型分類) {
    for (int 序數索引 = 0; 序數索引 < 32; ++序數索引) if (!通訊端端點列[序數索引].類型分類) {
        memset(&通訊端端點列[序數索引], 0, sizeof(通信終點)); 通訊端端點列[序數索引].類型分類 = 類型分類; 通訊端端點列[序數索引].是否待處理 = -1; return 序數索引;
    }
    return -24;
}
static void 發射值(unsigned 字元程式碼) { 傳輸資料[(發送側頭 + 發送側個數++) % sizeof(傳輸資料)] = 字元程式碼; }
static err_t 輸出結果(struct netif *項目個數, struct pbuf *資料位置, const ip4_addr_t *地址) {
    (void)項目個數; (void)地址;
    if (資料位置->tot_len > 1500 || 發送側個數 + 2 * 資料位置->tot_len + 2 > sizeof(傳輸資料)) return ERR_MEM;
    發射值(192);
    for (struct pbuf *下一偏移 = 資料位置; 下一偏移; 下一偏移 = 下一偏移->next) for (unsigned 序數索引 = 0; 序數索引 < 下一偏移->len; 序數索引++) {
        unsigned 字元程式碼 = ((unsigned char *)下一偏移->payload)[序數索引];
        if (字元程式碼 == 192 || 字元程式碼 == 219) { 發射值(219); 發射值(字元程式碼 == 192 ? 220 : 221); } else 發射值(字元程式碼);
    }
    發射值(192); 已發送數據報個數++; 已發送位元組個數 += 資料位置->tot_len; return ERR_OK;
}
static err_t 準備運行時(struct netif *項目個數) { 項目個數->name[0] = 's'; 項目個數->name[1] = 'l'; 項目個數->mtu = 1500; 項目個數->output = 輸出結果; return ERR_OK; }
void 準備網路(void) {
    if (是否已準備) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    計算機寄存器(輔助設備 + 4) |= 1; 計算機寄存器(輔助設備 + 0x60) = 0; 計算機寄存器(輔助設備 + 0x44) = 0;
    計算機寄存器(輔助設備 + 0x48) = 0xc6; 計算機寄存器(輔助設備 + 0x4c) = 3; 計算機寄存器(輔助設備 + 0x68) = 270; 計算機寄存器(輔助設備 + 0x60) = 3;
    lwip_init();
    ip4_addr_t 互聯網地址, 位元掩碼, 網關地址;
    使用有線網路=擁有有線設備();
    ip4_addr_set_u32(&互聯網地址, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&位元掩碼, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&網關地址, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&連接狀態設備, &互聯網地址, &位元掩碼, &網關地址, 0, 使用有線網路?準備有線網路:準備運行時, 使用有線網路?ethernet_input:ip4_input))return;
    netif_set_default(&連接狀態設備); netif_set_up(&連接狀態設備);if(!使用有線網路)netif_set_link_up(&連接狀態設備); 是否已準備 = 1;
    準備遠程();
}
static err_t 擁有已接收(void *附加參數列, struct tcp_pcb *傳輸狀態控制塊, struct pbuf *資料位置, err_t 錯誤) {
    通信終點 *字符串資料 = 附加參數列; (void)傳輸狀態控制塊; (void)錯誤;
    if (!資料位置) { 字符串資料->檔案結束 = 1; return ERR_OK; }
    if (資料位置->tot_len > sizeof(字符串資料->資料) - 字符串資料->條目個數) return ERR_MEM;
    unsigned 當前位置 = (字符串資料->前端條目 + 字符串資料->條目個數) % sizeof(字符串資料->資料);
    for (struct pbuf *下一偏移 = 資料位置; 下一偏移; 下一偏移 = 下一偏移->next) for (unsigned 序數索引 = 0; 序數索引 < 下一偏移->len; 序數索引++) {
        字符串資料->資料[當前位置] = ((unsigned char *)下一偏移->payload)[序數索引]; 當前位置 = (當前位置 + 1) % sizeof(字符串資料->資料);
    }
    字符串資料->條目個數 += 資料位置->tot_len; pbuf_free(資料位置); return ERR_OK;
}
static void 擁有失敗(void *附加參數列, err_t 錯誤) { 通信終點 *字符串資料 = 附加參數列; 字符串資料->連接狀態控制 = 0; 字符串資料->錯誤 = 錯誤編號(錯誤); }
static void 回調列(通信終點 *字符串資料) { tcp_arg(字符串資料->連接狀態控制, 字符串資料); tcp_recv(字符串資料->連接狀態控制, 擁有已接收); tcp_err(字符串資料->連接狀態控制, 擁有失敗); }
static err_t 已連接(void *附加參數列, struct tcp_pcb *傳輸狀態控制塊, err_t 錯誤) {
    通信終點 *字符串資料 = 附加參數列; (void)傳輸狀態控制塊; if (錯誤) 字符串資料->錯誤 = 錯誤編號(錯誤); else 字符串資料->已連接 = 1; return ERR_OK;
}
static err_t 已接受(void *附加參數列, struct tcp_pcb *傳輸狀態控制塊, err_t 錯誤) {
    通信終點 *父 = 附加參數列; if (錯誤) return 錯誤;
    int 檔案句柄 = 預留(1); if (檔案句柄 < 0) return ERR_MEM;
    通信終點 *字符串資料 = &通訊端端點列[檔案句柄]; 字符串資料->連接狀態控制 = 傳輸狀態控制塊; 字符串資料->已連接 = 1; 字符串資料->是否待處理 = (int)(父 - 通訊端端點列);
    字符串資料->對端地址 = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&傳輸狀態控制塊->remote_ip))); 字符串資料->對端端點編號 = 傳輸狀態控制塊->remote_port;
    回調列(字符串資料); return ERR_OK;
}
static void 數據報(void *附加參數列, struct udp_pcb *傳輸狀態控制塊, struct pbuf *資料位置, const ip_addr_t *地址, u16_t 埠編號) {
    通信終點 *字符串資料 = 附加參數列; (void)傳輸狀態控制塊;
    if (字符串資料->條目個數 < 4 && 資料位置->tot_len <= 512) {
        unsigned 位置索引 = (字符串資料->前端條目 + 字符串資料->條目個數) % 4;
        pbuf_copy_partial(資料位置, 字符串資料->資料 + 位置索引 * 512, 資料位置->tot_len, 0);
        字符串資料->長度列[位置索引] = 資料位置->tot_len; 字符串資料->埠列[位置索引] = 埠編號;
        字符串資料->地址列[位置索引] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(地址))); 字符串資料->條目個數++;
    }
    pbuf_free(資料位置);
}
int 創建通訊端端點(int 類型分類) {
    if (!是否已準備) return -100;
    if (類型分類 != 1 && 類型分類 != 2) return -93;
    int 檔案句柄 = 預留(類型分類); if (檔案句柄 < 0) return 檔案句柄;
    通信終點 *字符串資料 = &通訊端端點列[檔案句柄];
    if (類型分類 == 1) { 字符串資料->連接狀態控制 = tcp_new(); if (字符串資料->連接狀態控制) 回調列(字符串資料); }
    else { 字符串資料->數據報控制 = udp_new(); if (字符串資料->數據報控制) udp_recv(字符串資料->數據報控制, 數據報, 字符串資料); }
    if (!字符串資料->連接狀態控制 && !字符串資料->數據報控制) { 字符串資料->類型分類 = 0; return -12; } return 檔案句柄;
}
int 網路層綁定(int 檔案句柄, uint32_t 地址, unsigned 埠編號) {
    通信終點 *字符串資料 = 獲取值(檔案句柄); if (!字符串資料) return -9;
    if (埠編號 > 65535 || (地址 && 地址 != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&連接狀態設備))) && 地址 != 0x7f000001)) return -99;
    ip_addr_t 互聯網地址; ip_addr_set_ip4_u32(&互聯網地址, lwip_htonl(地址));
    err_t 輔助條目 = 字符串資料->類型分類 == 1 ? tcp_bind(字符串資料->連接狀態控制, &互聯網地址, 埠編號) : udp_bind(字符串資料->數據報控制, &互聯網地址, 埠編號); return 輔助條目 ? 錯誤編號(輔助條目) : 0;
}
void 複用通訊端地址(int 檔案句柄) { 通信終點 *字符串資料 = 獲取值(檔案句柄); if (字符串資料 && 字符串資料->連接狀態控制) ip_set_option(字符串資料->連接狀態控制, SOF_REUSEADDR); }
int 網路層偵聽(int 檔案句柄) {
    通信終點 *字符串資料 = 獲取值(檔案句柄); if (!字符串資料 || 字符串資料->類型分類 != 1) return -9;
    if (字符串資料->接收埠) return 0;
    err_t 輔助條目; struct tcp_pcb *傳輸狀態控制塊 = tcp_listen_with_backlog_and_err(字符串資料->連接狀態控制, 4, &輔助條目);
    if (!傳輸狀態控制塊) return 錯誤編號(輔助條目); 字符串資料->連接狀態控制 = 傳輸狀態控制塊; 字符串資料->接收埠 = 1; tcp_arg(傳輸狀態控制塊, 字符串資料); tcp_accept(傳輸狀態控制塊, 已接受); return 0;
}
int 網路層連接(int 檔案句柄, uint32_t 地址, unsigned 埠編號) {
    通信終點 *字符串資料 = 獲取值(檔案句柄); if (!字符串資料 || 字符串資料->類型分類 != 1) return -9;
    if (字符串資料->錯誤) return 字符串資料->錯誤;
    if (字符串資料->已連接) return 0;
    if (字符串資料->對端端點編號) return -115;
    if (!埠編號 || 埠編號 > 65535 || !地址) return -22;
    ip_addr_t 互聯網地址; ip_addr_set_ip4_u32(&互聯網地址, lwip_htonl(地址));
    字符串資料->對端地址 = 地址; 字符串資料->對端端點編號 = 埠編號;
    err_t 輔助條目 = tcp_connect(字符串資料->連接狀態控制, &互聯網地址, 埠編號, 已連接); return 輔助條目 ? 錯誤編號(輔助條目) : -115;
}
int 網路層接受(int 檔案句柄) {
    通信終點 *字符串資料 = 獲取值(檔案句柄); if (!字符串資料 || !字符串資料->接收埠) return -22;
    for (int 序數索引 = 0; 序數索引 < 32; 序數索引++) if (通訊端端點列[序數索引].類型分類 == 1 && 通訊端端點列[序數索引].是否待處理 == 檔案句柄) { 通訊端端點列[序數索引].是否待處理 = -1; return 序數索引; }
    return -11;
}
int 網路層讀取(int 檔案句柄, void *資料, unsigned 項目個數) {
    通信終點 *字符串資料 = 獲取值(檔案句柄); if (!字符串資料 || 字符串資料->類型分類 != 1) return -9;
    if (!項目個數) return 0; if (!字符串資料->條目個數) return 字符串資料->錯誤 ? 字符串資料->錯誤 : 字符串資料->檔案結束 ? 0 : -11;
    if (項目個數 > 字符串資料->條目個數) 項目個數 = 字符串資料->條目個數;
    for (unsigned 序數索引 = 0; 序數索引 < 項目個數; 序數索引++) { ((unsigned char *)資料)[序數索引] = 字符串資料->資料[字符串資料->前端條目]; 字符串資料->前端條目 = (字符串資料->前端條目 + 1) % sizeof(字符串資料->資料); }
    字符串資料->條目個數 -= 項目個數; if (字符串資料->連接狀態控制) tcp_recved(字符串資料->連接狀態控制, 項目個數); return 項目個數;
}
int 網路層寫入(int 檔案句柄, const void *資料, unsigned 項目個數) {
    通信終點 *字符串資料 = 獲取值(檔案句柄); if (!字符串資料 || 字符串資料->類型分類 != 1) return -9;
    if (字符串資料->錯誤) return 字符串資料->錯誤; if (!字符串資料->連接狀態控制 || !字符串資料->已連接) return -107;
    if (!項目個數) return 0; if (項目個數 > tcp_sndbuf(字符串資料->連接狀態控制)) 項目個數 = tcp_sndbuf(字符串資料->連接狀態控制);
    if (!項目個數) return -11; if (項目個數 > 1024) 項目個數 = 1024;
    err_t 輔助條目 = tcp_write(字符串資料->連接狀態控制, 資料, 項目個數, TCP_WRITE_FLAG_COPY); if (輔助條目) return 錯誤編號(輔助條目);
    tcp_output(字符串資料->連接狀態控制); return 項目個數;
}
int 發送數據報(int 檔案句柄, const void *資料, unsigned 項目個數, uint32_t 地址, unsigned 埠編號) {
    通信終點 *字符串資料 = 獲取值(檔案句柄); if (!字符串資料 || 字符串資料->類型分類 != 2) return -9;
    if (項目個數 > 512) return -90; if (!埠編號 || 埠編號 > 65535) return -22;
    struct pbuf *資料位置 = pbuf_alloc(PBUF_TRANSPORT, 項目個數, PBUF_RAM); if (!資料位置) return -11;
    pbuf_take(資料位置, 資料, 項目個數); ip_addr_t 互聯網地址; ip_addr_set_ip4_u32(&互聯網地址, lwip_htonl(地址));
    err_t 輔助條目 = udp_sendto(字符串資料->數據報控制, 資料位置, &互聯網地址, 埠編號); pbuf_free(資料位置); return 輔助條目 ? 錯誤編號(輔助條目) : (int)項目個數;
}
int 接收數據報(int 檔案句柄, void *資料, unsigned 項目個數) {
    通信終點 *字符串資料 = 獲取值(檔案句柄); if (!字符串資料 || 字符串資料->類型分類 != 2) return -9;
    if (!字符串資料->條目個數) return -11; unsigned 當前位置 = 字符串資料->前端條目;
    if (項目個數 > 字符串資料->長度列[當前位置]) 項目個數 = 字符串資料->長度列[當前位置]; memcpy(資料, 字符串資料->資料 + 當前位置 * 512, 項目個數);
    字符串資料->對端端點編號 = 字符串資料->埠列[當前位置]; 字符串資料->對端地址 = 字符串資料->地址列[當前位置]; 字符串資料->前端條目 = (當前位置 + 1) % 4; 字符串資料->條目個數--; return 項目個數;
}
unsigned 網路埠編號(int 檔案句柄) { 通信終點 *字符串資料 = 獲取值(檔案句柄); return !字符串資料 ? 0 : 字符串資料->連接狀態控制 ? 字符串資料->連接狀態控制->local_port : 字符串資料->數據報控制 ? 字符串資料->數據報控制->local_port : 0; }
unsigned 對端埠編號(int 檔案句柄) { 通信終點 *字符串資料 = 獲取值(檔案句柄); return 字符串資料 ? 字符串資料->對端端點編號 : 0; }
uint32_t 網路層對端地址(int 檔案句柄) { 通信終點 *字符串資料 = 獲取值(檔案句柄); return 字符串資料 ? 字符串資料->對端地址 : 0; }
void 關閉網路(int 檔案句柄) {
    通信終點 *字符串資料 = 獲取值(檔案句柄); if (!字符串資料) return;
    if (字符串資料->接收埠) for (int 序數索引 = 0; 序數索引 < 32; ++序數索引) if (通訊端端點列[序數索引].類型分類 && 通訊端端點列[序數索引].是否待處理 == 檔案句柄) 關閉網路(序數索引);
    if (字符串資料->連接狀態控制) {
        tcp_arg(字符串資料->連接狀態控制, 0); if (字符串資料->接收埠) tcp_accept(字符串資料->連接狀態控制, 0); else { tcp_recv(字符串資料->連接狀態控制, 0); tcp_err(字符串資料->連接狀態控制, 0); }
        if (tcp_close(字符串資料->連接狀態控制) != ERR_OK) tcp_abort(字符串資料->連接狀態控制);
    }
    if (字符串資料->數據報控制) udp_remove(字符串資料->數據報控制); 字符串資料->類型分類 = 0;
}
void 審查網路(void) {
    if (!是否已準備 || 輪詢) return; 輪詢 = 1;
    if(使用有線網路)審查有線網路(&連接狀態設備);
    for (unsigned 預算 = 0; !使用有線網路 && 預算 < 4096 && (計算機寄存器(輔助設備 + 0x54) & 1); 預算++) {
        unsigned 字元程式碼 = 計算機寄存器(輔助設備 + 0x40) & 255;
        if (字元程式碼 == 192) {
            if (接收用量 && !接收錯誤 && !接收轉義) {
                struct pbuf *資料位置 = pbuf_alloc(PBUF_RAW, 接收用量, PBUF_POOL);
                if (資料位置) { 已接收數據報個數++; 已接收位元組個數 += 接收用量; pbuf_take(資料位置, 接收資料緩衝區, 接收用量); if (連接狀態設備.input(資料位置, &連接狀態設備) != ERR_OK) { 已丟棄數數據報個數++; pbuf_free(資料位置); } }
                else 已丟棄數數據報個數++;
            }
            else if (接收用量) 已丟棄數數據報個數++;
            接收用量 = 接收錯誤 = 接收轉義 = 0;
        } else if (字元程式碼 == 219 && !接收轉義) 接收轉義 = 1;
        else {
            if (接收轉義) { if (字元程式碼 != 220 && 字元程式碼 != 221) 接收錯誤 = 1; 字元程式碼 = 字元程式碼 == 220 ? 192 : 219; 接收轉義 = 0; }
            if (接收用量 < sizeof(接收資料緩衝區)) 接收資料緩衝區[接收用量++] = 字元程式碼; else 接收錯誤 = 1;
        }
    }
    netif_poll(&連接狀態設備); sys_check_timeouts(); 審查檔案傳送(); 審查遠程();
    for (unsigned 預算 = 0; 預算 < 4096 && 發送側個數 && (計算機寄存器(輔助設備 + 0x54) & 0x20); 預算++) {
        計算機寄存器(輔助設備 + 0x40) = 傳輸資料[發送側頭]; 發送側頭 = (發送側頭 + 1) % sizeof(傳輸資料); 發送側個數--;
    }
    輪詢 = 0;
}

/* 設置·조회는 lwIP의 實際資料 인터페이스와 結束分 표를 사용한다. */
uint32_t 讀取網路運行狀態(unsigned 條目值, unsigned 編號) {
    if(條目值==20)return 使用有線網路;
    if(條目值==21)return 是否已準備&&netif_is_link_up(&連接狀態設備);
    if(條目值==22)return 使用有線網路?有線網路統計(5):0;
    if (!是否已準備) return 0;
    if(使用有線網路&&條目值>=4&&條目值<=8)return 有線網路統計(條目值-4);
    if (條目值 == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&連接狀態設備)));
    if (條目值 == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&連接狀態設備)));
    if (條目值 == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&連接狀態設備)));
    if (條目值 == 3) return netif_is_up(&連接狀態設備) != 0;
    if (條目值 == 4) return 已接收數據報個數;
    if (條目值 == 5) return 已發送數據報個數;
    if (條目值 == 6) return 已接收位元組個數;
    if (條目值 == 7) return 已發送位元組個數;
    if (條目值 == 8) return 已丟棄數數據報個數;
    if (條目值 == 9) return 發送側個數;
    if (編號 >= 32) return 0;
    通信終點 *結束分 = &通訊端端點列[編號];
    if (條目值 == 10) return 結束分->類型分類;
    if (!結束分->類型分類) return 0;
    if (條目值 == 11) return 網路埠編號(編號);
    if (條目值 == 12) return 結束分->對端地址;
    if (條目值 == 13) return 結束分->對端端點編號;
    if (條目值 == 14) return 結束分->接收埠 ? 1 : 結束分->檔案結束 ? 3 : 結束分->錯誤 ? 4 : 結束分->已連接 ? 2 : 0;
    if (條目值 == 15) return 結束分->條目個數;
    if (條目值 == 16) {
        const ip_addr_t *地址 = 結束分->類型分類 == 1 && 結束分->連接狀態控制 ? &結束分->連接狀態控制->local_ip :
            結束分->類型分類 == 2 && 結束分->數據報控制 ? &結束分->數據報控制->local_ip : 0;
        return 地址 ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(地址))) : 0;
    }
    return 0;
}

int 設定配置網路(unsigned 動作, uint32_t 地址, uint32_t 掩碼值, uint32_t 網關值) {
    if (!是否已準備) return -100;
    if (動作 == 1) { netif_set_up(&連接狀態設備); return 0; }
    if (動作 == 2) { netif_set_down(&連接狀態設備); return 0; }
    if (動作 != 0) return -22;
    /* 유니캐스트 IPv4, 稠密切換分支項集 掩碼值, 같은 망의 선택적 默認值 網關值. */
    uint32_t 已反轉掩碼 = ~掩碼值;
    if (!掩碼值 || (已反轉掩碼 & (已反轉掩碼 + 1)) || !地址 || (地址 >> 24) == 127 ||
        (地址 >> 24) == 0 || (地址 >> 28) >= 14 ||
        (已反轉掩碼 > 1 && (!(地址 & 已反轉掩碼) || (地址 & 已反轉掩碼) == 已反轉掩碼)) ||
        (網關值 && ((網關值 & 掩碼值) != (地址 & 掩碼值) || 網關值 == 地址 || (網關值 >> 28) >= 14 ||
         (已反轉掩碼 > 1 && (!(網關值 & 已反轉掩碼) || (網關值 & 已反轉掩碼) == 已反轉掩碼))))) return -22;
    /* 기존 연결을 地址 변경으로 몰래 끊지 않는다. */
    for (unsigned 編號 = 0; 編號 < 32; 編號++) if (通訊端端點列[編號].類型分類 &&
        !(通訊端端點列[編號].接收埠 && 通訊端端點列[編號].連接狀態控制 && ip_addr_isany(&通訊端端點列[編號].連接狀態控制->local_ip))) return -16;
    if(使用有線網路)dhcp_stop(&連接狀態設備);
    ip4_addr_t 新建地址, 新建掩碼, 新建網關值;
    ip4_addr_set_u32(&新建地址, lwip_htonl(地址)); ip4_addr_set_u32(&新建掩碼, lwip_htonl(掩碼值)); ip4_addr_set_u32(&新建網關值, lwip_htonl(網關值));
    netif_set_addr(&連接狀態設備, &新建地址, &新建掩碼, &新建網關值);
    return 0;
}

static struct raw_pcb *響應端點;
static uint32_t 測試地址, 測試時間, 響應時間;
static unsigned 測試序列, 測試標識符, 響應序列;
static int 響應狀態;
static u8_t 擁有響應(void *實參, struct raw_pcb *結束分, struct pbuf *資料, const ip_addr_t *地址) {
    (void)實參; (void)結束分;
    unsigned char 頭值[20], 回覆[16];
    if (響應狀態 != -11 || 資料->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(地址))) != 測試地址 || pbuf_copy_partial(資料, 頭值, 20, 0) != 20) return 0;
    unsigned 標頭大小 = (頭值[0] & 15) * 4;
    if ((頭值[0] >> 4) != 4 || 標頭大小 < 20 || 資料->tot_len < 標頭大小 + 16 ||
        pbuf_copy_partial(資料, 回覆, 16, 標頭大小) != 16 || 回覆[0] || 回覆[1] ||
        (((unsigned)回覆[4] << 8) | 回覆[5]) != 測試標識符 ||
        (((unsigned)回覆[6] << 8) | 回覆[7]) != 測試序列 ||
        回覆[8] != 'J' || 回覆[9] != 'K' || 回覆[10] != 'O' || 回覆[11] != 'S' ||
        (((uint32_t)回覆[12] << 24) | ((uint32_t)回覆[13] << 16) | ((uint32_t)回覆[14] << 8) | 回覆[15]) != 測試時間) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(資料, 標頭大小)) return 0;
    if (inet_chksum_pbuf(資料)) { pbuf_add_header(資料, 標頭大小); return 0; }
    響應時間 = (uint32_t)板經過毫秒() - 測試時間; 響應序列 = 頭值[8]; 響應狀態 = 0;
    pbuf_free(資料); return 1;
}
int 開始響應測試(uint32_t 地址, unsigned 排序值) {
    if (!是否已準備 || !netif_is_up(&連接狀態設備)) return -100;
    if (!地址 || (地址 >> 28) >= 14 || 地址 == 0xffffffffu) return -22;
    if (!響應端點) { 響應端點 = raw_new(IP_PROTO_ICMP); if (!響應端點) return -12; raw_recv(響應端點, 擁有響應, 0); }
    測試地址 = 地址; 測試序列 = 排序值 & 65535; 測試標識符 = (測試標識符 + 1) & 65535;
    測試時間 = 板經過毫秒(); 響應狀態 = -11; 響應時間 = 響應序列 = 0;
    unsigned char 資料[32] = {8,0,0,0};
    資料[4] = 測試標識符 >> 8; 資料[5] = 測試標識符; 資料[6] = 測試序列 >> 8; 資料[7] = 測試序列;
    資料[8]='J'; 資料[9]='K'; 資料[10]='O'; 資料[11]='S';
    資料[12]=測試時間 >> 24; 資料[13]=測試時間 >> 16; 資料[14]=測試時間 >> 8; 資料[15]=測試時間;
    for (unsigned 位置索引 = 16; 位置索引 < sizeof(資料); 位置索引++) 資料[位置索引] = 位置索引;
    uint16_t 驗證校驗和 = inet_chksum(資料, sizeof(資料)); memcpy(資料 + 2, &驗證校驗和, 2);
    struct pbuf *數據報 = pbuf_alloc(PBUF_IP, sizeof(資料), PBUF_RAM); if (!數據報) return -12;
    pbuf_take(數據報, 資料, sizeof(資料)); ip_addr_t 目的地址端點; ip_addr_set_ip4_u32(&目的地址端點, lwip_htonl(地址));
    err_t 已處理值 = raw_sendto(響應端點, 數據報, &目的地址端點); pbuf_free(數據報);
    if (已處理值) 響應狀態 = 錯誤編號(已處理值);
    return 已處理值 ? 響應狀態 : 0;
}
int 讀取響應測試(unsigned 條目值) {
    審查網路();
    return 條目值 == 0 ? 響應狀態 : 條目值 == 1 ? (int)響應時間 : 條目值 == 2 ? (int)響應序列 : -22;
}
