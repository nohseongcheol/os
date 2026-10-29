/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "ungasittuq_atuutilik.h"
#include "암호기반.h"
#include "Miksaanuungajuq.h"
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
static struct assh_session_s *kasuqsimaniq_e05f319b;
static struct assh_channel_s *saana_Iliniku;
static int 듣는곳=-1,ilagijaujuq_atuutilik=-1,인증됨,셸시작됨,piqujijjut_qanuittuuninga,isulittuq_qanuilinganiq=-1,닫을예정,pigiarniq_tammarniq,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *말,unsigned atuutilik) {
    while(*말)보드글자쓰기(*말++);
    char 숫자[12];unsigned 수=0;do{숫자[수++]='0'+atuutilik%10;atuutilik/=10;}while(atuutilik);
    while(수)보드글자쓰기(숫자[--수]);보드글자쓰기(10);
}
static assh_status_t Parnalli_puigujjaikkut(void *titiqqat,void **turaarut,size_t anininga,enum assh_alloc_type_e 종류) {
    (void)titiqqat;(void)종류;
    if(!anininga){anititaujuq_ungasittuq(*turaarut);*turaarut=0;return ASSH_OK;}
    void *새주소=원격재할당(*turaarut,anininga);
    if(!새주소)return ASSH_ERR_MEM;*turaarut=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *titiqqat,const struct assh_buffer_s *씨앗) {
    (void)titiqqat;(void)씨앗;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *titiqqat,uint8_t *결과,size_t takininga_atuutilik,uint_fast8_t 종류) {
    (void)titiqqat;(void)종류;if(takininga_atuutilik>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,takininga_atuutilik)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *titiqqat){(void)titiqqat;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void matuli_kasuqsimaniq(void) {
    인증됨=셸시작됨=0;saana_Iliniku=0;
    if(kasuqsimaniq_e05f319b)assh_session_release(kasuqsimaniq_e05f319b);kasuqsimaniq_e05f319b=0;
    if(ilagijaujuq_atuutilik>=0)matuli_Kasuqatigiitsimajut(ilagijaujuq_atuutilik);ilagijaujuq_atuutilik=-1;piqujijjut_qanuittuuninga=0;isulittuq_qanuilinganiq=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *titiqqat,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=titiqqat[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int immikkuuqtuq_atuutilik=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return immikkuuqtuq_atuutilik;
}
void 원격출력(unsigned char immikkuuqtuq_atuutilik) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=immikkuuqtuq_atuutilik==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=immikkuuqtuq_atuutilik;이전출력=immikkuuqtuq_atuutilik;
}
uintptr_t 보드원격명령끝(uintptr_t qanuilinganiq_atuutilik){if(셸시작됨&&piqujijjut_qanuittuuninga)isulittuq_qanuilinganiq=(int)qanuilinganiq_atuutilik;return 0;}
uintptr_t 보드원격대기(uintptr_t qanuilinganiq_atuutilik){셸대기중=qanuilinganiq_atuutilik!=0;return 0;}
static int Parnalli_piqujijjutiliriji(void) {
    if(듣는곳>=0)return 0;
    if(!문맥){
        assh_status_t tammarniq=assh_context_create(&문맥,ASSH_SERVER,Parnalli_puigujjaikkut,0,&난수기,0);
        if(tammarniq)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *방식[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        tammarniq=assh_algo_register(문맥,ASSH_SAFETY_WEAK,방식);
        if(!tammarniq)tammarniq=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=sunakkutaaq_naqigaq;
        if(!tammarniq)tammarniq=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(sunakkutaaq_naqigaq));
        if(tammarniq){진단("SSH init error ",tammarniq);assh_context_release(문맥);문맥=0;return -5;}
    }
    int kapputigaq_atuutilik=통신끝점만들기(1);if(kapputigaq_atuutilik<0)return kapputigaq_atuutilik;통신주소재사용(kapputigaq_atuutilik);
    int 결과=망주소묶기(kapputigaq_atuutilik,0,22);if(!결과)결과=연결기다리기(kapputigaq_atuutilik);
    if(결과<0){matuli_Kasuqatigiitsimajut(kapputigaq_atuutilik);return 결과;}듣는곳=kapputigaq_atuutilik;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t sugiarut) {
    if(종류==1)return(uint32_t)aulattivik_ungasittuq_saqqijaarli(sugiarut);
    if(sugiarut==0){matuli_kasuqsimaniq();if(듣는곳>=0)matuli_Kasuqatigiitsimajut(듣는곳);듣는곳=-1;return 0;}
    if(sugiarut==1){pigiarniq_tammarniq=Parnalli_piqujijjutiliriji();return(uint32_t)pigiarniq_tammarniq;}
    return(uint32_t)(듣는곳>=0?1:pigiarniq_tammarniq);
}
void Parnalli_ungasittuq(void){pigiarniq_tammarniq=Parnalli_piqujijjutiliriji();aulattivik_ungasittuq_saqqijaarli(1);}
static int 같은말(const struct assh_cbuffer_s *titiqqat,const char *말) {
    size_t takininga_atuutilik=strlen(말);return titiqqat->size==takininga_atuutilik&&!memcmp(titiqqat->data,말,takininga_atuutilik);
}
static int 터미널요청(const struct assh_cbuffer_s *titiqqat) {
    if(titiqqat->size<24)return 0;
    const unsigned char *자료위치=titiqqat->data;unsigned takininga_atuutilik=assh_load_u32(자료위치);
    if(takininga_atuutilik>128||titiqqat->size<takininga_atuutilik+24)return 0;
    unsigned mode_atuutilik=assh_load_u32(자료위치+4+takininga_atuutilik+16);
    return mode_atuutilik<=2048&&titiqqat->size==takininga_atuutilik+24+mode_atuutilik;
}
static void 요청처리(struct assh_event_request_s *piniku) {
    if(!인증됨||piniku->ch!=saana_Iliniku||!saana_Iliniku)return;
    if(같은말(&piniku->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&piniku->rq_data))piniku->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&piniku->type,"window-change")) {
        if(셸시작됨&&piniku->rq_data.size==16)piniku->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *piqujijjut=0;unsigned takininga_atuutilik=0;
    if(같은말(&piniku->type,"exec")) {
        if(piniku->rq_data.size<4)return;
        takininga_atuutilik=assh_load_u32(piniku->rq_data.data);
        if(!takininga_atuutilik||takininga_atuutilik>2048||piniku->rq_data.size!=takininga_atuutilik+4)return;
        piqujijjut=piniku->rq_data.data+4;
        for(unsigned 순번=0;순번<takininga_atuutilik;순번++)if(!piqujijjut[순번])return;
        piqujijjut_qanuittuuninga=1;
    }else if(!같은말(&piniku->type,"shell")||piniku->rq_data.size)return;
    if(sizeof(입력줄)-입력수<takininga_atuutilik+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(takininga_atuutilik)원격입력넣기(piqujijjut,takininga_atuutilik);원격입력넣기(&끝,1);
    셸시작됨=1;piniku->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!piqujijjut_qanuittuuninga){const char *README_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*README_eb81d7d9)원격출력(*README_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(ilagijaujuq_atuutilik<0){if(지금<재접속시각)return;ilagijaujuq_atuutilik=망연결받기(듣는곳);if(ilagijaujuq_atuutilik<0)return;
        접속시각=지금;assh_status_t tammarniq=assh_session_create(문맥,&kasuqsimaniq_e05f319b);
        if(tammarniq){kasuqsimaniq_e05f319b=0;진단("SSH session error ",tammarniq);matuli_kasuqsimaniq();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){matuli_kasuqsimaniq();return;}
    if(saana_Iliniku&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t tammarniq=assh_channel_data(saana_Iliniku,출력줄+출력앞,&수);
            if(!tammarniq){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(tammarniq!=ASSH_NO_DATA){matuli_kasuqsimaniq();return;}
        }
        if(isulittuq_qanuilinganiq>=0&&!출력수){unsigned char qanuilinganiq_atuutilik[4];assh_store_u32(qanuilinganiq_atuutilik,(uint32_t)isulittuq_qanuilinganiq);
            if(assh_request(kasuqsimaniq_e05f319b,saana_Iliniku,"exit-status",11,qanuilinganiq_atuutilik,4,0)||assh_channel_eof(saana_Iliniku)||assh_channel_close(saana_Iliniku)) {matuli_kasuqsimaniq();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s piniku;
        if(!assh_event_get(kasuqsimaniq_e05f319b,&piniku,지금/1000)){matuli_kasuqsimaniq();return;}
        assh_status_t tammarniq=ASSH_OK;int 쉬기=0,끊기=0;
        switch(piniku.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(ilagijaujuq_atuutilik,piniku.transport.read.buf.data,piniku.transport.read.buf.size);
            if(수>0)piniku.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(ilagijaujuq_atuutilik,piniku.transport.write.buf.data,piniku.transport.write.buf.size);
            if(수>0)piniku.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            piniku.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(piniku.userauth_server.methods.retries>3)piniku.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *titiqqat=&piniku.userauth_server.password;
            if(같은말(&titiqqat->username,"user")&&titiqqat->password.size<=256&&!titiqqat->new_password.size) {
                unsigned char naiglitiqsimajuq_atuutilik[32];ungasittuq_naiglitiqsimajuq(titiqqat->password.data,titiqqat->password.size,naiglitiqsimajuq_atuutilik);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=naiglitiqsimajuq_atuutilik[순번]^piqujijjutiliriji_isirut_naiglitiqsimajuq[순번];memset(naiglitiqsimajuq_atuutilik,0,32);
                if(!차이)titiqqat->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *titiqqat=&piniku.connection.channel_open;
            if(인증됨&&!saana_Iliniku&&셸대기중&&같은말(&titiqqat->type,"session")&&!titiqqat->rq_data.size) {
                titiqqat->reply=ASSH_CONNECTION_REPLY_SUCCESS;titiqqat->pkt_size=4096;
                titiqqat->win_size=-1;saana_Iliniku=titiqqat->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&piniku.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *titiqqat=&piniku.connection.channel_data;
            if(!셸시작됨||titiqqat->ch!=saana_Iliniku||titiqqat->ext){끊기=1;break;}
            unsigned 수=titiqqat->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(titiqqat->data.data[순번]==4){isulittuq_qanuilinganiq=0;수=순번;titiqqat->transferred=titiqqat->data.size;break;}
            원격입력넣기(titiqqat->data.data,수);if(!titiqqat->transferred)titiqqat->transferred=수;
            if(!수&&isulittuq_qanuilinganiq<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: saana_Iliniku=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",piniku.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(kasuqsimaniq_e05f319b,&piniku,tammarniq);
        if(끊기){matuli_kasuqsimaniq();return;}if(쉬기)return;
    }
}
