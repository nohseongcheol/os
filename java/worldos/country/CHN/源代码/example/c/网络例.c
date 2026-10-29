#include "示例约定.h"
#include <网络ABI.h>
int main(int 参数个数,char **实参) {
    if(参数个数!=2)return 输出("사용법: ./네트워크 UDP창구번호\n");
    unsigned 端口值=0;for(int 数=0;实参[1][数];数++) {
        if(实参[1][数]<'0'||实参[1][数]>'9')return 2;
        端口值=端口值*10+实参[1][数]-'0';if(端口值>65535)return 2;
    }
    if(!端口值)return 2;
    int 端点=创建端点(互联网族,数据报套接字,数据报协议);if(端点<0)return 3;
    struct 互联网套接字地址 地址={0};地址.地址族=互联网族;
    if(绑定地址(端点,(struct 套接字地址 *)&地址,sizeof(地址))<0)return 4;
    地址.端口编号=网络短整数(端口值);地址.互联网地址.地址值=网络整数(0x0a000202);
    const char 数据报[]="C UDP Chinese";
    if(发送数据报数据(端点,数据报,sizeof(数据报)-1,0,(struct 套接字地址 *)&地址,sizeof(地址))!=sizeof(数据报)-1)return 5;
    char 回复[512];unsigned 运行=毫秒();int 已接收个数;
    do {
        已接收个数=接收数据报数据(端点,回复,sizeof(回复),0,0,0);
        if(已接收个数<0&&错误编号!=尝试执行再次错误)return 6;
    } while(已接收个数<0&&(unsigned)(毫秒()-运行)<700);
    关闭文件(端点);if(已接收个数!=sizeof(数据报)-1)return 7;
    for(int 数=0;数<已接收个数;数++)if(数据报[数]!=回复[数])return 8;
    return 输出("C 네트워크 验证: UDP Chinese\n");
}
