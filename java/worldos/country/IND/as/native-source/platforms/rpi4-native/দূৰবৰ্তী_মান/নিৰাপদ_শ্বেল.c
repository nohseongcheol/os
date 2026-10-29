/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "দূৰবৰ্তী_মান.h"
#include "암호기반.h"
#include "প্ৰ_ফাইল.h"
#include "../নেটৱৰ্ক_ষ্টেক/নেটৱৰ্ক_ষ্টেক.h"
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
static struct assh_context_s *প্ৰসংগ_মান;
static struct assh_session_s *সংযোগ_e05f319b;
static struct assh_channel_s *চেনেল_প্রবিষ্ট;
static int 듣는곳=-1,পীয়েৰ_মান=-1,인증됨,셸시작됨,আদেশ_প্ৰকাৰ,অন্ত_কৰক_অৱস্থা=-1,닫을예정,বুট_ত্ৰুটি,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *말,unsigned মান) {
    while(*말)보드글자쓰기(*말++);
    char অংক_মান[12];unsigned 수=0;do{অংক_মান[수++]='0'+মান%10;মান/=10;}while(মান);
    while(수)보드글자쓰기(অংক_মান[--수]);보드글자쓰기(10);
}
static assh_status_t প্ৰস্তুত_কৰক_মেম_ৰি(void *ডাটা,void **ঠিকনা,size_t মাপ,enum assh_alloc_type_e 종류) {
    (void)ডাটা;(void)종류;
    if(!মাপ){ৰিলিজ_দূৰবৰ্তী(*ঠিকনা);*ঠিকনা=0;return ASSH_OK;}
    void *새주소=원격재할당(*ঠিকনা,মাপ);
    if(!새주소)return ASSH_ERR_MEM;*ঠিকনা=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ডাটা,const struct assh_buffer_s *বীজ_মান) {
    (void)ডাটা;(void)বীজ_মান;unsigned char 시험[32];int পৰিমাপ=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return পৰিমাপ?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ডাটা,uint8_t *পৰিমাপ,size_t দৈর্ঘ্য_মান,uint_fast8_t 종류) {
    (void)ডাটা;(void)종류;if(দৈর্ঘ্য_মান>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(পৰিমাপ,দৈর্ঘ্য_মান)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ডাটা){(void)ডাটা;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void বন্ধ_কৰক_সংযোগ(void) {
    인증됨=셸시작됨=0;চেনেল_প্রবিষ্ট=0;
    if(সংযোগ_e05f319b)assh_session_release(সংযোগ_e05f319b);সংযোগ_e05f319b=0;
    if(পীয়েৰ_মান>=0)বন্ধ_কৰক_নেটৱৰ্ক(পীয়েৰ_মান);পীয়েৰ_মান=-1;আদেশ_প্ৰকাৰ=0;অন্ত_কৰক_অৱস্থা=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ডাটা,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=ডাটা[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int বৰ্ণ_মান=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return বৰ্ণ_মান;
}
void 원격출력(unsigned char বৰ্ণ_মান) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=বৰ্ণ_মান==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=বৰ্ণ_মান;이전출력=বৰ্ণ_মান;
}
uintptr_t ব_ৰ্ড_অন্ত_কৰক_দূৰবৰ্তী_আদেশ(uintptr_t অৱস্থা_মান){if(셸시작됨&&আদেশ_প্ৰকাৰ)অন্ত_কৰক_অৱস্থা=(int)অৱস্থা_মান;return 0;}
uintptr_t 보드원격대기(uintptr_t অৱস্থা_মান){셸대기중=অৱস্থা_মান!=0;return 0;}
static int প্ৰস্তুত_কৰক_শ্বেল(void) {
    if(듣는곳>=0)return 0;
    if(!প্ৰসংগ_মান){
        assh_status_t ত্ৰুটি=assh_context_create(&প্ৰসংগ_মান,ASSH_SERVER,প্ৰস্তুত_কৰক_মেম_ৰি,0,&난수기,0);
        if(ত্ৰুটি)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *পদ্ধতি_মোড[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ত্ৰুটি=assh_algo_register(প্ৰসংগ_মান,ASSH_SAFETY_WEAK,পদ্ধতি_মোড);
        if(!ত্ৰুটি)ত্ৰুটি=assh_service_register_va(প্ৰসংগ_মান,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=চেলফোন_কী;
        if(!ত্ৰুটি)ত্ৰুটি=assh_key_load(প্ৰসংগ_মান,assh_context_keys(প্ৰসংগ_মান),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(চেলফোন_কী));
        if(ত্ৰুটি){진단("SSH init error ",ত্ৰুটি);assh_context_release(প্ৰসংগ_মান);প্ৰসংগ_মান=0;return -5;}
    }
    int পৰ্ট_মান=통신끝점만들기(1);if(পৰ্ট_মান<0)return পৰ্ট_মান;통신주소재사용(পৰ্ট_মান);
    int পৰিমাপ=망주소묶기(পৰ্ট_মান,0,22);if(!পৰিমাপ)পৰিমাপ=연결기다리기(পৰ্ট_মান);
    if(পৰিমাপ<0){বন্ধ_কৰক_নেটৱৰ্ক(পৰ্ট_মান);return পৰিমাপ;}듣는곳=পৰ্ট_মান;return 0;
}
uintptr_t ব_ৰ্ড_ছাঁয়াকৰণ(uintptr_t 종류,uintptr_t কাৰ্য্য) {
    if(종류==1)return(uint32_t)নিয়ন্ত্রণ_দূৰবৰ্তী_প্রদর্শন(কাৰ্য্য);
    if(কাৰ্য্য==0){বন্ধ_কৰক_সংযোগ();if(듣는곳>=0)বন্ধ_কৰক_নেটৱৰ্ক(듣는곳);듣는곳=-1;return 0;}
    if(কাৰ্য্য==1){বুট_ত্ৰুটি=প্ৰস্তুত_কৰক_শ্বেল();return(uint32_t)বুট_ত্ৰুটি;}
    return(uint32_t)(듣는곳>=0?1:বুট_ত্ৰুটি);
}
void প্ৰস্তুত_কৰক_দূৰবৰ্তী(void){বুট_ত্ৰুটি=প্ৰস্তুত_কৰক_শ্বেল();নিয়ন্ত্রণ_দূৰবৰ্তী_প্রদর্শন(1);}
static int 같은말(const struct assh_cbuffer_s *ডাটা,const char *말) {
    size_t দৈর্ঘ্য_মান=strlen(말);return ডাটা->size==দৈর্ঘ্য_মান&&!memcmp(ডাটা->data,말,দৈর্ঘ্য_মান);
}
static int 터미널요청(const struct assh_cbuffer_s *ডাটা) {
    if(ডাটা->size<24)return 0;
    const unsigned char *ডাটা_স্থান_সলনি_কৰক=ডাটা->data;unsigned দৈর্ঘ্য_মান=assh_load_u32(ডাটা_স্থান_সলনি_কৰক);
    if(দৈর্ঘ্য_মান>128||ডাটা->size<দৈর্ঘ্য_মান+24)return 0;
    unsigned মোড_মান=assh_load_u32(ডাটা_স্থান_সলনি_কৰক+4+দৈর্ঘ্য_মান+16);
    return মোড_মান<=2048&&ডাটা->size==দৈর্ঘ্য_মান+24+মোড_মান;
}
static void 요청처리(struct assh_event_request_s *ইভেণ্ট) {
    if(!인증됨||ইভেণ্ট->ch!=চেনেল_প্রবিষ্ট||!চেনেল_প্রবিষ্ট)return;
    if(같은말(&ইভেণ্ট->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&ইভেণ্ট->rq_data))ইভেণ্ট->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ইভেণ্ট->type,"window-change")) {
        if(셸시작됨&&ইভেণ্ট->rq_data.size==16)ইভেণ্ট->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *কমান্ড=0;unsigned দৈর্ঘ্য_মান=0;
    if(같은말(&ইভেণ্ট->type,"exec")) {
        if(ইভেণ্ট->rq_data.size<4)return;
        দৈর্ঘ্য_মান=assh_load_u32(ইভেণ্ট->rq_data.data);
        if(!দৈর্ঘ্য_মান||দৈর্ঘ্য_মান>2048||ইভেণ্ট->rq_data.size!=দৈর্ঘ্য_মান+4)return;
        কমান্ড=ইভেণ্ট->rq_data.data+4;
        for(unsigned 순번=0;순번<দৈর্ঘ্য_মান;순번++)if(!কমান্ড[순번])return;
        আদেশ_প্ৰকাৰ=1;
    }else if(!같은말(&ইভেণ্ট->type,"shell")||ইভেণ্ট->rq_data.size)return;
    if(sizeof(입력줄)-입력수<দৈর্ঘ্য_মান+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(দৈর্ঘ্য_মান)원격입력넣기(কমান্ড,দৈর্ঘ্য_মান);원격입력넣기(&끝,1);
    셸시작됨=1;ইভেণ্ট->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!আদেশ_প্ৰকাৰ){const char *ৰিডমি_ফাইল_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*ৰিডমি_ফাইল_eb81d7d9)원격출력(*ৰিডমি_ফাইল_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(পীয়েৰ_মান<0){if(지금<재접속시각)return;পীয়েৰ_মান=망연결받기(듣는곳);if(পীয়েৰ_মান<0)return;
        접속시각=지금;assh_status_t ত্ৰুটি=assh_session_create(প্ৰসংগ_মান,&সংযোগ_e05f319b);
        if(ত্ৰুটি){সংযোগ_e05f319b=0;진단("SSH session error ",ত্ৰুটি);বন্ধ_কৰক_সংযোগ();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){বন্ধ_কৰক_সংযোগ();return;}
    if(চেনেল_প্রবিষ্ট&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ত্ৰুটি=assh_channel_data(চেনেল_প্রবিষ্ট,출력줄+출력앞,&수);
            if(!ত্ৰুটি){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ত্ৰুটি!=ASSH_NO_DATA){বন্ধ_কৰক_সংযোগ();return;}
        }
        if(অন্ত_কৰক_অৱস্থা>=0&&!출력수){unsigned char অৱস্থা_মান[4];assh_store_u32(অৱস্থা_মান,(uint32_t)অন্ত_কৰক_অৱস্থা);
            if(assh_request(সংযোগ_e05f319b,চেনেল_প্রবিষ্ট,"exit-status",11,অৱস্থা_মান,4,0)||assh_channel_eof(চেনেল_প্রবিষ্ট)||assh_channel_close(চেনেল_প্রবিষ্ট)) {বন্ধ_কৰক_সংযোগ();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s ইভেণ্ট;
        if(!assh_event_get(সংযোগ_e05f319b,&ইভেণ্ট,지금/1000)){বন্ধ_কৰক_সংযোগ();return;}
        assh_status_t ত্ৰুটি=ASSH_OK;int 쉬기=0,끊기=0;
        switch(ইভেণ্ট.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(পীয়েৰ_মান,ইভেণ্ট.transport.read.buf.data,ইভেণ্ট.transport.read.buf.size);
            if(수>0)ইভেণ্ট.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(পীয়েৰ_মান,ইভেণ্ট.transport.write.buf.data,ইভেণ্ট.transport.write.buf.size);
            if(수>0)ইভেণ্ট.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ইভেণ্ট.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ইভেণ্ট.userauth_server.methods.retries>3)ইভেণ্ট.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ডাটা=&ইভেণ্ট.userauth_server.password;
            if(같은말(&ডাটা->username,"user")&&ডাটা->password.size<=256&&!ডাটা->new_password.size) {
                unsigned char সাৰাংশ_মান[32];দূৰবৰ্তী_সাৰাংশ(ডাটা->password.data,ডাটা->password.size,সাৰাংশ_মান);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=সাৰাংশ_মান[순번]^শ্বেল_পাছৱৰ্ড_সাৰাংশ[순번];memset(সাৰাংশ_মান,0,32);
                if(!차이)ডাটা->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ডাটা=&ইভেণ্ট.connection.channel_open;
            if(인증됨&&!চেনেল_প্রবিষ্ট&&셸대기중&&같은말(&ডাটা->type,"session")&&!ডাটা->rq_data.size) {
                ডাটা->reply=ASSH_CONNECTION_REPLY_SUCCESS;ডাটা->pkt_size=4096;
                ডাটা->win_size=-1;চেনেল_প্রবিষ্ট=ডাটা->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&ইভেণ্ট.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ডাটা=&ইভেণ্ট.connection.channel_data;
            if(!셸시작됨||ডাটা->ch!=চেনেল_প্রবিষ্ট||ডাটা->ext){끊기=1;break;}
            unsigned 수=ডাটা->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(ডাটা->data.data[순번]==4){অন্ত_কৰক_অৱস্থা=0;수=순번;ডাটা->transferred=ডাটা->data.size;break;}
            원격입력넣기(ডাটা->data.data,수);if(!ডাটা->transferred)ডাটা->transferred=수;
            if(!수&&অন্ত_কৰক_অৱস্থা<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: চেনেল_প্রবিষ্ট=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ইভেণ্ট.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(সংযোগ_e05f319b,&ইভেণ্ট,ত্ৰুটি);
        if(끊기){বন্ধ_কৰক_সংযোগ();return;}if(쉬기)return;
    }
}
