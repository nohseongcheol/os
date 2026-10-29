/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ.h"
#include "암호기반.h"
#include "ପ୍ରୋଫାଇଲ୍.h"
#include "../ନେଟ୍_ୱାର୍କ୍_ଗଦା/ନେଟ୍_ୱାର୍କ୍_ଗଦା.h"
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
static struct assh_context_s *ପ୍ରସଙ୍ଗ_ମୂଲ୍ୟ;
static struct assh_session_s *ସଂଯୋଗ_e05f319b;
static struct assh_channel_s *ଚ୍ୟାନେଲ୍_ଏଣ୍ଟ୍ରି;
static int 듣는곳=-1,ସମକକ୍ଷ_ମୂଲ୍ୟ=-1,인증됨,셸시작됨,ନିର୍ଦ୍ଦେଶ_ଟାଇପ୍_କରିବା,ଶେଷ_କରନ୍ତୁ_ସ୍ଥିତି_2bce2943=-1,닫을예정,ଷ୍ଟାର୍ଟଅପ୍_ତ୍ରୁଟି,ଖୋଳ_ୱଇଟିଙ୍ଗ୍;
static uintptr_t ସଂଯୋଗ_ସମୟ,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *말,unsigned ମୂଲ୍ୟ) {
    while(*말)보드글자쓰기(*말++);
    char ଅଙ୍କ_ମୂଲ୍ୟ[12];unsigned 수=0;do{ଅଙ୍କ_ମୂଲ୍ୟ[수++]='0'+ମୂଲ୍ୟ%10;ମୂଲ୍ୟ/=10;}while(ମୂଲ୍ୟ);
    while(수)보드글자쓰기(ଅଙ୍କ_ମୂଲ୍ୟ[--수]);보드글자쓰기(10);
}
static assh_status_t ପ୍ରସ୍ତୁତ_ମୋମରୀ(void *ଡାଟା,void **ଠିକଣା,size_t ଆକାର,enum assh_alloc_type_e 종류) {
    (void)ଡାଟା;(void)종류;
    if(!ଆକାର){ରିଲିଜ୍_ଦୂରବର୍ତ୍ତୀ(*ଠିକଣା);*ଠିକଣା=0;return ASSH_OK;}
    void *새주소=원격재할당(*ଠିକଣା,ଆକାର);
    if(!새주소)return ASSH_ERR_MEM;*ଠିକଣା=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ଡାଟା,const struct assh_buffer_s *ସିଡ୍_ମୂଲ୍ୟ) {
    (void)ଡାଟା;(void)ସିଡ୍_ମୂଲ୍ୟ;unsigned char 시험[32];int ମାପ=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return ମାପ?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ଡାଟା,uint8_t *ମାପ,size_t ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ,uint_fast8_t 종류) {
    (void)ଡାଟା;(void)종류;if(ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(ମାପ,ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ଡାଟା){(void)ଡାଟା;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void ବନ୍ଦ_ସଂଯୋଗ(void) {
    인증됨=셸시작됨=0;ଚ୍ୟାନେଲ୍_ଏଣ୍ଟ୍ରି=0;
    if(ସଂଯୋଗ_e05f319b)assh_session_release(ସଂଯୋଗ_e05f319b);ସଂଯୋଗ_e05f319b=0;
    if(ସମକକ୍ଷ_ମୂଲ୍ୟ>=0)ବନ୍ଦ_ନେଟ୍_ୱାର୍କ୍(ସମକକ୍ଷ_ମୂଲ୍ୟ);ସମକକ୍ଷ_ମୂଲ୍ୟ=-1;ନିର୍ଦ୍ଦେଶ_ଟାଇପ୍_କରିବା=0;ଶେଷ_କରନ୍ତୁ_ସ୍ଥିତି_2bce2943=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ଡାଟା,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=ଡାଟା[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int ବର୍ଣ୍ଣ_ମୂଲ୍ୟ=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return ବର୍ଣ୍ଣ_ମୂଲ୍ୟ;
}
void 원격출력(unsigned char ବର୍ଣ୍ଣ_ମୂଲ୍ୟ) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=ବର୍ଣ୍ଣ_ମୂଲ୍ୟ==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=ବର୍ଣ୍ଣ_ମୂଲ୍ୟ;이전출력=ବର୍ଣ୍ଣ_ମୂଲ୍ୟ;
}
uintptr_t ବୋର୍ଡ୍_ଶେଷ_କରନ୍ତୁ_ଦୂରବର୍ତ୍ତୀ_ନିର୍ଦ୍ଦେଶ(uintptr_t ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1){if(셸시작됨&&ନିର୍ଦ୍ଦେଶ_ଟାଇପ୍_କରିବା)ଶେଷ_କରନ୍ତୁ_ସ୍ଥିତି_2bce2943=(int)ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1;return 0;}
uintptr_t ବୋର୍ଡ୍_ଦୂରବର୍ତ୍ତୀ_ଅପେକ୍ଷା(uintptr_t ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1){ଖୋଳ_ୱଇଟିଙ୍ଗ୍=ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1!=0;return 0;}
static int ପ୍ରସ୍ତୁତ_ଖୋଳ(void) {
    if(듣는곳>=0)return 0;
    if(!ପ୍ରସଙ୍ଗ_ମୂଲ୍ୟ){
        assh_status_t ତ୍ରୁଟି=assh_context_create(&ପ୍ରସଙ୍ଗ_ମୂଲ୍ୟ,ASSH_SERVER,ପ୍ରସ୍ତୁତ_ମୋମରୀ,0,&난수기,0);
        if(ତ୍ରୁଟି)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *ପଦ୍ଧତି_ମୋଡ୍[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ତ୍ରୁଟି=assh_algo_register(ପ୍ରସଙ୍ଗ_ମୂଲ୍ୟ,ASSH_SAFETY_WEAK,ପଦ୍ଧତି_ମୋଡ୍);
        if(!ତ୍ରୁଟି)ତ୍ରୁଟି=assh_service_register_va(ପ୍ରସଙ୍ଗ_ମୂଲ୍ୟ,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=ଡିଭାଇସ_କୀ;
        if(!ତ୍ରୁଟି)ତ୍ରୁଟି=assh_key_load(ପ୍ରସଙ୍ଗ_ମୂଲ୍ୟ,assh_context_keys(ପ୍ରସଙ୍ଗ_ମୂଲ୍ୟ),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(ଡିଭାଇସ_କୀ));
        if(ତ୍ରୁଟି){진단("SSH init error ",ତ୍ରୁଟି);assh_context_release(ପ୍ରସଙ୍ଗ_ମୂଲ୍ୟ);ପ୍ରସଙ୍ଗ_ମୂଲ୍ୟ=0;return -5;}
    }
    int ପୋର୍ଟ_ମୂଲ୍ୟ=통신끝점만들기(1);if(ପୋର୍ଟ_ମୂଲ୍ୟ<0)return ପୋର୍ଟ_ମୂଲ୍ୟ;통신주소재사용(ପୋର୍ଟ_ମୂଲ୍ୟ);
    int ମାପ=망주소묶기(ପୋର୍ଟ_ମୂଲ୍ୟ,0,22);if(!ମାପ)ମାପ=연결기다리기(ପୋର୍ଟ_ମୂଲ୍ୟ);
    if(ମାପ<0){ବନ୍ଦ_ନେଟ୍_ୱାର୍କ୍(ପୋର୍ଟ_ମୂଲ୍ୟ);return ମାପ;}듣는곳=ପୋର୍ଟ_ମୂଲ୍ୟ;return 0;
}
uintptr_t ବୋର୍ଡ୍_ସେଡୋଇଂ(uintptr_t 종류,uintptr_t କାମ) {
    if(종류==1)return(uint32_t)ନିୟନ୍ତ୍ରଣ_ଦୂରବର୍ତ୍ତୀ_ଦେଖାଇବା(କାମ);
    if(କାମ==0){ବନ୍ଦ_ସଂଯୋଗ();if(듣는곳>=0)ବନ୍ଦ_ନେଟ୍_ୱାର୍କ୍(듣는곳);듣는곳=-1;return 0;}
    if(କାମ==1){ଷ୍ଟାର୍ଟଅପ୍_ତ୍ରୁଟି=ପ୍ରସ୍ତୁତ_ଖୋଳ();return(uint32_t)ଷ୍ଟାର୍ଟଅପ୍_ତ୍ରୁଟି;}
    return(uint32_t)(듣는곳>=0?1:ଷ୍ଟାର୍ଟଅପ୍_ତ୍ରୁଟି);
}
void ପ୍ରସ୍ତୁତ_ଦୂରବର୍ତ୍ତୀ(void){ଷ୍ଟାର୍ଟଅପ୍_ତ୍ରୁଟି=ପ୍ରସ୍ତୁତ_ଖୋଳ();ନିୟନ୍ତ୍ରଣ_ଦୂରବର୍ତ୍ତୀ_ଦେଖାଇବା(1);}
static int 같은말(const struct assh_cbuffer_s *ଡାଟା,const char *말) {
    size_t ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ=strlen(말);return ଡାଟା->size==ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ&&!memcmp(ଡାଟା->data,말,ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ);
}
static int 터미널요청(const struct assh_cbuffer_s *ଡାଟା) {
    if(ଡାଟା->size<24)return 0;
    const unsigned char *ଡାଟା_ସ୍ଥିତି=ଡାଟା->data;unsigned ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ=assh_load_u32(ଡାଟା_ସ୍ଥିତି);
    if(ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ>128||ଡାଟା->size<ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ+24)return 0;
    unsigned ମୋଡ୍_ମୂଲ୍ୟ=assh_load_u32(ଡାଟା_ସ୍ଥିତି+4+ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ+16);
    return ମୋଡ୍_ମୂଲ୍ୟ<=2048&&ଡାଟା->size==ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ+24+ମୋଡ୍_ମୂଲ୍ୟ;
}
static void 요청처리(struct assh_event_request_s *ଘଟଣା) {
    if(!인증됨||ଘଟଣା->ch!=ଚ୍ୟାନେଲ୍_ଏଣ୍ଟ୍ରି||!ଚ୍ୟାନେଲ୍_ଏଣ୍ଟ୍ରି)return;
    if(같은말(&ଘଟଣା->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&ଘଟଣା->rq_data))ଘଟଣା->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ଘଟଣା->type,"window-change")) {
        if(셸시작됨&&ଘଟଣା->rq_data.size==16)ଘଟଣା->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!ଖୋଳ_ୱଇଟିଙ୍ଗ୍)return;
    const unsigned char *ନିର୍ଦ୍ଦେଶ=0;unsigned ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ=0;
    if(같은말(&ଘଟଣା->type,"exec")) {
        if(ଘଟଣା->rq_data.size<4)return;
        ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ=assh_load_u32(ଘଟଣା->rq_data.data);
        if(!ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ||ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ>2048||ଘଟଣା->rq_data.size!=ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ+4)return;
        ନିର୍ଦ୍ଦେଶ=ଘଟଣା->rq_data.data+4;
        for(unsigned 순번=0;순번<ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ;순번++)if(!ନିର୍ଦ୍ଦେଶ[순번])return;
        ନିର୍ଦ୍ଦେଶ_ଟାଇପ୍_କରିବା=1;
    }else if(!같은말(&ଘଟଣା->type,"shell")||ଘଟଣା->rq_data.size)return;
    if(sizeof(입력줄)-입력수<ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ)원격입력넣기(ନିର୍ଦ୍ଦେଶ,ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ);원격입력넣기(&끝,1);
    셸시작됨=1;ଘଟଣା->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!ନିର୍ଦ୍ଦେଶ_ଟାଇପ୍_କରିବା){const char *ମତେପଢନ୍ତୁ_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*ମତେପଢନ୍ତୁ_eb81d7d9)원격출력(*ମତେପଢନ୍ତୁ_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(ସମକକ୍ଷ_ମୂଲ୍ୟ<0){if(지금<재접속시각)return;ସମକକ୍ଷ_ମୂଲ୍ୟ=망연결받기(듣는곳);if(ସମକକ୍ଷ_ମୂଲ୍ୟ<0)return;
        ସଂଯୋଗ_ସମୟ=지금;assh_status_t ତ୍ରୁଟି=assh_session_create(ପ୍ରସଙ୍ଗ_ମୂଲ୍ୟ,&ସଂଯୋଗ_e05f319b);
        if(ତ୍ରୁଟି){ସଂଯୋଗ_e05f319b=0;진단("SSH session error ",ତ୍ରୁଟି);ବନ୍ଦ_ସଂଯୋଗ();return;}}
    if((!인증됨&&지금-ସଂଯୋଗ_ସମୟ>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){ବନ୍ଦ_ସଂଯୋଗ();return;}
    if(ଚ୍ୟାନେଲ୍_ଏଣ୍ଟ୍ରି&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ତ୍ରୁଟି=assh_channel_data(ଚ୍ୟାନେଲ୍_ଏଣ୍ଟ୍ରି,출력줄+출력앞,&수);
            if(!ତ୍ରୁଟି){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ତ୍ରୁଟି!=ASSH_NO_DATA){ବନ୍ଦ_ସଂଯୋଗ();return;}
        }
        if(ଶେଷ_କରନ୍ତୁ_ସ୍ଥିତି_2bce2943>=0&&!출력수){unsigned char ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1[4];assh_store_u32(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1,(uint32_t)ଶେଷ_କରନ୍ତୁ_ସ୍ଥିତି_2bce2943);
            if(assh_request(ସଂଯୋଗ_e05f319b,ଚ୍ୟାନେଲ୍_ଏଣ୍ଟ୍ରି,"exit-status",11,ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1,4,0)||assh_channel_eof(ଚ୍ୟାନେଲ୍_ଏଣ୍ଟ୍ରି)||assh_channel_close(ଚ୍ୟାନେଲ୍_ଏଣ୍ଟ୍ରି)) {ବନ୍ଦ_ସଂଯୋଗ();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned 차례=0;차례<16;차례++) {
        struct assh_event_s ଘଟଣା;
        if(!assh_event_get(ସଂଯୋଗ_e05f319b,&ଘଟଣା,지금/1000)){ବନ୍ଦ_ସଂଯୋଗ();return;}
        assh_status_t ତ୍ରୁଟି=ASSH_OK;int 쉬기=0,끊기=0;
        switch(ଘଟଣା.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(ସମକକ୍ଷ_ମୂଲ୍ୟ,ଘଟଣା.transport.read.buf.data,ଘଟଣା.transport.read.buf.size);
            if(수>0)ଘଟଣା.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(ସମକକ୍ଷ_ମୂଲ୍ୟ,ଘଟଣା.transport.write.buf.data,ଘଟଣା.transport.write.buf.size);
            if(수>0)ଘଟଣା.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ଘଟଣା.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ଘଟଣା.userauth_server.methods.retries>3)ଘଟଣା.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ଡାଟା=&ଘଟଣା.userauth_server.password;
            if(같은말(&ଡାଟା->username,"user")&&ଡାଟା->password.size<=256&&!ଡାଟା->new_password.size) {
                unsigned char ସାରାଂଶ_ମୂଲ୍ୟ[32];ଦୂରବର୍ତ୍ତୀ_ସାରାଂଶ(ଡାଟା->password.data,ଡାଟା->password.size,ସାରାଂଶ_ମୂଲ୍ୟ);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=ସାରାଂଶ_ମୂଲ୍ୟ[순번]^ଖୋଳ_ପାସ୍_ୱାର୍ଡ୍_ସାରାଂଶ[순번];memset(ସାରାଂଶ_ମୂଲ୍ୟ,0,32);
                if(!차이)ଡାଟା->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ଡାଟା=&ଘଟଣା.connection.channel_open;
            if(인증됨&&!ଚ୍ୟାନେଲ୍_ଏଣ୍ଟ୍ରି&&ଖୋଳ_ୱଇଟିଙ୍ଗ୍&&같은말(&ଡାଟା->type,"session")&&!ଡାଟା->rq_data.size) {
                ଡାଟା->reply=ASSH_CONNECTION_REPLY_SUCCESS;ଡାଟା->pkt_size=4096;
                ଡାଟା->win_size=-1;ଚ୍ୟାନେଲ୍_ଏଣ୍ଟ୍ରି=ଡାଟା->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&ଘଟଣା.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ଡାଟା=&ଘଟଣା.connection.channel_data;
            if(!셸시작됨||ଡାଟା->ch!=ଚ୍ୟାନେଲ୍_ଏଣ୍ଟ୍ରି||ଡାଟା->ext){끊기=1;break;}
            unsigned 수=ଡାଟା->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(ଡାଟା->data.data[순번]==4){ଶେଷ_କରନ୍ତୁ_ସ୍ଥିତି_2bce2943=0;수=순번;ଡାଟା->transferred=ଡାଟା->data.size;break;}
            원격입력넣기(ଡାଟା->data.data,수);if(!ଡାଟା->transferred)ଡାଟା->transferred=수;
            if(!수&&ଶେଷ_କରନ୍ତୁ_ସ୍ଥିତି_2bce2943<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: ଚ୍ୟାନେଲ୍_ଏଣ୍ଟ୍ରି=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ଘଟଣା.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(ସଂଯୋଗ_e05f319b,&ଘଟଣା,ତ୍ରୁଟି);
        if(끊기){ବନ୍ଦ_ସଂଯୋଗ();return;}if(쉬기)return;
    }
}
