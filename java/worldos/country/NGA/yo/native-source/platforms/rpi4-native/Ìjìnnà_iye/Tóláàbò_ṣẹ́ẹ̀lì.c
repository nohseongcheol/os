/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "Ìjìnnà_iye.h"
#include "암호기반.h"
#include "Ìrísí_Olùlò.h"
#include "../Alásopọ̀_kójọ/Alásopọ̀_kójọ.h"
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
static struct assh_context_s *Ìṣètò_kíkà_iye;
static struct assh_session_s *Ìsomọ́_e05f319b;
static struct assh_channel_s *òpónà_ìgbéwọlé;
static int 듣는곳=-1,ọ̀gbà_iye=-1,인증됨,셸시작됨,àṣẹ_irú,parí_ipò=-1,닫을예정,ìbẹ̀rẹ̀_àṣìṣe,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Ọ̀rọ̀_SMS,unsigned iye) {
    while(*Ọ̀rọ̀_SMS)보드글자쓰기(*Ọ̀rọ̀_SMS++);
    char díjììtì_iye[12];unsigned 수=0;do{díjììtì_iye[수++]='0'+iye%10;iye/=10;}while(iye);
    while(수)보드글자쓰기(díjììtì_iye[--수]);보드글자쓰기(10);
}
static assh_status_t gbaradì_ibi_ìpamọ́(void *détà,void **àdírẹ́ẹ̀sì,size_t Ìwọ̀n,enum assh_alloc_type_e 종류) {
    (void)détà;(void)종류;
    if(!Ìwọ̀n){dápadà_Ìjìnnà(*àdírẹ́ẹ̀sì);*àdírẹ́ẹ̀sì=0;return ASSH_OK;}
    void *새주소=원격재할당(*àdírẹ́ẹ̀sì,Ìwọ̀n);
    if(!새주소)return ASSH_ERR_MEM;*àdírẹ́ẹ̀sì=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *détà,const struct assh_buffer_s *iye_ìbẹ̀rẹ̀_iye) {
    (void)détà;(void)iye_ìbẹ̀rẹ̀_iye;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *détà,uint8_t *결과,size_t gígùn_iye,uint_fast8_t 종류) {
    (void)détà;(void)종류;if(gígùn_iye>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,gígùn_iye)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *détà){(void)détà;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void pa_dé_Ìsomọ́(void) {
    인증됨=셸시작됨=0;òpónà_ìgbéwọlé=0;
    if(Ìsomọ́_e05f319b)assh_session_release(Ìsomọ́_e05f319b);Ìsomọ́_e05f319b=0;
    if(ọ̀gbà_iye>=0)pa_dé_Alásopọ̀(ọ̀gbà_iye);ọ̀gbà_iye=-1;àṣẹ_irú=0;parí_ipò=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *détà,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=détà[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int ẹyọ_ọ̀rọ̀_iye=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return ẹyọ_ọ̀rọ̀_iye;
}
void 원격출력(unsigned char ẹyọ_ọ̀rọ̀_iye) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=ẹyọ_ọ̀rọ̀_iye==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=ẹyọ_ọ̀rọ̀_iye;이전출력=ẹyọ_ọ̀rọ̀_iye;
}
uintptr_t 보드원격명령끝(uintptr_t ipò_iye){if(셸시작됨&&àṣẹ_irú)parí_ipò=(int)ipò_iye;return 0;}
uintptr_t 보드원격대기(uintptr_t ipò_iye){셸대기중=ipò_iye!=0;return 0;}
static int gbaradì_ṣẹ́ẹ̀lì(void) {
    if(듣는곳>=0)return 0;
    if(!Ìṣètò_kíkà_iye){
        assh_status_t àṣìṣe=assh_context_create(&Ìṣètò_kíkà_iye,ASSH_SERVER,gbaradì_ibi_ìpamọ́,0,&난수기,0);
        if(àṣìṣe)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *ìlànà_móòdù[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        àṣìṣe=assh_algo_register(Ìṣètò_kíkà_iye,ASSH_SAFETY_WEAK,ìlànà_móòdù);
        if(!àṣìṣe)àṣìṣe=assh_service_register_va(Ìṣètò_kíkà_iye,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=ohun_èlò_bọ́tìnnì;
        if(!àṣìṣe)àṣìṣe=assh_key_load(Ìṣètò_kíkà_iye,assh_context_keys(Ìṣètò_kíkà_iye),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(ohun_èlò_bọ́tìnnì));
        if(àṣìṣe){진단("SSH init error ",àṣìṣe);assh_context_release(Ìṣètò_kíkà_iye);Ìṣètò_kíkà_iye=0;return -5;}
    }
    int ojú_iye=통신끝점만들기(1);if(ojú_iye<0)return ojú_iye;통신주소재사용(ojú_iye);
    int 결과=망주소묶기(ojú_iye,0,22);if(!결과)결과=연결기다리기(ojú_iye);
    if(결과<0){pa_dé_Alásopọ̀(ojú_iye);return 결과;}듣는곳=ojú_iye;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t ìṣe) {
    if(종류==1)return(uint32_t)ìdarí_Ìjìnnà_ṣàfihàn(ìṣe);
    if(ìṣe==0){pa_dé_Ìsomọ́();if(듣는곳>=0)pa_dé_Alásopọ̀(듣는곳);듣는곳=-1;return 0;}
    if(ìṣe==1){ìbẹ̀rẹ̀_àṣìṣe=gbaradì_ṣẹ́ẹ̀lì();return(uint32_t)ìbẹ̀rẹ̀_àṣìṣe;}
    return(uint32_t)(듣는곳>=0?1:ìbẹ̀rẹ̀_àṣìṣe);
}
void gbaradì_Ìjìnnà(void){ìbẹ̀rẹ̀_àṣìṣe=gbaradì_ṣẹ́ẹ̀lì();ìdarí_Ìjìnnà_ṣàfihàn(1);}
static int 같은말(const struct assh_cbuffer_s *détà,const char *Ọ̀rọ̀_SMS) {
    size_t gígùn_iye=strlen(Ọ̀rọ̀_SMS);return détà->size==gígùn_iye&&!memcmp(détà->data,Ọ̀rọ̀_SMS,gígùn_iye);
}
static int 터미널요청(const struct assh_cbuffer_s *détà) {
    if(détà->size<24)return 0;
    const unsigned char *자료위치=détà->data;unsigned gígùn_iye=assh_load_u32(자료위치);
    if(gígùn_iye>128||détà->size<gígùn_iye+24)return 0;
    unsigned móòdù_iye=assh_load_u32(자료위치+4+gígùn_iye+16);
    return móòdù_iye<=2048&&détà->size==gígùn_iye+24+móòdù_iye;
}
static void 요청처리(struct assh_event_request_s *ìgbéṣẹ̀) {
    if(!인증됨||ìgbéṣẹ̀->ch!=òpónà_ìgbéwọlé||!òpónà_ìgbéwọlé)return;
    if(같은말(&ìgbéṣẹ̀->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&ìgbéṣẹ̀->rq_data))ìgbéṣẹ̀->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ìgbéṣẹ̀->type,"window-change")) {
        if(셸시작됨&&ìgbéṣẹ̀->rq_data.size==16)ìgbéṣẹ̀->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *Àṣẹ=0;unsigned gígùn_iye=0;
    if(같은말(&ìgbéṣẹ̀->type,"exec")) {
        if(ìgbéṣẹ̀->rq_data.size<4)return;
        gígùn_iye=assh_load_u32(ìgbéṣẹ̀->rq_data.data);
        if(!gígùn_iye||gígùn_iye>2048||ìgbéṣẹ̀->rq_data.size!=gígùn_iye+4)return;
        Àṣẹ=ìgbéṣẹ̀->rq_data.data+4;
        for(unsigned 순번=0;순번<gígùn_iye;순번++)if(!Àṣẹ[순번])return;
        àṣẹ_irú=1;
    }else if(!같은말(&ìgbéṣẹ̀->type,"shell")||ìgbéṣẹ̀->rq_data.size)return;
    if(sizeof(입력줄)-입력수<gígùn_iye+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(gígùn_iye)원격입력넣기(Àṣẹ,gígùn_iye);원격입력넣기(&끝,1);
    셸시작됨=1;ìgbéṣẹ̀->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!àṣẹ_irú){const char *KÀ_MÍ_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*KÀ_MÍ_eb81d7d9)원격출력(*KÀ_MÍ_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(ọ̀gbà_iye<0){if(지금<재접속시각)return;ọ̀gbà_iye=망연결받기(듣는곳);if(ọ̀gbà_iye<0)return;
        접속시각=지금;assh_status_t àṣìṣe=assh_session_create(Ìṣètò_kíkà_iye,&Ìsomọ́_e05f319b);
        if(àṣìṣe){Ìsomọ́_e05f319b=0;진단("SSH session error ",àṣìṣe);pa_dé_Ìsomọ́();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){pa_dé_Ìsomọ́();return;}
    if(òpónà_ìgbéwọlé&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t àṣìṣe=assh_channel_data(òpónà_ìgbéwọlé,출력줄+출력앞,&수);
            if(!àṣìṣe){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(àṣìṣe!=ASSH_NO_DATA){pa_dé_Ìsomọ́();return;}
        }
        if(parí_ipò>=0&&!출력수){unsigned char ipò_iye[4];assh_store_u32(ipò_iye,(uint32_t)parí_ipò);
            if(assh_request(Ìsomọ́_e05f319b,òpónà_ìgbéwọlé,"exit-status",11,ipò_iye,4,0)||assh_channel_eof(òpónà_ìgbéwọlé)||assh_channel_close(òpónà_ìgbéwọlé)) {pa_dé_Ìsomọ́();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned ÀTẸ̀LÉRA_iye=0;ÀTẸ̀LÉRA_iye<16;ÀTẸ̀LÉRA_iye++) {
        struct assh_event_s ìgbéṣẹ̀;
        if(!assh_event_get(Ìsomọ́_e05f319b,&ìgbéṣẹ̀,지금/1000)){pa_dé_Ìsomọ́();return;}
        assh_status_t àṣìṣe=ASSH_OK;int 쉬기=0,끊기=0;
        switch(ìgbéṣẹ̀.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(ọ̀gbà_iye,ìgbéṣẹ̀.transport.read.buf.data,ìgbéṣẹ̀.transport.read.buf.size);
            if(수>0)ìgbéṣẹ̀.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(ọ̀gbà_iye,ìgbéṣẹ̀.transport.write.buf.data,ìgbéṣẹ̀.transport.write.buf.size);
            if(수>0)ìgbéṣẹ̀.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ìgbéṣẹ̀.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ìgbéṣẹ̀.userauth_server.methods.retries>3)ìgbéṣẹ̀.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *détà=&ìgbéṣẹ̀.userauth_server.password;
            if(같은말(&détà->username,"user")&&détà->password.size<=256&&!détà->new_password.size) {
                unsigned char ìṣoníṣókí_iye[32];Ìjìnnà_ìṣoníṣókí(détà->password.data,détà->password.size,ìṣoníṣókí_iye);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=ìṣoníṣókí_iye[순번]^ṣẹ́ẹ̀lì_ọ̀rọ̀_aṣínà_ìṣoníṣókí[순번];memset(ìṣoníṣókí_iye,0,32);
                if(!차이)détà->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *détà=&ìgbéṣẹ̀.connection.channel_open;
            if(인증됨&&!òpónà_ìgbéwọlé&&셸대기중&&같은말(&détà->type,"session")&&!détà->rq_data.size) {
                détà->reply=ASSH_CONNECTION_REPLY_SUCCESS;détà->pkt_size=4096;
                détà->win_size=-1;òpónà_ìgbéwọlé=détà->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&ìgbéṣẹ̀.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *détà=&ìgbéṣẹ̀.connection.channel_data;
            if(!셸시작됨||détà->ch!=òpónà_ìgbéwọlé||détà->ext){끊기=1;break;}
            unsigned 수=détà->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(détà->data.data[순번]==4){parí_ipò=0;수=순번;détà->transferred=détà->data.size;break;}
            원격입력넣기(détà->data.data,수);if(!détà->transferred)détà->transferred=수;
            if(!수&&parí_ipò<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: òpónà_ìgbéwọlé=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ìgbéṣẹ̀.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(Ìsomọ́_e05f319b,&ìgbéṣẹ̀,àṣìṣe);
        if(끊기){pa_dé_Ìsomọ́();return;}if(쉬기)return;
    }
}
