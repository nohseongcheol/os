/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "راه_دور_مقدار.h"
#include "암호기반.h"
#include "نمایه.h"
#include "../شبکه_پشته/شبکه_پشته.h"
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
static struct assh_context_s *زمینه_مقدار;
static struct assh_session_s *اتصال_e05f319b;
static struct assh_channel_s *کانال_ورودی;
static int 듣는곳=-1,مشابه_مقدار=-1,인증됨,셸시작됨,فرمان_تایپ_کردن,پایان_دادن_وضعیت=-1,닫을예정,راه_اندازی_خطا,واسط_در_حال_انتظار;
static uintptr_t اتصال_زمان,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *کلمات_متن,unsigned مقدار) {
    while(*کلمات_متن)보드글자쓰기(*کلمات_متن++);
    char رقم_مقدار[12];unsigned 수=0;do{رقم_مقدار[수++]='0'+مقدار%10;مقدار/=10;}while(مقدار);
    while(수)보드글자쓰기(رقم_مقدار[--수]);보드글자쓰기(10);
}
static assh_status_t آماده_کردن_حافظه(void *داده_ها,void **آدرس,size_t اندازه,enum assh_alloc_type_e 종류) {
    (void)داده_ها;(void)종류;
    if(!اندازه){انتشار_راه_دور(*آدرس);*آدرس=0;return ASSH_OK;}
    void *새주소=원격재할당(*آدرس,اندازه);
    if(!새주소)return ASSH_ERR_MEM;*آدرس=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *داده_ها,const struct assh_buffer_s *دانه_مقدار) {
    (void)داده_ها;(void)دانه_مقدار;unsigned char 시험[32];int سنجش=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return سنجش?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *داده_ها,uint8_t *سنجش,size_t طول_مقدار,uint_fast8_t 종류) {
    (void)داده_ها;(void)종류;if(طول_مقدار>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(سنجش,طول_مقدار)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *داده_ها){(void)داده_ها;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void بستن_اتصال(void) {
    인증됨=셸시작됨=0;کانال_ورودی=0;
    if(اتصال_e05f319b)assh_session_release(اتصال_e05f319b);اتصال_e05f319b=0;
    if(مشابه_مقدار>=0)بستن_شبکه(مشابه_مقدار);مشابه_مقدار=-1;فرمان_تایپ_کردن=0;پایان_دادن_وضعیت=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *داده_ها,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=داده_ها[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int نویسه_مقدار=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return نویسه_مقدار;
}
void 원격출력(unsigned char نویسه_مقدار) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=نویسه_مقدار==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=نویسه_مقدار;이전출력=نویسه_مقدار;
}
uintptr_t تخته_ای_پایان_دادن_راه_دور_فرمان(uintptr_t وضعیت_مقدار){if(셸시작됨&&فرمان_تایپ_کردن)پایان_دادن_وضعیت=(int)وضعیت_مقدار;return 0;}
uintptr_t تخته_ای_راه_دور_منتظر_ماندن(uintptr_t وضعیت_مقدار){واسط_در_حال_انتظار=وضعیت_مقدار!=0;return 0;}
static int آماده_کردن_واسط(void) {
    if(듣는곳>=0)return 0;
    if(!زمینه_مقدار){
        assh_status_t خطا=assh_context_create(&زمینه_مقدار,ASSH_SERVER,آماده_کردن_حافظه,0,&난수기,0);
        if(خطا)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *روش_حالت[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        خطا=assh_algo_register(زمینه_مقدار,ASSH_SAFETY_WEAK,روش_حالت);
        if(!خطا)خطا=assh_service_register_va(زمینه_مقدار,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=دستگاه_کلید;
        if(!خطا)خطا=assh_key_load(زمینه_مقدار,assh_context_keys(زمینه_مقدار),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(دستگاه_کلید));
        if(خطا){진단("SSH init error ",خطا);assh_context_release(زمینه_مقدار);زمینه_مقدار=0;return -5;}
    }
    int تبدیل_مقدار=통신끝점만들기(1);if(تبدیل_مقدار<0)return تبدیل_مقدار;통신주소재사용(تبدیل_مقدار);
    int سنجش=망주소묶기(تبدیل_مقدار,0,22);if(!سنجش)سنجش=연결기다리기(تبدیل_مقدار);
    if(سنجش<0){بستن_شبکه(تبدیل_مقدار);return سنجش;}듣는곳=تبدیل_مقدار;return 0;
}
uintptr_t تخته_ای_کنترل_از_راه_دور(uintptr_t 종류,uintptr_t کنش) {
    if(종류==1)return(uint32_t)کنترل_راه_دور_صفحه_نمایش(کنش);
    if(کنش==0){بستن_اتصال();if(듣는곳>=0)بستن_شبکه(듣는곳);듣는곳=-1;return 0;}
    if(کنش==1){راه_اندازی_خطا=آماده_کردن_واسط();return(uint32_t)راه_اندازی_خطا;}
    return(uint32_t)(듣는곳>=0?1:راه_اندازی_خطا);
}
void آماده_کردن_راه_دور(void){راه_اندازی_خطا=آماده_کردن_واسط();کنترل_راه_دور_صفحه_نمایش(1);}
static int 같은말(const struct assh_cbuffer_s *داده_ها,const char *کلمات_متن) {
    size_t طول_مقدار=strlen(کلمات_متن);return داده_ها->size==طول_مقدار&&!memcmp(داده_ها->data,کلمات_متن,طول_مقدار);
}
static int 터미널요청(const struct assh_cbuffer_s *داده_ها) {
    if(داده_ها->size<24)return 0;
    const unsigned char *داده_ها_مرتب_کردن=داده_ها->data;unsigned طول_مقدار=assh_load_u32(داده_ها_مرتب_کردن);
    if(طول_مقدار>128||داده_ها->size<طول_مقدار+24)return 0;
    unsigned حالت_مقدار=assh_load_u32(داده_ها_مرتب_کردن+4+طول_مقدار+16);
    return حالت_مقدار<=2048&&داده_ها->size==طول_مقدار+24+حالت_مقدار;
}
static void 요청처리(struct assh_event_request_s *رویداد) {
    if(!인증됨||رویداد->ch!=کانال_ورودی||!کانال_ورودی)return;
    if(같은말(&رویداد->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&رویداد->rq_data))رویداد->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&رویداد->type,"window-change")) {
        if(셸시작됨&&رویداد->rq_data.size==16)رویداد->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!واسط_در_حال_انتظار)return;
    const unsigned char *فرمان=0;unsigned طول_مقدار=0;
    if(같은말(&رویداد->type,"exec")) {
        if(رویداد->rq_data.size<4)return;
        طول_مقدار=assh_load_u32(رویداد->rq_data.data);
        if(!طول_مقدار||طول_مقدار>2048||رویداد->rq_data.size!=طول_مقدار+4)return;
        فرمان=رویداد->rq_data.data+4;
        for(unsigned 순번=0;순번<طول_مقدار;순번++)if(!فرمان[순번])return;
        فرمان_تایپ_کردن=1;
    }else if(!같은말(&رویداد->type,"shell")||رویداد->rq_data.size)return;
    if(sizeof(입력줄)-입력수<طول_مقدار+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(طول_مقدار)원격입력넣기(فرمان,طول_مقدار);원격입력넣기(&끝,1);
    셸시작됨=1;رویداد->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!فرمان_تایپ_کردن){const char *مرا_بخوان_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*مرا_بخوان_eb81d7d9)원격출력(*مرا_بخوان_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t هم_اکنون_مقدار=보드밀리초();
    if(مشابه_مقدار<0){if(هم_اکنون_مقدار<재접속시각)return;مشابه_مقدار=망연결받기(듣는곳);if(مشابه_مقدار<0)return;
        اتصال_زمان=هم_اکنون_مقدار;assh_status_t خطا=assh_session_create(زمینه_مقدار,&اتصال_e05f319b);
        if(خطا){اتصال_e05f319b=0;진단("SSH session error ",خطا);بستن_اتصال();return;}}
    if((!인증됨&&هم_اکنون_مقدار-اتصال_زمان>30000)||닫을예정==2||(닫을예정&&هم_اکنون_مقدار>=닫는시각)){بستن_اتصال();return;}
    if(کانال_ورودی&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t خطا=assh_channel_data(کانال_ورودی,출력줄+출력앞,&수);
            if(!خطا){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(خطا!=ASSH_NO_DATA){بستن_اتصال();return;}
        }
        if(پایان_دادن_وضعیت>=0&&!출력수){unsigned char وضعیت_مقدار[4];assh_store_u32(وضعیت_مقدار,(uint32_t)پایان_دادن_وضعیت);
            if(assh_request(اتصال_e05f319b,کانال_ورودی,"exit-status",11,وضعیت_مقدار,4,0)||assh_channel_eof(کانال_ورودی)||assh_channel_close(کانال_ورودی)) {بستن_اتصال();return;}
            닫을예정=1;닫는시각=هم_اکنون_مقدار+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s رویداد;
        if(!assh_event_get(اتصال_e05f319b,&رویداد,هم_اکنون_مقدار/1000)){بستن_اتصال();return;}
        assh_status_t خطا=ASSH_OK;int 쉬기=0,끊기=0;
        switch(رویداد.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(مشابه_مقدار,رویداد.transport.read.buf.data,رویداد.transport.read.buf.size);
            if(수>0)رویداد.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(مشابه_مقدار,رویداد.transport.write.buf.data,رویداد.transport.write.buf.size);
            if(수>0)رویداد.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            رویداد.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(رویداد.userauth_server.methods.retries>3)رویداد.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *داده_ها=&رویداد.userauth_server.password;
            if(같은말(&داده_ها->username,"user")&&داده_ها->password.size<=256&&!داده_ها->new_password.size) {
                unsigned char خلاصه_مقدار[32];راه_دور_خلاصه(داده_ها->password.data,داده_ها->password.size,خلاصه_مقدار);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=خلاصه_مقدار[순번]^واسط_رمز_عبور_خلاصه[순번];memset(خلاصه_مقدار,0,32);
                if(!차이)داده_ها->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *داده_ها=&رویداد.connection.channel_open;
            if(인증됨&&!کانال_ورودی&&واسط_در_حال_انتظار&&같은말(&داده_ها->type,"session")&&!داده_ها->rq_data.size) {
                داده_ها->reply=ASSH_CONNECTION_REPLY_SUCCESS;داده_ها->pkt_size=4096;
                داده_ها->win_size=-1;کانال_ورودی=داده_ها->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&رویداد.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *داده_ها=&رویداد.connection.channel_data;
            if(!셸시작됨||داده_ها->ch!=کانال_ورودی||داده_ها->ext){끊기=1;break;}
            unsigned 수=داده_ها->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(داده_ها->data.data[순번]==4){پایان_دادن_وضعیت=0;수=순번;داده_ها->transferred=داده_ها->data.size;break;}
            원격입력넣기(داده_ها->data.data,수);if(!داده_ها->transferred)داده_ها->transferred=수;
            if(!수&&پایان_دادن_وضعیت<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: کانال_ورودی=0;셸시작됨=0;닫을예정=1;닫는시각=هم_اکنون_مقدار+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",رویداد.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(اتصال_e05f319b,&رویداد,خطا);
        if(끊기){بستن_اتصال();return;}if(쉬기)return;
    }
}
