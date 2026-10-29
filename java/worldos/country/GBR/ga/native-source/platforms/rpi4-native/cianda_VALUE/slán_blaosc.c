/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "cianda_VALUE.h"
#include "암호기반.h"
#include "Próifíl.h"
#include "../Líonra_Cruach/Líonra_Cruach.h"
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
static struct assh_context_s *Comhthéacs_VALUE;
static struct assh_session_s *nasc_e05f319b;
static struct assh_channel_s *cainéal_iontráil;
static int 듣는곳=-1,piara_VALUE=-1,인증됨,셸시작됨,ordú_TYPE,cuir_deireadh_le_staid=-1,닫을예정,tosú_earráid,셸대기중;
static uintptr_t nasc_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char digit_VALUE[12];unsigned 수=0;do{digit_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(digit_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Ullmhaigh_Cuimhne(void *sonraí,void **ADDRESS,size_t Méid,enum assh_alloc_type_e 종류) {
    (void)sonraí;(void)종류;
    if(!Méid){leagan_cianda(*ADDRESS);*ADDRESS=0;return ASSH_OK;}
    void *새주소=원격재할당(*ADDRESS,Méid);
    if(!새주소)return ASSH_ERR_MEM;*ADDRESS=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *sonraí,const struct assh_buffer_s *síol_VALUE) {
    (void)sonraí;(void)síol_VALUE;unsigned char 시험[32];int tomhas=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return tomhas?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *sonraí,uint8_t *tomhas,size_t fad_VALUE,uint_fast8_t 종류) {
    (void)sonraí;(void)종류;if(fad_VALUE>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(tomhas,fad_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *sonraí){(void)sonraí;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void dún_nasc(void) {
    인증됨=셸시작됨=0;cainéal_iontráil=0;
    if(nasc_e05f319b)assh_session_release(nasc_e05f319b);nasc_e05f319b=0;
    if(piara_VALUE>=0)dún_Líonra(piara_VALUE);piara_VALUE=-1;ordú_TYPE=0;cuir_deireadh_le_staid=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *sonraí,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=sonraí[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int carachtar_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return carachtar_VALUE;
}
void 원격출력(unsigned char carachtar_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=carachtar_VALUE==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=carachtar_VALUE;이전출력=carachtar_VALUE;
}
uintptr_t clár_cuir_deireadh_le_cianda_ordú(uintptr_t staid_VALUE){if(셸시작됨&&ordú_TYPE)cuir_deireadh_le_staid=(int)staid_VALUE;return 0;}
uintptr_t 보드원격대기(uintptr_t staid_VALUE){셸대기중=staid_VALUE!=0;return 0;}
static int Ullmhaigh_blaosc(void) {
    if(듣는곳>=0)return 0;
    if(!Comhthéacs_VALUE){
        assh_status_t ERREÁID=assh_context_create(&Comhthéacs_VALUE,ASSH_SERVER,Ullmhaigh_Cuimhne,0,&난수기,0);
        if(ERREÁID)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *modh_mód[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        ERREÁID=assh_algo_register(Comhthéacs_VALUE,ASSH_SAFETY_WEAK,modh_mód);
        if(!ERREÁID)ERREÁID=assh_service_register_va(Comhthéacs_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=gléas_eochair;
        if(!ERREÁID)ERREÁID=assh_key_load(Comhthéacs_VALUE,assh_context_keys(Comhthéacs_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(gléas_eochair));
        if(ERREÁID){진단("SSH init error ",ERREÁID);assh_context_release(Comhthéacs_VALUE);Comhthéacs_VALUE=0;return -5;}
    }
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int tomhas=망주소묶기(port_VALUE,0,22);if(!tomhas)tomhas=연결기다리기(port_VALUE);
    if(tomhas<0){dún_Líonra(port_VALUE);return tomhas;}듣는곳=port_VALUE;return 0;
}
uintptr_t clár_scáthú(uintptr_t 종류,uintptr_t Gníomh) {
    if(종류==1)return(uint32_t)rialú_cianda_taispeáin(Gníomh);
    if(Gníomh==0){dún_nasc();if(듣는곳>=0)dún_Líonra(듣는곳);듣는곳=-1;return 0;}
    if(Gníomh==1){tosú_earráid=Ullmhaigh_blaosc();return(uint32_t)tosú_earráid;}
    return(uint32_t)(듣는곳>=0?1:tosú_earráid);
}
void Ullmhaigh_cianda(void){tosú_earráid=Ullmhaigh_blaosc();rialú_cianda_taispeáin(1);}
static int 같은말(const struct assh_cbuffer_s *sonraí,const char *Word_SMS) {
    size_t fad_VALUE=strlen(Word_SMS);return sonraí->size==fad_VALUE&&!memcmp(sonraí->data,Word_SMS,fad_VALUE);
}
static int Teirminéal_iarratas_HTTP(const struct assh_cbuffer_s *sonraí) {
    if(sonraí->size<24)return 0;
    const unsigned char *sonraí_suíomh=sonraí->data;unsigned fad_VALUE=assh_load_u32(sonraí_suíomh);
    if(fad_VALUE>128||sonraí->size<fad_VALUE+24)return 0;
    unsigned mód_VALUE=assh_load_u32(sonraí_suíomh+4+fad_VALUE+16);
    return mód_VALUE<=2048&&sonraí->size==fad_VALUE+24+mód_VALUE;
}
static void hanla_iarratas_HTTP(struct assh_event_request_s *ócáid) {
    if(!인증됨||ócáid->ch!=cainéal_iontráil||!cainéal_iontráil)return;
    if(같은말(&ócáid->type,"pty-req")) {
        if(!셸시작됨&&Teirminéal_iarratas_HTTP(&ócáid->rq_data))ócáid->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&ócáid->type,"window-change")) {
        if(셸시작됨&&ócáid->rq_data.size==16)ócáid->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *Ordú=0;unsigned fad_VALUE=0;
    if(같은말(&ócáid->type,"exec")) {
        if(ócáid->rq_data.size<4)return;
        fad_VALUE=assh_load_u32(ócáid->rq_data.data);
        if(!fad_VALUE||fad_VALUE>2048||ócáid->rq_data.size!=fad_VALUE+4)return;
        Ordú=ócáid->rq_data.data+4;
        for(unsigned 순번=0;순번<fad_VALUE;순번++)if(!Ordú[순번])return;
        ordú_TYPE=1;
    }else if(!같은말(&ócáid->type,"shell")||ócáid->rq_data.size)return;
    if(sizeof(입력줄)-입력수<fad_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(fad_VALUE)원격입력넣기(Ordú,fad_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;ócáid->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!ordú_TYPE){const char *LÉIGHMÉ_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*LÉIGHMÉ_eb81d7d9)원격출력(*LÉIGHMÉ_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(piara_VALUE<0){if(NOW_VALUE<재접속시각)return;piara_VALUE=망연결받기(듣는곳);if(piara_VALUE<0)return;
        nasc_TIME=NOW_VALUE;assh_status_t ERREÁID=assh_session_create(Comhthéacs_VALUE,&nasc_e05f319b);
        if(ERREÁID){nasc_e05f319b=0;진단("SSH session error ",ERREÁID);dún_nasc();return;}}
    if((!인증됨&&NOW_VALUE-nasc_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){dún_nasc();return;}
    if(cainéal_iontráil&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t ERREÁID=assh_channel_data(cainéal_iontráil,출력줄+출력앞,&수);
            if(!ERREÁID){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(ERREÁID!=ASSH_NO_DATA){dún_nasc();return;}
        }
        if(cuir_deireadh_le_staid>=0&&!출력수){unsigned char staid_VALUE[4];assh_store_u32(staid_VALUE,(uint32_t)cuir_deireadh_le_staid);
            if(assh_request(nasc_e05f319b,cainéal_iontráil,"exit-status",11,staid_VALUE,4,0)||assh_channel_eof(cainéal_iontráil)||assh_channel_close(cainéal_iontráil)) {dún_nasc();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s ócáid;
        if(!assh_event_get(nasc_e05f319b,&ócáid,NOW_VALUE/1000)){dún_nasc();return;}
        assh_status_t ERREÁID=ASSH_OK;int 쉬기=0,끊기=0;
        switch(ócáid.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(piara_VALUE,ócáid.transport.read.buf.data,ócáid.transport.read.buf.size);
            if(수>0)ócáid.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(piara_VALUE,ócáid.transport.write.buf.data,ócáid.transport.write.buf.size);
            if(수>0)ócáid.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ócáid.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ócáid.userauth_server.methods.retries>3)ócáid.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *sonraí=&ócáid.userauth_server.password;
            if(같은말(&sonraí->username,"user")&&sonraí->password.size<=256&&!sonraí->new_password.size) {
                unsigned char achoimre_VALUE[32];cianda_achoimre(sonraí->password.data,sonraí->password.size,achoimre_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=achoimre_VALUE[순번]^blaosc_pasfhocal_achoimre[순번];memset(achoimre_VALUE,0,32);
                if(!차이)sonraí->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *sonraí=&ócáid.connection.channel_open;
            if(인증됨&&!cainéal_iontráil&&셸대기중&&같은말(&sonraí->type,"session")&&!sonraí->rq_data.size) {
                sonraí->reply=ASSH_CONNECTION_REPLY_SUCCESS;sonraí->pkt_size=4096;
                sonraí->win_size=-1;cainéal_iontráil=sonraí->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: hanla_iarratas_HTTP(&ócáid.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *sonraí=&ócáid.connection.channel_data;
            if(!셸시작됨||sonraí->ch!=cainéal_iontráil||sonraí->ext){끊기=1;break;}
            unsigned 수=sonraí->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(sonraí->data.data[순번]==4){cuir_deireadh_le_staid=0;수=순번;sonraí->transferred=sonraí->data.size;break;}
            원격입력넣기(sonraí->data.data,수);if(!sonraí->transferred)sonraí->transferred=수;
            if(!수&&cuir_deireadh_le_staid<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: cainéal_iontráil=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",ócáid.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(nasc_e05f319b,&ócáid,ERREÁID);
        if(끊기){dún_nasc();return;}if(쉬기)return;
    }
}
