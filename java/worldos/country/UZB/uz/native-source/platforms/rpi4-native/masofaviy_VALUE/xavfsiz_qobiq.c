/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "masofaviy_VALUE.h"
#include "암호기반.h"
#include "Profil.h"
#include "../Tarmoq_Stack/Tarmoq_Stack.h"
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
static struct assh_context_s *Kontekst_VALUE;
static struct assh_session_s *aloqa_e05f319b;
static struct assh_channel_s *kanal_kiritish;
static int 듣는곳=-1,bir_rangli_VALUE=-1,인증됨,셸시작됨,buyruq_TYPE,to_xtatmoq_holat_2bce2943=-1,닫을예정,yuklash_xato,qobiq_Kutish;
static uintptr_t aloqa_TIME,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char raqam_VALUE[12];unsigned 수=0;do{raqam_VALUE[수++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(수)보드글자쓰기(raqam_VALUE[--수]);보드글자쓰기(10);
}
static assh_status_t Tayyorlamoq_Xotira(void *ma_lumotlar,void **manzil,size_t Hajmi,enum assh_alloc_type_e 종류) {
    (void)ma_lumotlar;(void)종류;
    if(!Hajmi){nashr_masofaviy(*manzil);*manzil=0;return ASSH_OK;}
    void *새주소=원격재할당(*manzil,Hajmi);
    if(!새주소)return ASSH_ERR_MEM;*manzil=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *ma_lumotlar,const struct assh_buffer_s *quvvatlash_VALUE) {
    (void)ma_lumotlar;(void)quvvatlash_VALUE;unsigned char 시험[32];int o_lchov=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return o_lchov?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *ma_lumotlar,uint8_t *o_lchov,size_t uzunlik_VALUE,uint_fast8_t 종류) {
    (void)ma_lumotlar;(void)종류;if(uzunlik_VALUE>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(o_lchov,uzunlik_VALUE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *ma_lumotlar){(void)ma_lumotlar;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void yopmoq_aloqa(void) {
    인증됨=셸시작됨=0;kanal_kiritish=0;
    if(aloqa_e05f319b)assh_session_release(aloqa_e05f319b);aloqa_e05f319b=0;
    if(bir_rangli_VALUE>=0)yopmoq_Tarmoq(bir_rangli_VALUE);bir_rangli_VALUE=-1;buyruq_TYPE=0;to_xtatmoq_holat_2bce2943=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *ma_lumotlar,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=ma_lumotlar[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int belgi_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return belgi_VALUE;
}
void 원격출력(unsigned char belgi_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned 덧붙임=belgi_VALUE==10&&이전출력!=13;
    if(출력수+1+덧붙임>sizeof(출력줄)){닫을예정=2;return;}
    if(덧붙임)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=belgi_VALUE;이전출력=belgi_VALUE;
}
uintptr_t yozuv_taxtasi_to_xtatmoq_masofaviy_buyruq(uintptr_t holat_VALUE_e10195a1){if(셸시작됨&&buyruq_TYPE)to_xtatmoq_holat_2bce2943=(int)holat_VALUE_e10195a1;return 0;}
uintptr_t yozuv_taxtasi_masofaviy_bir_daqiqa(uintptr_t holat_VALUE_e10195a1){qobiq_Kutish=holat_VALUE_e10195a1!=0;return 0;}
static int Tayyorlamoq_qobiq(void) {
    if(듣는곳>=0)return 0;
    if(!Kontekst_VALUE){
        assh_status_t Xato=assh_context_create(&Kontekst_VALUE,ASSH_SERVER,Tayyorlamoq_Xotira,0,&난수기,0);
        if(Xato)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *uslub_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        Xato=assh_algo_register(Kontekst_VALUE,ASSH_SAFETY_WEAK,uslub_MODE);
        if(!Xato)Xato=assh_service_register_va(Kontekst_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=qurilma_Kalit;
        if(!Xato)Xato=assh_key_load(Kontekst_VALUE,assh_context_keys(Kontekst_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(qurilma_Kalit));
        if(Xato){진단("SSH init error ",Xato);assh_context_release(Kontekst_VALUE);Kontekst_VALUE=0;return -5;}
    }
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int o_lchov=망주소묶기(port_VALUE,0,22);if(!o_lchov)o_lchov=연결기다리기(port_VALUE);
    if(o_lchov<0){yopmoq_Tarmoq(port_VALUE);return o_lchov;}듣는곳=port_VALUE;return 0;
}
uintptr_t yozuv_taxtasi_soyalashtirish(uintptr_t 종류,uintptr_t Amal) {
    if(종류==1)return(uint32_t)boshqaruv_masofaviy_ekran(Amal);
    if(Amal==0){yopmoq_aloqa();if(듣는곳>=0)yopmoq_Tarmoq(듣는곳);듣는곳=-1;return 0;}
    if(Amal==1){yuklash_xato=Tayyorlamoq_qobiq();return(uint32_t)yuklash_xato;}
    return(uint32_t)(듣는곳>=0?1:yuklash_xato);
}
void Tayyorlamoq_masofaviy(void){yuklash_xato=Tayyorlamoq_qobiq();boshqaruv_masofaviy_ekran(1);}
static int 같은말(const struct assh_cbuffer_s *ma_lumotlar,const char *Word_SMS) {
    size_t uzunlik_VALUE=strlen(Word_SMS);return ma_lumotlar->size==uzunlik_VALUE&&!memcmp(ma_lumotlar->data,Word_SMS,uzunlik_VALUE);
}
static int 터미널요청(const struct assh_cbuffer_s *ma_lumotlar) {
    if(ma_lumotlar->size<24)return 0;
    const unsigned char *ma_lumotlar_holat=ma_lumotlar->data;unsigned uzunlik_VALUE=assh_load_u32(ma_lumotlar_holat);
    if(uzunlik_VALUE>128||ma_lumotlar->size<uzunlik_VALUE+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(ma_lumotlar_holat+4+uzunlik_VALUE+16);
    return MODE_VALUE<=2048&&ma_lumotlar->size==uzunlik_VALUE+24+MODE_VALUE;
}
static void 요청처리(struct assh_event_request_s *hodisa) {
    if(!인증됨||hodisa->ch!=kanal_kiritish||!kanal_kiritish)return;
    if(같은말(&hodisa->type,"pty-req")) {
        if(!셸시작됨&&터미널요청(&hodisa->rq_data))hodisa->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&hodisa->type,"window-change")) {
        if(셸시작됨&&hodisa->rq_data.size==16)hodisa->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!qobiq_Kutish)return;
    const unsigned char *Buyruq=0;unsigned uzunlik_VALUE=0;
    if(같은말(&hodisa->type,"exec")) {
        if(hodisa->rq_data.size<4)return;
        uzunlik_VALUE=assh_load_u32(hodisa->rq_data.data);
        if(!uzunlik_VALUE||uzunlik_VALUE>2048||hodisa->rq_data.size!=uzunlik_VALUE+4)return;
        Buyruq=hodisa->rq_data.data+4;
        for(unsigned 순번=0;순번<uzunlik_VALUE;순번++)if(!Buyruq[순번])return;
        buyruq_TYPE=1;
    }else if(!같은말(&hodisa->type,"shell")||hodisa->rq_data.size)return;
    if(sizeof(입력줄)-입력수<uzunlik_VALUE+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(uzunlik_VALUE)원격입력넣기(Buyruq,uzunlik_VALUE);원격입력넣기(&끝,1);
    셸시작됨=1;hodisa->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!buyruq_TYPE){const char *ma_lumot_fayli_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*ma_lumot_fayli_eb81d7d9)원격출력(*ma_lumot_fayli_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(듣는곳<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(bir_rangli_VALUE<0){if(NOW_VALUE<재접속시각)return;bir_rangli_VALUE=망연결받기(듣는곳);if(bir_rangli_VALUE<0)return;
        aloqa_TIME=NOW_VALUE;assh_status_t Xato=assh_session_create(Kontekst_VALUE,&aloqa_e05f319b);
        if(Xato){aloqa_e05f319b=0;진단("SSH session error ",Xato);yopmoq_aloqa();return;}}
    if((!인증됨&&NOW_VALUE-aloqa_TIME>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=닫는시각)){yopmoq_aloqa();return;}
    if(kanal_kiritish&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t Xato=assh_channel_data(kanal_kiritish,출력줄+출력앞,&수);
            if(!Xato){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(Xato!=ASSH_NO_DATA){yopmoq_aloqa();return;}
        }
        if(to_xtatmoq_holat_2bce2943>=0&&!출력수){unsigned char holat_VALUE_e10195a1[4];assh_store_u32(holat_VALUE_e10195a1,(uint32_t)to_xtatmoq_holat_2bce2943);
            if(assh_request(aloqa_e05f319b,kanal_kiritish,"exit-status",11,holat_VALUE_e10195a1,4,0)||assh_channel_eof(kanal_kiritish)||assh_channel_close(kanal_kiritish)) {yopmoq_aloqa();return;}
            닫을예정=1;닫는시각=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s hodisa;
        if(!assh_event_get(aloqa_e05f319b,&hodisa,NOW_VALUE/1000)){yopmoq_aloqa();return;}
        assh_status_t Xato=ASSH_OK;int 쉬기=0,끊기=0;
        switch(hodisa.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(bir_rangli_VALUE,hodisa.transport.read.buf.data,hodisa.transport.read.buf.size);
            if(수>0)hodisa.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(bir_rangli_VALUE,hodisa.transport.write.buf.data,hodisa.transport.write.buf.size);
            if(수>0)hodisa.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else 끊기=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            hodisa.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(hodisa.userauth_server.methods.retries>3)hodisa.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *ma_lumotlar=&hodisa.userauth_server.password;
            if(같은말(&ma_lumotlar->username,"user")&&ma_lumotlar->password.size<=256&&!ma_lumotlar->new_password.size) {
                unsigned char xulosa_VALUE[32];masofaviy_xulosa(ma_lumotlar->password.data,ma_lumotlar->password.size,xulosa_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=xulosa_VALUE[순번]^qobiq_parol_xulosa[순번];memset(xulosa_VALUE,0,32);
                if(!차이)ma_lumotlar->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *ma_lumotlar=&hodisa.connection.channel_open;
            if(인증됨&&!kanal_kiritish&&qobiq_Kutish&&같은말(&ma_lumotlar->type,"session")&&!ma_lumotlar->rq_data.size) {
                ma_lumotlar->reply=ASSH_CONNECTION_REPLY_SUCCESS;ma_lumotlar->pkt_size=4096;
                ma_lumotlar->win_size=-1;kanal_kiritish=ma_lumotlar->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: 요청처리(&hodisa.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *ma_lumotlar=&hodisa.connection.channel_data;
            if(!셸시작됨||ma_lumotlar->ch!=kanal_kiritish||ma_lumotlar->ext){끊기=1;break;}
            unsigned 수=ma_lumotlar->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(ma_lumotlar->data.data[순번]==4){to_xtatmoq_holat_2bce2943=0;수=순번;ma_lumotlar->transferred=ma_lumotlar->data.size;break;}
            원격입력넣기(ma_lumotlar->data.data,수);if(!ma_lumotlar->transferred)ma_lumotlar->transferred=수;
            if(!수&&to_xtatmoq_holat_2bce2943<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: kanal_kiritish=0;셸시작됨=0;닫을예정=1;닫는시각=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",hodisa.session.error.code);끊기=1;break;
        case ASSH_EVENT_DISCONNECT: 끊기=1;break;
        default: break;
        }
        assh_event_done(aloqa_e05f319b,&hodisa,Xato);
        if(끊기){yopmoq_aloqa();return;}if(쉬기)return;
    }
}
