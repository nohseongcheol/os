/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "kure_agaciro.h"
#include "암호기반.h"
#include "Umwirondoro.h"
#include "../Urusobemiyoboro_Ikirundo/Urusobemiyoboro_Ikirundo.h"
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
static struct assh_context_s *Imikoreshereze_agaciro;
static struct assh_session_s *kwihuza_e05f319b;
static struct assh_channel_s *umurongo_icyinjizwa;
static int 듣는곳=-1,Mugenzi_agaciro=-1,인증됨,셸시작됨,명령형,kurangiza_imimerere=-1,닫을예정,iyatsa_ikosa,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Ijambo_SMS,unsigned agaciro) {
    while(*Ijambo_SMS)보드글자쓰기(*Ijambo_SMS++);
    char umubare_agaciro[12];unsigned 수=0;do{umubare_agaciro[수++]='0'+agaciro%10;agaciro/=10;}while(agaciro);
    while(수)보드글자쓰기(umubare_agaciro[--수]);보드글자쓰기(10);
}
static assh_status_t Gutegura_ububiko(void *amakurushingiro,void **aderesi,size_t Ingano,enum assh_alloc_type_e 종류) {
    (void)amakurushingiro;(void)종류;
    if(!Ingano){kurekura_kure(*aderesi);*aderesi=0;return ASSH_OK;}
    void *새주소=원격재할당(*aderesi,Ingano);
    if(!새주소)return ASSH_ERR_MEM;*aderesi=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *amakurushingiro,const struct assh_buffer_s *amakuru_agaciro) {
    (void)amakurushingiro;(void)amakuru_agaciro;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *amakurushingiro,uint8_t *결과,size_t uburebure_agaciro,uint_fast8_t 종류) {
    (void)amakurushingiro;(void)종류;if(uburebure_agaciro>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,uburebure_agaciro)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *amakurushingiro){(void)amakurushingiro;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void gufunga_kwihuza(void) {
    인증됨=셸시작됨=0;umurongo_icyinjizwa=0;
    if(kwihuza_e05f319b)assh_session_release(kwihuza_e05f319b);kwihuza_e05f319b=0;
    if(Mugenzi_agaciro>=0)gufunga_Urusobemiyoboro(Mugenzi_agaciro);Mugenzi_agaciro=-1;명령형=0;kurangiza_imimerere=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *amakurushingiro,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=amakurushingiro[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int inyuguti_agaciro=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return inyuguti_agaciro;
}
void 원격출력(unsigned char inyuguti_agaciro) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=inyuguti_agaciro==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=inyuguti_agaciro;이전출력=inyuguti_agaciro;
}
uintptr_t 보드원격명령끝(uintptr_t imimerere_agaciro){if(셸시작됨&&명령형)kurangiza_imimerere=(int)imimerere_agaciro;return 0;}
uintptr_t 보드원격대기(uintptr_t imimerere_agaciro){셸대기중=imimerere_agaciro!=0;return 0;}
static int Gutegura_insomamabwiriza(void) {
    if(듣는곳>=0)return 0;
    if(!Imikoreshereze_agaciro){
        assh_status_t IKOSA=assh_context_create(&Imikoreshereze_agaciro,ASSH_SERVER,Gutegura_ububiko,0,&난수기,0);
        if(IKOSA)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *uburyo_uburyo[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        IKOSA=assh_algo_register(Imikoreshereze_agaciro,ASSH_SAFETY_WEAK,uburyo_uburyo);
        if(!IKOSA)IKOSA=assh_service_register_va(Imikoreshereze_agaciro,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=igendanwa_buto;
        if(!IKOSA)IKOSA=assh_key_load(Imikoreshereze_agaciro,assh_context_keys(Imikoreshereze_agaciro),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(igendanwa_buto));
        if(IKOSA){진단("SSH init error ",IKOSA);assh_context_release(Imikoreshereze_agaciro);Imikoreshereze_agaciro=0;return -5;}
    }
    int poti_agaciro=통신끝점만들기(1);if(poti_agaciro<0)return poti_agaciro;통신주소재사용(poti_agaciro);
    int 결과=망주소묶기(poti_agaciro,0,22);if(!결과)결과=연결기다리기(poti_agaciro);
    if(결과<0){gufunga_Urusobemiyoboro(poti_agaciro);return 결과;}듣는곳=poti_agaciro;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t Igikorwa) {
    if(종류==1)return(uint32_t)icunga_kure_kwerekana(Igikorwa);
    if(Igikorwa==0){gufunga_kwihuza();if(듣는곳>=0)gufunga_Urusobemiyoboro(듣는곳);듣는곳=-1;return 0;}
    if(Igikorwa==1){iyatsa_ikosa=Gutegura_insomamabwiriza();return(uint32_t)iyatsa_ikosa;}
    return(uint32_t)(듣는곳>=0?1:iyatsa_ikosa);
}
void Gutegura_kure(void){iyatsa_ikosa=Gutegura_insomamabwiriza();icunga_kure_kwerekana(1);}
static int 같은말(const struct assh_cbuffer_s *amakurushingiro,const char *Ijambo_SMS) {
    size_t uburebure_agaciro=strlen(Ijambo_SMS);return amakurushingiro->size==uburebure_agaciro&&!memcmp(amakurushingiro->data,Ijambo_SMS,uburebure_agaciro);
}
static int 터미널요청(const struct assh_cbuffer_s *amakurushingiro) {
    if(amakurushingiro->size<24)return 0;
    const unsigned char *자료위치=amakurushingiro->data;unsigned uburebure_agaciro=assh_load_u32(자료위치);
    if(uburebure_agaciro>128||amakurushingiro->size<uburebure_agaciro+24)return 0;
    unsigned uburyo_agaciro_a83655ea=assh_load_u32(자료위치+4+uburebure_agaciro+16);
    return uburyo_agaciro_a83655ea<=2048&&amakurushingiro->size==uburebure_agaciro+24+uburyo_agaciro_a83655ea;
}
static void 요청처리(struct assh_event_request_s *icyabaye) {
    if(!인증됨||icyabaye->ch!=umurongo_icyinjizwa||!umurongo_icyinjizwa)return;
    if(같은말(&icyabaye->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&icyabaye->rq_data))icyabaye->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&icyabaye->type,"window-change")) {
        if(셸시작됨&&icyabaye->rq_data.size==16)icyabaye->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *Icyo_wifuza=0;unsigned uburebure_agaciro=0;
    if(같은말(&icyabaye->type,"exec")) {
        if(icyabaye->rq_data.size<4)return;
        uburebure_agaciro=assh_load_u32(icyabaye->rq_data.data);
        if(!uburebure_agaciro||uburebure_agaciro>2048||icyabaye->rq_data.size!=uburebure_agaciro+4)return;
        Icyo_wifuza=icyabaye->rq_data.data+4;
        for(unsigned 순번=0;순번<uburebure_agaciro;순번++)if(!Icyo_wifuza[순번])return;
        명령형=1;
    }else if(!같은말(&icyabaye->type,"shell")||icyabaye->rq_data.size)return;
    if(sizeof(입력줄)-입력수<uburebure_agaciro+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(uburebure_agaciro)원격입력넣기(Icyo_wifuza,uburebure_agaciro);원격입력넣기(&끝,1);
    셸시작됨=1;icyabaye->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!명령형){const char *NSOMA_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*NSOMA_eb81d7d9)원격출력(*NSOMA_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(Mugenzi_agaciro<0){if(지금<재접속시각)return;Mugenzi_agaciro=망연결받기(듣는곳);if(Mugenzi_agaciro<0)return;
        접속시각=지금;assh_status_t IKOSA=assh_session_create(Imikoreshereze_agaciro,&kwihuza_e05f319b);
        if(IKOSA){kwihuza_e05f319b=0;진단("SSH session error ",IKOSA);gufunga_kwihuza();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){gufunga_kwihuza();return;}
    if(umurongo_icyinjizwa&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t IKOSA=assh_channel_data(umurongo_icyinjizwa,출력줄+출력앞,&수);
            if(!IKOSA){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(IKOSA!=ASSH_NO_DATA){gufunga_kwihuza();return;}
        }
        if(kurangiza_imimerere>=0&&!출력수){unsigned char imimerere_agaciro[4];assh_store_u32(imimerere_agaciro,(uint32_t)kurangiza_imimerere);
            if(assh_request(kwihuza_e05f319b,umurongo_icyinjizwa,"exit-status",11,imimerere_agaciro,4,0)||assh_channel_eof(umurongo_icyinjizwa)||assh_channel_close(umurongo_icyinjizwa)) {gufunga_kwihuza();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned URUKURIKIRANE_agaciro=0;URUKURIKIRANE_agaciro<16;URUKURIKIRANE_agaciro++) {
        struct assh_event_s icyabaye;
        if(!assh_event_get(kwihuza_e05f319b,&icyabaye,지금/1000)){gufunga_kwihuza();return;}
        assh_status_t IKOSA=ASSH_OK;int 쉬기=0,끊기=0;
        switch(icyabaye.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(Mugenzi_agaciro,icyabaye.transport.read.buf.data,icyabaye.transport.read.buf.size);
            if(수>0)icyabaye.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(Mugenzi_agaciro,icyabaye.transport.write.buf.data,icyabaye.transport.write.buf.size);
            if(수>0)icyabaye.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            icyabaye.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(icyabaye.userauth_server.methods.retries>3)icyabaye.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *amakurushingiro=&icyabaye.userauth_server.password;
            if(같은말(&amakurushingiro->username,"user")&&amakurushingiro->password.size<=256&&!amakurushingiro->new_password.size) {
                unsigned char 요약[32];원격요약(amakurushingiro->password.data,amakurushingiro->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)amakurushingiro->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *amakurushingiro=&icyabaye.connection.channel_open;
            if(인증됨&&!umurongo_icyinjizwa&&셸대기중&&같은말(&amakurushingiro->type,"session")&&!amakurushingiro->rq_data.size) {
                amakurushingiro->reply=ASSH_CONNECTION_REPLY_SUCCESS;amakurushingiro->pkt_size=4096;
                amakurushingiro->win_size=-1;umurongo_icyinjizwa=amakurushingiro->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&icyabaye.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *amakurushingiro=&icyabaye.connection.channel_data;
            if(!셸시작됨||amakurushingiro->ch!=umurongo_icyinjizwa||amakurushingiro->ext){끊기=1;break;}
            unsigned 수=amakurushingiro->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(amakurushingiro->data.data[순번]==4){kurangiza_imimerere=0;수=순번;amakurushingiro->transferred=amakurushingiro->data.size;break;}
            원격입력넣기(amakurushingiro->data.data,수);if(!amakurushingiro->transferred)amakurushingiro->transferred=수;
            if(!수&&kurangiza_imimerere<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: umurongo_icyinjizwa=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",icyabaye.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(kwihuza_e05f319b,&icyabaye,IKOSA);
        if(끊기){gufunga_kwihuza();return;}if(쉬기)return;
    }
}
