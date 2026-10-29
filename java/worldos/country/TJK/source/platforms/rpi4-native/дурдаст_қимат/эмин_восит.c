/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "дурдаст_қимат.h"
#include "암호기반.h"
#include "Профил.h"
#include "../Шабака_ҷамъ/Шабака_ҷамъ.h"
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
static struct assh_context_s *Контекст_қимат;
static struct assh_session_s *пайваст_e05f319b;
static struct assh_channel_s *канал_ворида;
static int 듣는곳=-1,ҳамсон_қимат=-1,인증됨,셸시작됨,фармон_навъ,анҷом_додан_вазъият=-1,닫을예정,оғози_кор_хато,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Калимабозӣ_Матн,unsigned қимат) {
    while(*Калимабозӣ_Матн)보드글자쓰기(*Калимабозӣ_Матн++);
    char рақам_қимат[12];unsigned 수=0;do{рақам_қимат[수++]='0'+қимат%10;қимат/=10;}while(қимат);
    while(수)보드글자쓰기(рақам_қимат[--수]);보드글자쓰기(10);
}
static assh_status_t Омода_кардан_ҳофиза(void *иттилоот,void **суроға,size_t андоза_кардан,enum assh_alloc_type_e 종류) {
    (void)иттилоот;(void)종류;
    if(!андоза_кардан){нашр_дурдаст(*суроға);*суроға=0;return ASSH_OK;}
    void *새주소=원격재할당(*суроға,андоза_кардан);
    if(!새주소)return ASSH_ERR_MEM;*суроға=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *иттилоот,const struct assh_buffer_s *тухм_қимат) {
    (void)иттилоот;(void)тухм_қимат;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *иттилоот,uint8_t *결과,size_t дарозӣ_қимат,uint_fast8_t 종류) {
    (void)иттилоот;(void)종류;if(дарозӣ_қимат>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,дарозӣ_қимат)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *иттилоот){(void)иттилоот;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void пӯшидан_пайваст(void) {
    인증됨=셸시작됨=0;канал_ворида=0;
    if(пайваст_e05f319b)assh_session_release(пайваст_e05f319b);пайваст_e05f319b=0;
    if(ҳамсон_қимат>=0)пӯшидан_Шабака(ҳамсон_қимат);ҳамсон_қимат=-1;фармон_навъ=0;анҷом_додан_вазъият=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *иттилоот,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=иттилоот[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int аломат_қимат_068c2631=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return аломат_қимат_068c2631;
}
void 원격출력(unsigned char аломат_қимат_068c2631) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=аломат_қимат_068c2631==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=аломат_қимат_068c2631;이전출력=аломат_қимат_068c2631;
}
uintptr_t 보드원격명령끝(uintptr_t вазъият_қимат){if(셸시작됨&&фармон_навъ)анҷом_додан_вазъият=(int)вазъият_қимат;return 0;}
uintptr_t 보드원격대기(uintptr_t вазъият_қимат){셸대기중=вазъият_қимат!=0;return 0;}
static int Омода_кардан_восит(void) {
    if(듣는곳>=0)return 0;
    if(!Контекст_қимат){
        assh_status_t Хато=assh_context_create(&Контекст_қимат,ASSH_SERVER,Омода_кардан_ҳофиза,0,&난수기,0);
        if(Хато)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *сабк_ҳолат[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Хато=assh_algo_register(Контекст_қимат,ASSH_SAFETY_WEAK,сабк_ҳолат);
        if(!Хато)Хато=assh_service_register_va(Контекст_қимат,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=мобилӣ_калид;
        if(!Хато)Хато=assh_key_load(Контекст_қимат,assh_context_keys(Контекст_қимат),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(мобилӣ_калид));
        if(Хато){진단("SSH init error ",Хато);assh_context_release(Контекст_қимат);Контекст_қимат=0;return -5;}
    }
    int порт_қимат=통신끝점만들기(1);if(порт_қимат<0)return порт_қимат;통신주소재사용(порт_қимат);
    int 결과=망주소묶기(порт_қимат,0,22);if(!결과)결과=연결기다리기(порт_қимат);
    if(결과<0){пӯшидан_Шабака(порт_қимат);return 결과;}듣는곳=порт_қимат;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t Амал) {
    if(종류==1)return(uint32_t)идоракунӣ_дурдаст_дисплей(Амал);
    if(Амал==0){пӯшидан_пайваст();if(듣는곳>=0)пӯшидан_Шабака(듣는곳);듣는곳=-1;return 0;}
    if(Амал==1){оғози_кор_хато=Омода_кардан_восит();return(uint32_t)оғози_кор_хато;}
    return(uint32_t)(듣는곳>=0?1:оғози_кор_хато);
}
void Омода_кардан_дурдаст(void){оғози_кор_хато=Омода_кардан_восит();идоракунӣ_дурдаст_дисплей(1);}
static int 같은말(const struct assh_cbuffer_s *иттилоот,const char *Калимабозӣ_Матн) {
    size_t дарозӣ_қимат=strlen(Калимабозӣ_Матн);return иттилоот->size==дарозӣ_қимат&&!memcmp(иттилоот->data,Калимабозӣ_Матн,дарозӣ_қимат);
}
static int 터미널요청(const struct assh_cbuffer_s *иттилоот) {
    if(иттилоот->size<24)return 0;
    const unsigned char *자료위치=иттилоот->data;unsigned дарозӣ_қимат=assh_load_u32(자료위치);
    if(дарозӣ_қимат>128||иттилоот->size<дарозӣ_қимат+24)return 0;
    unsigned ҳолат_қимат_a83655ea=assh_load_u32(자료위치+4+дарозӣ_қимат+16);
    return ҳолат_қимат_a83655ea<=2048&&иттилоот->size==дарозӣ_қимат+24+ҳолат_қимат_a83655ea;
}
static void 요청처리(struct assh_event_request_s *рӯйдод) {
    if(!인증됨||рӯйдод->ch!=канал_ворида||!канал_ворида)return;
    if(같은말(&рӯйдод->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&рӯйдод->rq_data))рӯйдод->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&рӯйдод->type,"window-change")) {
        if(셸시작됨&&рӯйдод->rq_data.size==16)рӯйдод->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *фармон=0;unsigned дарозӣ_қимат=0;
    if(같은말(&рӯйдод->type,"exec")) {
        if(рӯйдод->rq_data.size<4)return;
        дарозӣ_қимат=assh_load_u32(рӯйдод->rq_data.data);
        if(!дарозӣ_қимат||дарозӣ_қимат>2048||рӯйдод->rq_data.size!=дарозӣ_қимат+4)return;
        фармон=рӯйдод->rq_data.data+4;
        for(unsigned 순번=0;순번<дарозӣ_қимат;순번++)if(!фармон[순번])return;
        фармон_навъ=1;
    }else if(!같은말(&рӯйдод->type,"shell")||рӯйдод->rq_data.size)return;
    if(sizeof(입력줄)-입력수<дарозӣ_қимат+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(дарозӣ_қимат)원격입력넣기(фармон,дарозӣ_қимат);원격입력넣기(&끝,1);
    셸시작됨=1;рӯйдод->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!фармон_навъ){const char *файли_тафсилот_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*файли_тафсилот_eb81d7d9)원격출력(*файли_тафсилот_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(ҳамсон_қимат<0){if(지금<재접속시각)return;ҳамсон_қимат=망연결받기(듣는곳);if(ҳамсон_қимат<0)return;
        접속시각=지금;assh_status_t Хато=assh_session_create(Контекст_қимат,&пайваст_e05f319b);
        if(Хато){пайваст_e05f319b=0;진단("SSH session error ",Хато);пӯшидан_пайваст();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){пӯшидан_пайваст();return;}
    if(канал_ворида&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Хато=assh_channel_data(канал_ворида,출력줄+출력앞,&수);
            if(!Хато){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Хато!=ASSH_NO_DATA){пӯшидан_пайваст();return;}
        }
        if(анҷом_додан_вазъият>=0&&!출력수){unsigned char вазъият_қимат[4];assh_store_u32(вазъият_қимат,(uint32_t)анҷом_додан_вазъият);
            if(assh_request(пайваст_e05f319b,канал_ворида,"exit-status",11,вазъият_қимат,4,0)||assh_channel_eof(канал_ворида)||assh_channel_close(канал_ворида)) {пӯшидан_пайваст();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s рӯйдод;
        if(!assh_event_get(пайваст_e05f319b,&рӯйдод,지금/1000)){пӯшидан_пайваст();return;}
        assh_status_t Хато=ASSH_OK;int 쉬기=0,끊기=0;
        switch(рӯйдод.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(ҳамсон_қимат,рӯйдод.transport.read.buf.data,рӯйдод.transport.read.buf.size);
            if(수>0)рӯйдод.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(ҳамсон_қимат,рӯйдод.transport.write.buf.data,рӯйдод.transport.write.buf.size);
            if(수>0)рӯйдод.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            рӯйдод.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(рӯйдод.userauth_server.methods.retries>3)рӯйдод.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *иттилоот=&рӯйдод.userauth_server.password;
            if(같은말(&иттилоот->username,"user")&&иттилоот->password.size<=256&&!иттилоот->new_password.size) {
                unsigned char 요약[32];원격요약(иттилоот->password.data,иттилоот->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)иттилоот->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *иттилоот=&рӯйдод.connection.channel_open;
            if(인증됨&&!канал_ворида&&셸대기중&&같은말(&иттилоот->type,"session")&&!иттилоот->rq_data.size) {
                иттилоот->reply=ASSH_CONNECTION_REPLY_SUCCESS;иттилоот->pkt_size=4096;
                иттилоот->win_size=-1;канал_ворида=иттилоот->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&рӯйдод.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *иттилоот=&рӯйдод.connection.channel_data;
            if(!셸시작됨||иттилоот->ch!=канал_ворида||иттилоот->ext){끊기=1;break;}
            unsigned 수=иттилоот->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(иттилоот->data.data[순번]==4){анҷом_додан_вазъият=0;수=순번;иттилоот->transferred=иттилоот->data.size;break;}
            원격입력넣기(иттилоот->data.data,수);if(!иттилоот->transferred)иттилоот->transferred=수;
            if(!수&&анҷом_додан_вазъият<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: канал_ворида=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",рӯйдод.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(пайваст_e05f319b,&рӯйдод,Хато);
        if(끊기){пӯшидан_пайваст();return;}if(쉬기)return;
    }
}
