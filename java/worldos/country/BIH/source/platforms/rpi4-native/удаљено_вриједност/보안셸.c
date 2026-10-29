/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "удаљено_вриједност.h"
#include "암호기반.h"
#include "Профил.h"
#include "../통신망/통신망.h"
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
static struct assh_context_s *문맥;
static struct assh_session_s *веза_e05f319b;
static struct assh_channel_s *путања_унос;
static int 듣는곳=-1,peer_вриједност=-1,인증됨,셸시작됨,команда_куцати,завршити_стање=-1,닫을예정,Покренути_грешка,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *말,unsigned вриједност) {
    while(*말)보드글자쓰기(*말++);
    char 숫자[12];unsigned 수=0;do{숫자[수++]='0'+вриједност%10;вриједност/=10;}while(вриједност);
    while(수)보드글자쓰기(숫자[--수]);보드글자쓰기(10);
}
static assh_status_t Припремити_меморија(void *подаци,void **адреса,size_t подесити_величину,enum assh_alloc_type_e 종류) {
    (void)подаци;(void)종류;
    if(!подесити_величину){издање_удаљено(*адреса);*адреса=0;return ASSH_OK;}
    void *새주소=원격재할당(*адреса,подесити_величину);
    if(!새주소)return ASSH_ERR_MEM;*адреса=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *подаци,const struct assh_buffer_s *씨앗) {
    (void)подаци;(void)씨앗;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *подаци,uint8_t *결과,size_t дужина_вриједност,uint_fast8_t 종류) {
    (void)подаци;(void)종류;if(дужина_вриједност>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,дужина_вриједност)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *подаци){(void)подаци;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void затворити_веза(void) {
    인증됨=셸시작됨=0;путања_унос=0;
    if(веза_e05f319b)assh_session_release(веза_e05f319b);веза_e05f319b=0;
    if(peer_вриједност>=0)затворити_Мрежа(peer_вриједност);peer_вриједност=-1;команда_куцати=0;завршити_стање=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *подаци,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=подаци[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int знак_вриједност=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return знак_вриједност;
}
void 원격출력(unsigned char знак_вриједност) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=знак_вриједност==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=знак_вриједност;이전출력=знак_вриједност;
}
uintptr_t 보드원격명령끝(uintptr_t стање_вриједност){if(셸시작됨&&команда_куцати)завршити_стање=(int)стање_вриједност;return 0;}
uintptr_t 보드원격대기(uintptr_t стање_вриједност){셸대기중=стање_вриједност!=0;return 0;}
static int Припремити_љуска(void) {
    if(듣는곳>=0)return 0;
    if(!문맥){
        assh_status_t грешка=assh_context_create(&문맥,ASSH_SERVER,Припремити_меморија,0,&난수기,0);
        if(грешка)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *방식[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        грешка=assh_algo_register(문맥,ASSH_SAFETY_WEAK,방식);
        if(!грешка)грешка=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=уређај_кључ;
        if(!грешка)грешка=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(уређај_кључ));
        if(грешка){진단("SSH init error ",грешка);assh_context_release(문맥);문맥=0;return -5;}
    }
    int порт_вриједност=통신끝점만들기(1);if(порт_вриједност<0)return порт_вриједност;통신주소재사용(порт_вриједност);
    int 결과=망주소묶기(порт_вриједност,0,22);if(!결과)결과=연결기다리기(порт_вриједност);
    if(결과<0){затворити_Мрежа(порт_вриједност);return 결과;}듣는곳=порт_вриједност;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t радња) {
    if(종류==1)return(uint32_t)контрола_удаљено_екран(радња);
    if(радња==0){затворити_веза();if(듣는곳>=0)затворити_Мрежа(듣는곳);듣는곳=-1;return 0;}
    if(радња==1){Покренути_грешка=Припремити_љуска();return(uint32_t)Покренути_грешка;}
    return(uint32_t)(듣는곳>=0?1:Покренути_грешка);
}
void Припремити_удаљено(void){Покренути_грешка=Припремити_љуска();контрола_удаљено_екран(1);}
static int 같은말(const struct assh_cbuffer_s *подаци,const char *말) {
    size_t дужина_вриједност=strlen(말);return подаци->size==дужина_вриједност&&!memcmp(подаци->data,말,дужина_вриједност);
}
static int 터미널요청(const struct assh_cbuffer_s *подаци) {
    if(подаци->size<24)return 0;
    const unsigned char *자료위치=подаци->data;unsigned дужина_вриједност=assh_load_u32(자료위치);
    if(дужина_вриједност>128||подаци->size<дужина_вриједност+24)return 0;
    unsigned мод_вриједност=assh_load_u32(자료위치+4+дужина_вриједност+16);
    return мод_вриједност<=2048&&подаци->size==дужина_вриједност+24+мод_вриједност;
}
static void 요청처리(struct assh_event_request_s *догађај) {
    if(!인증됨||догађај->ch!=путања_унос||!путања_унос)return;
    if(같은말(&догађај->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&догађај->rq_data))догађај->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&догађај->type,"window-change")) {
        if(셸시작됨&&догађај->rq_data.size==16)догађај->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *команда=0;unsigned дужина_вриједност=0;
    if(같은말(&догађај->type,"exec")) {
        if(догађај->rq_data.size<4)return;
        дужина_вриједност=assh_load_u32(догађај->rq_data.data);
        if(!дужина_вриједност||дужина_вриједност>2048||догађај->rq_data.size!=дужина_вриједност+4)return;
        команда=догађај->rq_data.data+4;
        for(unsigned 순번=0;순번<дужина_вриједност;순번++)if(!команда[순번])return;
        команда_куцати=1;
    }else if(!같은말(&догађај->type,"shell")||догађај->rq_data.size)return;
    if(sizeof(입력줄)-입력수<дужина_вриједност+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(дужина_вриједност)원격입력넣기(команда,дужина_вриједност);원격입력넣기(&끝,1);
    셸시작됨=1;догађај->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!команда_куцати){const char *Прочитај_ме_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*Прочитај_ме_eb81d7d9)원격출력(*Прочитај_ме_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(peer_вриједност<0){if(지금<재접속시각)return;peer_вриједност=망연결받기(듣는곳);if(peer_вриједност<0)return;
        접속시각=지금;assh_status_t грешка=assh_session_create(문맥,&веза_e05f319b);
        if(грешка){веза_e05f319b=0;진단("SSH session error ",грешка);затворити_веза();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){затворити_веза();return;}
    if(путања_унос&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t грешка=assh_channel_data(путања_унос,출력줄+출력앞,&수);
            if(!грешка){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(грешка!=ASSH_NO_DATA){затворити_веза();return;}
        }
        if(завршити_стање>=0&&!출력수){unsigned char стање_вриједност[4];assh_store_u32(стање_вриједност,(uint32_t)завршити_стање);
            if(assh_request(веза_e05f319b,путања_унос,"exit-status",11,стање_вриједност,4,0)||assh_channel_eof(путања_унос)||assh_channel_close(путања_унос)) {затворити_веза();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s догађај;
        if(!assh_event_get(веза_e05f319b,&догађај,지금/1000)){затворити_веза();return;}
        assh_status_t грешка=ASSH_OK;int 쉬기=0,끊기=0;
        switch(догађај.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(peer_вриједност,догађај.transport.read.buf.data,догађај.transport.read.buf.size);
            if(수>0)догађај.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(peer_вриједност,догађај.transport.write.buf.data,догађај.transport.write.buf.size);
            if(수>0)догађај.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            догађај.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(догађај.userauth_server.methods.retries>3)догађај.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *подаци=&догађај.userauth_server.password;
            if(같은말(&подаци->username,"user")&&подаци->password.size<=256&&!подаци->new_password.size) {
                unsigned char резиме_вриједност[32];удаљено_резиме(подаци->password.data,подаци->password.size,резиме_вриједност);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=резиме_вриједност[순번]^љуска_лозинка_резиме[순번];memset(резиме_вриједност,0,32);
                if(!차이)подаци->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *подаци=&догађај.connection.channel_open;
            if(인증됨&&!путања_унос&&셸대기중&&같은말(&подаци->type,"session")&&!подаци->rq_data.size) {
                подаци->reply=ASSH_CONNECTION_REPLY_SUCCESS;подаци->pkt_size=4096;
                подаци->win_size=-1;путања_унос=подаци->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&догађај.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *подаци=&догађај.connection.channel_data;
            if(!셸시작됨||подаци->ch!=путања_унос||подаци->ext){끊기=1;break;}
            unsigned 수=подаци->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(подаци->data.data[순번]==4){завршити_стање=0;수=순번;подаци->transferred=подаци->data.size;break;}
            원격입력넣기(подаци->data.data,수);if(!подаци->transferred)подаци->transferred=수;
            if(!수&&завршити_стање<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: путања_унос=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",догађај.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(веза_e05f319b,&догађај,грешка);
        if(끊기){затворити_веза();return;}if(쉬기)return;
    }
}
