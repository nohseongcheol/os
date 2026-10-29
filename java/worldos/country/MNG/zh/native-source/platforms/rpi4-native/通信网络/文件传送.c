#include "../命名/计算机连接名称列.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "通信网络.h"
#include "string.h"
#include "文件ABI.h"
extern uintptr_t 板经过毫秒(void);
extern int32_t Java文件系统条目长度(int32_t), Java文件系统条目字节(int32_t,int32_t), Java文件系统条目大小(int32_t);
extern int32_t Java文件系统条目个数(void);
static int 接收端口 = -1, 控制 = -1, 手册连接状态 = -1, 数据 = -1;
static unsigned 是否已记日志输入侧, 用户正常确认, 行大小, 行错误, 结束程序, 执行中任务, 已使用容量, 已发送个数, 拥有失败;
static unsigned 回复大小, 回复已发送, 下一端口编号;
static uint32_t 活动;
static char 行[256], 回复列[2048], 文件条目名称[64], 传送名称[64];
static unsigned char 传送状态[16384];
static int 相等(const char *首位值, const char *第二值) { while (*首位值 && *首位值 == *第二值) { 首位值++; 第二值++; } return *首位值 == *第二值; }
static void 回复(const char *字符串数据) {
    size_t 项目个数 = strlen(字符串数据);
    if (回复已发送) { memmove(回复列, 回复列 + 回复已发送, 回复大小 - 回复已发送); 回复大小 -= 回复已发送; 回复已发送 = 0; }
    if (项目个数 > sizeof(回复列) - 回复大小) { 结束程序 = 1; return; }
    memcpy(回复列 + 回复大小, 字符串数据, 项目个数); 回复大小 += 项目个数;
}
static void 数值值(unsigned 值, char *结果数据, unsigned *项目个数) {
    char 数字个数[10]; unsigned 条目个数 = 0;
    do { 数字个数[条目个数++] = '0' + 值 % 10; 值 /= 10; } while (值);
    while (条目个数) 结果数据[(*项目个数)++] = 数字个数[--条目个数];
}
static void 停止传送(void) {
    if (数据 >= 0) 关闭网络(数据); if (手册连接状态 >= 0) 关闭网络(手册连接状态);
    数据 = 手册连接状态 = -1; 执行中任务 = 已使用容量 = 已发送个数 = 拥有失败 = 0;
}
static void 断开连接(void) {
    停止传送(); if (控制 >= 0) 关闭网络(控制); 控制 = -1;
    是否已记日志输入侧 = 用户正常确认 = 行大小 = 行错误 = 回复大小 = 回复已发送 = 结束程序 = 0;
}
int 文件传送控制(int 动作) {
    if (动作 == 2) return 接收端口 >= 0;
    if (动作 == 0) { 断开连接(); if (接收端口 >= 0) 关闭网络(接收端口); 接收端口 = -1; return 0; }
    if (动作 != 1) return -22; if (接收端口 >= 0) return 0;
    接收端口 = 创建套接字端点(1); if (接收端口 < 0) return 接收端口;
    int 已返回值 = 网络层绑定(接收端口, 读取网络运行状态(0,0), 21); if (!已返回值) 已返回值 = 网络层侦听(接收端口);
    if (已返回值 < 0) { 关闭网络(接收端口); 接收端口 = -1; } return 已返回值;
}
static int 路径(const char *名称) {
    unsigned 项目个数 = 0; if (*名称 == '/') 名称++;
    if (!*名称 || 相等(名称, ".") || 相等(名称, "..")) return 0;
    文件条目名称[项目个数++] = '/';
    while (*名称) {
        unsigned char 字符代码 = *名称++;
        if (项目个数 >= 63 || 字符代码 < 32 || 字符代码 == 127 || 字符代码 == '/' || 字符代码 == '\\') return 0;
        文件条目名称[项目个数++] = 字符代码;
    }
    文件条目名称[项目个数] = 0; return 1;
}
static void 发送列表(int 详情) {
    已使用容量 = 已发送个数 = 0;
    for (int 序数索引 = 0; 序数索引 < Java文件系统条目个数(); 序数索引++) {
        int 项目个数 = Java文件系统条目长度(序数索引); if (项目个数 <= 0) continue;
        const char *前导部分 = 详情 == 2 ? "type=file;size=" : 详情 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned 条目个数 = strlen(前导部分); memcpy(传送状态 + 已使用容量, 前导部分, 条目个数); 已使用容量 += 条目个数;
        if (详情) 数值值(Java文件系统条目大小(序数索引), (char *)传送状态, &已使用容量);
        const char *后缀值 = 详情 == 2 ? "; " : 详情 == 1 ? " Jan 01 00:00 " : "";
        条目个数 = strlen(后缀值); memcpy(传送状态 + 已使用容量, 后缀值, 条目个数); 已使用容量 += 条目个数;
        for (int 内部侧序数 = 0; 内部侧序数 < 项目个数; 内部侧序数++) 传送状态[已使用容量++] = Java文件系统条目字节(序数索引,内部侧序数);
        传送状态[已使用容量++] = '\r'; 传送状态[已使用容量++] = '\n';
    }
}
static void 准备手册连接状态(int 已扩展) {
    if (执行中任务) { 回复("450 Transfer in progress\r\n"); return; }
    停止传送(); 手册连接状态 = 创建套接字端点(1);
    if (手册连接状态 >= 0) 复用套接字地址(手册连接状态);
    unsigned 端口编号 = 50000 + 下一端口编号++ % 8;
    if (手册连接状态 < 0 || 网络层绑定(手册连接状态, 读取网络运行状态(0,0), 端口编号) || 网络层侦听(手册连接状态)) {
        停止传送(); 回复("425 Cannot open passive listener\r\n"); return;
    }
    char 响应[96]; const char *前导部分 = 已扩展 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned 项目个数 = strlen(前导部分); memcpy(响应, 前导部分, 项目个数);
    if (已扩展) { 数值值(端口编号, 响应, &项目个数); 响应[项目个数++] = '|'; }
    else {
        uint32_t 地址=读取网络运行状态(0,0);
        for (int 位置索引=24;位置索引>=0;位置索引-=8) { 数值值((地址>>位置索引)&255,响应,&项目个数);响应[项目个数++]=','; }
        数值值(端口编号 / 256, 响应, &项目个数); 响应[项目个数++] = ','; 数值值(端口编号 % 256, 响应, &项目个数);
    }
    响应[项目个数++] = ')'; 响应[项目个数++] = '\r'; 响应[项目个数++] = '\n'; 响应[项目个数] = 0; 回复(响应);
}
static void 命令(void) {
    行[行大小] = 0;
    char *附加参数列 = 行; while (*附加参数列 && *附加参数列 != ' ') { if (*附加参数列 >= 'a' && *附加参数列 <= 'z') *附加参数列 -= 32; 附加参数列++; }
    if (*附加参数列) *附加参数列++ = 0; while (*附加参数列 == ' ') 附加参数列++;
    if (相等(行, "QUIT")) { 停止传送(); 回复("221 Goodbye\r\n"); 结束程序 = 1; return; }
    if (相等(行, "NOOP")) { 回复("200 OK\r\n"); return; }
    if (相等(行, "SYST")) { 回复("215 UNIX Type: L8\r\n"); return; }
    if (相等(行, "FEAT")) { 回复("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (相等(行, "USER")) { 是否已记日志输入侧 = 0; 用户正常确认 = 相等(附加参数列, "anonymous") || 相等(附加参数列, "jkoros"); 回复(用户正常确认 ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (相等(行, "PASS")) { 是否已记日志输入侧 = 用户正常确认; 回复(是否已记日志输入侧 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!是否已记日志输入侧) { 回复("530 Login first\r\n"); return; }
    if (相等(行, "PWD")) 回复("257 \"/\"\r\n");
    else if (相等(行, "CWD")) 回复(相等(附加参数列, "/") || 相等(附加参数列, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (相等(行, "TYPE")) 回复(相等(附加参数列, "I") || 相等(附加参数列, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (相等(行, "OPTS")) 回复(相等(附加参数列, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (相等(行, "PASV")) 准备手册连接状态(0);
    else if (相等(行, "EPSV")) { if (*附加参数列 && !相等(附加参数列, "1")) 回复("522 IPv4 only\r\n"); else 准备手册连接状态(1); }
    else if (相等(行, "ABOR")) { 停止传送(); 回复("226 Transfer aborted\r\n"); }
    else if (相等(行, "DELE")) { 回复(路径(附加参数列) && pk_unlink(文件条目名称) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (相等(行, "LIST") || 相等(行, "NLST") || 相等(行, "MLSD")) {
        if (执行中任务) { 回复("450 Transfer in progress\r\n"); return; }
        if (手册连接状态 < 0 && 数据 < 0) { 回复("425 Use PASV or EPSV\r\n"); return; }
        if (*附加参数列 && !相等(附加参数列,"/") && !相等(附加参数列,".") && !相等(附加参数列,"-a") && !相等(附加参数列,"-l") && !相等(附加参数列,"-la")) { 回复("550 Root listing only\r\n"); return; }
        发送列表(相等(行,"MLSD") ? 2 : 相等(行,"LIST") ? 1 : 0); 执行中任务 = 2;
        回复("150 Opening directory listing\r\n");
    }
    else if (相等(行, "SIZE")) {
        if (!路径(附加参数列)) { 回复("550 Invalid filename\r\n"); return; }
        int 文件句柄 = pk_open(文件条目名称, 读取仅用值, 0); if (文件句柄 < 0) { 回复("550 File unavailable\r\n"); return; }
        int 大小 = pk_size(文件句柄); pk_close(文件句柄); char 响应[32] = "213 "; unsigned 项目个数 = 4;
        数值值(大小, 响应, &项目个数); 响应[项目个数++] = '\r'; 响应[项目个数++] = '\n'; 响应[项目个数] = 0; 回复(响应);
    } else if (相等(行, "STOR") || 相等(行, "RETR")) {
        if (执行中任务) { 回复("450 Transfer in progress\r\n"); return; }
        if (手册连接状态 < 0 && 数据 < 0) { 回复("425 Use PASV or EPSV\r\n"); return; }
        if (!路径(附加参数列)) { 回复("550 Invalid filename\r\n"); return; }
        执行中任务 = 相等(行, "STOR") ? 1 : 2; 已使用容量 = 已发送个数 = 拥有失败 = 0;
        memcpy(传送名称, 文件条目名称, strlen(文件条目名称) + 1);
        if (执行中任务 == 2) {
            int 文件句柄 = pk_open(文件条目名称, 读取仅用值, 0);
            if (文件句柄 < 0) { 执行中任务 = 0; 回复("550 File unavailable\r\n"); return; }
            int 项目个数 = pk_read(文件句柄, 传送状态, sizeof(传送状态)); pk_close(文件句柄);
            if (项目个数 < 0) { 执行中任务 = 0; 回复("451 Read failed\r\n"); return; } 已使用容量 = 项目个数;
        }
        回复("150 Opening binary data connection\r\n");
    } else 回复("502 Command not implemented\r\n");
}
void 审查文件传送(void) {
    if (接收端口 < 0) return;
    int 传入连接状态 = 网络层接受(接收端口);
    if (传入连接状态 >= 0) {
        if (控制 >= 0) { 网络层写入(传入连接状态, "421 One session at a time\r\n", 27); 关闭网络(传入连接状态); }
        else { 控制 = 传入连接状态; 活动 = 板经过毫秒(); 回复("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (控制 < 0) return;
    if ((uint32_t)(板经过毫秒() - 活动) > 60000) { 断开连接(); return; }
    if (!结束程序) for (unsigned 预算 = 0; 预算 < 256; 预算++) {
        unsigned char 字符代码; int 已返回值 = 网络层读取(控制, &字符代码, 1);
        if (已返回值 == -11) break; if (已返回值 <= 0) { 断开连接(); return; } 活动 = 板经过毫秒();
        if (字符代码 == '\n') { if (行错误) 回复("500 Command too long or invalid\r\n"); else 命令(); 行大小 = 行错误 = 0; if (结束程序) break; }
        else if (字符代码 != '\r') { if (!字符代码 || 行大小 >= sizeof(行) - 1) 行错误 = 1; else 行[行大小++] = 字符代码; }
    }
    if (手册连接状态 >= 0 && 数据 < 0) {
        int 已返回值 = 网络层接受(手册连接状态);
        if (已返回值 >= 0) {
            if (网络层对端地址(已返回值) != 网络层对端地址(控制)) 关闭网络(已返回值);
            else { 数据 = 已返回值; 关闭网络(手册连接状态); 手册连接状态 = -1; 活动 = 板经过毫秒(); }
        }
    }
    if (执行中任务 == 1 && 数据 >= 0) for (unsigned 预算 = 0; 预算 < 8; 预算++) {
        unsigned char 数据块[512]; int 项目个数 = 网络层读取(数据, 数据块, sizeof(数据块));
        if (项目个数 == -11) break;
        if (项目个数 < 0) { 停止传送(); 回复("426 Data connection failed\r\n"); break; }
        活动 = 板经过毫秒();
        if (项目个数 == 0) {
            int 结果 = -1;
            if (!拥有失败) {
                int 文件句柄 = pk_open(传送名称, 写入仅用值 | 创建条件缺失 | 截断内容, 0600);
                if (文件句柄 >= 0) { 结果 = pk_write(文件句柄, 传送状态, 已使用容量); pk_close(文件句柄); }
            }
            int 是否已成功 = !拥有失败 && 结果 == (int)已使用容量; 停止传送(); 回复(是否已成功 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)项目个数 > sizeof(传送状态) - 已使用容量) 拥有失败 = 1;
        if (!拥有失败) { memcpy(传送状态 + 已使用容量, 数据块, 项目个数); 已使用容量 += 项目个数; }
    }
    if (执行中任务 == 2 && 数据 >= 0) {
        int 项目个数 = 网络层写入(数据, 传送状态 + 已发送个数, 已使用容量 - 已发送个数);
        if (项目个数 >= 0) { 已发送个数 += 项目个数; 活动 = 板经过毫秒(); if (已发送个数 == 已使用容量) { 停止传送(); 回复("226 Transfer complete\r\n"); } }
        else if (项目个数 != -11) { 停止传送(); 回复("426 Data connection failed\r\n"); }
    }
    if (回复已发送 < 回复大小) {
        int 项目个数 = 网络层写入(控制, 回复列 + 回复已发送, 回复大小 - 回复已发送);
        if (项目个数 > 0) 回复已发送 += 项目个数; else if (项目个数 != -11) { 断开连接(); return; }
    }
    if (回复已发送 == 回复大小) { 回复大小 = 回复已发送 = 0; if (结束程序) 断开连接(); }
}
