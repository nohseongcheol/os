/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "kgakala_Boleng.h"
#include "암호기반.h"
#include "Porofaele.h"
#include "../Neteweke_kokoanyodinepe/Neteweke_kokoanyodinepe.h"
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
static struct assh_context_s *bokao_Boleng;
static struct assh_session_s *Kgolagano_e05f319b;
static struct assh_channel_s *mosele_tsenyo;
static int 듣는곳=-1,semphato_Boleng=-1,인증됨,셸시작됨,Taelo_tlanya,kgaola_kemo=-1,닫을예정,tshimologosešwa_phoso,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Lefoko_SMS,unsigned Boleng) {
    while(*Lefoko_SMS)보드글자쓰기(*Lefoko_SMS++);
    char dijite_Boleng[12];unsigned 수=0;do{dijite_Boleng[수++]='0'+Boleng%10;Boleng/=10;}while(Boleng);
    while(수)보드글자쓰기(dijite_Boleng[--수]);보드글자쓰기(10);
}
static assh_status_t Baakanya_memori(void *tshedimosetso,void **aterese,size_t lekanya,enum assh_alloc_type_e 종류) {
    (void)tshedimosetso;(void)종류;
    if(!lekanya){ntsha_kgakala(*aterese);*aterese=0;return ASSH_OK;}
    void *새주소=원격재할당(*aterese,lekanya);
    if(!새주소)return ASSH_ERR_MEM;*aterese=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *tshedimosetso,const struct assh_buffer_s *peo_Boleng) {
    (void)tshedimosetso;(void)peo_Boleng;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *tshedimosetso,uint8_t *결과,size_t boleele_Boleng,uint_fast8_t 종류) {
    (void)tshedimosetso;(void)종류;if(boleele_Boleng>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,boleele_Boleng)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *tshedimosetso){(void)tshedimosetso;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void tswala_Kgolagano(void) {
    인증됨=셸시작됨=0;mosele_tsenyo=0;
    if(Kgolagano_e05f319b)assh_session_release(Kgolagano_e05f319b);Kgolagano_e05f319b=0;
    if(semphato_Boleng>=0)tswala_Neteweke(semphato_Boleng);semphato_Boleng=-1;Taelo_tlanya=0;kgaola_kemo=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *tshedimosetso,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=tshedimosetso[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int Letshwao_Boleng=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return Letshwao_Boleng;
}
void 원격출력(unsigned char Letshwao_Boleng) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=Letshwao_Boleng==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=Letshwao_Boleng;이전출력=Letshwao_Boleng;
}
uintptr_t 보드원격명령끝(uintptr_t kemo_Boleng){if(셸시작됨&&Taelo_tlanya)kgaola_kemo=(int)kemo_Boleng;return 0;}
uintptr_t 보드원격대기(uintptr_t kemo_Boleng){셸대기중=kemo_Boleng!=0;return 0;}
static int Baakanya_setlhalosataelo(void) {
    if(듣는곳>=0)return 0;
    if(!bokao_Boleng){
        assh_status_t phoso=assh_context_create(&bokao_Boleng,ASSH_SERVER,Baakanya_memori,0,&난수기,0);
        if(phoso)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *mokgwa_mokgwa[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        phoso=assh_algo_register(bokao_Boleng,ASSH_SAFETY_WEAK,mokgwa_mokgwa);
        if(!phoso)phoso=assh_service_register_va(bokao_Boleng,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=mobaele_taetsi;
        if(!phoso)phoso=assh_key_load(bokao_Boleng,assh_context_keys(bokao_Boleng),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(mobaele_taetsi));
        if(phoso){진단("SSH init error ",phoso);assh_context_release(bokao_Boleng);bokao_Boleng=0;return -5;}
    }
    int gorogisetsa_Boleng=통신끝점만들기(1);if(gorogisetsa_Boleng<0)return gorogisetsa_Boleng;통신주소재사용(gorogisetsa_Boleng);
    int 결과=망주소묶기(gorogisetsa_Boleng,0,22);if(!결과)결과=연결기다리기(gorogisetsa_Boleng);
    if(결과<0){tswala_Neteweke(gorogisetsa_Boleng);return 결과;}듣는곳=gorogisetsa_Boleng;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t tiro) {
    if(종류==1)return(uint32_t)taolo_kgakala_bontsha(tiro);
    if(tiro==0){tswala_Kgolagano();if(듣는곳>=0)tswala_Neteweke(듣는곳);듣는곳=-1;return 0;}
    if(tiro==1){tshimologosešwa_phoso=Baakanya_setlhalosataelo();return(uint32_t)tshimologosešwa_phoso;}
    return(uint32_t)(듣는곳>=0?1:tshimologosešwa_phoso);
}
void Baakanya_kgakala(void){tshimologosešwa_phoso=Baakanya_setlhalosataelo();taolo_kgakala_bontsha(1);}
static int 같은말(const struct assh_cbuffer_s *tshedimosetso,const char *Lefoko_SMS) {
    size_t boleele_Boleng=strlen(Lefoko_SMS);return tshedimosetso->size==boleele_Boleng&&!memcmp(tshedimosetso->data,Lefoko_SMS,boleele_Boleng);
}
static int 터미널요청(const struct assh_cbuffer_s *tshedimosetso) {
    if(tshedimosetso->size<24)return 0;
    const unsigned char *자료위치=tshedimosetso->data;unsigned boleele_Boleng=assh_load_u32(자료위치);
    if(boleele_Boleng>128||tshedimosetso->size<boleele_Boleng+24)return 0;
    unsigned mokgwa_Boleng_a83655ea=assh_load_u32(자료위치+4+boleele_Boleng+16);
    return mokgwa_Boleng_a83655ea<=2048&&tshedimosetso->size==boleele_Boleng+24+mokgwa_Boleng_a83655ea;
}
static void 요청처리(struct assh_event_request_s *tiragalo) {
    if(!인증됨||tiragalo->ch!=mosele_tsenyo||!mosele_tsenyo)return;
    if(같은말(&tiragalo->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&tiragalo->rq_data))tiragalo->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&tiragalo->type,"window-change")) {
        if(셸시작됨&&tiragalo->rq_data.size==16)tiragalo->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *Taelo=0;unsigned boleele_Boleng=0;
    if(같은말(&tiragalo->type,"exec")) {
        if(tiragalo->rq_data.size<4)return;
        boleele_Boleng=assh_load_u32(tiragalo->rq_data.data);
        if(!boleele_Boleng||boleele_Boleng>2048||tiragalo->rq_data.size!=boleele_Boleng+4)return;
        Taelo=tiragalo->rq_data.data+4;
        for(unsigned 순번=0;순번<boleele_Boleng;순번++)if(!Taelo[순번])return;
        Taelo_tlanya=1;
    }else if(!같은말(&tiragalo->type,"shell")||tiragalo->rq_data.size)return;
    if(sizeof(입력줄)-입력수<boleele_Boleng+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(boleele_Boleng)원격입력넣기(Taelo,boleele_Boleng);원격입력넣기(&끝,1);
    셸시작됨=1;tiragalo->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!Taelo_tlanya){const char *MPUISE_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*MPUISE_eb81d7d9)원격출력(*MPUISE_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(semphato_Boleng<0){if(지금<재접속시각)return;semphato_Boleng=망연결받기(듣는곳);if(semphato_Boleng<0)return;
        접속시각=지금;assh_status_t phoso=assh_session_create(bokao_Boleng,&Kgolagano_e05f319b);
        if(phoso){Kgolagano_e05f319b=0;진단("SSH session error ",phoso);tswala_Kgolagano();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){tswala_Kgolagano();return;}
    if(mosele_tsenyo&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t phoso=assh_channel_data(mosele_tsenyo,출력줄+출력앞,&수);
            if(!phoso){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(phoso!=ASSH_NO_DATA){tswala_Kgolagano();return;}
        }
        if(kgaola_kemo>=0&&!출력수){unsigned char kemo_Boleng[4];assh_store_u32(kemo_Boleng,(uint32_t)kgaola_kemo);
            if(assh_request(Kgolagano_e05f319b,mosele_tsenyo,"exit-status",11,kemo_Boleng,4,0)||assh_channel_eof(mosele_tsenyo)||assh_channel_close(mosele_tsenyo)) {tswala_Kgolagano();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned TATELANO_Boleng=0;TATELANO_Boleng<16;TATELANO_Boleng++) {
        struct assh_event_s tiragalo;
        if(!assh_event_get(Kgolagano_e05f319b,&tiragalo,지금/1000)){tswala_Kgolagano();return;}
        assh_status_t phoso=ASSH_OK;int 쉬기=0,끊기=0;
        switch(tiragalo.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(semphato_Boleng,tiragalo.transport.read.buf.data,tiragalo.transport.read.buf.size);
            if(수>0)tiragalo.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(semphato_Boleng,tiragalo.transport.write.buf.data,tiragalo.transport.write.buf.size);
            if(수>0)tiragalo.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            tiragalo.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(tiragalo.userauth_server.methods.retries>3)tiragalo.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *tshedimosetso=&tiragalo.userauth_server.password;
            if(같은말(&tshedimosetso->username,"user")&&tshedimosetso->password.size<=256&&!tshedimosetso->new_password.size) {
                unsigned char tshobokanyo_Boleng[32];kgakala_tshobokanyo(tshedimosetso->password.data,tshedimosetso->password.size,tshobokanyo_Boleng);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=tshobokanyo_Boleng[순번]^setlhalosataelo_khoututseno_tshobokanyo[순번];memset(tshobokanyo_Boleng,0,32);
                if(!차이)tshedimosetso->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *tshedimosetso=&tiragalo.connection.channel_open;
            if(인증됨&&!mosele_tsenyo&&셸대기중&&같은말(&tshedimosetso->type,"session")&&!tshedimosetso->rq_data.size) {
                tshedimosetso->reply=ASSH_CONNECTION_REPLY_SUCCESS;tshedimosetso->pkt_size=4096;
                tshedimosetso->win_size=-1;mosele_tsenyo=tshedimosetso->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&tiragalo.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *tshedimosetso=&tiragalo.connection.channel_data;
            if(!셸시작됨||tshedimosetso->ch!=mosele_tsenyo||tshedimosetso->ext){끊기=1;break;}
            unsigned 수=tshedimosetso->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(tshedimosetso->data.data[순번]==4){kgaola_kemo=0;수=순번;tshedimosetso->transferred=tshedimosetso->data.size;break;}
            원격입력넣기(tshedimosetso->data.data,수);if(!tshedimosetso->transferred)tshedimosetso->transferred=수;
            if(!수&&kgaola_kemo<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: mosele_tsenyo=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",tiragalo.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(Kgolagano_e05f319b,&tiragalo,phoso);
        if(끊기){tswala_Kgolagano();return;}if(쉬기)return;
    }
}
