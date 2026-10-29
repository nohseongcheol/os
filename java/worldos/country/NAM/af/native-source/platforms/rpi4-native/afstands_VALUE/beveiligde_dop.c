/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "afstands_VALUE.h"
#include "암호기반.h"
#include "Profiel.h"
#include "../Netwerk_Stapel/Netwerk_Stapel.h"
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
static struct assh_context_s *Konteks_VALUE;
static struct assh_session_s *verbinding_e05f319b;
static struct assh_channel_s *kanaal_inskrywing;
static int 듣는곳=-1,portuur_VALUE=-1,인증됨,셸시작됨,bevel_TYPE,beëindig_stand=-1,닫을예정,selflaai_fout,dop_Besig_om_te_wag;
static uintptr_t verbinding_tyd,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char syfer_VALUE[12];unsigned 수=0;do{syfer_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(syfer_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Maak_gereed_Geheue(void *data,void **adres,size_t Grootte,enum assh_alloc_type_e 종류) {
    (void)data;(void)종류;
    if(!Grootte){stel_vry_afstands(*adres);*adres=0;return ASSH_OK;}
    void *새주소=원격재할당(*adres,Grootte);
    if(!새주소)return ASSH_ERR_MEM;*adres=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *data,const struct assh_buffer_s *voorsien_VALUE) {
    (void)data;(void)voorsien_VALUE;unsigned char 시험[32];int maatreël=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return maatreël?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *data,uint8_t *maatreël,size_t lengte_VALUE,uint_fast8_t 종류) {
    (void)data;(void)종류;if(lengte_VALUE>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(maatreël,lengte_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *data){(void)data;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void sluit_verbinding(void) {
    인증됨=셸시작됨=0;kanaal_inskrywing=0;
    if(verbinding_e05f319b)assh_session_release(verbinding_e05f319b);verbinding_e05f319b=0;
    if(portuur_VALUE>=0)sluit_Netwerk(portuur_VALUE);portuur_VALUE=-1;bevel_TYPE=0;beëindig_stand=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *data,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=data[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int karakter_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return karakter_VALUE;
}
void 원격출력(unsigned char karakter_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=karakter_VALUE==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=karakter_VALUE;이전출력=karakter_VALUE;
}
uintptr_t bord_beëindig_afstands_bevel(uintptr_t stand_VALUE){if(셸시작됨&&bevel_TYPE)beëindig_stand=(int)stand_VALUE;return 0;}
uintptr_t bord_afstands_wag(uintptr_t stand_VALUE){dop_Besig_om_te_wag=stand_VALUE!=0;return 0;}
static int Maak_gereed_dop(void) {
    if(듣는곳>=0)return 0;
    if(!Konteks_VALUE){
        assh_status_t Fout=assh_context_create(&Konteks_VALUE,ASSH_SERVER,Maak_gereed_Geheue,0,&난수기,0);
        if(Fout)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metode_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Fout=assh_algo_register(Konteks_VALUE,ASSH_SAFETY_WEAK,metode_MODE);
        if(!Fout)Fout=assh_service_register_va(Konteks_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=mobiel_Sleutel;
        if(!Fout)Fout=assh_key_load(Konteks_VALUE,assh_context_keys(Konteks_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(mobiel_Sleutel));
        if(Fout){진단("SSH init error ",Fout);assh_context_release(Konteks_VALUE);Konteks_VALUE=0;return -5;}
    }
    int ombou_VALUE=통신끝점만들기(1);if(ombou_VALUE<0)return ombou_VALUE;통신주소재사용(ombou_VALUE);
    int maatreël=망주소묶기(ombou_VALUE,0,22);if(!maatreël)maatreël=연결기다리기(ombou_VALUE);
    if(maatreël<0){sluit_Netwerk(ombou_VALUE);return maatreël;}듣는곳=ombou_VALUE;return 0;
}
uintptr_t bord_skaduwing(uintptr_t 종류,uintptr_t Aksie) {
    if(종류==1)return(uint32_t)kontrole_afstands_wys(Aksie);
    if(Aksie==0){sluit_verbinding();if(듣는곳>=0)sluit_Netwerk(듣는곳);듣는곳=-1;return 0;}
    if(Aksie==1){selflaai_fout=Maak_gereed_dop();return(uint32_t)selflaai_fout;}
    return(uint32_t)(듣는곳>=0?1:selflaai_fout);
}
void Maak_gereed_afstands(void){selflaai_fout=Maak_gereed_dop();kontrole_afstands_wys(1);}
static int 같은말(const struct assh_cbuffer_s *data,const char *Word_SMS) {
    size_t lengte_VALUE=strlen(Word_SMS);return data->size==lengte_VALUE&&!memcmp(data->data,Word_SMS,lengte_VALUE);
}
static int 터미널요청(const struct assh_cbuffer_s *data) {
    if(data->size<24)return 0;
    const unsigned char *data_plaas=data->data;unsigned lengte_VALUE=assh_load_u32(data_plaas);
    if(lengte_VALUE>128||data->size<lengte_VALUE+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(data_plaas+4+lengte_VALUE+16);
    return MODE_VALUE<=2048&&data->size==lengte_VALUE+24+MODE_VALUE;
}
static void 요청처리(struct assh_event_request_s *gebeurtenis) {
    if(!인증됨||gebeurtenis->ch!=kanaal_inskrywing||!kanaal_inskrywing)return;
    if(같은말(&gebeurtenis->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&gebeurtenis->rq_data))gebeurtenis->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&gebeurtenis->type,"window-change")) {
        if(셸시작됨&&gebeurtenis->rq_data.size==16)gebeurtenis->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!dop_Besig_om_te_wag)return;
    const unsigned char *Opdrag=0;unsigned lengte_VALUE=0;
    if(같은말(&gebeurtenis->type,"exec")) {
        if(gebeurtenis->rq_data.size<4)return;
        lengte_VALUE=assh_load_u32(gebeurtenis->rq_data.data);
        if(!lengte_VALUE||lengte_VALUE>2048||gebeurtenis->rq_data.size!=lengte_VALUE+4)return;
        Opdrag=gebeurtenis->rq_data.data+4;
        for(unsigned 순번=0;순번<lengte_VALUE;순번++)if(!Opdrag[순번])return;
        bevel_TYPE=1;
    }else if(!같은말(&gebeurtenis->type,"shell")||gebeurtenis->rq_data.size)return;
    if(sizeof(입력줄)-입력수<lengte_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(lengte_VALUE)원격입력넣기(Opdrag,lengte_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;gebeurtenis->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!bevel_TYPE){const char *README_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*README_eb81d7d9)원격출력(*README_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t NOU_VALUE=보드밀리초();
    if(portuur_VALUE<0){if(NOU_VALUE<재접속시각)return;portuur_VALUE=망연결받기(듣는곳);if(portuur_VALUE<0)return;
        verbinding_tyd=NOU_VALUE;assh_status_t Fout=assh_session_create(Konteks_VALUE,&verbinding_e05f319b);
        if(Fout){verbinding_e05f319b=0;진단("SSH session error ",Fout);sluit_verbinding();return;}}
    if((!인증됨&&NOU_VALUE-verbinding_tyd>30000)||닫을예정==2||(닫을예정&&NOU_VALUE>=닫는시각)){sluit_verbinding();return;}
    if(kanaal_inskrywing&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Fout=assh_channel_data(kanaal_inskrywing,출력줄+출력앞,&수);
            if(!Fout){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Fout!=ASSH_NO_DATA){sluit_verbinding();return;}
        }
        if(beëindig_stand>=0&&!출력수){unsigned char stand_VALUE[4];assh_store_u32(stand_VALUE,(uint32_t)beëindig_stand);
            if(assh_request(verbinding_e05f319b,kanaal_inskrywing,"exit-status",11,stand_VALUE,4,0)||assh_channel_eof(kanaal_inskrywing)||assh_channel_close(kanaal_inskrywing)) {sluit_verbinding();return;}
            닫을예정=1;닫는시각=NOU_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s gebeurtenis;
        if(!assh_event_get(verbinding_e05f319b,&gebeurtenis,NOU_VALUE/1000)){sluit_verbinding();return;}
        assh_status_t Fout=ASSH_OK;int 쉬기=0,끊기=0;
        switch(gebeurtenis.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(portuur_VALUE,gebeurtenis.transport.read.buf.data,gebeurtenis.transport.read.buf.size);
            if(수>0)gebeurtenis.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(portuur_VALUE,gebeurtenis.transport.write.buf.data,gebeurtenis.transport.write.buf.size);
            if(수>0)gebeurtenis.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            gebeurtenis.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(gebeurtenis.userauth_server.methods.retries>3)gebeurtenis.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *data=&gebeurtenis.userauth_server.password;
            if(같은말(&data->username,"user")&&data->password.size<=256&&!data->new_password.size) {
                unsigned char 요약[32];원격요약(data->password.data,data->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)data->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *data=&gebeurtenis.connection.channel_open;
            if(인증됨&&!kanaal_inskrywing&&dop_Besig_om_te_wag&&같은말(&data->type,"session")&&!data->rq_data.size) {
                data->reply=ASSH_CONNECTION_REPLY_SUCCESS;data->pkt_size=4096;
                data->win_size=-1;kanaal_inskrywing=data->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&gebeurtenis.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *data=&gebeurtenis.connection.channel_data;
            if(!셸시작됨||data->ch!=kanaal_inskrywing||data->ext){끊기=1;break;}
            unsigned 수=data->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(data->data.data[순번]==4){beëindig_stand=0;수=순번;data->transferred=data->data.size;break;}
            원격입력넣기(data->data.data,수);if(!data->transferred)data->transferred=수;
            if(!수&&beëindig_stand<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: kanaal_inskrywing=0;셸시작됨=0;닫을예정=1;닫는시각=NOU_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",gebeurtenis.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(verbinding_e05f319b,&gebeurtenis,Fout);
        if(끊기){sluit_verbinding();return;}if(쉬기)return;
    }
}
