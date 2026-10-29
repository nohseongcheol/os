/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "kwa_mbali_thamani.h"
#include "암호기반.h"
#include "Maelezo_mafupi.h"
#include "../Mtandao_Mpororo/Mtandao_Mpororo.h"
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
static struct assh_context_s *Muktadha_thamani;
static struct assh_session_s *muunganisho_e05f319b;
static struct assh_channel_s *mkondo_ingizo;
static int 듣는곳=-1,kompyuta_rika_thamani=-1,인증됨,셸시작됨,amri_aina,tamatia_hali=-1,닫을예정,uwashaji_kosa,셸대기중;
static uintptr_t muunganisho_saa,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Neno_SMS,unsigned thamani) {
    while(*Neno_SMS)보드글자쓰기(*Neno_SMS++);
    char dijiti_thamani[12];unsigned 수=0;do{dijiti_thamani[수++]='0'+thamani%10;thamani/=10;}while(thamani);
    while(수)보드글자쓰기(dijiti_thamani[--수]);보드글자쓰기(10);
}
static assh_status_t Andaa_kumbukumbu(void *data,void **anwani,size_t panga_ukubwa,enum assh_alloc_type_e 종류) {
    (void)data;(void)종류;
    if(!panga_ukubwa){toleo_kwa_mbali(*anwani);*anwani=0;return ASSH_OK;}
    void *새주소=원격재할당(*anwani,panga_ukubwa);
    if(!새주소)return ASSH_ERR_MEM;*anwani=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *data,const struct assh_buffer_s *pakia_thamani) {
    (void)data;(void)pakia_thamani;unsigned char 시험[32];int 결과=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return 결과?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *data,uint8_t *결과,size_t urefu_thamani,uint_fast8_t 종류) {
    (void)data;(void)종류;if(urefu_thamani>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(결과,urefu_thamani)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *data){(void)data;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void funga_muunganisho(void) {
    인증됨=셸시작됨=0;mkondo_ingizo=0;
    if(muunganisho_e05f319b)assh_session_release(muunganisho_e05f319b);muunganisho_e05f319b=0;
    if(kompyuta_rika_thamani>=0)funga_Mtandao(kompyuta_rika_thamani);kompyuta_rika_thamani=-1;amri_aina=0;tamatia_hali=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *data,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=data[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int kibambo_thamani=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return kibambo_thamani;
}
void 원격출력(unsigned char kibambo_thamani) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=kibambo_thamani==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=kibambo_thamani;이전출력=kibambo_thamani;
}
uintptr_t 보드원격명령끝(uintptr_t hali_thamani){if(셸시작됨&&amri_aina)tamatia_hali=(int)hali_thamani;return 0;}
uintptr_t 보드원격대기(uintptr_t hali_thamani){셸대기중=hali_thamani!=0;return 0;}
static int Andaa_sheli(void) {
    if(듣는곳>=0)return 0;
    if(!Muktadha_thamani){
        assh_status_t kosa=assh_context_create(&Muktadha_thamani,ASSH_SERVER,Andaa_kumbukumbu,0,&난수기,0);
        if(kosa)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *mbinu_hali_tumizi[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        kosa=assh_algo_register(Muktadha_thamani,ASSH_SAFETY_WEAK,mbinu_hali_tumizi);
        if(!kosa)kosa=assh_service_register_va(Muktadha_thamani,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=kifaa_Kitufe;
        if(!kosa)kosa=assh_key_load(Muktadha_thamani,assh_context_keys(Muktadha_thamani),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(kifaa_Kitufe));
        if(kosa){진단("SSH init error ",kosa);assh_context_release(Muktadha_thamani);Muktadha_thamani=0;return -5;}
    }
    int kituo_thamani=통신끝점만들기(1);if(kituo_thamani<0)return kituo_thamani;통신주소재사용(kituo_thamani);
    int 결과=망주소묶기(kituo_thamani,0,22);if(!결과)결과=연결기다리기(kituo_thamani);
    if(결과<0){funga_Mtandao(kituo_thamani);return 결과;}듣는곳=kituo_thamani;return 0;
}
uintptr_t 보드원격제어(uintptr_t 종류,uintptr_t Kitendo) {
    if(종류==1)return(uint32_t)udhibiti_kwa_mbali_onyesha(Kitendo);
    if(Kitendo==0){funga_muunganisho();if(듣는곳>=0)funga_Mtandao(듣는곳);듣는곳=-1;return 0;}
    if(Kitendo==1){uwashaji_kosa=Andaa_sheli();return(uint32_t)uwashaji_kosa;}
    return(uint32_t)(듣는곳>=0?1:uwashaji_kosa);
}
void Andaa_kwa_mbali(void){uwashaji_kosa=Andaa_sheli();udhibiti_kwa_mbali_onyesha(1);}
static int 같은말(const struct assh_cbuffer_s *data,const char *Neno_SMS) {
    size_t urefu_thamani=strlen(Neno_SMS);return data->size==urefu_thamani&&!memcmp(data->data,Neno_SMS,urefu_thamani);
}
static int 터미널요청(const struct assh_cbuffer_s *data) {
    if(data->size<24)return 0;
    const unsigned char *자료위치=data->data;unsigned urefu_thamani=assh_load_u32(자료위치);
    if(urefu_thamani>128||data->size<urefu_thamani+24)return 0;
    unsigned hali_tumizi_thamani=assh_load_u32(자료위치+4+urefu_thamani+16);
    return hali_tumizi_thamani<=2048&&data->size==urefu_thamani+24+hali_tumizi_thamani;
}
static void 요청처리(struct assh_event_request_s *tukio) {
    if(!인증됨||tukio->ch!=mkondo_ingizo||!mkondo_ingizo)return;
    if(같은말(&tukio->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&tukio->rq_data))tukio->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&tukio->type,"window-change")) {
        if(셸시작됨&&tukio->rq_data.size==16)tukio->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!셸대기중)return;
    const unsigned char *amri=0;unsigned urefu_thamani=0;
    if(같은말(&tukio->type,"exec")) {
        if(tukio->rq_data.size<4)return;
        urefu_thamani=assh_load_u32(tukio->rq_data.data);
        if(!urefu_thamani||urefu_thamani>2048||tukio->rq_data.size!=urefu_thamani+4)return;
        amri=tukio->rq_data.data+4;
        for(unsigned 순번=0;순번<urefu_thamani;순번++)if(!amri[순번])return;
        amri_aina=1;
    }else if(!같은말(&tukio->type,"shell")||tukio->rq_data.size)return;
    if(sizeof(입력줄)-입력수<urefu_thamani+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(urefu_thamani)원격입력넣기(amri,urefu_thamani);원격입력넣기(&끝,1);
    셸시작됨=1;tukio->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!amri_aina){const char *NISOME_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*NISOME_eb81d7d9)원격출력(*NISOME_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t SASA_thamani=보드밀리초();
    if(kompyuta_rika_thamani<0){if(SASA_thamani<재접속시각)return;kompyuta_rika_thamani=망연결받기(듣는곳);if(kompyuta_rika_thamani<0)return;
        muunganisho_saa=SASA_thamani;assh_status_t kosa=assh_session_create(Muktadha_thamani,&muunganisho_e05f319b);
        if(kosa){muunganisho_e05f319b=0;진단("SSH session error ",kosa);funga_muunganisho();return;}}
    if((!인증됨&&SASA_thamani-muunganisho_saa>30000)||닫을예정==2||(닫을예정&&SASA_thamani>=닫는시각)){funga_muunganisho();return;}
    if(mkondo_ingizo&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t kosa=assh_channel_data(mkondo_ingizo,출력줄+출력앞,&수);
            if(!kosa){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(kosa!=ASSH_NO_DATA){funga_muunganisho();return;}
        }
        if(tamatia_hali>=0&&!출력수){unsigned char hali_thamani[4];assh_store_u32(hali_thamani,(uint32_t)tamatia_hali);
            if(assh_request(muunganisho_e05f319b,mkondo_ingizo,"exit-status",11,hali_thamani,4,0)||assh_channel_eof(mkondo_ingizo)||assh_channel_close(mkondo_ingizo)) {funga_muunganisho();return;}
            닫을예정=1;닫는시각=SASA_thamani+3000;
        }
    }
    for(unsigned MFUATANO_thamani=0;MFUATANO_thamani<16;MFUATANO_thamani++) {
        struct assh_event_s tukio;
        if(!assh_event_get(muunganisho_e05f319b,&tukio,SASA_thamani/1000)){funga_muunganisho();return;}
        assh_status_t kosa=ASSH_OK;int 쉬기=0,끊기=0;
        switch(tukio.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(kompyuta_rika_thamani,tukio.transport.read.buf.data,tukio.transport.read.buf.size);
            if(수>0)tukio.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(kompyuta_rika_thamani,tukio.transport.write.buf.data,tukio.transport.write.buf.size);
            if(수>0)tukio.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            tukio.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(tukio.userauth_server.methods.retries>3)tukio.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *data=&tukio.userauth_server.password;
            if(같은말(&data->username,"user")&&data->password.size<=256&&!data->new_password.size) {
                unsigned char muhtasari_thamani[32];kwa_mbali_muhtasari(data->password.data,data->password.size,muhtasari_thamani);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=muhtasari_thamani[순번]^sheli_nywila_muhtasari[순번];memset(muhtasari_thamani,0,32);
                if(!차이)data->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *data=&tukio.connection.channel_open;
            if(인증됨&&!mkondo_ingizo&&셸대기중&&같은말(&data->type,"session")&&!data->rq_data.size) {
                data->reply=ASSH_CONNECTION_REPLY_SUCCESS;data->pkt_size=4096;
                data->win_size=-1;mkondo_ingizo=data->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&tukio.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *data=&tukio.connection.channel_data;
            if(!셸시작됨||data->ch!=mkondo_ingizo||data->ext){끊기=1;break;}
            unsigned 수=data->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(data->data.data[순번]==4){tamatia_hali=0;수=순번;data->transferred=data->data.size;break;}
            원격입력넣기(data->data.data,수);if(!data->transferred)data->transferred=수;
            if(!수&&tamatia_hali<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: mkondo_ingizo=0;셸시작됨=0;닫을예정=1;닫는시각=SASA_thamani+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",tukio.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(muunganisho_e05f319b,&tukio,kosa);
        if(끊기){funga_muunganisho();return;}if(쉬기)return;
    }
}
