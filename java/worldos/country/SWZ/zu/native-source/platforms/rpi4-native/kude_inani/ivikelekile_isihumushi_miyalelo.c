/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "kude_inani.h"
#include "암호기반.h"
#include "Iphrofayili.h"
#include "../iNethiwekhi_Isitaki/iNethiwekhi_Isitaki.h"
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
static struct assh_context_s *Umongo_inani;
static struct assh_session_s *uxhumano_e05f319b;
static struct assh_channel_s *umgudu_okufakwayo;
static int 듣는곳=-1,untanga_inani=-1,인증됨,셸시작됨,umyalo_thayipha,yekisa_isimo=-1,닫을예정,ukuvula_iphutha,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Amagama_I_SMS,unsigned inani) {
    while(*Amagama_I_SMS)보드글자쓰기(*Amagama_I_SMS++);
    char idijithi_inani[12];unsigned 수=0;do{idijithi_inani[수++]='0'+inani%10;inani/=10;}while(inani);
    while(수)보드글자쓰기(idijithi_inani[--수]);보드글자쓰기(10);
}
static assh_status_t Hlela_inkumbulo(void *imininingwane,void **ikheli,size_t Ubungako,enum assh_alloc_type_e 종류) {
    (void)imininingwane;(void)종류;
    if(!Ubungako){khulula_kude(*ikheli);*ikheli=0;return ASSH_OK;}
    void *새주소=원격재할당(*ikheli,Ubungako);
    if(!새주소)return ASSH_ERR_MEM;*ikheli=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *imininingwane,const struct assh_buffer_s *isidi_inani) {
    (void)imininingwane;(void)isidi_inani;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *imininingwane,uint8_t *결과,size_t ubude_inani,uint_fast8_t 종류) {
    (void)imininingwane;(void)종류;if(ubude_inani>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,ubude_inani)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *imininingwane){(void)imininingwane;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void vala_uxhumano(void) {
    인증됨=셸시작됨=0;umgudu_okufakwayo=0;
    if(uxhumano_e05f319b)assh_session_release(uxhumano_e05f319b);uxhumano_e05f319b=0;
    if(untanga_inani>=0)vala_iNethiwekhi(untanga_inani);untanga_inani=-1;umyalo_thayipha=0;yekisa_isimo=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *imininingwane,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=imininingwane[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int uhlamvusimo_inani=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return uhlamvusimo_inani;
}
void 원격출력(unsigned char uhlamvusimo_inani) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=uhlamvusimo_inani==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=uhlamvusimo_inani;이전출력=uhlamvusimo_inani;
}
uintptr_t 보드원격명령끝(uintptr_t isimo_inani){if(셸시작됨&&umyalo_thayipha)yekisa_isimo=(int)isimo_inani;return 0;}
uintptr_t 보드원격대기(uintptr_t isimo_inani){셸대기중=isimo_inani!=0;return 0;}
static int Hlela_isihumushi_miyalelo(void) {
    if(듣는곳>=0)return 0;
    if(!Umongo_inani){
        assh_status_t Iphutha=assh_context_create(&Umongo_inani,ASSH_SERVER,Hlela_inkumbulo,0,&난수기,0);
        if(Iphutha)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *indlela_inqubo[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Iphutha=assh_algo_register(Umongo_inani,ASSH_SAFETY_WEAK,indlela_inqubo);
        if(!Iphutha)Iphutha=assh_service_register_va(Umongo_inani,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=idivayisi_inkomba;
        if(!Iphutha)Iphutha=assh_key_load(Umongo_inani,assh_context_keys(Umongo_inani),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(idivayisi_inkomba));
        if(Iphutha){진단("SSH init error ",Iphutha);assh_context_release(Umongo_inani);Umongo_inani=0;return -5;}
    }
    int intuba_inani=통신끝점만들기(1);if(intuba_inani<0)return intuba_inani;통신주소재사용(intuba_inani);
    int 결과=망주소묶기(intuba_inani,0,22);if(!결과)결과=연결기다리기(intuba_inani);
    if(결과<0){vala_iNethiwekhi(intuba_inani);return 결과;}듣는곳=intuba_inani;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t Isenzo) {
    if(종류==1)return(uint32_t)isilawuli_kude_bonisa(Isenzo);
    if(Isenzo==0){vala_uxhumano();if(듣는곳>=0)vala_iNethiwekhi(듣는곳);듣는곳=-1;return 0;}
    if(Isenzo==1){ukuvula_iphutha=Hlela_isihumushi_miyalelo();return(uint32_t)ukuvula_iphutha;}
    return(uint32_t)(듣는곳>=0?1:ukuvula_iphutha);
}
void Hlela_kude(void){ukuvula_iphutha=Hlela_isihumushi_miyalelo();isilawuli_kude_bonisa(1);}
static int 같은말(const struct assh_cbuffer_s *imininingwane,const char *Amagama_I_SMS) {
    size_t ubude_inani=strlen(Amagama_I_SMS);return imininingwane->size==ubude_inani&&!memcmp(imininingwane->data,Amagama_I_SMS,ubude_inani);
}
static int 터미널요청(const struct assh_cbuffer_s *imininingwane) {
    if(imininingwane->size<24)return 0;
    const unsigned char *자료위치=imininingwane->data;unsigned ubude_inani=assh_load_u32(자료위치);
    if(ubude_inani>128||imininingwane->size<ubude_inani+24)return 0;
    unsigned inqubo_inani=assh_load_u32(자료위치+4+ubude_inani+16);
    return inqubo_inani<=2048&&imininingwane->size==ubude_inani+24+inqubo_inani;
}
static void 요청처리(struct assh_event_request_s *isigameko) {
    if(!인증됨||isigameko->ch!=umgudu_okufakwayo||!umgudu_okufakwayo)return;
    if(같은말(&isigameko->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&isigameko->rq_data))isigameko->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&isigameko->type,"window-change")) {
        if(셸시작됨&&isigameko->rq_data.size==16)isigameko->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *Umlayelo=0;unsigned ubude_inani=0;
    if(같은말(&isigameko->type,"exec")) {
        if(isigameko->rq_data.size<4)return;
        ubude_inani=assh_load_u32(isigameko->rq_data.data);
        if(!ubude_inani||ubude_inani>2048||isigameko->rq_data.size!=ubude_inani+4)return;
        Umlayelo=isigameko->rq_data.data+4;
        for(unsigned 순번=0;순번<ubude_inani;순번++)if(!Umlayelo[순번])return;
        umyalo_thayipha=1;
    }else if(!같은말(&isigameko->type,"shell")||isigameko->rq_data.size)return;
    if(sizeof(입력줄)-입력수<ubude_inani+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(ubude_inani)원격입력넣기(Umlayelo,ubude_inani);원격입력넣기(&끝,1);
    셸시작됨=1;isigameko->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!umyalo_thayipha){const char *NGIFUNDE_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*NGIFUNDE_eb81d7d9)원격출력(*NGIFUNDE_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(untanga_inani<0){if(지금<재접속시각)return;untanga_inani=망연결받기(듣는곳);if(untanga_inani<0)return;
        접속시각=지금;assh_status_t Iphutha=assh_session_create(Umongo_inani,&uxhumano_e05f319b);
        if(Iphutha){uxhumano_e05f319b=0;진단("SSH session error ",Iphutha);vala_uxhumano();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){vala_uxhumano();return;}
    if(umgudu_okufakwayo&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Iphutha=assh_channel_data(umgudu_okufakwayo,출력줄+출력앞,&수);
            if(!Iphutha){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Iphutha!=ASSH_NO_DATA){vala_uxhumano();return;}
        }
        if(yekisa_isimo>=0&&!출력수){unsigned char isimo_inani[4];assh_store_u32(isimo_inani,(uint32_t)yekisa_isimo);
            if(assh_request(uxhumano_e05f319b,umgudu_okufakwayo,"exit-status",11,isimo_inani,4,0)||assh_channel_eof(umgudu_okufakwayo)||assh_channel_close(umgudu_okufakwayo)) {vala_uxhumano();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned UKULANDELANA_inani=0;UKULANDELANA_inani<16;UKULANDELANA_inani++) {
        struct assh_event_s isigameko;
        if(!assh_event_get(uxhumano_e05f319b,&isigameko,지금/1000)){vala_uxhumano();return;}
        assh_status_t Iphutha=ASSH_OK;int 쉬기=0,끊기=0;
        switch(isigameko.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(untanga_inani,isigameko.transport.read.buf.data,isigameko.transport.read.buf.size);
            if(수>0)isigameko.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(untanga_inani,isigameko.transport.write.buf.data,isigameko.transport.write.buf.size);
            if(수>0)isigameko.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            isigameko.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(isigameko.userauth_server.methods.retries>3)isigameko.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *imininingwane=&isigameko.userauth_server.password;
            if(같은말(&imininingwane->username,"user")&&imininingwane->password.size<=256&&!imininingwane->new_password.size) {
                unsigned char isifinyezo_inani[32];kude_isifinyezo(imininingwane->password.data,imininingwane->password.size,isifinyezo_inani);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=isifinyezo_inani[순번]^isihumushi_miyalelo_iphasiwedi_isifinyezo[순번];memset(isifinyezo_inani,0,32);
                if(!차이)imininingwane->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *imininingwane=&isigameko.connection.channel_open;
            if(인증됨&&!umgudu_okufakwayo&&셸대기중&&같은말(&imininingwane->type,"session")&&!imininingwane->rq_data.size) {
                imininingwane->reply=ASSH_CONNECTION_REPLY_SUCCESS;imininingwane->pkt_size=4096;
                imininingwane->win_size=-1;umgudu_okufakwayo=imininingwane->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&isigameko.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *imininingwane=&isigameko.connection.channel_data;
            if(!셸시작됨||imininingwane->ch!=umgudu_okufakwayo||imininingwane->ext){끊기=1;break;}
            unsigned 수=imininingwane->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(imininingwane->data.data[순번]==4){yekisa_isimo=0;수=순번;imininingwane->transferred=imininingwane->data.size;break;}
            원격입력넣기(imininingwane->data.data,수);if(!imininingwane->transferred)imininingwane->transferred=수;
            if(!수&&yekisa_isimo<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: umgudu_okufakwayo=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",isigameko.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(uxhumano_e05f319b,&isigameko,Iphutha);
        if(끊기){vala_uxhumano();return;}if(쉬기)return;
    }
}
