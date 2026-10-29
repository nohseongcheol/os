#include "../命名/计算机连接名称列.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "通信网络.h"
extern int32_t Java回环网络套接字(int32_t,int32_t,int32_t), Java回环网络绑定(int32_t,int32_t,int32_t);
extern int32_t Java回环网络发送(int32_t,int32_t,int32_t,int32_t), Java回环网络接收操作(int32_t,int32_t);
extern int32_t Java回环网络端口(int32_t), Java回环网络地址(int32_t), Java回环网络对端(int32_t), Java回环网络关闭(int32_t);
extern int32_t Java网络放入(int32_t,int32_t),Java网络获取(int32_t);
extern int32_t Java回环流创建(void),Java回环流绑定(int32_t,int32_t,int32_t),Java回环流侦听(int32_t,int32_t);
extern int32_t Java回环流连接(int32_t,int32_t,int32_t),Java回环流接受(int32_t),Java回环流读取(int32_t,int32_t),Java回环流写入(int32_t,int32_t);
extern int32_t Java回环流端口(int32_t),Java回环流对端(int32_t),Java回环流关闭(int32_t);
static int 外部[24];
static int 任意地址[24], 双重侦听器[24], UDP外部对端[8], 已绑定地址[8];
static int 外部编号(int 文件句柄) { return 文件句柄>=32 && 文件句柄<56 ? 外部[文件句柄-32]-1 : -1; }
static int 粘贴文本(int 文件句柄,int 类型分类) {
    if(文件句柄<32||文件句柄>=56)return -9;int 上一个项目=外部编号(文件句柄);if(上一个项目>=0)return 上一个项目;
    int 项目个数=创建套接字端点(类型分类);if(项目个数>=0)外部[文件句柄-32]=项目个数+1;return 项目个数;
}
int32_t Java网络套接字(int32_t 首位值,int32_t 第二值,int32_t 字符代码){return Java回环网络套接字(首位值,第二值,字符代码);}
int32_t Java网络绑定(int32_t 文件句柄,int32_t 互联网地址,int32_t 端口编号){
    if(互联网地址==0x7f000001)return Java回环网络绑定(文件句柄,互联网地址,端口编号);
    if(互联网地址!=0&&互联网地址!=读取网络运行状态(0,0))return -99;
    int 已返回值=Java回环网络绑定(文件句柄,0,端口编号);if(已返回值<0)return 已返回值;
    int 项目个数=粘贴文本(文件句柄,2);if(项目个数<0)return 项目个数;已返回值=网络层绑定(项目个数,读取网络运行状态(0,0),Java回环网络端口(文件句柄));if(!已返回值)已绑定地址[文件句柄-32]=互联网地址;return 已返回值;
}
int32_t Java网络发送(int32_t 文件句柄,int32_t 互联网地址,int32_t 端口编号,int32_t 大小){
    if(互联网地址==0x7f000001)return Java回环网络发送(文件句柄,互联网地址,端口编号,大小);
    if(大小<0||大小>512)return -90;if(端口编号<1||端口编号>65535)return -22;
    if(Java回环网络端口(文件句柄)<0)return -9;
    if(Java回环网络地址(文件句柄)==0x7f000001)return -101;
    int 项目个数=外部编号(文件句柄);if(项目个数<0){int 已返回值=0;if(Java回环网络端口(文件句柄)==0)已返回值=Java回环网络绑定(文件句柄,0,0);if(已返回值<0)return 已返回值;项目个数=粘贴文本(文件句柄,2);if(项目个数<0)return 项目个数;已返回值=网络层绑定(项目个数,读取网络运行状态(0,0),Java回环网络端口(文件句柄));if(已返回值<0)return 已返回值;}
    unsigned char 数据[512];for(int 序数索引=0;序数索引<大小;序数索引++)数据[序数索引]=Java网络获取(序数索引);return 发送数据报(项目个数,数据,大小,互联网地址,端口编号);
}
int32_t Java网络接收操作(int32_t 文件句柄,int32_t 大小){
    int 项目个数=外部编号(文件句柄);if(项目个数<0)return Java回环网络接收操作(文件句柄,大小);if(大小<0||大小>512)return -22;
    int 局部=Java回环网络接收操作(文件句柄,大小);if(局部!=-11){UDP外部对端[文件句柄-32]=0;return 局部;}
    unsigned char 数据[512];int 已返回值=接收数据报(项目个数,数据,大小);if(已返回值>=0)UDP外部对端[文件句柄-32]=1;for(int 序数索引=0;序数索引<已返回值;序数索引++)Java网络放入(序数索引,数据[序数索引]);return 已返回值;
}
int32_t Java网络端口(int32_t 文件句柄){int 项目个数=外部编号(文件句柄);return 项目个数<0?Java回环网络端口(文件句柄):(int32_t)网络端口编号(项目个数);}
int32_t Java网络地址(int32_t 文件句柄){return 外部编号(文件句柄)<0?Java回环网络地址(文件句柄):已绑定地址[文件句柄-32];}
int32_t Java网络对端(int32_t 文件句柄){int 项目个数=外部编号(文件句柄);return 项目个数<0||!UDP外部对端[文件句柄-32]?Java回环网络对端(文件句柄):(int32_t)对端端口编号(项目个数);}
int32_t Java网络远程(int32_t 文件句柄){int 项目个数=外部编号(文件句柄);return 项目个数<0||!UDP外部对端[文件句柄-32]?0x7f000001:(int32_t)网络层对端地址(项目个数);}
int32_t Java网络关闭(int32_t 文件句柄){int 项目个数=外部编号(文件句柄);if(项目个数>=0){关闭网络(项目个数);外部[文件句柄-32]=0;}if(文件句柄>=32&&文件句柄<40)UDP外部对端[文件句柄-32]=已绑定地址[文件句柄-32]=0;return Java回环网络关闭(文件句柄);}
int32_t Java流创建(void){return Java回环流创建();}
int32_t Java流绑定(int32_t 文件句柄,int32_t 互联网地址,int32_t 端口编号){
    if(互联网地址==0||互联网地址==0x7f000001){int 已返回值=Java回环流绑定(文件句柄,互联网地址,端口编号);if(!已返回值)任意地址[文件句柄-32]=互联网地址==0;return 已返回值;}
    if(互联网地址!=读取网络运行状态(0,0))return -99;int 已返回值=Java回环流绑定(文件句柄,0,端口编号);if(已返回值<0)return 已返回值;
    int 项目个数=粘贴文本(文件句柄,1);return 项目个数<0?项目个数:网络层绑定(项目个数,互联网地址,Java回环流端口(文件句柄));
}
int32_t Java流侦听(int32_t 文件句柄,int32_t 待接队列长度){
    int 项目个数=外部编号(文件句柄);if(项目个数<0){int 已返回值=Java回环流侦听(文件句柄,待接队列长度);if(已返回值<0||!任意地址[文件句柄-32])return 已返回值;
        项目个数=粘贴文本(文件句柄,1);if(项目个数<0)return 项目个数;已返回值=网络层绑定(项目个数,读取网络运行状态(0,0),Java回环流端口(文件句柄));if(已返回值<0)return 已返回值;双重侦听器[文件句柄-32]=1;
    }return 待接队列长度<1?-22:网络层侦听(项目个数);
}
int32_t Java流连接(int32_t 文件句柄,int32_t 互联网地址,int32_t 端口编号){
    if(互联网地址==0x7f000001 && 外部编号(文件句柄)<0)return Java回环流连接(文件句柄,互联网地址,端口编号);
    if(Java回环流端口(文件句柄)<0)return -9;int 项目个数=粘贴文本(文件句柄,1);return 项目个数<0?项目个数:网络层连接(项目个数,互联网地址,端口编号);
}
int32_t Java流接受(int32_t 文件句柄){
    int 项目个数=外部编号(文件句柄);if(项目个数<0)return Java回环流接受(文件句柄);
    if(双重侦听器[文件句柄-32]){int 局部=Java回环流接受(文件句柄);if(局部!=-11)return 局部;}
    int 对端值=网络层接受(项目个数);if(对端值<0)return 对端值;
    int 目标值=Java回环流创建();if(目标值<0){关闭网络(对端值);return 目标值;}外部[目标值-32]=对端值+1;return 目标值;
}
int32_t Java流读取(int32_t 文件句柄,int32_t 大小){
    int 项目个数=外部编号(文件句柄);if(项目个数<0)return Java回环流读取(文件句柄,大小);if(大小<0||大小>512)return -22;
    unsigned char 数据[512];int 已返回值=网络层读取(项目个数,数据,大小);for(int 序数索引=0;序数索引<已返回值;序数索引++)Java网络放入(序数索引,数据[序数索引]);return 已返回值;
}
int32_t Java流写入(int32_t 文件句柄,int32_t 大小){
    int 项目个数=外部编号(文件句柄);if(项目个数<0)return Java回环流写入(文件句柄,大小);if(大小<0||大小>512)return -22;
    unsigned char 数据[512];for(int 序数索引=0;序数索引<大小;序数索引++)数据[序数索引]=Java网络获取(序数索引);return 网络层写入(项目个数,数据,大小);
}
int32_t Java流端口(int32_t 文件句柄){int 项目个数=外部编号(文件句柄);return 项目个数<0?Java回环流端口(文件句柄):(int32_t)网络端口编号(项目个数);}
int32_t Java流对端(int32_t 文件句柄){int 项目个数=外部编号(文件句柄);return 项目个数<0?Java回环流对端(文件句柄):(int32_t)对端端口编号(项目个数);}
int32_t Java流地址(int32_t 文件句柄){return 外部编号(文件句柄)<0?0x7f000001:双重侦听器[文件句柄-32]?0:读取网络运行状态(0,0);}
int32_t Java流关闭(int32_t 文件句柄){int 项目个数=外部编号(文件句柄);if(项目个数>=0){关闭网络(项目个数);外部[文件句柄-32]=0;}if(文件句柄>=40&&文件句柄<56)任意地址[文件句柄-32]=双重侦听器[文件句柄-32]=0;return Java回环流关闭(文件句柄);}
