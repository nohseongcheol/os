/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "بعيد_قدر.h"
#include "암호기반.h"
#include "پروفائيل.h"
#include "../نيٽ_ورڪ_اڀرڻ/نيٽ_ورڪ_اڀرڻ.h"
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
static struct assh_context_s *مفهوم_قدر;
static struct assh_session_s *ڪنيڪشن_e05f319b;
static struct assh_channel_s *چينل_داخلا;
static int 듣는곳=-1,همعصر_قدر=-1,인증됨,셸시작됨,حڪم_قسم,ختم_ڪريو_حالت=-1,닫을예정,شروعات_نقص,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *ورڊ_متن,unsigned قدر) {
    while(*ورڊ_متن)보드글자쓰기(*ورڊ_متن++);
    char ڊجٽ_قدر[12];unsigned 수=0;do{ڊجٽ_قدر[수++]='0'+قدر%10;قدر/=10;}while(قدر);
    while(수)보드글자쓰기(ڊجٽ_قدر[--수]);보드글자쓰기(10);
}
static assh_status_t تياري_ڪريو_ميموري(void *ڪوائف,void **پتو,size_t سائيز,enum assh_alloc_type_e 종류) {
    (void)ڪوائف;(void)종류;
    if(!سائيز){جاري_ڪريو_بعيد(*پتو);*پتو=0;return ASSH_OK;}
    void *새주소=원격재할당(*پتو,سائيز);
    if(!새주소)return ASSH_ERR_MEM;*پتو=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ڪوائف,const struct assh_buffer_s *ٻج_قدر) {
    (void)ڪوائف;(void)ٻج_قدر;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ڪوائف,uint8_t *결과,size_t لمبائي_قدر,uint_fast8_t 종류) {
    (void)ڪوائف;(void)종류;if(لمبائي_قدر>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,لمبائي_قدر)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ڪوائف){(void)ڪوائف;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void بند_ڪرڻ_ڪنيڪشن(void) {
    인증됨=셸시작됨=0;چينل_داخلا=0;
    if(ڪنيڪشن_e05f319b)assh_session_release(ڪنيڪشن_e05f319b);ڪنيڪشن_e05f319b=0;
    if(همعصر_قدر>=0)بند_ڪرڻ_نيٽ_ورڪ(همعصر_قدر);همعصر_قدر=-1;حڪم_قسم=0;ختم_ڪريو_حالت=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ڪوائف,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=ڪوائف[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int ڪريڪٽر_قدر=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return ڪريڪٽر_قدر;
}
void 원격출력(unsigned char ڪريڪٽر_قدر) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=ڪريڪٽر_قدر==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=ڪريڪٽر_قدر;이전출력=ڪريڪٽر_قدر;
}
uintptr_t 보드원격명령끝(uintptr_t حالت_قدر){if(셸시작됨&&حڪم_قسم)ختم_ڪريو_حالت=(int)حالت_قدر;return 0;}
uintptr_t 보드원격대기(uintptr_t حالت_قدر){셸대기중=حالت_قدر!=0;return 0;}
static int تياري_ڪريو_شيل(void) {
    if(듣는곳>=0)return 0;
    if(!مفهوم_قدر){
        assh_status_t نقص=assh_context_create(&مفهوم_قدر,ASSH_SERVER,تياري_ڪريو_ميموري,0,&난수기,0);
        if(نقص)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *طريقو_موڊ[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        نقص=assh_algo_register(مفهوم_قدر,ASSH_SAFETY_WEAK,طريقو_موڊ);
        if(!نقص)نقص=assh_service_register_va(مفهوم_قدر,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=آلو_ڪليد;
        if(!نقص)نقص=assh_key_load(مفهوم_قدر,assh_context_keys(مفهوم_قدر),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(آلو_ڪليد));
        if(نقص){진단("SSH init error ",نقص);assh_context_release(مفهوم_قدر);مفهوم_قدر=0;return -5;}
    }
    int پورٽ_قدر=통신끝점만들기(1);if(پورٽ_قدر<0)return پورٽ_قدر;통신주소재사용(پورٽ_قدر);
    int 결과=망주소묶기(پورٽ_قدر,0,22);if(!결과)결과=연결기다리기(پورٽ_قدر);
    if(결과<0){بند_ڪرڻ_نيٽ_ورڪ(پورٽ_قدر);return 결과;}듣는곳=پورٽ_قدر;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t عمل) {
    if(종류==1)return(uint32_t)ڪنٽرول_بعيد_ڊسپلي(عمل);
    if(عمل==0){بند_ڪرڻ_ڪنيڪشن();if(듣는곳>=0)بند_ڪرڻ_نيٽ_ورڪ(듣는곳);듣는곳=-1;return 0;}
    if(عمل==1){شروعات_نقص=تياري_ڪريو_شيل();return(uint32_t)شروعات_نقص;}
    return(uint32_t)(듣는곳>=0?1:شروعات_نقص);
}
void تياري_ڪريو_بعيد(void){شروعات_نقص=تياري_ڪريو_شيل();ڪنٽرول_بعيد_ڊسپلي(1);}
static int 같은말(const struct assh_cbuffer_s *ڪوائف,const char *ورڊ_متن) {
    size_t لمبائي_قدر=strlen(ورڊ_متن);return ڪوائف->size==لمبائي_قدر&&!memcmp(ڪوائف->data,ورڊ_متن,لمبائي_قدر);
}
static int 터미널요청(const struct assh_cbuffer_s *ڪوائف) {
    if(ڪوائف->size<24)return 0;
    const unsigned char *자료위치=ڪوائف->data;unsigned لمبائي_قدر=assh_load_u32(자료위치);
    if(لمبائي_قدر>128||ڪوائف->size<لمبائي_قدر+24)return 0;
    unsigned موڊ_قدر=assh_load_u32(자료위치+4+لمبائي_قدر+16);
    return موڊ_قدر<=2048&&ڪوائف->size==لمبائي_قدر+24+موڊ_قدر;
}
static void 요청처리(struct assh_event_request_s *واقعو) {
    if(!인증됨||واقعو->ch!=چينل_داخلا||!چينل_داخلا)return;
    if(같은말(&واقعو->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&واقعو->rq_data))واقعو->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&واقعو->type,"window-change")) {
        if(셸시작됨&&واقعو->rq_data.size==16)واقعو->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *حڪم=0;unsigned لمبائي_قدر=0;
    if(같은말(&واقعو->type,"exec")) {
        if(واقعو->rq_data.size<4)return;
        لمبائي_قدر=assh_load_u32(واقعو->rq_data.data);
        if(!لمبائي_قدر||لمبائي_قدر>2048||واقعو->rq_data.size!=لمبائي_قدر+4)return;
        حڪم=واقعو->rq_data.data+4;
        for(unsigned 순번=0;순번<لمبائي_قدر;순번++)if(!حڪم[순번])return;
        حڪم_قسم=1;
    }else if(!같은말(&واقعو->type,"shell")||واقعو->rq_data.size)return;
    if(sizeof(입력줄)-입력수<لمبائي_قدر+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(لمبائي_قدر)원격입력넣기(حڪم,لمبائي_قدر);원격입력넣기(&끝,1);
    셸시작됨=1;واقعو->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!حڪم_قسم){const char *پڙهو_فائل_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*پڙهو_فائل_eb81d7d9)원격출력(*پڙهو_فائل_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(همعصر_قدر<0){if(지금<재접속시각)return;همعصر_قدر=망연결받기(듣는곳);if(همعصر_قدر<0)return;
        접속시각=지금;assh_status_t نقص=assh_session_create(مفهوم_قدر,&ڪنيڪشن_e05f319b);
        if(نقص){ڪنيڪشن_e05f319b=0;진단("SSH session error ",نقص);بند_ڪرڻ_ڪنيڪشن();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){بند_ڪرڻ_ڪنيڪشن();return;}
    if(چينل_داخلا&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t نقص=assh_channel_data(چينل_داخلا,출력줄+출력앞,&수);
            if(!نقص){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(نقص!=ASSH_NO_DATA){بند_ڪرڻ_ڪنيڪشن();return;}
        }
        if(ختم_ڪريو_حالت>=0&&!출력수){unsigned char حالت_قدر[4];assh_store_u32(حالت_قدر,(uint32_t)ختم_ڪريو_حالت);
            if(assh_request(ڪنيڪشن_e05f319b,چينل_داخلا,"exit-status",11,حالت_قدر,4,0)||assh_channel_eof(چينل_داخلا)||assh_channel_close(چينل_داخلا)) {بند_ڪرڻ_ڪنيڪشن();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned ترتيب_قدر_e9fa7815=0;ترتيب_قدر_e9fa7815<16;ترتيب_قدر_e9fa7815++) {
        struct assh_event_s واقعو;
        if(!assh_event_get(ڪنيڪشن_e05f319b,&واقعو,지금/1000)){بند_ڪرڻ_ڪنيڪشن();return;}
        assh_status_t نقص=ASSH_OK;int 쉬기=0,끊기=0;
        switch(واقعو.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(همعصر_قدر,واقعو.transport.read.buf.data,واقعو.transport.read.buf.size);
            if(수>0)واقعو.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(همعصر_قدر,واقعو.transport.write.buf.data,واقعو.transport.write.buf.size);
            if(수>0)واقعو.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            واقعو.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(واقعو.userauth_server.methods.retries>3)واقعو.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ڪوائف=&واقعو.userauth_server.password;
            if(같은말(&ڪوائف->username,"user")&&ڪوائف->password.size<=256&&!ڪوائف->new_password.size) {
                unsigned char 요약[32];원격요약(ڪوائف->password.data,ڪوائف->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)ڪوائف->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ڪوائف=&واقعو.connection.channel_open;
            if(인증됨&&!چينل_داخلا&&셸대기중&&같은말(&ڪوائف->type,"session")&&!ڪوائف->rq_data.size) {
                ڪوائف->reply=ASSH_CONNECTION_REPLY_SUCCESS;ڪوائف->pkt_size=4096;
                ڪوائف->win_size=-1;چينل_داخلا=ڪوائف->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&واقعو.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ڪوائف=&واقعو.connection.channel_data;
            if(!셸시작됨||ڪوائف->ch!=چينل_داخلا||ڪوائف->ext){끊기=1;break;}
            unsigned 수=ڪوائف->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(ڪوائف->data.data[순번]==4){ختم_ڪريو_حالت=0;수=순번;ڪوائف->transferred=ڪوائف->data.size;break;}
            원격입력넣기(ڪوائف->data.data,수);if(!ڪوائف->transferred)ڪوائف->transferred=수;
            if(!수&&ختم_ڪريو_حالت<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: چينل_داخلا=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",واقعو.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(ڪنيڪشن_e05f319b,&واقعو,نقص);
        if(끊기){بند_ڪرڻ_ڪنيڪشن();return;}if(쉬기)return;
    }
}
