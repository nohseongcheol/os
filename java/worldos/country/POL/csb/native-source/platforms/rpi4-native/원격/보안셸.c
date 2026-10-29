/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "원격.h"
#include "암호기반.h"
#include "접속설정.h"
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
static struct assh_session_s *접속;
static struct assh_channel_s *통로;
static int 듣는곳=-1,상대=-1,인증됨,셸시작됨,명령형,끝상태=-1,닫을예정,시작오류,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *말,unsigned 값) {
    while(*말)보드글자쓰기(*말++);
    char 숫자[12];unsigned 수=0;do{숫자[수++]='0'+값%10;값/=10;}while(값);
    while(수)보드글자쓰기(숫자[--수]);보드글자쓰기(10);
}
static assh_status_t 기억마련(void *자료,void **주소,size_t 크기,enum assh_alloc_type_e 종류) {
    (void)자료;(void)종류;
    if(!크기){원격해제(*주소);*주소=0;return ASSH_OK;}
    void *새주소=원격재할당(*주소,크기);
    if(!새주소)return ASSH_ERR_MEM;*주소=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *자료,const struct assh_buffer_s *씨앗) {
    (void)자료;(void)씨앗;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *자료,uint8_t *결과,size_t 길이,uint_fast8_t 종류) {
    (void)자료;(void)종류;if(길이>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,길이)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *자료){(void)자료;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void 연결닫기(void) {
    인증됨=셸시작됨=0;통로=0;
    if(접속)assh_session_release(접속);접속=0;
    if(상대>=0)통신닫기(상대);상대=-1;명령형=0;끝상태=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *자료,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=자료[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int 글자=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return 글자;
}
void 원격출력(unsigned char 글자) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=글자==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=글자;이전출력=글자;
}
uintptr_t 보드원격명령끝(uintptr_t 상태){if(셸시작됨&&명령형)끝상태=(int)상태;return 0;}
uintptr_t 보드원격대기(uintptr_t 상태){셸대기중=상태!=0;return 0;}
static int 셸준비(void) {
    if(듣는곳>=0)return 0;
    if(!문맥){
        assh_status_t Fela=assh_context_create(&문맥,ASSH_SERVER,기억마련,0,&난수기,0);
        if(Fela)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *방식[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Fela=assh_algo_register(문맥,ASSH_SAFETY_WEAK,방식);
        if(!Fela)Fela=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=장치열쇠;
        if(!Fela)Fela=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(장치열쇠));
        if(Fela){진단("SSH init error ",Fela);assh_context_release(문맥);문맥=0;return -5;}
    }
    int 창구=통신끝점만들기(1);if(창구<0)return 창구;통신주소재사용(창구);
    int 결과=망주소묶기(창구,0,22);if(!결과)결과=연결기다리기(창구);
    if(결과<0){통신닫기(창구);return 결과;}듣는곳=창구;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t Dzejanié) {
    if(종류==1)return(uint32_t)원격화면제어(Dzejanié);
    if(Dzejanié==0){연결닫기();if(듣는곳>=0)통신닫기(듣는곳);듣는곳=-1;return 0;}
    if(Dzejanié==1){시작오류=셸준비();return(uint32_t)시작오류;}
    return(uint32_t)(듣는곳>=0?1:시작오류);
}
void 원격준비(void){시작오류=셸준비();원격화면제어(1);}
static int 같은말(const struct assh_cbuffer_s *자료,const char *말) {
    size_t 길이=strlen(말);return 자료->size==길이&&!memcmp(자료->data,말,길이);
}
static int 터미널요청(const struct assh_cbuffer_s *자료) {
    if(자료->size<24)return 0;
    const unsigned char *자료위치=자료->data;unsigned 길이=assh_load_u32(자료위치);
    if(길이>128||자료->size<길이+24)return 0;
    unsigned 모드=assh_load_u32(자료위치+4+길이+16);
    return 모드<=2048&&자료->size==길이+24+모드;
}
static void 요청처리(struct assh_event_request_s *사건) {
    if(!인증됨||사건->ch!=통로||!통로)return;
    if(같은말(&사건->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&사건->rq_data))사건->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&사건->type,"window-change")) {
        if(셸시작됨&&사건->rq_data.size==16)사건->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *Pòlét=0;unsigned 길이=0;
    if(같은말(&사건->type,"exec")) {
        if(사건->rq_data.size<4)return;
        길이=assh_load_u32(사건->rq_data.data);
        if(!길이||길이>2048||사건->rq_data.size!=길이+4)return;
        Pòlét=사건->rq_data.data+4;
        for(unsigned 순번=0;순번<길이;순번++)if(!Pòlét[순번])return;
        명령형=1;
    }else if(!같은말(&사건->type,"shell")||사건->rq_data.size)return;
    if(sizeof(입력줄)-입력수<길이+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(길이)원격입력넣기(Pòlét,길이);원격입력넣기(&끝,1);
    셸시작됨=1;사건->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!명령형){const char *안내="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*안내)원격출력(*안내++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(상대<0){if(지금<재접속시각)return;상대=망연결받기(듣는곳);if(상대<0)return;
        접속시각=지금;assh_status_t Fela=assh_session_create(문맥,&접속);
        if(Fela){접속=0;진단("SSH session error ",Fela);연결닫기();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){연결닫기();return;}
    if(통로&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Fela=assh_channel_data(통로,출력줄+출력앞,&수);
            if(!Fela){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Fela!=ASSH_NO_DATA){연결닫기();return;}
        }
        if(끝상태>=0&&!출력수){unsigned char 상태[4];assh_store_u32(상태,(uint32_t)끝상태);
            if(assh_request(접속,통로,"exit-status",11,상태,4,0)||assh_channel_eof(통로)||assh_channel_close(통로)) {연결닫기();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s 사건;
        if(!assh_event_get(접속,&사건,지금/1000)){연결닫기();return;}
        assh_status_t Fela=ASSH_OK;int 쉬기=0,끊기=0;
        switch(사건.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(상대,사건.transport.read.buf.data,사건.transport.read.buf.size);
            if(수>0)사건.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(상대,사건.transport.write.buf.data,사건.transport.write.buf.size);
            if(수>0)사건.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            사건.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(사건.userauth_server.methods.retries>3)사건.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *자료=&사건.userauth_server.password;
            if(같은말(&자료->username,"user")&&자료->password.size<=256&&!자료->new_password.size) {
                unsigned char 요약[32];원격요약(자료->password.data,자료->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)자료->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *자료=&사건.connection.channel_open;
            if(인증됨&&!통로&&셸대기중&&같은말(&자료->type,"session")&&!자료->rq_data.size) {
                자료->reply=ASSH_CONNECTION_REPLY_SUCCESS;자료->pkt_size=4096;
                자료->win_size=-1;통로=자료->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&사건.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *자료=&사건.connection.channel_data;
            if(!셸시작됨||자료->ch!=통로||자료->ext){끊기=1;break;}
            unsigned 수=자료->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(자료->data.data[순번]==4){끝상태=0;수=순번;자료->transferred=자료->data.size;break;}
            원격입력넣기(자료->data.data,수);if(!자료->transferred)자료->transferred=수;
            if(!수&&끝상태<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: 통로=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",사건.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(접속,&사건,Fela);
        if(끊기){연결닫기();return;}if(쉬기)return;
    }
}
