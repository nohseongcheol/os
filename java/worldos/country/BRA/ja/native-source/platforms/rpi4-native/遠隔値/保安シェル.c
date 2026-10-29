/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "遠隔値.h"
#include "暗号学支援.h"
#include "動作設定.h"
#include "../通信網/通信網.h"
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
extern uintptr_t 基板経過ミリ秒(void);
extern uintptr_t 基板文字出力(uintptr_t);
static struct assh_context_s *文脈値;
static struct assh_session_s *接続状態;
static struct assh_channel_s *チャネル入口;
static int 待受中通信端点=-1,通信相手値=-1,判定認証済み,シェル開始済み,命令型,終端位置状況=-1,予定閉鎖,始動エラー,シェル待機中;
static uintptr_t 接続状態時間,再接続時間,閉鎖中時間;
static unsigned char 入力行[8192],出力行[65536];
static unsigned 入力先頭部,入力個数,出力先頭部,出力個数,前回出力;
static void 診断値(const char *語本文,unsigned 値) {
    while(*語本文)基板文字出力(*語本文++);
    char 桁値[12];unsigned 数=0;do{桁値[数++]='0'+値%10;値/=10;}while(値);
    while(数)基板文字出力(桁値[--数]);基板文字出力(10);
}
static assh_status_t 記憶用意(void *データ,void **番地,size_t 容量,enum assh_alloc_type_e 種別値) {
    (void)データ;(void)種別値;
    if(!容量){遠隔解放(*番地);*番地=0;return ASSH_OK;}
    void *新規番地=遠隔再確保(*番地,容量);
    if(!新規番地)return ASSH_ERR_MEM;*番地=新規番地;return ASSH_OK;
}
static assh_status_t 乱数用意(struct assh_context_s *データ,const struct assh_buffer_s *種値) {
    (void)データ;(void)種値;unsigned char 試験[32];int 結果=遠隔乱数(試験,sizeof(試験));memset(試験,0,sizeof(試験));
    return 結果?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 乱数読取(struct assh_context_s *データ,uint8_t *結果,size_t 長さ,uint_fast8_t 種別値) {
    (void)データ;(void)種別値;if(長さ>65536)return ASSH_ERR_CRYPTO;
    return 遠隔乱数(結果,長さ)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 乱数終端位置(struct assh_context_s *データ){(void)データ;}
static const struct assh_prng_s 乱数生成器={乱数用意,乱数読取,乱数終端位置};
static void 接続状態閉鎖(void) {
    判定認証済み=シェル開始済み=0;チャネル入口=0;
    if(接続状態)assh_session_release(接続状態);接続状態=0;
    if(通信相手値>=0)通信網閉鎖(通信相手値);通信相手値=-1;命令型=0;終端位置状況=-1;予定閉鎖=0;
    入力先頭部=入力個数=出力先頭部=出力個数=前回出力=0;再接続時間=基板経過ミリ秒()+250;
}
int 供給遠隔入力(const unsigned char *データ,unsigned 数) {
    if(数>sizeof(入力行)-入力個数)return -11;
    for(unsigned 序数添字=0;序数添字<数;序数添字++)入力行[(入力先頭部+入力個数++)%sizeof(入力行)]=データ[序数添字];return 数;
}
int 遠隔入力(void) {
    if(!入力個数)return -1;int 文字値=入力行[入力先頭部];入力先頭部=(入力先頭部+1)%sizeof(入力行);入力個数--;return 文字値;
}
void 遠隔出力(unsigned char 文字値) {
    if(!シェル開始済み||予定閉鎖)return;
    unsigned 方式追記=文字値==10&&前回出力!=13;
    if(出力個数+1+方式追記>sizeof(出力行)){予定閉鎖=2;return;}
    if(方式追記)出力行[(出力先頭部+出力個数++)%sizeof(出力行)]=13;
    出力行[(出力先頭部+出力個数++)%sizeof(出力行)]=文字値;前回出力=文字値;
}
uintptr_t 基板終端位置遠隔命令(uintptr_t 状況値){if(シェル開始済み&&命令型)終端位置状況=(int)状況値;return 0;}
uintptr_t 基板遠隔待合(uintptr_t 状況値){シェル待機中=状況値!=0;return 0;}
static int シェル用意(void) {
    if(待受中通信端点>=0)return 0;
    if(!文脈値){
        assh_status_t エラー=assh_context_create(&文脈値,ASSH_SERVER,記憶用意,0,&乱数生成器,0);
        if(エラー)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *メソッド方式[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        エラー=assh_algo_register(文脈値,ASSH_SAFETY_WEAK,メソッド方式);
        if(!エラー)エラー=assh_service_register_va(文脈値,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *キー素材=装置キー;
        if(!エラー)エラー=assh_key_load(文脈値,assh_context_keys(文脈値),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&キー素材,sizeof(装置キー));
        if(エラー){診断値("SSH init error ",エラー);assh_context_release(文脈値);文脈値=0;return -5;}
    }
    int ポート値=ソケット通信端点作成(1);if(ポート値<0)return ポート値;再利用ソケット番地(ポート値);
    int 結果=網結合(ポート値,0,22);if(!結果)結果=網接続待機(ポート値);
    if(結果<0){通信網閉鎖(ポート値);return 結果;}待受中通信端点=ポート値;return 0;
}
uintptr_t 基板遠隔制御(uintptr_t 種別値,uintptr_t 動作) {
    if(種別値==1)return(uint32_t)制御遠隔表示処理(動作);
    if(動作==0){接続状態閉鎖();if(待受中通信端点>=0)通信網閉鎖(待受中通信端点);待受中通信端点=-1;return 0;}
    if(動作==1){始動エラー=シェル用意();return(uint32_t)始動エラー;}
    return(uint32_t)(待受中通信端点>=0?1:始動エラー);
}
void 遠隔用意(void){始動エラー=シェル用意();制御遠隔表示処理(1);}
static int 照合中語(const struct assh_cbuffer_s *データ,const char *語本文) {
    size_t 長さ=strlen(語本文);return データ->size==長さ&&!memcmp(データ->data,語本文,長さ);
}
static int 端末要求(const struct assh_cbuffer_s *データ) {
    if(データ->size<24)return 0;
    const unsigned char *データ位置=データ->data;unsigned 長さ=assh_load_u32(データ位置);
    if(長さ>128||データ->size<長さ+24)return 0;
    unsigned 方式値=assh_load_u32(データ位置+4+長さ+16);
    return 方式値<=2048&&データ->size==長さ+24+方式値;
}
static void 取扱い要求(struct assh_event_request_s *イベント) {
    if(!判定認証済み||イベント->ch!=チャネル入口||!チャネル入口)return;
    if(照合中語(&イベント->type,"pty-req")) {
        if(!シェル開始済み&&端末要求(&イベント->rq_data))イベント->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(照合中語(&イベント->type,"window-change")) {
        if(シェル開始済み&&イベント->rq_data.size==16)イベント->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(シェル開始済み||!シェル待機中)return;
    const unsigned char *命令=0;unsigned 長さ=0;
    if(照合中語(&イベント->type,"exec")) {
        if(イベント->rq_data.size<4)return;
        長さ=assh_load_u32(イベント->rq_data.data);
        if(!長さ||長さ>2048||イベント->rq_data.size!=長さ+4)return;
        命令=イベント->rq_data.data+4;
        for(unsigned 序数添字=0;序数添字<長さ;序数添字++)if(!命令[序数添字])return;
        命令型=1;
    }else if(!照合中語(&イベント->type,"shell")||イベント->rq_data.size)return;
    if(sizeof(入力行)-入力個数<長さ+2)return;
    const unsigned char 消去済み値=21,終端=13;
    供給遠隔入力(&消去済み値,1);if(長さ)供給遠隔入力(命令,長さ);供給遠隔入力(&終端,1);
    シェル開始済み=1;イベント->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!命令型){const char *案内="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*案内)遠隔出力(*案内++);}
}
void 遠隔調査(void) {
    遠隔表示処理調査();
    if(待受中通信端点<0)return;
    uintptr_t 現時点値=基板経過ミリ秒();
    if(通信相手値<0){if(現時点値<再接続時間)return;通信相手値=網受理(待受中通信端点);if(通信相手値<0)return;
        接続状態時間=現時点値;assh_status_t エラー=assh_session_create(文脈値,&接続状態);
        if(エラー){接続状態=0;診断値("SSH session error ",エラー);接続状態閉鎖();return;}}
    if((!判定認証済み&&現時点値-接続状態時間>30000)||予定閉鎖==2||(予定閉鎖&&現時点値>=閉鎖中時間)){接続状態閉鎖();return;}
    if(チャネル入口&&シェル開始済み&&!予定閉鎖) {
        if(出力個数){size_t 数=sizeof(出力行)-出力先頭部;if(数>出力個数)数=出力個数;if(数>2048)数=2048;
            assh_status_t エラー=assh_channel_data(チャネル入口,出力行+出力先頭部,&数);
            if(!エラー){出力先頭部=(出力先頭部+数)%sizeof(出力行);出力個数-=数;}
            else if(エラー!=ASSH_NO_DATA){接続状態閉鎖();return;}
        }
        if(終端位置状況>=0&&!出力個数){unsigned char 状況値[4];assh_store_u32(状況値,(uint32_t)終端位置状況);
            if(assh_request(接続状態,チャネル入口,"exit-status",11,状況値,4,0)||assh_channel_eof(チャネル入口)||assh_channel_close(チャネル入口)) {接続状態閉鎖();return;}
            予定閉鎖=1;閉鎖中時間=現時点値+3000;
        }
    }
    for(unsigned 列順値=0;列順値<16;列順値++) {
        struct assh_event_s イベント;
        if(!assh_event_get(接続状態,&イベント,現時点値/1000)){接続状態閉鎖();return;}
        assh_status_t エラー=ASSH_OK;int 残部短時間だけ=0,切断通信端点=0;
        switch(イベント.id) {
        case ASSH_EVENT_READ: {
            int 数=網読取(通信相手値,イベント.transport.read.buf.data,イベント.transport.read.buf.size);
            if(数>0)イベント.transport.read.transferred=数;
            else if(数==-11)残部短時間だけ=1;else 切断通信端点=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 数=網書込(通信相手値,イベント.transport.write.buf.data,イベント.transport.write.buf.size);
            if(数>0)イベント.transport.write.transferred=数;
            else if(数==-11)残部短時間だけ=1;else 切断通信端点=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            イベント.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(イベント.userauth_server.methods.retries>3)イベント.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *データ=&イベント.userauth_server.password;
            if(照合中語(&データ->username,"user")&&データ->password.size<=256&&!データ->new_password.size) {
                unsigned char 要約値[32];遠隔要約(データ->password.data,データ->password.size,要約値);
                unsigned 差分値=0;for(unsigned 序数添字=0;序数添字<32;序数添字++)差分値|=要約値[序数添字]^シェル合言葉要約[序数添字];memset(要約値,0,32);
                if(!差分値)データ->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 判定認証済み=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *データ=&イベント.connection.channel_open;
            if(判定認証済み&&!チャネル入口&&シェル待機中&&照合中語(&データ->type,"session")&&!データ->rq_data.size) {
                データ->reply=ASSH_CONNECTION_REPLY_SUCCESS;データ->pkt_size=4096;
                データ->win_size=-1;チャネル入口=データ->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 取扱い要求(&イベント.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *データ=&イベント.connection.channel_data;
            if(!シェル開始済み||データ->ch!=チャネル入口||データ->ext){切断通信端点=1;break;}
            unsigned 数=データ->data.size;if(数>sizeof(入力行)-入力個数)数=sizeof(入力行)-入力個数;
            for(unsigned 序数添字=0;序数添字<数;序数添字++)if(データ->data.data[序数添字]==4){終端位置状況=0;数=序数添字;データ->transferred=データ->data.size;break;}
            供給遠隔入力(データ->data.data,数);if(!データ->transferred)データ->transferred=数;
            if(!数&&終端位置状況<0)残部短時間だけ=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: チャネル入口=0;シェル開始済み=0;予定閉鎖=1;閉鎖中時間=現時点値+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 判定認証済み=シェル開始済み=0;診断値("SSH error ",イベント.session.error.code);切断通信端点=1;break;
        case ASSH_EVENT_DISCONNECT: 切断通信端点=1;break;
        default: break;
        }
        assh_event_done(接続状態,&イベント,エラー);
        if(切断通信端点){接続状態閉鎖();return;}if(残部短時間だけ)return;
    }
}
