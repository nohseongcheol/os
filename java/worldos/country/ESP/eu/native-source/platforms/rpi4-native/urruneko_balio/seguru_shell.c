/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "urruneko_balio.h"
#include "암호기반.h"
#include "profil.h"
#include "../sare_pila/sare_pila.h"
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
static struct assh_context_s *문맥;
static struct assh_session_s *konexio_e05f319b;
static struct assh_channel_s *kanal_sarrera;
static int Entzuten_amaiera_puntu=-1,pareko_balio=-1,인증됨,셸시작됨,komando_MOTA,amaitu_Egoera=-1,닫을예정,abio_errore,shell_Zain;
static uintptr_t konexio_ordua,재접속시각,닫는시각;
static unsigned char 입력줄[8192],출력줄[65536];
static unsigned 입력앞,입력수,출력앞,출력수,이전출력;
static void 진단(const char *Word_SMS,unsigned balio) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char digitu_balio[12];unsigned 수=0;do{digitu_balio[수++]='0'+balio%10;balio/=10;}while(balio);
    while(수)보드글자쓰기(digitu_balio[--수]);보드글자쓰기(10);
}
static assh_status_t 기억마련(void *datuak,void **helbide,size_t Tamaina,enum assh_alloc_type_e 종류) {
    (void)datuak;(void)종류;
    if(!Tamaina){askatu_urruneko(*helbide);*helbide=0;return ASSH_OK;}
    void *새주소=원격재할당(*helbide,Tamaina);
    if(!새주소)return ASSH_ERR_MEM;*helbide=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *datuak,const struct assh_buffer_s *serie_balio) {
    (void)datuak;(void)serie_balio;unsigned char 시험[32];int EMAITZA=원격난수(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return EMAITZA?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *datuak,uint8_t *EMAITZA,size_t luzera_balio,uint_fast8_t 종류) {
    (void)datuak;(void)종류;if(luzera_balio>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(EMAITZA,luzera_balio)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *datuak){(void)datuak;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void itxi_konexio(void) {
    인증됨=셸시작됨=0;kanal_sarrera=0;
    if(konexio_e05f319b)assh_session_release(konexio_e05f319b);konexio_e05f319b=0;
    if(pareko_balio>=0)itxi_sare(pareko_balio);pareko_balio=-1;komando_MOTA=0;amaitu_Egoera=-1;닫을예정=0;
    입력앞=입력수=출력앞=출력수=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *datuak,unsigned 수) {
    if(수>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<수;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=datuak[순번];return 수;
}
int 원격입력(void) {
    if(!입력수)return -1;int karaktere_balio=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return karaktere_balio;
}
void 원격출력(unsigned char karaktere_balio) {
    if(!셸시작됨||닫을예정)return;
    unsigned Erantsi_MODA=karaktere_balio==10&&이전출력!=13;
    if(출력수+1+Erantsi_MODA>sizeof(출력줄)){닫을예정=2;return;}
    if(Erantsi_MODA)출력줄[(출력앞+출력수++)%sizeof(출력줄)]=13;
    출력줄[(출력앞+출력수++)%sizeof(출력줄)]=karaktere_balio;이전출력=karaktere_balio;
}
uintptr_t arbel_amaitu_urruneko_komando(uintptr_t Egoera_balio){if(셸시작됨&&komando_MOTA)amaitu_Egoera=(int)Egoera_balio;return 0;}
uintptr_t arbel_urruneko_itxaron(uintptr_t Egoera_balio){shell_Zain=Egoera_balio!=0;return 0;}
static int 셸준비(void) {
    if(Entzuten_amaiera_puntu>=0)return 0;
    if(!문맥){
        assh_status_t errorea=assh_context_create(&문맥,ASSH_SERVER,기억마련,0,&난수기,0);
        if(errorea)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *방식[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        errorea=assh_algo_register(문맥,ASSH_SAFETY_WEAK,방식);
        if(!errorea)errorea=assh_service_register_va(문맥,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=gailu_gako;
        if(!errorea)errorea=assh_key_load(문맥,assh_context_keys(문맥),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(gailu_gako));
        if(errorea){진단("SSH init error ",errorea);assh_context_release(문맥);문맥=0;return -5;}
    }
    int ataka_balio=통신끝점만들기(1);if(ataka_balio<0)return ataka_balio;통신주소재사용(ataka_balio);
    int EMAITZA=망주소묶기(ataka_balio,0,22);if(!EMAITZA)EMAITZA=연결기다리기(ataka_balio);
    if(EMAITZA<0){itxi_sare(ataka_balio);return EMAITZA;}Entzuten_amaiera_puntu=ataka_balio;return 0;
}
uintptr_t arbel_aldi_bereko_saio(uintptr_t 종류,uintptr_t Ekintza) {
    if(종류==1)return(uint32_t)kontrol_urruneko_pantaila(Ekintza);
    if(Ekintza==0){itxi_konexio();if(Entzuten_amaiera_puntu>=0)itxi_sare(Entzuten_amaiera_puntu);Entzuten_amaiera_puntu=-1;return 0;}
    if(Ekintza==1){abio_errore=셸준비();return(uint32_t)abio_errore;}
    return(uint32_t)(Entzuten_amaiera_puntu>=0?1:abio_errore);
}
void 원격준비(void){abio_errore=셸준비();kontrol_urruneko_pantaila(1);}
static int 같은말(const struct assh_cbuffer_s *datuak,const char *Word_SMS) {
    size_t luzera_balio=strlen(Word_SMS);return datuak->size==luzera_balio&&!memcmp(datuak->data,Word_SMS,luzera_balio);
}
static int Terminal_eskaera(const struct assh_cbuffer_s *datuak) {
    if(datuak->size<24)return 0;
    const unsigned char *datuak_kargu=datuak->data;unsigned luzera_balio=assh_load_u32(datuak_kargu);
    if(luzera_balio>128||datuak->size<luzera_balio+24)return 0;
    unsigned MODA_balio=assh_load_u32(datuak_kargu+4+luzera_balio+16);
    return MODA_balio<=2048&&datuak->size==luzera_balio+24+MODA_balio;
}
static void helduleku_eskaera(struct assh_event_request_s *Gertaera) {
    if(!인증됨||Gertaera->ch!=kanal_sarrera||!kanal_sarrera)return;
    if(같은말(&Gertaera->type,"pty-req")) {
        if(!셸시작됨&&Terminal_eskaera(&Gertaera->rq_data))Gertaera->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Gertaera->type,"window-change")) {
        if(셸시작됨&&Gertaera->rq_data.size==16)Gertaera->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!shell_Zain)return;
    const unsigned char *Komandoa=0;unsigned luzera_balio=0;
    if(같은말(&Gertaera->type,"exec")) {
        if(Gertaera->rq_data.size<4)return;
        luzera_balio=assh_load_u32(Gertaera->rq_data.data);
        if(!luzera_balio||luzera_balio>2048||Gertaera->rq_data.size!=luzera_balio+4)return;
        Komandoa=Gertaera->rq_data.data+4;
        for(unsigned 순번=0;순번<luzera_balio;순번++)if(!Komandoa[순번])return;
        komando_MOTA=1;
    }else if(!같은말(&Gertaera->type,"shell")||Gertaera->rq_data.size)return;
    if(sizeof(입력줄)-입력수<luzera_balio+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(luzera_balio)원격입력넣기(Komandoa,luzera_balio);원격입력넣기(&끝,1);
    셸시작됨=1;Gertaera->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!komando_MOTA){const char *IRAKHAU_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*IRAKHAU_eb81d7d9)원격출력(*IRAKHAU_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Entzuten_amaiera_puntu<0)return;
    uintptr_t ORAIN_balio=보드밀리초();
    if(pareko_balio<0){if(ORAIN_balio<재접속시각)return;pareko_balio=망연결받기(Entzuten_amaiera_puntu);if(pareko_balio<0)return;
        konexio_ordua=ORAIN_balio;assh_status_t errorea=assh_session_create(문맥,&konexio_e05f319b);
        if(errorea){konexio_e05f319b=0;진단("SSH session error ",errorea);itxi_konexio();return;}}
    if((!인증됨&&ORAIN_balio-konexio_ordua>30000)||닫을예정==2||(닫을예정&&ORAIN_balio>=닫는시각)){itxi_konexio();return;}
    if(kanal_sarrera&&셸시작됨&&!닫을예정) {
        if(출력수){size_t 수=sizeof(출력줄)-출력앞;if(수>출력수)수=출력수;if(수>2048)수=2048;
            assh_status_t errorea=assh_channel_data(kanal_sarrera,출력줄+출력앞,&수);
            if(!errorea){출력앞=(출력앞+수)%sizeof(출력줄);출력수-=수;}
            else if(errorea!=ASSH_NO_DATA){itxi_konexio();return;}
        }
        if(amaitu_Egoera>=0&&!출력수){unsigned char Egoera_balio[4];assh_store_u32(Egoera_balio,(uint32_t)amaitu_Egoera);
            if(assh_request(konexio_e05f319b,kanal_sarrera,"exit-status",11,Egoera_balio,4,0)||assh_channel_eof(kanal_sarrera)||assh_channel_close(kanal_sarrera)) {itxi_konexio();return;}
            닫을예정=1;닫는시각=ORAIN_balio+3000;
        }
    }
    for(unsigned SEKUENTZIA_balio=0;SEKUENTZIA_balio<16;SEKUENTZIA_balio++) {
        struct assh_event_s Gertaera;
        if(!assh_event_get(konexio_e05f319b,&Gertaera,ORAIN_balio/1000)){itxi_konexio();return;}
        assh_status_t errorea=ASSH_OK;int 쉬기=0,deskonektatu_amaiera_puntu=0;
        switch(Gertaera.id) {
        case ASSH_EVENT_READ: {
            int 수=통신읽기(pareko_balio,Gertaera.transport.read.buf.data,Gertaera.transport.read.buf.size);
            if(수>0)Gertaera.transport.read.transferred=수;
            else if(수==-11)쉬기=1;else deskonektatu_amaiera_puntu=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int 수=통신쓰기(pareko_balio,Gertaera.transport.write.buf.data,Gertaera.transport.write.buf.size);
            if(수>0)Gertaera.transport.write.transferred=수;
            else if(수==-11)쉬기=1;else deskonektatu_amaiera_puntu=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Gertaera.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Gertaera.userauth_server.methods.retries>3)Gertaera.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *datuak=&Gertaera.userauth_server.password;
            if(같은말(&datuak->username,"user")&&datuak->password.size<=256&&!datuak->new_password.size) {
                unsigned char 요약[32];원격요약(datuak->password.data,datuak->password.size,요약);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=요약[순번]^셸암호요약[순번];memset(요약,0,32);
                if(!차이)datuak->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *datuak=&Gertaera.connection.channel_open;
            if(인증됨&&!kanal_sarrera&&shell_Zain&&같은말(&datuak->type,"session")&&!datuak->rq_data.size) {
                datuak->reply=ASSH_CONNECTION_REPLY_SUCCESS;datuak->pkt_size=4096;
                datuak->win_size=-1;kanal_sarrera=datuak->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: helduleku_eskaera(&Gertaera.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *datuak=&Gertaera.connection.channel_data;
            if(!셸시작됨||datuak->ch!=kanal_sarrera||datuak->ext){deskonektatu_amaiera_puntu=1;break;}
            unsigned 수=datuak->data.size;if(수>sizeof(입력줄)-입력수)수=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<수;순번++)if(datuak->data.data[순번]==4){amaitu_Egoera=0;수=순번;datuak->transferred=datuak->data.size;break;}
            원격입력넣기(datuak->data.data,수);if(!datuak->transferred)datuak->transferred=수;
            if(!수&&amaitu_Egoera<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: kanal_sarrera=0;셸시작됨=0;닫을예정=1;닫는시각=ORAIN_balio+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Gertaera.session.error.code);deskonektatu_amaiera_puntu=1;break;
        case ASSH_EVENT_DISCONNECT: deskonektatu_amaiera_puntu=1;break;
        default: break;
        }
        assh_event_done(konexio_e05f319b,&Gertaera,errorea);
        if(deskonektatu_amaiera_puntu){itxi_konexio();return;}if(쉬기)return;
    }
}
