#include "../命名/计算机连接名称列.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "通信网络.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../远程值/远程值.h"
#include "有线网络.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define 计算机寄存器(首位值) (*(volatile uint32_t *)(uintptr_t)(首位值))
#define 辅助设备 0xfe215000ul
extern uintptr_t 板经过毫秒(void);
static struct netif 连接状态设备;
static int 是否已准备, 轮询;
static int 使用有线网络;
static unsigned 接收用量, 接收转义, 接收错误;
static unsigned char 接收数据缓冲[1600];
static unsigned char 传输数据[32768];
static unsigned 发送侧头, 发送侧个数;
static uint32_t 已接收数据报个数, 已发送数据报个数, 已接收字节个数, 已发送字节个数, 已丢弃数数据报个数;
typedef struct {
    int 类型分类, 接收端口, 是否待处理, 已连接, 文件结束, 错误;
    struct tcp_pcb *连接状态控制;
    struct udp_pcb *数据报控制;
    unsigned 前端条目, 条目个数;
    unsigned char 数据[4096];
    unsigned 长度列[4], 端口列[4], 对端端点编号;
    uint32_t 地址列[4], 对端地址;
} 通信终点;
static 通信终点 套接字端点列[32];
u32_t sys_now(void) { return (u32_t)板经过毫秒(); }
static int 错误编号(err_t 辅助条目) {
    return 辅助条目 == ERR_MEM || 辅助条目 == ERR_BUF || 辅助条目 == ERR_WOULDBLOCK ? -11 : 辅助条目 == ERR_USE ? -98 :
        辅助条目 == ERR_RTE ? -101 : 辅助条目 == ERR_RST ? -104 : 辅助条目 == ERR_CONN ? -107 : 辅助条目 == ERR_TIMEOUT ? -110 : -5;
}
static 通信终点 *获取值(int 文件句柄) { return 文件句柄 >= 0 && 文件句柄 < 32 && 套接字端点列[文件句柄].类型分类 ? &套接字端点列[文件句柄] : 0; }
static int 预留(int 类型分类) {
    for (int 序数索引 = 0; 序数索引 < 32; ++序数索引) if (!套接字端点列[序数索引].类型分类) {
        memset(&套接字端点列[序数索引], 0, sizeof(通信终点)); 套接字端点列[序数索引].类型分类 = 类型分类; 套接字端点列[序数索引].是否待处理 = -1; return 序数索引;
    }
    return -24;
}
static void 发射值(unsigned 字符代码) { 传输数据[(发送侧头 + 发送侧个数++) % sizeof(传输数据)] = 字符代码; }
static err_t 输出结果(struct netif *项目个数, struct pbuf *数据位置, const ip4_addr_t *地址) {
    (void)项目个数; (void)地址;
    if (数据位置->tot_len > 1500 || 发送侧个数 + 2 * 数据位置->tot_len + 2 > sizeof(传输数据)) return ERR_MEM;
    发射值(192);
    for (struct pbuf *下一偏移 = 数据位置; 下一偏移; 下一偏移 = 下一偏移->next) for (unsigned 序数索引 = 0; 序数索引 < 下一偏移->len; 序数索引++) {
        unsigned 字符代码 = ((unsigned char *)下一偏移->payload)[序数索引];
        if (字符代码 == 192 || 字符代码 == 219) { 发射值(219); 发射值(字符代码 == 192 ? 220 : 221); } else 发射值(字符代码);
    }
    发射值(192); 已发送数据报个数++; 已发送字节个数 += 数据位置->tot_len; return ERR_OK;
}
static err_t 准备运行时(struct netif *项目个数) { 项目个数->name[0] = 's'; 项目个数->name[1] = 'l'; 项目个数->mtu = 1500; 项目个数->output = 输出结果; return ERR_OK; }
void 准备网络(void) {
    if (是否已准备) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    计算机寄存器(辅助设备 + 4) |= 1; 计算机寄存器(辅助设备 + 0x60) = 0; 计算机寄存器(辅助设备 + 0x44) = 0;
    计算机寄存器(辅助设备 + 0x48) = 0xc6; 计算机寄存器(辅助设备 + 0x4c) = 3; 计算机寄存器(辅助设备 + 0x68) = 270; 计算机寄存器(辅助设备 + 0x60) = 3;
    lwip_init();
    ip4_addr_t 互联网地址, 位掩码, 网关地址;
    使用有线网络=拥有有线设备();
    ip4_addr_set_u32(&互联网地址, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&位掩码, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&网关地址, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&连接状态设备, &互联网地址, &位掩码, &网关地址, 0, 使用有线网络?准备有线网络:准备运行时, 使用有线网络?ethernet_input:ip4_input))return;
    netif_set_default(&连接状态设备); netif_set_up(&连接状态设备);if(!使用有线网络)netif_set_link_up(&连接状态设备); 是否已准备 = 1;
    准备远程();
}
static err_t 拥有已接收(void *附加参数列, struct tcp_pcb *传输状态控制块, struct pbuf *数据位置, err_t 错误) {
    通信终点 *字符串数据 = 附加参数列; (void)传输状态控制块; (void)错误;
    if (!数据位置) { 字符串数据->文件结束 = 1; return ERR_OK; }
    if (数据位置->tot_len > sizeof(字符串数据->数据) - 字符串数据->条目个数) return ERR_MEM;
    unsigned 当前位置 = (字符串数据->前端条目 + 字符串数据->条目个数) % sizeof(字符串数据->数据);
    for (struct pbuf *下一偏移 = 数据位置; 下一偏移; 下一偏移 = 下一偏移->next) for (unsigned 序数索引 = 0; 序数索引 < 下一偏移->len; 序数索引++) {
        字符串数据->数据[当前位置] = ((unsigned char *)下一偏移->payload)[序数索引]; 当前位置 = (当前位置 + 1) % sizeof(字符串数据->数据);
    }
    字符串数据->条目个数 += 数据位置->tot_len; pbuf_free(数据位置); return ERR_OK;
}
static void 拥有失败(void *附加参数列, err_t 错误) { 通信终点 *字符串数据 = 附加参数列; 字符串数据->连接状态控制 = 0; 字符串数据->错误 = 错误编号(错误); }
static void 回调列(通信终点 *字符串数据) { tcp_arg(字符串数据->连接状态控制, 字符串数据); tcp_recv(字符串数据->连接状态控制, 拥有已接收); tcp_err(字符串数据->连接状态控制, 拥有失败); }
static err_t 已连接(void *附加参数列, struct tcp_pcb *传输状态控制块, err_t 错误) {
    通信终点 *字符串数据 = 附加参数列; (void)传输状态控制块; if (错误) 字符串数据->错误 = 错误编号(错误); else 字符串数据->已连接 = 1; return ERR_OK;
}
static err_t 已接受(void *附加参数列, struct tcp_pcb *传输状态控制块, err_t 错误) {
    通信终点 *父 = 附加参数列; if (错误) return 错误;
    int 文件句柄 = 预留(1); if (文件句柄 < 0) return ERR_MEM;
    通信终点 *字符串数据 = &套接字端点列[文件句柄]; 字符串数据->连接状态控制 = 传输状态控制块; 字符串数据->已连接 = 1; 字符串数据->是否待处理 = (int)(父 - 套接字端点列);
    字符串数据->对端地址 = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&传输状态控制块->remote_ip))); 字符串数据->对端端点编号 = 传输状态控制块->remote_port;
    回调列(字符串数据); return ERR_OK;
}
static void 数据报(void *附加参数列, struct udp_pcb *传输状态控制块, struct pbuf *数据位置, const ip_addr_t *地址, u16_t 端口编号) {
    通信终点 *字符串数据 = 附加参数列; (void)传输状态控制块;
    if (字符串数据->条目个数 < 4 && 数据位置->tot_len <= 512) {
        unsigned 位置索引 = (字符串数据->前端条目 + 字符串数据->条目个数) % 4;
        pbuf_copy_partial(数据位置, 字符串数据->数据 + 位置索引 * 512, 数据位置->tot_len, 0);
        字符串数据->长度列[位置索引] = 数据位置->tot_len; 字符串数据->端口列[位置索引] = 端口编号;
        字符串数据->地址列[位置索引] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(地址))); 字符串数据->条目个数++;
    }
    pbuf_free(数据位置);
}
int 创建套接字端点(int 类型分类) {
    if (!是否已准备) return -100;
    if (类型分类 != 1 && 类型分类 != 2) return -93;
    int 文件句柄 = 预留(类型分类); if (文件句柄 < 0) return 文件句柄;
    通信终点 *字符串数据 = &套接字端点列[文件句柄];
    if (类型分类 == 1) { 字符串数据->连接状态控制 = tcp_new(); if (字符串数据->连接状态控制) 回调列(字符串数据); }
    else { 字符串数据->数据报控制 = udp_new(); if (字符串数据->数据报控制) udp_recv(字符串数据->数据报控制, 数据报, 字符串数据); }
    if (!字符串数据->连接状态控制 && !字符串数据->数据报控制) { 字符串数据->类型分类 = 0; return -12; } return 文件句柄;
}
int 网络层绑定(int 文件句柄, uint32_t 地址, unsigned 端口编号) {
    通信终点 *字符串数据 = 获取值(文件句柄); if (!字符串数据) return -9;
    if (端口编号 > 65535 || (地址 && 地址 != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&连接状态设备))) && 地址 != 0x7f000001)) return -99;
    ip_addr_t 互联网地址; ip_addr_set_ip4_u32(&互联网地址, lwip_htonl(地址));
    err_t 辅助条目 = 字符串数据->类型分类 == 1 ? tcp_bind(字符串数据->连接状态控制, &互联网地址, 端口编号) : udp_bind(字符串数据->数据报控制, &互联网地址, 端口编号); return 辅助条目 ? 错误编号(辅助条目) : 0;
}
void 复用套接字地址(int 文件句柄) { 通信终点 *字符串数据 = 获取值(文件句柄); if (字符串数据 && 字符串数据->连接状态控制) ip_set_option(字符串数据->连接状态控制, SOF_REUSEADDR); }
int 网络层侦听(int 文件句柄) {
    通信终点 *字符串数据 = 获取值(文件句柄); if (!字符串数据 || 字符串数据->类型分类 != 1) return -9;
    if (字符串数据->接收端口) return 0;
    err_t 辅助条目; struct tcp_pcb *传输状态控制块 = tcp_listen_with_backlog_and_err(字符串数据->连接状态控制, 4, &辅助条目);
    if (!传输状态控制块) return 错误编号(辅助条目); 字符串数据->连接状态控制 = 传输状态控制块; 字符串数据->接收端口 = 1; tcp_arg(传输状态控制块, 字符串数据); tcp_accept(传输状态控制块, 已接受); return 0;
}
int 网络层连接(int 文件句柄, uint32_t 地址, unsigned 端口编号) {
    通信终点 *字符串数据 = 获取值(文件句柄); if (!字符串数据 || 字符串数据->类型分类 != 1) return -9;
    if (字符串数据->错误) return 字符串数据->错误;
    if (字符串数据->已连接) return 0;
    if (字符串数据->对端端点编号) return -115;
    if (!端口编号 || 端口编号 > 65535 || !地址) return -22;
    ip_addr_t 互联网地址; ip_addr_set_ip4_u32(&互联网地址, lwip_htonl(地址));
    字符串数据->对端地址 = 地址; 字符串数据->对端端点编号 = 端口编号;
    err_t 辅助条目 = tcp_connect(字符串数据->连接状态控制, &互联网地址, 端口编号, 已连接); return 辅助条目 ? 错误编号(辅助条目) : -115;
}
int 网络层接受(int 文件句柄) {
    通信终点 *字符串数据 = 获取值(文件句柄); if (!字符串数据 || !字符串数据->接收端口) return -22;
    for (int 序数索引 = 0; 序数索引 < 32; 序数索引++) if (套接字端点列[序数索引].类型分类 == 1 && 套接字端点列[序数索引].是否待处理 == 文件句柄) { 套接字端点列[序数索引].是否待处理 = -1; return 序数索引; }
    return -11;
}
int 网络层读取(int 文件句柄, void *数据, unsigned 项目个数) {
    通信终点 *字符串数据 = 获取值(文件句柄); if (!字符串数据 || 字符串数据->类型分类 != 1) return -9;
    if (!项目个数) return 0; if (!字符串数据->条目个数) return 字符串数据->错误 ? 字符串数据->错误 : 字符串数据->文件结束 ? 0 : -11;
    if (项目个数 > 字符串数据->条目个数) 项目个数 = 字符串数据->条目个数;
    for (unsigned 序数索引 = 0; 序数索引 < 项目个数; 序数索引++) { ((unsigned char *)数据)[序数索引] = 字符串数据->数据[字符串数据->前端条目]; 字符串数据->前端条目 = (字符串数据->前端条目 + 1) % sizeof(字符串数据->数据); }
    字符串数据->条目个数 -= 项目个数; if (字符串数据->连接状态控制) tcp_recved(字符串数据->连接状态控制, 项目个数); return 项目个数;
}
int 网络层写入(int 文件句柄, const void *数据, unsigned 项目个数) {
    通信终点 *字符串数据 = 获取值(文件句柄); if (!字符串数据 || 字符串数据->类型分类 != 1) return -9;
    if (字符串数据->错误) return 字符串数据->错误; if (!字符串数据->连接状态控制 || !字符串数据->已连接) return -107;
    if (!项目个数) return 0; if (项目个数 > tcp_sndbuf(字符串数据->连接状态控制)) 项目个数 = tcp_sndbuf(字符串数据->连接状态控制);
    if (!项目个数) return -11; if (项目个数 > 1024) 项目个数 = 1024;
    err_t 辅助条目 = tcp_write(字符串数据->连接状态控制, 数据, 项目个数, TCP_WRITE_FLAG_COPY); if (辅助条目) return 错误编号(辅助条目);
    tcp_output(字符串数据->连接状态控制); return 项目个数;
}
int 发送数据报(int 文件句柄, const void *数据, unsigned 项目个数, uint32_t 地址, unsigned 端口编号) {
    通信终点 *字符串数据 = 获取值(文件句柄); if (!字符串数据 || 字符串数据->类型分类 != 2) return -9;
    if (项目个数 > 512) return -90; if (!端口编号 || 端口编号 > 65535) return -22;
    struct pbuf *数据位置 = pbuf_alloc(PBUF_TRANSPORT, 项目个数, PBUF_RAM); if (!数据位置) return -11;
    pbuf_take(数据位置, 数据, 项目个数); ip_addr_t 互联网地址; ip_addr_set_ip4_u32(&互联网地址, lwip_htonl(地址));
    err_t 辅助条目 = udp_sendto(字符串数据->数据报控制, 数据位置, &互联网地址, 端口编号); pbuf_free(数据位置); return 辅助条目 ? 错误编号(辅助条目) : (int)项目个数;
}
int 接收数据报(int 文件句柄, void *数据, unsigned 项目个数) {
    通信终点 *字符串数据 = 获取值(文件句柄); if (!字符串数据 || 字符串数据->类型分类 != 2) return -9;
    if (!字符串数据->条目个数) return -11; unsigned 当前位置 = 字符串数据->前端条目;
    if (项目个数 > 字符串数据->长度列[当前位置]) 项目个数 = 字符串数据->长度列[当前位置]; memcpy(数据, 字符串数据->数据 + 当前位置 * 512, 项目个数);
    字符串数据->对端端点编号 = 字符串数据->端口列[当前位置]; 字符串数据->对端地址 = 字符串数据->地址列[当前位置]; 字符串数据->前端条目 = (当前位置 + 1) % 4; 字符串数据->条目个数--; return 项目个数;
}
unsigned 网络端口编号(int 文件句柄) { 通信终点 *字符串数据 = 获取值(文件句柄); return !字符串数据 ? 0 : 字符串数据->连接状态控制 ? 字符串数据->连接状态控制->local_port : 字符串数据->数据报控制 ? 字符串数据->数据报控制->local_port : 0; }
unsigned 对端端口编号(int 文件句柄) { 通信终点 *字符串数据 = 获取值(文件句柄); return 字符串数据 ? 字符串数据->对端端点编号 : 0; }
uint32_t 网络层对端地址(int 文件句柄) { 通信终点 *字符串数据 = 获取值(文件句柄); return 字符串数据 ? 字符串数据->对端地址 : 0; }
void 关闭网络(int 文件句柄) {
    通信终点 *字符串数据 = 获取值(文件句柄); if (!字符串数据) return;
    if (字符串数据->接收端口) for (int 序数索引 = 0; 序数索引 < 32; ++序数索引) if (套接字端点列[序数索引].类型分类 && 套接字端点列[序数索引].是否待处理 == 文件句柄) 关闭网络(序数索引);
    if (字符串数据->连接状态控制) {
        tcp_arg(字符串数据->连接状态控制, 0); if (字符串数据->接收端口) tcp_accept(字符串数据->连接状态控制, 0); else { tcp_recv(字符串数据->连接状态控制, 0); tcp_err(字符串数据->连接状态控制, 0); }
        if (tcp_close(字符串数据->连接状态控制) != ERR_OK) tcp_abort(字符串数据->连接状态控制);
    }
    if (字符串数据->数据报控制) udp_remove(字符串数据->数据报控制); 字符串数据->类型分类 = 0;
}
void 审查网络(void) {
    if (!是否已准备 || 轮询) return; 轮询 = 1;
    if(使用有线网络)审查有线网络(&连接状态设备);
    for (unsigned 预算 = 0; !使用有线网络 && 预算 < 4096 && (计算机寄存器(辅助设备 + 0x54) & 1); 预算++) {
        unsigned 字符代码 = 计算机寄存器(辅助设备 + 0x40) & 255;
        if (字符代码 == 192) {
            if (接收用量 && !接收错误 && !接收转义) {
                struct pbuf *数据位置 = pbuf_alloc(PBUF_RAW, 接收用量, PBUF_POOL);
                if (数据位置) { 已接收数据报个数++; 已接收字节个数 += 接收用量; pbuf_take(数据位置, 接收数据缓冲, 接收用量); if (连接状态设备.input(数据位置, &连接状态设备) != ERR_OK) { 已丢弃数数据报个数++; pbuf_free(数据位置); } }
                else 已丢弃数数据报个数++;
            }
            else if (接收用量) 已丢弃数数据报个数++;
            接收用量 = 接收错误 = 接收转义 = 0;
        } else if (字符代码 == 219 && !接收转义) 接收转义 = 1;
        else {
            if (接收转义) { if (字符代码 != 220 && 字符代码 != 221) 接收错误 = 1; 字符代码 = 字符代码 == 220 ? 192 : 219; 接收转义 = 0; }
            if (接收用量 < sizeof(接收数据缓冲)) 接收数据缓冲[接收用量++] = 字符代码; else 接收错误 = 1;
        }
    }
    netif_poll(&连接状态设备); sys_check_timeouts(); 审查文件传送(); 审查远程();
    for (unsigned 预算 = 0; 预算 < 4096 && 发送侧个数 && (计算机寄存器(辅助设备 + 0x54) & 0x20); 预算++) {
        计算机寄存器(辅助设备 + 0x40) = 传输数据[发送侧头]; 发送侧头 = (发送侧头 + 1) % sizeof(传输数据); 发送侧个数--;
    }
    轮询 = 0;
}

/* 设置·조회는 lwIP의 实际数据 인터페이스와 结束分 표를 사용한다. */
uint32_t 读取网络运行状态(unsigned 条目值, unsigned 编号) {
    if(条目值==20)return 使用有线网络;
    if(条目值==21)return 是否已准备&&netif_is_link_up(&连接状态设备);
    if(条目值==22)return 使用有线网络?有线网络统计(5):0;
    if (!是否已准备) return 0;
    if(使用有线网络&&条目值>=4&&条目值<=8)return 有线网络统计(条目值-4);
    if (条目值 == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&连接状态设备)));
    if (条目值 == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&连接状态设备)));
    if (条目值 == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&连接状态设备)));
    if (条目值 == 3) return netif_is_up(&连接状态设备) != 0;
    if (条目值 == 4) return 已接收数据报个数;
    if (条目值 == 5) return 已发送数据报个数;
    if (条目值 == 6) return 已接收字节个数;
    if (条目值 == 7) return 已发送字节个数;
    if (条目值 == 8) return 已丢弃数数据报个数;
    if (条目值 == 9) return 发送侧个数;
    if (编号 >= 32) return 0;
    通信终点 *结束分 = &套接字端点列[编号];
    if (条目值 == 10) return 结束分->类型分类;
    if (!结束分->类型分类) return 0;
    if (条目值 == 11) return 网络端口编号(编号);
    if (条目值 == 12) return 结束分->对端地址;
    if (条目值 == 13) return 结束分->对端端点编号;
    if (条目值 == 14) return 结束分->接收端口 ? 1 : 结束分->文件结束 ? 3 : 结束分->错误 ? 4 : 结束分->已连接 ? 2 : 0;
    if (条目值 == 15) return 结束分->条目个数;
    if (条目值 == 16) {
        const ip_addr_t *地址 = 结束分->类型分类 == 1 && 结束分->连接状态控制 ? &结束分->连接状态控制->local_ip :
            结束分->类型分类 == 2 && 结束分->数据报控制 ? &结束分->数据报控制->local_ip : 0;
        return 地址 ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(地址))) : 0;
    }
    return 0;
}

int 设定配置网络(unsigned 动作, uint32_t 地址, uint32_t 掩码值, uint32_t 网关值) {
    if (!是否已准备) return -100;
    if (动作 == 1) { netif_set_up(&连接状态设备); return 0; }
    if (动作 == 2) { netif_set_down(&连接状态设备); return 0; }
    if (动作 != 0) return -22;
    /* 유니캐스트 IPv4, 稠密切换分支项集 掩码值, 같은 망의 선택적 默认值 网关值. */
    uint32_t 已反转掩码 = ~掩码值;
    if (!掩码值 || (已反转掩码 & (已反转掩码 + 1)) || !地址 || (地址 >> 24) == 127 ||
        (地址 >> 24) == 0 || (地址 >> 28) >= 14 ||
        (已反转掩码 > 1 && (!(地址 & 已反转掩码) || (地址 & 已反转掩码) == 已反转掩码)) ||
        (网关值 && ((网关值 & 掩码值) != (地址 & 掩码值) || 网关值 == 地址 || (网关值 >> 28) >= 14 ||
         (已反转掩码 > 1 && (!(网关值 & 已反转掩码) || (网关值 & 已反转掩码) == 已反转掩码))))) return -22;
    /* 기존 연결을 地址 변경으로 몰래 끊지 않는다. */
    for (unsigned 编号 = 0; 编号 < 32; 编号++) if (套接字端点列[编号].类型分类 &&
        !(套接字端点列[编号].接收端口 && 套接字端点列[编号].连接状态控制 && ip_addr_isany(&套接字端点列[编号].连接状态控制->local_ip))) return -16;
    if(使用有线网络)dhcp_stop(&连接状态设备);
    ip4_addr_t 新建地址, 新建掩码, 新建网关值;
    ip4_addr_set_u32(&新建地址, lwip_htonl(地址)); ip4_addr_set_u32(&新建掩码, lwip_htonl(掩码值)); ip4_addr_set_u32(&新建网关值, lwip_htonl(网关值));
    netif_set_addr(&连接状态设备, &新建地址, &新建掩码, &新建网关值);
    return 0;
}

static struct raw_pcb *响应端点;
static uint32_t 测试地址, 测试时间, 响应时间;
static unsigned 测试序列, 测试标识符, 响应序列;
static int 响应状态;
static u8_t 拥有响应(void *实参, struct raw_pcb *结束分, struct pbuf *数据, const ip_addr_t *地址) {
    (void)实参; (void)结束分;
    unsigned char 头值[20], 回复[16];
    if (响应状态 != -11 || 数据->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(地址))) != 测试地址 || pbuf_copy_partial(数据, 头值, 20, 0) != 20) return 0;
    unsigned 头部大小 = (头值[0] & 15) * 4;
    if ((头值[0] >> 4) != 4 || 头部大小 < 20 || 数据->tot_len < 头部大小 + 16 ||
        pbuf_copy_partial(数据, 回复, 16, 头部大小) != 16 || 回复[0] || 回复[1] ||
        (((unsigned)回复[4] << 8) | 回复[5]) != 测试标识符 ||
        (((unsigned)回复[6] << 8) | 回复[7]) != 测试序列 ||
        回复[8] != 'J' || 回复[9] != 'K' || 回复[10] != 'O' || 回复[11] != 'S' ||
        (((uint32_t)回复[12] << 24) | ((uint32_t)回复[13] << 16) | ((uint32_t)回复[14] << 8) | 回复[15]) != 测试时间) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(数据, 头部大小)) return 0;
    if (inet_chksum_pbuf(数据)) { pbuf_add_header(数据, 头部大小); return 0; }
    响应时间 = (uint32_t)板经过毫秒() - 测试时间; 响应序列 = 头值[8]; 响应状态 = 0;
    pbuf_free(数据); return 1;
}
int 开始响应测试(uint32_t 地址, unsigned 排序值) {
    if (!是否已准备 || !netif_is_up(&连接状态设备)) return -100;
    if (!地址 || (地址 >> 28) >= 14 || 地址 == 0xffffffffu) return -22;
    if (!响应端点) { 响应端点 = raw_new(IP_PROTO_ICMP); if (!响应端点) return -12; raw_recv(响应端点, 拥有响应, 0); }
    测试地址 = 地址; 测试序列 = 排序值 & 65535; 测试标识符 = (测试标识符 + 1) & 65535;
    测试时间 = 板经过毫秒(); 响应状态 = -11; 响应时间 = 响应序列 = 0;
    unsigned char 数据[32] = {8,0,0,0};
    数据[4] = 测试标识符 >> 8; 数据[5] = 测试标识符; 数据[6] = 测试序列 >> 8; 数据[7] = 测试序列;
    数据[8]='J'; 数据[9]='K'; 数据[10]='O'; 数据[11]='S';
    数据[12]=测试时间 >> 24; 数据[13]=测试时间 >> 16; 数据[14]=测试时间 >> 8; 数据[15]=测试时间;
    for (unsigned 位置索引 = 16; 位置索引 < sizeof(数据); 位置索引++) 数据[位置索引] = 位置索引;
    uint16_t 验证校验和 = inet_chksum(数据, sizeof(数据)); memcpy(数据 + 2, &验证校验和, 2);
    struct pbuf *数据报 = pbuf_alloc(PBUF_IP, sizeof(数据), PBUF_RAM); if (!数据报) return -12;
    pbuf_take(数据报, 数据, sizeof(数据)); ip_addr_t 目的地址端点; ip_addr_set_ip4_u32(&目的地址端点, lwip_htonl(地址));
    err_t 已处理值 = raw_sendto(响应端点, 数据报, &目的地址端点); pbuf_free(数据报);
    if (已处理值) 响应状态 = 错误编号(已处理值);
    return 已处理值 ? 响应状态 : 0;
}
int 读取响应测试(unsigned 条目值) {
    审查网络();
    return 条目值 == 0 ? 响应状态 : 条目值 == 1 ? (int)响应时间 : 条目值 == 2 ? (int)响应序列 : -22;
}
