/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "원격.h"
#include "암호기반.h"
#include "heftinirde_kuutoro.h"
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
static struct assh_session_s *ceŋondiral_e05f319b;
static struct assh_channel_s *kanaal_naatnugol;
static int 듣는곳=-1,giƴiraaɗo_njaru=-1,인증됨,셸시작됨,명령형,taƴde_ngonka=-1,닫을예정,kuɓɓagol_juumre,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *말,unsigned njaru) {
    while(*말)보드글자쓰기(*말++);
    char 숫자[12];unsigned 수=0;do{숫자[수++]='0'+njaru%10;njaru/=10;}while(njaru);
    while(수)보드글자쓰기(숫자[--수]);보드글자쓰기(10);
}
static assh_status_t Heblu_teskordu(void *keɓe,void **ñiiɓirde,size_t waylude_etannde,enum assh_alloc_type_e 종류) {
    (void)keɓe;(void)종류;
    if(!waylude_etannde){원격해제(*ñiiɓirde);*ñiiɓirde=0;return ASSH_OK;}
    void *새주소=원격재할당(*ñiiɓirde,waylude_etannde);
    if(!새주소)return ASSH_ERR_MEM;*ñiiɓirde=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *keɓe,const struct assh_buffer_s *씨앗) {
    (void)keɓe;(void)씨앗;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *keɓe,uint8_t *결과,size_t njuuteendi_njaru,uint_fast8_t 종류) {
    (void)keɓe;(void)종류;if(njuuteendi_njaru>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,njuuteendi_njaru)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *keɓe){(void)keɓe;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void uddude_ceŋondiral(void) {
    인증됨=셸시작됨=0;kanaal_naatnugol=0;
    if(ceŋondiral_e05f319b)assh_session_release(ceŋondiral_e05f319b);ceŋondiral_e05f319b=0;
    if(giƴiraaɗo_njaru>=0)uddude_laylaytol(giƴiraaɗo_njaru);giƴiraaɗo_njaru=-1;명령형=0;taƴde_ngonka=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *keɓe,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=keɓe[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int alkulal_njaru=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return alkulal_njaru;
}
void 원격출력(unsigned char alkulal_njaru) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=alkulal_njaru==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=alkulal_njaru;이전출력=alkulal_njaru;
}
uintptr_t 보드원격명령끝(uintptr_t ngonka_njaru){if(셸시작됨&&명령형)taƴde_ngonka=(int)ngonka_njaru;return 0;}
uintptr_t 보드원격대기(uintptr_t ngonka_njaru){셸대기중=ngonka_njaru!=0;return 0;}
static int Heblu_laalagal(void) {
    if(듣는곳>=0)return 0;
    if(!문맥){
        assh_status_t juumre=assh_context_create(&문맥,ASSH_SERVER,Heblu_teskordu,0,&난수기,0);
        if(juumre)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *방식[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        juumre=assh_algo_register(문맥,ASSH_SAFETY_WEAK,방식);
        if(!juumre)juumre=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=kaɓirgal_kelal;
        if(!juumre)juumre=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(kaɓirgal_kelal));
        if(juumre){진단("SSH init error ",juumre);assh_context_release(문맥);문맥=0;return -5;}
    }
    int poor_njaru=통신끝점만들기(1);if(poor_njaru<0)return poor_njaru;통신주소재사용(poor_njaru);
    int 결과=망주소묶기(poor_njaru,0,22);if(!결과)결과=연결기다리기(poor_njaru);
    if(결과<0){uddude_laylaytol(poor_njaru);return 결과;}듣는곳=poor_njaru;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t gollal) {
    if(종류==1)return(uint32_t)원격화면제어(gollal);
    if(gollal==0){uddude_ceŋondiral();if(듣는곳>=0)uddude_laylaytol(듣는곳);듣는곳=-1;return 0;}
    if(gollal==1){kuɓɓagol_juumre=Heblu_laalagal();return(uint32_t)kuɓɓagol_juumre;}
    return(uint32_t)(듣는곳>=0?1:kuɓɓagol_juumre);
}
void 원격준비(void){kuɓɓagol_juumre=Heblu_laalagal();원격화면제어(1);}
static int 같은말(const struct assh_cbuffer_s *keɓe,const char *말) {
    size_t njuuteendi_njaru=strlen(말);return keɓe->size==njuuteendi_njaru&&!memcmp(keɓe->data,말,njuuteendi_njaru);
}
static int 터미널요청(const struct assh_cbuffer_s *keɓe) {
    if(keɓe->size<24)return 0;
    const unsigned char *자료위치=keɓe->data;unsigned njuuteendi_njaru=assh_load_u32(자료위치);
    if(njuuteendi_njaru>128||keɓe->size<njuuteendi_njaru+24)return 0;
    unsigned modd_njaru=assh_load_u32(자료위치+4+njuuteendi_njaru+16);
    return modd_njaru<=2048&&keɓe->size==njuuteendi_njaru+24+modd_njaru;
}
static void 요청처리(struct assh_event_request_s *saɗteende) {
    if(!인증됨||saɗteende->ch!=kanaal_naatnugol||!kanaal_naatnugol)return;
    if(같은말(&saɗteende->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&saɗteende->rq_data))saɗteende->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&saɗteende->type,"window-change")) {
        if(셸시작됨&&saɗteende->rq_data.size==16)saɗteende->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *ginol=0;unsigned njuuteendi_njaru=0;
    if(같은말(&saɗteende->type,"exec")) {
        if(saɗteende->rq_data.size<4)return;
        njuuteendi_njaru=assh_load_u32(saɗteende->rq_data.data);
        if(!njuuteendi_njaru||njuuteendi_njaru>2048||saɗteende->rq_data.size!=njuuteendi_njaru+4)return;
        ginol=saɗteende->rq_data.data+4;
        for(unsigned 순번=0;순번<njuuteendi_njaru;순번++)if(!ginol[순번])return;
        명령형=1;
    }else if(!같은말(&saɗteende->type,"shell")||saɗteende->rq_data.size)return;
    if(sizeof(입력줄)-입력수<njuuteendi_njaru+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(njuuteendi_njaru)원격입력넣기(ginol,njuuteendi_njaru);원격입력넣기(&끝,1);
    셸시작됨=1;saɗteende->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!명령형){const char *TARƊOO_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*TARƊOO_eb81d7d9)원격출력(*TARƊOO_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(giƴiraaɗo_njaru<0){if(지금<재접속시각)return;giƴiraaɗo_njaru=망연결받기(듣는곳);if(giƴiraaɗo_njaru<0)return;
        접속시각=지금;assh_status_t juumre=assh_session_create(문맥,&ceŋondiral_e05f319b);
        if(juumre){ceŋondiral_e05f319b=0;진단("SSH session error ",juumre);uddude_ceŋondiral();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){uddude_ceŋondiral();return;}
    if(kanaal_naatnugol&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t juumre=assh_channel_data(kanaal_naatnugol,출력줄+출력앞,&수);
            if(!juumre){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(juumre!=ASSH_NO_DATA){uddude_ceŋondiral();return;}
        }
        if(taƴde_ngonka>=0&&!출력수){unsigned char ngonka_njaru[4];assh_store_u32(ngonka_njaru,(uint32_t)taƴde_ngonka);
            if(assh_request(ceŋondiral_e05f319b,kanaal_naatnugol,"exit-status",11,ngonka_njaru,4,0)||assh_channel_eof(kanaal_naatnugol)||assh_channel_close(kanaal_naatnugol)) {uddude_ceŋondiral();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s saɗteende;
        if(!assh_event_get(ceŋondiral_e05f319b,&saɗteende,지금/1000)){uddude_ceŋondiral();return;}
        assh_status_t juumre=ASSH_OK;int 쉬기=0,끊기=0;
        switch(saɗteende.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(giƴiraaɗo_njaru,saɗteende.transport.read.buf.data,saɗteende.transport.read.buf.size);
            if(수>0)saɗteende.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(giƴiraaɗo_njaru,saɗteende.transport.write.buf.data,saɗteende.transport.write.buf.size);
            if(수>0)saɗteende.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            saɗteende.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(saɗteende.userauth_server.methods.retries>3)saɗteende.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *keɓe=&saɗteende.userauth_server.password;
            if(같은말(&keɓe->username,"user")&&keɓe->password.size<=256&&!keɓe->new_password.size) {
                unsigned char 요약[32];원격요약(keɓe->password.data,keɓe->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)keɓe->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *keɓe=&saɗteende.connection.channel_open;
            if(인증됨&&!kanaal_naatnugol&&셸대기중&&같은말(&keɓe->type,"session")&&!keɓe->rq_data.size) {
                keɓe->reply=ASSH_CONNECTION_REPLY_SUCCESS;keɓe->pkt_size=4096;
                keɓe->win_size=-1;kanaal_naatnugol=keɓe->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&saɗteende.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *keɓe=&saɗteende.connection.channel_data;
            if(!셸시작됨||keɓe->ch!=kanaal_naatnugol||keɓe->ext){끊기=1;break;}
            unsigned 수=keɓe->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(keɓe->data.data[순번]==4){taƴde_ngonka=0;수=순번;keɓe->transferred=keɓe->data.size;break;}
            원격입력넣기(keɓe->data.data,수);if(!keɓe->transferred)keɓe->transferred=수;
            if(!수&&taƴde_ngonka<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: kanaal_naatnugol=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",saɗteende.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(ceŋondiral_e05f319b,&saɗteende,juumre);
        if(끊기){uddude_ceŋondiral();return;}if(쉬기)return;
    }
}
