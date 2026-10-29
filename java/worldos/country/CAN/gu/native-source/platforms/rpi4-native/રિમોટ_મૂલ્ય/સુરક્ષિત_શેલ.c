/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "રિમોટ_મૂલ્ય.h"
#include "암호기반.h"
#include "પ્રોફાઇલ.h"
#include "../નેટવર્ક_સ્ટેક/નેટવર્ક_સ્ટેક.h"
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
static struct assh_context_s *સંદર્ભ_મૂલ્ય;
static struct assh_session_s *કનેક્શન_e05f319b;
static struct assh_channel_s *ચૅનલ_પ્રવેશ;
static int 듣는곳=-1,પીઅર_મૂલ્ય=-1,인증됨,셸시작됨,આદેશ_લખો,અંત_કરો_સ્થિતિ_2bce2943=-1,닫을예정,બૂટ_ભૂલ,શેલ_પ્રતીક્ષા_કરવી;
static uintptr_t કનેક્શન_સમય,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *શબ્દ_પાઠ,unsigned મૂલ્ય) {
    while(*શબ્દ_પાઠ)보드글자쓰기(*શબ્દ_પાઠ++);
    char અંક_મૂલ્ય[12];unsigned 수=0;do{અંક_મૂલ્ય[수++]='0'+મૂલ્ય%10;મૂલ્ય/=10;}while(મૂલ્ય);
    while(수)보드글자쓰기(અંક_મૂલ્ય[--수]);보드글자쓰기(10);
}
static assh_status_t તૈયાર_કરો_મેમરી(void *ડેટા,void **સરનામું,size_t માપ,enum assh_alloc_type_e 종류) {
    (void)ડેટા;(void)종류;
    if(!માપ){રિલીઝ_રિમોટ(*સરનામું);*સરનામું=0;return ASSH_OK;}
    void *새주소=원격재할당(*સરનામું,માપ);
    if(!새주소)return ASSH_ERR_MEM;*સરનામું=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ડેટા,const struct assh_buffer_s *સીડ_મૂલ્ય) {
    (void)ડેટા;(void)સીડ_મૂલ્ય;unsigned char 시험[32];int પરિમાણ=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return પરિમાણ?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ડેટા,uint8_t *પરિમાણ,size_t લંબાઈ_મૂલ્ય,uint_fast8_t 종류) {
    (void)ડેટા;(void)종류;if(લંબાઈ_મૂલ્ય>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(પરિમાણ,લંબાઈ_મૂલ્ય)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ડેટા){(void)ડેટા;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void બંધ_કરો_કનેક્શન(void) {
    인증됨=셸시작됨=0;ચૅનલ_પ્રવેશ=0;
    if(કનેક્શન_e05f319b)assh_session_release(કનેક્શન_e05f319b);કનેક્શન_e05f319b=0;
    if(પીઅર_મૂલ્ય>=0)બંધ_કરો_નેટવર્ક(પીઅર_મૂલ્ય);પીઅર_મૂલ્ય=-1;આદેશ_લખો=0;અંત_કરો_સ્થિતિ_2bce2943=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ડેટા,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=ડેટા[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int વર્ણ_મૂલ્ય=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return વર્ણ_મૂલ્ય;
}
void 원격출력(unsigned char વર્ણ_મૂલ્ય) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=વર્ણ_મૂલ્ય==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=વર્ણ_મૂલ્ય;이전출력=વર્ણ_મૂલ્ય;
}
uintptr_t બોર્ડ_અંત_કરો_રિમોટ_આદેશ(uintptr_t સ્થિતિ_મૂલ્ય_e10195a1){if(셸시작됨&&આદેશ_લખો)અંત_કરો_સ્થિતિ_2bce2943=(int)સ્થિતિ_મૂલ્ય_e10195a1;return 0;}
uintptr_t બોર્ડ_રિમોટ_પ્રતીક્ષા(uintptr_t સ્થિતિ_મૂલ્ય_e10195a1){શેલ_પ્રતીક્ષા_કરવી=સ્થિતિ_મૂલ્ય_e10195a1!=0;return 0;}
static int તૈયાર_કરો_શેલ(void) {
    if(듣는곳>=0)return 0;
    if(!સંદર્ભ_મૂલ્ય){
        assh_status_t ભૂલ=assh_context_create(&સંદર્ભ_મૂલ્ય,ASSH_SERVER,તૈયાર_કરો_મેમરી,0,&난수기,0);
        if(ભૂલ)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *પદ્ધતિ_મોડ[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ભૂલ=assh_algo_register(સંદર્ભ_મૂલ્ય,ASSH_SAFETY_WEAK,પદ્ધતિ_મોડ);
        if(!ભૂલ)ભૂલ=assh_service_register_va(સંદર્ભ_મૂલ્ય,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=ડિવાઇસ_કી;
        if(!ભૂલ)ભૂલ=assh_key_load(સંદર્ભ_મૂલ્ય,assh_context_keys(સંદર્ભ_મૂલ્ય),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(ડિવાઇસ_કી));
        if(ભૂલ){진단("SSH init error ",ભૂલ);assh_context_release(સંદર્ભ_મૂલ્ય);સંદર્ભ_મૂલ્ય=0;return -5;}
    }
    int પૉર્ટ_મૂલ્ય=통신끝점만들기(1);if(પૉર્ટ_મૂલ્ય<0)return પૉર્ટ_મૂલ્ય;통신주소재사용(પૉર્ટ_મૂલ્ય);
    int પરિમાણ=망주소묶기(પૉર્ટ_મૂલ્ય,0,22);if(!પરિમાણ)પરિમાણ=연결기다리기(પૉર્ટ_મૂલ્ય);
    if(પરિમાણ<0){બંધ_કરો_નેટવર્ક(પૉર્ટ_મૂલ્ય);return પરિમાણ;}듣는곳=પૉર્ટ_મૂલ્ય;return 0;
}
uintptr_t બોર્ડ_છાયાંકિત(uintptr_t 종류,uintptr_t ક્રિયા) {
    if(종류==1)return(uint32_t)નિયંત્રણ_રિમોટ_પ્રદર્શન(ક્રિયા);
    if(ક્રિયા==0){બંધ_કરો_કનેક્શન();if(듣는곳>=0)બંધ_કરો_નેટવર્ક(듣는곳);듣는곳=-1;return 0;}
    if(ક્રિયા==1){બૂટ_ભૂલ=તૈયાર_કરો_શેલ();return(uint32_t)બૂટ_ભૂલ;}
    return(uint32_t)(듣는곳>=0?1:બૂટ_ભૂલ);
}
void તૈયાર_કરો_રિમોટ(void){બૂટ_ભૂલ=તૈયાર_કરો_શેલ();નિયંત્રણ_રિમોટ_પ્રદર્શન(1);}
static int 같은말(const struct assh_cbuffer_s *ડેટા,const char *શબ્દ_પાઠ) {
    size_t લંબાઈ_મૂલ્ય=strlen(શબ્દ_પાઠ);return ડેટા->size==લંબાઈ_મૂલ્ય&&!memcmp(ડેટા->data,શબ્દ_પાઠ,લંબાઈ_મૂલ્ય);
}
static int 터미널요청(const struct assh_cbuffer_s *ડેટા) {
    if(ડેટા->size<24)return 0;
    const unsigned char *ડેટા_સ્થિતિ=ડેટા->data;unsigned લંબાઈ_મૂલ્ય=assh_load_u32(ડેટા_સ્થિતિ);
    if(લંબાઈ_મૂલ્ય>128||ડેટા->size<લંબાઈ_મૂલ્ય+24)return 0;
    unsigned મોડ_મૂલ્ય=assh_load_u32(ડેટા_સ્થિતિ+4+લંબાઈ_મૂલ્ય+16);
    return મોડ_મૂલ્ય<=2048&&ડેટા->size==લંબાઈ_મૂલ્ય+24+મોડ_મૂલ્ય;
}
static void 요청처리(struct assh_event_request_s *ઇવેંટ) {
    if(!인증됨||ઇવેંટ->ch!=ચૅનલ_પ્રવેશ||!ચૅનલ_પ્રવેશ)return;
    if(같은말(&ઇવેંટ->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&ઇવેંટ->rq_data))ઇવેંટ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ઇવેંટ->type,"window-change")) {
        if(셸시작됨&&ઇવેંટ->rq_data.size==16)ઇવેંટ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!શેલ_પ્રતીક્ષા_કરવી)return;
    const unsigned char *આદેશ=0;unsigned લંબાઈ_મૂલ્ય=0;
    if(같은말(&ઇવેંટ->type,"exec")) {
        if(ઇવેંટ->rq_data.size<4)return;
        લંબાઈ_મૂલ્ય=assh_load_u32(ઇવેંટ->rq_data.data);
        if(!લંબાઈ_મૂલ્ય||લંબાઈ_મૂલ્ય>2048||ઇવેંટ->rq_data.size!=લંબાઈ_મૂલ્ય+4)return;
        આદેશ=ઇવેંટ->rq_data.data+4;
        for(unsigned 순번=0;순번<લંબાઈ_મૂલ્ય;순번++)if(!આદેશ[순번])return;
        આદેશ_લખો=1;
    }else if(!같은말(&ઇવેંટ->type,"shell")||ઇવેંટ->rq_data.size)return;
    if(sizeof(입력줄)-입력수<લંબાઈ_મૂલ્ય+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(લંબાઈ_મૂલ્ય)원격입력넣기(આદેશ,લંબાઈ_મૂલ્ય);원격입력넣기(&끝,1);
    셸시작됨=1;ઇવેંટ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!આદેશ_લખો){const char *રીડમી_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*રીડમી_eb81d7d9)원격출력(*રીડમી_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(પીઅર_મૂલ્ય<0){if(지금<재접속시각)return;પીઅર_મૂલ્ય=망연결받기(듣는곳);if(પીઅર_મૂલ્ય<0)return;
        કનેક્શન_સમય=지금;assh_status_t ભૂલ=assh_session_create(સંદર્ભ_મૂલ્ય,&કનેક્શન_e05f319b);
        if(ભૂલ){કનેક્શન_e05f319b=0;진단("SSH session error ",ભૂલ);બંધ_કરો_કનેક્શન();return;}}
    if((!인증됨&&지금-કનેક્શન_સમય>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){બંધ_કરો_કનેક્શન();return;}
    if(ચૅનલ_પ્રવેશ&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ભૂલ=assh_channel_data(ચૅનલ_પ્રવેશ,출력줄+출력앞,&수);
            if(!ભૂલ){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ભૂલ!=ASSH_NO_DATA){બંધ_કરો_કનેક્શન();return;}
        }
        if(અંત_કરો_સ્થિતિ_2bce2943>=0&&!출력수){unsigned char સ્થિતિ_મૂલ્ય_e10195a1[4];assh_store_u32(સ્થિતિ_મૂલ્ય_e10195a1,(uint32_t)અંત_કરો_સ્થિતિ_2bce2943);
            if(assh_request(કનેક્શન_e05f319b,ચૅનલ_પ્રવેશ,"exit-status",11,સ્થિતિ_મૂલ્ય_e10195a1,4,0)||assh_channel_eof(ચૅનલ_પ્રવેશ)||assh_channel_close(ચૅનલ_પ્રવેશ)) {બંધ_કરો_કનેક્શન();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s ઇવેંટ;
        if(!assh_event_get(કનેક્શન_e05f319b,&ઇવેંટ,지금/1000)){બંધ_કરો_કનેક્શન();return;}
        assh_status_t ભૂલ=ASSH_OK;int 쉬기=0,끊기=0;
        switch(ઇવેંટ.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(પીઅર_મૂલ્ય,ઇવેંટ.transport.read.buf.data,ઇવેંટ.transport.read.buf.size);
            if(수>0)ઇવેંટ.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(પીઅર_મૂલ્ય,ઇવેંટ.transport.write.buf.data,ઇવેંટ.transport.write.buf.size);
            if(수>0)ઇવેંટ.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ઇવેંટ.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ઇવેંટ.userauth_server.methods.retries>3)ઇવેંટ.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ડેટા=&ઇવેંટ.userauth_server.password;
            if(같은말(&ડેટા->username,"user")&&ડેટા->password.size<=256&&!ડેટા->new_password.size) {
                unsigned char 요약[32];원격요약(ડેટા->password.data,ડેટા->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)ડેટા->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ડેટા=&ઇવેંટ.connection.channel_open;
            if(인증됨&&!ચૅનલ_પ્રવેશ&&શેલ_પ્રતીક્ષા_કરવી&&같은말(&ડેટા->type,"session")&&!ડેટા->rq_data.size) {
                ડેટા->reply=ASSH_CONNECTION_REPLY_SUCCESS;ડેટા->pkt_size=4096;
                ડેટા->win_size=-1;ચૅનલ_પ્રવેશ=ડેટા->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&ઇવેંટ.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ડેટા=&ઇવેંટ.connection.channel_data;
            if(!셸시작됨||ડેટા->ch!=ચૅનલ_પ્રવેશ||ડેટા->ext){끊기=1;break;}
            unsigned 수=ડેટા->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(ડેટા->data.data[순번]==4){અંત_કરો_સ્થિતિ_2bce2943=0;수=순번;ડેટા->transferred=ડેટા->data.size;break;}
            원격입력넣기(ડેટા->data.data,수);if(!ડેટા->transferred)ડેટા->transferred=수;
            if(!수&&અંત_કરો_સ્થિતિ_2bce2943<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: ચૅનલ_પ્રવેશ=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ઇવેંટ.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(કનેક્શન_e05f319b,&ઇવેંટ,ભૂલ);
        if(끊기){બંધ_કરો_કનેક્શન();return;}if(쉬기)return;
    }
}
