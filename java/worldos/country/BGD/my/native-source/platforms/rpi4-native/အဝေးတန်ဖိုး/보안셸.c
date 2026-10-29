/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "အဝေးတန်ဖိုး.h"
#include "암호기반.h"
#include "ချိတ်ဆက်ပုံစံ.h"
#include "../ကွန်ရက်အလွှာစု/ကွန်ရက်အလွှာစု.h"
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
static struct assh_context_s *ပတ်ဝန်းကျင်အဓိပ္ပာယ်တန်ဖိုး;
static struct assh_session_s *ချိတ်ဆက်မှု;
static struct assh_channel_s *ချန်နယ်အချက်;
static int 듣는곳=-1,တစ်ဖက်တန်ဖိုး=-1,인증됨,셸시작됨,အမိန့်အမျိုးပုံစံ,အဆုံးအခြေအနေ=-1,닫을예정,시작오류,အမိန့်ဝင်းစောင့်နေ;
static uintptr_t ချိတ်ဆက်မှုအချိန်,재접속시각,닫는시각;
static unsigned char အဝင်စာကြောင်း[8192],အထွက်စာကြောင်း[65536];
static unsigned အဝင်ဦးခေါင်း,အဝင်အရေအတွက်,အထွက်ဦးခေါင်း,အထွက်အရေအတွက်,ယခင်အထွက်;
static void 진단(const char *စကားလုံးစာသား,unsigned တန်ဖိုး) {
    while(*စကားလုံးစာသား)보드글자쓰기(*စကားလုံးစာသား++);
    char ဂဏန်းတန်ဖိုး[12];unsigned ကိန်းတန်ဖိုး=0;do{ဂဏန်းတန်ဖိုး[ကိန်းတန်ဖိုး++]='0'+တန်ဖိုး%10;တန်ဖိုး/=10;}while(တန်ဖိုး);
    while(ကိန်းတန်ဖိုး)보드글자쓰기(ဂဏန်းတန်ဖိုး[--ကိန်းတန်ဖိုး]);보드글자쓰기(10);
}
static assh_status_t မှတ်ဉာဏ်ပြင်ဆင်(void *ဒေတာ,void **လိပ်စာ,size_t အရွယ်,enum assh_alloc_type_e အမျိုးအစားတန်ဖိုး) {
    (void)ဒေတာ;(void)အမျိုးအစားတန်ဖိုး;
    if(!အရွယ်){အဝေးလွှတ်ပေး(*လိပ်စာ);*လိပ်စာ=0;return ASSH_OK;}
    void *အသစ်လိပ်စာ=원격재할당(*လိပ်စာ,အရွယ်);
    if(!အသစ်လိပ်စာ)return ASSH_ERR_MEM;*လိပ်စာ=အသစ်လိပ်စာ;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ဒေတာ,const struct assh_buffer_s *씨앗) {
    (void)ဒေတာ;(void)씨앗;unsigned char စမ်းသပ်မှု[32];int ရလဒ်=원격난수(စမ်းသပ်မှု,sizeof(စမ်းသပ်မှု));memset(စမ်းသပ်မှု,0,sizeof(စမ်းသပ်မှု));
    return ရလဒ်?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ဒေတာ,uint8_t *ရလဒ်,size_t အလျား,uint_fast8_t အမျိုးအစားတန်ဖိုး) {
    (void)ဒေတာ;(void)အမျိုးအစားတန်ဖိုး;if(အလျား>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(ရလဒ်,အလျား)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ဒေတာ){(void)ဒေတာ;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void ချိတ်ဆက်မှုပိတ်(void) {
    인증됨=셸시작됨=0;ချန်နယ်အချက်=0;
    if(ချိတ်ဆက်မှု)assh_session_release(ချိတ်ဆက်မှု);ချိတ်ဆက်မှု=0;
    if(တစ်ဖက်တန်ဖိုး>=0)ကွန်ရက်ပိတ်(တစ်ဖက်တန်ဖိုး);တစ်ဖက်တန်ဖိုး=-1;အမိန့်အမျိုးပုံစံ=0;အဆုံးအခြေအနေ=-1;닫을예정=0;
    အဝင်ဦးခေါင်း=အဝင်အရေအတွက်=အထွက်ဦးခေါင်း=အထွက်အရေအတွက်=ယခင်အထွက်=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ဒေတာ,unsigned ကိန်းတန်ဖိုး) {
    if(ကိန်းတန်ဖိုး>sizeof(အဝင်စာကြောင်း)-အဝင်အရေအတွက်)return -11;
    for(unsigned အစဉ်အမှတ်=0;အစဉ်အမှတ်<ကိန်းတန်ဖိုး;အစဉ်အမှတ်++)အဝင်စာကြောင်း[(အဝင်ဦးခေါင်း+အဝင်အရေအတွက်++)%sizeof(အဝင်စာကြောင်း)]=ဒေတာ[အစဉ်အမှတ်];return ကိန်းတန်ဖိုး;
}
int အဝေးအဝင်(void) {
    if(!အဝင်အရေအတွက်)return -1;int အက္ခရာတန်ဖိုး=အဝင်စာကြောင်း[အဝင်ဦးခေါင်း];အဝင်ဦးခေါင်း=(အဝင်ဦးခေါင်း+1)%sizeof(အဝင်စာကြောင်း);အဝင်အရေအတွက်--;return အက္ခရာတန်ဖိုး;
}
void အဝေးအထွက်(unsigned char အက္ခရာတန်ဖိုး) {
    if(!셸시작됨||닫을예정)return;
    unsigned နည်းစနစ်နောက်တွဲ=အက္ခရာတန်ဖိုး==10&&ယခင်အထွက်!=13;
    if(အထွက်အရေအတွက်+1+နည်းစနစ်နောက်တွဲ>sizeof(အထွက်စာကြောင်း)){닫을예정=2;return;}
    if(နည်းစနစ်နောက်တွဲ)အထွက်စာကြောင်း[(အထွက်ဦးခေါင်း+အထွက်အရေအတွက်++)%sizeof(အထွက်စာကြောင်း)]=13;
    အထွက်စာကြောင်း[(အထွက်ဦးခေါင်း+အထွက်အရေအတွက်++)%sizeof(အထွက်စာကြောင်း)]=အက္ခရာတန်ဖိုး;ယခင်အထွက်=အက္ခရာတန်ဖိုး;
}
uintptr_t ဆားကစ်ပြားအဆုံးအဝေးအမိန့်(uintptr_t အခြေအနေတန်ဖိုး){if(셸시작됨&&အမိန့်အမျိုးပုံစံ)အဆုံးအခြေအနေ=(int)အခြေအနေတန်ဖိုး;return 0;}
uintptr_t ဆားကစ်ပြားအဝေးစောင့်(uintptr_t အခြေအနေတန်ဖိုး){အမိန့်ဝင်းစောင့်နေ=အခြေအနေတန်ဖိုး!=0;return 0;}
static int အမိန့်ဝင်းပြင်ဆင်(void) {
    if(듣는곳>=0)return 0;
    if(!ပတ်ဝန်းကျင်အဓိပ္ပာယ်တန်ဖိုး){
        assh_status_t အမှား=assh_context_create(&ပတ်ဝန်းကျင်အဓိပ္ပာယ်တန်ဖိုး,ASSH_SERVER,မှတ်ဉာဏ်ပြင်ဆင်,0,&난수기,0);
        if(အမှား)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *နည်းလမ်းနည်းစနစ်[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        အမှား=assh_algo_register(ပတ်ဝန်းကျင်အဓိပ္ပာယ်တန်ဖိုး,ASSH_SAFETY_WEAK,နည်းလမ်းနည်းစနစ်);
        if(!အမှား)အမှား=assh_service_register_va(ပတ်ဝန်းကျင်အဓိပ္ပာယ်တန်ဖိုး,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *အဓိကသော့=ကိရိယာသော့;
        if(!အမှား)အမှား=assh_key_load(ပတ်ဝန်းကျင်အဓိပ္ပာယ်တန်ဖိုး,assh_context_keys(ပတ်ဝန်းကျင်အဓိပ္ပာယ်တန်ဖိုး),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&အဓိကသော့,sizeof(ကိရိယာသော့));
        if(အမှား){진단("SSH init error ",အမှား);assh_context_release(ပတ်ဝန်းကျင်အဓိပ္ပာယ်တန်ဖိုး);ပတ်ဝန်းကျင်အဓိပ္ပာယ်တန်ဖိုး=0;return -5;}
    }
    int ဆက်သွယ်ပေါက်တန်ဖိုး=ကွန်ရက်ပေါက်အဆုံးမှတ်ဖန်တီး(1);if(ဆက်သွယ်ပေါက်တန်ဖိုး<0)return ဆက်သွယ်ပေါက်တန်ဖိုး;통신주소재사용(ဆက်သွယ်ပေါက်တန်ဖိုး);
    int ရလဒ်=망주소묶기(ဆက်သွယ်ပေါက်တန်ဖိုး,0,22);if(!ရလဒ်)ရလဒ်=연결기다리기(ဆက်သွယ်ပေါက်တန်ဖိုး);
    if(ရလဒ်<0){ကွန်ရက်ပိတ်(ဆက်သွယ်ပေါက်တန်ဖိုး);return ရလဒ်;}듣는곳=ဆက်သွယ်ပေါက်တန်ဖိုး;return 0;
}
uintptr_t ဆားကစ်ပြားအဝေးထိန်းချုပ်(uintptr_t အမျိုးအစားတန်ဖိုး,uintptr_t လှုပ်ရှားမှု) {
    if(အမျိုးအစားတန်ဖိုး==1)return(uint32_t)ထိန်းချုပ်အဝေးမြင်ကွင်း(လှုပ်ရှားမှု);
    if(လှုပ်ရှားမှု==0){ချိတ်ဆက်မှုပိတ်();if(듣는곳>=0)ကွန်ရက်ပိတ်(듣는곳);듣는곳=-1;return 0;}
    if(လှုပ်ရှားမှု==1){시작오류=အမိန့်ဝင်းပြင်ဆင်();return(uint32_t)시작오류;}
    return(uint32_t)(듣는곳>=0?1:시작오류);
}
void အဝေးပြင်ဆင်(void){시작오류=အမိန့်ဝင်းပြင်ဆင်();ထိန်းချုပ်အဝေးမြင်ကွင်း(1);}
static int ကိုက်ညီစကားလုံး(const struct assh_cbuffer_s *ဒေတာ,const char *စကားလုံးစာသား) {
    size_t အလျား=strlen(စကားလုံးစာသား);return ဒေတာ->size==အလျား&&!memcmp(ဒေတာ->data,စကားလုံးစာသား,အလျား);
}
static int အဆုံးသုံးစက်တောင်းဆိုချက်(const struct assh_cbuffer_s *ဒေတာ) {
    if(ဒေတာ->size<24)return 0;
    const unsigned char *ဒေတာနေရာ=ဒေတာ->data;unsigned အလျား=assh_load_u32(ဒေတာနေရာ);
    if(အလျား>128||ဒေတာ->size<အလျား+24)return 0;
    unsigned နည်းစနစ်တန်ဖိုး=assh_load_u32(ဒေတာနေရာ+4+အလျား+16);
    return နည်းစနစ်တန်ဖိုး<=2048&&ဒေတာ->size==အလျား+24+နည်းစနစ်တန်ဖိုး;
}
static void ကိုင်တွယ်ရာတောင်းဆိုချက်(struct assh_event_request_s *ဖြစ်ရပ်) {
    if(!인증됨||ဖြစ်ရပ်->ch!=ချန်နယ်အချက်||!ချန်နယ်အချက်)return;
    if(ကိုက်ညီစကားလုံး(&ဖြစ်ရပ်->type,"pty-req")) {
        if(!셸시작됨&&အဆုံးသုံးစက်တောင်းဆိုချက်(&ဖြစ်ရပ်->rq_data))ဖြစ်ရပ်->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(ကိုက်ညီစကားလုံး(&ဖြစ်ရပ်->type,"window-change")) {
        if(셸시작됨&&ဖြစ်ရပ်->rq_data.size==16)ဖြစ်ရပ်->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!အမိန့်ဝင်းစောင့်နေ)return;
    const unsigned char *အမိန့်=0;unsigned အလျား=0;
    if(ကိုက်ညီစကားလုံး(&ဖြစ်ရပ်->type,"exec")) {
        if(ဖြစ်ရပ်->rq_data.size<4)return;
        အလျား=assh_load_u32(ဖြစ်ရပ်->rq_data.data);
        if(!အလျား||အလျား>2048||ဖြစ်ရပ်->rq_data.size!=အလျား+4)return;
        အမိန့်=ဖြစ်ရပ်->rq_data.data+4;
        for(unsigned အစဉ်အမှတ်=0;အစဉ်အမှတ်<အလျား;အစဉ်အမှတ်++)if(!အမိန့်[အစဉ်အမှတ်])return;
        အမိန့်အမျိုးပုံစံ=1;
    }else if(!ကိုက်ညီစကားလုံး(&ဖြစ်ရပ်->type,"shell")||ဖြစ်ရပ်->rq_data.size)return;
    if(sizeof(အဝင်စာကြောင်း)-အဝင်အရေအတွက်<အလျား+2)return;
    const unsigned char 지움=21,အဆုံး=13;
    원격입력넣기(&지움,1);if(အလျား)원격입력넣기(အမိန့်,အလျား);원격입력넣기(&အဆုံး,1);
    셸시작됨=1;ဖြစ်ရပ်->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!အမိန့်အမျိုးပုံစံ){const char *လမ်းညွှန်="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*လမ်းညွှန်)အဝေးအထွက်(*လမ်းညွှန်++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(တစ်ဖက်တန်ဖိုး<0){if(지금<재접속시각)return;တစ်ဖက်တန်ဖိုး=망연결받기(듣는곳);if(တစ်ဖက်တန်ဖိုး<0)return;
        ချိတ်ဆက်မှုအချိန်=지금;assh_status_t အမှား=assh_session_create(ပတ်ဝန်းကျင်အဓိပ္ပာယ်တန်ဖိုး,&ချိတ်ဆက်မှု);
        if(အမှား){ချိတ်ဆက်မှု=0;진단("SSH session error ",အမှား);ချိတ်ဆက်မှုပိတ်();return;}}
    if((!인증됨&&지금-ချိတ်ဆက်မှုအချိန်>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){ချိတ်ဆက်မှုပိတ်();return;}
    if(ချန်နယ်အချက်&&셸시작됨&&!닫을예정) {
        if(အထွက်အရေအတွက်){size_t ကိန်းတန်ဖိုး=sizeof(အထွက်စာကြောင်း)-အထွက်ဦးခေါင်း;if(ကိန်းတန်ဖိုး>အထွက်အရေအတွက်)ကိန်းတန်ဖိုး=အထွက်အရေအတွက်;if(ကိန်းတန်ဖိုး>2048)ကိန်းတန်ဖိုး=2048;
            assh_status_t အမှား=assh_channel_data(ချန်နယ်အချက်,အထွက်စာကြောင်း+အထွက်ဦးခေါင်း,&ကိန်းတန်ဖိုး);
            if(!အမှား){အထွက်ဦးခေါင်း=(အထွက်ဦးခေါင်း+ကိန်းတန်ဖိုး)%sizeof(အထွက်စာကြောင်း);အထွက်အရေအတွက်-=ကိန်းတန်ဖိုး;}
            else if(အမှား!=ASSH_NO_DATA){ချိတ်ဆက်မှုပိတ်();return;}
        }
        if(အဆုံးအခြေအနေ>=0&&!အထွက်အရေအတွက်){unsigned char အခြေအနေတန်ဖိုး[4];assh_store_u32(အခြေအနေတန်ဖိုး,(uint32_t)အဆုံးအခြေအနေ);
            if(assh_request(ချိတ်ဆက်မှု,ချန်နယ်အချက်,"exit-status",11,အခြေအနေတန်ဖိုး,4,0)||assh_channel_eof(ချန်နယ်အချက်)||assh_channel_close(ချန်နယ်အချက်)) {ချိတ်ဆက်မှုပိတ်();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned အစဉ်လိုက်တန်ဖိုး=0;အစဉ်လိုက်တန်ဖိုး<16;အစဉ်လိုက်တန်ဖိုး++) {
        struct assh_event_s ဖြစ်ရပ်;
        if(!assh_event_get(ချိတ်ဆက်မှု,&ဖြစ်ရပ်,지금/1000)){ချိတ်ဆက်မှုပိတ်();return;}
        assh_status_t အမှား=ASSH_OK;int ခဏနား=0,끊기=0;
        switch(ဖြစ်ရပ်.id) {
        case ASSH_EVENT_READ: {
            int ကိန်းတန်ဖိုး=통신읽기(တစ်ဖက်တန်ဖိုး,ဖြစ်ရပ်.transport.read.buf.data,ဖြစ်ရပ်.transport.read.buf.size);
            if(ကိန်းတန်ဖိုး>0)ဖြစ်ရပ်.transport.read.transferred=ကိန်းတန်ဖိုး;
            else if(ကိန်းတန်ဖိုး==-11)ခဏနား=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int ကိန်းတန်ဖိုး=통신쓰기(တစ်ဖက်တန်ဖိုး,ဖြစ်ရပ်.transport.write.buf.data,ဖြစ်ရပ်.transport.write.buf.size);
            if(ကိန်းတန်ဖိုး>0)ဖြစ်ရပ်.transport.write.transferred=ကိန်းတန်ဖိုး;
            else if(ကိန်းတန်ဖိုး==-11)ခဏနား=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ဖြစ်ရပ်.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ဖြစ်ရပ်.userauth_server.methods.retries>3)ဖြစ်ရပ်.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ဒေတာ=&ဖြစ်ရပ်.userauth_server.password;
            if(ကိုက်ညီစကားလုံး(&ဒေတာ->username,"user")&&ဒေတာ->password.size<=256&&!ဒေတာ->new_password.size) {
                unsigned char အကျဉ်းချုပ်တန်ဖိုး[32];အဝေးအကျဉ်းချုပ်(ဒေတာ->password.data,ဒေတာ->password.size,အကျဉ်းချုပ်တန်ဖိုး);
                unsigned ခြားနားချက်=0;for(unsigned အစဉ်အမှတ်=0;အစဉ်အမှတ်<32;အစဉ်အမှတ်++)ခြားနားချက်|=အကျဉ်းချုပ်တန်ဖိုး[အစဉ်အမှတ်]^အမိန့်ဝင်းစကားဝှက်အကျဉ်းချုပ်[အစဉ်အမှတ်];memset(အကျဉ်းချုပ်တန်ဖိုး,0,32);
                if(!ခြားနားချက်)ဒေတာ->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ဒေတာ=&ဖြစ်ရပ်.connection.channel_open;
            if(인증됨&&!ချန်နယ်အချက်&&အမိန့်ဝင်းစောင့်နေ&&ကိုက်ညီစကားလုံး(&ဒေတာ->type,"session")&&!ဒေတာ->rq_data.size) {
                ဒေတာ->reply=ASSH_CONNECTION_REPLY_SUCCESS;ဒေတာ->pkt_size=4096;
                ဒေတာ->win_size=-1;ချန်နယ်အချက်=ဒေတာ->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: ကိုင်တွယ်ရာတောင်းဆိုချက်(&ဖြစ်ရပ်.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ဒေတာ=&ဖြစ်ရပ်.connection.channel_data;
            if(!셸시작됨||ဒေတာ->ch!=ချန်နယ်အချက်||ဒေတာ->ext){끊기=1;break;}
            unsigned ကိန်းတန်ဖိုး=ဒေတာ->data.size;if(ကိန်းတန်ဖိုး>sizeof(အဝင်စာကြောင်း)-အဝင်အရေအတွက်)ကိန်းတန်ဖိုး=sizeof(အဝင်စာကြောင်း)-အဝင်အရေအတွက်;
            for(unsigned အစဉ်အမှတ်=0;အစဉ်အမှတ်<ကိန်းတန်ဖိုး;အစဉ်အမှတ်++)if(ဒေတာ->data.data[အစဉ်အမှတ်]==4){အဆုံးအခြေအနေ=0;ကိန်းတန်ဖိုး=အစဉ်အမှတ်;ဒေတာ->transferred=ဒေတာ->data.size;break;}
            원격입력넣기(ဒေတာ->data.data,ကိန်းတန်ဖိုး);if(!ဒေတာ->transferred)ဒေတာ->transferred=ကိန်းတန်ဖိုး;
            if(!ကိန်းတန်ဖိုး&&အဆုံးအခြေအနေ<0)ခဏနား=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: ချန်နယ်အချက်=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ဖြစ်ရပ်.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(ချိတ်ဆက်မှု,&ဖြစ်ရပ်,အမှား);
        if(끊기){ချိတ်ဆက်မှုပိတ်();return;}if(ခဏနား)return;
    }
}
