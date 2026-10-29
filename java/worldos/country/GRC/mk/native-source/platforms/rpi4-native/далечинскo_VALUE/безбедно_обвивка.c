/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "далечинскo_VALUE.h"
#include "암호기반.h"
#include "Профил.h"
#include "../Мрежа_Купче/Мрежа_Купче.h"
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
static struct assh_context_s *Контекст_VALUE;
static struct assh_session_s *врска_e05f319b;
static struct assh_channel_s *канал_внес;
static int 듣는곳=-1,рамноправен_уред_VALUE=-1,인증됨,셸시작됨,наредба_TYPE,крај_статус=-1,닫을예정,подигање_грешка,обвивка_Чекам;
static uintptr_t врска_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_СМС,unsigned VALUE) {
    while(*Word_СМС)보드글자쓰기(*Word_СМС++);
    char цифра_VALUE[12];unsigned 수=0;do{цифра_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(цифра_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Подготви_Меморија(void *податоци,void **адреса,size_t Големина,enum assh_alloc_type_e 종류) {
    (void)податоци;(void)종류;
    if(!Големина){издание_далечинскo(*адреса);*адреса=0;return ASSH_OK;}
    void *새주소=원격재할당(*адреса,Големина);
    if(!새주소)return ASSH_ERR_MEM;*адреса=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *податоци,const struct assh_buffer_s *семе_VALUE) {
    (void)податоци;(void)семе_VALUE;unsigned char 시험[32];int мерка=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return мерка?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *податоци,uint8_t *мерка,size_t должина_VALUE,uint_fast8_t 종류) {
    (void)податоци;(void)종류;if(должина_VALUE>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(мерка,должина_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *податоци){(void)податоци;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void затвори_врска(void) {
    인증됨=셸시작됨=0;канал_внес=0;
    if(врска_e05f319b)assh_session_release(врска_e05f319b);врска_e05f319b=0;
    if(рамноправен_уред_VALUE>=0)затвори_Мрежа(рамноправен_уред_VALUE);рамноправен_уред_VALUE=-1;наредба_TYPE=0;крај_статус=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *податоци,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=податоци[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int знак_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return знак_VALUE;
}
void 원격출력(unsigned char знак_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=знак_VALUE==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=знак_VALUE;이전출력=знак_VALUE;
}
uintptr_t табла_крај_далечинскo_наредба(uintptr_t статус_VALUE){if(셸시작됨&&наредба_TYPE)крај_статус=(int)статус_VALUE;return 0;}
uintptr_t табла_далечинскo_почекај(uintptr_t статус_VALUE){обвивка_Чекам=статус_VALUE!=0;return 0;}
static int Подготви_обвивка(void) {
    if(듣는곳>=0)return 0;
    if(!Контекст_VALUE){
        assh_status_t ГРЕШКА=assh_context_create(&Контекст_VALUE,ASSH_SERVER,Подготви_Меморија,0,&난수기,0);
        if(ГРЕШКА)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *метод_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ГРЕШКА=assh_algo_register(Контекст_VALUE,ASSH_SAFETY_WEAK,метод_MODE);
        if(!ГРЕШКА)ГРЕШКА=assh_service_register_va(Контекст_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=уред_Клуч;
        if(!ГРЕШКА)ГРЕШКА=assh_key_load(Контекст_VALUE,assh_context_keys(Контекст_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(уред_Клуч));
        if(ГРЕШКА){진단("SSH init error ",ГРЕШКА);assh_context_release(Контекст_VALUE);Контекст_VALUE=0;return -5;}
    }
    int порта_VALUE=통신끝점만들기(1);if(порта_VALUE<0)return порта_VALUE;통신주소재사용(порта_VALUE);
    int мерка=망주소묶기(порта_VALUE,0,22);if(!мерка)мерка=연결기다리기(порта_VALUE);
    if(мерка<0){затвори_Мрежа(порта_VALUE);return мерка;}듣는곳=порта_VALUE;return 0;
}
uintptr_t табла_набљудување(uintptr_t 종류,uintptr_t Дејство) {
    if(종류==1)return(uint32_t)контрола_далечинскo_екран(Дејство);
    if(Дејство==0){затвори_врска();if(듣는곳>=0)затвори_Мрежа(듣는곳);듣는곳=-1;return 0;}
    if(Дејство==1){подигање_грешка=Подготви_обвивка();return(uint32_t)подигање_грешка;}
    return(uint32_t)(듣는곳>=0?1:подигање_грешка);
}
void Подготви_далечинскo(void){подигање_грешка=Подготви_обвивка();контрола_далечинскo_екран(1);}
static int 같은말(const struct assh_cbuffer_s *податоци,const char *Word_СМС) {
    size_t должина_VALUE=strlen(Word_СМС);return податоци->size==должина_VALUE&&!memcmp(податоци->data,Word_СМС,должина_VALUE);
}
static int Терминал_Барање_на_HTTP(const struct assh_cbuffer_s *податоци) {
    if(податоци->size<24)return 0;
    const unsigned char *податоци_позиционирање=податоци->data;unsigned должина_VALUE=assh_load_u32(податоци_позиционирање);
    if(должина_VALUE>128||податоци->size<должина_VALUE+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(податоци_позиционирање+4+должина_VALUE+16);
    return MODE_VALUE<=2048&&податоци->size==должина_VALUE+24+MODE_VALUE;
}
static void рачка_Барање_на_HTTP(struct assh_event_request_s *настан) {
    if(!인증됨||настан->ch!=канал_внес||!канал_внес)return;
    if(같은말(&настан->type,"pty-req")) {
        if(!셸시작됨&&Терминал_Барање_на_HTTP(&настан->rq_data))настан->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&настан->type,"window-change")) {
        if(셸시작됨&&настан->rq_data.size==16)настан->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!обвивка_Чекам)return;
    const unsigned char *Команда=0;unsigned должина_VALUE=0;
    if(같은말(&настан->type,"exec")) {
        if(настан->rq_data.size<4)return;
        должина_VALUE=assh_load_u32(настан->rq_data.data);
        if(!должина_VALUE||должина_VALUE>2048||настан->rq_data.size!=должина_VALUE+4)return;
        Команда=настан->rq_data.data+4;
        for(unsigned 순번=0;순번<должина_VALUE;순번++)if(!Команда[순번])return;
        наредба_TYPE=1;
    }else if(!같은말(&настан->type,"shell")||настан->rq_data.size)return;
    if(sizeof(입력줄)-입력수<должина_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(должина_VALUE)원격입력넣기(Команда,должина_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;настан->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!наредба_TYPE){const char *информации_пред_употреба_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*информации_пред_употреба_eb81d7d9)원격출력(*информации_пред_употреба_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(рамноправен_уред_VALUE<0){if(NOW_VALUE<재접속시각)return;рамноправен_уред_VALUE=망연결받기(듣는곳);if(рамноправен_уред_VALUE<0)return;
        врска_TIME=NOW_VALUE;assh_status_t ГРЕШКА=assh_session_create(Контекст_VALUE,&врска_e05f319b);
        if(ГРЕШКА){врска_e05f319b=0;진단("SSH session error ",ГРЕШКА);затвори_врска();return;}}
    if((!인증됨&&NOW_VALUE-врска_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){затвори_врска();return;}
    if(канал_внес&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ГРЕШКА=assh_channel_data(канал_внес,출력줄+출력앞,&수);
            if(!ГРЕШКА){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ГРЕШКА!=ASSH_NO_DATA){затвори_врска();return;}
        }
        if(крај_статус>=0&&!출력수){unsigned char статус_VALUE[4];assh_store_u32(статус_VALUE,(uint32_t)крај_статус);
            if(assh_request(врска_e05f319b,канал_внес,"exit-status",11,статус_VALUE,4,0)||assh_channel_eof(канал_внес)||assh_channel_close(канал_внес)) {затвори_врска();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s настан;
        if(!assh_event_get(врска_e05f319b,&настан,NOW_VALUE/1000)){затвори_врска();return;}
        assh_status_t ГРЕШКА=ASSH_OK;int 쉬기=0,끊기=0;
        switch(настан.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(рамноправен_уред_VALUE,настан.transport.read.buf.data,настан.transport.read.buf.size);
            if(수>0)настан.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(рамноправен_уред_VALUE,настан.transport.write.buf.data,настан.transport.write.buf.size);
            if(수>0)настан.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            настан.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(настан.userauth_server.methods.retries>3)настан.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *податоци=&настан.userauth_server.password;
            if(같은말(&податоци->username,"user")&&податоци->password.size<=256&&!податоци->new_password.size) {
                unsigned char резиме_VALUE[32];далечинскo_резиме(податоци->password.data,податоци->password.size,резиме_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=резиме_VALUE[순번]^обвивка_лозинка_резиме[순번];memset(резиме_VALUE,0,32);
                if(!차이)податоци->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *податоци=&настан.connection.channel_open;
            if(인증됨&&!канал_внес&&обвивка_Чекам&&같은말(&податоци->type,"session")&&!податоци->rq_data.size) {
                податоци->reply=ASSH_CONNECTION_REPLY_SUCCESS;податоци->pkt_size=4096;
                податоци->win_size=-1;канал_внес=податоци->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: рачка_Барање_на_HTTP(&настан.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *податоци=&настан.connection.channel_data;
            if(!셸시작됨||податоци->ch!=канал_внес||податоци->ext){끊기=1;break;}
            unsigned 수=податоци->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(податоци->data.data[순번]==4){крај_статус=0;수=순번;податоци->transferred=податоци->data.size;break;}
            원격입력넣기(податоци->data.data,수);if(!податоци->transferred)податоци->transferred=수;
            if(!수&&крај_статус<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: канал_внес=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",настан.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(врска_e05f319b,&настан,ГРЕШКА);
        if(끊기){затвори_врска();return;}if(쉬기)return;
    }
}
