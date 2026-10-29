/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "بعيد_قيمة.h"
#include "تشفير_دعم.h"
#include "يحلل.h"
#include "../شبكة_رمز/شبكة_رمز.h"
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
static struct assh_context_s *سياق_قيمة;
static struct assh_session_s *صديق_e05f319b;
static struct assh_channel_s *قناة_إدخال;
static int استماع_المشارك=-1,نظير_قيمة=-1,인증됨,셸시작됨,أمر_نوع,إنهاء_مكالمة_حالة=-1,닫을예정,بدء_التشغيل_خطأ,셸대기중;
static uintptr_t صديق_وقت,재접속시각,إقفال_وقت;
static unsigned char إدخال_خط[8192],الناتج_خط[65536];
static unsigned إدخال_رأس,입력수,الناتج_رأس,출력수,이전출력;
static void 진단(const char *الكلمات_نص,unsigned قيمة) {
    while(*الكلمات_نص)보드글자쓰기(*الكلمات_نص++);
    char رقم_قيمة[12];unsigned رقم=0;do{رقم_قيمة[رقم++]='0'+قيمة%10;قيمة/=10;}while(قيمة);
    while(رقم)보드글자쓰기(رقم_قيمة[--رقم]);보드글자쓰기(10);
}
static assh_status_t إعداد_ذاكرة(void *بيانات,void **عنوان,size_t حجم,enum assh_alloc_type_e 종류) {
    (void)بيانات;(void)종류;
    if(!حجم){إصدار_بعيد(*عنوان);*عنوان=0;return ASSH_OK;}
    void *새주소=원격재할당(*عنوان,حجم);
    if(!새주소)return ASSH_ERR_MEM;*عنوان=새주소;return ASSH_OK;
}
static assh_status_t إعداد_عشوائي(struct assh_context_s *بيانات,const struct assh_buffer_s *القيمة_الأولية) {
    (void)بيانات;(void)القيمة_الأولية;unsigned char اختبارات[32];int نتيجة=بعيد_عشوائي(اختبارات,sizeof(اختبارات));memset(اختبارات,0,sizeof(اختبارات));
    return نتيجة?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t يقرأ_عشوائي(struct assh_context_s *بيانات,uint8_t *نتيجة,size_t 길이,uint_fast8_t 종류) {
    (void)بيانات;(void)종류;if(길이>65536)return ASSH_ERR_CRYPTO;
    return بعيد_عشوائي(نتيجة,길이)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void عشوائي_إنهاء_مكالمة(struct assh_context_s *بيانات){(void)بيانات;}
static const struct assh_prng_s عشوائي_مُنشئ={إعداد_عشوائي,يقرأ_عشوائي,عشوائي_إنهاء_مكالمة};
static void يغلق_صديق(void) {
    인증됨=셸시작됨=0;قناة_إدخال=0;
    if(صديق_e05f319b)assh_session_release(صديق_e05f319b);صديق_e05f319b=0;
    if(نظير_قيمة>=0)يغلق_شبكة(نظير_قيمة);نظير_قيمة=-1;أمر_نوع=0;إنهاء_مكالمة_حالة=-1;닫을예정=0;
    إدخال_رأس=입력수=الناتج_رأس=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int موجز_بعيد_إدخال(const unsigned char *بيانات,unsigned رقم) {
    if(رقم>sizeof(إدخال_خط)-입력수)return -11;
    for(unsigned 순번=0;순번<رقم;순번++)إدخال_خط[(إدخال_رأس+입력수++)%sizeof(إدخال_خط)]=بيانات[순번];return رقم;
}
int بعيد_إدخال(void) {
    if(!입력수)return -1;int حرف_قيمة=إدخال_خط[إدخال_رأس];إدخال_رأس=(إدخال_رأس+1)%sizeof(إدخال_خط);입력수--;return حرف_قيمة;
}
void بعيد_الناتج(unsigned char حرف_قيمة) {
    if(!셸시작됨||닫을예정)return;
    unsigned إلحاق_الوضع=حرف_قيمة==10&&이전출력!=13;
    if(출력수+1+إلحاق_الوضع>sizeof(الناتج_خط)){닫을예정=2;return;}
    if(إلحاق_الوضع)الناتج_خط[(الناتج_رأس+출력수++)%sizeof(الناتج_خط)]=13;
    الناتج_خط[(الناتج_رأس+출력수++)%sizeof(الناتج_خط)]=حرف_قيمة;이전출력=حرف_قيمة;
}
uintptr_t لوحة_إنهاء_مكالمة_بعيد_أمر(uintptr_t حالة_قيمة){if(셸시작됨&&أمر_نوع)إنهاء_مكالمة_حالة=(int)حالة_قيمة;return 0;}
uintptr_t لوحة_بعيد_انتظر(uintptr_t حالة_قيمة){셸대기중=حالة_قيمة!=0;return 0;}
static int 셸준비(void) {
    if(استماع_المشارك>=0)return 0;
    if(!سياق_قيمة){
        assh_status_t خطأ=assh_context_create(&سياق_قيمة,ASSH_SERVER,إعداد_ذاكرة,0,&عشوائي_مُنشئ,0);
        if(خطأ)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *أسلوب_الوضع[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        خطأ=assh_algo_register(سياق_قيمة,ASSH_SAFETY_WEAK,أسلوب_الوضع);
        if(!خطأ)خطأ=assh_service_register_va(سياق_قيمة,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=جهاز_مفتاح;
        if(!خطأ)خطأ=assh_key_load(سياق_قيمة,assh_context_keys(سياق_قيمة),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(جهاز_مفتاح));
        if(خطأ){진단("SSH init error ",خطأ);assh_context_release(سياق_قيمة);سياق_قيمة=0;return -5;}
    }
    int منفذ_قيمة=فتح_مأخذ_التوصيل_المشارك(1);if(منفذ_قيمة<0)return منفذ_قيمة;통신주소재사용(منفذ_قيمة);
    int نتيجة=صافي_يربط(منفذ_قيمة,0,22);if(!نتيجة)نتيجة=صافي_انصات(منفذ_قيمة);
    if(نتيجة<0){يغلق_شبكة(منفذ_قيمة);return نتيجة;}استماع_المشارك=منفذ_قيمة;return 0;
}
uintptr_t لوحة_تحكم_عن_بعد(uintptr_t 종류,uintptr_t إجراء) {
    if(종류==1)return(uint32_t)تحكم_بعيد_يعرض(إجراء);
    if(إجراء==0){يغلق_صديق();if(استماع_المشارك>=0)يغلق_شبكة(استماع_المشارك);استماع_المشارك=-1;return 0;}
    if(إجراء==1){بدء_التشغيل_خطأ=셸준비();return(uint32_t)بدء_التشغيل_خطأ;}
    return(uint32_t)(استماع_المشارك>=0?1:بدء_التشغيل_خطأ);
}
void إعداد_بعيد(void){بدء_التشغيل_خطأ=셸준비();تحكم_بعيد_يعرض(1);}
static int 같은말(const struct assh_cbuffer_s *بيانات,const char *الكلمات_نص) {
    size_t 길이=strlen(الكلمات_نص);return بيانات->size==길이&&!memcmp(بيانات->data,الكلمات_نص,길이);
}
static int الوحدة_الطرفية_طلب(const struct assh_cbuffer_s *بيانات) {
    if(بيانات->size<24)return 0;
    const unsigned char *بيانات_منصب=بيانات->data;unsigned 길이=assh_load_u32(بيانات_منصب);
    if(길이>128||بيانات->size<길이+24)return 0;
    unsigned الوضع_قيمة=assh_load_u32(بيانات_منصب+4+길이+16);
    return الوضع_قيمة<=2048&&بيانات->size==길이+24+الوضع_قيمة;
}
static void مؤشر_طلب(struct assh_event_request_s *حدث) {
    if(!인증됨||حدث->ch!=قناة_إدخال||!قناة_إدخال)return;
    if(같은말(&حدث->type,"pty-req")) {
        if(!셸시작됨&&الوحدة_الطرفية_طلب(&حدث->rq_data))حدث->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&حدث->type,"window-change")) {
        if(셸시작됨&&حدث->rq_data.size==16)حدث->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *أمر=0;unsigned 길이=0;
    if(같은말(&حدث->type,"exec")) {
        if(حدث->rq_data.size<4)return;
        길이=assh_load_u32(حدث->rq_data.data);
        if(!길이||길이>2048||حدث->rq_data.size!=길이+4)return;
        أمر=حدث->rq_data.data+4;
        for(unsigned 순번=0;순번<길이;순번++)if(!أمر[순번])return;
        أمر_نوع=1;
    }else if(!같은말(&حدث->type,"shell")||حدث->rq_data.size)return;
    if(sizeof(إدخال_خط)-입력수<길이+2)return;
    const unsigned char 지움=21,끝=13;
    موجز_بعيد_إدخال(&지움,1);if(길이)موجز_بعيد_إدخال(أمر,길이);موجز_بعيد_إدخال(&끝,1);
    셸시작됨=1;حدث->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!أمر_نوع){const char *안내="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*안내)بعيد_الناتج(*안내++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(استماع_المشارك<0)return;
    uintptr_t الآن_قيمة=보드밀리초();
    if(نظير_قيمة<0){if(الآن_قيمة<재접속시각)return;نظير_قيمة=صافي_قبول(استماع_المشارك);if(نظير_قيمة<0)return;
        صديق_وقت=الآن_قيمة;assh_status_t خطأ=assh_session_create(سياق_قيمة,&صديق_e05f319b);
        if(خطأ){صديق_e05f319b=0;진단("SSH session error ",خطأ);يغلق_صديق();return;}}
    if((!인증됨&&الآن_قيمة-صديق_وقت>30000)||닫을예정==2||(닫을예정&&الآن_قيمة>=إقفال_وقت)){يغلق_صديق();return;}
    if(قناة_إدخال&&셸시작됨&&!닫을예정) {
        if(출력수){size_t رقم=sizeof(الناتج_خط)-الناتج_رأس;if(رقم>출력수)رقم=출력수;if(رقم>2048)رقم=2048;
            assh_status_t خطأ=assh_channel_data(قناة_إدخال,الناتج_خط+الناتج_رأس,&رقم);
            if(!خطأ){الناتج_رأس=(الناتج_رأس+رقم)%sizeof(الناتج_خط);출력수-=رقم;}
            else if(خطأ!=ASSH_NO_DATA){يغلق_صديق();return;}
        }
        if(إنهاء_مكالمة_حالة>=0&&!출력수){unsigned char حالة_قيمة[4];assh_store_u32(حالة_قيمة,(uint32_t)إنهاء_مكالمة_حالة);
            if(assh_request(صديق_e05f319b,قناة_إدخال,"exit-status",11,حالة_قيمة,4,0)||assh_channel_eof(قناة_إدخال)||assh_channel_close(قناة_إدخال)) {يغلق_صديق();return;}
            닫을예정=1;إقفال_وقت=الآن_قيمة+3000;
        }
    }
    for(unsigned تسلسل_قيمة=0;تسلسل_قيمة<16;تسلسل_قيمة++) {
        struct assh_event_s حدث;
        if(!assh_event_get(صديق_e05f319b,&حدث,الآن_قيمة/1000)){يغلق_صديق();return;}
        assh_status_t خطأ=ASSH_OK;int 쉬기=0,قطع_الاتصال_المشارك=0;
        switch(حدث.id) {
        case ASSH_EVENT_READ: {
            int رقم=صافي_يقرأ(نظير_قيمة,حدث.transport.read.buf.data,حدث.transport.read.buf.size);
            if(رقم>0)حدث.transport.read.transferred=رقم;
            else if(رقم==-11)쉬기=1;else قطع_الاتصال_المشارك=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int رقم=صافي_كتابة(نظير_قيمة,حدث.transport.write.buf.data,حدث.transport.write.buf.size);
            if(رقم>0)حدث.transport.write.transferred=رقم;
            else if(رقم==-11)쉬기=1;else قطع_الاتصال_المشارك=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            حدث.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(حدث.userauth_server.methods.retries>3)حدث.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *بيانات=&حدث.userauth_server.password;
            if(같은말(&بيانات->username,"user")&&بيانات->password.size<=256&&!بيانات->new_password.size) {
                unsigned char الملخص_قيمة[32];بعيد_الملخص(بيانات->password.data,بيانات->password.size,الملخص_قيمة);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=الملخص_قيمة[순번]^셸암호요약[순번];memset(الملخص_قيمة,0,32);
                if(!차이)بيانات->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *بيانات=&حدث.connection.channel_open;
            if(인증됨&&!قناة_إدخال&&셸대기중&&같은말(&بيانات->type,"session")&&!بيانات->rq_data.size) {
                بيانات->reply=ASSH_CONNECTION_REPLY_SUCCESS;بيانات->pkt_size=4096;
                بيانات->win_size=-1;قناة_إدخال=بيانات->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: مؤشر_طلب(&حدث.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *بيانات=&حدث.connection.channel_data;
            if(!셸시작됨||بيانات->ch!=قناة_إدخال||بيانات->ext){قطع_الاتصال_المشارك=1;break;}
            unsigned رقم=بيانات->data.size;if(رقم>sizeof(إدخال_خط)-입력수)رقم=sizeof(إدخال_خط)-입력수;
            for(unsigned 순번=0;순번<رقم;순번++)if(بيانات->data.data[순번]==4){إنهاء_مكالمة_حالة=0;رقم=순번;بيانات->transferred=بيانات->data.size;break;}
            موجز_بعيد_إدخال(بيانات->data.data,رقم);if(!بيانات->transferred)بيانات->transferred=رقم;
            if(!رقم&&إنهاء_مكالمة_حالة<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: قناة_إدخال=0;셸시작됨=0;닫을예정=1;إقفال_وقت=الآن_قيمة+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",حدث.session.error.code);قطع_الاتصال_المشارك=1;break;
        case ASSH_EVENT_DISCONNECT: قطع_الاتصال_المشارك=1;break;
        default: break;
        }
        assh_event_done(صديق_e05f319b,&حدث,خطأ);
        if(قطع_الاتصال_المشارك){يغلق_صديق();return;}if(쉬기)return;
    }
}
