/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "fjartengdur_VALUE.h"
#include "암호기반.h"
#include "prófíll.h"
#include "../Net_bunki/Net_bunki.h"
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
static struct assh_context_s *Samhengi_VALUE;
static struct assh_session_s *tenging_e05f319b;
static struct assh_channel_s *rás_færsla;
static int Hlustar_endastöð=-1,jafningi_VALUE=-1,인증됨,셸시작됨,skipun_TYPE,ljúka_staða_2bce2943=-1,닫을예정,ræsa_villa,skel_Bíður;
static uintptr_t tenging_TIME,재접속시각,lokun_TIME;
static unsigned char 입력줄[8192],úttak_lína[65536];
static unsigned 입력앞,입력수,출력앞,úttak_COUNT,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char tölustafur_VALUE[12];unsigned númer=0;do{tölustafur_VALUE[númer++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(númer)보드글자쓰기(tölustafur_VALUE[--númer]);보드글자쓰기(10);
}
static assh_status_t Undirbúa_Minni(void *gögn,void **slóð,size_t Stærð,enum assh_alloc_type_e 종류) {
    (void)gögn;(void)종류;
    if(!Stærð){losa_fjartengdur(*slóð);*slóð=0;return ASSH_OK;}
    void *새주소=원격재할당(*slóð,Stærð);
    if(!새주소)return ASSH_ERR_MEM;*slóð=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *gögn,const struct assh_buffer_s *fræ_VALUE) {
    (void)gögn;(void)fræ_VALUE;unsigned char 시험[32];int NIÐURSTAÐA=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return NIÐURSTAÐA?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *gögn,uint8_t *NIÐURSTAÐA,size_t lengd_VALUE,uint_fast8_t 종류) {
    (void)gögn;(void)종류;if(lengd_VALUE>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(NIÐURSTAÐA,lengd_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *gögn){(void)gögn;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void loka_tenging(void) {
    인증됨=셸시작됨=0;rás_færsla=0;
    if(tenging_e05f319b)assh_session_release(tenging_e05f319b);tenging_e05f319b=0;
    if(jafningi_VALUE>=0)loka_Net(jafningi_VALUE);jafningi_VALUE=-1;skipun_TYPE=0;ljúka_staða_2bce2943=-1;닫을예정=0;
    입력앞=입력수=출력앞=úttak_COUNT=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *gögn,unsigned númer) {
    if(númer>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<númer;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=gögn[순번];return númer;
}
int 원격입력(void) {
    if(!입력수)return -1;int stafur_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return stafur_VALUE;
}
void fjartengdur_úttak(unsigned char stafur_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=stafur_VALUE==10&&이전출력!=13;
    if(úttak_COUNT+1+덧붙임>sizeof(úttak_lína)){닫을예정=2;return;}
    if(덧붙임)úttak_lína[(출력앞+úttak_COUNT++)%sizeof(úttak_lína)]=13;
    úttak_lína[(출력앞+úttak_COUNT++)%sizeof(úttak_lína)]=stafur_VALUE;이전출력=stafur_VALUE;
}
uintptr_t bretti_ljúka_fjartengdur_skipun(uintptr_t staða_VALUE_e10195a1){if(셸시작됨&&skipun_TYPE)ljúka_staða_2bce2943=(int)staða_VALUE_e10195a1;return 0;}
uintptr_t bretti_fjartengdur_Bíddu(uintptr_t staða_VALUE_e10195a1){skel_Bíður=staða_VALUE_e10195a1!=0;return 0;}
static int Undirbúa_skel(void) {
    if(Hlustar_endastöð>=0)return 0;
    if(!Samhengi_VALUE){
        assh_status_t Villa=assh_context_create(&Samhengi_VALUE,ASSH_SERVER,Undirbúa_Minni,0,&난수기,0);
        if(Villa)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *aðferð_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Villa=assh_algo_register(Samhengi_VALUE,ASSH_SAFETY_WEAK,aðferð_MODE);
        if(!Villa)Villa=assh_service_register_va(Samhengi_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=tæki_Lykill;
        if(!Villa)Villa=assh_key_load(Samhengi_VALUE,assh_context_keys(Samhengi_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(tæki_Lykill));
        if(Villa){진단("SSH init error ",Villa);assh_context_release(Samhengi_VALUE);Samhengi_VALUE=0;return -5;}
    }
    int gátt_VALUE=통신끝점만들기(1);if(gátt_VALUE<0)return gátt_VALUE;통신주소재사용(gátt_VALUE);
    int NIÐURSTAÐA=nettó_BIND(gátt_VALUE,0,22);if(!NIÐURSTAÐA)NIÐURSTAÐA=nettó_hlusta(gátt_VALUE);
    if(NIÐURSTAÐA<0){loka_Net(gátt_VALUE);return NIÐURSTAÐA;}Hlustar_endastöð=gátt_VALUE;return 0;
}
uintptr_t bretti_fjarvöktun(uintptr_t 종류,uintptr_t Aðgerð) {
    if(종류==1)return(uint32_t)stýring_fjartengdur_birta(Aðgerð);
    if(Aðgerð==0){loka_tenging();if(Hlustar_endastöð>=0)loka_Net(Hlustar_endastöð);Hlustar_endastöð=-1;return 0;}
    if(Aðgerð==1){ræsa_villa=Undirbúa_skel();return(uint32_t)ræsa_villa;}
    return(uint32_t)(Hlustar_endastöð>=0?1:ræsa_villa);
}
void Undirbúa_fjartengdur(void){ræsa_villa=Undirbúa_skel();stýring_fjartengdur_birta(1);}
static int samsvörun_Word(const struct assh_cbuffer_s *gögn,const char *Word_SMS) {
    size_t lengd_VALUE=strlen(Word_SMS);return gögn->size==lengd_VALUE&&!memcmp(gögn->data,Word_SMS,lengd_VALUE);
}
static int 터미널요청(const struct assh_cbuffer_s *gögn) {
    if(gögn->size<24)return 0;
    const unsigned char *gögn_staða=gögn->data;unsigned lengd_VALUE=assh_load_u32(gögn_staða);
    if(lengd_VALUE>128||gögn->size<lengd_VALUE+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(gögn_staða+4+lengd_VALUE+16);
    return MODE_VALUE<=2048&&gögn->size==lengd_VALUE+24+MODE_VALUE;
}
static void 요청처리(struct assh_event_request_s *atvik) {
    if(!인증됨||atvik->ch!=rás_færsla||!rás_færsla)return;
    if(samsvörun_Word(&atvik->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&atvik->rq_data))atvik->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(samsvörun_Word(&atvik->type,"window-change")) {
        if(셸시작됨&&atvik->rq_data.size==16)atvik->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!skel_Bíður)return;
    const unsigned char *Skipun=0;unsigned lengd_VALUE=0;
    if(samsvörun_Word(&atvik->type,"exec")) {
        if(atvik->rq_data.size<4)return;
        lengd_VALUE=assh_load_u32(atvik->rq_data.data);
        if(!lengd_VALUE||lengd_VALUE>2048||atvik->rq_data.size!=lengd_VALUE+4)return;
        Skipun=atvik->rq_data.data+4;
        for(unsigned 순번=0;순번<lengd_VALUE;순번++)if(!Skipun[순번])return;
        skipun_TYPE=1;
    }else if(!samsvörun_Word(&atvik->type,"shell")||atvik->rq_data.size)return;
    if(sizeof(입력줄)-입력수<lengd_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(lengd_VALUE)원격입력넣기(Skipun,lengd_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;atvik->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!skipun_TYPE){const char *LESTUMIG_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*LESTUMIG_eb81d7d9)fjartengdur_úttak(*LESTUMIG_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Hlustar_endastöð<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(jafningi_VALUE<0){if(NOW_VALUE<재접속시각)return;jafningi_VALUE=nettó_samþykkja(Hlustar_endastöð);if(jafningi_VALUE<0)return;
        tenging_TIME=NOW_VALUE;assh_status_t Villa=assh_session_create(Samhengi_VALUE,&tenging_e05f319b);
        if(Villa){tenging_e05f319b=0;진단("SSH session error ",Villa);loka_tenging();return;}}
    if((!인증됨&&NOW_VALUE-tenging_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=lokun_TIME)){loka_tenging();return;}
    if(rás_færsla&&셸시작됨&&!닫을예정) {
        if(úttak_COUNT){size_t númer=sizeof(úttak_lína)-출력앞;if(númer>úttak_COUNT)númer=úttak_COUNT;if(númer>2048)númer=2048;
            assh_status_t Villa=assh_channel_data(rás_færsla,úttak_lína+출력앞,&númer);
            if(!Villa){출력앞=(출력앞+númer)%sizeof(úttak_lína);úttak_COUNT-=númer;}
            else if(Villa!=ASSH_NO_DATA){loka_tenging();return;}
        }
        if(ljúka_staða_2bce2943>=0&&!úttak_COUNT){unsigned char staða_VALUE_e10195a1[4];assh_store_u32(staða_VALUE_e10195a1,(uint32_t)ljúka_staða_2bce2943);
            if(assh_request(tenging_e05f319b,rás_færsla,"exit-status",11,staða_VALUE_e10195a1,4,0)||assh_channel_eof(rás_færsla)||assh_channel_close(rás_færsla)) {loka_tenging();return;}
            닫을예정=1;lokun_TIME=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s atvik;
        if(!assh_event_get(tenging_e05f319b,&atvik,NOW_VALUE/1000)){loka_tenging();return;}
        assh_status_t Villa=ASSH_OK;int 쉬기=0,aftengja_endastöð=0;
        switch(atvik.id) {
        case ASSH_EVENT_READ: {
            int númer=통신읽기(jafningi_VALUE,atvik.transport.read.buf.data,atvik.transport.read.buf.size);
            if(númer>0)atvik.transport.read.transferred=númer;
            else if(númer==-11)쉬기=1;else aftengja_endastöð=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int númer=nettó_skrifa(jafningi_VALUE,atvik.transport.write.buf.data,atvik.transport.write.buf.size);
            if(númer>0)atvik.transport.write.transferred=númer;
            else if(númer==-11)쉬기=1;else aftengja_endastöð=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            atvik.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(atvik.userauth_server.methods.retries>3)atvik.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *gögn=&atvik.userauth_server.password;
            if(samsvörun_Word(&gögn->username,"user")&&gögn->password.size<=256&&!gögn->new_password.size) {
                unsigned char samantekt_VALUE[32];fjartengdur_samantekt(gögn->password.data,gögn->password.size,samantekt_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=samantekt_VALUE[순번]^skel_aðgangsorð_samantekt[순번];memset(samantekt_VALUE,0,32);
                if(!차이)gögn->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *gögn=&atvik.connection.channel_open;
            if(인증됨&&!rás_færsla&&skel_Bíður&&samsvörun_Word(&gögn->type,"session")&&!gögn->rq_data.size) {
                gögn->reply=ASSH_CONNECTION_REPLY_SUCCESS;gögn->pkt_size=4096;
                gögn->win_size=-1;rás_færsla=gögn->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&atvik.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *gögn=&atvik.connection.channel_data;
            if(!셸시작됨||gögn->ch!=rás_færsla||gögn->ext){aftengja_endastöð=1;break;}
            unsigned númer=gögn->data.size;if(númer>sizeof(입력줄)-입력수)númer=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<númer;순번++)if(gögn->data.data[순번]==4){ljúka_staða_2bce2943=0;númer=순번;gögn->transferred=gögn->data.size;break;}
            원격입력넣기(gögn->data.data,númer);if(!gögn->transferred)gögn->transferred=númer;
            if(!númer&&ljúka_staða_2bce2943<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: rás_færsla=0;셸시작됨=0;닫을예정=1;lokun_TIME=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",atvik.session.error.code);aftengja_endastöð=1;break;
        case ASSH_EVENT_DISCONNECT: aftengja_endastöð=1;break;
        default: break;
        }
        assh_event_done(tenging_e05f319b,&atvik,Villa);
        if(aftengja_endastöð){loka_tenging();return;}if(쉬기)return;
    }
}
