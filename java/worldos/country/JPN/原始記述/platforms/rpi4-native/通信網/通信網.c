#include "../命名/機械連結名前一覧.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "通信網.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../遠隔値/遠隔値.h"
#include "結線済み通信網.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define 機械レジスタ(先頭位置値) (*(volatile uint32_t *)(uintptr_t)(先頭位置値))
#define 補助装置 0xfe215000ul
extern uintptr_t 基板経過ミリ秒(void);
static struct netif 接続状態装置;
static int 判定用意済み, 周期監視;
static int 使用結線済み通信網;
static unsigned 使用量受取, エスケープ受取, エラー受取;
static unsigned char データ緩衝域受取[1600];
static unsigned char 伝送データ[32768];
static unsigned 送信側先頭部, 送信側個数;
static uint32_t 受信済みデータグラム個数, 送信済みデータグラム個数, 受信済みバイト個数, 送信済みバイト個数, 破棄件数データグラム個数;
typedef struct {
    int 型分類, ポート受取, 判定未処理, 接続済み, ファイル終端位置, エラー;
    struct tcp_pcb *接続状態制御;
    struct udp_pcb *データグラム制御;
    unsigned 前面入口, 入口個数;
    unsigned char データ[4096];
    unsigned 長さ一覧[4], ポート一覧[4], 通信相手通信端点番号;
    uint32_t 番地一覧[4], 通信相手番地;
} 通信終点;
static 通信終点 ソケット端点一覧[32];
u32_t sys_now(void) { return (u32_t)基板経過ミリ秒(); }
static int エラー番号(err_t 補助入口) {
    return 補助入口 == ERR_MEM || 補助入口 == ERR_BUF || 補助入口 == ERR_WOULDBLOCK ? -11 : 補助入口 == ERR_USE ? -98 :
        補助入口 == ERR_RTE ? -101 : 補助入口 == ERR_RST ? -104 : 補助入口 == ERR_CONN ? -107 : 補助入口 == ERR_TIMEOUT ? -110 : -5;
}
static 通信終点 *値取得(int ファイル取扱い) { return ファイル取扱い >= 0 && ファイル取扱い < 32 && ソケット端点一覧[ファイル取扱い].型分類 ? &ソケット端点一覧[ファイル取扱い] : 0; }
static int 予約(int 型分類) {
    for (int 序数添字 = 0; 序数添字 < 32; ++序数添字) if (!ソケット端点一覧[序数添字].型分類) {
        memset(&ソケット端点一覧[序数添字], 0, sizeof(通信終点)); ソケット端点一覧[序数添字].型分類 = 型分類; ソケット端点一覧[序数添字].判定未処理 = -1; return 序数添字;
    }
    return -24;
}
static void 値出力(unsigned 文字コード) { 伝送データ[(送信側先頭部 + 送信側個数++) % sizeof(伝送データ)] = 文字コード; }
static err_t 出力結果(struct netif *項目個数, struct pbuf *データ位置, const ip4_addr_t *番地) {
    (void)項目個数; (void)番地;
    if (データ位置->tot_len > 1500 || 送信側個数 + 2 * データ位置->tot_len + 2 > sizeof(伝送データ)) return ERR_MEM;
    値出力(192);
    for (struct pbuf *次回変位量 = データ位置; 次回変位量; 次回変位量 = 次回変位量->next) for (unsigned 序数添字 = 0; 序数添字 < 次回変位量->len; 序数添字++) {
        unsigned 文字コード = ((unsigned char *)次回変位量->payload)[序数添字];
        if (文字コード == 192 || 文字コード == 219) { 値出力(219); 値出力(文字コード == 192 ? 220 : 221); } else 値出力(文字コード);
    }
    値出力(192); 送信済みデータグラム個数++; 送信済みバイト個数 += データ位置->tot_len; return ERR_OK;
}
static err_t 実行環境用意(struct netif *項目個数) { 項目個数->name[0] = 's'; 項目個数->name[1] = 'l'; 項目個数->mtu = 1500; 項目個数->output = 出力結果; return ERR_OK; }
void 通信網用意(void) {
    if (判定用意済み) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    機械レジスタ(補助装置 + 4) |= 1; 機械レジスタ(補助装置 + 0x60) = 0; 機械レジスタ(補助装置 + 0x44) = 0;
    機械レジスタ(補助装置 + 0x48) = 0xc6; 機械レジスタ(補助装置 + 0x4c) = 3; 機械レジスタ(補助装置 + 0x68) = 270; 機械レジスタ(補助装置 + 0x60) = 3;
    lwip_init();
    ip4_addr_t インターネット番地, ビットマスク, 中継門番地;
    使用結線済み通信網=保有結線済み装置();
    ip4_addr_set_u32(&インターネット番地, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&ビットマスク, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&中継門番地, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&接続状態装置, &インターネット番地, &ビットマスク, &中継門番地, 0, 使用結線済み通信網?結線済み通信網用意:実行環境用意, 使用結線済み通信網?ethernet_input:ip4_input))return;
    netif_set_default(&接続状態装置); netif_set_up(&接続状態装置);if(!使用結線済み通信網)netif_set_link_up(&接続状態装置); 判定用意済み = 1;
    遠隔用意();
}
static err_t 保有受信済み(void *追加分引数列, struct tcp_pcb *伝送状態制御ブロック, struct pbuf *データ位置, err_t エラー) {
    通信終点 *文字列データ = 追加分引数列; (void)伝送状態制御ブロック; (void)エラー;
    if (!データ位置) { 文字列データ->ファイル終端位置 = 1; return ERR_OK; }
    if (データ位置->tot_len > sizeof(文字列データ->データ) - 文字列データ->入口個数) return ERR_MEM;
    unsigned 現在位置 = (文字列データ->前面入口 + 文字列データ->入口個数) % sizeof(文字列データ->データ);
    for (struct pbuf *次回変位量 = データ位置; 次回変位量; 次回変位量 = 次回変位量->next) for (unsigned 序数添字 = 0; 序数添字 < 次回変位量->len; 序数添字++) {
        文字列データ->データ[現在位置] = ((unsigned char *)次回変位量->payload)[序数添字]; 現在位置 = (現在位置 + 1) % sizeof(文字列データ->データ);
    }
    文字列データ->入口個数 += データ位置->tot_len; pbuf_free(データ位置); return ERR_OK;
}
static void 保有失敗済み(void *追加分引数列, err_t エラー) { 通信終点 *文字列データ = 追加分引数列; 文字列データ->接続状態制御 = 0; 文字列データ->エラー = エラー番号(エラー); }
static void 折返し処理一覧(通信終点 *文字列データ) { tcp_arg(文字列データ->接続状態制御, 文字列データ); tcp_recv(文字列データ->接続状態制御, 保有受信済み); tcp_err(文字列データ->接続状態制御, 保有失敗済み); }
static err_t 接続済み(void *追加分引数列, struct tcp_pcb *伝送状態制御ブロック, err_t エラー) {
    通信終点 *文字列データ = 追加分引数列; (void)伝送状態制御ブロック; if (エラー) 文字列データ->エラー = エラー番号(エラー); else 文字列データ->接続済み = 1; return ERR_OK;
}
static err_t 受理済み(void *追加分引数列, struct tcp_pcb *伝送状態制御ブロック, err_t エラー) {
    通信終点 *親 = 追加分引数列; if (エラー) return エラー;
    int ファイル取扱い = 予約(1); if (ファイル取扱い < 0) return ERR_MEM;
    通信終点 *文字列データ = &ソケット端点一覧[ファイル取扱い]; 文字列データ->接続状態制御 = 伝送状態制御ブロック; 文字列データ->接続済み = 1; 文字列データ->判定未処理 = (int)(親 - ソケット端点一覧);
    文字列データ->通信相手番地 = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&伝送状態制御ブロック->remote_ip))); 文字列データ->通信相手通信端点番号 = 伝送状態制御ブロック->remote_port;
    折返し処理一覧(文字列データ); return ERR_OK;
}
static void データグラム(void *追加分引数列, struct udp_pcb *伝送状態制御ブロック, struct pbuf *データ位置, const ip_addr_t *番地, u16_t ポート番号) {
    通信終点 *文字列データ = 追加分引数列; (void)伝送状態制御ブロック;
    if (文字列データ->入口個数 < 4 && データ位置->tot_len <= 512) {
        unsigned 位置添字 = (文字列データ->前面入口 + 文字列データ->入口個数) % 4;
        pbuf_copy_partial(データ位置, 文字列データ->データ + 位置添字 * 512, データ位置->tot_len, 0);
        文字列データ->長さ一覧[位置添字] = データ位置->tot_len; 文字列データ->ポート一覧[位置添字] = ポート番号;
        文字列データ->番地一覧[位置添字] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(番地))); 文字列データ->入口個数++;
    }
    pbuf_free(データ位置);
}
int ソケット通信端点作成(int 型分類) {
    if (!判定用意済み) return -100;
    if (型分類 != 1 && 型分類 != 2) return -93;
    int ファイル取扱い = 予約(型分類); if (ファイル取扱い < 0) return ファイル取扱い;
    通信終点 *文字列データ = &ソケット端点一覧[ファイル取扱い];
    if (型分類 == 1) { 文字列データ->接続状態制御 = tcp_new(); if (文字列データ->接続状態制御) 折返し処理一覧(文字列データ); }
    else { 文字列データ->データグラム制御 = udp_new(); if (文字列データ->データグラム制御) udp_recv(文字列データ->データグラム制御, データグラム, 文字列データ); }
    if (!文字列データ->接続状態制御 && !文字列データ->データグラム制御) { 文字列データ->型分類 = 0; return -12; } return ファイル取扱い;
}
int 網結合(int ファイル取扱い, uint32_t 番地, unsigned ポート番号) {
    通信終点 *文字列データ = 値取得(ファイル取扱い); if (!文字列データ) return -9;
    if (ポート番号 > 65535 || (番地 && 番地 != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&接続状態装置))) && 番地 != 0x7f000001)) return -99;
    ip_addr_t インターネット番地; ip_addr_set_ip4_u32(&インターネット番地, lwip_htonl(番地));
    err_t 補助入口 = 文字列データ->型分類 == 1 ? tcp_bind(文字列データ->接続状態制御, &インターネット番地, ポート番号) : udp_bind(文字列データ->データグラム制御, &インターネット番地, ポート番号); return 補助入口 ? エラー番号(補助入口) : 0;
}
void 再利用ソケット番地(int ファイル取扱い) { 通信終点 *文字列データ = 値取得(ファイル取扱い); if (文字列データ && 文字列データ->接続状態制御) ip_set_option(文字列データ->接続状態制御, SOF_REUSEADDR); }
int 網接続待機(int ファイル取扱い) {
    通信終点 *文字列データ = 値取得(ファイル取扱い); if (!文字列データ || 文字列データ->型分類 != 1) return -9;
    if (文字列データ->ポート受取) return 0;
    err_t 補助入口; struct tcp_pcb *伝送状態制御ブロック = tcp_listen_with_backlog_and_err(文字列データ->接続状態制御, 4, &補助入口);
    if (!伝送状態制御ブロック) return エラー番号(補助入口); 文字列データ->接続状態制御 = 伝送状態制御ブロック; 文字列データ->ポート受取 = 1; tcp_arg(伝送状態制御ブロック, 文字列データ); tcp_accept(伝送状態制御ブロック, 受理済み); return 0;
}
int 網接続(int ファイル取扱い, uint32_t 番地, unsigned ポート番号) {
    通信終点 *文字列データ = 値取得(ファイル取扱い); if (!文字列データ || 文字列データ->型分類 != 1) return -9;
    if (文字列データ->エラー) return 文字列データ->エラー;
    if (文字列データ->接続済み) return 0;
    if (文字列データ->通信相手通信端点番号) return -115;
    if (!ポート番号 || ポート番号 > 65535 || !番地) return -22;
    ip_addr_t インターネット番地; ip_addr_set_ip4_u32(&インターネット番地, lwip_htonl(番地));
    文字列データ->通信相手番地 = 番地; 文字列データ->通信相手通信端点番号 = ポート番号;
    err_t 補助入口 = tcp_connect(文字列データ->接続状態制御, &インターネット番地, ポート番号, 接続済み); return 補助入口 ? エラー番号(補助入口) : -115;
}
int 網受理(int ファイル取扱い) {
    通信終点 *文字列データ = 値取得(ファイル取扱い); if (!文字列データ || !文字列データ->ポート受取) return -22;
    for (int 序数添字 = 0; 序数添字 < 32; 序数添字++) if (ソケット端点一覧[序数添字].型分類 == 1 && ソケット端点一覧[序数添字].判定未処理 == ファイル取扱い) { ソケット端点一覧[序数添字].判定未処理 = -1; return 序数添字; }
    return -11;
}
int 網読取(int ファイル取扱い, void *データ, unsigned 項目個数) {
    通信終点 *文字列データ = 値取得(ファイル取扱い); if (!文字列データ || 文字列データ->型分類 != 1) return -9;
    if (!項目個数) return 0; if (!文字列データ->入口個数) return 文字列データ->エラー ? 文字列データ->エラー : 文字列データ->ファイル終端位置 ? 0 : -11;
    if (項目個数 > 文字列データ->入口個数) 項目個数 = 文字列データ->入口個数;
    for (unsigned 序数添字 = 0; 序数添字 < 項目個数; 序数添字++) { ((unsigned char *)データ)[序数添字] = 文字列データ->データ[文字列データ->前面入口]; 文字列データ->前面入口 = (文字列データ->前面入口 + 1) % sizeof(文字列データ->データ); }
    文字列データ->入口個数 -= 項目個数; if (文字列データ->接続状態制御) tcp_recved(文字列データ->接続状態制御, 項目個数); return 項目個数;
}
int 網書込(int ファイル取扱い, const void *データ, unsigned 項目個数) {
    通信終点 *文字列データ = 値取得(ファイル取扱い); if (!文字列データ || 文字列データ->型分類 != 1) return -9;
    if (文字列データ->エラー) return 文字列データ->エラー; if (!文字列データ->接続状態制御 || !文字列データ->接続済み) return -107;
    if (!項目個数) return 0; if (項目個数 > tcp_sndbuf(文字列データ->接続状態制御)) 項目個数 = tcp_sndbuf(文字列データ->接続状態制御);
    if (!項目個数) return -11; if (項目個数 > 1024) 項目個数 = 1024;
    err_t 補助入口 = tcp_write(文字列データ->接続状態制御, データ, 項目個数, TCP_WRITE_FLAG_COPY); if (補助入口) return エラー番号(補助入口);
    tcp_output(文字列データ->接続状態制御); return 項目個数;
}
int データグラム送信(int ファイル取扱い, const void *データ, unsigned 項目個数, uint32_t 番地, unsigned ポート番号) {
    通信終点 *文字列データ = 値取得(ファイル取扱い); if (!文字列データ || 文字列データ->型分類 != 2) return -9;
    if (項目個数 > 512) return -90; if (!ポート番号 || ポート番号 > 65535) return -22;
    struct pbuf *データ位置 = pbuf_alloc(PBUF_TRANSPORT, 項目個数, PBUF_RAM); if (!データ位置) return -11;
    pbuf_take(データ位置, データ, 項目個数); ip_addr_t インターネット番地; ip_addr_set_ip4_u32(&インターネット番地, lwip_htonl(番地));
    err_t 補助入口 = udp_sendto(文字列データ->データグラム制御, データ位置, &インターネット番地, ポート番号); pbuf_free(データ位置); return 補助入口 ? エラー番号(補助入口) : (int)項目個数;
}
int データグラム受取(int ファイル取扱い, void *データ, unsigned 項目個数) {
    通信終点 *文字列データ = 値取得(ファイル取扱い); if (!文字列データ || 文字列データ->型分類 != 2) return -9;
    if (!文字列データ->入口個数) return -11; unsigned 現在位置 = 文字列データ->前面入口;
    if (項目個数 > 文字列データ->長さ一覧[現在位置]) 項目個数 = 文字列データ->長さ一覧[現在位置]; memcpy(データ, 文字列データ->データ + 現在位置 * 512, 項目個数);
    文字列データ->通信相手通信端点番号 = 文字列データ->ポート一覧[現在位置]; 文字列データ->通信相手番地 = 文字列データ->番地一覧[現在位置]; 文字列データ->前面入口 = (現在位置 + 1) % 4; 文字列データ->入口個数--; return 項目個数;
}
unsigned 通信網ポート番号(int ファイル取扱い) { 通信終点 *文字列データ = 値取得(ファイル取扱い); return !文字列データ ? 0 : 文字列データ->接続状態制御 ? 文字列データ->接続状態制御->local_port : 文字列データ->データグラム制御 ? 文字列データ->データグラム制御->local_port : 0; }
unsigned 通信相手ポート番号(int ファイル取扱い) { 通信終点 *文字列データ = 値取得(ファイル取扱い); return 文字列データ ? 文字列データ->通信相手通信端点番号 : 0; }
uint32_t 網通信相手番地(int ファイル取扱い) { 通信終点 *文字列データ = 値取得(ファイル取扱い); return 文字列データ ? 文字列データ->通信相手番地 : 0; }
void 通信網閉鎖(int ファイル取扱い) {
    通信終点 *文字列データ = 値取得(ファイル取扱い); if (!文字列データ) return;
    if (文字列データ->ポート受取) for (int 序数添字 = 0; 序数添字 < 32; ++序数添字) if (ソケット端点一覧[序数添字].型分類 && ソケット端点一覧[序数添字].判定未処理 == ファイル取扱い) 通信網閉鎖(序数添字);
    if (文字列データ->接続状態制御) {
        tcp_arg(文字列データ->接続状態制御, 0); if (文字列データ->ポート受取) tcp_accept(文字列データ->接続状態制御, 0); else { tcp_recv(文字列データ->接続状態制御, 0); tcp_err(文字列データ->接続状態制御, 0); }
        if (tcp_close(文字列データ->接続状態制御) != ERR_OK) tcp_abort(文字列データ->接続状態制御);
    }
    if (文字列データ->データグラム制御) udp_remove(文字列データ->データグラム制御); 文字列データ->型分類 = 0;
}
void 通信網調査(void) {
    if (!判定用意済み || 周期監視) return; 周期監視 = 1;
    if(使用結線済み通信網)結線済み通信網調査(&接続状態装置);
    for (unsigned 予算 = 0; !使用結線済み通信網 && 予算 < 4096 && (機械レジスタ(補助装置 + 0x54) & 1); 予算++) {
        unsigned 文字コード = 機械レジスタ(補助装置 + 0x40) & 255;
        if (文字コード == 192) {
            if (使用量受取 && !エラー受取 && !エスケープ受取) {
                struct pbuf *データ位置 = pbuf_alloc(PBUF_RAW, 使用量受取, PBUF_POOL);
                if (データ位置) { 受信済みデータグラム個数++; 受信済みバイト個数 += 使用量受取; pbuf_take(データ位置, データ緩衝域受取, 使用量受取); if (接続状態装置.input(データ位置, &接続状態装置) != ERR_OK) { 破棄件数データグラム個数++; pbuf_free(データ位置); } }
                else 破棄件数データグラム個数++;
            }
            else if (使用量受取) 破棄件数データグラム個数++;
            使用量受取 = エラー受取 = エスケープ受取 = 0;
        } else if (文字コード == 219 && !エスケープ受取) エスケープ受取 = 1;
        else {
            if (エスケープ受取) { if (文字コード != 220 && 文字コード != 221) エラー受取 = 1; 文字コード = 文字コード == 220 ? 192 : 219; エスケープ受取 = 0; }
            if (使用量受取 < sizeof(データ緩衝域受取)) データ緩衝域受取[使用量受取++] = 文字コード; else エラー受取 = 1;
        }
    }
    netif_poll(&接続状態装置); sys_check_timeouts(); ファイル転送調査(); 遠隔調査();
    for (unsigned 予算 = 0; 予算 < 4096 && 送信側個数 && (機械レジスタ(補助装置 + 0x54) & 0x20); 予算++) {
        機械レジスタ(補助装置 + 0x40) = 伝送データ[送信側先頭部]; 送信側先頭部 = (送信側先頭部 + 1) % sizeof(伝送データ); 送信側個数--;
    }
    周期監視 = 0;
}

/* 設定値·조회는 lwIP의 実際データ 인터페이스와 終端位置点 표를 사용한다. */
uint32_t 通信網状態読取(unsigned 入口値, unsigned 番号) {
    if(入口値==20)return 使用結線済み通信網;
    if(入口値==21)return 判定用意済み&&netif_is_link_up(&接続状態装置);
    if(入口値==22)return 使用結線済み通信網?結線済み通信網統計(5):0;
    if (!判定用意済み) return 0;
    if(使用結線済み通信網&&入口値>=4&&入口値<=8)return 結線済み通信網統計(入口値-4);
    if (入口値 == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&接続状態装置)));
    if (入口値 == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&接続状態装置)));
    if (入口値 == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&接続状態装置)));
    if (入口値 == 3) return netif_is_up(&接続状態装置) != 0;
    if (入口値 == 4) return 受信済みデータグラム個数;
    if (入口値 == 5) return 送信済みデータグラム個数;
    if (入口値 == 6) return 受信済みバイト個数;
    if (入口値 == 7) return 送信済みバイト個数;
    if (入口値 == 8) return 破棄件数データグラム個数;
    if (入口値 == 9) return 送信側個数;
    if (番号 >= 32) return 0;
    通信終点 *終端位置点 = &ソケット端点一覧[番号];
    if (入口値 == 10) return 終端位置点->型分類;
    if (!終端位置点->型分類) return 0;
    if (入口値 == 11) return 通信網ポート番号(番号);
    if (入口値 == 12) return 終端位置点->通信相手番地;
    if (入口値 == 13) return 終端位置点->通信相手通信端点番号;
    if (入口値 == 14) return 終端位置点->ポート受取 ? 1 : 終端位置点->ファイル終端位置 ? 3 : 終端位置点->エラー ? 4 : 終端位置点->接続済み ? 2 : 0;
    if (入口値 == 15) return 終端位置点->入口個数;
    if (入口値 == 16) {
        const ip_addr_t *番地 = 終端位置点->型分類 == 1 && 終端位置点->接続状態制御 ? &終端位置点->接続状態制御->local_ip :
            終端位置点->型分類 == 2 && 終端位置点->データグラム制御 ? &終端位置点->データグラム制御->local_ip : 0;
        return 番地 ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(番地))) : 0;
    }
    return 0;
}

int 通信網構成(unsigned 動作, uint32_t 番地, uint32_t マスク値, uint32_t 中継門値) {
    if (!判定用意済み) return -100;
    if (動作 == 1) { netif_set_up(&接続状態装置); return 0; }
    if (動作 == 2) { netif_set_down(&接続状態装置); return 0; }
    if (動作 != 0) return -22;
    /* 유니캐스트 IPv4, 密切替分岐一覧 マスク値, 같은 망의 선택적 既定値 中継門値. */
    uint32_t 反転済みマスク = ~マスク値;
    if (!マスク値 || (反転済みマスク & (反転済みマスク + 1)) || !番地 || (番地 >> 24) == 127 ||
        (番地 >> 24) == 0 || (番地 >> 28) >= 14 ||
        (反転済みマスク > 1 && (!(番地 & 反転済みマスク) || (番地 & 反転済みマスク) == 反転済みマスク)) ||
        (中継門値 && ((中継門値 & マスク値) != (番地 & マスク値) || 中継門値 == 番地 || (中継門値 >> 28) >= 14 ||
         (反転済みマスク > 1 && (!(中継門値 & 反転済みマスク) || (中継門値 & 反転済みマスク) == 反転済みマスク))))) return -22;
    /* 기존 연결을 番地 변경으로 몰래 끊지 않는다. */
    for (unsigned 番号 = 0; 番号 < 32; 番号++) if (ソケット端点一覧[番号].型分類 &&
        !(ソケット端点一覧[番号].ポート受取 && ソケット端点一覧[番号].接続状態制御 && ip_addr_isany(&ソケット端点一覧[番号].接続状態制御->local_ip))) return -16;
    if(使用結線済み通信網)dhcp_stop(&接続状態装置);
    ip4_addr_t 新規番地, 新規マスク, 新規中継門値;
    ip4_addr_set_u32(&新規番地, lwip_htonl(番地)); ip4_addr_set_u32(&新規マスク, lwip_htonl(マスク値)); ip4_addr_set_u32(&新規中継門値, lwip_htonl(中継門値));
    netif_set_addr(&接続状態装置, &新規番地, &新規マスク, &新規中継門値);
    return 0;
}

static struct raw_pcb *応答通信端点;
static uint32_t 番地試験, 時間試験, 応答時間;
static unsigned 列順試験, 識別子試験, 応答列順;
static int 応答状況;
static u8_t 保有応答(void *引数, struct raw_pcb *終端位置点, struct pbuf *データ, const ip_addr_t *番地) {
    (void)引数; (void)終端位置点;
    unsigned char 先頭部値[20], 返答[16];
    if (応答状況 != -11 || データ->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(番地))) != 番地試験 || pbuf_copy_partial(データ, 先頭部値, 20, 0) != 20) return 0;
    unsigned ヘッダー容量 = (先頭部値[0] & 15) * 4;
    if ((先頭部値[0] >> 4) != 4 || ヘッダー容量 < 20 || データ->tot_len < ヘッダー容量 + 16 ||
        pbuf_copy_partial(データ, 返答, 16, ヘッダー容量) != 16 || 返答[0] || 返答[1] ||
        (((unsigned)返答[4] << 8) | 返答[5]) != 識別子試験 ||
        (((unsigned)返答[6] << 8) | 返答[7]) != 列順試験 ||
        返答[8] != 'J' || 返答[9] != 'K' || 返答[10] != 'O' || 返答[11] != 'S' ||
        (((uint32_t)返答[12] << 24) | ((uint32_t)返答[13] << 16) | ((uint32_t)返答[14] << 8) | 返答[15]) != 時間試験) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(データ, ヘッダー容量)) return 0;
    if (inet_chksum_pbuf(データ)) { pbuf_add_header(データ, ヘッダー容量); return 0; }
    応答時間 = (uint32_t)基板経過ミリ秒() - 時間試験; 応答列順 = 先頭部値[8]; 応答状況 = 0;
    pbuf_free(データ); return 1;
}
int 応答試験開始処理(uint32_t 番地, unsigned 順序値) {
    if (!判定用意済み || !netif_is_up(&接続状態装置)) return -100;
    if (!番地 || (番地 >> 28) >= 14 || 番地 == 0xffffffffu) return -22;
    if (!応答通信端点) { 応答通信端点 = raw_new(IP_PROTO_ICMP); if (!応答通信端点) return -12; raw_recv(応答通信端点, 保有応答, 0); }
    番地試験 = 番地; 列順試験 = 順序値 & 65535; 識別子試験 = (識別子試験 + 1) & 65535;
    時間試験 = 基板経過ミリ秒(); 応答状況 = -11; 応答時間 = 応答列順 = 0;
    unsigned char データ[32] = {8,0,0,0};
    データ[4] = 識別子試験 >> 8; データ[5] = 識別子試験; データ[6] = 列順試験 >> 8; データ[7] = 列順試験;
    データ[8]='J'; データ[9]='K'; データ[10]='O'; データ[11]='S';
    データ[12]=時間試験 >> 24; データ[13]=時間試験 >> 16; データ[14]=時間試験 >> 8; データ[15]=時間試験;
    for (unsigned 位置添字 = 16; 位置添字 < sizeof(データ); 位置添字++) データ[位置添字] = 位置添字;
    uint16_t 検証結果検査和 = inet_chksum(データ, sizeof(データ)); memcpy(データ + 2, &検証結果検査和, 2);
    struct pbuf *データグラム = pbuf_alloc(PBUF_IP, sizeof(データ), PBUF_RAM); if (!データグラム) return -12;
    pbuf_take(データグラム, データ, sizeof(データ)); ip_addr_t 宛先通信端点; ip_addr_set_ip4_u32(&宛先通信端点, lwip_htonl(番地));
    err_t 処理済み値 = raw_sendto(応答通信端点, データグラム, &宛先通信端点); pbuf_free(データグラム);
    if (処理済み値) 応答状況 = エラー番号(処理済み値);
    return 処理済み値 ? 応答状況 : 0;
}
int 応答試験読取(unsigned 入口値) {
    通信網調査();
    return 入口値 == 0 ? 応答状況 : 入口値 == 1 ? (int)応答時間 : 入口値 == 2 ? (int)応答列順 : -22;
}
