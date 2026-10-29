/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "დისტანციური_მნიშვნელობა.h"
#include "암호기반.h"
#include "პროფილი.h"
#include "../ქსელი_დასტა/ქსელი_დასტა.h"
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
static struct assh_session_s *კავშირი_e05f319b;
static struct assh_channel_s *არხი_შენატანი;
static int 듣는곳=-1,კვანძი_მნიშვნელობა_6a3b6fa7=-1,인증됨,셸시작됨,ბრძანება_აკრეფა,დასასრული_სტატუსი=-1,닫을예정,ჩატვირთვა_შეცდომა,გარემო_ლოდინი;
static uintptr_t კავშირი_დრო,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *სიტყვები_ტექსტი,unsigned მნიშვნელობა) {
    while(*სიტყვები_ტექსტი)보드글자쓰기(*სიტყვები_ტექსტი++);
    char ციფრი_მნიშვნელობა[12];unsigned 수=0;do{ციფრი_მნიშვნელობა[수++]='0'+მნიშვნელობა%10;მნიშვნელობა/=10;}while(მნიშვნელობა);
    while(수)보드글자쓰기(ციფრი_მნიშვნელობა[--수]);보드글자쓰기(10);
}
static assh_status_t მომზადება_მეხსიერება(void *მონაცემები,void **მისამართი,size_t ზომა,enum assh_alloc_type_e 종류) {
    (void)მონაცემები;(void)종류;
    if(!ზომა){რელიზი_დისტანციური(*მისამართი);*მისამართი=0;return ASSH_OK;}
    void *새주소=원격재할당(*მისამართი,ზომა);
    if(!새주소)return ASSH_ERR_MEM;*მისამართი=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *მონაცემები,const struct assh_buffer_s *საწყისი_მნიშვნელობის_მინიჭება_მნიშვნელობა) {
    (void)მონაცემები;(void)საწყისი_მნიშვნელობის_მინიჭება_მნიშვნელობა;unsigned char 시험[32];int გაზომვა=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return გაზომვა?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *მონაცემები,uint8_t *გაზომვა,size_t სიგრძე_მნიშვნელობა,uint_fast8_t 종류) {
    (void)მონაცემები;(void)종류;if(სიგრძე_მნიშვნელობა>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(გაზომვა,სიგრძე_მნიშვნელობა)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *მონაცემები){(void)მონაცემები;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void დახურვა_კავშირი(void) {
    인증됨=셸시작됨=0;არხი_შენატანი=0;
    if(კავშირი_e05f319b)assh_session_release(კავშირი_e05f319b);კავშირი_e05f319b=0;
    if(კვანძი_მნიშვნელობა_6a3b6fa7>=0)დახურვა_ქსელი(კვანძი_მნიშვნელობა_6a3b6fa7);კვანძი_მნიშვნელობა_6a3b6fa7=-1;ბრძანება_აკრეფა=0;დასასრული_სტატუსი=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *მონაცემები,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=მონაცემები[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int სიმბოლო_მნიშვნელობა_068c2631=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return სიმბოლო_მნიშვნელობა_068c2631;
}
void 원격출력(unsigned char სიმბოლო_მნიშვნელობა_068c2631) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=სიმბოლო_მნიშვნელობა_068c2631==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=სიმბოლო_მნიშვნელობა_068c2631;이전출력=სიმბოლო_მნიშვნელობა_068c2631;
}
uintptr_t დაფა_დასასრული_დისტანციური_ბრძანება(uintptr_t სტატუსი_მნიშვნელობა){if(셸시작됨&&ბრძანება_აკრეფა)დასასრული_სტატუსი=(int)სტატუსი_მნიშვნელობა;return 0;}
uintptr_t დაფა_დისტანციური_მოლოდინი(uintptr_t სტატუსი_მნიშვნელობა){გარემო_ლოდინი=სტატუსი_მნიშვნელობა!=0;return 0;}
static int მომზადება_გარემო(void) {
    if(듣는곳>=0)return 0;
    if(!문맥){
        assh_status_t შეცდომა=assh_context_create(&문맥,ASSH_SERVER,მომზადება_მეხსიერება,0,&난수기,0);
        if(შეცდომა)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *მეთოდი_რეჟიმი[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        შეცდომა=assh_algo_register(문맥,ASSH_SAFETY_WEAK,მეთოდი_რეჟიმი);
        if(!შეცდომა)შეცდომა=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=მობილური_კლავიში;
        if(!შეცდომა)შეცდომა=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(მობილური_კლავიში));
        if(შეცდომა){진단("SSH init error ",შეცდომა);assh_context_release(문맥);문맥=0;return -5;}
    }
    int პორტი_მნიშვნელობა=통신끝점만들기(1);if(პორტი_მნიშვნელობა<0)return პორტი_მნიშვნელობა;통신주소재사용(პორტი_მნიშვნელობა);
    int გაზომვა=망주소묶기(პორტი_მნიშვნელობა,0,22);if(!გაზომვა)გაზომვა=연결기다리기(პორტი_მნიშვნელობა);
    if(გაზომვა<0){დახურვა_ქსელი(პორტი_მნიშვნელობა);return გაზომვა;}듣는곳=პორტი_მნიშვნელობა;return 0;
}
uintptr_t დაფა_ჩრდილური_მართვა(uintptr_t 종류,uintptr_t ქმედება) {
    if(종류==1)return(uint32_t)მართვა_დისტანციური_ჩვენება(ქმედება);
    if(ქმედება==0){დახურვა_კავშირი();if(듣는곳>=0)დახურვა_ქსელი(듣는곳);듣는곳=-1;return 0;}
    if(ქმედება==1){ჩატვირთვა_შეცდომა=მომზადება_გარემო();return(uint32_t)ჩატვირთვა_შეცდომა;}
    return(uint32_t)(듣는곳>=0?1:ჩატვირთვა_შეცდომა);
}
void მომზადება_დისტანციური(void){ჩატვირთვა_შეცდომა=მომზადება_გარემო();მართვა_დისტანციური_ჩვენება(1);}
static int 같은말(const struct assh_cbuffer_s *მონაცემები,const char *სიტყვები_ტექსტი) {
    size_t სიგრძე_მნიშვნელობა=strlen(სიტყვები_ტექსტი);return მონაცემები->size==სიგრძე_მნიშვნელობა&&!memcmp(მონაცემები->data,სიტყვები_ტექსტი,სიგრძე_მნიშვნელობა);
}
static int 터미널요청(const struct assh_cbuffer_s *მონაცემები) {
    if(მონაცემები->size<24)return 0;
    const unsigned char *მონაცემები_პოზიცია=მონაცემები->data;unsigned სიგრძე_მნიშვნელობა=assh_load_u32(მონაცემები_პოზიცია);
    if(სიგრძე_მნიშვნელობა>128||მონაცემები->size<სიგრძე_მნიშვნელობა+24)return 0;
    unsigned რეჟიმი_მნიშვნელობა=assh_load_u32(მონაცემები_პოზიცია+4+სიგრძე_მნიშვნელობა+16);
    return რეჟიმი_მნიშვნელობა<=2048&&მონაცემები->size==სიგრძე_მნიშვნელობა+24+რეჟიმი_მნიშვნელობა;
}
static void 요청처리(struct assh_event_request_s *მოვლენა) {
    if(!인증됨||მოვლენა->ch!=არხი_შენატანი||!არხი_შენატანი)return;
    if(같은말(&მოვლენა->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&მოვლენა->rq_data))მოვლენა->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&მოვლენა->type,"window-change")) {
        if(셸시작됨&&მოვლენა->rq_data.size==16)მოვლენა->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!გარემო_ლოდინი)return;
    const unsigned char *ბრძანება=0;unsigned სიგრძე_მნიშვნელობა=0;
    if(같은말(&მოვლენა->type,"exec")) {
        if(მოვლენა->rq_data.size<4)return;
        სიგრძე_მნიშვნელობა=assh_load_u32(მოვლენა->rq_data.data);
        if(!სიგრძე_მნიშვნელობა||სიგრძე_მნიშვნელობა>2048||მოვლენა->rq_data.size!=სიგრძე_მნიშვნელობა+4)return;
        ბრძანება=მოვლენა->rq_data.data+4;
        for(unsigned 순번=0;순번<სიგრძე_მნიშვნელობა;순번++)if(!ბრძანება[순번])return;
        ბრძანება_აკრეფა=1;
    }else if(!같은말(&მოვლენა->type,"shell")||მოვლენა->rq_data.size)return;
    if(sizeof(입력줄)-입력수<სიგრძე_მნიშვნელობა+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(სიგრძე_მნიშვნელობა)원격입력넣기(ბრძანება,სიგრძე_მნიშვნელობა);원격입력넣기(&끝,1);
    셸시작됨=1;მოვლენა->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!ბრძანება_აკრეფა){const char *წასაკითხი_ფაილი_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*წასაკითხი_ფაილი_eb81d7d9)원격출력(*წასაკითხი_ფაილი_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(კვანძი_მნიშვნელობა_6a3b6fa7<0){if(지금<재접속시각)return;კვანძი_მნიშვნელობა_6a3b6fa7=망연결받기(듣는곳);if(კვანძი_მნიშვნელობა_6a3b6fa7<0)return;
        კავშირი_დრო=지금;assh_status_t შეცდომა=assh_session_create(문맥,&კავშირი_e05f319b);
        if(შეცდომა){კავშირი_e05f319b=0;진단("SSH session error ",შეცდომა);დახურვა_კავშირი();return;}}
    if((!인증됨&&지금-კავშირი_დრო>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){დახურვა_კავშირი();return;}
    if(არხი_შენატანი&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t შეცდომა=assh_channel_data(არხი_შენატანი,출력줄+출력앞,&수);
            if(!შეცდომა){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(შეცდომა!=ASSH_NO_DATA){დახურვა_კავშირი();return;}
        }
        if(დასასრული_სტატუსი>=0&&!출력수){unsigned char სტატუსი_მნიშვნელობა[4];assh_store_u32(სტატუსი_მნიშვნელობა,(uint32_t)დასასრული_სტატუსი);
            if(assh_request(კავშირი_e05f319b,არხი_შენატანი,"exit-status",11,სტატუსი_მნიშვნელობა,4,0)||assh_channel_eof(არხი_შენატანი)||assh_channel_close(არხი_შენატანი)) {დახურვა_კავშირი();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s მოვლენა;
        if(!assh_event_get(კავშირი_e05f319b,&მოვლენა,지금/1000)){დახურვა_კავშირი();return;}
        assh_status_t შეცდომა=ASSH_OK;int 쉬기=0,끊기=0;
        switch(მოვლენა.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(კვანძი_მნიშვნელობა_6a3b6fa7,მოვლენა.transport.read.buf.data,მოვლენა.transport.read.buf.size);
            if(수>0)მოვლენა.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(კვანძი_მნიშვნელობა_6a3b6fa7,მოვლენა.transport.write.buf.data,მოვლენა.transport.write.buf.size);
            if(수>0)მოვლენა.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            მოვლენა.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(მოვლენა.userauth_server.methods.retries>3)მოვლენა.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *მონაცემები=&მოვლენა.userauth_server.password;
            if(같은말(&მონაცემები->username,"user")&&მონაცემები->password.size<=256&&!მონაცემები->new_password.size) {
                unsigned char რეზიუმე_მნიშვნელობა[32];დისტანციური_რეზიუმე(მონაცემები->password.data,მონაცემები->password.size,რეზიუმე_მნიშვნელობა);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=რეზიუმე_მნიშვნელობა[순번]^გარემო_პაროლი_რეზიუმე[순번];memset(რეზიუმე_მნიშვნელობა,0,32);
                if(!차이)მონაცემები->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *მონაცემები=&მოვლენა.connection.channel_open;
            if(인증됨&&!არხი_შენატანი&&გარემო_ლოდინი&&같은말(&მონაცემები->type,"session")&&!მონაცემები->rq_data.size) {
                მონაცემები->reply=ASSH_CONNECTION_REPLY_SUCCESS;მონაცემები->pkt_size=4096;
                მონაცემები->win_size=-1;არხი_შენატანი=მონაცემები->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&მოვლენა.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *მონაცემები=&მოვლენა.connection.channel_data;
            if(!셸시작됨||მონაცემები->ch!=არხი_შენატანი||მონაცემები->ext){끊기=1;break;}
            unsigned 수=მონაცემები->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(მონაცემები->data.data[순번]==4){დასასრული_სტატუსი=0;수=순번;მონაცემები->transferred=მონაცემები->data.size;break;}
            원격입력넣기(მონაცემები->data.data,수);if(!მონაცემები->transferred)მონაცემები->transferred=수;
            if(!수&&დასასრული_სტატუსი<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: არხი_შენატანი=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",მოვლენა.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(კავშირი_e05f319b,&მოვლენა,შეცდომა);
        if(끊기){დახურვა_კავშირი();return;}if(쉬기)return;
    }
}
