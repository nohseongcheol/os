/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "remoto_VALORE.h"
#include "crittografia_Supporto.h"
#include "Profilo.h"
#include "../rete_Pila/rete_Pila.h"
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
static struct assh_context_s *contesto_VALORE;
static struct assh_session_s *connessione_e05f319b;
static struct assh_channel_s *Canale_voce;
static int In_ascolto_endpoint=-1,peer_VALORE=-1,인증됨,셸시작됨,comando_TIPO,chiudere_Stato=-1,닫을예정,avvio_errore,Shell_In_attesa;
static uintptr_t connessione_time,재접속시각,chiusura_time;
static unsigned char input_riga[8192],output_riga[65536];
static unsigned input_intestazione,input_CONTA_NUMERI,output_intestazione,output_CONTA_NUMERI,Indietro_output;
static void 진단(const char *Word_SMS,unsigned VALORE) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char cifra_VALORE[12];unsigned numero=0;do{cifra_VALORE[numero++]='0'+VALORE%10;VALORE/=10;}while(VALORE);
    while(numero)보드글자쓰기(cifra_VALORE[--numero]);보드글자쓰기(10);
}
static assh_status_t Prepara_Memoria(void *dati,void **e_mail,size_t Dimensione,enum assh_alloc_type_e Kind_VALORE) {
    (void)dati;(void)Kind_VALORE;
    if(!Dimensione){release_remoto(*e_mail);*e_mail=0;return ASSH_OK;}
    void *새주소=원격재할당(*e_mail,Dimensione);
    if(!새주소)return ASSH_ERR_MEM;*e_mail=새주소;return ASSH_OK;
}
static assh_status_t Prepara_casuale(struct assh_context_s *dati,const struct assh_buffer_s *valore_di_inizializzazione) {
    (void)dati;(void)valore_di_inizializzazione;unsigned char prove[32];int risultato=remoto_casuale(prove,sizeof(prove));memset(prove,0,sizeof(prove));
    return risultato?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t 난수받기(struct assh_context_s *dati,uint8_t *risultato,size_t durata_VALORE,uint_fast8_t Kind_VALORE) {
    (void)dati;(void)Kind_VALORE;if(durata_VALORE>65536)return ASSH_ERR_CRYPTO;
    return remoto_casuale(risultato,durata_VALORE)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void casuale_chiudere(struct assh_context_s *dati){(void)dati;}
static const struct assh_prng_s casuale_generatore={Prepara_casuale,난수받기,casuale_chiudere};
static void Chiudi_connessione(void) {
    인증됨=셸시작됨=0;Canale_voce=0;
    if(connessione_e05f319b)assh_session_release(connessione_e05f319b);connessione_e05f319b=0;
    if(peer_VALORE>=0)Chiudi_rete(peer_VALORE);peer_VALORE=-1;comando_TIPO=0;chiudere_Stato=-1;닫을예정=0;
    input_intestazione=input_CONTA_NUMERI=output_intestazione=output_CONTA_NUMERI=Indietro_output=0;재접속시각=보드밀리초()+250;
}
int feed_remoto_input(const unsigned char *dati,unsigned numero) {
    if(numero>sizeof(input_riga)-input_CONTA_NUMERI)return -11;
    for(unsigned 순번=0;순번<numero;순번++)input_riga[(input_intestazione+input_CONTA_NUMERI++)%sizeof(input_riga)]=dati[순번];return numero;
}
int remoto_input(void) {
    if(!input_CONTA_NUMERI)return -1;int carattere_VALORE=input_riga[input_intestazione];input_intestazione=(input_intestazione+1)%sizeof(input_riga);input_CONTA_NUMERI--;return carattere_VALORE;
}
void remoto_output(unsigned char carattere_VALORE) {
    if(!셸시작됨||닫을예정)return;
    unsigned modalità_Append=carattere_VALORE==10&&Indietro_output!=13;
    if(output_CONTA_NUMERI+1+modalità_Append>sizeof(output_riga)){닫을예정=2;return;}
    if(modalità_Append)output_riga[(output_intestazione+output_CONTA_NUMERI++)%sizeof(output_riga)]=13;
    output_riga[(output_intestazione+output_CONTA_NUMERI++)%sizeof(output_riga)]=carattere_VALORE;Indietro_output=carattere_VALORE;
}
uintptr_t scheda_chiudere_remoto_comando(uintptr_t Stato_VALORE){if(셸시작됨&&comando_TIPO)chiudere_Stato=(int)Stato_VALORE;return 0;}
uintptr_t scheda_remoto_aspetta(uintptr_t Stato_VALORE){Shell_In_attesa=Stato_VALORE!=0;return 0;}
static int Prepara_Shell(void) {
    if(In_ascolto_endpoint>=0)return 0;
    if(!contesto_VALORE){
        assh_status_t errore=assh_context_create(&contesto_VALORE,ASSH_SERVER,Prepara_Memoria,0,&casuale_generatore,0);
        if(errore)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *metodo_MODA[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        errore=assh_algo_register(contesto_VALORE,ASSH_SAFETY_WEAK,metodo_MODA);
        if(!errore)errore=assh_service_register_va(contesto_VALORE,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *tasto_materiale=cellulare_tasto;
        if(!errore)errore=assh_key_load(contesto_VALORE,assh_context_keys(contesto_VALORE),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&tasto_materiale,sizeof(cellulare_tasto));
        if(errore){진단("SSH init error ",errore);assh_context_release(contesto_VALORE);contesto_VALORE=0;return -5;}
    }
    int porta_VALORE=Crea_socket_endpoint(1);if(porta_VALORE<0)return porta_VALORE;통신주소재사용(porta_VALORE);
    int risultato=NET_BIND(porta_VALORE,0,22);if(!risultato)risultato=NET_essere_in_ascolto(porta_VALORE);
    if(risultato<0){Chiudi_rete(porta_VALORE);return risultato;}In_ascolto_endpoint=porta_VALORE;return 0;
}
uintptr_t scheda_shadowing(uintptr_t Kind_VALORE,uintptr_t Azione) {
    if(Kind_VALORE==1)return(uint32_t)controllo_remoto_display(Azione);
    if(Azione==0){Chiudi_connessione();if(In_ascolto_endpoint>=0)Chiudi_rete(In_ascolto_endpoint);In_ascolto_endpoint=-1;return 0;}
    if(Azione==1){avvio_errore=Prepara_Shell();return(uint32_t)avvio_errore;}
    return(uint32_t)(In_ascolto_endpoint>=0?1:avvio_errore);
}
void Prepara_remoto(void){avvio_errore=Prepara_Shell();controllo_remoto_display(1);}
static int collegamento_movimenti_Word(const struct assh_cbuffer_s *dati,const char *Word_SMS) {
    size_t durata_VALORE=strlen(Word_SMS);return dati->size==durata_VALORE&&!memcmp(dati->data,Word_SMS,durata_VALORE);
}
static int Terminale_richiesta(const struct assh_cbuffer_s *dati) {
    if(dati->size<24)return 0;
    const unsigned char *dati_funzione=dati->data;unsigned durata_VALORE=assh_load_u32(dati_funzione);
    if(durata_VALORE>128||dati->size<durata_VALORE+24)return 0;
    unsigned MODA_VALORE=assh_load_u32(dati_funzione+4+durata_VALORE+16);
    return MODA_VALORE<=2048&&dati->size==durata_VALORE+24+MODA_VALORE;
}
static void handle_richiesta(struct assh_event_request_s *Evento) {
    if(!인증됨||Evento->ch!=Canale_voce||!Canale_voce)return;
    if(collegamento_movimenti_Word(&Evento->type,"pty-req")) {
        if(!셸시작됨&&Terminale_richiesta(&Evento->rq_data))Evento->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(collegamento_movimenti_Word(&Evento->type,"window-change")) {
        if(셸시작됨&&Evento->rq_data.size==16)Evento->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!Shell_In_attesa)return;
    const unsigned char *comando=0;unsigned durata_VALORE=0;
    if(collegamento_movimenti_Word(&Evento->type,"exec")) {
        if(Evento->rq_data.size<4)return;
        durata_VALORE=assh_load_u32(Evento->rq_data.data);
        if(!durata_VALORE||durata_VALORE>2048||Evento->rq_data.size!=durata_VALORE+4)return;
        comando=Evento->rq_data.data+4;
        for(unsigned 순번=0;순번<durata_VALORE;순번++)if(!comando[순번])return;
        comando_TIPO=1;
    }else if(!collegamento_movimenti_Word(&Evento->type,"shell")||Evento->rq_data.size)return;
    if(sizeof(input_riga)-input_CONTA_NUMERI<durata_VALORE+2)return;
    const unsigned char 지움=21,끝=13;
    feed_remoto_input(&지움,1);if(durata_VALORE)feed_remoto_input(comando,durata_VALORE);feed_remoto_input(&끝,1);
    셸시작됨=1;Evento->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!comando_TIPO){const char *README_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*README_eb81d7d9)remoto_output(*README_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(In_ascolto_endpoint<0)return;
    uintptr_t ADESSO_VALORE=보드밀리초();
    if(peer_VALORE<0){if(ADESSO_VALORE<재접속시각)return;peer_VALORE=NET_accettare(In_ascolto_endpoint);if(peer_VALORE<0)return;
        connessione_time=ADESSO_VALORE;assh_status_t errore=assh_session_create(contesto_VALORE,&connessione_e05f319b);
        if(errore){connessione_e05f319b=0;진단("SSH session error ",errore);Chiudi_connessione();return;}}
    if((!인증됨&&ADESSO_VALORE-connessione_time>30000)||닫을예정==2||(닫을예정&&ADESSO_VALORE>=chiusura_time)){Chiudi_connessione();return;}
    if(Canale_voce&&셸시작됨&&!닫을예정) {
        if(output_CONTA_NUMERI){size_t numero=sizeof(output_riga)-output_intestazione;if(numero>output_CONTA_NUMERI)numero=output_CONTA_NUMERI;if(numero>2048)numero=2048;
            assh_status_t errore=assh_channel_data(Canale_voce,output_riga+output_intestazione,&numero);
            if(!errore){output_intestazione=(output_intestazione+numero)%sizeof(output_riga);output_CONTA_NUMERI-=numero;}
            else if(errore!=ASSH_NO_DATA){Chiudi_connessione();return;}
        }
        if(chiudere_Stato>=0&&!output_CONTA_NUMERI){unsigned char Stato_VALORE[4];assh_store_u32(Stato_VALORE,(uint32_t)chiudere_Stato);
            if(assh_request(connessione_e05f319b,Canale_voce,"exit-status",11,Stato_VALORE,4,0)||assh_channel_eof(Canale_voce)||assh_channel_close(Canale_voce)) {Chiudi_connessione();return;}
            닫을예정=1;chiusura_time=ADESSO_VALORE+3000;
        }
    }
    for(unsigned SEQUENZA_VALORE=0;SEQUENZA_VALORE<16;SEQUENZA_VALORE++) {
        struct assh_event_s Evento;
        if(!assh_event_get(connessione_e05f319b,&Evento,ADESSO_VALORE/1000)){Chiudi_connessione();return;}
        assh_status_t errore=ASSH_OK;int 쉬기=0,scollegare_endpoint=0;
        switch(Evento.id) {
        case ASSH_EVENT_READ: {
            int numero=통신읽기(peer_VALORE,Evento.transport.read.buf.data,Evento.transport.read.buf.size);
            if(numero>0)Evento.transport.read.transferred=numero;
            else if(numero==-11)쉬기=1;else scollegare_endpoint=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int numero=NET_scrivere(peer_VALORE,Evento.transport.write.buf.data,Evento.transport.write.buf.size);
            if(numero>0)Evento.transport.write.transferred=numero;
            else if(numero==-11)쉬기=1;else scollegare_endpoint=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Evento.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Evento.userauth_server.methods.retries>3)Evento.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *dati=&Evento.userauth_server.password;
            if(collegamento_movimenti_Word(&dati->username,"user")&&dati->password.size<=256&&!dati->new_password.size) {
                unsigned char riepilogo_VALORE[32];remoto_riepilogo(dati->password.data,dati->password.size,riepilogo_VALORE);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=riepilogo_VALORE[순번]^Shell_password_riepilogo[순번];memset(riepilogo_VALORE,0,32);
                if(!차이)dati->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *dati=&Evento.connection.channel_open;
            if(인증됨&&!Canale_voce&&Shell_In_attesa&&collegamento_movimenti_Word(&dati->type,"session")&&!dati->rq_data.size) {
                dati->reply=ASSH_CONNECTION_REPLY_SUCCESS;dati->pkt_size=4096;
                dati->win_size=-1;Canale_voce=dati->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: handle_richiesta(&Evento.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *dati=&Evento.connection.channel_data;
            if(!셸시작됨||dati->ch!=Canale_voce||dati->ext){scollegare_endpoint=1;break;}
            unsigned numero=dati->data.size;if(numero>sizeof(input_riga)-input_CONTA_NUMERI)numero=sizeof(input_riga)-input_CONTA_NUMERI;
            for(unsigned 순번=0;순번<numero;순번++)if(dati->data.data[순번]==4){chiudere_Stato=0;numero=순번;dati->transferred=dati->data.size;break;}
            feed_remoto_input(dati->data.data,numero);if(!dati->transferred)dati->transferred=numero;
            if(!numero&&chiudere_Stato<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Canale_voce=0;셸시작됨=0;닫을예정=1;chiusura_time=ADESSO_VALORE+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Evento.session.error.code);scollegare_endpoint=1;break;
        case ASSH_EVENT_DISCONNECT: scollegare_endpoint=1;break;
        default: break;
        }
        assh_event_done(connessione_e05f319b,&Evento,errore);
        if(scollegare_endpoint){Chiudi_connessione();return;}if(쉬기)return;
    }
}
