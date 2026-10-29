/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "mamao_uara.h"
#include "암호기반.h"
#include "Kōtaha.h"
#include "../whatunga_Huinga/whatunga_Huinga.h"
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
static struct assh_context_s *Horopaki_uara;
static struct assh_session_s *hononga_e05f319b;
static struct assh_channel_s *hongere_tāurunga;
static int 듣는곳=-1,hoa_uara=-1,인증됨,셸시작됨,tono_TYPE,mutu_tūnga=-1,닫을예정,whakaara_hapa,셸대기중;
static uintptr_t hononga_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_TEXT,unsigned uara) {
    while(*Word_TEXT)보드글자쓰기(*Word_TEXT++);
    char mati_uara[12];unsigned 수=0;do{mati_uara[수++]='0'+uara%10;uara/=10;}while(uara);
    while(수)보드글자쓰기(mati_uara[--수]);보드글자쓰기(10);
}
static assh_status_t Whakarite_Pūmahara(void *raraunga,void **ADDRESS,size_t rahi,enum assh_alloc_type_e 종류) {
    (void)raraunga;(void)종류;
    if(!rahi){tuku_mamao(*ADDRESS);*ADDRESS=0;return ASSH_OK;}
    void *새주소=원격재할당(*ADDRESS,rahi);
    if(!새주소)return ASSH_ERR_MEM;*ADDRESS=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *raraunga,const struct assh_buffer_s *kākano_uara) {
    (void)raraunga;(void)kākano_uara;unsigned char 시험[32];int mēhua=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return mēhua?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *raraunga,uint8_t *mēhua,size_t roa_uara,uint_fast8_t 종류) {
    (void)raraunga;(void)종류;if(roa_uara>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(mēhua,roa_uara)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *raraunga){(void)raraunga;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void kati_hononga(void) {
    인증됨=셸시작됨=0;hongere_tāurunga=0;
    if(hononga_e05f319b)assh_session_release(hononga_e05f319b);hononga_e05f319b=0;
    if(hoa_uara>=0)kati_whatunga(hoa_uara);hoa_uara=-1;tono_TYPE=0;mutu_tūnga=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *raraunga,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=raraunga[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int pūāhua_uara=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return pūāhua_uara;
}
void 원격출력(unsigned char pūāhua_uara) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=pūāhua_uara==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=pūāhua_uara;이전출력=pūāhua_uara;
}
uintptr_t papa_mutu_mamao_tono(uintptr_t tūnga_uara){if(셸시작됨&&tono_TYPE)mutu_tūnga=(int)tūnga_uara;return 0;}
uintptr_t 보드원격대기(uintptr_t tūnga_uara){셸대기중=tūnga_uara!=0;return 0;}
static int Whakarite_anga(void) {
    if(듣는곳>=0)return 0;
    if(!Horopaki_uara){
        assh_status_t Pōhēhē=assh_context_create(&Horopaki_uara,ASSH_SERVER,Whakarite_Pūmahara,0,&난수기,0);
        if(Pōhēhē)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *aratuka_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Pōhēhē=assh_algo_register(Horopaki_uara,ASSH_SAFETY_WEAK,aratuka_MODE);
        if(!Pōhēhē)Pōhēhē=assh_service_register_va(Horopaki_uara,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=pūkoro_kī;
        if(!Pōhēhē)Pōhēhē=assh_key_load(Horopaki_uara,assh_context_keys(Horopaki_uara),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(pūkoro_kī));
        if(Pōhēhē){진단("SSH init error ",Pōhēhē);assh_context_release(Horopaki_uara);Horopaki_uara=0;return -5;}
    }
    int kawe_uara=통신끝점만들기(1);if(kawe_uara<0)return kawe_uara;통신주소재사용(kawe_uara);
    int mēhua=망주소묶기(kawe_uara,0,22);if(!mēhua)mēhua=연결기다리기(kawe_uara);
    if(mēhua<0){kati_whatunga(kawe_uara);return mēhua;}듣는곳=kawe_uara;return 0;
}
uintptr_t papa_mātaki(uintptr_t 종류,uintptr_t hohenga) {
    if(종류==1)return(uint32_t)mana_mamao_whakaatu(hohenga);
    if(hohenga==0){kati_hononga();if(듣는곳>=0)kati_whatunga(듣는곳);듣는곳=-1;return 0;}
    if(hohenga==1){whakaara_hapa=Whakarite_anga();return(uint32_t)whakaara_hapa;}
    return(uint32_t)(듣는곳>=0?1:whakaara_hapa);
}
void Whakarite_mamao(void){whakaara_hapa=Whakarite_anga();mana_mamao_whakaatu(1);}
static int 같은말(const struct assh_cbuffer_s *raraunga,const char *Word_TEXT) {
    size_t roa_uara=strlen(Word_TEXT);return raraunga->size==roa_uara&&!memcmp(raraunga->data,Word_TEXT,roa_uara);
}
static int 터미널요청(const struct assh_cbuffer_s *raraunga) {
    if(raraunga->size<24)return 0;
    const unsigned char *raraunga_tūranga=raraunga->data;unsigned roa_uara=assh_load_u32(raraunga_tūranga);
    if(roa_uara>128||raraunga->size<roa_uara+24)return 0;
    unsigned MODE_uara=assh_load_u32(raraunga_tūranga+4+roa_uara+16);
    return MODE_uara<=2048&&raraunga->size==roa_uara+24+MODE_uara;
}
static void 요청처리(struct assh_event_request_s *hui) {
    if(!인증됨||hui->ch!=hongere_tāurunga||!hongere_tāurunga)return;
    if(같은말(&hui->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&hui->rq_data))hui->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&hui->type,"window-change")) {
        if(셸시작됨&&hui->rq_data.size==16)hui->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *tono=0;unsigned roa_uara=0;
    if(같은말(&hui->type,"exec")) {
        if(hui->rq_data.size<4)return;
        roa_uara=assh_load_u32(hui->rq_data.data);
        if(!roa_uara||roa_uara>2048||hui->rq_data.size!=roa_uara+4)return;
        tono=hui->rq_data.data+4;
        for(unsigned 순번=0;순번<roa_uara;순번++)if(!tono[순번])return;
        tono_TYPE=1;
    }else if(!같은말(&hui->type,"shell")||hui->rq_data.size)return;
    if(sizeof(입력줄)-입력수<roa_uara+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(roa_uara)원격입력넣기(tono,roa_uara);원격입력넣기(&끝,1);
    셸시작됨=1;hui->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!tono_TYPE){const char *PĀNUIMAI_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*PĀNUIMAI_eb81d7d9)원격출력(*PĀNUIMAI_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t NOW_uara=보드밀리초();
    if(hoa_uara<0){if(NOW_uara<재접속시각)return;hoa_uara=망연결받기(듣는곳);if(hoa_uara<0)return;
        hononga_TIME=NOW_uara;assh_status_t Pōhēhē=assh_session_create(Horopaki_uara,&hononga_e05f319b);
        if(Pōhēhē){hononga_e05f319b=0;진단("SSH session error ",Pōhēhē);kati_hononga();return;}}
    if((!인증됨&&NOW_uara-hononga_TIME>30000)||닫을예정==2||(닫을예정&&NOW_uara>=닫는시각)){kati_hononga();return;}
    if(hongere_tāurunga&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Pōhēhē=assh_channel_data(hongere_tāurunga,출력줄+출력앞,&수);
            if(!Pōhēhē){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Pōhēhē!=ASSH_NO_DATA){kati_hononga();return;}
        }
        if(mutu_tūnga>=0&&!출력수){unsigned char tūnga_uara[4];assh_store_u32(tūnga_uara,(uint32_t)mutu_tūnga);
            if(assh_request(hononga_e05f319b,hongere_tāurunga,"exit-status",11,tūnga_uara,4,0)||assh_channel_eof(hongere_tāurunga)||assh_channel_close(hongere_tāurunga)) {kati_hononga();return;}
            닫을예정=1;닫는시각=NOW_uara+3000;
        }
    }
    for(unsigned SEQUENCE_uara=0;SEQUENCE_uara<16;SEQUENCE_uara++) {
        struct assh_event_s hui;
        if(!assh_event_get(hononga_e05f319b,&hui,NOW_uara/1000)){kati_hononga();return;}
        assh_status_t Pōhēhē=ASSH_OK;int 쉬기=0,끊기=0;
        switch(hui.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(hoa_uara,hui.transport.read.buf.data,hui.transport.read.buf.size);
            if(수>0)hui.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(hoa_uara,hui.transport.write.buf.data,hui.transport.write.buf.size);
            if(수>0)hui.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            hui.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(hui.userauth_server.methods.retries>3)hui.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *raraunga=&hui.userauth_server.password;
            if(같은말(&raraunga->username,"user")&&raraunga->password.size<=256&&!raraunga->new_password.size) {
                unsigned char whakarāpoto_uara[32];mamao_whakarāpoto(raraunga->password.data,raraunga->password.size,whakarāpoto_uara);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=whakarāpoto_uara[순번]^anga_kupuhipa_whakarāpoto[순번];memset(whakarāpoto_uara,0,32);
                if(!차이)raraunga->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *raraunga=&hui.connection.channel_open;
            if(인증됨&&!hongere_tāurunga&&셸대기중&&같은말(&raraunga->type,"session")&&!raraunga->rq_data.size) {
                raraunga->reply=ASSH_CONNECTION_REPLY_SUCCESS;raraunga->pkt_size=4096;
                raraunga->win_size=-1;hongere_tāurunga=raraunga->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&hui.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *raraunga=&hui.connection.channel_data;
            if(!셸시작됨||raraunga->ch!=hongere_tāurunga||raraunga->ext){끊기=1;break;}
            unsigned 수=raraunga->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(raraunga->data.data[순번]==4){mutu_tūnga=0;수=순번;raraunga->transferred=raraunga->data.size;break;}
            원격입력넣기(raraunga->data.data,수);if(!raraunga->transferred)raraunga->transferred=수;
            if(!수&&mutu_tūnga<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: hongere_tāurunga=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_uara+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",hui.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(hononga_e05f319b,&hui,Pōhēhē);
        if(끊기){kati_hononga();return;}if(쉬기)return;
    }
}
