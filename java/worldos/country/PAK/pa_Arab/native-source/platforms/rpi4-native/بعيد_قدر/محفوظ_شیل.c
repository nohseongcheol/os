/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "بعيد_قدر.h"
#include "암호기반.h"
#include "پروفائل.h"
#include "../نیٹ_ورک_گٹھا/نیٹ_ورک_گٹھا.h"
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
extern uintptr_t 보드밀리초(void);
extern uintptr_t 보드글자쓰기(uintptr_t);
static struct assh_context_s *سیاق_قدر;
static struct assh_session_s *کنکشن_e05f319b;
static struct assh_channel_s *چینل_داخلہ;
static int 듣는곳=-1,ہم_سر_قدر=-1,인증됨,셸시작됨,حکم_ٹائپ_کرو,ختم_کرو_حالت=-1,닫을예정,آغاز_نقص,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *لفظ_متن,unsigned قدر) {
    while(*لفظ_متن)보드글자쓰기(*لفظ_متن++);
    char عدد_قدر[12];unsigned 수=0;do{عدد_قدر[수++]='0'+قدر%10;قدر/=10;}while(قدر);
    while(수)보드글자쓰기(عدد_قدر[--수]);보드글자쓰기(10);
}
static assh_status_t تیاری_کرو_میموری(void *کوائف,void **پتا,size_t سائز,enum assh_alloc_type_e 종류) {
    (void)کوائف;(void)종류;
    if(!سائز){اجراء_بعيد(*پتا);*پتا=0;return ASSH_OK;}
    void *새주소=원격재할당(*پتا,سائز);
    if(!새주소)return ASSH_ERR_MEM;*پتا=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *کوائف,const struct assh_buffer_s *نقلی_قدر) {
    (void)کوائف;(void)نقلی_قدر;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *کوائف,uint8_t *결과,size_t لمبائی_قدر,uint_fast8_t 종류) {
    (void)کوائف;(void)종류;if(لمبائی_قدر>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,لمبائی_قدر)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *کوائف){(void)کوائف;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void بند_کرو_کنکشن(void) {
    인증됨=셸시작됨=0;چینل_داخلہ=0;
    if(کنکشن_e05f319b)assh_session_release(کنکشن_e05f319b);کنکشن_e05f319b=0;
    if(ہم_سر_قدر>=0)بند_کرو_نیٹ_ورک(ہم_سر_قدر);ہم_سر_قدر=-1;حکم_ٹائپ_کرو=0;ختم_کرو_حالت=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *کوائف,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=کوائف[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int کریکٹر_قدر=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return کریکٹر_قدر;
}
void 원격출력(unsigned char کریکٹر_قدر) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=کریکٹر_قدر==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=کریکٹر_قدر;이전출력=کریکٹر_قدر;
}
uintptr_t 보드원격명령끝(uintptr_t حالت_قدر){if(셸시작됨&&حکم_ٹائپ_کرو)ختم_کرو_حالت=(int)حالت_قدر;return 0;}
uintptr_t 보드원격대기(uintptr_t حالت_قدر){셸대기중=حالت_قدر!=0;return 0;}
static int تیاری_کرو_شیل(void) {
    if(듣는곳>=0)return 0;
    if(!سیاق_قدر){
        assh_status_t نقص=assh_context_create(&سیاق_قدر,ASSH_SERVER,تیاری_کرو_میموری,0,&난수기,0);
        if(نقص)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *طریقہ_موڈ[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        نقص=assh_algo_register(سیاق_قدر,ASSH_SAFETY_WEAK,طریقہ_موڈ);
        if(!نقص)نقص=assh_service_register_va(سیاق_قدر,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=آلہ_کلید;
        if(!نقص)نقص=assh_key_load(سیاق_قدر,assh_context_keys(سیاق_قدر),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(آلہ_کلید));
        if(نقص){진단("SSH init error ",نقص);assh_context_release(سیاق_قدر);سیاق_قدر=0;return -5;}
    }
    int دہانہ_قدر=통신끝점만들기(1);if(دہانہ_قدر<0)return دہانہ_قدر;통신주소재사용(دہانہ_قدر);
    int 결과=망주소묶기(دہانہ_قدر,0,22);if(!결과)결과=연결기다리기(دہانہ_قدر);
    if(결과<0){بند_کرو_نیٹ_ورک(دہانہ_قدر);return 결과;}듣는곳=دہانہ_قدر;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t کم) {
    if(종류==1)return(uint32_t)کنٹرول_بعيد_ڈسپلے(کم);
    if(کم==0){بند_کرو_کنکشن();if(듣는곳>=0)بند_کرو_نیٹ_ورک(듣는곳);듣는곳=-1;return 0;}
    if(کم==1){آغاز_نقص=تیاری_کرو_شیل();return(uint32_t)آغاز_نقص;}
    return(uint32_t)(듣는곳>=0?1:آغاز_نقص);
}
void تیاری_کرو_بعيد(void){آغاز_نقص=تیاری_کرو_شیل();کنٹرول_بعيد_ڈسپلے(1);}
static int 같은말(const struct assh_cbuffer_s *کوائف,const char *لفظ_متن) {
    size_t لمبائی_قدر=strlen(لفظ_متن);return کوائف->size==لمبائی_قدر&&!memcmp(کوائف->data,لفظ_متن,لمبائی_قدر);
}
static int 터미널요청(const struct assh_cbuffer_s *کوائف) {
    if(کوائف->size<24)return 0;
    const unsigned char *자료위치=کوائف->data;unsigned لمبائی_قدر=assh_load_u32(자료위치);
    if(لمبائی_قدر>128||کوائف->size<لمبائی_قدر+24)return 0;
    unsigned موڈ_قدر=assh_load_u32(자료위치+4+لمبائی_قدر+16);
    return موڈ_قدر<=2048&&کوائف->size==لمبائی_قدر+24+موڈ_قدر;
}
static void 요청처리(struct assh_event_request_s *واقعہ) {
    if(!인증됨||واقعہ->ch!=چینل_داخلہ||!چینل_داخلہ)return;
    if(같은말(&واقعہ->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&واقعہ->rq_data))واقعہ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&واقعہ->type,"window-change")) {
        if(셸시작됨&&واقعہ->rq_data.size==16)واقعہ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *حکم=0;unsigned لمبائی_قدر=0;
    if(같은말(&واقعہ->type,"exec")) {
        if(واقعہ->rq_data.size<4)return;
        لمبائی_قدر=assh_load_u32(واقعہ->rq_data.data);
        if(!لمبائی_قدر||لمبائی_قدر>2048||واقعہ->rq_data.size!=لمبائی_قدر+4)return;
        حکم=واقعہ->rq_data.data+4;
        for(unsigned 순번=0;순번<لمبائی_قدر;순번++)if(!حکم[순번])return;
        حکم_ٹائپ_کرو=1;
    }else if(!같은말(&واقعہ->type,"shell")||واقعہ->rq_data.size)return;
    if(sizeof(입력줄)-입력수<لمبائی_قدر+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(لمبائی_قدر)원격입력넣기(حکم,لمبائی_قدر);원격입력넣기(&끝,1);
    셸시작됨=1;واقعہ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!حکم_ٹائپ_کرو){const char *فائل_مینوں_پڑھو_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*فائل_مینوں_پڑھو_eb81d7d9)원격출력(*فائل_مینوں_پڑھو_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(ہم_سر_قدر<0){if(지금<재접속시각)return;ہم_سر_قدر=망연결받기(듣는곳);if(ہم_سر_قدر<0)return;
        접속시각=지금;assh_status_t نقص=assh_session_create(سیاق_قدر,&کنکشن_e05f319b);
        if(نقص){کنکشن_e05f319b=0;진단("SSH session error ",نقص);بند_کرو_کنکشن();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){بند_کرو_کنکشن();return;}
    if(چینل_داخلہ&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t نقص=assh_channel_data(چینل_داخلہ,출력줄+출력앞,&수);
            if(!نقص){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(نقص!=ASSH_NO_DATA){بند_کرو_کنکشن();return;}
        }
        if(ختم_کرو_حالت>=0&&!출력수){unsigned char حالت_قدر[4];assh_store_u32(حالت_قدر,(uint32_t)ختم_کرو_حالت);
            if(assh_request(کنکشن_e05f319b,چینل_داخلہ,"exit-status",11,حالت_قدر,4,0)||assh_channel_eof(چینل_داخلہ)||assh_channel_close(چینل_داخلہ)) {بند_کرو_کنکشن();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s واقعہ;
        if(!assh_event_get(کنکشن_e05f319b,&واقعہ,지금/1000)){بند_کرو_کنکشن();return;}
        assh_status_t نقص=ASSH_OK;int 쉬기=0,끊기=0;
        switch(واقعہ.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(ہم_سر_قدر,واقعہ.transport.read.buf.data,واقعہ.transport.read.buf.size);
            if(수>0)واقعہ.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(ہم_سر_قدر,واقعہ.transport.write.buf.data,واقعہ.transport.write.buf.size);
            if(수>0)واقعہ.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            واقعہ.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(واقعہ.userauth_server.methods.retries>3)واقعہ.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *کوائف=&واقعہ.userauth_server.password;
            if(같은말(&کوائف->username,"user")&&کوائف->password.size<=256&&!کوائف->new_password.size) {
                unsigned char 요약[32];원격요약(کوائف->password.data,کوائف->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)کوائف->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *کوائف=&واقعہ.connection.channel_open;
            if(인증됨&&!چینل_داخلہ&&셸대기중&&같은말(&کوائف->type,"session")&&!کوائف->rq_data.size) {
                کوائف->reply=ASSH_CONNECTION_REPLY_SUCCESS;کوائف->pkt_size=4096;
                کوائف->win_size=-1;چینل_داخلہ=کوائف->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&واقعہ.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *کوائف=&واقعہ.connection.channel_data;
            if(!셸시작됨||کوائف->ch!=چینل_داخلہ||کوائف->ext){끊기=1;break;}
            unsigned 수=کوائف->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(کوائف->data.data[순번]==4){ختم_کرو_حالت=0;수=순번;کوائف->transferred=کوائف->data.size;break;}
            원격입력넣기(کوائف->data.data,수);if(!کوائف->transferred)کوائف->transferred=수;
            if(!수&&ختم_کرو_حالت<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: چینل_داخلہ=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",واقعہ.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(کنکشن_e05f319b,&واقعہ,نقص);
        if(끊기){بند_کرو_کنکشن();return;}if(쉬기)return;
    }
}
