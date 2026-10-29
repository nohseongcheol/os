/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "ਰਿਮੋਟ_ਕੀਮਤ.h"
#include "암호기반.h"
#include "ਪ੍ਰੋਫਾਈਲ.h"
#include "../ਨੈਟਵਰਕ_ਸਟੈਕ/ਨੈਟਵਰਕ_ਸਟੈਕ.h"
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
static struct assh_context_s *ਸੰਦਰਭ_ਕੀਮਤ;
static struct assh_session_s *ਸਬੰਧ_e05f319b;
static struct assh_channel_s *ਚੈਨਲ_ਦਾਖਲਾ;
static int 듣는곳=-1,ਪਿਅਰ_ਕੀਮਤ=-1,인증됨,셸시작됨,ਆਦੇਸ਼_ਟਾਈਪ_ਕਰੋ,ਅੰਤ_ਸਥਿਤੀ=-1,닫을예정,ਬੂਟ_ਗਲਤ,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *ਸ਼ਬਦ_ਪਾਠ,unsigned ਕੀਮਤ) {
    while(*ਸ਼ਬਦ_ਪਾਠ)보드글자쓰기(*ਸ਼ਬਦ_ਪਾਠ++);
    char ਅੰਕ_ਕੀਮਤ[12];unsigned 수=0;do{ਅੰਕ_ਕੀਮਤ[수++]='0'+ਕੀਮਤ%10;ਕੀਮਤ/=10;}while(ਕੀਮਤ);
    while(수)보드글자쓰기(ਅੰਕ_ਕੀਮਤ[--수]);보드글자쓰기(10);
}
static assh_status_t ਤਿਆਰ_ਕਰੋ_ਮੈਮਰੀ(void *ਸਮੱਗਰੀ,void **ਪਤਾ,size_t ਆਕਾਰ,enum assh_alloc_type_e 종류) {
    (void)ਸਮੱਗਰੀ;(void)종류;
    if(!ਆਕਾਰ){ਰਿਲੀਜ_ਰਿਮੋਟ(*ਪਤਾ);*ਪਤਾ=0;return ASSH_OK;}
    void *새주소=원격재할당(*ਪਤਾ,ਆਕਾਰ);
    if(!새주소)return ASSH_ERR_MEM;*ਪਤਾ=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ਸਮੱਗਰੀ,const struct assh_buffer_s *ਸੀਡ_ਕੀਮਤ) {
    (void)ਸਮੱਗਰੀ;(void)ਸੀਡ_ਕੀਮਤ;unsigned char 시험[32];int ਮਾਪ=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return ਮਾਪ?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ਸਮੱਗਰੀ,uint8_t *ਮਾਪ,size_t ਲੰਬਾਈ_ਕੀਮਤ,uint_fast8_t 종류) {
    (void)ਸਮੱਗਰੀ;(void)종류;if(ਲੰਬਾਈ_ਕੀਮਤ>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(ਮਾਪ,ਲੰਬਾਈ_ਕੀਮਤ)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ਸਮੱਗਰੀ){(void)ਸਮੱਗਰੀ;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void ਬੰਦ_ਕਰੋ_ਸਬੰਧ(void) {
    인증됨=셸시작됨=0;ਚੈਨਲ_ਦਾਖਲਾ=0;
    if(ਸਬੰਧ_e05f319b)assh_session_release(ਸਬੰਧ_e05f319b);ਸਬੰਧ_e05f319b=0;
    if(ਪਿਅਰ_ਕੀਮਤ>=0)ਬੰਦ_ਕਰੋ_ਨੈਟਵਰਕ(ਪਿਅਰ_ਕੀਮਤ);ਪਿਅਰ_ਕੀਮਤ=-1;ਆਦੇਸ਼_ਟਾਈਪ_ਕਰੋ=0;ਅੰਤ_ਸਥਿਤੀ=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ਸਮੱਗਰੀ,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=ਸਮੱਗਰੀ[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int ਵਰਣ_ਕੀਮਤ=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return ਵਰਣ_ਕੀਮਤ;
}
void 원격출력(unsigned char ਵਰਣ_ਕੀਮਤ) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=ਵਰਣ_ਕੀਮਤ==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=ਵਰਣ_ਕੀਮਤ;이전출력=ਵਰਣ_ਕੀਮਤ;
}
uintptr_t ਬੋਰਡ_ਅੰਤ_ਰਿਮੋਟ_ਆਦੇਸ਼(uintptr_t ਸਥਿਤੀ_ਕੀਮਤ){if(셸시작됨&&ਆਦੇਸ਼_ਟਾਈਪ_ਕਰੋ)ਅੰਤ_ਸਥਿਤੀ=(int)ਸਥਿਤੀ_ਕੀਮਤ;return 0;}
uintptr_t 보드원격대기(uintptr_t ਸਥਿਤੀ_ਕੀਮਤ){셸대기중=ਸਥਿਤੀ_ਕੀਮਤ!=0;return 0;}
static int ਤਿਆਰ_ਕਰੋ_ਸ਼ੈਲ(void) {
    if(듣는곳>=0)return 0;
    if(!ਸੰਦਰਭ_ਕੀਮਤ){
        assh_status_t ਗਲਤੀ=assh_context_create(&ਸੰਦਰਭ_ਕੀਮਤ,ASSH_SERVER,ਤਿਆਰ_ਕਰੋ_ਮੈਮਰੀ,0,&난수기,0);
        if(ਗਲਤੀ)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *ਮੈਥਡ_ਮੋਡ[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ਗਲਤੀ=assh_algo_register(ਸੰਦਰਭ_ਕੀਮਤ,ASSH_SAFETY_WEAK,ਮੈਥਡ_ਮੋਡ);
        if(!ਗਲਤੀ)ਗਲਤੀ=assh_service_register_va(ਸੰਦਰਭ_ਕੀਮਤ,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=ਤਜਵੀਜ_ਕੀ;
        if(!ਗਲਤੀ)ਗਲਤੀ=assh_key_load(ਸੰਦਰਭ_ਕੀਮਤ,assh_context_keys(ਸੰਦਰਭ_ਕੀਮਤ),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(ਤਜਵੀਜ_ਕੀ));
        if(ਗਲਤੀ){진단("SSH init error ",ਗਲਤੀ);assh_context_release(ਸੰਦਰਭ_ਕੀਮਤ);ਸੰਦਰਭ_ਕੀਮਤ=0;return -5;}
    }
    int ਪੋਰਟ_ਕੀਮਤ=통신끝점만들기(1);if(ਪੋਰਟ_ਕੀਮਤ<0)return ਪੋਰਟ_ਕੀਮਤ;통신주소재사용(ਪੋਰਟ_ਕੀਮਤ);
    int ਮਾਪ=망주소묶기(ਪੋਰਟ_ਕੀਮਤ,0,22);if(!ਮਾਪ)ਮਾਪ=연결기다리기(ਪੋਰਟ_ਕੀਮਤ);
    if(ਮਾਪ<0){ਬੰਦ_ਕਰੋ_ਨੈਟਵਰਕ(ਪੋਰਟ_ਕੀਮਤ);return ਮਾਪ;}듣는곳=ਪੋਰਟ_ਕੀਮਤ;return 0;
}
uintptr_t ਬੋਰਡ_ਰਿਮੋਟ_ਨਿਯੰਤਰਣ(uintptr_t 종류,uintptr_t ਐਕਸ਼ਨ) {
    if(종류==1)return(uint32_t)ਨਿਯੰਤਰਣ_ਰਿਮੋਟ_ਪ੍ਰਦਰਸ਼ਨ(ਐਕਸ਼ਨ);
    if(ਐਕਸ਼ਨ==0){ਬੰਦ_ਕਰੋ_ਸਬੰਧ();if(듣는곳>=0)ਬੰਦ_ਕਰੋ_ਨੈਟਵਰਕ(듣는곳);듣는곳=-1;return 0;}
    if(ਐਕਸ਼ਨ==1){ਬੂਟ_ਗਲਤ=ਤਿਆਰ_ਕਰੋ_ਸ਼ੈਲ();return(uint32_t)ਬੂਟ_ਗਲਤ;}
    return(uint32_t)(듣는곳>=0?1:ਬੂਟ_ਗਲਤ);
}
void ਤਿਆਰ_ਕਰੋ_ਰਿਮੋਟ(void){ਬੂਟ_ਗਲਤ=ਤਿਆਰ_ਕਰੋ_ਸ਼ੈਲ();ਨਿਯੰਤਰਣ_ਰਿਮੋਟ_ਪ੍ਰਦਰਸ਼ਨ(1);}
static int 같은말(const struct assh_cbuffer_s *ਸਮੱਗਰੀ,const char *ਸ਼ਬਦ_ਪਾਠ) {
    size_t ਲੰਬਾਈ_ਕੀਮਤ=strlen(ਸ਼ਬਦ_ਪਾਠ);return ਸਮੱਗਰੀ->size==ਲੰਬਾਈ_ਕੀਮਤ&&!memcmp(ਸਮੱਗਰੀ->data,ਸ਼ਬਦ_ਪਾਠ,ਲੰਬਾਈ_ਕੀਮਤ);
}
static int 터미널요청(const struct assh_cbuffer_s *ਸਮੱਗਰੀ) {
    if(ਸਮੱਗਰੀ->size<24)return 0;
    const unsigned char *ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ=ਸਮੱਗਰੀ->data;unsigned ਲੰਬਾਈ_ਕੀਮਤ=assh_load_u32(ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ);
    if(ਲੰਬਾਈ_ਕੀਮਤ>128||ਸਮੱਗਰੀ->size<ਲੰਬਾਈ_ਕੀਮਤ+24)return 0;
    unsigned ਮੋਡ_ਕੀਮਤ=assh_load_u32(ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ+4+ਲੰਬਾਈ_ਕੀਮਤ+16);
    return ਮੋਡ_ਕੀਮਤ<=2048&&ਸਮੱਗਰੀ->size==ਲੰਬਾਈ_ਕੀਮਤ+24+ਮੋਡ_ਕੀਮਤ;
}
static void 요청처리(struct assh_event_request_s *ਇਵੈਂਟ) {
    if(!인증됨||ਇਵੈਂਟ->ch!=ਚੈਨਲ_ਦਾਖਲਾ||!ਚੈਨਲ_ਦਾਖਲਾ)return;
    if(같은말(&ਇਵੈਂਟ->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&ਇਵੈਂਟ->rq_data))ਇਵੈਂਟ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ਇਵੈਂਟ->type,"window-change")) {
        if(셸시작됨&&ਇਵੈਂਟ->rq_data.size==16)ਇਵੈਂਟ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *ਕਮਾਂਡ=0;unsigned ਲੰਬਾਈ_ਕੀਮਤ=0;
    if(같은말(&ਇਵੈਂਟ->type,"exec")) {
        if(ਇਵੈਂਟ->rq_data.size<4)return;
        ਲੰਬਾਈ_ਕੀਮਤ=assh_load_u32(ਇਵੈਂਟ->rq_data.data);
        if(!ਲੰਬਾਈ_ਕੀਮਤ||ਲੰਬਾਈ_ਕੀਮਤ>2048||ਇਵੈਂਟ->rq_data.size!=ਲੰਬਾਈ_ਕੀਮਤ+4)return;
        ਕਮਾਂਡ=ਇਵੈਂਟ->rq_data.data+4;
        for(unsigned 순번=0;순번<ਲੰਬਾਈ_ਕੀਮਤ;순번++)if(!ਕਮਾਂਡ[순번])return;
        ਆਦੇਸ਼_ਟਾਈਪ_ਕਰੋ=1;
    }else if(!같은말(&ਇਵੈਂਟ->type,"shell")||ਇਵੈਂਟ->rq_data.size)return;
    if(sizeof(입력줄)-입력수<ਲੰਬਾਈ_ਕੀਮਤ+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(ਲੰਬਾਈ_ਕੀਮਤ)원격입력넣기(ਕਮਾਂਡ,ਲੰਬਾਈ_ਕੀਮਤ);원격입력넣기(&끝,1);
    셸시작됨=1;ਇਵੈਂਟ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!ਆਦੇਸ਼_ਟਾਈਪ_ਕਰੋ){const char *ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ_eb81d7d9)원격출력(*ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(ਪਿਅਰ_ਕੀਮਤ<0){if(지금<재접속시각)return;ਪਿਅਰ_ਕੀਮਤ=망연결받기(듣는곳);if(ਪਿਅਰ_ਕੀਮਤ<0)return;
        접속시각=지금;assh_status_t ਗਲਤੀ=assh_session_create(ਸੰਦਰਭ_ਕੀਮਤ,&ਸਬੰਧ_e05f319b);
        if(ਗਲਤੀ){ਸਬੰਧ_e05f319b=0;진단("SSH session error ",ਗਲਤੀ);ਬੰਦ_ਕਰੋ_ਸਬੰਧ();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){ਬੰਦ_ਕਰੋ_ਸਬੰਧ();return;}
    if(ਚੈਨਲ_ਦਾਖਲਾ&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ਗਲਤੀ=assh_channel_data(ਚੈਨਲ_ਦਾਖਲਾ,출력줄+출력앞,&수);
            if(!ਗਲਤੀ){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ਗਲਤੀ!=ASSH_NO_DATA){ਬੰਦ_ਕਰੋ_ਸਬੰਧ();return;}
        }
        if(ਅੰਤ_ਸਥਿਤੀ>=0&&!출력수){unsigned char ਸਥਿਤੀ_ਕੀਮਤ[4];assh_store_u32(ਸਥਿਤੀ_ਕੀਮਤ,(uint32_t)ਅੰਤ_ਸਥਿਤੀ);
            if(assh_request(ਸਬੰਧ_e05f319b,ਚੈਨਲ_ਦਾਖਲਾ,"exit-status",11,ਸਥਿਤੀ_ਕੀਮਤ,4,0)||assh_channel_eof(ਚੈਨਲ_ਦਾਖਲਾ)||assh_channel_close(ਚੈਨਲ_ਦਾਖਲਾ)) {ਬੰਦ_ਕਰੋ_ਸਬੰਧ();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s ਇਵੈਂਟ;
        if(!assh_event_get(ਸਬੰਧ_e05f319b,&ਇਵੈਂਟ,지금/1000)){ਬੰਦ_ਕਰੋ_ਸਬੰਧ();return;}
        assh_status_t ਗਲਤੀ=ASSH_OK;int 쉬기=0,끊기=0;
        switch(ਇਵੈਂਟ.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(ਪਿਅਰ_ਕੀਮਤ,ਇਵੈਂਟ.transport.read.buf.data,ਇਵੈਂਟ.transport.read.buf.size);
            if(수>0)ਇਵੈਂਟ.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(ਪਿਅਰ_ਕੀਮਤ,ਇਵੈਂਟ.transport.write.buf.data,ਇਵੈਂਟ.transport.write.buf.size);
            if(수>0)ਇਵੈਂਟ.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ਇਵੈਂਟ.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ਇਵੈਂਟ.userauth_server.methods.retries>3)ਇਵੈਂਟ.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ਸਮੱਗਰੀ=&ਇਵੈਂਟ.userauth_server.password;
            if(같은말(&ਸਮੱਗਰੀ->username,"user")&&ਸਮੱਗਰੀ->password.size<=256&&!ਸਮੱਗਰੀ->new_password.size) {
                unsigned char ਸਾਰ_ਕੀਮਤ[32];ਰਿਮੋਟ_ਸਾਰ(ਸਮੱਗਰੀ->password.data,ਸਮੱਗਰੀ->password.size,ਸਾਰ_ਕੀਮਤ);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=ਸਾਰ_ਕੀਮਤ[순번]^ਸ਼ੈਲ_ਪਾਸਵਰਡ_ਸਾਰ[순번];memset(ਸਾਰ_ਕੀਮਤ,0,32);
                if(!차이)ਸਮੱਗਰੀ->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ਸਮੱਗਰੀ=&ਇਵੈਂਟ.connection.channel_open;
            if(인증됨&&!ਚੈਨਲ_ਦਾਖਲਾ&&셸대기중&&같은말(&ਸਮੱਗਰੀ->type,"session")&&!ਸਮੱਗਰੀ->rq_data.size) {
                ਸਮੱਗਰੀ->reply=ASSH_CONNECTION_REPLY_SUCCESS;ਸਮੱਗਰੀ->pkt_size=4096;
                ਸਮੱਗਰੀ->win_size=-1;ਚੈਨਲ_ਦਾਖਲਾ=ਸਮੱਗਰੀ->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&ਇਵੈਂਟ.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ਸਮੱਗਰੀ=&ਇਵੈਂਟ.connection.channel_data;
            if(!셸시작됨||ਸਮੱਗਰੀ->ch!=ਚੈਨਲ_ਦਾਖਲਾ||ਸਮੱਗਰੀ->ext){끊기=1;break;}
            unsigned 수=ਸਮੱਗਰੀ->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(ਸਮੱਗਰੀ->data.data[순번]==4){ਅੰਤ_ਸਥਿਤੀ=0;수=순번;ਸਮੱਗਰੀ->transferred=ਸਮੱਗਰੀ->data.size;break;}
            원격입력넣기(ਸਮੱਗਰੀ->data.data,수);if(!ਸਮੱਗਰੀ->transferred)ਸਮੱਗਰੀ->transferred=수;
            if(!수&&ਅੰਤ_ਸਥਿਤੀ<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: ਚੈਨਲ_ਦਾਖਲਾ=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ਇਵੈਂਟ.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(ਸਬੰਧ_e05f319b,&ਇਵੈਂਟ,ਗਲਤੀ);
        if(끊기){ਬੰਦ_ਕਰੋ_ਸਬੰਧ();return;}if(쉬기)return;
    }
}
