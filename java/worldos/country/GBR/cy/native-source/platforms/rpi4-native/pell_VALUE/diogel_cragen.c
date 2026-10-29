/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "pell_VALUE.h"
#include "암호기반.h"
#include "Proffil.h"
#include "../Rhwydwaith_pentwr/Rhwydwaith_pentwr.h"
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
static struct assh_context_s *Cyd_destun_VALUE;
static struct assh_session_s *cyswllt_e05f319b;
static struct assh_channel_s *sianel_cofnod;
static int 듣는곳=-1,cymar_VALUE=-1,인증됨,셸시작됨,gorchymyn_TYPE,gorffen_cyflwr=-1,닫을예정,bwtio_gwall,cragen_Wrthi_n_aros;
static uintptr_t cyswllt_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char digid_VALUE[12];unsigned 수=0;do{digid_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(digid_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Paratoi_Cof(void *data,void **ADDRESS,size_t Maint,enum assh_alloc_type_e 종류) {
    (void)data;(void)종류;
    if(!Maint){rhyddhau_pell(*ADDRESS);*ADDRESS=0;return ASSH_OK;}
    void *새주소=원격재할당(*ADDRESS,Maint);
    if(!새주소)return ASSH_ERR_MEM;*ADDRESS=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *data,const struct assh_buffer_s *dosbarthiad_VALUE) {
    (void)data;(void)dosbarthiad_VALUE;unsigned char 시험[32];int mesur=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return mesur?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *data,uint8_t *mesur,size_t hyd_VALUE,uint_fast8_t 종류) {
    (void)data;(void)종류;if(hyd_VALUE>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(mesur,hyd_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *data){(void)data;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void cau_cyswllt(void) {
    인증됨=셸시작됨=0;sianel_cofnod=0;
    if(cyswllt_e05f319b)assh_session_release(cyswllt_e05f319b);cyswllt_e05f319b=0;
    if(cymar_VALUE>=0)cau_Rhwydwaith(cymar_VALUE);cymar_VALUE=-1;gorchymyn_TYPE=0;gorffen_cyflwr=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *data,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=data[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int nod_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return nod_VALUE;
}
void 원격출력(unsigned char nod_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=nod_VALUE==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=nod_VALUE;이전출력=nod_VALUE;
}
uintptr_t bwrdd_gorffen_pell_gorchymyn(uintptr_t cyflwr_VALUE){if(셸시작됨&&gorchymyn_TYPE)gorffen_cyflwr=(int)cyflwr_VALUE;return 0;}
uintptr_t bwrdd_pell_aros(uintptr_t cyflwr_VALUE){cragen_Wrthi_n_aros=cyflwr_VALUE!=0;return 0;}
static int Paratoi_cragen(void) {
    if(듣는곳>=0)return 0;
    if(!Cyd_destun_VALUE){
        assh_status_t Gwall=assh_context_create(&Cyd_destun_VALUE,ASSH_SERVER,Paratoi_Cof,0,&난수기,0);
        if(Gwall)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *dull_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Gwall=assh_algo_register(Cyd_destun_VALUE,ASSH_SAFETY_WEAK,dull_MODE);
        if(!Gwall)Gwall=assh_service_register_va(Cyd_destun_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=dyfais_bysell;
        if(!Gwall)Gwall=assh_key_load(Cyd_destun_VALUE,assh_context_keys(Cyd_destun_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(dyfais_bysell));
        if(Gwall){진단("SSH init error ",Gwall);assh_context_release(Cyd_destun_VALUE);Cyd_destun_VALUE=0;return -5;}
    }
    int porth_VALUE=통신끝점만들기(1);if(porth_VALUE<0)return porth_VALUE;통신주소재사용(porth_VALUE);
    int mesur=망주소묶기(porth_VALUE,0,22);if(!mesur)mesur=연결기다리기(porth_VALUE);
    if(mesur<0){cau_Rhwydwaith(porth_VALUE);return mesur;}듣는곳=porth_VALUE;return 0;
}
uintptr_t bwrdd_cysgodi(uintptr_t 종류,uintptr_t Gweithrediad) {
    if(종류==1)return(uint32_t)rheoli_pell_dangos(Gweithrediad);
    if(Gweithrediad==0){cau_cyswllt();if(듣는곳>=0)cau_Rhwydwaith(듣는곳);듣는곳=-1;return 0;}
    if(Gweithrediad==1){bwtio_gwall=Paratoi_cragen();return(uint32_t)bwtio_gwall;}
    return(uint32_t)(듣는곳>=0?1:bwtio_gwall);
}
void Paratoi_pell(void){bwtio_gwall=Paratoi_cragen();rheoli_pell_dangos(1);}
static int 같은말(const struct assh_cbuffer_s *data,const char *Word_SMS) {
    size_t hyd_VALUE=strlen(Word_SMS);return data->size==hyd_VALUE&&!memcmp(data->data,Word_SMS,hyd_VALUE);
}
static int Terfynell_cais_HTTP(const struct assh_cbuffer_s *data) {
    if(data->size<24)return 0;
    const unsigned char *data_safle=data->data;unsigned hyd_VALUE=assh_load_u32(data_safle);
    if(hyd_VALUE>128||data->size<hyd_VALUE+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(data_safle+4+hyd_VALUE+16);
    return MODE_VALUE<=2048&&data->size==hyd_VALUE+24+MODE_VALUE;
}
static void dolen_cais_HTTP(struct assh_event_request_s *digwyddiad) {
    if(!인증됨||digwyddiad->ch!=sianel_cofnod||!sianel_cofnod)return;
    if(같은말(&digwyddiad->type,"pty-req")) {
        if(!셸시작됨&&Terfynell_cais_HTTP(&digwyddiad->rq_data))digwyddiad->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&digwyddiad->type,"window-change")) {
        if(셸시작됨&&digwyddiad->rq_data.size==16)digwyddiad->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!cragen_Wrthi_n_aros)return;
    const unsigned char *Gorchymyn=0;unsigned hyd_VALUE=0;
    if(같은말(&digwyddiad->type,"exec")) {
        if(digwyddiad->rq_data.size<4)return;
        hyd_VALUE=assh_load_u32(digwyddiad->rq_data.data);
        if(!hyd_VALUE||hyd_VALUE>2048||digwyddiad->rq_data.size!=hyd_VALUE+4)return;
        Gorchymyn=digwyddiad->rq_data.data+4;
        for(unsigned 순번=0;순번<hyd_VALUE;순번++)if(!Gorchymyn[순번])return;
        gorchymyn_TYPE=1;
    }else if(!같은말(&digwyddiad->type,"shell")||digwyddiad->rq_data.size)return;
    if(sizeof(입력줄)-입력수<hyd_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(hyd_VALUE)원격입력넣기(Gorchymyn,hyd_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;digwyddiad->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!gorchymyn_TYPE){const char *GWYBODAETH_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*GWYBODAETH_eb81d7d9)원격출력(*GWYBODAETH_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(cymar_VALUE<0){if(NOW_VALUE<재접속시각)return;cymar_VALUE=망연결받기(듣는곳);if(cymar_VALUE<0)return;
        cyswllt_TIME=NOW_VALUE;assh_status_t Gwall=assh_session_create(Cyd_destun_VALUE,&cyswllt_e05f319b);
        if(Gwall){cyswllt_e05f319b=0;진단("SSH session error ",Gwall);cau_cyswllt();return;}}
    if((!인증됨&&NOW_VALUE-cyswllt_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){cau_cyswllt();return;}
    if(sianel_cofnod&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Gwall=assh_channel_data(sianel_cofnod,출력줄+출력앞,&수);
            if(!Gwall){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Gwall!=ASSH_NO_DATA){cau_cyswllt();return;}
        }
        if(gorffen_cyflwr>=0&&!출력수){unsigned char cyflwr_VALUE[4];assh_store_u32(cyflwr_VALUE,(uint32_t)gorffen_cyflwr);
            if(assh_request(cyswllt_e05f319b,sianel_cofnod,"exit-status",11,cyflwr_VALUE,4,0)||assh_channel_eof(sianel_cofnod)||assh_channel_close(sianel_cofnod)) {cau_cyswllt();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s digwyddiad;
        if(!assh_event_get(cyswllt_e05f319b,&digwyddiad,NOW_VALUE/1000)){cau_cyswllt();return;}
        assh_status_t Gwall=ASSH_OK;int 쉬기=0,끊기=0;
        switch(digwyddiad.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(cymar_VALUE,digwyddiad.transport.read.buf.data,digwyddiad.transport.read.buf.size);
            if(수>0)digwyddiad.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(cymar_VALUE,digwyddiad.transport.write.buf.data,digwyddiad.transport.write.buf.size);
            if(수>0)digwyddiad.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            digwyddiad.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(digwyddiad.userauth_server.methods.retries>3)digwyddiad.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *data=&digwyddiad.userauth_server.password;
            if(같은말(&data->username,"user")&&data->password.size<=256&&!data->new_password.size) {
                unsigned char crynodeb_VALUE[32];pell_crynodeb(data->password.data,data->password.size,crynodeb_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=crynodeb_VALUE[순번]^cragen_cyfrinair_crynodeb[순번];memset(crynodeb_VALUE,0,32);
                if(!차이)data->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *data=&digwyddiad.connection.channel_open;
            if(인증됨&&!sianel_cofnod&&cragen_Wrthi_n_aros&&같은말(&data->type,"session")&&!data->rq_data.size) {
                data->reply=ASSH_CONNECTION_REPLY_SUCCESS;data->pkt_size=4096;
                data->win_size=-1;sianel_cofnod=data->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: dolen_cais_HTTP(&digwyddiad.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *data=&digwyddiad.connection.channel_data;
            if(!셸시작됨||data->ch!=sianel_cofnod||data->ext){끊기=1;break;}
            unsigned 수=data->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(data->data.data[순번]==4){gorffen_cyflwr=0;수=순번;data->transferred=data->data.size;break;}
            원격입력넣기(data->data.data,수);if(!data->transferred)data->transferred=수;
            if(!수&&gorffen_cyflwr<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: sianel_cofnod=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",digwyddiad.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(cyswllt_e05f319b,&digwyddiad,Gwall);
        if(끊기){cau_cyswllt();return;}if(쉬기)return;
    }
}
