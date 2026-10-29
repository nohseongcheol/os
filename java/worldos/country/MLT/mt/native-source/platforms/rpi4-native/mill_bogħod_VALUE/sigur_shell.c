/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "mill_bogħod_VALUE.h"
#include "암호기반.h"
#include "Profil.h"
#include "../netwerk_Munzell/netwerk_Munzell.h"
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
static struct assh_context_s *Kuntest_VALUE;
static struct assh_session_s *konnessjoni_e05f319b;
static struct assh_channel_s *Kanal_entrata;
static int 듣는곳=-1,peer_VALUE=-1,인증됨,셸시작됨,kmand_TYPE,ttermina_stat=-1,닫을예정,ftuħ_żball,셸대기중;
static uintptr_t konnessjoni_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char ċifra_VALUE[12];unsigned 수=0;do{ċifra_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(ċifra_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Ħejji_Memorja(void *data,void **ADDRESS,size_t daqqas,enum assh_alloc_type_e 종류) {
    (void)data;(void)종류;
    if(!daqqas){mexxi_mill_bogħod(*ADDRESS);*ADDRESS=0;return ASSH_OK;}
    void *새주소=원격재할당(*ADDRESS,daqqas);
    if(!새주소)return ASSH_ERR_MEM;*ADDRESS=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *data,const struct assh_buffer_s *valur_inizjali_VALUE) {
    (void)data;(void)valur_inizjali_VALUE;unsigned char 시험[32];int miżura=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return miżura?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *data,uint8_t *miżura,size_t tul_VALUE,uint_fast8_t 종류) {
    (void)data;(void)종류;if(tul_VALUE>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(miżura,tul_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *data){(void)data;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void agħlaq_konnessjoni(void) {
    인증됨=셸시작됨=0;Kanal_entrata=0;
    if(konnessjoni_e05f319b)assh_session_release(konnessjoni_e05f319b);konnessjoni_e05f319b=0;
    if(peer_VALUE>=0)agħlaq_netwerk(peer_VALUE);peer_VALUE=-1;kmand_TYPE=0;ttermina_stat=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *data,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=data[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int karattru_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return karattru_VALUE;
}
void 원격출력(unsigned char karattru_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=karattru_VALUE==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=karattru_VALUE;이전출력=karattru_VALUE;
}
uintptr_t bord_ttermina_mill_bogħod_kmand(uintptr_t stat_VALUE){if(셸시작됨&&kmand_TYPE)ttermina_stat=(int)stat_VALUE;return 0;}
uintptr_t 보드원격대기(uintptr_t stat_VALUE){셸대기중=stat_VALUE!=0;return 0;}
static int Ħejji_shell(void) {
    if(듣는곳>=0)return 0;
    if(!Kuntest_VALUE){
        assh_status_t żball=assh_context_create(&Kuntest_VALUE,ASSH_SERVER,Ħejji_Memorja,0,&난수기,0);
        if(żball)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metodu_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        żball=assh_algo_register(Kuntest_VALUE,ASSH_SAFETY_WEAK,metodu_MODE);
        if(!żball)żball=assh_service_register_va(Kuntest_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=mowbajl_tast;
        if(!żball)żball=assh_key_load(Kuntest_VALUE,assh_context_keys(Kuntest_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(mowbajl_tast));
        if(żball){진단("SSH init error ",żball);assh_context_release(Kuntest_VALUE);Kuntest_VALUE=0;return -5;}
    }
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int miżura=망주소묶기(port_VALUE,0,22);if(!miżura)miżura=연결기다리기(port_VALUE);
    if(miżura<0){agħlaq_netwerk(port_VALUE);return miżura;}듣는곳=port_VALUE;return 0;
}
uintptr_t bord_insegwiment(uintptr_t 종류,uintptr_t azzjoni) {
    if(종류==1)return(uint32_t)kontroll_mill_bogħod_wera(azzjoni);
    if(azzjoni==0){agħlaq_konnessjoni();if(듣는곳>=0)agħlaq_netwerk(듣는곳);듣는곳=-1;return 0;}
    if(azzjoni==1){ftuħ_żball=Ħejji_shell();return(uint32_t)ftuħ_żball;}
    return(uint32_t)(듣는곳>=0?1:ftuħ_żball);
}
void Ħejji_mill_bogħod(void){ftuħ_żball=Ħejji_shell();kontroll_mill_bogħod_wera(1);}
static int 같은말(const struct assh_cbuffer_s *data,const char *Word_SMS) {
    size_t tul_VALUE=strlen(Word_SMS);return data->size==tul_VALUE&&!memcmp(data->data,Word_SMS,tul_VALUE);
}
static int 터미널요청(const struct assh_cbuffer_s *data) {
    if(data->size<24)return 0;
    const unsigned char *data_pożizzjoni=data->data;unsigned tul_VALUE=assh_load_u32(data_pożizzjoni);
    if(tul_VALUE>128||data->size<tul_VALUE+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(data_pożizzjoni+4+tul_VALUE+16);
    return MODE_VALUE<=2048&&data->size==tul_VALUE+24+MODE_VALUE;
}
static void 요청처리(struct assh_event_request_s *avveniment) {
    if(!인증됨||avveniment->ch!=Kanal_entrata||!Kanal_entrata)return;
    if(같은말(&avveniment->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&avveniment->rq_data))avveniment->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&avveniment->type,"window-change")) {
        if(셸시작됨&&avveniment->rq_data.size==16)avveniment->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *kmand=0;unsigned tul_VALUE=0;
    if(같은말(&avveniment->type,"exec")) {
        if(avveniment->rq_data.size<4)return;
        tul_VALUE=assh_load_u32(avveniment->rq_data.data);
        if(!tul_VALUE||tul_VALUE>2048||avveniment->rq_data.size!=tul_VALUE+4)return;
        kmand=avveniment->rq_data.data+4;
        for(unsigned 순번=0;순번<tul_VALUE;순번++)if(!kmand[순번])return;
        kmand_TYPE=1;
    }else if(!같은말(&avveniment->type,"shell")||avveniment->rq_data.size)return;
    if(sizeof(입력줄)-입력수<tul_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(tul_VALUE)원격입력넣기(kmand,tul_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;avveniment->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!kmand_TYPE){const char *AQRANI_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*AQRANI_eb81d7d9)원격출력(*AQRANI_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(peer_VALUE<0){if(NOW_VALUE<재접속시각)return;peer_VALUE=망연결받기(듣는곳);if(peer_VALUE<0)return;
        konnessjoni_TIME=NOW_VALUE;assh_status_t żball=assh_session_create(Kuntest_VALUE,&konnessjoni_e05f319b);
        if(żball){konnessjoni_e05f319b=0;진단("SSH session error ",żball);agħlaq_konnessjoni();return;}}
    if((!인증됨&&NOW_VALUE-konnessjoni_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){agħlaq_konnessjoni();return;}
    if(Kanal_entrata&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t żball=assh_channel_data(Kanal_entrata,출력줄+출력앞,&수);
            if(!żball){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(żball!=ASSH_NO_DATA){agħlaq_konnessjoni();return;}
        }
        if(ttermina_stat>=0&&!출력수){unsigned char stat_VALUE[4];assh_store_u32(stat_VALUE,(uint32_t)ttermina_stat);
            if(assh_request(konnessjoni_e05f319b,Kanal_entrata,"exit-status",11,stat_VALUE,4,0)||assh_channel_eof(Kanal_entrata)||assh_channel_close(Kanal_entrata)) {agħlaq_konnessjoni();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s avveniment;
        if(!assh_event_get(konnessjoni_e05f319b,&avveniment,NOW_VALUE/1000)){agħlaq_konnessjoni();return;}
        assh_status_t żball=ASSH_OK;int 쉬기=0,끊기=0;
        switch(avveniment.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(peer_VALUE,avveniment.transport.read.buf.data,avveniment.transport.read.buf.size);
            if(수>0)avveniment.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(peer_VALUE,avveniment.transport.write.buf.data,avveniment.transport.write.buf.size);
            if(수>0)avveniment.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            avveniment.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(avveniment.userauth_server.methods.retries>3)avveniment.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *data=&avveniment.userauth_server.password;
            if(같은말(&data->username,"user")&&data->password.size<=256&&!data->new_password.size) {
                unsigned char sommarju_VALUE[32];mill_bogħod_sommarju(data->password.data,data->password.size,sommarju_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=sommarju_VALUE[순번]^shell_password_sommarju[순번];memset(sommarju_VALUE,0,32);
                if(!차이)data->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *data=&avveniment.connection.channel_open;
            if(인증됨&&!Kanal_entrata&&셸대기중&&같은말(&data->type,"session")&&!data->rq_data.size) {
                data->reply=ASSH_CONNECTION_REPLY_SUCCESS;data->pkt_size=4096;
                data->win_size=-1;Kanal_entrata=data->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&avveniment.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *data=&avveniment.connection.channel_data;
            if(!셸시작됨||data->ch!=Kanal_entrata||data->ext){끊기=1;break;}
            unsigned 수=data->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(data->data.data[순번]==4){ttermina_stat=0;수=순번;data->transferred=data->data.size;break;}
            원격입력넣기(data->data.data,수);if(!data->transferred)data->transferred=수;
            if(!수&&ttermina_stat<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Kanal_entrata=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",avveniment.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(konnessjoni_e05f319b,&avveniment,żball);
        if(끊기){agħlaq_konnessjoni();return;}if(쉬기)return;
    }
}
