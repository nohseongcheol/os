/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "extern_WAARDE_28edcfa1.h"
#include "cryptografie_steun.h"
#include "Profiel.h"
#include "../net_stack/net_stack.h"
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
static struct assh_context_s *context_WAARDE;
static struct assh_session_s *verbinding_e05f319b;
static struct assh_channel_s *Kanaal_invoer;
static int Luisteren_eindpunt=-1,peer_WAARDE=-1,인증됨,셸시작됨,opdracht_TYPE,beëindigen_Status=-1,닫을예정,bootstrap_fout,Shell_Wachten;
static uintptr_t verbinding_TIJD,재접속시각,afsluiting_TIJD;
static unsigned char invoer_lijn[8192],uitvoer_lijn[65536];
static unsigned invoer_kop,invoer_AANTAL,uitvoer_kop,uitvoer_AANTAL,Vorige_uitvoer;
static void 진단(const char *Word_sms,unsigned WAARDE) {
    while(*Word_sms)보드글자쓰기(*Word_sms++);
    char cijfer_WAARDE[12];unsigned nummer=0;do{cijfer_WAARDE[nummer++]='0'+WAARDE%10;WAARDE/=10;}while(WAARDE);
    while(nummer)보드글자쓰기(cijfer_WAARDE[--nummer]);보드글자쓰기(10);
}
static assh_status_t Bereid_voor_Geheugen(void *gegevens,void **ADRES,size_t Grootte,enum assh_alloc_type_e soort_WAARDE) {
    (void)gegevens;(void)soort_WAARDE;
    if(!Grootte){versie_extern(*ADRES);*ADRES=0;return ASSH_OK;}
    void *새주소=원격재할당(*ADRES,Grootte);
    if(!새주소)return ASSH_ERR_MEM;*ADRES=새주소;return ASSH_OK;
}
static assh_status_t Bereid_voor_willekeurig(struct assh_context_s *gegevens,const struct assh_buffer_s *seed_waarde) {
    (void)gegevens;(void)seed_waarde;unsigned char tests[32];int resultaat=extern_willekeurig(tests,sizeof(tests));memset(tests,0,sizeof(tests));
    return resultaat?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *gegevens,uint8_t *resultaat,size_t tijdsduur_WAARDE,uint_fast8_t soort_WAARDE) {
    (void)gegevens;(void)soort_WAARDE;if(tijdsduur_WAARDE>65536)return ASSH_ERR_CRYPTO;
    return extern_willekeurig(resultaat,tijdsduur_WAARDE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void willekeurig_beëindigen(struct assh_context_s *gegevens){(void)gegevens;}
static const struct assh_prng_s willekeurig_generator={Bereid_voor_willekeurig,난수받기,willekeurig_beëindigen};
static void Sluiten_verbinding(void) {
    인증됨=셸시작됨=0;Kanaal_invoer=0;
    if(verbinding_e05f319b)assh_session_release(verbinding_e05f319b);verbinding_e05f319b=0;
    if(peer_WAARDE>=0)Sluiten_net(peer_WAARDE);peer_WAARDE=-1;opdracht_TYPE=0;beëindigen_Status=-1;닫을예정=0;
    invoer_kop=invoer_AANTAL=uitvoer_kop=uitvoer_AANTAL=Vorige_uitvoer=0;재접속시각=보드밀리초()+250;
}
int feed_extern_invoer(const unsigned char *gegevens,unsigned nummer) {
    if(nummer>sizeof(invoer_lijn)-invoer_AANTAL)return -11;
    for(unsigned 순번=0;순번<nummer;순번++)invoer_lijn[(invoer_kop+invoer_AANTAL++)%sizeof(invoer_lijn)]=gegevens[순번];return nummer;
}
int extern_invoer(void) {
    if(!invoer_AANTAL)return -1;int teken_WAARDE=invoer_lijn[invoer_kop];invoer_kop=(invoer_kop+1)%sizeof(invoer_lijn);invoer_AANTAL--;return teken_WAARDE;
}
void extern_uitvoer(unsigned char teken_WAARDE) {
    if(!셸시작됨||닫을예정)return;
    unsigned toevoegen_MODUS=teken_WAARDE==10&&Vorige_uitvoer!=13;
    if(uitvoer_AANTAL+1+toevoegen_MODUS>sizeof(uitvoer_lijn)){닫을예정=2;return;}
    if(toevoegen_MODUS)uitvoer_lijn[(uitvoer_kop+uitvoer_AANTAL++)%sizeof(uitvoer_lijn)]=13;
    uitvoer_lijn[(uitvoer_kop+uitvoer_AANTAL++)%sizeof(uitvoer_lijn)]=teken_WAARDE;Vorige_uitvoer=teken_WAARDE;
}
uintptr_t Bord_beëindigen_extern_opdracht(uintptr_t Status_WAARDE){if(셸시작됨&&opdracht_TYPE)beëindigen_Status=(int)Status_WAARDE;return 0;}
uintptr_t Bord_extern_wachten(uintptr_t Status_WAARDE){Shell_Wachten=Status_WAARDE!=0;return 0;}
static int Bereid_voor_Shell(void) {
    if(Luisteren_eindpunt>=0)return 0;
    if(!context_WAARDE){
        assh_status_t fout=assh_context_create(&context_WAARDE,ASSH_SERVER,Bereid_voor_Geheugen,0,&willekeurig_generator,0);
        if(fout)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *methode_MODUS[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        fout=assh_algo_register(context_WAARDE,ASSH_SAFETY_WEAK,methode_MODUS);
        if(!fout)fout=assh_service_register_va(context_WAARDE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *열쇠=mobiel_toets;
        if(!fout)fout=assh_key_load(context_WAARDE,assh_context_keys(context_WAARDE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&열쇠,sizeof(mobiel_toets));
        if(fout){진단("SSH init error ",fout);assh_context_release(context_WAARDE);context_WAARDE=0;return -5;}
    }
    int poort_WAARDE=maken_socket_eindpunt(1);if(poort_WAARDE<0)return poort_WAARDE;통신주소재사용(poort_WAARDE);
    int resultaat=NET_BIND(poort_WAARDE,0,22);if(!resultaat)resultaat=연결기다리기(poort_WAARDE);
    if(resultaat<0){Sluiten_net(poort_WAARDE);return resultaat;}Luisteren_eindpunt=poort_WAARDE;return 0;
}
uintptr_t Bord_extern_beheer(uintptr_t soort_WAARDE,uintptr_t Actie) {
    if(soort_WAARDE==1)return(uint32_t)controle_extern_weergeven(Actie);
    if(Actie==0){Sluiten_verbinding();if(Luisteren_eindpunt>=0)Sluiten_net(Luisteren_eindpunt);Luisteren_eindpunt=-1;return 0;}
    if(Actie==1){bootstrap_fout=Bereid_voor_Shell();return(uint32_t)bootstrap_fout;}
    return(uint32_t)(Luisteren_eindpunt>=0?1:bootstrap_fout);
}
void Bereid_voor_extern(void){bootstrap_fout=Bereid_voor_Shell();controle_extern_weergeven(1);}
static int vereffenen_Word(const struct assh_cbuffer_s *gegevens,const char *Word_sms) {
    size_t tijdsduur_WAARDE=strlen(Word_sms);return gegevens->size==tijdsduur_WAARDE&&!memcmp(gegevens->data,Word_sms,tijdsduur_WAARDE);
}
static int Terminal_aanvraag(const struct assh_cbuffer_s *gegevens) {
    if(gegevens->size<24)return 0;
    const unsigned char *gegevens_functie=gegevens->data;unsigned tijdsduur_WAARDE=assh_load_u32(gegevens_functie);
    if(tijdsduur_WAARDE>128||gegevens->size<tijdsduur_WAARDE+24)return 0;
    unsigned MODUS_WAARDE=assh_load_u32(gegevens_functie+4+tijdsduur_WAARDE+16);
    return MODUS_WAARDE<=2048&&gegevens->size==tijdsduur_WAARDE+24+MODUS_WAARDE;
}
static void greep_aanvraag(struct assh_event_request_s *Gebeurtenis) {
    if(!인증됨||Gebeurtenis->ch!=Kanaal_invoer||!Kanaal_invoer)return;
    if(vereffenen_Word(&Gebeurtenis->type,"pty-req")) {
        if(!셸시작됨&&Terminal_aanvraag(&Gebeurtenis->rq_data))Gebeurtenis->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(vereffenen_Word(&Gebeurtenis->type,"window-change")) {
        if(셸시작됨&&Gebeurtenis->rq_data.size==16)Gebeurtenis->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!Shell_Wachten)return;
    const unsigned char *opdracht=0;unsigned tijdsduur_WAARDE=0;
    if(vereffenen_Word(&Gebeurtenis->type,"exec")) {
        if(Gebeurtenis->rq_data.size<4)return;
        tijdsduur_WAARDE=assh_load_u32(Gebeurtenis->rq_data.data);
        if(!tijdsduur_WAARDE||tijdsduur_WAARDE>2048||Gebeurtenis->rq_data.size!=tijdsduur_WAARDE+4)return;
        opdracht=Gebeurtenis->rq_data.data+4;
        for(unsigned 순번=0;순번<tijdsduur_WAARDE;순번++)if(!opdracht[순번])return;
        opdracht_TYPE=1;
    }else if(!vereffenen_Word(&Gebeurtenis->type,"shell")||Gebeurtenis->rq_data.size)return;
    if(sizeof(invoer_lijn)-invoer_AANTAL<tijdsduur_WAARDE+2)return;
    const unsigned char 지움=21,끝=13;
    feed_extern_invoer(&지움,1);if(tijdsduur_WAARDE)feed_extern_invoer(opdracht,tijdsduur_WAARDE);feed_extern_invoer(&끝,1);
    셸시작됨=1;Gebeurtenis->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!opdracht_TYPE){const char *LEESMIJ_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*LEESMIJ_eb81d7d9)extern_uitvoer(*LEESMIJ_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Luisteren_eindpunt<0)return;
    uintptr_t NU_WAARDE=보드밀리초();
    if(peer_WAARDE<0){if(NU_WAARDE<재접속시각)return;peer_WAARDE=NET_accepteren(Luisteren_eindpunt);if(peer_WAARDE<0)return;
        verbinding_TIJD=NU_WAARDE;assh_status_t fout=assh_session_create(context_WAARDE,&verbinding_e05f319b);
        if(fout){verbinding_e05f319b=0;진단("SSH session error ",fout);Sluiten_verbinding();return;}}
    if((!인증됨&&NU_WAARDE-verbinding_TIJD>30000)||닫을예정==2||(닫을예정&&NU_WAARDE>=afsluiting_TIJD)){Sluiten_verbinding();return;}
    if(Kanaal_invoer&&셸시작됨&&!닫을예정) {
        if(uitvoer_AANTAL){size_t nummer=sizeof(uitvoer_lijn)-uitvoer_kop;if(nummer>uitvoer_AANTAL)nummer=uitvoer_AANTAL;if(nummer>2048)nummer=2048;
            assh_status_t fout=assh_channel_data(Kanaal_invoer,uitvoer_lijn+uitvoer_kop,&nummer);
            if(!fout){uitvoer_kop=(uitvoer_kop+nummer)%sizeof(uitvoer_lijn);uitvoer_AANTAL-=nummer;}
            else if(fout!=ASSH_NO_DATA){Sluiten_verbinding();return;}
        }
        if(beëindigen_Status>=0&&!uitvoer_AANTAL){unsigned char Status_WAARDE[4];assh_store_u32(Status_WAARDE,(uint32_t)beëindigen_Status);
            if(assh_request(verbinding_e05f319b,Kanaal_invoer,"exit-status",11,Status_WAARDE,4,0)||assh_channel_eof(Kanaal_invoer)||assh_channel_close(Kanaal_invoer)) {Sluiten_verbinding();return;}
            닫을예정=1;afsluiting_TIJD=NU_WAARDE+3000;
        }
    }
    for(unsigned REEKS_WAARDE=0;REEKS_WAARDE<16;REEKS_WAARDE++) {
        struct assh_event_s Gebeurtenis;
        if(!assh_event_get(verbinding_e05f319b,&Gebeurtenis,NU_WAARDE/1000)){Sluiten_verbinding();return;}
        assh_status_t fout=ASSH_OK;int 쉬기=0,verbinding_verbreken_eindpunt=0;
        switch(Gebeurtenis.id) {
        case ASSH_EVENT_READ: {
            int nummer=통신읽기(peer_WAARDE,Gebeurtenis.transport.read.buf.data,Gebeurtenis.transport.read.buf.size);
            if(nummer>0)Gebeurtenis.transport.read.transferred=nummer;
            else if(nummer==-11)쉬기=1;else verbinding_verbreken_eindpunt=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int nummer=NET_schrijven(peer_WAARDE,Gebeurtenis.transport.write.buf.data,Gebeurtenis.transport.write.buf.size);
            if(nummer>0)Gebeurtenis.transport.write.transferred=nummer;
            else if(nummer==-11)쉬기=1;else verbinding_verbreken_eindpunt=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Gebeurtenis.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Gebeurtenis.userauth_server.methods.retries>3)Gebeurtenis.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *gegevens=&Gebeurtenis.userauth_server.password;
            if(vereffenen_Word(&gegevens->username,"user")&&gegevens->password.size<=256&&!gegevens->new_password.size) {
                unsigned char samenvatting_WAARDE[32];extern_samenvatting(gegevens->password.data,gegevens->password.size,samenvatting_WAARDE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=samenvatting_WAARDE[순번]^Shell_wachtwoord_samenvatting[순번];memset(samenvatting_WAARDE,0,32);
                if(!차이)gegevens->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *gegevens=&Gebeurtenis.connection.channel_open;
            if(인증됨&&!Kanaal_invoer&&Shell_Wachten&&vereffenen_Word(&gegevens->type,"session")&&!gegevens->rq_data.size) {
                gegevens->reply=ASSH_CONNECTION_REPLY_SUCCESS;gegevens->pkt_size=4096;
                gegevens->win_size=-1;Kanaal_invoer=gegevens->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: greep_aanvraag(&Gebeurtenis.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *gegevens=&Gebeurtenis.connection.channel_data;
            if(!셸시작됨||gegevens->ch!=Kanaal_invoer||gegevens->ext){verbinding_verbreken_eindpunt=1;break;}
            unsigned nummer=gegevens->data.size;if(nummer>sizeof(invoer_lijn)-invoer_AANTAL)nummer=sizeof(invoer_lijn)-invoer_AANTAL;
            for(unsigned 순번=0;순번<nummer;순번++)if(gegevens->data.data[순번]==4){beëindigen_Status=0;nummer=순번;gegevens->transferred=gegevens->data.size;break;}
            feed_extern_invoer(gegevens->data.data,nummer);if(!gegevens->transferred)gegevens->transferred=nummer;
            if(!nummer&&beëindigen_Status<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Kanaal_invoer=0;셸시작됨=0;닫을예정=1;afsluiting_TIJD=NU_WAARDE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Gebeurtenis.session.error.code);verbinding_verbreken_eindpunt=1;break;
        case ASSH_EVENT_DISCONNECT: verbinding_verbreken_eindpunt=1;break;
        default: break;
        }
        assh_event_done(verbinding_e05f319b,&Gebeurtenis,fout);
        if(verbinding_verbreken_eindpunt){Sluiten_verbinding();return;}if(쉬기)return;
    }
}
