/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "بعید_قدر.h"
#include "암호기반.h"
#include "پروفائل.h"
#include "../نیٹ_ورک_اسٹیک/نیٹ_ورک_اسٹیک.h"
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
static struct assh_context_s *متن_قدر;
static struct assh_session_s *رابطہ_e05f319b;
static struct assh_channel_s *چینل_اندراج;
static int 듣는곳=-1,ساتھی_قدر=-1,인증됨,셸시작됨,حکم_ٹائپ_کریں,اختتام_حالت=-1,닫을예정,بوٹ_کریں_نقص,셸대기중;
static uintptr_t رابطہ_وقت,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *الفاظ_متن,unsigned قدر) {
    while(*الفاظ_متن)보드글자쓰기(*الفاظ_متن++);
    char عدد_قدر[12];unsigned 수=0;do{عدد_قدر[수++]='0'+قدر%10;قدر/=10;}while(قدر);
    while(수)보드글자쓰기(عدد_قدر[--수]);보드글자쓰기(10);
}
static assh_status_t تیار_کریں_میموری(void *کوائف,void **پتہ,size_t حجم,enum assh_alloc_type_e 종류) {
    (void)کوائف;(void)종류;
    if(!حجم){ریلیز_بعید(*پتہ);*پتہ=0;return ASSH_OK;}
    void *새주소=원격재할당(*پتہ,حجم);
    if(!새주소)return ASSH_ERR_MEM;*پتہ=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *کوائف,const struct assh_buffer_s *بیج_قدر) {
    (void)کوائف;(void)بیج_قدر;unsigned char 시험[32];int پیمائش=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return پیمائش?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *کوائف,uint8_t *پیمائش,size_t لمبا_ئی_قدر,uint_fast8_t 종류) {
    (void)کوائف;(void)종류;if(لمبا_ئی_قدر>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(پیمائش,لمبا_ئی_قدر)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *کوائف){(void)کوائف;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void بند_رابطہ(void) {
    인증됨=셸시작됨=0;چینل_اندراج=0;
    if(رابطہ_e05f319b)assh_session_release(رابطہ_e05f319b);رابطہ_e05f319b=0;
    if(ساتھی_قدر>=0)بند_نیٹ_ورک(ساتھی_قدر);ساتھی_قدر=-1;حکم_ٹائپ_کریں=0;اختتام_حالت=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *کوائف,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=کوائف[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int کریکٹر_قدر=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return کریکٹر_قدر;
}
void 원격출력(unsigned char کریکٹر_قدر) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=کریکٹر_قدر==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=کریکٹر_قدر;이전출력=کریکٹر_قدر;
}
uintptr_t بورڈ_اختتام_بعید_حکم(uintptr_t حالت_قدر){if(셸시작됨&&حکم_ٹائپ_کریں)اختتام_حالت=(int)حالت_قدر;return 0;}
uintptr_t بورڈ_بعید_انتظار(uintptr_t حالت_قدر){셸대기중=حالت_قدر!=0;return 0;}
static int تیار_کریں_شیل(void) {
    if(듣는곳>=0)return 0;
    if(!متن_قدر){
        assh_status_t غلطی=assh_context_create(&متن_قدر,ASSH_SERVER,تیار_کریں_میموری,0,&난수기,0);
        if(غلطی)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *طریقہ_موڈ[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        غلطی=assh_algo_register(متن_قدر,ASSH_SAFETY_WEAK,طریقہ_موڈ);
        if(!غلطی)غلطی=assh_service_register_va(متن_قدر,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=آلہ_کلید;
        if(!غلطی)غلطی=assh_key_load(متن_قدر,assh_context_keys(متن_قدر),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(آلہ_کلید));
        if(غلطی){진단("SSH init error ",غلطی);assh_context_release(متن_قدر);متن_قدر=0;return -5;}
    }
    int پورٹ_قدر=통신끝점만들기(1);if(پورٹ_قدر<0)return پورٹ_قدر;통신주소재사용(پورٹ_قدر);
    int پیمائش=망주소묶기(پورٹ_قدر,0,22);if(!پیمائش)پیمائش=연결기다리기(پورٹ_قدر);
    if(پیمائش<0){بند_نیٹ_ورک(پورٹ_قدر);return پیمائش;}듣는곳=پورٹ_قدر;return 0;
}
uintptr_t بورڈ_سایہ_کاری(uintptr_t 종류,uintptr_t عمل) {
    if(종류==1)return(uint32_t)کنٹرول_بعید_ڈسپلے(عمل);
    if(عمل==0){بند_رابطہ();if(듣는곳>=0)بند_نیٹ_ورک(듣는곳);듣는곳=-1;return 0;}
    if(عمل==1){بوٹ_کریں_نقص=تیار_کریں_شیل();return(uint32_t)بوٹ_کریں_نقص;}
    return(uint32_t)(듣는곳>=0?1:بوٹ_کریں_نقص);
}
void تیار_کریں_بعید(void){بوٹ_کریں_نقص=تیار_کریں_شیل();کنٹرول_بعید_ڈسپلے(1);}
static int 같은말(const struct assh_cbuffer_s *کوائف,const char *الفاظ_متن) {
    size_t لمبا_ئی_قدر=strlen(الفاظ_متن);return کوائف->size==لمبا_ئی_قدر&&!memcmp(کوائف->data,الفاظ_متن,لمبا_ئی_قدر);
}
static int 터미널요청(const struct assh_cbuffer_s *کوائف) {
    if(کوائف->size<24)return 0;
    const unsigned char *کوائف_پوزیشن_ٹھیک_کریں=کوائف->data;unsigned لمبا_ئی_قدر=assh_load_u32(کوائف_پوزیشن_ٹھیک_کریں);
    if(لمبا_ئی_قدر>128||کوائف->size<لمبا_ئی_قدر+24)return 0;
    unsigned موڈ_قدر=assh_load_u32(کوائف_پوزیشن_ٹھیک_کریں+4+لمبا_ئی_قدر+16);
    return موڈ_قدر<=2048&&کوائف->size==لمبا_ئی_قدر+24+موڈ_قدر;
}
static void 요청처리(struct assh_event_request_s *واقعہ) {
    if(!인증됨||واقعہ->ch!=چینل_اندراج||!چینل_اندراج)return;
    if(같은말(&واقعہ->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&واقعہ->rq_data))واقعہ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&واقعہ->type,"window-change")) {
        if(셸시작됨&&واقعہ->rq_data.size==16)واقعہ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *حکم=0;unsigned لمبا_ئی_قدر=0;
    if(같은말(&واقعہ->type,"exec")) {
        if(واقعہ->rq_data.size<4)return;
        لمبا_ئی_قدر=assh_load_u32(واقعہ->rq_data.data);
        if(!لمبا_ئی_قدر||لمبا_ئی_قدر>2048||واقعہ->rq_data.size!=لمبا_ئی_قدر+4)return;
        حکم=واقعہ->rq_data.data+4;
        for(unsigned 순번=0;순번<لمبا_ئی_قدر;순번++)if(!حکم[순번])return;
        حکم_ٹائپ_کریں=1;
    }else if(!같은말(&واقعہ->type,"shell")||واقعہ->rq_data.size)return;
    if(sizeof(입력줄)-입력수<لمبا_ئی_قدر+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(لمبا_ئی_قدر)원격입력넣기(حکم,لمبا_ئی_قدر);원격입력넣기(&끝,1);
    셸시작됨=1;واقعہ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!حکم_ٹائپ_کریں){const char *مجھے_پڑھیں_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*مجھے_پڑھیں_eb81d7d9)원격출력(*مجھے_پڑھیں_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(ساتھی_قدر<0){if(지금<재접속시각)return;ساتھی_قدر=망연결받기(듣는곳);if(ساتھی_قدر<0)return;
        رابطہ_وقت=지금;assh_status_t غلطی=assh_session_create(متن_قدر,&رابطہ_e05f319b);
        if(غلطی){رابطہ_e05f319b=0;진단("SSH session error ",غلطی);بند_رابطہ();return;}}
    if((!인증됨&&지금-رابطہ_وقت>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){بند_رابطہ();return;}
    if(چینل_اندراج&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t غلطی=assh_channel_data(چینل_اندراج,출력줄+출력앞,&수);
            if(!غلطی){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(غلطی!=ASSH_NO_DATA){بند_رابطہ();return;}
        }
        if(اختتام_حالت>=0&&!출력수){unsigned char حالت_قدر[4];assh_store_u32(حالت_قدر,(uint32_t)اختتام_حالت);
            if(assh_request(رابطہ_e05f319b,چینل_اندراج,"exit-status",11,حالت_قدر,4,0)||assh_channel_eof(چینل_اندراج)||assh_channel_close(چینل_اندراج)) {بند_رابطہ();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s واقعہ;
        if(!assh_event_get(رابطہ_e05f319b,&واقعہ,지금/1000)){بند_رابطہ();return;}
        assh_status_t غلطی=ASSH_OK;int 쉬기=0,끊기=0;
        switch(واقعہ.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(ساتھی_قدر,واقعہ.transport.read.buf.data,واقعہ.transport.read.buf.size);
            if(수>0)واقعہ.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(ساتھی_قدر,واقعہ.transport.write.buf.data,واقعہ.transport.write.buf.size);
            if(수>0)واقعہ.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            واقعہ.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(واقعہ.userauth_server.methods.retries>3)واقعہ.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *کوائف=&واقعہ.userauth_server.password;
            if(같은말(&کوائف->username,"user")&&کوائف->password.size<=256&&!کوائف->new_password.size) {
                unsigned char خلاصہ_قدر[32];بعید_خلاصہ(کوائف->password.data,کوائف->password.size,خلاصہ_قدر);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=خلاصہ_قدر[순번]^شیل_پاس_ورڈ_خلاصہ[순번];memset(خلاصہ_قدر,0,32);
                if(!차이)کوائف->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *کوائف=&واقعہ.connection.channel_open;
            if(인증됨&&!چینل_اندراج&&셸대기중&&같은말(&کوائف->type,"session")&&!کوائف->rq_data.size) {
                کوائف->reply=ASSH_CONNECTION_REPLY_SUCCESS;کوائف->pkt_size=4096;
                کوائف->win_size=-1;چینل_اندراج=کوائف->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&واقعہ.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *کوائف=&واقعہ.connection.channel_data;
            if(!셸시작됨||کوائف->ch!=چینل_اندراج||کوائف->ext){끊기=1;break;}
            unsigned 수=کوائف->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(کوائف->data.data[순번]==4){اختتام_حالت=0;수=순번;کوائف->transferred=کوائف->data.size;break;}
            원격입력넣기(کوائف->data.data,수);if(!کوائف->transferred)کوائف->transferred=수;
            if(!수&&اختتام_حالت<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: چینل_اندراج=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",واقعہ.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(رابطہ_e05f319b,&واقعہ,غلطی);
        if(끊기){بند_رابطہ();return;}if(쉬기)return;
    }
}
