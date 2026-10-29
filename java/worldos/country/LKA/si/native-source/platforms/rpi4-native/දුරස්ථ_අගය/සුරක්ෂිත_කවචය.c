/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "දුරස්ථ_අගය.h"
#include "암호기반.h"
#include "පැතිකඩ.h"
#include "../ජාලය_කැටිය/ජාලය_කැටිය.h"
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
static struct assh_context_s *සන්දර්භය_අගය;
static struct assh_session_s *සබැඳුම_e05f319b;
static struct assh_channel_s *නාලිකාව_පිවිසුම;
static int 듣는곳=-1,සමානයා_අගය=-1,인증됨,셸시작됨,විධානය_ටයිප්_කරන්න,නිමා_කරන්න_තත්වය=-1,닫을예정,ඇරඹුම_දොස,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *말,unsigned අගය) {
    while(*말)보드글자쓰기(*말++);
    char සංඛ්_යාංකය_අගය[12];unsigned 수=0;do{සංඛ්_යාංකය_අගය[수++]='0'+අගය%10;අගය/=10;}while(අගය);
    while(수)보드글자쓰기(සංඛ්_යාංකය_අගය[--수]);보드글자쓰기(10);
}
static assh_status_t පිළියෙල_කරන්න_මතකය(void *දත්ත,void **යොමුව,size_t ප්_රමාණය,enum assh_alloc_type_e 종류) {
    (void)දත්ත;(void)종류;
    if(!ප්_රමාණය){මුදාහැරීම_දුරස්ථ(*යොමුව);*යොමුව=0;return ASSH_OK;}
    void *새주소=원격재할당(*යොමුව,ප්_රමාණය);
    if(!새주소)return ASSH_ERR_MEM;*යොමුව=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *දත්ත,const struct assh_buffer_s *බීජනය_අගය) {
    (void)දත්ත;(void)බීජනය_අගය;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *දත්ත,uint8_t *결과,size_t දිග_අගය,uint_fast8_t 종류) {
    (void)දත්ත;(void)종류;if(දිග_අගය>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,දිග_අගය)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *දත්ත){(void)දත්ත;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void වසන්න_සබැඳුම(void) {
    인증됨=셸시작됨=0;නාලිකාව_පිවිසුම=0;
    if(සබැඳුම_e05f319b)assh_session_release(සබැඳුම_e05f319b);සබැඳුම_e05f319b=0;
    if(සමානයා_අගය>=0)වසන්න_ජාලය(සමානයා_අගය);සමානයා_අගය=-1;විධානය_ටයිප්_කරන්න=0;නිමා_කරන්න_තත්වය=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *දත්ත,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=දත්ත[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int අනුලකුණ_අගය=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return අනුලකුණ_අගය;
}
void 원격출력(unsigned char අනුලකුණ_අගය) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=අනුලකුණ_අගය==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=අනුලකුණ_අගය;이전출력=අනුලකුණ_අගය;
}
uintptr_t 보드원격명령끝(uintptr_t තත්වය_අගය){if(셸시작됨&&විධානය_ටයිප්_කරන්න)නිමා_කරන්න_තත්වය=(int)තත්වය_අගය;return 0;}
uintptr_t 보드원격대기(uintptr_t තත්වය_අගය){셸대기중=තත්වය_අගය!=0;return 0;}
static int පිළියෙල_කරන්න_කවචය(void) {
    if(듣는곳>=0)return 0;
    if(!සන්දර්භය_අගය){
        assh_status_t දෝෂය=assh_context_create(&සන්දර්භය_අගය,ASSH_SERVER,පිළියෙල_කරන්න_මතකය,0,&난수기,0);
        if(දෝෂය)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *ක්_රමය_ප්_රකාරය[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        දෝෂය=assh_algo_register(සන්දර්භය_අගය,ASSH_SAFETY_WEAK,ක්_රමය_ප්_රකාරය);
        if(!දෝෂය)දෝෂය=assh_service_register_va(සන්දර්භය_අගය,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=ජංගම_යතුර;
        if(!දෝෂය)දෝෂය=assh_key_load(සන්දර්භය_අගය,assh_context_keys(සන්දර්භය_අගය),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(ජංගම_යතුර));
        if(දෝෂය){진단("SSH init error ",දෝෂය);assh_context_release(සන්දර්භය_අගය);සන්දර්භය_අගය=0;return -5;}
    }
    int තොට_අගය=통신끝점만들기(1);if(තොට_අගය<0)return තොට_අගය;통신주소재사용(තොට_අගය);
    int 결과=망주소묶기(තොට_අගය,0,22);if(!결과)결과=연결기다리기(තොට_අගය);
    if(결과<0){වසන්න_ජාලය(තොට_අගය);return 결과;}듣는곳=තොට_අගය;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t ක්_රීයාව) {
    if(종류==1)return(uint32_t)පාලකය_දුරස්ථ_සංදර්ශකය(ක්_රීයාව);
    if(ක්_රීයාව==0){වසන්න_සබැඳුම();if(듣는곳>=0)වසන්න_ජාලය(듣는곳);듣는곳=-1;return 0;}
    if(ක්_රීයාව==1){ඇරඹුම_දොස=පිළියෙල_කරන්න_කවචය();return(uint32_t)ඇරඹුම_දොස;}
    return(uint32_t)(듣는곳>=0?1:ඇරඹුම_දොස);
}
void පිළියෙල_කරන්න_දුරස්ථ(void){ඇරඹුම_දොස=පිළියෙල_කරන්න_කවචය();පාලකය_දුරස්ථ_සංදර්ශකය(1);}
static int 같은말(const struct assh_cbuffer_s *දත්ත,const char *말) {
    size_t දිග_අගය=strlen(말);return දත්ත->size==දිග_අගය&&!memcmp(දත්ත->data,말,දිග_අගය);
}
static int 터미널요청(const struct assh_cbuffer_s *දත්ත) {
    if(දත්ත->size<24)return 0;
    const unsigned char *자료위치=දත්ත->data;unsigned දිග_අගය=assh_load_u32(자료위치);
    if(දිග_අගය>128||දත්ත->size<දිග_අගය+24)return 0;
    unsigned ප්_රකාරය_අගය=assh_load_u32(자료위치+4+දිග_අගය+16);
    return ප්_රකාරය_අගය<=2048&&දත්ත->size==දිග_අගය+24+ප්_රකාරය_අගය;
}
static void 요청처리(struct assh_event_request_s *සිදුවීම) {
    if(!인증됨||සිදුවීම->ch!=නාලිකාව_පිවිසුම||!නාලිකාව_පිවිසුම)return;
    if(같은말(&සිදුවීම->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&සිදුවීම->rq_data))සිදුවීම->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&සිදුවීම->type,"window-change")) {
        if(셸시작됨&&සිදුවීම->rq_data.size==16)සිදුවීම->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *විධානය=0;unsigned දිග_අගය=0;
    if(같은말(&සිදුවීම->type,"exec")) {
        if(සිදුවීම->rq_data.size<4)return;
        දිග_අගය=assh_load_u32(සිදුවීම->rq_data.data);
        if(!දිග_අගය||දිග_අගය>2048||සිදුවීම->rq_data.size!=දිග_අගය+4)return;
        විධානය=සිදුවීම->rq_data.data+4;
        for(unsigned 순번=0;순번<දිග_අගය;순번++)if(!විධානය[순번])return;
        විධානය_ටයිප්_කරන්න=1;
    }else if(!같은말(&සිදුවීම->type,"shell")||සිදුවීම->rq_data.size)return;
    if(sizeof(입력줄)-입력수<දිග_අගය+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(දිග_අගය)원격입력넣기(විධානය,දිග_අගය);원격입력넣기(&끝,1);
    셸시작됨=1;සිදුවීම->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!විධානය_ටයිප්_කරන්න){const char *README_ගොනුව_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*README_ගොනුව_eb81d7d9)원격출력(*README_ගොනුව_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(සමානයා_අගය<0){if(지금<재접속시각)return;සමානයා_අගය=망연결받기(듣는곳);if(සමානයා_අගය<0)return;
        접속시각=지금;assh_status_t දෝෂය=assh_session_create(සන්දර්භය_අගය,&සබැඳුම_e05f319b);
        if(දෝෂය){සබැඳුම_e05f319b=0;진단("SSH session error ",දෝෂය);වසන්න_සබැඳුම();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){වසන්න_සබැඳුම();return;}
    if(නාලිකාව_පිවිසුම&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t දෝෂය=assh_channel_data(නාලිකාව_පිවිසුම,출력줄+출력앞,&수);
            if(!දෝෂය){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(දෝෂය!=ASSH_NO_DATA){වසන්න_සබැඳුම();return;}
        }
        if(නිමා_කරන්න_තත්වය>=0&&!출력수){unsigned char තත්වය_අගය[4];assh_store_u32(තත්වය_අගය,(uint32_t)නිමා_කරන්න_තත්වය);
            if(assh_request(සබැඳුම_e05f319b,නාලිකාව_පිවිසුම,"exit-status",11,තත්වය_අගය,4,0)||assh_channel_eof(නාලිකාව_පිවිසුම)||assh_channel_close(නාලිකාව_පිවිසුම)) {වසන්න_සබැඳුම();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned අනුක්_රමය_අගය=0;අනුක්_රමය_අගය<16;අනුක්_රමය_අගය++) {
        struct assh_event_s සිදුවීම;
        if(!assh_event_get(සබැඳුම_e05f319b,&සිදුවීම,지금/1000)){වසන්න_සබැඳුම();return;}
        assh_status_t දෝෂය=ASSH_OK;int 쉬기=0,끊기=0;
        switch(සිදුවීම.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(සමානයා_අගය,සිදුවීම.transport.read.buf.data,සිදුවීම.transport.read.buf.size);
            if(수>0)සිදුවීම.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(සමානයා_අගය,සිදුවීම.transport.write.buf.data,සිදුවීම.transport.write.buf.size);
            if(수>0)සිදුවීම.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            සිදුවීම.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(සිදුවීම.userauth_server.methods.retries>3)සිදුවීම.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *දත්ත=&සිදුවීම.userauth_server.password;
            if(같은말(&දත්ත->username,"user")&&දත්ත->password.size<=256&&!දත්ත->new_password.size) {
                unsigned char සාරාංශය_අගය[32];දුරස්ථ_සාරාංශය(දත්ත->password.data,දත්ත->password.size,සාරාංශය_අගය);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=සාරාංශය_අගය[순번]^කවචය_මුර_පදය_සාරාංශය[순번];memset(සාරාංශය_අගය,0,32);
                if(!차이)දත්ත->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *දත්ත=&සිදුවීම.connection.channel_open;
            if(인증됨&&!නාලිකාව_පිවිසුම&&셸대기중&&같은말(&දත්ත->type,"session")&&!දත්ත->rq_data.size) {
                දත්ත->reply=ASSH_CONNECTION_REPLY_SUCCESS;දත්ත->pkt_size=4096;
                දත්ත->win_size=-1;නාලිකාව_පිවිසුම=දත්ත->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&සිදුවීම.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *දත්ත=&සිදුවීම.connection.channel_data;
            if(!셸시작됨||දත්ත->ch!=නාලිකාව_පිවිසුම||දත්ත->ext){끊기=1;break;}
            unsigned 수=දත්ත->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(දත්ත->data.data[순번]==4){නිමා_කරන්න_තත්වය=0;수=순번;දත්ත->transferred=දත්ත->data.size;break;}
            원격입력넣기(දත්ත->data.data,수);if(!දත්ත->transferred)දත්ත->transferred=수;
            if(!수&&නිමා_කරන්න_තත්වය<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: නාලිකාව_පිවිසුම=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",සිදුවීම.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(සබැඳුම_e05f319b,&සිදුවීම,දෝෂය);
        if(끊기){වසන්න_සබැඳුම();return;}if(쉬기)return;
    }
}
