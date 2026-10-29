/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "원격.h"
#include "암호기반.h"
#include "ᎬᏗᏍᎩ_ᏄᏍᏗᏓᏅᎢ.h"
#include "../통신망/통신망.h"
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
static struct assh_session_s *ᎫᏓᎸᎢ_e05f319b;
static struct assh_channel_s *ᎦᎳᏅᏛ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ;
static int 듣는곳=-1,ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ=-1,인증됨,셸시작됨,명령형,ᎠᏍᏆᏗᏍᏙᏗ_ᏄᏍᏗᏓᏅ=-1,닫을예정,ᎠᏂᎩᏍᏙᎢ_ᎦᎵᏓᏍᏔᏅ,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *말,unsigned ᏧᎬᏩᎶᏗᏯ) {
    while(*말)보드글자쓰기(*말++);
    char 숫자[12];unsigned 수=0;do{숫자[수++]='0'+ᏧᎬᏩᎶᏗᏯ%10;ᏧᎬᏩᎶᏗᏯ/=10;}while(ᏧᎬᏩᎶᏗᏯ);
    while(수)보드글자쓰기(숫자[--수]);보드글자쓰기(10);
}
static assh_status_t ᎭᏛᏅᎢᏍᏓ_ᎠᏅᏓᏗᏍᏙ(void *ᎦᏟᏌᏅᎯ,void **ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,size_t ᎢᎩᏓ,enum assh_alloc_type_e 종류) {
    (void)ᎦᏟᏌᏅᎯ;(void)종류;
    if(!ᎢᎩᏓ){원격해제(*ᎪᏪᎵ_ᏫᏗᎦᏅᏗ);*ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=0;return ASSH_OK;}
    void *새주소=원격재할당(*ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,ᎢᎩᏓ);
    if(!새주소)return ASSH_ERR_MEM;*ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ᎦᏟᏌᏅᎯ,const struct assh_buffer_s *씨앗) {
    (void)ᎦᏟᏌᏅᎯ;(void)씨앗;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ᎦᏟᏌᏅᎯ,uint8_t *결과,size_t ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ,uint_fast8_t 종류) {
    (void)ᎦᏟᏌᏅᎯ;(void)종류;if(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ᎦᏟᏌᏅᎯ){(void)ᎦᏟᏌᏅᎯ;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void ᎯᏍᏚᎲᎦ_ᎫᏓᎸᎢ(void) {
    인증됨=셸시작됨=0;ᎦᎳᏅᏛ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ=0;
    if(ᎫᏓᎸᎢ_e05f319b)assh_session_release(ᎫᏓᎸᎢ_e05f319b);ᎫᏓᎸᎢ_e05f319b=0;
    if(ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ>=0)ᎯᏍᏚᎲᎦ_ᏧᎾᏚᏓᎵ(ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ);ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ=-1;명령형=0;ᎠᏍᏆᏗᏍᏙᏗ_ᏄᏍᏗᏓᏅ=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ᎦᏟᏌᏅᎯ,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=ᎦᏟᏌᏅᎯ[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ;
}
void 원격출력(unsigned char ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ;이전출력=ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ;
}
uintptr_t 보드원격명령끝(uintptr_t ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ){if(셸시작됨&&명령형)ᎠᏍᏆᏗᏍᏙᏗ_ᏄᏍᏗᏓᏅ=(int)ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ;return 0;}
uintptr_t 보드원격대기(uintptr_t ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ){셸대기중=ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ!=0;return 0;}
static int ᎭᏛᏅᎢᏍᏓ_ᎤᏯᏍᎦ(void) {
    if(듣는곳>=0)return 0;
    if(!문맥){
        assh_status_t ᎦᎵᏓᏍᏔᏅ=assh_context_create(&문맥,ASSH_SERVER,ᎭᏛᏅᎢᏍᏓ_ᎠᏅᏓᏗᏍᏙ,0,&난수기,0);
        if(ᎦᎵᏓᏍᏔᏅ)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *method_ᎬᏙᏗ[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ᎦᎵᏓᏍᏔᏅ=assh_algo_register(문맥,ASSH_SAFETY_WEAK,method_ᎬᏙᏗ);
        if(!ᎦᎵᏓᏍᏔᏅ)ᎦᎵᏓᏍᏔᏅ=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=ᎠᏂᎩᏍᎩ_ᏍᏚᎢᏍᏗ;
        if(!ᎦᎵᏓᏍᏔᏅ)ᎦᎵᏓᏍᏔᏅ=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(ᎠᏂᎩᏍᎩ_ᏍᏚᎢᏍᏗ));
        if(ᎦᎵᏓᏍᏔᏅ){진단("SSH init error ",ᎦᎵᏓᏍᏔᏅ);assh_context_release(문맥);문맥=0;return -5;}
    }
    int ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ=통신끝점만들기(1);if(ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ<0)return ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ;통신주소재사용(ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ);
    int 결과=망주소묶기(ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ,0,22);if(!결과)결과=연결기다리기(ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ);
    if(결과<0){ᎯᏍᏚᎲᎦ_ᏧᎾᏚᏓᎵ(ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ);return 결과;}듣는곳=ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t ᎠᏛᏁᎵᏓ) {
    if(종류==1)return(uint32_t)원격화면제어(ᎠᏛᏁᎵᏓ);
    if(ᎠᏛᏁᎵᏓ==0){ᎯᏍᏚᎲᎦ_ᎫᏓᎸᎢ();if(듣는곳>=0)ᎯᏍᏚᎲᎦ_ᏧᎾᏚᏓᎵ(듣는곳);듣는곳=-1;return 0;}
    if(ᎠᏛᏁᎵᏓ==1){ᎠᏂᎩᏍᏙᎢ_ᎦᎵᏓᏍᏔᏅ=ᎭᏛᏅᎢᏍᏓ_ᎤᏯᏍᎦ();return(uint32_t)ᎠᏂᎩᏍᏙᎢ_ᎦᎵᏓᏍᏔᏅ;}
    return(uint32_t)(듣는곳>=0?1:ᎠᏂᎩᏍᏙᎢ_ᎦᎵᏓᏍᏔᏅ);
}
void 원격준비(void){ᎠᏂᎩᏍᏙᎢ_ᎦᎵᏓᏍᏔᏅ=ᎭᏛᏅᎢᏍᏓ_ᎤᏯᏍᎦ();원격화면제어(1);}
static int 같은말(const struct assh_cbuffer_s *ᎦᏟᏌᏅᎯ,const char *말) {
    size_t ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ=strlen(말);return ᎦᏟᏌᏅᎯ->size==ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ&&!memcmp(ᎦᏟᏌᏅᎯ->data,말,ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);
}
static int 터미널요청(const struct assh_cbuffer_s *ᎦᏟᏌᏅᎯ) {
    if(ᎦᏟᏌᏅᎯ->size<24)return 0;
    const unsigned char *자료위치=ᎦᏟᏌᏅᎯ->data;unsigned ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ=assh_load_u32(자료위치);
    if(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ>128||ᎦᏟᏌᏅᎯ->size<ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ+24)return 0;
    unsigned ᎬᏙᏗ_ᏧᎬᏩᎶᏗᏯ=assh_load_u32(자료위치+4+ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ+16);
    return ᎬᏙᏗ_ᏧᎬᏩᎶᏗᏯ<=2048&&ᎦᏟᏌᏅᎯ->size==ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ+24+ᎬᏙᏗ_ᏧᎬᏩᎶᏗᏯ;
}
static void 요청처리(struct assh_event_request_s *ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ) {
    if(!인증됨||ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ->ch!=ᎦᎳᏅᏛ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ||!ᎦᎳᏅᏛ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ)return;
    if(같은말(&ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ->rq_data))ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ->type,"window-change")) {
        if(셸시작됨&&ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ->rq_data.size==16)ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *ᎤᏁᏤᎸᎩ=0;unsigned ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ=0;
    if(같은말(&ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ->type,"exec")) {
        if(ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ->rq_data.size<4)return;
        ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ=assh_load_u32(ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ->rq_data.data);
        if(!ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ||ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ>2048||ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ->rq_data.size!=ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ+4)return;
        ᎤᏁᏤᎸᎩ=ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ->rq_data.data+4;
        for(unsigned 순번=0;순번<ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ;순번++)if(!ᎤᏁᏤᎸᎩ[순번])return;
        명령형=1;
    }else if(!같은말(&ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ->type,"shell")||ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ->rq_data.size)return;
    if(sizeof(입력줄)-입력수<ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ)원격입력넣기(ᎤᏁᏤᎸᎩ,ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);원격입력넣기(&끝,1);
    셸시작됨=1;ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!명령형){const char *ᏍᎩᎪᎵᏯ_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*ᏍᎩᎪᎵᏯ_eb81d7d9)원격출력(*ᏍᎩᎪᎵᏯ_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ<0){if(지금<재접속시각)return;ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ=망연결받기(듣는곳);if(ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ<0)return;
        접속시각=지금;assh_status_t ᎦᎵᏓᏍᏔᏅ=assh_session_create(문맥,&ᎫᏓᎸᎢ_e05f319b);
        if(ᎦᎵᏓᏍᏔᏅ){ᎫᏓᎸᎢ_e05f319b=0;진단("SSH session error ",ᎦᎵᏓᏍᏔᏅ);ᎯᏍᏚᎲᎦ_ᎫᏓᎸᎢ();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){ᎯᏍᏚᎲᎦ_ᎫᏓᎸᎢ();return;}
    if(ᎦᎳᏅᏛ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ᎦᎵᏓᏍᏔᏅ=assh_channel_data(ᎦᎳᏅᏛ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ,출력줄+출력앞,&수);
            if(!ᎦᎵᏓᏍᏔᏅ){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ᎦᎵᏓᏍᏔᏅ!=ASSH_NO_DATA){ᎯᏍᏚᎲᎦ_ᎫᏓᎸᎢ();return;}
        }
        if(ᎠᏍᏆᏗᏍᏙᏗ_ᏄᏍᏗᏓᏅ>=0&&!출력수){unsigned char ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ[4];assh_store_u32(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ,(uint32_t)ᎠᏍᏆᏗᏍᏙᏗ_ᏄᏍᏗᏓᏅ);
            if(assh_request(ᎫᏓᎸᎢ_e05f319b,ᎦᎳᏅᏛ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ,"exit-status",11,ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ,4,0)||assh_channel_eof(ᎦᎳᏅᏛ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ)||assh_channel_close(ᎦᎳᏅᏛ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ)) {ᎯᏍᏚᎲᎦ_ᎫᏓᎸᎢ();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ;
        if(!assh_event_get(ᎫᏓᎸᎢ_e05f319b,&ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ,지금/1000)){ᎯᏍᏚᎲᎦ_ᎫᏓᎸᎢ();return;}
        assh_status_t ᎦᎵᏓᏍᏔᏅ=ASSH_OK;int 쉬기=0,끊기=0;
        switch(ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ,ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.transport.read.buf.data,ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.transport.read.buf.size);
            if(수>0)ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ,ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.transport.write.buf.data,ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.transport.write.buf.size);
            if(수>0)ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.userauth_server.methods.retries>3)ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ᎦᏟᏌᏅᎯ=&ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.userauth_server.password;
            if(같은말(&ᎦᏟᏌᏅᎯ->username,"user")&&ᎦᏟᏌᏅᎯ->password.size<=256&&!ᎦᏟᏌᏅᎯ->new_password.size) {
                unsigned char 요약[32];원격요약(ᎦᏟᏌᏅᎯ->password.data,ᎦᏟᏌᏅᎯ->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)ᎦᏟᏌᏅᎯ->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ᎦᏟᏌᏅᎯ=&ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.connection.channel_open;
            if(인증됨&&!ᎦᎳᏅᏛ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ&&셸대기중&&같은말(&ᎦᏟᏌᏅᎯ->type,"session")&&!ᎦᏟᏌᏅᎯ->rq_data.size) {
                ᎦᏟᏌᏅᎯ->reply=ASSH_CONNECTION_REPLY_SUCCESS;ᎦᏟᏌᏅᎯ->pkt_size=4096;
                ᎦᏟᏌᏅᎯ->win_size=-1;ᎦᎳᏅᏛ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ=ᎦᏟᏌᏅᎯ->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ᎦᏟᏌᏅᎯ=&ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.connection.channel_data;
            if(!셸시작됨||ᎦᏟᏌᏅᎯ->ch!=ᎦᎳᏅᏛ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ||ᎦᏟᏌᏅᎯ->ext){끊기=1;break;}
            unsigned 수=ᎦᏟᏌᏅᎯ->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(ᎦᏟᏌᏅᎯ->data.data[순번]==4){ᎠᏍᏆᏗᏍᏙᏗ_ᏄᏍᏗᏓᏅ=0;수=순번;ᎦᏟᏌᏅᎯ->transferred=ᎦᏟᏌᏅᎯ->data.size;break;}
            원격입력넣기(ᎦᏟᏌᏅᎯ->data.data,수);if(!ᎦᏟᏌᏅᎯ->transferred)ᎦᏟᏌᏅᎯ->transferred=수;
            if(!수&&ᎠᏍᏆᏗᏍᏙᏗ_ᏄᏍᏗᏓᏅ<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: ᎦᎳᏅᏛ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(ᎫᏓᎸᎢ_e05f319b,&ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ,ᎦᎵᏓᏍᏔᏅ);
        if(끊기){ᎯᏍᏚᎲᎦ_ᎫᏓᎸᎢ();return;}if(쉬기)return;
    }
}
