/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "遠程值.h"
#include "密碼學支持.h"
#include "配置檔.h"
#include "../通信網絡/通信網絡.h"
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
extern uintptr_t 板經過毫秒(void);
extern uintptr_t 板寫字符(uintptr_t);
static struct assh_context_s *上下文值;
static struct assh_session_s *接通狀態;
static struct assh_channel_s *信道條目;
static int 偵聽中端點=-1,對端值=-1,是否已認證,命令殼已開始,命令類型,結束狀態=-1,將要關閉,啓動錯誤,命令殼等待中;
static uintptr_t 連接狀態時間,重新連接時間,關閉中時間;
static unsigned char 輸入行[8192],輸出行[65536];
static unsigned 輸入頭,輸入個數,輸出頭,輸出個數,上一個輸出;
static void 診斷值(const char *機器字文本,unsigned 值) {
    while(*機器字文本)板寫字符(*機器字文本++);
    char 數字值[12];unsigned 數=0;do{數字值[數++]='0'+值%10;值/=10;}while(值);
    while(數)板寫字符(數字值[--數]);板寫字符(10);
}
static assh_status_t 準備記憶體(void *資料,void **地址,size_t 大小,enum assh_alloc_type_e 種類值) {
    (void)資料;(void)種類值;
    if(!大小){釋放遠程(*地址);*地址=0;return ASSH_OK;}
    void *新建地址=重新分配遠程(*地址,大小);
    if(!新建地址)return ASSH_ERR_MEM;*地址=新建地址;return ASSH_OK;
}
static assh_status_t 準備隨機(struct assh_context_s *資料,const struct assh_buffer_s *種子值) {
    (void)資料;(void)種子值;unsigned char 測試[32];int 結果=遠程隨機(測試,sizeof(測試));memset(測試,0,sizeof(測試));
    return 結果?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 讀取隨機(struct assh_context_s *資料,uint8_t *結果,size_t 長度,uint_fast8_t 種類值) {
    (void)資料;(void)種類值;if(長度>65536)return ASSH_ERR_CRYPTO;
    return 遠程隨機(結果,長度)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 隨機結束(struct assh_context_s *資料){(void)資料;}
static const struct assh_prng_s 隨機生成器={準備隨機,讀取隨機,隨機結束};
static void 關閉連接狀態(void) {
    是否已認證=命令殼已開始=0;信道條目=0;
    if(接通狀態)assh_session_release(接通狀態);接通狀態=0;
    if(對端值>=0)關閉網路(對端值);對端值=-1;命令類型=0;結束狀態=-1;將要關閉=0;
    輸入頭=輸入個數=輸出頭=輸出個數=上一個輸出=0;重新連接時間=板經過毫秒()+250;
}
int 供給遠程輸入(const unsigned char *資料,unsigned 數) {
    if(數>sizeof(輸入行)-輸入個數)return -11;
    for(unsigned 序數索引=0;序數索引<數;序數索引++)輸入行[(輸入頭+輸入個數++)%sizeof(輸入行)]=資料[序數索引];return 數;
}
int 遠程輸入(void) {
    if(!輸入個數)return -1;int 字元值=輸入行[輸入頭];輸入頭=(輸入頭+1)%sizeof(輸入行);輸入個數--;return 字元值;
}
void 遠程輸出(unsigned char 字元值) {
    if(!命令殼已開始||將要關閉)return;
    unsigned 追加模式=字元值==10&&上一個輸出!=13;
    if(輸出個數+1+追加模式>sizeof(輸出行)){將要關閉=2;return;}
    if(追加模式)輸出行[(輸出頭+輸出個數++)%sizeof(輸出行)]=13;
    輸出行[(輸出頭+輸出個數++)%sizeof(輸出行)]=字元值;上一個輸出=字元值;
}
uintptr_t 板結束遠程命令(uintptr_t 狀態值){if(命令殼已開始&&命令類型)結束狀態=(int)狀態值;return 0;}
uintptr_t 板遠程等待狀態(uintptr_t 狀態值){命令殼等待中=狀態值!=0;return 0;}
static int 準備命令殼(void) {
    if(偵聽中端點>=0)return 0;
    if(!上下文值){
        assh_status_t 錯誤=assh_context_create(&上下文值,ASSH_SERVER,準備記憶體,0,&隨機生成器,0);
        if(錯誤)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *方法模式[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        錯誤=assh_algo_register(上下文值,ASSH_SAFETY_WEAK,方法模式);
        if(!錯誤)錯誤=assh_service_register_va(上下文值,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *鍵材料=設備鍵;
        if(!錯誤)錯誤=assh_key_load(上下文值,assh_context_keys(上下文值),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&鍵材料,sizeof(設備鍵));
        if(錯誤){診斷值("SSH init error ",錯誤);assh_context_release(上下文值);上下文值=0;return -5;}
    }
    int 埠值=創建通訊端端點(1);if(埠值<0)return 埠值;複用通訊端地址(埠值);
    int 結果=網路層綁定(埠值,0,22);if(!結果)結果=網路層偵聽(埠值);
    if(結果<0){關閉網路(埠值);return 結果;}偵聽中端點=埠值;return 0;
}
uintptr_t 板遠程控制(uintptr_t 種類值,uintptr_t 動作) {
    if(種類值==1)return(uint32_t)控制遠程顯示操作(動作);
    if(動作==0){關閉連接狀態();if(偵聽中端點>=0)關閉網路(偵聽中端點);偵聽中端點=-1;return 0;}
    if(動作==1){啓動錯誤=準備命令殼();return(uint32_t)啓動錯誤;}
    return(uint32_t)(偵聽中端點>=0?1:啓動錯誤);
}
void 準備遠程(void){啓動錯誤=準備命令殼();控制遠程顯示操作(1);}
static int 匹配中機器字(const struct assh_cbuffer_s *資料,const char *機器字文本) {
    size_t 長度=strlen(機器字文本);return 資料->size==長度&&!memcmp(資料->data,機器字文本,長度);
}
static int 終端申請(const struct assh_cbuffer_s *資料) {
    if(資料->size<24)return 0;
    const unsigned char *資料位置=資料->data;unsigned 長度=assh_load_u32(資料位置);
    if(長度>128||資料->size<長度+24)return 0;
    unsigned 模式值=assh_load_u32(資料位置+4+長度+16);
    return 模式值<=2048&&資料->size==長度+24+模式值;
}
static void 句柄申請(struct assh_event_request_s *事件) {
    if(!是否已認證||事件->ch!=信道條目||!信道條目)return;
    if(匹配中機器字(&事件->type,"pty-req")) {
        if(!命令殼已開始&&終端申請(&事件->rq_data))事件->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(匹配中機器字(&事件->type,"window-change")) {
        if(命令殼已開始&&事件->rq_data.size==16)事件->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(命令殼已開始||!命令殼等待中)return;
    const unsigned char *命令=0;unsigned 長度=0;
    if(匹配中機器字(&事件->type,"exec")) {
        if(事件->rq_data.size<4)return;
        長度=assh_load_u32(事件->rq_data.data);
        if(!長度||長度>2048||事件->rq_data.size!=長度+4)return;
        命令=事件->rq_data.data+4;
        for(unsigned 序數索引=0;序數索引<長度;序數索引++)if(!命令[序數索引])return;
        命令類型=1;
    }else if(!匹配中機器字(&事件->type,"shell")||事件->rq_data.size)return;
    if(sizeof(輸入行)-輸入個數<長度+2)return;
    const unsigned char 已擦除值=21,結尾=13;
    供給遠程輸入(&已擦除值,1);if(長度)供給遠程輸入(命令,長度);供給遠程輸入(&結尾,1);
    命令殼已開始=1;事件->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!命令類型){const char *指南="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*指南)遠程輸出(*指南++);}
}
void 審查遠程(void) {
    審查遠程顯示操作();
    if(偵聽中端點<0)return;
    uintptr_t 當前時刻值=板經過毫秒();
    if(對端值<0){if(當前時刻值<重新連接時間)return;對端值=網路層接受(偵聽中端點);if(對端值<0)return;
        連接狀態時間=當前時刻值;assh_status_t 錯誤=assh_session_create(上下文值,&接通狀態);
        if(錯誤){接通狀態=0;診斷值("SSH session error ",錯誤);關閉連接狀態();return;}}
    if((!是否已認證&&當前時刻值-連接狀態時間>30000)||將要關閉==2||(將要關閉&&當前時刻值>=關閉中時間)){關閉連接狀態();return;}
    if(信道條目&&命令殼已開始&&!將要關閉) {
        if(輸出個數){size_t 數=sizeof(輸出行)-輸出頭;if(數>輸出個數)數=輸出個數;if(數>2048)數=2048;
            assh_status_t 錯誤=assh_channel_data(信道條目,輸出行+輸出頭,&數);
            if(!錯誤){輸出頭=(輸出頭+數)%sizeof(輸出行);輸出個數-=數;}
            else if(錯誤!=ASSH_NO_DATA){關閉連接狀態();return;}
        }
        if(結束狀態>=0&&!輸出個數){unsigned char 狀態值[4];assh_store_u32(狀態值,(uint32_t)結束狀態);
            if(assh_request(接通狀態,信道條目,"exit-status",11,狀態值,4,0)||assh_channel_eof(信道條目)||assh_channel_close(信道條目)) {關閉連接狀態();return;}
            將要關閉=1;關閉中時間=當前時刻值+3000;
        }
    }
    for(unsigned 序列值=0;序列值<16;序列值++) {
        struct assh_event_s 事件;
        if(!assh_event_get(接通狀態,&事件,當前時刻值/1000)){關閉連接狀態();return;}
        assh_status_t 錯誤=ASSH_OK;int 剩餘部分短暫地=0,斷開連接端點=0;
        switch(事件.id) {
        case ASSH_EVENT_READ: {
            int 數=網路層讀取(對端值,事件.transport.read.buf.data,事件.transport.read.buf.size);
            if(數>0)事件.transport.read.transferred=數;
            else if(數==-11)剩餘部分短暫地=1;else 斷開連接端點=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 數=網路層寫入(對端值,事件.transport.write.buf.data,事件.transport.write.buf.size);
            if(數>0)事件.transport.write.transferred=數;
            else if(數==-11)剩餘部分短暫地=1;else 斷開連接端點=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            事件.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(事件.userauth_server.methods.retries>3)事件.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *資料=&事件.userauth_server.password;
            if(匹配中機器字(&資料->username,"user")&&資料->password.size<=256&&!資料->new_password.size) {
                unsigned char 摘要值[32];遠程摘要(資料->password.data,資料->password.size,摘要值);
                unsigned 差異值=0;for(unsigned 序數索引=0;序數索引<32;序數索引++)差異值|=摘要值[序數索引]^命令殼密碼摘要[序數索引];memset(摘要值,0,32);
                if(!差異值)資料->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 是否已認證=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *資料=&事件.connection.channel_open;
            if(是否已認證&&!信道條目&&命令殼等待中&&匹配中機器字(&資料->type,"session")&&!資料->rq_data.size) {
                資料->reply=ASSH_CONNECTION_REPLY_SUCCESS;資料->pkt_size=4096;
                資料->win_size=-1;信道條目=資料->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 句柄申請(&事件.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *資料=&事件.connection.channel_data;
            if(!命令殼已開始||資料->ch!=信道條目||資料->ext){斷開連接端點=1;break;}
            unsigned 數=資料->data.size;if(數>sizeof(輸入行)-輸入個數)數=sizeof(輸入行)-輸入個數;
            for(unsigned 序數索引=0;序數索引<數;序數索引++)if(資料->data.data[序數索引]==4){結束狀態=0;數=序數索引;資料->transferred=資料->data.size;break;}
            供給遠程輸入(資料->data.data,數);if(!資料->transferred)資料->transferred=數;
            if(!數&&結束狀態<0)剩餘部分短暫地=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: 信道條目=0;命令殼已開始=0;將要關閉=1;關閉中時間=當前時刻值+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 是否已認證=命令殼已開始=0;診斷值("SSH error ",事件.session.error.code);斷開連接端點=1;break;
        case ASSH_EVENT_DISCONNECT: 斷開連接端點=1;break;
        default: break;
        }
        assh_event_done(接通狀態,&事件,錯誤);
        if(斷開連接端點){關閉連接狀態();return;}if(剩餘部分短暫地)return;
    }
}
