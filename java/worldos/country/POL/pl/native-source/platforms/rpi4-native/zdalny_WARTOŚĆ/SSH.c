/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "zdalny_WARTOŚĆ.h"
#include "kryptografia_wsparcie.h"
#include "Profil.h"
#include "../sieć_Stos/sieć_Stos.h"
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
static struct assh_context_s *kontekst_WARTOŚĆ;
static struct assh_session_s *połączenie_e05f319b;
static struct assh_channel_s *Kanał_wpis;
static int Nasłuchiwanie_uczestnik=-1,węzeł_równorzędny_WARTOŚĆ=-1,인증됨,셸시작됨,polecenie_TYP,Koniec_Stan=-1,닫을예정,uruchomienie_błąd,powłoka_Czekam;
static uintptr_t połączenie_CZAS,재접속시각,zamknięcie_CZAS;
static unsigned char wejście_linia[8192],produkt_wyjściowy_linia[65536];
static unsigned 입력앞,wejście_ILE_LICZB,출력앞,produkt_wyjściowy_ILE_LICZB,Wstecz_produkt_wyjściowy;
static void 진단(const char *Word_SMS,unsigned WARTOŚĆ) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char cyfra_WARTOŚĆ[12];unsigned identyfikator=0;do{cyfra_WARTOŚĆ[identyfikator++]='0'+WARTOŚĆ%10;WARTOŚĆ/=10;}while(WARTOŚĆ);
    while(identyfikator)보드글자쓰기(cyfra_WARTOŚĆ[--identyfikator]);보드글자쓰기(10);
}
static assh_status_t Przygotuj_Pamięć(void *dane,void **Adres,size_t Rozmiar,enum assh_alloc_type_e Rodzaj_WARTOŚĆ) {
    (void)dane;(void)Rodzaj_WARTOŚĆ;
    if(!Rozmiar){wersja_zdalny(*Adres);*Adres=0;return ASSH_OK;}
    void *새주소=원격재할당(*Adres,Rozmiar);
    if(!새주소)return ASSH_ERR_MEM;*Adres=새주소;return ASSH_OK;
}
static assh_status_t Przygotuj_losowy(struct assh_context_s *dane,const struct assh_buffer_s *wartość_inicjatora) {
    (void)dane;(void)wartość_inicjatora;unsigned char testy[32];int WYNIK=zdalny_losowy(testy,sizeof(testy));memset(testy,0,sizeof(testy));
    return WYNIK?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *dane,uint8_t *WYNIK,size_t długość_WARTOŚĆ,uint_fast8_t Rodzaj_WARTOŚĆ) {
    (void)dane;(void)Rodzaj_WARTOŚĆ;if(długość_WARTOŚĆ>65536)return ASSH_ERR_CRYPTO;
    return zdalny_losowy(WYNIK,długość_WARTOŚĆ)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void losowy_Koniec(struct assh_context_s *dane){(void)dane;}
static const struct assh_prng_s losowy_generator={Przygotuj_losowy,난수받기,losowy_Koniec};
static void Zamknij_połączenie(void) {
    인증됨=셸시작됨=0;Kanał_wpis=0;
    if(połączenie_e05f319b)assh_session_release(połączenie_e05f319b);połączenie_e05f319b=0;
    if(węzeł_równorzędny_WARTOŚĆ>=0)Zamknij_sieć(węzeł_równorzędny_WARTOŚĆ);węzeł_równorzędny_WARTOŚĆ=-1;polecenie_TYP=0;Koniec_Stan=-1;닫을예정=0;
    입력앞=wejście_ILE_LICZB=출력앞=produkt_wyjściowy_ILE_LICZB=Wstecz_produkt_wyjściowy=0;재접속시각=보드밀리초()+250;
}
int kanał_zdalny_wejście(const unsigned char *dane,unsigned identyfikator) {
    if(identyfikator>sizeof(wejście_linia)-wejście_ILE_LICZB)return -11;
    for(unsigned 순번=0;순번<identyfikator;순번++)wejście_linia[(입력앞+wejście_ILE_LICZB++)%sizeof(wejście_linia)]=dane[순번];return identyfikator;
}
int zdalny_wejście(void) {
    if(!wejście_ILE_LICZB)return -1;int znak_WARTOŚĆ=wejście_linia[입력앞];입력앞=(입력앞+1)%sizeof(wejście_linia);wejście_ILE_LICZB--;return znak_WARTOŚĆ;
}
void zdalny_produkt_wyjściowy(unsigned char znak_WARTOŚĆ) {
    if(!셸시작됨||닫을예정)return;
    unsigned dołączać_tryb=znak_WARTOŚĆ==10&&Wstecz_produkt_wyjściowy!=13;
    if(produkt_wyjściowy_ILE_LICZB+1+dołączać_tryb>sizeof(produkt_wyjściowy_linia)){닫을예정=2;return;}
    if(dołączać_tryb)produkt_wyjściowy_linia[(출력앞+produkt_wyjściowy_ILE_LICZB++)%sizeof(produkt_wyjściowy_linia)]=13;
    produkt_wyjściowy_linia[(출력앞+produkt_wyjściowy_ILE_LICZB++)%sizeof(produkt_wyjściowy_linia)]=znak_WARTOŚĆ;Wstecz_produkt_wyjściowy=znak_WARTOŚĆ;
}
uintptr_t Tablica_Koniec_zdalny_polecenie(uintptr_t Stan_WARTOŚĆ){if(셸시작됨&&polecenie_TYP)Koniec_Stan=(int)Stan_WARTOŚĆ;return 0;}
uintptr_t Tablica_zdalny_chwileczkę(uintptr_t Stan_WARTOŚĆ){powłoka_Czekam=Stan_WARTOŚĆ!=0;return 0;}
static int Przygotuj_powłoka(void) {
    if(Nasłuchiwanie_uczestnik>=0)return 0;
    if(!kontekst_WARTOŚĆ){
        assh_status_t błąd=assh_context_create(&kontekst_WARTOŚĆ,ASSH_SERVER,Przygotuj_Pamięć,0,&losowy_generator,0);
        if(błąd)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metoda_tryb[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        błąd=assh_algo_register(kontekst_WARTOŚĆ,ASSH_SAFETY_WEAK,metoda_tryb);
        if(!błąd)błąd=assh_service_register_va(kontekst_WARTOŚĆ,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *Klucz_materiał=urządzenie_Klucz;
        if(!błąd)błąd=assh_key_load(kontekst_WARTOŚĆ,assh_context_keys(kontekst_WARTOŚĆ),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&Klucz_materiał,sizeof(urządzenie_Klucz));
        if(błąd){진단("SSH init error ",błąd);assh_context_release(kontekst_WARTOŚĆ);kontekst_WARTOŚĆ=0;return -5;}
    }
    int port_WARTOŚĆ=Twórca_gniazdo_uczestnik(1);if(port_WARTOŚĆ<0)return port_WARTOŚĆ;통신주소재사용(port_WARTOŚĆ);
    int WYNIK=NET_BIND(port_WARTOŚĆ,0,22);if(!WYNIK)WYNIK=NET_nasłuchiwać(port_WARTOŚĆ);
    if(WYNIK<0){Zamknij_sieć(port_WARTOŚĆ);return WYNIK;}Nasłuchiwanie_uczestnik=port_WARTOŚĆ;return 0;
}
uintptr_t Tablica_obserwowanie(uintptr_t Rodzaj_WARTOŚĆ,uintptr_t Akcja) {
    if(Rodzaj_WARTOŚĆ==1)return(uint32_t)kontrola_zdalny_wyświetlać(Akcja);
    if(Akcja==0){Zamknij_połączenie();if(Nasłuchiwanie_uczestnik>=0)Zamknij_sieć(Nasłuchiwanie_uczestnik);Nasłuchiwanie_uczestnik=-1;return 0;}
    if(Akcja==1){uruchomienie_błąd=Przygotuj_powłoka();return(uint32_t)uruchomienie_błąd;}
    return(uint32_t)(Nasłuchiwanie_uczestnik>=0?1:uruchomienie_błąd);
}
void Przygotuj_zdalny(void){uruchomienie_błąd=Przygotuj_powłoka();kontrola_zdalny_wyświetlać(1);}
static int 같은말(const struct assh_cbuffer_s *dane,const char *Word_SMS) {
    size_t długość_WARTOŚĆ=strlen(Word_SMS);return dane->size==długość_WARTOŚĆ&&!memcmp(dane->data,Word_SMS,długość_WARTOŚĆ);
}
static int Terminal_żądanie(const struct assh_cbuffer_s *dane) {
    if(dane->size<24)return 0;
    const unsigned char *dane_stanowisko=dane->data;unsigned długość_WARTOŚĆ=assh_load_u32(dane_stanowisko);
    if(długość_WARTOŚĆ>128||dane->size<długość_WARTOŚĆ+24)return 0;
    unsigned tryb_WARTOŚĆ=assh_load_u32(dane_stanowisko+4+długość_WARTOŚĆ+16);
    return tryb_WARTOŚĆ<=2048&&dane->size==długość_WARTOŚĆ+24+tryb_WARTOŚĆ;
}
static void uchwyt_żądanie(struct assh_event_request_s *Wydarzenie) {
    if(!인증됨||Wydarzenie->ch!=Kanał_wpis||!Kanał_wpis)return;
    if(같은말(&Wydarzenie->type,"pty-req")) {
        if(!셸시작됨&&Terminal_żądanie(&Wydarzenie->rq_data))Wydarzenie->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Wydarzenie->type,"window-change")) {
        if(셸시작됨&&Wydarzenie->rq_data.size==16)Wydarzenie->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!powłoka_Czekam)return;
    const unsigned char *polecenie=0;unsigned długość_WARTOŚĆ=0;
    if(같은말(&Wydarzenie->type,"exec")) {
        if(Wydarzenie->rq_data.size<4)return;
        długość_WARTOŚĆ=assh_load_u32(Wydarzenie->rq_data.data);
        if(!długość_WARTOŚĆ||długość_WARTOŚĆ>2048||Wydarzenie->rq_data.size!=długość_WARTOŚĆ+4)return;
        polecenie=Wydarzenie->rq_data.data+4;
        for(unsigned 순번=0;순번<długość_WARTOŚĆ;순번++)if(!polecenie[순번])return;
        polecenie_TYP=1;
    }else if(!같은말(&Wydarzenie->type,"shell")||Wydarzenie->rq_data.size)return;
    if(sizeof(wejście_linia)-wejście_ILE_LICZB<długość_WARTOŚĆ+2)return;
    const unsigned char 지움=21,끝=13;
    kanał_zdalny_wejście(&지움,1);if(długość_WARTOŚĆ)kanał_zdalny_wejście(polecenie,długość_WARTOŚĆ);kanał_zdalny_wejście(&끝,1);
    셸시작됨=1;Wydarzenie->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!polecenie_TYP){const char *plik_README_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*plik_README_eb81d7d9)zdalny_produkt_wyjściowy(*plik_README_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Nasłuchiwanie_uczestnik<0)return;
    uintptr_t TERAZ_WARTOŚĆ=보드밀리초();
    if(węzeł_równorzędny_WARTOŚĆ<0){if(TERAZ_WARTOŚĆ<재접속시각)return;węzeł_równorzędny_WARTOŚĆ=NET_akceptować(Nasłuchiwanie_uczestnik);if(węzeł_równorzędny_WARTOŚĆ<0)return;
        połączenie_CZAS=TERAZ_WARTOŚĆ;assh_status_t błąd=assh_session_create(kontekst_WARTOŚĆ,&połączenie_e05f319b);
        if(błąd){połączenie_e05f319b=0;진단("SSH session error ",błąd);Zamknij_połączenie();return;}}
    if((!인증됨&&TERAZ_WARTOŚĆ-połączenie_CZAS>30000)||닫을예정==2||(닫을예정&&TERAZ_WARTOŚĆ>=zamknięcie_CZAS)){Zamknij_połączenie();return;}
    if(Kanał_wpis&&셸시작됨&&!닫을예정) {
        if(produkt_wyjściowy_ILE_LICZB){size_t identyfikator=sizeof(produkt_wyjściowy_linia)-출력앞;if(identyfikator>produkt_wyjściowy_ILE_LICZB)identyfikator=produkt_wyjściowy_ILE_LICZB;if(identyfikator>2048)identyfikator=2048;
            assh_status_t błąd=assh_channel_data(Kanał_wpis,produkt_wyjściowy_linia+출력앞,&identyfikator);
            if(!błąd){출력앞=(출력앞+identyfikator)%sizeof(produkt_wyjściowy_linia);produkt_wyjściowy_ILE_LICZB-=identyfikator;}
            else if(błąd!=ASSH_NO_DATA){Zamknij_połączenie();return;}
        }
        if(Koniec_Stan>=0&&!produkt_wyjściowy_ILE_LICZB){unsigned char Stan_WARTOŚĆ[4];assh_store_u32(Stan_WARTOŚĆ,(uint32_t)Koniec_Stan);
            if(assh_request(połączenie_e05f319b,Kanał_wpis,"exit-status",11,Stan_WARTOŚĆ,4,0)||assh_channel_eof(Kanał_wpis)||assh_channel_close(Kanał_wpis)) {Zamknij_połączenie();return;}
            닫을예정=1;zamknięcie_CZAS=TERAZ_WARTOŚĆ+3000;
        }
    }
    for(unsigned SEKWENCJA_WARTOŚĆ=0;SEKWENCJA_WARTOŚĆ<16;SEKWENCJA_WARTOŚĆ++) {
        struct assh_event_s Wydarzenie;
        if(!assh_event_get(połączenie_e05f319b,&Wydarzenie,TERAZ_WARTOŚĆ/1000)){Zamknij_połączenie();return;}
        assh_status_t błąd=ASSH_OK;int 쉬기=0,rozłączać_uczestnik=0;
        switch(Wydarzenie.id) {
        case ASSH_EVENT_READ: {
            int identyfikator=통신읽기(węzeł_równorzędny_WARTOŚĆ,Wydarzenie.transport.read.buf.data,Wydarzenie.transport.read.buf.size);
            if(identyfikator>0)Wydarzenie.transport.read.transferred=identyfikator;
            else if(identyfikator==-11)쉬기=1;else rozłączać_uczestnik=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int identyfikator=NET_zapis(węzeł_równorzędny_WARTOŚĆ,Wydarzenie.transport.write.buf.data,Wydarzenie.transport.write.buf.size);
            if(identyfikator>0)Wydarzenie.transport.write.transferred=identyfikator;
            else if(identyfikator==-11)쉬기=1;else rozłączać_uczestnik=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Wydarzenie.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Wydarzenie.userauth_server.methods.retries>3)Wydarzenie.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *dane=&Wydarzenie.userauth_server.password;
            if(같은말(&dane->username,"user")&&dane->password.size<=256&&!dane->new_password.size) {
                unsigned char podsumowanie_WARTOŚĆ[32];zdalny_podsumowanie(dane->password.data,dane->password.size,podsumowanie_WARTOŚĆ);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=podsumowanie_WARTOŚĆ[순번]^powłoka_hasło_podsumowanie[순번];memset(podsumowanie_WARTOŚĆ,0,32);
                if(!차이)dane->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *dane=&Wydarzenie.connection.channel_open;
            if(인증됨&&!Kanał_wpis&&powłoka_Czekam&&같은말(&dane->type,"session")&&!dane->rq_data.size) {
                dane->reply=ASSH_CONNECTION_REPLY_SUCCESS;dane->pkt_size=4096;
                dane->win_size=-1;Kanał_wpis=dane->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: uchwyt_żądanie(&Wydarzenie.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *dane=&Wydarzenie.connection.channel_data;
            if(!셸시작됨||dane->ch!=Kanał_wpis||dane->ext){rozłączać_uczestnik=1;break;}
            unsigned identyfikator=dane->data.size;if(identyfikator>sizeof(wejście_linia)-wejście_ILE_LICZB)identyfikator=sizeof(wejście_linia)-wejście_ILE_LICZB;
            for(unsigned 순번=0;순번<identyfikator;순번++)if(dane->data.data[순번]==4){Koniec_Stan=0;identyfikator=순번;dane->transferred=dane->data.size;break;}
            kanał_zdalny_wejście(dane->data.data,identyfikator);if(!dane->transferred)dane->transferred=identyfikator;
            if(!identyfikator&&Koniec_Stan<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Kanał_wpis=0;셸시작됨=0;닫을예정=1;zamknięcie_CZAS=TERAZ_WARTOŚĆ+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Wydarzenie.session.error.code);rozłączać_uczestnik=1;break;
        case ASSH_EVENT_DISCONNECT: rozłączać_uczestnik=1;break;
        default: break;
        }
        assh_event_done(połączenie_e05f319b,&Wydarzenie,błąd);
        if(rozłączać_uczestnik){Zamknij_połączenie();return;}if(쉬기)return;
    }
}
