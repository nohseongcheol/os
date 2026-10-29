/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "ya_kgole_boleng.h"
#include "암호기반.h"
#include "Profaele.h"
#include "../Netweke_kgoboko/Netweke_kgoboko.h"
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
static struct assh_context_s *Kamano_boleng;
static struct assh_session_s *kgokaganya_e05f319b;
static struct assh_channel_s *mokero_go_tsenya_tshedimošo;
static int 듣는곳=-1,sedirišwa_sa_legoro_le_tee_boleng=-1,인증됨,셸시작됨,taelo_thaepa,fetša_boemo=-1,닫을예정,bula_phošo,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Thalokontšu_SMS,unsigned boleng) {
    while(*Thalokontšu_SMS)보드글자쓰기(*Thalokontšu_SMS++);
    char 숫자[12];unsigned 수=0;do{숫자[수++]='0'+boleng%10;boleng/=10;}while(boleng);
    while(수)보드글자쓰기(숫자[--수]);보드글자쓰기(10);
}
static assh_status_t Lokišetša_memori(void *data,void **atrese,size_t Bogolo,enum assh_alloc_type_e 종류) {
    (void)data;(void)종류;
    if(!Bogolo){lokolla_ya_kgole(*atrese);*atrese=0;return ASSH_OK;}
    void *새주소=원격재할당(*atrese,Bogolo);
    if(!새주소)return ASSH_ERR_MEM;*atrese=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *data,const struct assh_buffer_s *kalo_boleng) {
    (void)data;(void)kalo_boleng;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *data,uint8_t *결과,size_t botelele_boleng,uint_fast8_t 종류) {
    (void)data;(void)종류;if(botelele_boleng>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,botelele_boleng)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *data){(void)data;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void tswalela_kgokaganya(void) {
    인증됨=셸시작됨=0;mokero_go_tsenya_tshedimošo=0;
    if(kgokaganya_e05f319b)assh_session_release(kgokaganya_e05f319b);kgokaganya_e05f319b=0;
    if(sedirišwa_sa_legoro_le_tee_boleng>=0)tswalela_Netweke(sedirišwa_sa_legoro_le_tee_boleng);sedirišwa_sa_legoro_le_tee_boleng=-1;taelo_thaepa=0;fetša_boemo=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *data,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=data[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int tlhaka_boleng=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return tlhaka_boleng;
}
void 원격출력(unsigned char tlhaka_boleng) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=tlhaka_boleng==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=tlhaka_boleng;이전출력=tlhaka_boleng;
}
uintptr_t 보드원격명령끝(uintptr_t boemo_boleng){if(셸시작됨&&taelo_thaepa)fetša_boemo=(int)boemo_boleng;return 0;}
uintptr_t 보드원격대기(uintptr_t boemo_boleng){셸대기중=boemo_boleng!=0;return 0;}
static int Lokišetša_šele(void) {
    if(듣는곳>=0)return 0;
    if(!Kamano_boleng){
        assh_status_t Phošo=assh_context_create(&Kamano_boleng,ASSH_SERVER,Lokišetša_memori,0,&난수기,0);
        if(Phošo)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *mokgwa_mokgwa[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Phošo=assh_algo_register(Kamano_boleng,ASSH_SAFETY_WEAK,mokgwa_mokgwa);
        if(!Phošo)Phošo=assh_service_register_va(Kamano_boleng,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=sedirišwa_khii;
        if(!Phošo)Phošo=assh_key_load(Kamano_boleng,assh_context_keys(Kamano_boleng),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(sedirišwa_khii));
        if(Phošo){진단("SSH init error ",Phošo);assh_context_release(Kamano_boleng);Kamano_boleng=0;return -5;}
    }
    int phote_boleng=통신끝점만들기(1);if(phote_boleng<0)return phote_boleng;통신주소재사용(phote_boleng);
    int 결과=망주소묶기(phote_boleng,0,22);if(!결과)결과=연결기다리기(phote_boleng);
    if(결과<0){tswalela_Netweke(phote_boleng);return 결과;}듣는곳=phote_boleng;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t Mogato) {
    if(종류==1)return(uint32_t)taolo_ya_kgole_bontšha(Mogato);
    if(Mogato==0){tswalela_kgokaganya();if(듣는곳>=0)tswalela_Netweke(듣는곳);듣는곳=-1;return 0;}
    if(Mogato==1){bula_phošo=Lokišetša_šele();return(uint32_t)bula_phošo;}
    return(uint32_t)(듣는곳>=0?1:bula_phošo);
}
void Lokišetša_ya_kgole(void){bula_phošo=Lokišetša_šele();taolo_ya_kgole_bontšha(1);}
static int 같은말(const struct assh_cbuffer_s *data,const char *Thalokontšu_SMS) {
    size_t botelele_boleng=strlen(Thalokontšu_SMS);return data->size==botelele_boleng&&!memcmp(data->data,Thalokontšu_SMS,botelele_boleng);
}
static int 터미널요청(const struct assh_cbuffer_s *data) {
    if(data->size<24)return 0;
    const unsigned char *자료위치=data->data;unsigned botelele_boleng=assh_load_u32(자료위치);
    if(botelele_boleng>128||data->size<botelele_boleng+24)return 0;
    unsigned mokgwa_boleng_a83655ea=assh_load_u32(자료위치+4+botelele_boleng+16);
    return mokgwa_boleng_a83655ea<=2048&&data->size==botelele_boleng+24+mokgwa_boleng_a83655ea;
}
static void 요청처리(struct assh_event_request_s *tiragalo) {
    if(!인증됨||tiragalo->ch!=mokero_go_tsenya_tshedimošo||!mokero_go_tsenya_tshedimošo)return;
    if(같은말(&tiragalo->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&tiragalo->rq_data))tiragalo->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&tiragalo->type,"window-change")) {
        if(셸시작됨&&tiragalo->rq_data.size==16)tiragalo->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *Taelo=0;unsigned botelele_boleng=0;
    if(같은말(&tiragalo->type,"exec")) {
        if(tiragalo->rq_data.size<4)return;
        botelele_boleng=assh_load_u32(tiragalo->rq_data.data);
        if(!botelele_boleng||botelele_boleng>2048||tiragalo->rq_data.size!=botelele_boleng+4)return;
        Taelo=tiragalo->rq_data.data+4;
        for(unsigned 순번=0;순번<botelele_boleng;순번++)if(!Taelo[순번])return;
        taelo_thaepa=1;
    }else if(!같은말(&tiragalo->type,"shell")||tiragalo->rq_data.size)return;
    if(sizeof(입력줄)-입력수<botelele_boleng+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(botelele_boleng)원격입력넣기(Taelo,botelele_boleng);원격입력넣기(&끝,1);
    셸시작됨=1;tiragalo->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!taelo_thaepa){const char *faele_ya_MPALE_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*faele_ya_MPALE_eb81d7d9)원격출력(*faele_ya_MPALE_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(sedirišwa_sa_legoro_le_tee_boleng<0){if(지금<재접속시각)return;sedirišwa_sa_legoro_le_tee_boleng=망연결받기(듣는곳);if(sedirišwa_sa_legoro_le_tee_boleng<0)return;
        접속시각=지금;assh_status_t Phošo=assh_session_create(Kamano_boleng,&kgokaganya_e05f319b);
        if(Phošo){kgokaganya_e05f319b=0;진단("SSH session error ",Phošo);tswalela_kgokaganya();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){tswalela_kgokaganya();return;}
    if(mokero_go_tsenya_tshedimošo&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Phošo=assh_channel_data(mokero_go_tsenya_tshedimošo,출력줄+출력앞,&수);
            if(!Phošo){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Phošo!=ASSH_NO_DATA){tswalela_kgokaganya();return;}
        }
        if(fetša_boemo>=0&&!출력수){unsigned char boemo_boleng[4];assh_store_u32(boemo_boleng,(uint32_t)fetša_boemo);
            if(assh_request(kgokaganya_e05f319b,mokero_go_tsenya_tshedimošo,"exit-status",11,boemo_boleng,4,0)||assh_channel_eof(mokero_go_tsenya_tshedimošo)||assh_channel_close(mokero_go_tsenya_tshedimošo)) {tswalela_kgokaganya();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned TATELANO_boleng=0;TATELANO_boleng<16;TATELANO_boleng++) {
        struct assh_event_s tiragalo;
        if(!assh_event_get(kgokaganya_e05f319b,&tiragalo,지금/1000)){tswalela_kgokaganya();return;}
        assh_status_t Phošo=ASSH_OK;int 쉬기=0,끊기=0;
        switch(tiragalo.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(sedirišwa_sa_legoro_le_tee_boleng,tiragalo.transport.read.buf.data,tiragalo.transport.read.buf.size);
            if(수>0)tiragalo.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(sedirišwa_sa_legoro_le_tee_boleng,tiragalo.transport.write.buf.data,tiragalo.transport.write.buf.size);
            if(수>0)tiragalo.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            tiragalo.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(tiragalo.userauth_server.methods.retries>3)tiragalo.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *data=&tiragalo.userauth_server.password;
            if(같은말(&data->username,"user")&&data->password.size<=256&&!data->new_password.size) {
                unsigned char khutsofatšo_boleng[32];ya_kgole_khutsofatšo(data->password.data,data->password.size,khutsofatšo_boleng);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=khutsofatšo_boleng[순번]^šele_phasewete_khutsofatšo[순번];memset(khutsofatšo_boleng,0,32);
                if(!차이)data->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *data=&tiragalo.connection.channel_open;
            if(인증됨&&!mokero_go_tsenya_tshedimošo&&셸대기중&&같은말(&data->type,"session")&&!data->rq_data.size) {
                data->reply=ASSH_CONNECTION_REPLY_SUCCESS;data->pkt_size=4096;
                data->win_size=-1;mokero_go_tsenya_tshedimošo=data->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&tiragalo.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *data=&tiragalo.connection.channel_data;
            if(!셸시작됨||data->ch!=mokero_go_tsenya_tshedimošo||data->ext){끊기=1;break;}
            unsigned 수=data->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(data->data.data[순번]==4){fetša_boemo=0;수=순번;data->transferred=data->data.size;break;}
            원격입력넣기(data->data.data,수);if(!data->transferred)data->transferred=수;
            if(!수&&fetša_boemo<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: mokero_go_tsenya_tshedimošo=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",tiragalo.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(kgokaganya_e05f319b,&tiragalo,Phošo);
        if(끊기){tswalela_kgokaganya();return;}if(쉬기)return;
    }
}
