/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "kude_ixabiso.h"
#include "암호기반.h"
#include "Iprofayile.h"
#include "../Inethiwekhi_fumba/Inethiwekhi_fumba.h"
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
static struct assh_context_s *umxholo_ixabiso;
static struct assh_session_s *uqhagamshelo_e05f319b;
static struct assh_channel_s *ijelo_ufako_nkcukacha;
static int 듣는곳=-1,untanga_ixabiso=-1,인증됨,셸시작됨,umyalelo_uhlobo,phela_imo=-1,닫을예정,ukuvula_impazamo,셸대기중;
static uintptr_t 접속시각,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Igama_I_SMS,unsigned ixabiso) {
    while(*Igama_I_SMS)보드글자쓰기(*Igama_I_SMS++);
    char inani_ixabiso[12];unsigned 수=0;do{inani_ixabiso[수++]='0'+ixabiso%10;ixabiso/=10;}while(ixabiso);
    while(수)보드글자쓰기(inani_ixabiso[--수]);보드글자쓰기(10);
}
static assh_status_t lungisa_imemori(void *iingcombolo,void **idilesi,size_t Ubukhulu,enum assh_alloc_type_e 종류) {
    (void)iingcombolo;(void)종류;
    if(!Ubukhulu){vulela_kude(*idilesi);*idilesi=0;return ASSH_OK;}
    void *새주소=원격재할당(*idilesi,Ubukhulu);
    if(!새주소)return ASSH_ERR_MEM;*idilesi=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *iingcombolo,const struct assh_buffer_s *imbewu_ixabiso) {
    (void)iingcombolo;(void)imbewu_ixabiso;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *iingcombolo,uint8_t *결과,size_t ubude_ixabiso,uint_fast8_t 종류) {
    (void)iingcombolo;(void)종류;if(ubude_ixabiso>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,ubude_ixabiso)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *iingcombolo){(void)iingcombolo;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void vala_uqhagamshelo(void) {
    인증됨=셸시작됨=0;ijelo_ufako_nkcukacha=0;
    if(uqhagamshelo_e05f319b)assh_session_release(uqhagamshelo_e05f319b);uqhagamshelo_e05f319b=0;
    if(untanga_ixabiso>=0)vala_Inethiwekhi(untanga_ixabiso);untanga_ixabiso=-1;umyalelo_uhlobo=0;phela_imo=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *iingcombolo,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=iingcombolo[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int ikharakhtha_ixabiso=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return ikharakhtha_ixabiso;
}
void 원격출력(unsigned char ikharakhtha_ixabiso) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=ikharakhtha_ixabiso==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=ikharakhtha_ixabiso;이전출력=ikharakhtha_ixabiso;
}
uintptr_t 보드원격명령끝(uintptr_t imo_ixabiso){if(셸시작됨&&umyalelo_uhlobo)phela_imo=(int)imo_ixabiso;return 0;}
uintptr_t 보드원격대기(uintptr_t imo_ixabiso){셸대기중=imo_ixabiso!=0;return 0;}
static int lungisa_isiniki_myalelo(void) {
    if(듣는곳>=0)return 0;
    if(!umxholo_ixabiso){
        assh_status_t Impazamo=assh_context_create(&umxholo_ixabiso,ASSH_SERVER,lungisa_imemori,0,&난수기,0);
        if(Impazamo)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *imethodi_imo[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Impazamo=assh_algo_register(umxholo_ixabiso,ASSH_SAFETY_WEAK,imethodi_imo);
        if(!Impazamo)Impazamo=assh_service_register_va(umxholo_ixabiso,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=isixhobo_iqhosha;
        if(!Impazamo)Impazamo=assh_key_load(umxholo_ixabiso,assh_context_keys(umxholo_ixabiso),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(isixhobo_iqhosha));
        if(Impazamo){진단("SSH init error ",Impazamo);assh_context_release(umxholo_ixabiso);umxholo_ixabiso=0;return -5;}
    }
    int iphothi_ixabiso=통신끝점만들기(1);if(iphothi_ixabiso<0)return iphothi_ixabiso;통신주소재사용(iphothi_ixabiso);
    int 결과=망주소묶기(iphothi_ixabiso,0,22);if(!결과)결과=연결기다리기(iphothi_ixabiso);
    if(결과<0){vala_Inethiwekhi(iphothi_ixabiso);return 결과;}듣는곳=iphothi_ixabiso;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t Intshukumo) {
    if(종류==1)return(uint32_t)isilawuli_kude_bonisa(Intshukumo);
    if(Intshukumo==0){vala_uqhagamshelo();if(듣는곳>=0)vala_Inethiwekhi(듣는곳);듣는곳=-1;return 0;}
    if(Intshukumo==1){ukuvula_impazamo=lungisa_isiniki_myalelo();return(uint32_t)ukuvula_impazamo;}
    return(uint32_t)(듣는곳>=0?1:ukuvula_impazamo);
}
void lungisa_kude(void){ukuvula_impazamo=lungisa_isiniki_myalelo();isilawuli_kude_bonisa(1);}
static int 같은말(const struct assh_cbuffer_s *iingcombolo,const char *Igama_I_SMS) {
    size_t ubude_ixabiso=strlen(Igama_I_SMS);return iingcombolo->size==ubude_ixabiso&&!memcmp(iingcombolo->data,Igama_I_SMS,ubude_ixabiso);
}
static int 터미널요청(const struct assh_cbuffer_s *iingcombolo) {
    if(iingcombolo->size<24)return 0;
    const unsigned char *자료위치=iingcombolo->data;unsigned ubude_ixabiso=assh_load_u32(자료위치);
    if(ubude_ixabiso>128||iingcombolo->size<ubude_ixabiso+24)return 0;
    unsigned imo_ixabiso_a83655ea=assh_load_u32(자료위치+4+ubude_ixabiso+16);
    return imo_ixabiso_a83655ea<=2048&&iingcombolo->size==ubude_ixabiso+24+imo_ixabiso_a83655ea;
}
static void 요청처리(struct assh_event_request_s *umcimbi) {
    if(!인증됨||umcimbi->ch!=ijelo_ufako_nkcukacha||!ijelo_ufako_nkcukacha)return;
    if(같은말(&umcimbi->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&umcimbi->rq_data))umcimbi->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&umcimbi->type,"window-change")) {
        if(셸시작됨&&umcimbi->rq_data.size==16)umcimbi->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *Umyalelo=0;unsigned ubude_ixabiso=0;
    if(같은말(&umcimbi->type,"exec")) {
        if(umcimbi->rq_data.size<4)return;
        ubude_ixabiso=assh_load_u32(umcimbi->rq_data.data);
        if(!ubude_ixabiso||ubude_ixabiso>2048||umcimbi->rq_data.size!=ubude_ixabiso+4)return;
        Umyalelo=umcimbi->rq_data.data+4;
        for(unsigned 순번=0;순번<ubude_ixabiso;순번++)if(!Umyalelo[순번])return;
        umyalelo_uhlobo=1;
    }else if(!같은말(&umcimbi->type,"shell")||umcimbi->rq_data.size)return;
    if(sizeof(입력줄)-입력수<ubude_ixabiso+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(ubude_ixabiso)원격입력넣기(Umyalelo,ubude_ixabiso);원격입력넣기(&끝,1);
    셸시작됨=1;umcimbi->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!umyalelo_uhlobo){const char *i_README_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*i_README_eb81d7d9)원격출력(*i_README_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t 지금=보드밀리초();
    if(untanga_ixabiso<0){if(지금<재접속시각)return;untanga_ixabiso=망연결받기(듣는곳);if(untanga_ixabiso<0)return;
        접속시각=지금;assh_status_t Impazamo=assh_session_create(umxholo_ixabiso,&uqhagamshelo_e05f319b);
        if(Impazamo){uqhagamshelo_e05f319b=0;진단("SSH session error ",Impazamo);vala_uqhagamshelo();return;}}
    if((!인증됨&&지금-접속시각>30000)||닫을예정==2||(닫을예정&&지금>=닫는시각)){vala_uqhagamshelo();return;}
    if(ijelo_ufako_nkcukacha&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Impazamo=assh_channel_data(ijelo_ufako_nkcukacha,출력줄+출력앞,&수);
            if(!Impazamo){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Impazamo!=ASSH_NO_DATA){vala_uqhagamshelo();return;}
        }
        if(phela_imo>=0&&!출력수){unsigned char imo_ixabiso[4];assh_store_u32(imo_ixabiso,(uint32_t)phela_imo);
            if(assh_request(uqhagamshelo_e05f319b,ijelo_ufako_nkcukacha,"exit-status",11,imo_ixabiso,4,0)||assh_channel_eof(ijelo_ufako_nkcukacha)||assh_channel_close(ijelo_ufako_nkcukacha)) {vala_uqhagamshelo();return;}
            닫을예정=1;닫는시각=지금+3000;
        }
    }
    for(unsigned ULANDELELWANO_ixabiso=0;ULANDELELWANO_ixabiso<16;ULANDELELWANO_ixabiso++) {
        struct assh_event_s umcimbi;
        if(!assh_event_get(uqhagamshelo_e05f319b,&umcimbi,지금/1000)){vala_uqhagamshelo();return;}
        assh_status_t Impazamo=ASSH_OK;int 쉬기=0,끊기=0;
        switch(umcimbi.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(untanga_ixabiso,umcimbi.transport.read.buf.data,umcimbi.transport.read.buf.size);
            if(수>0)umcimbi.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(untanga_ixabiso,umcimbi.transport.write.buf.data,umcimbi.transport.write.buf.size);
            if(수>0)umcimbi.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            umcimbi.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(umcimbi.userauth_server.methods.retries>3)umcimbi.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *iingcombolo=&umcimbi.userauth_server.password;
            if(같은말(&iingcombolo->username,"user")&&iingcombolo->password.size<=256&&!iingcombolo->new_password.size) {
                unsigned char ushwankathelo_ixabiso[32];kude_ushwankathelo(iingcombolo->password.data,iingcombolo->password.size,ushwankathelo_ixabiso);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=ushwankathelo_ixabiso[순번]^isiniki_myalelo_iphaswedi_ushwankathelo[순번];memset(ushwankathelo_ixabiso,0,32);
                if(!차이)iingcombolo->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *iingcombolo=&umcimbi.connection.channel_open;
            if(인증됨&&!ijelo_ufako_nkcukacha&&셸대기중&&같은말(&iingcombolo->type,"session")&&!iingcombolo->rq_data.size) {
                iingcombolo->reply=ASSH_CONNECTION_REPLY_SUCCESS;iingcombolo->pkt_size=4096;
                iingcombolo->win_size=-1;ijelo_ufako_nkcukacha=iingcombolo->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&umcimbi.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *iingcombolo=&umcimbi.connection.channel_data;
            if(!셸시작됨||iingcombolo->ch!=ijelo_ufako_nkcukacha||iingcombolo->ext){끊기=1;break;}
            unsigned 수=iingcombolo->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(iingcombolo->data.data[순번]==4){phela_imo=0;수=순번;iingcombolo->transferred=iingcombolo->data.size;break;}
            원격입력넣기(iingcombolo->data.data,수);if(!iingcombolo->transferred)iingcombolo->transferred=수;
            if(!수&&phela_imo<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: ijelo_ufako_nkcukacha=0;셸시작됨=0;닫을예정=1;닫는시각=지금+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",umcimbi.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(uqhagamshelo_e05f319b,&umcimbi,Impazamo);
        if(끊기){vala_uqhagamshelo();return;}if(쉬기)return;
    }
}
