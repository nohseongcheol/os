/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "аддалены_значэнне.h"
#include "암호기반.h"
#include "Профіль.h"
#include "../Сетка_Стэк/Сетка_Стэк.h"
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
static struct assh_context_s *Кантэкст_значэнне;
static struct assh_session_s *кантакт_e05f319b;
static struct assh_channel_s *канал_увядзенне;
static int 듣는곳=-1,аднарангавы_значэнне=-1,인증됨,셸시작됨,каманда_друкаваць,скончыць_стан=-1,닫을예정,запуск_памылка,셸대기중;
static uintptr_t кантакт_час,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Гульні_са_словамі_Тэкст,unsigned значэнне) {
    while(*Гульні_са_словамі_Тэкст)보드글자쓰기(*Гульні_са_словамі_Тэкст++);
    char лічба_значэнне[12];unsigned 수=0;do{лічба_значэнне[수++]='0'+значэнне%10;значэнне/=10;}while(значэнне);
    while(수)보드글자쓰기(лічба_значэнне[--수]);보드글자쓰기(10);
}
static assh_status_t Падрыхтаваць_памяць(void *дадзеныя,void **адрас,size_t Памер,enum assh_alloc_type_e 종류) {
    (void)дадзеныя;(void)종류;
    if(!Памер){выпуск_аддалены(*адрас);*адрас=0;return ASSH_OK;}
    void *새주소=원격재할당(*адрас,Памер);
    if(!새주소)return ASSH_ERR_MEM;*адрас=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *дадзеныя,const struct assh_buffer_s *пачатковае_значэнне_значэнне) {
    (void)дадзеныя;(void)пачатковае_значэнне_значэнне;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *дадзеныя,uint8_t *결과,size_t даўжыня_значэнне,uint_fast8_t 종류) {
    (void)дадзеныя;(void)종류;if(даўжыня_значэнне>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,даўжыня_значэнне)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *дадзеныя){(void)дадзеныя;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void закрыць_кантакт(void) {
    인증됨=셸시작됨=0;канал_увядзенне=0;
    if(кантакт_e05f319b)assh_session_release(кантакт_e05f319b);кантакт_e05f319b=0;
    if(аднарангавы_значэнне>=0)закрыць_Сетка(аднарангавы_значэнне);аднарангавы_значэнне=-1;каманда_друкаваць=0;скончыць_стан=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *дадзеныя,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=дадзеныя[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int сімвал_значэнне_068c2631=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return сімвал_значэнне_068c2631;
}
void 원격출력(unsigned char сімвал_значэнне_068c2631) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=сімвал_значэнне_068c2631==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=сімвал_значэнне_068c2631;이전출력=сімвал_значэнне_068c2631;
}
uintptr_t 보드원격명령끝(uintptr_t стан_значэнне){if(셸시작됨&&каманда_друкаваць)скончыць_стан=(int)стан_значэнне;return 0;}
uintptr_t 보드원격대기(uintptr_t стан_значэнне){셸대기중=стан_значэнне!=0;return 0;}
static int Падрыхтаваць_абалонка(void) {
    if(듣는곳>=0)return 0;
    if(!Кантэкст_значэнне){
        assh_status_t ПАМЫЛКА=assh_context_create(&Кантэкст_значэнне,ASSH_SERVER,Падрыхтаваць_памяць,0,&난수기,0);
        if(ПАМЫЛКА)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *спосаб_рэжым[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ПАМЫЛКА=assh_algo_register(Кантэкст_значэнне,ASSH_SAFETY_WEAK,спосаб_рэжым);
        if(!ПАМЫЛКА)ПАМЫЛКА=assh_service_register_va(Кантэкст_значэнне,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=прылада_клавіша;
        if(!ПАМЫЛКА)ПАМЫЛКА=assh_key_load(Кантэкст_значэнне,assh_context_keys(Кантэкст_значэнне),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(прылада_клавіша));
        if(ПАМЫЛКА){진단("SSH init error ",ПАМЫЛКА);assh_context_release(Кантэкст_значэнне);Кантэкст_значэнне=0;return -5;}
    }
    int порт_значэнне=통신끝점만들기(1);if(порт_значэнне<0)return порт_значэнне;통신주소재사용(порт_значэнне);
    int 결과=망주소묶기(порт_значэнне,0,22);if(!결과)결과=연결기다리기(порт_значэнне);
    if(결과<0){закрыць_Сетка(порт_значэнне);return 결과;}듣는곳=порт_значэнне;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t Дзеянне) {
    if(종류==1)return(uint32_t)кіраванне_аддалены_дысплэй(Дзеянне);
    if(Дзеянне==0){закрыць_кантакт();if(듣는곳>=0)закрыць_Сетка(듣는곳);듣는곳=-1;return 0;}
    if(Дзеянне==1){запуск_памылка=Падрыхтаваць_абалонка();return(uint32_t)запуск_памылка;}
    return(uint32_t)(듣는곳>=0?1:запуск_памылка);
}
void Падрыхтаваць_аддалены(void){запуск_памылка=Падрыхтаваць_абалонка();кіраванне_аддалены_дысплэй(1);}
static int 같은말(const struct assh_cbuffer_s *дадзеныя,const char *Гульні_са_словамі_Тэкст) {
    size_t даўжыня_значэнне=strlen(Гульні_са_словамі_Тэкст);return дадзеныя->size==даўжыня_значэнне&&!memcmp(дадзеныя->data,Гульні_са_словамі_Тэкст,даўжыня_значэнне);
}
static int 터미널요청(const struct assh_cbuffer_s *дадзеныя) {
    if(дадзеныя->size<24)return 0;
    const unsigned char *자료위치=дадзеныя->data;unsigned даўжыня_значэнне=assh_load_u32(자료위치);
    if(даўжыня_значэнне>128||дадзеныя->size<даўжыня_значэнне+24)return 0;
    unsigned рэжым_значэнне=assh_load_u32(자료위치+4+даўжыня_значэнне+16);
    return рэжым_значэнне<=2048&&дадзеныя->size==даўжыня_значэнне+24+рэжым_значэнне;
}
static void 요청처리(struct assh_event_request_s *Падзея) {
    if(!인증됨||Падзея->ch!=канал_увядзенне||!канал_увядзенне)return;
    if(같은말(&Падзея->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&Падзея->rq_data))Падзея->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Падзея->type,"window-change")) {
        if(셸시작됨&&Падзея->rq_data.size==16)Падзея->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *Загад=0;unsigned даўжыня_значэнне=0;
    if(같은말(&Падзея->type,"exec")) {
        if(Падзея->rq_data.size<4)return;
        даўжыня_значэнне=assh_load_u32(Падзея->rq_data.data);
        if(!даўжыня_значэнне||даўжыня_значэнне>2048||Падзея->rq_data.size!=даўжыня_значэнне+4)return;
        Загад=Падзея->rq_data.data+4;
        for(unsigned 순번=0;순번<даўжыня_значэнне;순번++)if(!Загад[순번])return;
        каманда_друкаваць=1;
    }else if(!같은말(&Падзея->type,"shell")||Падзея->rq_data.size)return;
    if(sizeof(입력줄)-입력수<даўжыня_значэнне+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(даўжыня_значэнне)원격입력넣기(Загад,даўжыня_значэнне);원격입력넣기(&끝,1);
    셸시작됨=1;Падзея->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!каманда_друкаваць){const char *файл_звестак_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*файл_звестак_eb81d7d9)원격출력(*файл_звестак_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t ЗАРАЗ_значэнне=보드밀리초();
    if(аднарангавы_значэнне<0){if(ЗАРАЗ_значэнне<재접속시각)return;аднарангавы_значэнне=망연결받기(듣는곳);if(аднарангавы_значэнне<0)return;
        кантакт_час=ЗАРАЗ_значэнне;assh_status_t ПАМЫЛКА=assh_session_create(Кантэкст_значэнне,&кантакт_e05f319b);
        if(ПАМЫЛКА){кантакт_e05f319b=0;진단("SSH session error ",ПАМЫЛКА);закрыць_кантакт();return;}}
    if((!인증됨&&ЗАРАЗ_значэнне-кантакт_час>30000)||닫을예정==2||(닫을예정&&ЗАРАЗ_значэнне>=닫는시각)){закрыць_кантакт();return;}
    if(канал_увядзенне&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ПАМЫЛКА=assh_channel_data(канал_увядзенне,출력줄+출력앞,&수);
            if(!ПАМЫЛКА){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ПАМЫЛКА!=ASSH_NO_DATA){закрыць_кантакт();return;}
        }
        if(скончыць_стан>=0&&!출력수){unsigned char стан_значэнне[4];assh_store_u32(стан_значэнне,(uint32_t)скончыць_стан);
            if(assh_request(кантакт_e05f319b,канал_увядзенне,"exit-status",11,стан_значэнне,4,0)||assh_channel_eof(канал_увядзенне)||assh_channel_close(канал_увядзенне)) {закрыць_кантакт();return;}
            닫을예정=1;닫는시각=ЗАРАЗ_значэнне+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s Падзея;
        if(!assh_event_get(кантакт_e05f319b,&Падзея,ЗАРАЗ_значэнне/1000)){закрыць_кантакт();return;}
        assh_status_t ПАМЫЛКА=ASSH_OK;int 쉬기=0,끊기=0;
        switch(Падзея.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(аднарангавы_значэнне,Падзея.transport.read.buf.data,Падзея.transport.read.buf.size);
            if(수>0)Падзея.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(аднарангавы_значэнне,Падзея.transport.write.buf.data,Падзея.transport.write.buf.size);
            if(수>0)Падзея.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Падзея.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Падзея.userauth_server.methods.retries>3)Падзея.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *дадзеныя=&Падзея.userauth_server.password;
            if(같은말(&дадзеныя->username,"user")&&дадзеныя->password.size<=256&&!дадзеныя->new_password.size) {
                unsigned char 요약[32];원격요약(дадзеныя->password.data,дадзеныя->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)дадзеныя->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *дадзеныя=&Падзея.connection.channel_open;
            if(인증됨&&!канал_увядзенне&&셸대기중&&같은말(&дадзеныя->type,"session")&&!дадзеныя->rq_data.size) {
                дадзеныя->reply=ASSH_CONNECTION_REPLY_SUCCESS;дадзеныя->pkt_size=4096;
                дадзеныя->win_size=-1;канал_увядзенне=дадзеныя->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&Падзея.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *дадзеныя=&Падзея.connection.channel_data;
            if(!셸시작됨||дадзеныя->ch!=канал_увядзенне||дадзеныя->ext){끊기=1;break;}
            unsigned 수=дадзеныя->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(дадзеныя->data.data[순번]==4){скончыць_стан=0;수=순번;дадзеныя->transferred=дадзеныя->data.size;break;}
            원격입력넣기(дадзеныя->data.data,수);if(!дадзеныя->transferred)дадзеныя->transferred=수;
            if(!수&&скончыць_стан<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: канал_увядзенне=0;셸시작됨=0;닫을예정=1;닫는시각=ЗАРАЗ_значэнне+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Падзея.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(кантакт_e05f319b,&Падзея,ПАМЫЛКА);
        if(끊기){закрыць_кантакт();return;}if(쉬기)return;
    }
}
