/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "cian_VALUE.h"
#include "암호기반.h"
#include "Pròifil.h"
#include "../lìonra_stac/lìonra_stac.h"
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
static struct assh_context_s *co_theacsa_VALUE;
static struct assh_session_s *ceangal_e05f319b;
static struct assh_channel_s *seanail_cur_a_steach;
static int 듣는곳=-1,seise_VALUE=-1,인증됨,셸시작됨,àithne_TYPE,crìochnaich_cor=-1,닫을예정,tòiseachadh_mearachd,slige_A_feitheamh;
static uintptr_t ceangal_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char figear_VALUE[12];unsigned 수=0;do{figear_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(figear_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Ullaich_cuimhne(void *dàta,void **ADDRESS,size_t atharraich_am_meud,enum assh_alloc_type_e 종류) {
    (void)dàta;(void)종류;
    if(!atharraich_am_meud){sgaoileadh_cian(*ADDRESS);*ADDRESS=0;return ASSH_OK;}
    void *새주소=원격재할당(*ADDRESS,atharraich_am_meud);
    if(!새주소)return ASSH_ERR_MEM;*ADDRESS=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *dàta,const struct assh_buffer_s *sìol_VALUE) {
    (void)dàta;(void)sìol_VALUE;unsigned char 시험[32];int tomhas=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return tomhas?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *dàta,uint8_t *tomhas,size_t faid_VALUE,uint_fast8_t 종류) {
    (void)dàta;(void)종류;if(faid_VALUE>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(tomhas,faid_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *dàta){(void)dàta;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void dùin_ceangal(void) {
    인증됨=셸시작됨=0;seanail_cur_a_steach=0;
    if(ceangal_e05f319b)assh_session_release(ceangal_e05f319b);ceangal_e05f319b=0;
    if(seise_VALUE>=0)dùin_lìonra(seise_VALUE);seise_VALUE=-1;àithne_TYPE=0;crìochnaich_cor=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *dàta,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=dàta[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int caractar_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return caractar_VALUE;
}
void 원격출력(unsigned char caractar_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=caractar_VALUE==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=caractar_VALUE;이전출력=caractar_VALUE;
}
uintptr_t bòrd_crìochnaich_cian_àithne(uintptr_t cor_VALUE){if(셸시작됨&&àithne_TYPE)crìochnaich_cor=(int)cor_VALUE;return 0;}
uintptr_t bòrd_cian_fuirich(uintptr_t cor_VALUE){slige_A_feitheamh=cor_VALUE!=0;return 0;}
static int Ullaich_slige(void) {
    if(듣는곳>=0)return 0;
    if(!co_theacsa_VALUE){
        assh_status_t Mearachd=assh_context_create(&co_theacsa_VALUE,ASSH_SERVER,Ullaich_cuimhne,0,&난수기,0);
        if(Mearachd)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *dòigh_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Mearachd=assh_algo_register(co_theacsa_VALUE,ASSH_SAFETY_WEAK,dòigh_MODE);
        if(!Mearachd)Mearachd=assh_service_register_va(co_theacsa_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=uidheam_Iuchair;
        if(!Mearachd)Mearachd=assh_key_load(co_theacsa_VALUE,assh_context_keys(co_theacsa_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(uidheam_Iuchair));
        if(Mearachd){진단("SSH init error ",Mearachd);assh_context_release(co_theacsa_VALUE);co_theacsa_VALUE=0;return -5;}
    }
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int tomhas=망주소묶기(port_VALUE,0,22);if(!tomhas)tomhas=연결기다리기(port_VALUE);
    if(tomhas<0){dùin_lìonra(port_VALUE);return tomhas;}듣는곳=port_VALUE;return 0;
}
uintptr_t bòrd_co_sheisean(uintptr_t 종류,uintptr_t Gnìomh) {
    if(종류==1)return(uint32_t)smachd_cian_taisbean(Gnìomh);
    if(Gnìomh==0){dùin_ceangal();if(듣는곳>=0)dùin_lìonra(듣는곳);듣는곳=-1;return 0;}
    if(Gnìomh==1){tòiseachadh_mearachd=Ullaich_slige();return(uint32_t)tòiseachadh_mearachd;}
    return(uint32_t)(듣는곳>=0?1:tòiseachadh_mearachd);
}
void Ullaich_cian(void){tòiseachadh_mearachd=Ullaich_slige();smachd_cian_taisbean(1);}
static int 같은말(const struct assh_cbuffer_s *dàta,const char *Word_SMS) {
    size_t faid_VALUE=strlen(Word_SMS);return dàta->size==faid_VALUE&&!memcmp(dàta->data,Word_SMS,faid_VALUE);
}
static int 터미널요청(const struct assh_cbuffer_s *dàta) {
    if(dàta->size<24)return 0;
    const unsigned char *dàta_suidhich=dàta->data;unsigned faid_VALUE=assh_load_u32(dàta_suidhich);
    if(faid_VALUE>128||dàta->size<faid_VALUE+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(dàta_suidhich+4+faid_VALUE+16);
    return MODE_VALUE<=2048&&dàta->size==faid_VALUE+24+MODE_VALUE;
}
static void 요청처리(struct assh_event_request_s *tachartas) {
    if(!인증됨||tachartas->ch!=seanail_cur_a_steach||!seanail_cur_a_steach)return;
    if(같은말(&tachartas->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&tachartas->rq_data))tachartas->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&tachartas->type,"window-change")) {
        if(셸시작됨&&tachartas->rq_data.size==16)tachartas->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!slige_A_feitheamh)return;
    const unsigned char *àithne=0;unsigned faid_VALUE=0;
    if(같은말(&tachartas->type,"exec")) {
        if(tachartas->rq_data.size<4)return;
        faid_VALUE=assh_load_u32(tachartas->rq_data.data);
        if(!faid_VALUE||faid_VALUE>2048||tachartas->rq_data.size!=faid_VALUE+4)return;
        àithne=tachartas->rq_data.data+4;
        for(unsigned 순번=0;순번<faid_VALUE;순번++)if(!àithne[순번])return;
        àithne_TYPE=1;
    }else if(!같은말(&tachartas->type,"shell")||tachartas->rq_data.size)return;
    if(sizeof(입력줄)-입력수<faid_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(faid_VALUE)원격입력넣기(àithne,faid_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;tachartas->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!àithne_TYPE){const char *LEUGHMI_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*LEUGHMI_eb81d7d9)원격출력(*LEUGHMI_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(seise_VALUE<0){if(NOW_VALUE<재접속시각)return;seise_VALUE=망연결받기(듣는곳);if(seise_VALUE<0)return;
        ceangal_TIME=NOW_VALUE;assh_status_t Mearachd=assh_session_create(co_theacsa_VALUE,&ceangal_e05f319b);
        if(Mearachd){ceangal_e05f319b=0;진단("SSH session error ",Mearachd);dùin_ceangal();return;}}
    if((!인증됨&&NOW_VALUE-ceangal_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){dùin_ceangal();return;}
    if(seanail_cur_a_steach&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Mearachd=assh_channel_data(seanail_cur_a_steach,출력줄+출력앞,&수);
            if(!Mearachd){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Mearachd!=ASSH_NO_DATA){dùin_ceangal();return;}
        }
        if(crìochnaich_cor>=0&&!출력수){unsigned char cor_VALUE[4];assh_store_u32(cor_VALUE,(uint32_t)crìochnaich_cor);
            if(assh_request(ceangal_e05f319b,seanail_cur_a_steach,"exit-status",11,cor_VALUE,4,0)||assh_channel_eof(seanail_cur_a_steach)||assh_channel_close(seanail_cur_a_steach)) {dùin_ceangal();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s tachartas;
        if(!assh_event_get(ceangal_e05f319b,&tachartas,NOW_VALUE/1000)){dùin_ceangal();return;}
        assh_status_t Mearachd=ASSH_OK;int 쉬기=0,끊기=0;
        switch(tachartas.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(seise_VALUE,tachartas.transport.read.buf.data,tachartas.transport.read.buf.size);
            if(수>0)tachartas.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(seise_VALUE,tachartas.transport.write.buf.data,tachartas.transport.write.buf.size);
            if(수>0)tachartas.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            tachartas.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(tachartas.userauth_server.methods.retries>3)tachartas.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *dàta=&tachartas.userauth_server.password;
            if(같은말(&dàta->username,"user")&&dàta->password.size<=256&&!dàta->new_password.size) {
                unsigned char 요약[32];원격요약(dàta->password.data,dàta->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)dàta->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *dàta=&tachartas.connection.channel_open;
            if(인증됨&&!seanail_cur_a_steach&&slige_A_feitheamh&&같은말(&dàta->type,"session")&&!dàta->rq_data.size) {
                dàta->reply=ASSH_CONNECTION_REPLY_SUCCESS;dàta->pkt_size=4096;
                dàta->win_size=-1;seanail_cur_a_steach=dàta->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&tachartas.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *dàta=&tachartas.connection.channel_data;
            if(!셸시작됨||dàta->ch!=seanail_cur_a_steach||dàta->ext){끊기=1;break;}
            unsigned 수=dàta->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(dàta->data.data[순번]==4){crìochnaich_cor=0;수=순번;dàta->transferred=dàta->data.size;break;}
            원격입력넣기(dàta->data.data,수);if(!dàta->transferred)dàta->transferred=수;
            if(!수&&crìochnaich_cor<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: seanail_cur_a_steach=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",tachartas.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(ceangal_e05f319b,&tachartas,Mearachd);
        if(끊기){dùin_ceangal();return;}if(쉬기)return;
    }
}
