/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "uzaq_VALUE.h"
#include "암호기반.h"
#include "Profil.h"
#include "../Şəbəkə_Yığın/Şəbəkə_Yığın.h"
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
static struct assh_context_s *kontekst_VALUE;
static struct assh_session_s *qoşulma_e05f319b;
static struct assh_channel_s *kanal_daxiletmə;
static int 듣는곳=-1,eynisəviyyəli_VALUE=-1,인증됨,셸시작됨,əmr_TYPE,bitirmək_vəziyyət=-1,닫을예정,yükləmə_səhv,örtük_Gözləyir;
static uintptr_t qoşulma_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Söz_SMS,unsigned VALUE) {
    while(*Söz_SMS)보드글자쓰기(*Söz_SMS++);
    char rəqəm_VALUE[12];unsigned 수=0;do{rəqəm_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(rəqəm_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Hazırla_Yaddaş(void *verilənlər,void **ünvan,size_t Böyüklük,enum assh_alloc_type_e 종류) {
    (void)verilənlər;(void)종류;
    if(!Böyüklük){burax_uzaq(*ünvan);*ünvan=0;return ASSH_OK;}
    void *새주소=원격재할당(*ünvan,Böyüklük);
    if(!새주소)return ASSH_ERR_MEM;*ünvan=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *verilənlər,const struct assh_buffer_s *mənbə_VALUE) {
    (void)verilənlər;(void)mənbə_VALUE;unsigned char 시험[32];int ölçü=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return ölçü?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *verilənlər,uint8_t *ölçü,size_t uzunluq_VALUE,uint_fast8_t 종류) {
    (void)verilənlər;(void)종류;if(uzunluq_VALUE>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(ölçü,uzunluq_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *verilənlər){(void)verilənlər;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void bağlamaq_qoşulma(void) {
    인증됨=셸시작됨=0;kanal_daxiletmə=0;
    if(qoşulma_e05f319b)assh_session_release(qoşulma_e05f319b);qoşulma_e05f319b=0;
    if(eynisəviyyəli_VALUE>=0)bağlamaq_Şəbəkə(eynisəviyyəli_VALUE);eynisəviyyəli_VALUE=-1;əmr_TYPE=0;bitirmək_vəziyyət=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *verilənlər,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=verilənlər[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int simvol_VALUE_068c2631=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return simvol_VALUE_068c2631;
}
void 원격출력(unsigned char simvol_VALUE_068c2631) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=simvol_VALUE_068c2631==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=simvol_VALUE_068c2631;이전출력=simvol_VALUE_068c2631;
}
uintptr_t lövhə_bitirmək_uzaq_əmr(uintptr_t vəziyyət_VALUE){if(셸시작됨&&əmr_TYPE)bitirmək_vəziyyət=(int)vəziyyət_VALUE;return 0;}
uintptr_t lövhə_uzaq_gözlə(uintptr_t vəziyyət_VALUE){örtük_Gözləyir=vəziyyət_VALUE!=0;return 0;}
static int Hazırla_örtük(void) {
    if(듣는곳>=0)return 0;
    if(!kontekst_VALUE){
        assh_status_t XƏTA=assh_context_create(&kontekst_VALUE,ASSH_SERVER,Hazırla_Yaddaş,0,&난수기,0);
        if(XƏTA)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metod_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        XƏTA=assh_algo_register(kontekst_VALUE,ASSH_SAFETY_WEAK,metod_MODE);
        if(!XƏTA)XƏTA=assh_service_register_va(kontekst_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=cihaz_Açar;
        if(!XƏTA)XƏTA=assh_key_load(kontekst_VALUE,assh_context_keys(kontekst_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(cihaz_Açar));
        if(XƏTA){진단("SSH init error ",XƏTA);assh_context_release(kontekst_VALUE);kontekst_VALUE=0;return -5;}
    }
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int ölçü=망주소묶기(port_VALUE,0,22);if(!ölçü)ölçü=연결기다리기(port_VALUE);
    if(ölçü<0){bağlamaq_Şəbəkə(port_VALUE);return ölçü;}듣는곳=port_VALUE;return 0;
}
uintptr_t lövhə_kölgələmə(uintptr_t 종류,uintptr_t Gedişat) {
    if(종류==1)return(uint32_t)nəzarət_uzaq_displey(Gedişat);
    if(Gedişat==0){bağlamaq_qoşulma();if(듣는곳>=0)bağlamaq_Şəbəkə(듣는곳);듣는곳=-1;return 0;}
    if(Gedişat==1){yükləmə_səhv=Hazırla_örtük();return(uint32_t)yükləmə_səhv;}
    return(uint32_t)(듣는곳>=0?1:yükləmə_səhv);
}
void Hazırla_uzaq(void){yükləmə_səhv=Hazırla_örtük();nəzarət_uzaq_displey(1);}
static int 같은말(const struct assh_cbuffer_s *verilənlər,const char *Söz_SMS) {
    size_t uzunluq_VALUE=strlen(Söz_SMS);return verilənlər->size==uzunluq_VALUE&&!memcmp(verilənlər->data,Söz_SMS,uzunluq_VALUE);
}
static int Terminal_HTTP_sorğusu(const struct assh_cbuffer_s *verilənlər) {
    if(verilənlər->size<24)return 0;
    const unsigned char *verilənlər_yerinə_qoymaq=verilənlər->data;unsigned uzunluq_VALUE=assh_load_u32(verilənlər_yerinə_qoymaq);
    if(uzunluq_VALUE>128||verilənlər->size<uzunluq_VALUE+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(verilənlər_yerinə_qoymaq+4+uzunluq_VALUE+16);
    return MODE_VALUE<=2048&&verilənlər->size==uzunluq_VALUE+24+MODE_VALUE;
}
static void tutacaq_HTTP_sorğusu(struct assh_event_request_s *hadisə) {
    if(!인증됨||hadisə->ch!=kanal_daxiletmə||!kanal_daxiletmə)return;
    if(같은말(&hadisə->type,"pty-req")) {
        if(!셸시작됨&&Terminal_HTTP_sorğusu(&hadisə->rq_data))hadisə->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&hadisə->type,"window-change")) {
        if(셸시작됨&&hadisə->rq_data.size==16)hadisə->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!örtük_Gözləyir)return;
    const unsigned char *Əmr=0;unsigned uzunluq_VALUE=0;
    if(같은말(&hadisə->type,"exec")) {
        if(hadisə->rq_data.size<4)return;
        uzunluq_VALUE=assh_load_u32(hadisə->rq_data.data);
        if(!uzunluq_VALUE||uzunluq_VALUE>2048||hadisə->rq_data.size!=uzunluq_VALUE+4)return;
        Əmr=hadisə->rq_data.data+4;
        for(unsigned 순번=0;순번<uzunluq_VALUE;순번++)if(!Əmr[순번])return;
        əmr_TYPE=1;
    }else if(!같은말(&hadisə->type,"shell")||hadisə->rq_data.size)return;
    if(sizeof(입력줄)-입력수<uzunluq_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(uzunluq_VALUE)원격입력넣기(Əmr,uzunluq_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;hadisə->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!əmr_TYPE){const char *OXUMƏNİ_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*OXUMƏNİ_eb81d7d9)원격출력(*OXUMƏNİ_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(eynisəviyyəli_VALUE<0){if(NOW_VALUE<재접속시각)return;eynisəviyyəli_VALUE=망연결받기(듣는곳);if(eynisəviyyəli_VALUE<0)return;
        qoşulma_TIME=NOW_VALUE;assh_status_t XƏTA=assh_session_create(kontekst_VALUE,&qoşulma_e05f319b);
        if(XƏTA){qoşulma_e05f319b=0;진단("SSH session error ",XƏTA);bağlamaq_qoşulma();return;}}
    if((!인증됨&&NOW_VALUE-qoşulma_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){bağlamaq_qoşulma();return;}
    if(kanal_daxiletmə&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t XƏTA=assh_channel_data(kanal_daxiletmə,출력줄+출력앞,&수);
            if(!XƏTA){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(XƏTA!=ASSH_NO_DATA){bağlamaq_qoşulma();return;}
        }
        if(bitirmək_vəziyyət>=0&&!출력수){unsigned char vəziyyət_VALUE[4];assh_store_u32(vəziyyət_VALUE,(uint32_t)bitirmək_vəziyyət);
            if(assh_request(qoşulma_e05f319b,kanal_daxiletmə,"exit-status",11,vəziyyət_VALUE,4,0)||assh_channel_eof(kanal_daxiletmə)||assh_channel_close(kanal_daxiletmə)) {bağlamaq_qoşulma();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s hadisə;
        if(!assh_event_get(qoşulma_e05f319b,&hadisə,NOW_VALUE/1000)){bağlamaq_qoşulma();return;}
        assh_status_t XƏTA=ASSH_OK;int 쉬기=0,끊기=0;
        switch(hadisə.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(eynisəviyyəli_VALUE,hadisə.transport.read.buf.data,hadisə.transport.read.buf.size);
            if(수>0)hadisə.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(eynisəviyyəli_VALUE,hadisə.transport.write.buf.data,hadisə.transport.write.buf.size);
            if(수>0)hadisə.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            hadisə.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(hadisə.userauth_server.methods.retries>3)hadisə.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *verilənlər=&hadisə.userauth_server.password;
            if(같은말(&verilənlər->username,"user")&&verilənlər->password.size<=256&&!verilənlər->new_password.size) {
                unsigned char xülasə_VALUE[32];uzaq_xülasə(verilənlər->password.data,verilənlər->password.size,xülasə_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=xülasə_VALUE[순번]^örtük_parol_xülasə[순번];memset(xülasə_VALUE,0,32);
                if(!차이)verilənlər->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *verilənlər=&hadisə.connection.channel_open;
            if(인증됨&&!kanal_daxiletmə&&örtük_Gözləyir&&같은말(&verilənlər->type,"session")&&!verilənlər->rq_data.size) {
                verilənlər->reply=ASSH_CONNECTION_REPLY_SUCCESS;verilənlər->pkt_size=4096;
                verilənlər->win_size=-1;kanal_daxiletmə=verilənlər->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: tutacaq_HTTP_sorğusu(&hadisə.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *verilənlər=&hadisə.connection.channel_data;
            if(!셸시작됨||verilənlər->ch!=kanal_daxiletmə||verilənlər->ext){끊기=1;break;}
            unsigned 수=verilənlər->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(verilənlər->data.data[순번]==4){bitirmək_vəziyyət=0;수=순번;verilənlər->transferred=verilənlər->data.size;break;}
            원격입력넣기(verilənlər->data.data,수);if(!verilənlər->transferred)verilənlər->transferred=수;
            if(!수&&bitirmək_vəziyyət<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: kanal_daxiletmə=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",hadisə.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(qoşulma_e05f319b,&hadisə,XƏTA);
        if(끊기){bağlamaq_qoşulma();return;}if(쉬기)return;
    }
}
