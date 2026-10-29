/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "etä_ARVO.h"
#include "salaus_Tuki.h"
#include "Profiili.h"
#include "../verkko_Pino/verkko_Pino.h"
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
static struct assh_context_s *konteksti_ARVO;
static struct assh_session_s *yhteys_e05f319b;
static struct assh_channel_s *Media_merkintä;
static int Kuuntelee_päätepiste=-1,vertaissolmu_ARVO=-1,인증됨,셸시작됨,komento_TYYPPI,lopettaa_puhelu_Tila=-1,닫을예정,käynnistys_virhe,liittymä_Odotetaan;
static uintptr_t yhteys_AIKA,재접속시각,sulkeminen_AIKA;
static unsigned char syöte_rivi[8192],tulos_rivi[65536];
static unsigned 입력앞,syöte_LASKE,출력앞,tulos_LASKE,Edellinen_tulos;
static void 진단(const char *Word_SMS,unsigned ARVO) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char numero_ARVO[12];unsigned numero=0;do{numero_ARVO[numero++]='0'+ARVO%10;ARVO/=10;}while(ARVO);
    while(numero)보드글자쓰기(numero_ARVO[--numero]);보드글자쓰기(10);
}
static assh_status_t Valmistele_Muisti(void *data,void **OSOITE,size_t Koko,enum assh_alloc_type_e 종류) {
    (void)data;(void)종류;
    if(!Koko){julkaista_etä(*OSOITE);*OSOITE=0;return ASSH_OK;}
    void *새주소=원격재할당(*OSOITE,Koko);
    if(!새주소)return ASSH_ERR_MEM;*OSOITE=새주소;return ASSH_OK;
}
static assh_status_t 난수준비(struct assh_context_s *data,const struct assh_buffer_s *alkuarvo) {
    (void)data;(void)alkuarvo;unsigned char testit[32];int TULOS=원격난수(testit,sizeof(testit));memset(testit,0,sizeof(testit));
    return TULOS?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *data,uint8_t *TULOS,size_t kesto_ARVO,uint_fast8_t 종류) {
    (void)data;(void)종류;if(kesto_ARVO>65536)return ASSH_ERR_CRYPTO;
    return 원격난수(TULOS,kesto_ARVO)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void 난수끝(struct assh_context_s *data){(void)data;}
static const struct assh_prng_s 난수기={난수준비,난수받기,난수끝};
static void Sulje_yhteys(void) {
    인증됨=셸시작됨=0;Media_merkintä=0;
    if(yhteys_e05f319b)assh_session_release(yhteys_e05f319b);yhteys_e05f319b=0;
    if(vertaissolmu_ARVO>=0)Sulje_verkko(vertaissolmu_ARVO);vertaissolmu_ARVO=-1;komento_TYYPPI=0;lopettaa_puhelu_Tila=-1;닫을예정=0;
    입력앞=syöte_LASKE=출력앞=tulos_LASKE=Edellinen_tulos=0;재접속시각=보드밀리초()+250;
}
int syöte_etä_syöte(const unsigned char *data,unsigned numero) {
    if(numero>sizeof(syöte_rivi)-syöte_LASKE)return -11;
    for(unsigned 순번=0;순번<numero;순번++)syöte_rivi[(입력앞+syöte_LASKE++)%sizeof(syöte_rivi)]=data[순번];return numero;
}
int etä_syöte(void) {
    if(!syöte_LASKE)return -1;int merkki_ARVO=syöte_rivi[입력앞];입력앞=(입력앞+1)%sizeof(syöte_rivi);syöte_LASKE--;return merkki_ARVO;
}
void etä_tulos(unsigned char merkki_ARVO) {
    if(!셸시작됨||닫을예정)return;
    unsigned liitä_tila=merkki_ARVO==10&&Edellinen_tulos!=13;
    if(tulos_LASKE+1+liitä_tila>sizeof(tulos_rivi)){닫을예정=2;return;}
    if(liitä_tila)tulos_rivi[(출력앞+tulos_LASKE++)%sizeof(tulos_rivi)]=13;
    tulos_rivi[(출력앞+tulos_LASKE++)%sizeof(tulos_rivi)]=merkki_ARVO;Edellinen_tulos=merkki_ARVO;
}
uintptr_t Taulu_lopettaa_puhelu_etä_komento(uintptr_t Tila_ARVO){if(셸시작됨&&komento_TYYPPI)lopettaa_puhelu_Tila=(int)Tila_ARVO;return 0;}
uintptr_t Taulu_etä_odottaa(uintptr_t Tila_ARVO){liittymä_Odotetaan=Tila_ARVO!=0;return 0;}
static int Valmistele_liittymä(void) {
    if(Kuuntelee_päätepiste>=0)return 0;
    if(!konteksti_ARVO){
        assh_status_t VIRHE=assh_context_create(&konteksti_ARVO,ASSH_SERVER,Valmistele_Muisti,0,&난수기,0);
        if(VIRHE)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *menetelmä_tila[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        VIRHE=assh_algo_register(konteksti_ARVO,ASSH_SAFETY_WEAK,menetelmä_tila);
        if(!VIRHE)VIRHE=assh_service_register_va(konteksti_ARVO,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=laite_Avain;
        if(!VIRHE)VIRHE=assh_key_load(konteksti_ARVO,assh_context_keys(konteksti_ARVO),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(laite_Avain));
        if(VIRHE){진단("SSH init error ",VIRHE);assh_context_release(konteksti_ARVO);konteksti_ARVO=0;return -5;}
    }
    int portti_ARVO=Luo_vastake_päätepiste(1);if(portti_ARVO<0)return portti_ARVO;통신주소재사용(portti_ARVO);
    int TULOS=NET_BIND(portti_ARVO,0,22);if(!TULOS)TULOS=NET_kuunnella(portti_ARVO);
    if(TULOS<0){Sulje_verkko(portti_ARVO);return TULOS;}Kuuntelee_päätepiste=portti_ARVO;return 0;
}
uintptr_t Taulu_etähallinta(uintptr_t 종류,uintptr_t Toiminto) {
    if(종류==1)return(uint32_t)ohjain_etä_näyttö(Toiminto);
    if(Toiminto==0){Sulje_yhteys();if(Kuuntelee_päätepiste>=0)Sulje_verkko(Kuuntelee_päätepiste);Kuuntelee_päätepiste=-1;return 0;}
    if(Toiminto==1){käynnistys_virhe=Valmistele_liittymä();return(uint32_t)käynnistys_virhe;}
    return(uint32_t)(Kuuntelee_päätepiste>=0?1:käynnistys_virhe);
}
void Valmistele_etä(void){käynnistys_virhe=Valmistele_liittymä();ohjain_etä_näyttö(1);}
static int kohdistus_Word(const struct assh_cbuffer_s *data,const char *Word_SMS) {
    size_t kesto_ARVO=strlen(Word_SMS);return data->size==kesto_ARVO&&!memcmp(data->data,Word_SMS,kesto_ARVO);
}
static int Pääte_pyyntö(const struct assh_cbuffer_s *data) {
    if(data->size<24)return 0;
    const unsigned char *data_toimi=data->data;unsigned kesto_ARVO=assh_load_u32(data_toimi);
    if(kesto_ARVO>128||data->size<kesto_ARVO+24)return 0;
    unsigned tila_ARVO=assh_load_u32(data_toimi+4+kesto_ARVO+16);
    return tila_ARVO<=2048&&data->size==kesto_ARVO+24+tila_ARVO;
}
static void kahva_pyyntö(struct assh_event_request_s *Tapahtuma) {
    if(!인증됨||Tapahtuma->ch!=Media_merkintä||!Media_merkintä)return;
    if(kohdistus_Word(&Tapahtuma->type,"pty-req")) {
        if(!셸시작됨&&Pääte_pyyntö(&Tapahtuma->rq_data))Tapahtuma->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(kohdistus_Word(&Tapahtuma->type,"window-change")) {
        if(셸시작됨&&Tapahtuma->rq_data.size==16)Tapahtuma->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!liittymä_Odotetaan)return;
    const unsigned char *komento=0;unsigned kesto_ARVO=0;
    if(kohdistus_Word(&Tapahtuma->type,"exec")) {
        if(Tapahtuma->rq_data.size<4)return;
        kesto_ARVO=assh_load_u32(Tapahtuma->rq_data.data);
        if(!kesto_ARVO||kesto_ARVO>2048||Tapahtuma->rq_data.size!=kesto_ARVO+4)return;
        komento=Tapahtuma->rq_data.data+4;
        for(unsigned 순번=0;순번<kesto_ARVO;순번++)if(!komento[순번])return;
        komento_TYYPPI=1;
    }else if(!kohdistus_Word(&Tapahtuma->type,"shell")||Tapahtuma->rq_data.size)return;
    if(sizeof(syöte_rivi)-syöte_LASKE<kesto_ARVO+2)return;
    const unsigned char 지움=21,끝=13;
    syöte_etä_syöte(&지움,1);if(kesto_ARVO)syöte_etä_syöte(komento,kesto_ARVO);syöte_etä_syöte(&끝,1);
    셸시작됨=1;Tapahtuma->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!komento_TYYPPI){const char *Lueminut_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*Lueminut_eb81d7d9)etä_tulos(*Lueminut_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Kuuntelee_päätepiste<0)return;
    uintptr_t NYT_ARVO=보드밀리초();
    if(vertaissolmu_ARVO<0){if(NYT_ARVO<재접속시각)return;vertaissolmu_ARVO=NET_hyväksyä(Kuuntelee_päätepiste);if(vertaissolmu_ARVO<0)return;
        yhteys_AIKA=NYT_ARVO;assh_status_t VIRHE=assh_session_create(konteksti_ARVO,&yhteys_e05f319b);
        if(VIRHE){yhteys_e05f319b=0;진단("SSH session error ",VIRHE);Sulje_yhteys();return;}}
    if((!인증됨&&NYT_ARVO-yhteys_AIKA>30000)||닫을예정==2||(닫을예정&&NYT_ARVO>=sulkeminen_AIKA)){Sulje_yhteys();return;}
    if(Media_merkintä&&셸시작됨&&!닫을예정) {
        if(tulos_LASKE){size_t numero=sizeof(tulos_rivi)-출력앞;if(numero>tulos_LASKE)numero=tulos_LASKE;if(numero>2048)numero=2048;
            assh_status_t VIRHE=assh_channel_data(Media_merkintä,tulos_rivi+출력앞,&numero);
            if(!VIRHE){출력앞=(출력앞+numero)%sizeof(tulos_rivi);tulos_LASKE-=numero;}
            else if(VIRHE!=ASSH_NO_DATA){Sulje_yhteys();return;}
        }
        if(lopettaa_puhelu_Tila>=0&&!tulos_LASKE){unsigned char Tila_ARVO[4];assh_store_u32(Tila_ARVO,(uint32_t)lopettaa_puhelu_Tila);
            if(assh_request(yhteys_e05f319b,Media_merkintä,"exit-status",11,Tila_ARVO,4,0)||assh_channel_eof(Media_merkintä)||assh_channel_close(Media_merkintä)) {Sulje_yhteys();return;}
            닫을예정=1;sulkeminen_AIKA=NYT_ARVO+3000;
        }
    }
    for(unsigned JONO_ARVO=0;JONO_ARVO<16;JONO_ARVO++) {
        struct assh_event_s Tapahtuma;
        if(!assh_event_get(yhteys_e05f319b,&Tapahtuma,NYT_ARVO/1000)){Sulje_yhteys();return;}
        assh_status_t VIRHE=ASSH_OK;int 쉬기=0,katkaise_päätepiste=0;
        switch(Tapahtuma.id) {
        case ASSH_EVENT_READ: {
            int numero=NET_lukea(vertaissolmu_ARVO,Tapahtuma.transport.read.buf.data,Tapahtuma.transport.read.buf.size);
            if(numero>0)Tapahtuma.transport.read.transferred=numero;
            else if(numero==-11)쉬기=1;else katkaise_päätepiste=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int numero=NET_kirjoitus(vertaissolmu_ARVO,Tapahtuma.transport.write.buf.data,Tapahtuma.transport.write.buf.size);
            if(numero>0)Tapahtuma.transport.write.transferred=numero;
            else if(numero==-11)쉬기=1;else katkaise_päätepiste=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Tapahtuma.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Tapahtuma.userauth_server.methods.retries>3)Tapahtuma.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *data=&Tapahtuma.userauth_server.password;
            if(kohdistus_Word(&data->username,"user")&&data->password.size<=256&&!data->new_password.size) {
                unsigned char yhteenveto_ARVO[32];etä_yhteenveto(data->password.data,data->password.size,yhteenveto_ARVO);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=yhteenveto_ARVO[순번]^liittymä_salasana_yhteenveto[순번];memset(yhteenveto_ARVO,0,32);
                if(!차이)data->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *data=&Tapahtuma.connection.channel_open;
            if(인증됨&&!Media_merkintä&&liittymä_Odotetaan&&kohdistus_Word(&data->type,"session")&&!data->rq_data.size) {
                data->reply=ASSH_CONNECTION_REPLY_SUCCESS;data->pkt_size=4096;
                data->win_size=-1;Media_merkintä=data->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: kahva_pyyntö(&Tapahtuma.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *data=&Tapahtuma.connection.channel_data;
            if(!셸시작됨||data->ch!=Media_merkintä||data->ext){katkaise_päätepiste=1;break;}
            unsigned numero=data->data.size;if(numero>sizeof(syöte_rivi)-syöte_LASKE)numero=sizeof(syöte_rivi)-syöte_LASKE;
            for(unsigned 순번=0;순번<numero;순번++)if(data->data.data[순번]==4){lopettaa_puhelu_Tila=0;numero=순번;data->transferred=data->data.size;break;}
            syöte_etä_syöte(data->data.data,numero);if(!data->transferred)data->transferred=numero;
            if(!numero&&lopettaa_puhelu_Tila<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Media_merkintä=0;셸시작됨=0;닫을예정=1;sulkeminen_AIKA=NYT_ARVO+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Tapahtuma.session.error.code);katkaise_päätepiste=1;break;
        case ASSH_EVENT_DISCONNECT: katkaise_päätepiste=1;break;
        default: break;
        }
        assh_event_done(yhteys_e05f319b,&Tapahtuma,VIRHE);
        if(katkaise_päätepiste){Sulje_yhteys();return;}if(쉬기)return;
    }
}
