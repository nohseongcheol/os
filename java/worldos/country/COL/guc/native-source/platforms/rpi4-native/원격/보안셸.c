/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "원격.h"
#include "암호기반.h"
#include "ka_yataayakua_ipakalü.h"
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
static struct assh_session_s *epe_ipajia_e05f319b;
static struct assh_channel_s *kanaalü_ekeroliaa;
static int 듣는곳=-1,wanaawasü_ajutuu=-1,인증됨,셸시작됨,명령형,ajattiraa_jamakua_iparülein=-1,닫을예정,o_ttiriaa_ajachitia,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *말,unsigned ajutuu) {
    while(*말)보드글자쓰기(*말++);
    char 숫자[12];unsigned 수=0;do{숫자[수++]='0'+ajutuu%10;ajutuu/=10;}while(ajutuu);
    while(수)보드글자쓰기(숫자[--수]);보드글자쓰기(10);
}
static assh_status_t 기억마련(void *atijaaya,void **ejepüsee,size_t 크기,enum assh_alloc_type_e 종류) {
    (void)atijaaya;(void)종류;
    if(!크기){원격해제(*ejepüsee);*ejepüsee=0;return ASSH_OK;}
    void *새주소=원격재할당(*ejepüsee,크기);
    if(!새주소)return ASSH_ERR_MEM;*ejepüsee=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *atijaaya,const struct assh_buffer_s *씨앗) {
    (void)atijaaya;(void)씨앗;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *atijaaya,uint8_t *결과,size_t akaliaa_ajutuu,uint_fast8_t 종류) {
    (void)atijaaya;(void)종류;if(akaliaa_ajutuu>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,akaliaa_ajutuu)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *atijaaya){(void)atijaaya;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void asürülaa_epe_ipajia(void) {
    인증됨=셸시작됨=0;kanaalü_ekeroliaa=0;
    if(epe_ipajia_e05f319b)assh_session_release(epe_ipajia_e05f319b);epe_ipajia_e05f319b=0;
    if(wanaawasü_ajutuu>=0)asürülaa_kusu(wanaawasü_ajutuu);wanaawasü_ajutuu=-1;명령형=0;ajattiraa_jamakua_iparülein=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *atijaaya,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=atijaaya[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int jeerü_ajutuu=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return jeerü_ajutuu;
}
void 원격출력(unsigned char jeerü_ajutuu) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=jeerü_ajutuu==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=jeerü_ajutuu;이전출력=jeerü_ajutuu;
}
uintptr_t 보드원격명령끝(uintptr_t jamakua_iparülein_ajutuu){if(셸시작됨&&명령형)ajattiraa_jamakua_iparülein=(int)jamakua_iparülein_ajutuu;return 0;}
uintptr_t 보드원격대기(uintptr_t jamakua_iparülein_ajutuu){셸대기중=jamakua_iparülein_ajutuu!=0;return 0;}
static int 셸준비(void) {
    if(듣는곳>=0)return 0;
    if(!문맥){
        assh_status_t ajachitia=assh_context_create(&문맥,ASSH_SERVER,기억마련,0,&난수기,0);
        if(ajachitia)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *방식[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ajachitia=assh_algo_register(문맥,ASSH_SAFETY_WEAK,방식);
        if(!ajachitia)ajachitia=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=serulaalü_ajüttia;
        if(!ajachitia)ajachitia=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(serulaalü_ajüttia));
        if(ajachitia){진단("SSH init error ",ajachitia);assh_context_release(문맥);문맥=0;return -5;}
    }
    int outtülee_ajutuu=통신끝점만들기(1);if(outtülee_ajutuu<0)return outtülee_ajutuu;통신주소재사용(outtülee_ajutuu);
    int 결과=망주소묶기(outtülee_ajutuu,0,22);if(!결과)결과=연결기다리기(outtülee_ajutuu);
    if(결과<0){asürülaa_kusu(outtülee_ajutuu);return 결과;}듣는곳=outtülee_ajutuu;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t aa_inra_awai) {
    if(종류==1)return(uint32_t)원격화면제어(aa_inra_awai);
    if(aa_inra_awai==0){asürülaa_epe_ipajia();if(듣는곳>=0)asürülaa_kusu(듣는곳);듣는곳=-1;return 0;}
    if(aa_inra_awai==1){o_ttiriaa_ajachitia=셸준비();return(uint32_t)o_ttiriaa_ajachitia;}
    return(uint32_t)(듣는곳>=0?1:o_ttiriaa_ajachitia);
}
void 원격준비(void){o_ttiriaa_ajachitia=셸준비();원격화면제어(1);}
static int 같은말(const struct assh_cbuffer_s *atijaaya,const char *말) {
    size_t akaliaa_ajutuu=strlen(말);return atijaaya->size==akaliaa_ajutuu&&!memcmp(atijaaya->data,말,akaliaa_ajutuu);
}
static int 터미널요청(const struct assh_cbuffer_s *atijaaya) {
    if(atijaaya->size<24)return 0;
    const unsigned char *자료위치=atijaaya->data;unsigned akaliaa_ajutuu=assh_load_u32(자료위치);
    if(akaliaa_ajutuu>128||atijaaya->size<akaliaa_ajutuu+24)return 0;
    unsigned akua_ipaa_ajutuu_a83655ea=assh_load_u32(자료위치+4+akaliaa_ajutuu+16);
    return akua_ipaa_ajutuu_a83655ea<=2048&&atijaaya->size==akaliaa_ajutuu+24+akua_ipaa_ajutuu_a83655ea;
}
static void 요청처리(struct assh_event_request_s *kasachiki) {
    if(!인증됨||kasachiki->ch!=kanaalü_ekeroliaa||!kanaalü_ekeroliaa)return;
    if(같은말(&kasachiki->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&kasachiki->rq_data))kasachiki->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&kasachiki->type,"window-change")) {
        if(셸시작됨&&kasachiki->rq_data.size==16)kasachiki->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *aluwataaya=0;unsigned akaliaa_ajutuu=0;
    if(같은말(&kasachiki->type,"exec")) {
        if(kasachiki->rq_data.size<4)return;
        akaliaa_ajutuu=assh_load_u32(kasachiki->rq_data.data);
        if(!akaliaa_ajutuu||akaliaa_ajutuu>2048||kasachiki->rq_data.size!=akaliaa_ajutuu+4)return;
        aluwataaya=kasachiki->rq_data.data+4;
        for(unsigned 순번=0;순번<akaliaa_ajutuu;순번++)if(!aluwataaya[순번])return;
        명령형=1;
    }else if(!같은말(&kasachiki->type,"shell")||kasachiki->rq_data.size)return;
    if(sizeof(입력줄)-입력수<akaliaa_ajutuu+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(akaliaa_ajutuu)원격입력넣기(aluwataaya,akaliaa_ajutuu);원격입력넣기(&끝,1);
    셸시작됨=1;kasachiki->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!명령형){const char *PAASHAJE_ERAN_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*PAASHAJE_ERAN_eb81d7d9)원격출력(*PAASHAJE_ERAN_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(wanaawasü_ajutuu<0){if(지금<재접속시각)return;wanaawasü_ajutuu=망연결받기(듣는곳);if(wanaawasü_ajutuu<0)return;
        접속시각=지금;assh_status_t ajachitia=assh_session_create(문맥,&epe_ipajia_e05f319b);
        if(ajachitia){epe_ipajia_e05f319b=0;진단("SSH session error ",ajachitia);asürülaa_epe_ipajia();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){asürülaa_epe_ipajia();return;}
    if(kanaalü_ekeroliaa&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ajachitia=assh_channel_data(kanaalü_ekeroliaa,출력줄+출력앞,&수);
            if(!ajachitia){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ajachitia!=ASSH_NO_DATA){asürülaa_epe_ipajia();return;}
        }
        if(ajattiraa_jamakua_iparülein>=0&&!출력수){unsigned char jamakua_iparülein_ajutuu[4];assh_store_u32(jamakua_iparülein_ajutuu,(uint32_t)ajattiraa_jamakua_iparülein);
            if(assh_request(epe_ipajia_e05f319b,kanaalü_ekeroliaa,"exit-status",11,jamakua_iparülein_ajutuu,4,0)||assh_channel_eof(kanaalü_ekeroliaa)||assh_channel_close(kanaalü_ekeroliaa)) {asürülaa_epe_ipajia();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s kasachiki;
        if(!assh_event_get(epe_ipajia_e05f319b,&kasachiki,지금/1000)){asürülaa_epe_ipajia();return;}
        assh_status_t ajachitia=ASSH_OK;int 쉬기=0,끊기=0;
        switch(kasachiki.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(wanaawasü_ajutuu,kasachiki.transport.read.buf.data,kasachiki.transport.read.buf.size);
            if(수>0)kasachiki.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(wanaawasü_ajutuu,kasachiki.transport.write.buf.data,kasachiki.transport.write.buf.size);
            if(수>0)kasachiki.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            kasachiki.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(kasachiki.userauth_server.methods.retries>3)kasachiki.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *atijaaya=&kasachiki.userauth_server.password;
            if(같은말(&atijaaya->username,"user")&&atijaaya->password.size<=256&&!atijaaya->new_password.size) {
                unsigned char 요약[32];원격요약(atijaaya->password.data,atijaaya->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)atijaaya->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *atijaaya=&kasachiki.connection.channel_open;
            if(인증됨&&!kanaalü_ekeroliaa&&셸대기중&&같은말(&atijaaya->type,"session")&&!atijaaya->rq_data.size) {
                atijaaya->reply=ASSH_CONNECTION_REPLY_SUCCESS;atijaaya->pkt_size=4096;
                atijaaya->win_size=-1;kanaalü_ekeroliaa=atijaaya->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&kasachiki.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *atijaaya=&kasachiki.connection.channel_data;
            if(!셸시작됨||atijaaya->ch!=kanaalü_ekeroliaa||atijaaya->ext){끊기=1;break;}
            unsigned 수=atijaaya->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(atijaaya->data.data[순번]==4){ajattiraa_jamakua_iparülein=0;수=순번;atijaaya->transferred=atijaaya->data.size;break;}
            원격입력넣기(atijaaya->data.data,수);if(!atijaaya->transferred)atijaaya->transferred=수;
            if(!수&&ajattiraa_jamakua_iparülein<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: kanaalü_ekeroliaa=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",kasachiki.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(epe_ipajia_e05f319b,&kasachiki,ajachitia);
        if(끊기){asürülaa_epe_ipajia();return;}if(쉬기)return;
    }
}
