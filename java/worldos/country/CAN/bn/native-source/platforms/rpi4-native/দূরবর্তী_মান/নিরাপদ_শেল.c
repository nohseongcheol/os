/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "দূরবর্তী_মান.h"
#include "암호기반.h"
#include "বিবরণী.h"
#include "../নেটওয়ার্ক_গাদা/নেটওয়ার্ক_গাদা.h"
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
static struct assh_context_s *প্রসঙ্গ_মান;
static struct assh_session_s *সংযোগ_e05f319b;
static struct assh_channel_s *চ্যানেল_ভুক্তি;
static int 듣는곳=-1,পিয়ার_মান=-1,인증됨,셸시작됨,আদেশ_টাইপ_করুন,শেষ_করা_অবস্হা=-1,닫을예정,বুট_ত্রুটি,শেল_প্রতীক্ষা;
static uintptr_t সংযোগ_সময়,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *শব্দ_পাঠ,unsigned মান) {
    while(*শব্দ_পাঠ)보드글자쓰기(*শব্দ_পাঠ++);
    char সংখ্যা_মান[12];unsigned 수=0;do{সংখ্যা_মান[수++]='0'+মান%10;মান/=10;}while(মান);
    while(수)보드글자쓰기(সংখ্যা_মান[--수]);보드글자쓰기(10);
}
static assh_status_t প্রস্তুত_করুন_মেমরি(void *ডাটা,void **ইমেইল,size_t আকার,enum assh_alloc_type_e 종류) {
    (void)ডাটা;(void)종류;
    if(!আকার){রিলিজ_দূরবর্তী(*ইমেইল);*ইমেইল=0;return ASSH_OK;}
    void *새주소=원격재할당(*ইমেইল,আকার);
    if(!새주소)return ASSH_ERR_MEM;*ইমেইল=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ডাটা,const struct assh_buffer_s *সীড_মান) {
    (void)ডাটা;(void)সীড_মান;unsigned char 시험[32];int পরিমাপ=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return পরিমাপ?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ডাটা,uint8_t *পরিমাপ,size_t দৈর্ঘ্য_মান,uint_fast8_t 종류) {
    (void)ডাটা;(void)종류;if(দৈর্ঘ্য_মান>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(পরিমাপ,দৈর্ঘ্য_মান)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ডাটা){(void)ডাটা;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void বন্ধ_সংযোগ(void) {
    인증됨=셸시작됨=0;চ্যানেল_ভুক্তি=0;
    if(সংযোগ_e05f319b)assh_session_release(সংযোগ_e05f319b);সংযোগ_e05f319b=0;
    if(পিয়ার_মান>=0)বন্ধ_নেটওয়ার্ক(পিয়ার_মান);পিয়ার_মান=-1;আদেশ_টাইপ_করুন=0;শেষ_করা_অবস্হা=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ডাটা,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=ডাটা[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int অক্ষর_মান=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return অক্ষর_মান;
}
void 원격출력(unsigned char অক্ষর_মান) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=অক্ষর_মান==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=অক্ষর_মান;이전출력=অক্ষর_মান;
}
uintptr_t বোর্ড_শেষ_করা_দূরবর্তী_আদেশ(uintptr_t অবস্হা_মান){if(셸시작됨&&আদেশ_টাইপ_করুন)শেষ_করা_অবস্হা=(int)অবস্হা_মান;return 0;}
uintptr_t বোর্ড_দূরবর্তী_অপেক্ষা(uintptr_t অবস্হা_মান){শেল_প্রতীক্ষা=অবস্হা_মান!=0;return 0;}
static int প্রস্তুত_করুন_শেল(void) {
    if(듣는곳>=0)return 0;
    if(!প্রসঙ্গ_মান){
        assh_status_t ত্রুটি=assh_context_create(&প্রসঙ্গ_মান,ASSH_SERVER,প্রস্তুত_করুন_মেমরি,0,&난수기,0);
        if(ত্রুটি)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *পদ্ধতি_মোড[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ত্রুটি=assh_algo_register(প্রসঙ্গ_মান,ASSH_SAFETY_WEAK,পদ্ধতি_মোড);
        if(!ত্রুটি)ত্রুটি=assh_service_register_va(প্রসঙ্গ_মান,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=ডিভাইস_কী;
        if(!ত্রুটি)ত্রুটি=assh_key_load(প্রসঙ্গ_মান,assh_context_keys(প্রসঙ্গ_মান),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(ডিভাইস_কী));
        if(ত্রুটি){진단("SSH init error ",ত্রুটি);assh_context_release(প্রসঙ্গ_মান);প্রসঙ্গ_মান=0;return -5;}
    }
    int পোর্ট_মান=통신끝점만들기(1);if(পোর্ট_মান<0)return পোর্ট_মান;통신주소재사용(পোর্ট_মান);
    int পরিমাপ=망주소묶기(পোর্ট_মান,0,22);if(!পরিমাপ)পরিমাপ=연결기다리기(পোর্ট_মান);
    if(পরিমাপ<0){বন্ধ_নেটওয়ার্ক(পোর্ট_মান);return পরিমাপ;}듣는곳=পোর্ট_মান;return 0;
}
uintptr_t বোর্ড_শ্যাডো_করা(uintptr_t 종류,uintptr_t কাজ) {
    if(종류==1)return(uint32_t)নিয়ন্ত্রণ_দূরবর্তী_ডিসপ্লে(কাজ);
    if(কাজ==0){বন্ধ_সংযোগ();if(듣는곳>=0)বন্ধ_নেটওয়ার্ক(듣는곳);듣는곳=-1;return 0;}
    if(কাজ==1){বুট_ত্রুটি=প্রস্তুত_করুন_শেল();return(uint32_t)বুট_ত্রুটি;}
    return(uint32_t)(듣는곳>=0?1:বুট_ত্রুটি);
}
void প্রস্তুত_করুন_দূরবর্তী(void){বুট_ত্রুটি=প্রস্তুত_করুন_শেল();নিয়ন্ত্রণ_দূরবর্তী_ডিসপ্লে(1);}
static int 같은말(const struct assh_cbuffer_s *ডাটা,const char *শব্দ_পাঠ) {
    size_t দৈর্ঘ্য_মান=strlen(শব্দ_পাঠ);return ডাটা->size==দৈর্ঘ্য_মান&&!memcmp(ডাটা->data,শব্দ_পাঠ,দৈর্ঘ্য_মান);
}
static int 터미널요청(const struct assh_cbuffer_s *ডাটা) {
    if(ডাটা->size<24)return 0;
    const unsigned char *ডাটা_পদ=ডাটা->data;unsigned দৈর্ঘ্য_মান=assh_load_u32(ডাটা_পদ);
    if(দৈর্ঘ্য_মান>128||ডাটা->size<দৈর্ঘ্য_মান+24)return 0;
    unsigned মোড_মান=assh_load_u32(ডাটা_পদ+4+দৈর্ঘ্য_মান+16);
    return মোড_মান<=2048&&ডাটা->size==দৈর্ঘ্য_মান+24+মোড_মান;
}
static void 요청처리(struct assh_event_request_s *ঘটনা) {
    if(!인증됨||ঘটনা->ch!=চ্যানেল_ভুক্তি||!চ্যানেল_ভুক্তি)return;
    if(같은말(&ঘটনা->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&ঘটনা->rq_data))ঘটনা->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ঘটনা->type,"window-change")) {
        if(셸시작됨&&ঘটনা->rq_data.size==16)ঘটনা->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!শেল_প্রতীক্ষা)return;
    const unsigned char *আদেশ=0;unsigned দৈর্ঘ্য_মান=0;
    if(같은말(&ঘটনা->type,"exec")) {
        if(ঘটনা->rq_data.size<4)return;
        দৈর্ঘ্য_মান=assh_load_u32(ঘটনা->rq_data.data);
        if(!দৈর্ঘ্য_মান||দৈর্ঘ্য_মান>2048||ঘটনা->rq_data.size!=দৈর্ঘ্য_মান+4)return;
        আদেশ=ঘটনা->rq_data.data+4;
        for(unsigned 순번=0;순번<দৈর্ঘ্য_মান;순번++)if(!আদেশ[순번])return;
        আদেশ_টাইপ_করুন=1;
    }else if(!같은말(&ঘটনা->type,"shell")||ঘটনা->rq_data.size)return;
    if(sizeof(입력줄)-입력수<দৈর্ঘ্য_মান+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(দৈর্ঘ্য_মান)원격입력넣기(আদেশ,দৈর্ঘ্য_মান);원격입력넣기(&끝,1);
    셸시작됨=1;ঘটনা->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!আদেশ_টাইপ_করুন){const char *স্বনিবন্ধ_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*স্বনিবন্ধ_eb81d7d9)원격출력(*স্বনিবন্ধ_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t নাউ_মান=보드밀리초();
    if(পিয়ার_মান<0){if(নাউ_মান<재접속시각)return;পিয়ার_মান=망연결받기(듣는곳);if(পিয়ার_মান<0)return;
        সংযোগ_সময়=নাউ_মান;assh_status_t ত্রুটি=assh_session_create(প্রসঙ্গ_মান,&সংযোগ_e05f319b);
        if(ত্রুটি){সংযোগ_e05f319b=0;진단("SSH session error ",ত্রুটি);বন্ধ_সংযোগ();return;}}
    if((!인증됨&&নাউ_মান-সংযোগ_সময়>30000)||닫을예정==2||(닫을예정&&নাউ_মান>=닫는시각)){বন্ধ_সংযোগ();return;}
    if(চ্যানেল_ভুক্তি&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ত্রুটি=assh_channel_data(চ্যানেল_ভুক্তি,출력줄+출력앞,&수);
            if(!ত্রুটি){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ত্রুটি!=ASSH_NO_DATA){বন্ধ_সংযোগ();return;}
        }
        if(শেষ_করা_অবস্হা>=0&&!출력수){unsigned char অবস্হা_মান[4];assh_store_u32(অবস্হা_মান,(uint32_t)শেষ_করা_অবস্হা);
            if(assh_request(সংযোগ_e05f319b,চ্যানেল_ভুক্তি,"exit-status",11,অবস্হা_মান,4,0)||assh_channel_eof(চ্যানেল_ভুক্তি)||assh_channel_close(চ্যানেল_ভুক্তি)) {বন্ধ_সংযোগ();return;}
            닫을예정=1;닫는시각=নাউ_মান+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s ঘটনা;
        if(!assh_event_get(সংযোগ_e05f319b,&ঘটনা,নাউ_মান/1000)){বন্ধ_সংযোগ();return;}
        assh_status_t ত্রুটি=ASSH_OK;int 쉬기=0,끊기=0;
        switch(ঘটনা.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(পিয়ার_মান,ঘটনা.transport.read.buf.data,ঘটনা.transport.read.buf.size);
            if(수>0)ঘটনা.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(পিয়ার_মান,ঘটনা.transport.write.buf.data,ঘটনা.transport.write.buf.size);
            if(수>0)ঘটনা.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ঘটনা.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ঘটনা.userauth_server.methods.retries>3)ঘটনা.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ডাটা=&ঘটনা.userauth_server.password;
            if(같은말(&ডাটা->username,"user")&&ডাটা->password.size<=256&&!ডাটা->new_password.size) {
                unsigned char সামারি_মান[32];দূরবর্তী_সামারি(ডাটা->password.data,ডাটা->password.size,সামারি_মান);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=সামারি_মান[순번]^শেল_পাসওয়ার্ড_সামারি[순번];memset(সামারি_মান,0,32);
                if(!차이)ডাটা->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ডাটা=&ঘটনা.connection.channel_open;
            if(인증됨&&!চ্যানেল_ভুক্তি&&শেল_প্রতীক্ষা&&같은말(&ডাটা->type,"session")&&!ডাটা->rq_data.size) {
                ডাটা->reply=ASSH_CONNECTION_REPLY_SUCCESS;ডাটা->pkt_size=4096;
                ডাটা->win_size=-1;চ্যানেল_ভুক্তি=ডাটা->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&ঘটনা.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ডাটা=&ঘটনা.connection.channel_data;
            if(!셸시작됨||ডাটা->ch!=চ্যানেল_ভুক্তি||ডাটা->ext){끊기=1;break;}
            unsigned 수=ডাটা->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(ডাটা->data.data[순번]==4){শেষ_করা_অবস্হা=0;수=순번;ডাটা->transferred=ডাটা->data.size;break;}
            원격입력넣기(ডাটা->data.data,수);if(!ডাটা->transferred)ডাটা->transferred=수;
            if(!수&&শেষ_করা_অবস্হা<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: চ্যানেল_ভুক্তি=0;셸시작됨=0;닫을예정=1;닫는시각=নাউ_মান+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ঘটনা.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(সংযোগ_e05f319b,&ঘটনা,ত্রুটি);
        if(끊기){বন্ধ_সংযোগ();return;}if(쉬기)return;
    }
}
