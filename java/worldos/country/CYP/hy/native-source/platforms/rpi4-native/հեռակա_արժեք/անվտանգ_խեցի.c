/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "հեռակա_արժեք.h"
#include "암호기반.h"
#include "Հատկագիր.h"
#include "../Ցանց_Շեղջ/Ցանց_Շեղջ.h"
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
static struct assh_context_s *Համատեքստ_արժեք;
static struct assh_session_s *կապ_e05f319b;
static struct assh_channel_s *կապուղի_մուտքագրում;
static int 듣는곳=-1,հավասարազոր_սարք_արժեք=-1,인증됨,셸시작됨,հրաման_մուտքագրել,վերջացնել_վիճակ=-1,닫을예정,մեկնարկում_սխալ,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Բառ_Գրվածք,unsigned արժեք) {
    while(*Բառ_Գրվածք)보드글자쓰기(*Բառ_Գրվածք++);
    char թվանշան_արժեք[12];unsigned 수=0;do{թվանշան_արժեք[수++]='0'+արժեք%10;արժեք/=10;}while(արժեք);
    while(수)보드글자쓰기(թվանշան_արժեք[--수]);보드글자쓰기(10);
}
static assh_status_t Պատրաստել_Հիշողություն(void *տվյալ,void **հասցե,size_t Չափս,enum assh_alloc_type_e 종류) {
    (void)տվյալ;(void)종류;
    if(!Չափս){արձակել_հեռակա(*հասցե);*հասցե=0;return ASSH_OK;}
    void *새주소=원격재할당(*հասցե,Չափս);
    if(!새주소)return ASSH_ERR_MEM;*հասցե=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *տվյալ,const struct assh_buffer_s *նախնական_իմաստ_արժեք) {
    (void)տվյալ;(void)նախնական_իմաստ_արժեք;unsigned char 시험[32];int չափ=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return չափ?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *տվյալ,uint8_t *չափ,size_t տեւողություն_արժեք,uint_fast8_t 종류) {
    (void)տվյալ;(void)종류;if(տեւողություն_արժեք>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(չափ,տեւողություն_արժեք)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *տվյալ){(void)տվյալ;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void փակել_կապ(void) {
    인증됨=셸시작됨=0;կապուղի_մուտքագրում=0;
    if(կապ_e05f319b)assh_session_release(կապ_e05f319b);կապ_e05f319b=0;
    if(հավասարազոր_սարք_արժեք>=0)փակել_Ցանց(հավասարազոր_սարք_արժեք);հավասարազոր_սարք_արժեք=-1;հրաման_մուտքագրել=0;վերջացնել_վիճակ=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *տվյալ,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=տվյալ[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int գրանշան_արժեք=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return գրանշան_արժեք;
}
void 원격출력(unsigned char գրանշան_արժեք) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=գրանշան_արժեք==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=գրանշան_արժեք;이전출력=գրանշան_արժեք;
}
uintptr_t տախտակ_վերջացնել_հեռակա_հրաման(uintptr_t վիճակ_արժեք){if(셸시작됨&&հրաման_մուտքագրել)վերջացնել_վիճակ=(int)վիճակ_արժեք;return 0;}
uintptr_t 보드원격대기(uintptr_t վիճակ_արժեք){셸대기중=վիճակ_արժեք!=0;return 0;}
static int Պատրաստել_խեցի(void) {
    if(듣는곳>=0)return 0;
    if(!Համատեքստ_արժեք){
        assh_status_t Սխալ=assh_context_create(&Համատեքստ_արժեք,ASSH_SERVER,Պատրաստել_Հիշողություն,0,&난수기,0);
        if(Սխալ)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *եղանակ_կերպ[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Սխալ=assh_algo_register(Համատեքստ_արժեք,ASSH_SAFETY_WEAK,եղանակ_կերպ);
        if(!Սխալ)Սխալ=assh_service_register_va(Համատեքստ_արժեք,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=սարք_ստեղն;
        if(!Սխալ)Սխալ=assh_key_load(Համատեքստ_արժեք,assh_context_keys(Համատեքստ_արժեք),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(սարք_ստեղն));
        if(Սխալ){진단("SSH init error ",Սխալ);assh_context_release(Համատեքստ_արժեք);Համատեքստ_արժեք=0;return -5;}
    }
    int միացք_արժեք=통신끝점만들기(1);if(միացք_արժեք<0)return միացք_արժեք;통신주소재사용(միացք_արժեք);
    int չափ=망주소묶기(միացք_արժեք,0,22);if(!չափ)չափ=연결기다리기(միացք_արժեք);
    if(չափ<0){փակել_Ցանց(միացք_արժեք);return չափ;}듣는곳=միացք_արժեք;return 0;
}
uintptr_t տախտակ_հետեւում(uintptr_t 종류,uintptr_t Գործողություն) {
    if(종류==1)return(uint32_t)հսկում_հեռակա_ցուցադրել(Գործողություն);
    if(Գործողություն==0){փակել_կապ();if(듣는곳>=0)փակել_Ցանց(듣는곳);듣는곳=-1;return 0;}
    if(Գործողություն==1){մեկնարկում_սխալ=Պատրաստել_խեցի();return(uint32_t)մեկնարկում_սխալ;}
    return(uint32_t)(듣는곳>=0?1:մեկնարկում_սխալ);
}
void Պատրաստել_հեռակա(void){մեկնարկում_սխալ=Պատրաստել_խեցի();հսկում_հեռակա_ցուցադրել(1);}
static int 같은말(const struct assh_cbuffer_s *տվյալ,const char *Բառ_Գրվածք) {
    size_t տեւողություն_արժեք=strlen(Բառ_Գրվածք);return տվյալ->size==տեւողություն_արժեք&&!memcmp(տվյալ->data,Բառ_Գրվածք,տեւողություն_արժեք);
}
static int 터미널요청(const struct assh_cbuffer_s *տվյալ) {
    if(տվյալ->size<24)return 0;
    const unsigned char *տվյալ_դիրք=տվյալ->data;unsigned տեւողություն_արժեք=assh_load_u32(տվյալ_դիրք);
    if(տեւողություն_արժեք>128||տվյալ->size<տեւողություն_արժեք+24)return 0;
    unsigned կերպ_արժեք=assh_load_u32(տվյալ_դիրք+4+տեւողություն_արժեք+16);
    return կերպ_արժեք<=2048&&տվյալ->size==տեւողություն_արժեք+24+կերպ_արժեք;
}
static void 요청처리(struct assh_event_request_s *միջոցառում) {
    if(!인증됨||միջոցառում->ch!=կապուղի_մուտքագրում||!կապուղի_մուտքագրում)return;
    if(같은말(&միջոցառում->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&միջոցառում->rq_data))միջոցառում->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&միջոցառում->type,"window-change")) {
        if(셸시작됨&&միջոցառում->rq_data.size==16)միջոցառում->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *Հրահանգ=0;unsigned տեւողություն_արժեք=0;
    if(같은말(&միջոցառում->type,"exec")) {
        if(միջոցառում->rq_data.size<4)return;
        տեւողություն_արժեք=assh_load_u32(միջոցառում->rq_data.data);
        if(!տեւողություն_արժեք||տեւողություն_արժեք>2048||միջոցառում->rq_data.size!=տեւողություն_արժեք+4)return;
        Հրահանգ=միջոցառում->rq_data.data+4;
        for(unsigned 순번=0;순번<տեւողություն_արժեք;순번++)if(!Հրահանգ[순번])return;
        հրաման_մուտքագրել=1;
    }else if(!같은말(&միջոցառում->type,"shell")||միջոցառում->rq_data.size)return;
    if(sizeof(입력줄)-입력수<տեւողություն_արժեք+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(տեւողություն_արժեք)원격입력넣기(Հրահանգ,տեւողություն_արժեք);원격입력넣기(&끝,1);
    셸시작됨=1;միջոցառում->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!հրաման_մուտքագրել){const char *ԿԱՐԴԱ_ԻՆՁ_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*ԿԱՐԴԱ_ԻՆՁ_eb81d7d9)원격출력(*ԿԱՐԴԱ_ԻՆՁ_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(հավասարազոր_սարք_արժեք<0){if(지금<재접속시각)return;հավասարազոր_սարք_արժեք=망연결받기(듣는곳);if(հավասարազոր_սարք_արժեք<0)return;
        접속시각=지금;assh_status_t Սխալ=assh_session_create(Համատեքստ_արժեք,&կապ_e05f319b);
        if(Սխալ){կապ_e05f319b=0;진단("SSH session error ",Սխալ);փակել_կապ();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){փակել_կապ();return;}
    if(կապուղի_մուտքագրում&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Սխալ=assh_channel_data(կապուղի_մուտքագրում,출력줄+출력앞,&수);
            if(!Սխալ){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Սխալ!=ASSH_NO_DATA){փակել_կապ();return;}
        }
        if(վերջացնել_վիճակ>=0&&!출력수){unsigned char վիճակ_արժեք[4];assh_store_u32(վիճակ_արժեք,(uint32_t)վերջացնել_վիճակ);
            if(assh_request(կապ_e05f319b,կապուղի_մուտքագրում,"exit-status",11,վիճակ_արժեք,4,0)||assh_channel_eof(կապուղի_մուտքագրում)||assh_channel_close(կապուղի_մուտքագրում)) {փակել_կապ();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s միջոցառում;
        if(!assh_event_get(կապ_e05f319b,&միջոցառում,지금/1000)){փակել_կապ();return;}
        assh_status_t Սխալ=ASSH_OK;int 쉬기=0,끊기=0;
        switch(միջոցառում.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(հավասարազոր_սարք_արժեք,միջոցառում.transport.read.buf.data,միջոցառում.transport.read.buf.size);
            if(수>0)միջոցառում.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(հավասարազոր_սարք_արժեք,միջոցառում.transport.write.buf.data,միջոցառում.transport.write.buf.size);
            if(수>0)միջոցառում.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            միջոցառում.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(միջոցառում.userauth_server.methods.retries>3)միջոցառում.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *տվյալ=&միջոցառում.userauth_server.password;
            if(같은말(&տվյալ->username,"user")&&տվյալ->password.size<=256&&!տվյալ->new_password.size) {
                unsigned char ամփոփագիր_արժեք[32];հեռակա_ամփոփագիր(տվյալ->password.data,տվյալ->password.size,ամփոփագիր_արժեք);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=ամփոփագիր_արժեք[순번]^խեցի_գաղտնաբառ_ամփոփագիր[순번];memset(ամփոփագիր_արժեք,0,32);
                if(!차이)տվյալ->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *տվյալ=&միջոցառում.connection.channel_open;
            if(인증됨&&!կապուղի_մուտքագրում&&셸대기중&&같은말(&տվյալ->type,"session")&&!տվյալ->rq_data.size) {
                տվյալ->reply=ASSH_CONNECTION_REPLY_SUCCESS;տվյալ->pkt_size=4096;
                տվյալ->win_size=-1;կապուղի_մուտքագրում=տվյալ->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&միջոցառում.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *տվյալ=&միջոցառում.connection.channel_data;
            if(!셸시작됨||տվյալ->ch!=կապուղի_մուտքագրում||տվյալ->ext){끊기=1;break;}
            unsigned 수=տվյալ->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(տվյալ->data.data[순번]==4){վերջացնել_վիճակ=0;수=순번;տվյալ->transferred=տվյալ->data.size;break;}
            원격입력넣기(տվյալ->data.data,수);if(!տվյալ->transferred)տվյալ->transferred=수;
            if(!수&&վերջացնել_վիճակ<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: կապուղի_մուտքագրում=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",միջոցառում.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(կապ_e05f319b,&միջոցառում,Սխալ);
        if(끊기){փակել_կապ();return;}if(쉬기)return;
    }
}
