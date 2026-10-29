/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "entferntWert.h"
#include "kryptographieUnterstützung.h"
#include "profil.h"
#include "../Netzwerkstapel/Netzwerkstapel.h"
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
extern uintptr_t platineVergangeneMillisekunden(void);
extern uintptr_t platineZeichenSchreiben(uintptr_t);
static struct assh_context_s *kontextWert;
static struct assh_session_s *verbindung;
static struct assh_channel_s *kanalEintrag;
static int lauschendEndpunkt=-1,gegenstelleWert=-1,istAuthentifiziert,befehlshülleGestartet,befehlTyp,endeStatuswert=-1,künftigSchließen,anlaufFehler,befehlshülleWartend;
static uintptr_t verbindungZeit,neuverbindenZeit,schließendZeit;
static unsigned char eingabeZeile[8192],ausgabeZeile[65536];
static unsigned eingabeKopf,eingabeAnzahl,ausgabeKopf,ausgabeAnzahl,vorherigAusgabe;
static void diagnoseWert(const char *maschinenwortText,unsigned Wert) {
    while(*maschinenwortText)platineZeichenSchreiben(*maschinenwortText++);
    char zifferWert[12];unsigned Zahl=0;do{zifferWert[Zahl++]='0'+Wert%10;Wert/=10;}while(Wert);
    while(Zahl)platineZeichenSchreiben(zifferWert[--Zahl]);platineZeichenSchreiben(10);
}
static assh_status_t speicherVorbereiten(void *Daten,void **adresse,size_t größe,enum assh_alloc_type_e artWert) {
    (void)Daten;(void)artWert;
    if(!größe){entferntFreigeben(*adresse);*adresse=0;return ASSH_OK;}
    void *neuAdresse=entferntNeuzuteilen(*adresse,größe);
    if(!neuAdresse)return ASSH_ERR_MEM;*adresse=neuAdresse;return ASSH_OK;
}
static assh_status_t zufälligVorbereiten(struct assh_context_s *Daten,const struct assh_buffer_s *startwertWert) {
    (void)Daten;(void)startwertWert;unsigned char Prüfungen[32];int ergebnis=entferntZufällig(Prüfungen,sizeof(Prüfungen));memset(Prüfungen,0,sizeof(Prüfungen));
    return ergebnis?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t zufälligLesen(struct assh_context_s *Daten,uint8_t *ergebnis,size_t Länge,uint_fast8_t artWert) {
    (void)Daten;(void)artWert;if(Länge>65536)return ASSH_ERR_CRYPTO;
    return entferntZufällig(ergebnis,Länge)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void zufälligEnde(struct assh_context_s *Daten){(void)Daten;}
static const struct assh_prng_s zufälligErzeuger={zufälligVorbereiten,zufälligLesen,zufälligEnde};
static void verbindungSchließen(void) {
    istAuthentifiziert=befehlshülleGestartet=0;kanalEintrag=0;
    if(verbindung)assh_session_release(verbindung);verbindung=0;
    if(gegenstelleWert>=0)netzwerkSchließen(gegenstelleWert);gegenstelleWert=-1;befehlTyp=0;endeStatuswert=-1;künftigSchließen=0;
    eingabeKopf=eingabeAnzahl=ausgabeKopf=ausgabeAnzahl=vorherigAusgabe=0;neuverbindenZeit=platineVergangeneMillisekunden()+250;
}
int zuführenEntferntEingabe(const unsigned char *Daten,unsigned Zahl) {
    if(Zahl>sizeof(eingabeZeile)-eingabeAnzahl)return -11;
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<Zahl;ordnungszahlIndex++)eingabeZeile[(eingabeKopf+eingabeAnzahl++)%sizeof(eingabeZeile)]=Daten[ordnungszahlIndex];return Zahl;
}
int entferntEingabe(void) {
    if(!eingabeAnzahl)return -1;int zeichenWert=eingabeZeile[eingabeKopf];eingabeKopf=(eingabeKopf+1)%sizeof(eingabeZeile);eingabeAnzahl--;return zeichenWert;
}
void entferntAusgabe(unsigned char zeichenWert) {
    if(!befehlshülleGestartet||künftigSchließen)return;
    unsigned betriebsartAnhängen=zeichenWert==10&&vorherigAusgabe!=13;
    if(ausgabeAnzahl+1+betriebsartAnhängen>sizeof(ausgabeZeile)){künftigSchließen=2;return;}
    if(betriebsartAnhängen)ausgabeZeile[(ausgabeKopf+ausgabeAnzahl++)%sizeof(ausgabeZeile)]=13;
    ausgabeZeile[(ausgabeKopf+ausgabeAnzahl++)%sizeof(ausgabeZeile)]=zeichenWert;vorherigAusgabe=zeichenWert;
}
uintptr_t platineEndeEntferntBefehl(uintptr_t statuswertWert){if(befehlshülleGestartet&&befehlTyp)endeStatuswert=(int)statuswertWert;return 0;}
uintptr_t platineEntferntWarten(uintptr_t statuswertWert){befehlshülleWartend=statuswertWert!=0;return 0;}
static int befehlshülleVorbereiten(void) {
    if(lauschendEndpunkt>=0)return 0;
    if(!kontextWert){
        assh_status_t fehler=assh_context_create(&kontextWert,ASSH_SERVER,speicherVorbereiten,0,&zufälligErzeuger,0);
        if(fehler)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *methodeBetriebsart[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        fehler=assh_algo_register(kontextWert,ASSH_SAFETY_WEAK,methodeBetriebsart);
        if(!fehler)fehler=assh_service_register_va(kontextWert,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *tasteMaterial=gerätTaste;
        if(!fehler)fehler=assh_key_load(kontextWert,assh_context_keys(kontextWert),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&tasteMaterial,sizeof(gerätTaste));
        if(fehler){diagnoseWert("SSH init error ",fehler);assh_context_release(kontextWert);kontextWert=0;return -5;}
    }
    int portWert=netzbuchseEndpunktErstellen(1);if(portWert<0)return portWert;wiederverwendenNetzbuchseAdresse(portWert);
    int ergebnis=netzZuordnen(portWert,0,22);if(!ergebnis)ergebnis=netzLauschen(portWert);
    if(ergebnis<0){netzwerkSchließen(portWert);return ergebnis;}lauschendEndpunkt=portWert;return 0;
}
uintptr_t platineEntferntSteuerung(uintptr_t artWert,uintptr_t aktion) {
    if(artWert==1)return(uint32_t)steuerungEntferntDarstellen(aktion);
    if(aktion==0){verbindungSchließen();if(lauschendEndpunkt>=0)netzwerkSchließen(lauschendEndpunkt);lauschendEndpunkt=-1;return 0;}
    if(aktion==1){anlaufFehler=befehlshülleVorbereiten();return(uint32_t)anlaufFehler;}
    return(uint32_t)(lauschendEndpunkt>=0?1:anlaufFehler);
}
void entferntVorbereiten(void){anlaufFehler=befehlshülleVorbereiten();steuerungEntferntDarstellen(1);}
static int passendMaschinenwort(const struct assh_cbuffer_s *Daten,const char *maschinenwortText) {
    size_t Länge=strlen(maschinenwortText);return Daten->size==Länge&&!memcmp(Daten->data,maschinenwortText,Länge);
}
static int terminalAnfrage(const struct assh_cbuffer_s *Daten) {
    if(Daten->size<24)return 0;
    const unsigned char *datenPosition=Daten->data;unsigned Länge=assh_load_u32(datenPosition);
    if(Länge>128||Daten->size<Länge+24)return 0;
    unsigned betriebsartWert=assh_load_u32(datenPosition+4+Länge+16);
    return betriebsartWert<=2048&&Daten->size==Länge+24+betriebsartWert;
}
static void kennwertAnfrage(struct assh_event_request_s *ereignis) {
    if(!istAuthentifiziert||ereignis->ch!=kanalEintrag||!kanalEintrag)return;
    if(passendMaschinenwort(&ereignis->type,"pty-req")) {
        if(!befehlshülleGestartet&&terminalAnfrage(&ereignis->rq_data))ereignis->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(passendMaschinenwort(&ereignis->type,"window-change")) {
        if(befehlshülleGestartet&&ereignis->rq_data.size==16)ereignis->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(befehlshülleGestartet||!befehlshülleWartend)return;
    const unsigned char *befehl=0;unsigned Länge=0;
    if(passendMaschinenwort(&ereignis->type,"exec")) {
        if(ereignis->rq_data.size<4)return;
        Länge=assh_load_u32(ereignis->rq_data.data);
        if(!Länge||Länge>2048||ereignis->rq_data.size!=Länge+4)return;
        befehl=ereignis->rq_data.data+4;
        for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<Länge;ordnungszahlIndex++)if(!befehl[ordnungszahlIndex])return;
        befehlTyp=1;
    }else if(!passendMaschinenwort(&ereignis->type,"shell")||ereignis->rq_data.size)return;
    if(sizeof(eingabeZeile)-eingabeAnzahl<Länge+2)return;
    const unsigned char gelöschtWert=21,endung=13;
    zuführenEntferntEingabe(&gelöschtWert,1);if(Länge)zuführenEntferntEingabe(befehl,Länge);zuführenEntferntEingabe(&endung,1);
    befehlshülleGestartet=1;ereignis->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!befehlTyp){const char *Anleitung="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*Anleitung)entferntAusgabe(*Anleitung++);}
}
void entferntUntersuchen(void) {
    entferntDarstellenUntersuchen();
    if(lauschendEndpunkt<0)return;
    uintptr_t jetztWert=platineVergangeneMillisekunden();
    if(gegenstelleWert<0){if(jetztWert<neuverbindenZeit)return;gegenstelleWert=netzAnnehmen(lauschendEndpunkt);if(gegenstelleWert<0)return;
        verbindungZeit=jetztWert;assh_status_t fehler=assh_session_create(kontextWert,&verbindung);
        if(fehler){verbindung=0;diagnoseWert("SSH session error ",fehler);verbindungSchließen();return;}}
    if((!istAuthentifiziert&&jetztWert-verbindungZeit>30000)||künftigSchließen==2||(künftigSchließen&&jetztWert>=schließendZeit)){verbindungSchließen();return;}
    if(kanalEintrag&&befehlshülleGestartet&&!künftigSchließen) {
        if(ausgabeAnzahl){size_t Zahl=sizeof(ausgabeZeile)-ausgabeKopf;if(Zahl>ausgabeAnzahl)Zahl=ausgabeAnzahl;if(Zahl>2048)Zahl=2048;
            assh_status_t fehler=assh_channel_data(kanalEintrag,ausgabeZeile+ausgabeKopf,&Zahl);
            if(!fehler){ausgabeKopf=(ausgabeKopf+Zahl)%sizeof(ausgabeZeile);ausgabeAnzahl-=Zahl;}
            else if(fehler!=ASSH_NO_DATA){verbindungSchließen();return;}
        }
        if(endeStatuswert>=0&&!ausgabeAnzahl){unsigned char statuswertWert[4];assh_store_u32(statuswertWert,(uint32_t)endeStatuswert);
            if(assh_request(verbindung,kanalEintrag,"exit-status",11,statuswertWert,4,0)||assh_channel_eof(kanalEintrag)||assh_channel_close(kanalEintrag)) {verbindungSchließen();return;}
            künftigSchließen=1;schließendZeit=jetztWert+3000;
        }
    }
    for(unsigned folgeWert=0;folgeWert<16;folgeWert++) {
        struct assh_event_s ereignis;
        if(!assh_event_get(verbindung,&ereignis,jetztWert/1000)){verbindungSchließen();return;}
        assh_status_t fehler=ASSH_OK;int übrigKurzzeitigTun=0,trennenEndpunkt=0;
        switch(ereignis.id) {
        case ASSH_EVENT_READ: {
            int Zahl=netzLesen(gegenstelleWert,ereignis.transport.read.buf.data,ereignis.transport.read.buf.size);
            if(Zahl>0)ereignis.transport.read.transferred=Zahl;
            else if(Zahl==-11)übrigKurzzeitigTun=1;else trennenEndpunkt=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int Zahl=netzSchreiben(gegenstelleWert,ereignis.transport.write.buf.data,ereignis.transport.write.buf.size);
            if(Zahl>0)ereignis.transport.write.transferred=Zahl;
            else if(Zahl==-11)übrigKurzzeitigTun=1;else trennenEndpunkt=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            ereignis.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(ereignis.userauth_server.methods.retries>3)ereignis.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *Daten=&ereignis.userauth_server.password;
            if(passendMaschinenwort(&Daten->username,"user")&&Daten->password.size<=256&&!Daten->new_password.size) {
                unsigned char zusammenfassungWert[32];entferntZusammenfassung(Daten->password.data,Daten->password.size,zusammenfassungWert);
                unsigned unterschiedWert=0;for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<32;ordnungszahlIndex++)unterschiedWert|=zusammenfassungWert[ordnungszahlIndex]^befehlshüllePasswortZusammenfassung[ordnungszahlIndex];memset(zusammenfassungWert,0,32);
                if(!unterschiedWert)Daten->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: istAuthentifiziert=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *Daten=&ereignis.connection.channel_open;
            if(istAuthentifiziert&&!kanalEintrag&&befehlshülleWartend&&passendMaschinenwort(&Daten->type,"session")&&!Daten->rq_data.size) {
                Daten->reply=ASSH_CONNECTION_REPLY_SUCCESS;Daten->pkt_size=4096;
                Daten->win_size=-1;kanalEintrag=Daten->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: kennwertAnfrage(&ereignis.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *Daten=&ereignis.connection.channel_data;
            if(!befehlshülleGestartet||Daten->ch!=kanalEintrag||Daten->ext){trennenEndpunkt=1;break;}
            unsigned Zahl=Daten->data.size;if(Zahl>sizeof(eingabeZeile)-eingabeAnzahl)Zahl=sizeof(eingabeZeile)-eingabeAnzahl;
            for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<Zahl;ordnungszahlIndex++)if(Daten->data.data[ordnungszahlIndex]==4){endeStatuswert=0;Zahl=ordnungszahlIndex;Daten->transferred=Daten->data.size;break;}
            zuführenEntferntEingabe(Daten->data.data,Zahl);if(!Daten->transferred)Daten->transferred=Zahl;
            if(!Zahl&&endeStatuswert<0)übrigKurzzeitigTun=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: kanalEintrag=0;befehlshülleGestartet=0;künftigSchließen=1;schließendZeit=jetztWert+1000;break;
        case ASSH_EVENT_SESSION_ERROR: istAuthentifiziert=befehlshülleGestartet=0;diagnoseWert("SSH error ",ereignis.session.error.code);trennenEndpunkt=1;break;
        case ASSH_EVENT_DISCONNECT: trennenEndpunkt=1;break;
        default: break;
        }
        assh_event_done(verbindung,&ereignis,fehler);
        if(trennenEndpunkt){verbindungSchließen();return;}if(übrigKurzzeitigTun)return;
    }
}
