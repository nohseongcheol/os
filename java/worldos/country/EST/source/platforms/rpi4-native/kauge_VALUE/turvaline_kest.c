/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "kauge_VALUE.h"
#include "krüptograafia_tugi.h"
#include "Profiil.h"
#include "../võrk_Virn/võrk_Virn.h"
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
static struct assh_session_s *ühendus_e05f319b;
static struct assh_channel_s *Kanal_kirje;
static int Kuulamine_osaleja=-1,partner_VALUE=-1,인증됨,셸시작됨,käsk_TYPE,lõpeta_kõne_Olek=-1,닫을예정,käivitus_tõrge,kest_Ootamine;
static uintptr_t ühendus_Aeg,재접속시각,sulgemine_Aeg;
static unsigned char 입력줄[8192],toodang_liin[65536];
static unsigned 입력앞,입력수,출력앞,toodang_COUNT,이전출력;
static void 진단(const char *Word_SMS,unsigned VALUE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char number_VALUE[12];unsigned number=0;do{number_VALUE[number++]='0'+VALUE%10;VALUE/=10;}while(VALUE);
    while(number)보드글자쓰기(number_VALUE[--number]);보드글자쓰기(10);
}
static assh_status_t Ettevalmistamine_Mälu(void *andmed,void **ADDRESS,size_t Suurus,enum assh_alloc_type_e 종류) {
    (void)andmed;(void)종류;
    if(!Suurus){vabastama_kauge(*ADDRESS);*ADDRESS=0;return ASSH_OK;}
    void *새주소=원격재할당(*ADDRESS,Suurus);
    if(!새주소)return ASSH_ERR_MEM;*ADDRESS=새주소;return ASSH_OK;
}
static assh_status_t Ettevalmistamine_juhuslik(struct assh_context_s *andmed,const struct assh_buffer_s *lähteväärtus) {
    (void)andmed;(void)lähteväärtus;unsigned char 시험[32];int TULEMUS=kauge_juhuslik(시험,sizeof(시험));memset(시험,0,sizeof(시험));
    return TULEMUS?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *andmed,uint8_t *TULEMUS,size_t 길이,uint_fast8_t 종류) {
    (void)andmed;(void)종류;if(길이>65536)return ASSH_ERR_CRYPTO;
    return kauge_juhuslik(TULEMUS,길이)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void juhuslik_lõpeta_kõne(struct assh_context_s *andmed){(void)andmed;}
static const struct assh_prng_s juhuslik_generaator={Ettevalmistamine_juhuslik,난수받기,juhuslik_lõpeta_kõne};
static void Sule_ühendus(void) {
    인증됨=셸시작됨=0;Kanal_kirje=0;
    if(ühendus_e05f319b)assh_session_release(ühendus_e05f319b);ühendus_e05f319b=0;
    if(partner_VALUE>=0)Sule_võrk(partner_VALUE);partner_VALUE=-1;käsk_TYPE=0;lõpeta_kõne_Olek=-1;닫을예정=0;
    입력앞=입력수=출력앞=toodang_COUNT=이전출력=0;재접속시각=보드밀리초()+250;
}
int 원격입력넣기(const unsigned char *andmed,unsigned number) {
    if(number>sizeof(입력줄)-입력수)return -11;
    for(unsigned 순번=0;순번<number;순번++)입력줄[(입력앞+입력수++)%sizeof(입력줄)]=andmed[순번];return number;
}
int 원격입력(void) {
    if(!입력수)return -1;int märk_VALUE=입력줄[입력앞];입력앞=(입력앞+1)%sizeof(입력줄);입력수--;return märk_VALUE;
}
void kauge_toodang(unsigned char märk_VALUE) {
    if(!셸시작됨||닫을예정)return;
    unsigned Lisa_MODE=märk_VALUE==10&&이전출력!=13;
    if(toodang_COUNT+1+Lisa_MODE>sizeof(toodang_liin)){닫을예정=2;return;}
    if(Lisa_MODE)toodang_liin[(출력앞+toodang_COUNT++)%sizeof(toodang_liin)]=13;
    toodang_liin[(출력앞+toodang_COUNT++)%sizeof(toodang_liin)]=märk_VALUE;이전출력=märk_VALUE;
}
uintptr_t Tahvel_lõpeta_kõne_kauge_käsk(uintptr_t Olek_VALUE){if(셸시작됨&&käsk_TYPE)lõpeta_kõne_Olek=(int)Olek_VALUE;return 0;}
uintptr_t Tahvel_kauge_Oota(uintptr_t Olek_VALUE){kest_Ootamine=Olek_VALUE!=0;return 0;}
static int Ettevalmistamine_kest(void) {
    if(Kuulamine_osaleja>=0)return 0;
    if(!kontekst_VALUE){
        assh_status_t VIGA=assh_context_create(&kontekst_VALUE,ASSH_SERVER,Ettevalmistamine_Mälu,0,&juhuslik_generaator,0);
        if(VIGA)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *meetod_MODE[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        VIGA=assh_algo_register(kontekst_VALUE,ASSH_SAFETY_WEAK,meetod_MODE);
        if(!VIGA)VIGA=assh_service_register_va(kontekst_VALUE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=seade_Võti;
        if(!VIGA)VIGA=assh_key_load(kontekst_VALUE,assh_context_keys(kontekst_VALUE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(seade_Võti));
        if(VIGA){진단("SSH init error ",VIGA);assh_context_release(kontekst_VALUE);kontekst_VALUE=0;return -5;}
    }
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int TULEMUS=NET_BIND(port_VALUE,0,22);if(!TULEMUS)TULEMUS=NET_jälgima(port_VALUE);
    if(TULEMUS<0){Sule_võrk(port_VALUE);return TULEMUS;}Kuulamine_osaleja=port_VALUE;return 0;
}
uintptr_t Tahvel_varikasutus(uintptr_t 종류,uintptr_t Nimi) {
    if(종류==1)return(uint32_t)meede_kauge_ekraan(Nimi);
    if(Nimi==0){Sule_ühendus();if(Kuulamine_osaleja>=0)Sule_võrk(Kuulamine_osaleja);Kuulamine_osaleja=-1;return 0;}
    if(Nimi==1){käivitus_tõrge=Ettevalmistamine_kest();return(uint32_t)käivitus_tõrge;}
    return(uint32_t)(Kuulamine_osaleja>=0?1:käivitus_tõrge);
}
void Ettevalmistamine_kauge(void){käivitus_tõrge=Ettevalmistamine_kest();meede_kauge_ekraan(1);}
static int 같은말(const struct assh_cbuffer_s *andmed,const char *Word_SMS) {
    size_t 길이=strlen(Word_SMS);return andmed->size==길이&&!memcmp(andmed->data,Word_SMS,길이);
}
static int terminal_päring(const struct assh_cbuffer_s *andmed) {
    if(andmed->size<24)return 0;
    const unsigned char *andmed_ametikoht=andmed->data;unsigned 길이=assh_load_u32(andmed_ametikoht);
    if(길이>128||andmed->size<길이+24)return 0;
    unsigned MODE_VALUE=assh_load_u32(andmed_ametikoht+4+길이+16);
    return MODE_VALUE<=2048&&andmed->size==길이+24+MODE_VALUE;
}
static void pide_päring(struct assh_event_request_s *Sündmus) {
    if(!인증됨||Sündmus->ch!=Kanal_kirje||!Kanal_kirje)return;
    if(같은말(&Sündmus->type,"pty-req")) {
        if(!셸시작됨&&terminal_päring(&Sündmus->rq_data))Sündmus->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Sündmus->type,"window-change")) {
        if(셸시작됨&&Sündmus->rq_data.size==16)Sündmus->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!kest_Ootamine)return;
    const unsigned char *Käsk=0;unsigned 길이=0;
    if(같은말(&Sündmus->type,"exec")) {
        if(Sündmus->rq_data.size<4)return;
        길이=assh_load_u32(Sündmus->rq_data.data);
        if(!길이||길이>2048||Sündmus->rq_data.size!=길이+4)return;
        Käsk=Sündmus->rq_data.data+4;
        for(unsigned 순번=0;순번<길이;순번++)if(!Käsk[순번])return;
        käsk_TYPE=1;
    }else if(!같은말(&Sündmus->type,"shell")||Sündmus->rq_data.size)return;
    if(sizeof(입력줄)-입력수<길이+2)return;
    const unsigned char 지움=21,끝=13;
    원격입력넣기(&지움,1);if(길이)원격입력넣기(Käsk,길이);원격입력넣기(&끝,1);
    셸시작됨=1;Sündmus->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!käsk_TYPE){const char *안내="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*안내)kauge_toodang(*안내++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Kuulamine_osaleja<0)return;
    uintptr_t NOW_VALUE=보드밀리초();
    if(partner_VALUE<0){if(NOW_VALUE<재접속시각)return;partner_VALUE=NET_aktsepteerima(Kuulamine_osaleja);if(partner_VALUE<0)return;
        ühendus_Aeg=NOW_VALUE;assh_status_t VIGA=assh_session_create(kontekst_VALUE,&ühendus_e05f319b);
        if(VIGA){ühendus_e05f319b=0;진단("SSH session error ",VIGA);Sule_ühendus();return;}}
    if((!인증됨&&NOW_VALUE-ühendus_Aeg>30000)||닫을예정==2||(닫을예정&&NOW_VALUE>=sulgemine_Aeg)){Sule_ühendus();return;}
    if(Kanal_kirje&&셸시작됨&&!닫을예정) {
        if(toodang_COUNT){size_t number=sizeof(toodang_liin)-출력앞;if(number>toodang_COUNT)number=toodang_COUNT;if(number>2048)number=2048;
            assh_status_t VIGA=assh_channel_data(Kanal_kirje,toodang_liin+출력앞,&number);
            if(!VIGA){출력앞=(출력앞+number)%sizeof(toodang_liin);toodang_COUNT-=number;}
            else if(VIGA!=ASSH_NO_DATA){Sule_ühendus();return;}
        }
        if(lõpeta_kõne_Olek>=0&&!toodang_COUNT){unsigned char Olek_VALUE[4];assh_store_u32(Olek_VALUE,(uint32_t)lõpeta_kõne_Olek);
            if(assh_request(ühendus_e05f319b,Kanal_kirje,"exit-status",11,Olek_VALUE,4,0)||assh_channel_eof(Kanal_kirje)||assh_channel_close(Kanal_kirje)) {Sule_ühendus();return;}
            닫을예정=1;sulgemine_Aeg=NOW_VALUE+3000;
        }
    }
    for(unsigned SEQUENCE_VALUE=0;SEQUENCE_VALUE<16;SEQUENCE_VALUE++) {
        struct assh_event_s Sündmus;
        if(!assh_event_get(ühendus_e05f319b,&Sündmus,NOW_VALUE/1000)){Sule_ühendus();return;}
        assh_status_t VIGA=ASSH_OK;int 쉬기=0,ühendust_katkestama_osaleja=0;
        switch(Sündmus.id) {
        case ASSH_EVENT_READ: {
            int number=통신읽기(partner_VALUE,Sündmus.transport.read.buf.data,Sündmus.transport.read.buf.size);
            if(number>0)Sündmus.transport.read.transferred=number;
            else if(number==-11)쉬기=1;else ühendust_katkestama_osaleja=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int number=NET_kirjutamine(partner_VALUE,Sündmus.transport.write.buf.data,Sündmus.transport.write.buf.size);
            if(number>0)Sündmus.transport.write.transferred=number;
            else if(number==-11)쉬기=1;else ühendust_katkestama_osaleja=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Sündmus.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Sündmus.userauth_server.methods.retries>3)Sündmus.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *andmed=&Sündmus.userauth_server.password;
            if(같은말(&andmed->username,"user")&&andmed->password.size<=256&&!andmed->new_password.size) {
                unsigned char kokkuvõte_VALUE[32];kauge_kokkuvõte(andmed->password.data,andmed->password.size,kokkuvõte_VALUE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=kokkuvõte_VALUE[순번]^kest_parool_kokkuvõte[순번];memset(kokkuvõte_VALUE,0,32);
                if(!차이)andmed->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *andmed=&Sündmus.connection.channel_open;
            if(인증됨&&!Kanal_kirje&&kest_Ootamine&&같은말(&andmed->type,"session")&&!andmed->rq_data.size) {
                andmed->reply=ASSH_CONNECTION_REPLY_SUCCESS;andmed->pkt_size=4096;
                andmed->win_size=-1;Kanal_kirje=andmed->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: pide_päring(&Sündmus.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *andmed=&Sündmus.connection.channel_data;
            if(!셸시작됨||andmed->ch!=Kanal_kirje||andmed->ext){ühendust_katkestama_osaleja=1;break;}
            unsigned number=andmed->data.size;if(number>sizeof(입력줄)-입력수)number=sizeof(입력줄)-입력수;
            for(unsigned 순번=0;순번<number;순번++)if(andmed->data.data[순번]==4){lõpeta_kõne_Olek=0;number=순번;andmed->transferred=andmed->data.size;break;}
            원격입력넣기(andmed->data.data,number);if(!andmed->transferred)andmed->transferred=number;
            if(!number&&lõpeta_kõne_Olek<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Kanal_kirje=0;셸시작됨=0;닫을예정=1;sulgemine_Aeg=NOW_VALUE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Sündmus.session.error.code);ühendust_katkestama_osaleja=1;break;
        case ASSH_EVENT_DISCONNECT: ühendust_katkestama_osaleja=1;break;
        default: break;
        }
        assh_event_done(ühendus_e05f319b,&Sündmus,VIGA);
        if(ühendust_katkestama_osaleja){Sule_ühendus();return;}if(쉬기)return;
    }
}
