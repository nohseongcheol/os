/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "دوورەدەس_نرخ.h"
#include "암호기반.h"
#include "پرۆفایل.h"
#include "../تۆڕ_ستاك/تۆڕ_ستاك.h"
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
static struct assh_context_s *ریزکردنی_سیاق_نرخ;
static struct assh_session_s *گرێدان_e05f319b;
static struct assh_channel_s *کاناڵ_تێنووسین;
static int 듣는곳=-1,هاوتا_نرخ=-1,인증됨,셸시작됨,فەرمان_چاپکردن,دوایی_کردن_دۆخ=-1,닫을예정,دەسپێک_هەڵە,توێکڵ_چاوەڕوانی;
static uintptr_t گرێدان_کات,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *وشە_دەق,unsigned نرخ) {
    while(*وشە_دەق)보드글자쓰기(*وشە_دەق++);
    char ڕه_نووس_نرخ[12];unsigned 수=0;do{ڕه_نووس_نرخ[수++]='0'+نرخ%10;نرخ/=10;}while(نرخ);
    while(수)보드글자쓰기(ڕه_نووس_نرخ[--수]);보드글자쓰기(10);
}
static assh_status_t ئامادە_کردن_بیرگە(void *دەیتا,void **ناونیشان,size_t گۆڕینی_ئەندازە,enum assh_alloc_type_e 종류) {
    (void)دەیتا;(void)종류;
    if(!گۆڕینی_ئەندازە){وەشان_دوورەدەس(*ناونیشان);*ناونیشان=0;return ASSH_OK;}
    void *새주소=원격재할당(*ناونیشان,گۆڕینی_ئەندازە);
    if(!새주소)return ASSH_ERR_MEM;*ناونیشان=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *دەیتا,const struct assh_buffer_s *تۆو_نرخ) {
    (void)دەیتا;(void)تۆو_نرخ;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *دەیتا,uint8_t *결과,size_t درێژی_نرخ,uint_fast8_t 종류) {
    (void)دەیتا;(void)종류;if(درێژی_نرخ>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,درێژی_نرخ)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *دەیتا){(void)دەیتا;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void داخستن_گرێدان(void) {
    인증됨=셸시작됨=0;کاناڵ_تێنووسین=0;
    if(گرێدان_e05f319b)assh_session_release(گرێدان_e05f319b);گرێدان_e05f319b=0;
    if(هاوتا_نرخ>=0)داخستن_تۆڕ(هاوتا_نرخ);هاوتا_نرخ=-1;فەرمان_چاپکردن=0;دوایی_کردن_دۆخ=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *دەیتا,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=دەیتا[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int نووسە_نرخ=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return نووسە_نرخ;
}
void 원격출력(unsigned char نووسە_نرخ) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=نووسە_نرخ==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=نووسە_نرخ;이전출력=نووسە_نرخ;
}
uintptr_t 보드원격명령끝(uintptr_t دۆخ_نرخ){if(셸시작됨&&فەرمان_چاپکردن)دوایی_کردن_دۆخ=(int)دۆخ_نرخ;return 0;}
uintptr_t 보드원격대기(uintptr_t دۆخ_نرخ){توێکڵ_چاوەڕوانی=دۆخ_نرخ!=0;return 0;}
static int ئامادە_کردن_توێکڵ(void) {
    if(듣는곳>=0)return 0;
    if(!ریزکردنی_سیاق_نرخ){
        assh_status_t هەڵە=assh_context_create(&ریزکردنی_سیاق_نرخ,ASSH_SERVER,ئامادە_کردن_بیرگە,0,&난수기,0);
        if(هەڵە)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *ڕێگا_دۆخ[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        هەڵە=assh_algo_register(ریزکردنی_سیاق_نرخ,ASSH_SAFETY_WEAK,ڕێگا_دۆخ);
        if(!هەڵە)هەڵە=assh_service_register_va(ریزکردنی_سیاق_نرخ,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=ئامێر_کلیل;
        if(!هەڵە)هەڵە=assh_key_load(ریزکردنی_سیاق_نرخ,assh_context_keys(ریزکردنی_سیاق_نرخ),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(ئامێر_کلیل));
        if(هەڵە){진단("SSH init error ",هەڵە);assh_context_release(ریزکردنی_سیاق_نرخ);ریزکردنی_سیاق_نرخ=0;return -5;}
    }
    int دەرگا_نرخ=통신끝점만들기(1);if(دەرگا_نرخ<0)return دەرگا_نرخ;통신주소재사용(دەرگا_نرخ);
    int 결과=망주소묶기(دەرگا_نرخ,0,22);if(!결과)결과=연결기다리기(دەرگا_نرخ);
    if(결과<0){داخستن_تۆڕ(دەرگا_نرخ);return 결과;}듣는곳=دەرگا_نرخ;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t ئاکشن) {
    if(종류==1)return(uint32_t)کۆنترۆڵ_دوورەدەس_نیشاندان(ئاکشن);
    if(ئاکشن==0){داخستن_گرێدان();if(듣는곳>=0)داخستن_تۆڕ(듣는곳);듣는곳=-1;return 0;}
    if(ئاکشن==1){دەسپێک_هەڵە=ئامادە_کردن_توێکڵ();return(uint32_t)دەسپێک_هەڵە;}
    return(uint32_t)(듣는곳>=0?1:دەسپێک_هەڵە);
}
void ئامادە_کردن_دوورەدەس(void){دەسپێک_هەڵە=ئامادە_کردن_توێکڵ();کۆنترۆڵ_دوورەدەس_نیشاندان(1);}
static int 같은말(const struct assh_cbuffer_s *دەیتا,const char *وشە_دەق) {
    size_t درێژی_نرخ=strlen(وشە_دەق);return دەیتا->size==درێژی_نرخ&&!memcmp(دەیتا->data,وشە_دەق,درێژی_نرخ);
}
static int 터미널요청(const struct assh_cbuffer_s *دەیتا) {
    if(دەیتا->size<24)return 0;
    const unsigned char *자료위치=دەیتا->data;unsigned درێژی_نرخ=assh_load_u32(자료위치);
    if(درێژی_نرخ>128||دەیتا->size<درێژی_نرخ+24)return 0;
    unsigned دۆخ_نرخ_a83655ea=assh_load_u32(자료위치+4+درێژی_نرخ+16);
    return دۆخ_نرخ_a83655ea<=2048&&دەیتا->size==درێژی_نرخ+24+دۆخ_نرخ_a83655ea;
}
static void 요청처리(struct assh_event_request_s *پێشهات) {
    if(!인증됨||پێشهات->ch!=کاناڵ_تێنووسین||!کاناڵ_تێنووسین)return;
    if(같은말(&پێشهات->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&پێشهات->rq_data))پێشهات->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&پێشهات->type,"window-change")) {
        if(셸시작됨&&پێشهات->rq_data.size==16)پێشهات->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!توێکڵ_چاوەڕوانی)return;
    const unsigned char *فەرمان=0;unsigned درێژی_نرخ=0;
    if(같은말(&پێشهات->type,"exec")) {
        if(پێشهات->rq_data.size<4)return;
        درێژی_نرخ=assh_load_u32(پێشهات->rq_data.data);
        if(!درێژی_نرخ||درێژی_نرخ>2048||پێشهات->rq_data.size!=درێژی_نرخ+4)return;
        فەرمان=پێشهات->rq_data.data+4;
        for(unsigned 순번=0;순번<درێژی_نرخ;순번++)if(!فەرمان[순번])return;
        فەرمان_چاپکردن=1;
    }else if(!같은말(&پێشهات->type,"shell")||پێشهات->rq_data.size)return;
    if(sizeof(입력줄)-입력수<درێژی_نرخ+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(درێژی_نرخ)원격입력넣기(فەرمان,درێژی_نرخ);원격입력넣기(&끝,1);
    셸시작됨=1;پێشهات->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!فەرمان_چاپکردن){const char *رێخۆشکەر_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*رێخۆشکەر_eb81d7d9)원격출력(*رێخۆشکەر_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(هاوتا_نرخ<0){if(지금<재접속시각)return;هاوتا_نرخ=망연결받기(듣는곳);if(هاوتا_نرخ<0)return;
        گرێدان_کات=지금;assh_status_t هەڵە=assh_session_create(ریزکردنی_سیاق_نرخ,&گرێدان_e05f319b);
        if(هەڵە){گرێدان_e05f319b=0;진단("SSH session error ",هەڵە);داخستن_گرێدان();return;}}
    if((!인증됨&&지금-گرێدان_کات>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){داخستن_گرێدان();return;}
    if(کاناڵ_تێنووسین&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t هەڵە=assh_channel_data(کاناڵ_تێنووسین,출력줄+출력앞,&수);
            if(!هەڵە){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(هەڵە!=ASSH_NO_DATA){داخستن_گرێدان();return;}
        }
        if(دوایی_کردن_دۆخ>=0&&!출력수){unsigned char دۆخ_نرخ[4];assh_store_u32(دۆخ_نرخ,(uint32_t)دوایی_کردن_دۆخ);
            if(assh_request(گرێدان_e05f319b,کاناڵ_تێنووسین,"exit-status",11,دۆخ_نرخ,4,0)||assh_channel_eof(کاناڵ_تێنووسین)||assh_channel_close(کاناڵ_تێنووسین)) {داخستن_گرێدان();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned زنجیره_نرخ=0;زنجیره_نرخ<16;زنجیره_نرخ++) {
        struct assh_event_s پێشهات;
        if(!assh_event_get(گرێدان_e05f319b,&پێشهات,지금/1000)){داخستن_گرێدان();return;}
        assh_status_t هەڵە=ASSH_OK;int 쉬기=0,끊기=0;
        switch(پێشهات.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(هاوتا_نرخ,پێشهات.transport.read.buf.data,پێشهات.transport.read.buf.size);
            if(수>0)پێشهات.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(هاوتا_نرخ,پێشهات.transport.write.buf.data,پێشهات.transport.write.buf.size);
            if(수>0)پێشهات.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            پێشهات.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(پێشهات.userauth_server.methods.retries>3)پێشهات.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *دەیتا=&پێشهات.userauth_server.password;
            if(같은말(&دەیتا->username,"user")&&دەیتا->password.size<=256&&!دەیتا->new_password.size) {
                unsigned char 요약[32];원격요약(دەیتا->password.data,دەیتا->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)دەیتا->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *دەیتا=&پێشهات.connection.channel_open;
            if(인증됨&&!کاناڵ_تێنووسین&&توێکڵ_چاوەڕوانی&&같은말(&دەیتا->type,"session")&&!دەیتا->rq_data.size) {
                دەیتا->reply=ASSH_CONNECTION_REPLY_SUCCESS;دەیتا->pkt_size=4096;
                دەیتا->win_size=-1;کاناڵ_تێنووسین=دەیتا->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&پێشهات.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *دەیتا=&پێشهات.connection.channel_data;
            if(!셸시작됨||دەیتا->ch!=کاناڵ_تێنووسین||دەیتا->ext){끊기=1;break;}
            unsigned 수=دەیتا->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(دەیتا->data.data[순번]==4){دوایی_کردن_دۆخ=0;수=순번;دەیتا->transferred=دەیتا->data.size;break;}
            원격입력넣기(دەیتا->data.data,수);if(!دەیتا->transferred)دەیتا->transferred=수;
            if(!수&&دوایی_کردن_دۆخ<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: کاناڵ_تێنووسین=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",پێشهات.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(گرێدان_e05f319b,&پێشهات,هەڵە);
        if(끊기){داخستن_گرێدان();return;}if(쉬기)return;
    }
}
