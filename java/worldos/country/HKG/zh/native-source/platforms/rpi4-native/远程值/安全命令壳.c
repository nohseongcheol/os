/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "远程值.h"
#include "密码学支持.h"
#include "配置档.h"
#include "../通信网络/通信网络.h"
/* The allocator/PRNG module descriptors are part of this pinned port's ABI. */
#define ASSH_PV
#include <assh/assh_session.h>
#include <assh/assh_context.h>
#include <assh/assh_service.h>
#include <assh/assh_transport.h>
#include <assh/assh_userauth_server.h>
#include <assh/assh_connection.h>
#include <assh/assh_kex.h>
#include <assh/assh_key.h>
#include <assh/assh_sign.h>
#include <assh/assh_cipher.h>
#include <assh/assh_mac.h>
#include <assh/assh_compress.h>
#include <assh/assh_alloc.h>
#include <assh/assh_prng.h>
#include <assh/mod_builtin.h>
#include <assh/assh_event.h>
#include <string.h>
extern uintptr_t 板经过毫秒(void);
extern uintptr_t 板写字符(uintptr_t);
static struct assh_context_s *上下文值;
static struct assh_session_s *接通状态;
static struct assh_channel_s *信道条目;
static int 侦听中端点=-1,对端值=-1,是否已认证,命令壳已开始,命令类型,结束状态=-1,将要关闭,启动错误,命令壳等待中;
static uintptr_t 连接状态时间,重新连接时间,关闭中时间;
static unsigned char 输入行[8192],输出行[65536];
static unsigned 输入头,输入个数,输出头,输出个数,上一个输出;
static void 诊断值(const char *机器字文本,unsigned 值) {
    while(*机器字文本)板写字符(*机器字文本++);
    char 数字值[12];unsigned 数=0;do{数字值[数++]='0'+值%10;值/=10;}while(值);
    while(数)板写字符(数字值[--数]);板写字符(10);
}
static assh_status_t 准备内存(void *数据,void **地址,size_t 大小,enum assh_alloc_type_e 种类值) {
    (void)数据;(void)种类值;
    if(!大小){释放远程(*地址);*地址=0;return ASSH_OK;}
    void *新建地址=重新分配远程(*地址,大小);
    if(!新建地址)return ASSH_ERR_MEM;*地址=新建地址;return ASSH_OK;
}
static assh_status_t 准备随机(struct assh_context_s *数据,const struct assh_buffer_s *种子值) {
    (void)数据;(void)种子值;unsigned char 测试[32];int 结果=远程随机(测试,sizeof(测试));memset(测试,0,sizeof(测试));
    return 结果?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 读取随机(struct assh_context_s *数据,uint8_t *结果,size_t 长度,uint_fast8_t 种类值) {
    (void)数据;(void)种类值;if(长度>65536)return ASSH_ERR_CRYPTO;
    return 远程随机(结果,长度)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 随机结束(struct assh_context_s *数据){(void)数据;}
static const struct assh_prng_s 随机生成器={准备随机,读取随机,随机结束};
static void 关闭连接状态(void) {
    是否已认证=命令壳已开始=0;信道条目=0;
    if(接通状态)assh_session_release(接通状态);接通状态=0;
    if(对端值>=0)关闭网络(对端值);对端值=-1;命令类型=0;结束状态=-1;将要关闭=0;
    输入头=输入个数=输出头=输出个数=上一个输出=0;重新连接时间=板经过毫秒()+250;
}
int 供给远程输入(const unsigned char *数据,unsigned 数) {
    if(数>sizeof(输入行)-输入个数)return -11;
    for(unsigned 序数索引=0;序数索引<数;序数索引++)输入行[(输入头+输入个数++)%sizeof(输入行)]=数据[序数索引];return 数;
}
int 远程输入(void) {
    if(!输入个数)return -1;int 字符值=输入行[输入头];输入头=(输入头+1)%sizeof(输入行);输入个数--;return 字符值;
}
void 远程输出(unsigned char 字符值) {
    if(!命令壳已开始||将要关闭)return;
    unsigned 追加模式=字符值==10&&上一个输出!=13;
    if(输出个数+1+追加模式>sizeof(输出行)){将要关闭=2;return;}
    if(追加模式)输出行[(输出头+输出个数++)%sizeof(输出行)]=13;
    输出行[(输出头+输出个数++)%sizeof(输出行)]=字符值;上一个输出=字符值;
}
uintptr_t 板结束远程命令(uintptr_t 状态值){if(命令壳已开始&&命令类型)结束状态=(int)状态值;return 0;}
uintptr_t 板远程等待状态(uintptr_t 状态值){命令壳等待中=状态值!=0;return 0;}
static int 准备命令壳(void) {
    if(侦听中端点>=0)return 0;
    if(!上下文值){
        assh_status_t 错误=assh_context_create(&上下文值,ASSH_SERVER,准备内存,0,&随机生成器,0);
        if(错误)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *方法模式[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        错误=assh_algo_register(上下文值,ASSH_SAFETY_WEAK,方法模式);
        if(!错误)错误=assh_service_register_va(上下文值,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *键材料=设备键;
        if(!错误)错误=assh_key_load(上下文值,assh_context_keys(上下文值),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&键材料,sizeof(设备键));
        if(错误){诊断值("SSH init error ",错误);assh_context_release(上下文值);上下文值=0;return -5;}
    }
    int 端口值=创建套接字端点(1);if(端口值<0)return 端口值;复用套接字地址(端口值);
    int 结果=网络层绑定(端口值,0,22);if(!结果)结果=网络层侦听(端口值);
    if(结果<0){关闭网络(端口值);return 结果;}侦听中端点=端口值;return 0;
}
uintptr_t 板远程控制(uintptr_t 种类值,uintptr_t 动作) {
    if(种类值==1)return(uint32_t)控制远程显示操作(动作);
    if(动作==0){关闭连接状态();if(侦听中端点>=0)关闭网络(侦听中端点);侦听中端点=-1;return 0;}
    if(动作==1){启动错误=准备命令壳();return(uint32_t)启动错误;}
    return(uint32_t)(侦听中端点>=0?1:启动错误);
}
void 准备远程(void){启动错误=准备命令壳();控制远程显示操作(1);}
static int 匹配中机器字(const struct assh_cbuffer_s *数据,const char *机器字文本) {
    size_t 长度=strlen(机器字文本);return 数据->size==长度&&!memcmp(数据->data,机器字文本,长度);
}
static int 终端申请(const struct assh_cbuffer_s *数据) {
    if(数据->size<24)return 0;
    const unsigned char *数据位置=数据->data;unsigned 长度=assh_load_u32(数据位置);
    if(长度>128||数据->size<长度+24)return 0;
    unsigned 模式值=assh_load_u32(数据位置+4+长度+16);
    return 模式值<=2048&&数据->size==长度+24+模式值;
}
static void 句柄申请(struct assh_event_request_s *事件) {
    if(!是否已认证||事件->ch!=信道条目||!信道条目)return;
    if(匹配中机器字(&事件->type,"pty-req")) {
        if(!命令壳已开始&&终端申请(&事件->rq_data))事件->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(匹配中机器字(&事件->type,"window-change")) {
        if(命令壳已开始&&事件->rq_data.size==16)事件->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(命令壳已开始||!命令壳等待中)return;
    const unsigned char *命令=0;unsigned 长度=0;
    if(匹配中机器字(&事件->type,"exec")) {
        if(事件->rq_data.size<4)return;
        长度=assh_load_u32(事件->rq_data.data);
        if(!长度||长度>2048||事件->rq_data.size!=长度+4)return;
        命令=事件->rq_data.data+4;
        for(unsigned 序数索引=0;序数索引<长度;序数索引++)if(!命令[序数索引])return;
        命令类型=1;
    }else if(!匹配中机器字(&事件->type,"shell")||事件->rq_data.size)return;
    if(sizeof(输入行)-输入个数<长度+2)return;
    const unsigned char 已擦除值=21,结尾=13;
    供给远程输入(&已擦除值,1);if(长度)供给远程输入(命令,长度);供给远程输入(&结尾,1);
    命令壳已开始=1;事件->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!命令类型){const char *指南="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*指南)远程输出(*指南++);}
}
void 审查远程(void) {
    审查远程显示操作();
    if(侦听中端点<0)return;
    uintptr_t 当前时刻值=板经过毫秒();
    if(对端值<0){if(当前时刻值<重新连接时间)return;对端值=网络层接受(侦听中端点);if(对端值<0)return;
        连接状态时间=当前时刻值;assh_status_t 错误=assh_session_create(上下文值,&接通状态);
        if(错误){接通状态=0;诊断值("SSH session error ",错误);关闭连接状态();return;}}
    if((!是否已认证&&当前时刻值-连接状态时间>30000)||将要关闭==2||(将要关闭&&当前时刻值>=关闭中时间)){关闭连接状态();return;}
    if(信道条目&&命令壳已开始&&!将要关闭) {
        if(输出个数){size_t 数=sizeof(输出行)-输出头;if(数>输出个数)数=输出个数;if(数>2048)数=2048;
            assh_status_t 错误=assh_channel_data(信道条目,输出行+输出头,&数);
            if(!错误){输出头=(输出头+数)%sizeof(输出行);输出个数-=数;}
            else if(错误!=ASSH_NO_DATA){关闭连接状态();return;}
        }
        if(结束状态>=0&&!输出个数){unsigned char 状态值[4];assh_store_u32(状态值,(uint32_t)结束状态);
            if(assh_request(接通状态,信道条目,"exit-status",11,状态值,4,0)||assh_channel_eof(信道条目)||assh_channel_close(信道条目)) {关闭连接状态();return;}
            将要关闭=1;关闭中时间=当前时刻值+3000;
        }
    }
    for(unsigned 序列值=0;序列值<16;序列值++) {
        struct assh_event_s 事件;
        if(!assh_event_get(接通状态,&事件,当前时刻值/1000)){关闭连接状态();return;}
        assh_status_t 错误=ASSH_OK;int 剩余部分短暂地=0,断开连接端点=0;
        switch(事件.id) {
        case ASSH_EVENT_READ: {
            int 数=网络层读取(对端值,事件.transport.read.buf.data,事件.transport.read.buf.size);
            if(数>0)事件.transport.read.transferred=数;
            else if(数==-11)剩余部分短暂地=1;else 断开连接端点=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 数=网络层写入(对端值,事件.transport.write.buf.data,事件.transport.write.buf.size);
            if(数>0)事件.transport.write.transferred=数;
            else if(数==-11)剩余部分短暂地=1;else 断开连接端点=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            事件.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(事件.userauth_server.methods.retries>3)事件.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *数据=&事件.userauth_server.password;
            if(匹配中机器字(&数据->username,"user")&&数据->password.size<=256&&!数据->new_password.size) {
                unsigned char 摘要值[32];远程摘要(数据->password.data,数据->password.size,摘要值);
                unsigned 差异值=0;for(unsigned 序数索引=0;序数索引<32;序数索引++)差异值|=摘要值[序数索引]^命令壳密码摘要[序数索引];memset(摘要值,0,32);
                if(!差异值)数据->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 是否已认证=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *数据=&事件.connection.channel_open;
            if(是否已认证&&!信道条目&&命令壳等待中&&匹配中机器字(&数据->type,"session")&&!数据->rq_data.size) {
                数据->reply=ASSH_CONNECTION_REPLY_SUCCESS;数据->pkt_size=4096;
                数据->win_size=-1;信道条目=数据->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 句柄申请(&事件.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *数据=&事件.connection.channel_data;
            if(!命令壳已开始||数据->ch!=信道条目||数据->ext){断开连接端点=1;break;}
            unsigned 数=数据->data.size;if(数>sizeof(输入行)-输入个数)数=sizeof(输入行)-输入个数;
            for(unsigned 序数索引=0;序数索引<数;序数索引++)if(数据->data.data[序数索引]==4){结束状态=0;数=序数索引;数据->transferred=数据->data.size;break;}
            供给远程输入(数据->data.data,数);if(!数据->transferred)数据->transferred=数;
            if(!数&&结束状态<0)剩余部分短暂地=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: 信道条目=0;命令壳已开始=0;将要关闭=1;关闭中时间=当前时刻值+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 是否已认证=命令壳已开始=0;诊断值("SSH error ",事件.session.error.code);断开连接端点=1;break;
        case ASSH_EVENT_DISCONNECT: 断开连接端点=1;break;
        default: break;
        }
        assh_event_done(接通状态,&事件,错误);
        if(断开连接端点){关闭连接状态();return;}if(剩余部分短暂地)return;
    }
}
