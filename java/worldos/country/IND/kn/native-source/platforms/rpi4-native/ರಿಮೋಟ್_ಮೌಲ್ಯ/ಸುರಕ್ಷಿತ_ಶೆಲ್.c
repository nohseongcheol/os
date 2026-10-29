/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "ರಿಮೋಟ್_ಮೌಲ್ಯ.h"
#include "암호기반.h"
#include "ಪ್ರೊಫೈಲ್.h"
#include "../ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್/ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್.h"
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
static struct assh_context_s *ಸಂದರ್ಭ_ಮೌಲ್ಯ;
static struct assh_session_s *ಸಂಪರ್ಕ_e05f319b;
static struct assh_channel_s *ಚಾನಲ್_ನಮೂದು;
static int 듣는곳=-1,ಪೀರ್_ಮೌಲ್ಯ=-1,인증됨,셸시작됨,ಆದೇಶ_ಪ್ರಕಾರ,ಅಂತ್ಯಗೊಳಿಸು_ಸ್ಥಿತಿ=-1,닫을예정,ಬೂಟ್_ದೋಷ,ಶೆಲ್_ನಿರೀಕ್ಷಿಸು;
static uintptr_t ಸಂಪರ್ಕ_ಸಮಯ,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *ಪದ_ಪಠ್ಯ,unsigned ಮೌಲ್ಯ) {
    while(*ಪದ_ಪಠ್ಯ)보드글자쓰기(*ಪದ_ಪಠ್ಯ++);
    char ಅಂಕೆ_ಮೌಲ್ಯ[12];unsigned 수=0;do{ಅಂಕೆ_ಮೌಲ್ಯ[수++]='0'+ಮೌಲ್ಯ%10;ಮೌಲ್ಯ/=10;}while(ಮೌಲ್ಯ);
    while(수)보드글자쓰기(ಅಂಕೆ_ಮೌಲ್ಯ[--수]);보드글자쓰기(10);
}
static assh_status_t ಸಿದ್ಧಪಡಿಸು_ಮೆಮೊರಿ(void *ಡೇಟಾ,void **ಇಮೇಲ್,size_t ಗಾತ್ರ,enum assh_alloc_type_e 종류) {
    (void)ಡೇಟಾ;(void)종류;
    if(!ಗಾತ್ರ){ಬಿಡುಗಡೆ_ರಿಮೋಟ್(*ಇಮೇಲ್);*ಇಮೇಲ್=0;return ASSH_OK;}
    void *새주소=원격재할당(*ಇಮೇಲ್,ಗಾತ್ರ);
    if(!새주소)return ASSH_ERR_MEM;*ಇಮೇಲ್=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ಡೇಟಾ,const struct assh_buffer_s *ಸೀಡ್_ಮೌಲ್ಯ) {
    (void)ಡೇಟಾ;(void)ಸೀಡ್_ಮೌಲ್ಯ;unsigned char 시험[32];int ಮಾಪನ=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return ಮಾಪನ?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ಡೇಟಾ,uint8_t *ಮಾಪನ,size_t ಉದ್ದ_ಮೌಲ್ಯ,uint_fast8_t 종류) {
    (void)ಡೇಟಾ;(void)종류;if(ಉದ್ದ_ಮೌಲ್ಯ>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(ಮಾಪನ,ಉದ್ದ_ಮೌಲ್ಯ)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ಡೇಟಾ){(void)ಡೇಟಾ;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void ಮುಚ್ಚು_ಸಂಪರ್ಕ(void) {
    인증됨=셸시작됨=0;ಚಾನಲ್_ನಮೂದು=0;
    if(ಸಂಪರ್ಕ_e05f319b)assh_session_release(ಸಂಪರ್ಕ_e05f319b);ಸಂಪರ್ಕ_e05f319b=0;
    if(ಪೀರ್_ಮೌಲ್ಯ>=0)ಮುಚ್ಚು_ನೆಟ್_ವರ್ಕ್(ಪೀರ್_ಮೌಲ್ಯ);ಪೀರ್_ಮೌಲ್ಯ=-1;ಆದೇಶ_ಪ್ರಕಾರ=0;ಅಂತ್ಯಗೊಳಿಸು_ಸ್ಥಿತಿ=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ಡೇಟಾ,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=ಡೇಟಾ[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int ಅಕ್ಷರ_ಮೌಲ್ಯ=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return ಅಕ್ಷರ_ಮೌಲ್ಯ;
}
void 원격출력(unsigned char ಅಕ್ಷರ_ಮೌಲ್ಯ) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=ಅಕ್ಷರ_ಮೌಲ್ಯ==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=ಅಕ್ಷರ_ಮೌಲ್ಯ;이전출력=ಅಕ್ಷರ_ಮೌಲ್ಯ;
}
uintptr_t ಬೋರ್ಡ್_ಅಂತ್ಯಗೊಳಿಸು_ರಿಮೋಟ್_ಆದೇಶ(uintptr_t ಸ್ಥಿತಿ_ಮೌಲ್ಯ){if(셸시작됨&&ಆದೇಶ_ಪ್ರಕಾರ)ಅಂತ್ಯಗೊಳಿಸು_ಸ್ಥಿತಿ=(int)ಸ್ಥಿತಿ_ಮೌಲ್ಯ;return 0;}
uintptr_t ಬೋರ್ಡ್_ರಿಮೋಟ್_ನಿರೀಕ್ಷಣೆ(uintptr_t ಸ್ಥಿತಿ_ಮೌಲ್ಯ){ಶೆಲ್_ನಿರೀಕ್ಷಿಸು=ಸ್ಥಿತಿ_ಮೌಲ್ಯ!=0;return 0;}
static int ಸಿದ್ಧಪಡಿಸು_ಶೆಲ್(void) {
    if(듣는곳>=0)return 0;
    if(!ಸಂದರ್ಭ_ಮೌಲ್ಯ){
        assh_status_t ದೋಷ=assh_context_create(&ಸಂದರ್ಭ_ಮೌಲ್ಯ,ASSH_SERVER,ಸಿದ್ಧಪಡಿಸು_ಮೆಮೊರಿ,0,&난수기,0);
        if(ದೋಷ)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *ವಿಧಾನ_ಮೋಡ್[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ದೋಷ=assh_algo_register(ಸಂದರ್ಭ_ಮೌಲ್ಯ,ASSH_SAFETY_WEAK,ವಿಧಾನ_ಮೋಡ್);
        if(!ದೋಷ)ದೋಷ=assh_service_register_va(ಸಂದರ್ಭ_ಮೌಲ್ಯ,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=ಸಾಧನ_ಕೀ;
        if(!ದೋಷ)ದೋಷ=assh_key_load(ಸಂದರ್ಭ_ಮೌಲ್ಯ,assh_context_keys(ಸಂದರ್ಭ_ಮೌಲ್ಯ),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(ಸಾಧನ_ಕೀ));
        if(ದೋಷ){진단("SSH init error ",ದೋಷ);assh_context_release(ಸಂದರ್ಭ_ಮೌಲ್ಯ);ಸಂದರ್ಭ_ಮೌಲ್ಯ=0;return -5;}
    }
    int ಪೋರ್ಟ್_ಮೌಲ್ಯ=통신끝점만들기(1);if(ಪೋರ್ಟ್_ಮೌಲ್ಯ<0)return ಪೋರ್ಟ್_ಮೌಲ್ಯ;통신주소재사용(ಪೋರ್ಟ್_ಮೌಲ್ಯ);
    int ಮಾಪನ=망주소묶기(ಪೋರ್ಟ್_ಮೌಲ್ಯ,0,22);if(!ಮಾಪನ)ಮಾಪನ=연결기다리기(ಪೋರ್ಟ್_ಮೌಲ್ಯ);
    if(ಮಾಪನ<0){ಮುಚ್ಚು_ನೆಟ್_ವರ್ಕ್(ಪೋರ್ಟ್_ಮೌಲ್ಯ);return ಮಾಪನ;}듣는곳=ಪೋರ್ಟ್_ಮೌಲ್ಯ;return 0;
}
uintptr_t ಬೋರ್ಡ್_ಶಾಡೋಯಿಂಗ್(uintptr_t 종류,uintptr_t ಹಕ್ರಿಯೆ) {
    if(종류==1)return(uint32_t)ನಿಯಂತ್ರಣ_ರಿಮೋಟ್_ಪ್ರದರ್ಶನ(ಹಕ್ರಿಯೆ);
    if(ಹಕ್ರಿಯೆ==0){ಮುಚ್ಚು_ಸಂಪರ್ಕ();if(듣는곳>=0)ಮುಚ್ಚು_ನೆಟ್_ವರ್ಕ್(듣는곳);듣는곳=-1;return 0;}
    if(ಹಕ್ರಿಯೆ==1){ಬೂಟ್_ದೋಷ=ಸಿದ್ಧಪಡಿಸು_ಶೆಲ್();return(uint32_t)ಬೂಟ್_ದೋಷ;}
    return(uint32_t)(듣는곳>=0?1:ಬೂಟ್_ದೋಷ);
}
void ಸಿದ್ಧಪಡಿಸು_ರಿಮೋಟ್(void){ಬೂಟ್_ದೋಷ=ಸಿದ್ಧಪಡಿಸು_ಶೆಲ್();ನಿಯಂತ್ರಣ_ರಿಮೋಟ್_ಪ್ರದರ್ಶನ(1);}
static int 같은말(const struct assh_cbuffer_s *ಡೇಟಾ,const char *ಪದ_ಪಠ್ಯ) {
    size_t ಉದ್ದ_ಮೌಲ್ಯ=strlen(ಪದ_ಪಠ್ಯ);return ಡೇಟಾ->size==ಉದ್ದ_ಮೌಲ್ಯ&&!memcmp(ಡೇಟಾ->data,ಪದ_ಪಠ್ಯ,ಉದ್ದ_ಮೌಲ್ಯ);
}
static int 터미널요청(const struct assh_cbuffer_s *ಡೇಟಾ) {
    if(ಡೇಟಾ->size<24)return 0;
    const unsigned char *ಡೇಟಾ_ಹುದ್ದೆ=ಡೇಟಾ->data;unsigned ಉದ್ದ_ಮೌಲ್ಯ=assh_load_u32(ಡೇಟಾ_ಹುದ್ದೆ);
    if(ಉದ್ದ_ಮೌಲ್ಯ>128||ಡೇಟಾ->size<ಉದ್ದ_ಮೌಲ್ಯ+24)return 0;
    unsigned ಮೋಡ್_ಮೌಲ್ಯ=assh_load_u32(ಡೇಟಾ_ಹುದ್ದೆ+4+ಉದ್ದ_ಮೌಲ್ಯ+16);
    return ಮೋಡ್_ಮೌಲ್ಯ<=2048&&ಡೇಟಾ->size==ಉದ್ದ_ಮೌಲ್ಯ+24+ಮೋಡ್_ಮೌಲ್ಯ;
}
static void 요청처리(struct assh_event_request_s *ಸಂಗತಿ) {
    if(!인증됨||ಸಂಗತಿ->ch!=ಚಾನಲ್_ನಮೂದು||!ಚಾನಲ್_ನಮೂದು)return;
    if(같은말(&ಸಂಗತಿ->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&ಸಂಗತಿ->rq_data))ಸಂಗತಿ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ಸಂಗತಿ->type,"window-change")) {
        if(셸시작됨&&ಸಂಗತಿ->rq_data.size==16)ಸಂಗತಿ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!ಶೆಲ್_ನಿರೀಕ್ಷಿಸು)return;
    const unsigned char *ಆಜ್ಞೆ=0;unsigned ಉದ್ದ_ಮೌಲ್ಯ=0;
    if(같은말(&ಸಂಗತಿ->type,"exec")) {
        if(ಸಂಗತಿ->rq_data.size<4)return;
        ಉದ್ದ_ಮೌಲ್ಯ=assh_load_u32(ಸಂಗತಿ->rq_data.data);
        if(!ಉದ್ದ_ಮೌಲ್ಯ||ಉದ್ದ_ಮೌಲ್ಯ>2048||ಸಂಗತಿ->rq_data.size!=ಉದ್ದ_ಮೌಲ್ಯ+4)return;
        ಆಜ್ಞೆ=ಸಂಗತಿ->rq_data.data+4;
        for(unsigned 순번=0;순번<ಉದ್ದ_ಮೌಲ್ಯ;순번++)if(!ಆಜ್ಞೆ[순번])return;
        ಆದೇಶ_ಪ್ರಕಾರ=1;
    }else if(!같은말(&ಸಂಗತಿ->type,"shell")||ಸಂಗತಿ->rq_data.size)return;
    if(sizeof(입력줄)-입력수<ಉದ್ದ_ಮೌಲ್ಯ+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(ಉದ್ದ_ಮೌಲ್ಯ)원격입력넣기(ಆಜ್ಞೆ,ಉದ್ದ_ಮೌಲ್ಯ);원격입력넣기(&끝,1);
    셸시작됨=1;ಸಂಗತಿ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!ಆದೇಶ_ಪ್ರಕಾರ){const char *README_ಫೈಲ್_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*README_ಫೈಲ್_eb81d7d9)원격출력(*README_ಫೈಲ್_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t ಇದೀಗ_ಮೌಲ್ಯ=보드밀리초();
    if(ಪೀರ್_ಮೌಲ್ಯ<0){if(ಇದೀಗ_ಮೌಲ್ಯ<재접속시각)return;ಪೀರ್_ಮೌಲ್ಯ=망연결받기(듣는곳);if(ಪೀರ್_ಮೌಲ್ಯ<0)return;
        ಸಂಪರ್ಕ_ಸಮಯ=ಇದೀಗ_ಮೌಲ್ಯ;assh_status_t ದೋಷ=assh_session_create(ಸಂದರ್ಭ_ಮೌಲ್ಯ,&ಸಂಪರ್ಕ_e05f319b);
        if(ದೋಷ){ಸಂಪರ್ಕ_e05f319b=0;진단("SSH session error ",ದೋಷ);ಮುಚ್ಚು_ಸಂಪರ್ಕ();return;}}
    if((!인증됨&&ಇದೀಗ_ಮೌಲ್ಯ-ಸಂಪರ್ಕ_ಸಮಯ>30000)||닫을예정==2||(닫을예정&&ಇದೀಗ_ಮೌಲ್ಯ>=닫는시각)){ಮುಚ್ಚು_ಸಂಪರ್ಕ();return;}
    if(ಚಾನಲ್_ನಮೂದು&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ದೋಷ=assh_channel_data(ಚಾನಲ್_ನಮೂದು,출력줄+출력앞,&수);
            if(!ದೋಷ){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ದೋಷ!=ASSH_NO_DATA){ಮುಚ್ಚು_ಸಂಪರ್ಕ();return;}
        }
        if(ಅಂತ್ಯಗೊಳಿಸು_ಸ್ಥಿತಿ>=0&&!출력수){unsigned char ಸ್ಥಿತಿ_ಮೌಲ್ಯ[4];assh_store_u32(ಸ್ಥಿತಿ_ಮೌಲ್ಯ,(uint32_t)ಅಂತ್ಯಗೊಳಿಸು_ಸ್ಥಿತಿ);
            if(assh_request(ಸಂಪರ್ಕ_e05f319b,ಚಾನಲ್_ನಮೂದು,"exit-status",11,ಸ್ಥಿತಿ_ಮೌಲ್ಯ,4,0)||assh_channel_eof(ಚಾನಲ್_ನಮೂದು)||assh_channel_close(ಚಾನಲ್_ನಮೂದು)) {ಮುಚ್ಚು_ಸಂಪರ್ಕ();return;}
            닫을예정=1;닫는시각=ಇದೀಗ_ಮೌಲ್ಯ+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s ಸಂಗತಿ;
        if(!assh_event_get(ಸಂಪರ್ಕ_e05f319b,&ಸಂಗತಿ,ಇದೀಗ_ಮೌಲ್ಯ/1000)){ಮುಚ್ಚು_ಸಂಪರ್ಕ();return;}
        assh_status_t ದೋಷ=ASSH_OK;int 쉬기=0,끊기=0;
        switch(ಸಂಗತಿ.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(ಪೀರ್_ಮೌಲ್ಯ,ಸಂಗತಿ.transport.read.buf.data,ಸಂಗತಿ.transport.read.buf.size);
            if(수>0)ಸಂಗತಿ.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(ಪೀರ್_ಮೌಲ್ಯ,ಸಂಗತಿ.transport.write.buf.data,ಸಂಗತಿ.transport.write.buf.size);
            if(수>0)ಸಂಗತಿ.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ಸಂಗತಿ.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ಸಂಗತಿ.userauth_server.methods.retries>3)ಸಂಗತಿ.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ಡೇಟಾ=&ಸಂಗತಿ.userauth_server.password;
            if(같은말(&ಡೇಟಾ->username,"user")&&ಡೇಟಾ->password.size<=256&&!ಡೇಟಾ->new_password.size) {
                unsigned char 요약[32];원격요약(ಡೇಟಾ->password.data,ಡೇಟಾ->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)ಡೇಟಾ->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ಡೇಟಾ=&ಸಂಗತಿ.connection.channel_open;
            if(인증됨&&!ಚಾನಲ್_ನಮೂದು&&ಶೆಲ್_ನಿರೀಕ್ಷಿಸು&&같은말(&ಡೇಟಾ->type,"session")&&!ಡೇಟಾ->rq_data.size) {
                ಡೇಟಾ->reply=ASSH_CONNECTION_REPLY_SUCCESS;ಡೇಟಾ->pkt_size=4096;
                ಡೇಟಾ->win_size=-1;ಚಾನಲ್_ನಮೂದು=ಡೇಟಾ->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&ಸಂಗತಿ.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ಡೇಟಾ=&ಸಂಗತಿ.connection.channel_data;
            if(!셸시작됨||ಡೇಟಾ->ch!=ಚಾನಲ್_ನಮೂದು||ಡೇಟಾ->ext){끊기=1;break;}
            unsigned 수=ಡೇಟಾ->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(ಡೇಟಾ->data.data[순번]==4){ಅಂತ್ಯಗೊಳಿಸು_ಸ್ಥಿತಿ=0;수=순번;ಡೇಟಾ->transferred=ಡೇಟಾ->data.size;break;}
            원격입력넣기(ಡೇಟಾ->data.data,수);if(!ಡೇಟಾ->transferred)ಡೇಟಾ->transferred=수;
            if(!수&&ಅಂತ್ಯಗೊಳಿಸು_ಸ್ಥಿತಿ<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: ಚಾನಲ್_ನಮೂದು=0;셸시작됨=0;닫을예정=1;닫는시각=ಇದೀಗ_ಮೌಲ್ಯ+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ಸಂಗತಿ.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(ಸಂಪರ್ಕ_e05f319b,&ಸಂಗತಿ,ದೋಷ);
        if(끊기){ಮುಚ್ಚು_ಸಂಪರ್ಕ();return;}if(쉬기)return;
    }
}
