/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "valeurDistant.h"
#include "priseEnChargeCryptographie.h"
#include "profil.h"
#include "../PileRéseau/PileRéseau.h"
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
extern uintptr_t millisecondesÉcouléesCarteMatérielle(void);
extern uintptr_t écrireCaractèreCarteMatérielle(uintptr_t);
static struct assh_context_s *valeurContexte;
static struct assh_session_s *connexion;
static struct assh_channel_s *entréeÉlémentCanal;
static int extrémitéÉcouteEnCours=-1,valeurPairRéseau=-1,estAuthentifié,démarréInterpréteurCommandes,typeCommande,étatValeurFin=-1,futurFermer,erreurDémarrage,attenteEnCoursInterpréteurCommandes;
static uintptr_t tempsConnexion,tempsReconnecter,tempsFermetureEnCours;
static unsigned char ligneEntrée[8192],ligneSortie[65536];
static unsigned têteEntrée,nombreÉlémentsEntrée,têteSortie,nombreÉlémentsSortie,sortiePrécédentÉlément;
static void valeurDiagnostic(const char *texteMot,unsigned valeur) {
    while(*texteMot)écrireCaractèreCarteMatérielle(*texteMot++);
    char valeurChiffre[12];unsigned nombre=0;do{valeurChiffre[nombre++]='0'+valeur%10;valeur/=10;}while(valeur);
    while(nombre)écrireCaractèreCarteMatérielle(valeurChiffre[--nombre]);écrireCaractèreCarteMatérielle(10);
}
static assh_status_t préparerMémoire(void *Données,void **adresse,size_t taille,enum assh_alloc_type_e valeurGenre) {
    (void)Données;(void)valeurGenre;
    if(!taille){libérerDistant(*adresse);*adresse=0;return ASSH_OK;}
    void *adresseNouveau=réallouerDistant(*adresse,taille);
    if(!adresseNouveau)return ASSH_ERR_MEM;*adresse=adresseNouveau;return ASSH_OK;
}
static assh_status_t préparerAléatoire(struct assh_context_s *Données,const struct assh_buffer_s *valeurGraine) {
    (void)Données;(void)valeurGraine;unsigned char Tests[32];int résultat=aléatoireDistant(Tests,sizeof(Tests));memset(Tests,0,sizeof(Tests));
    return résultat?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t lireAléatoire(struct assh_context_s *Données,uint8_t *résultat,size_t longueur,uint_fast8_t valeurGenre) {
    (void)Données;(void)valeurGenre;if(longueur>65536)return ASSH_ERR_CRYPTO;
    return aléatoireDistant(résultat,longueur)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void finAléatoire(struct assh_context_s *Données){(void)Données;}
static const struct assh_prng_s générateurAléatoire={préparerAléatoire,lireAléatoire,finAléatoire};
static void fermerConnexion(void) {
    estAuthentifié=démarréInterpréteurCommandes=0;entréeÉlémentCanal=0;
    if(connexion)assh_session_release(connexion);connexion=0;
    if(valeurPairRéseau>=0)fermerRéseau(valeurPairRéseau);valeurPairRéseau=-1;typeCommande=0;étatValeurFin=-1;futurFermer=0;
    têteEntrée=nombreÉlémentsEntrée=têteSortie=nombreÉlémentsSortie=sortiePrécédentÉlément=0;tempsReconnecter=millisecondesÉcouléesCarteMatérielle()+250;
}
int entréeDistantAlimenter(const unsigned char *Données,unsigned nombre) {
    if(nombre>sizeof(ligneEntrée)-nombreÉlémentsEntrée)return -11;
    for(unsigned indiceOrdinal=0;indiceOrdinal<nombre;indiceOrdinal++)ligneEntrée[(têteEntrée+nombreÉlémentsEntrée++)%sizeof(ligneEntrée)]=Données[indiceOrdinal];return nombre;
}
int entréeDistant(void) {
    if(!nombreÉlémentsEntrée)return -1;int valeurCaractère=ligneEntrée[têteEntrée];têteEntrée=(têteEntrée+1)%sizeof(ligneEntrée);nombreÉlémentsEntrée--;return valeurCaractère;
}
void sortieDistant(unsigned char valeurCaractère) {
    if(!démarréInterpréteurCommandes||futurFermer)return;
    unsigned ajouterFinMode=valeurCaractère==10&&sortiePrécédentÉlément!=13;
    if(nombreÉlémentsSortie+1+ajouterFinMode>sizeof(ligneSortie)){futurFermer=2;return;}
    if(ajouterFinMode)ligneSortie[(têteSortie+nombreÉlémentsSortie++)%sizeof(ligneSortie)]=13;
    ligneSortie[(têteSortie+nombreÉlémentsSortie++)%sizeof(ligneSortie)]=valeurCaractère;sortiePrécédentÉlément=valeurCaractère;
}
uintptr_t commandeDistantFinCarteMatérielle(uintptr_t valeurÉtatValeur){if(démarréInterpréteurCommandes&&typeCommande)étatValeurFin=(int)valeurÉtatValeur;return 0;}
uintptr_t attendreDistantCarteMatérielle(uintptr_t valeurÉtatValeur){attenteEnCoursInterpréteurCommandes=valeurÉtatValeur!=0;return 0;}
static int préparerInterpréteurCommandes(void) {
    if(extrémitéÉcouteEnCours>=0)return 0;
    if(!valeurContexte){
        assh_status_t erreur=assh_context_create(&valeurContexte,ASSH_SERVER,préparerMémoire,0,&générateurAléatoire,0);
        if(erreur)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *modeMéthode[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        erreur=assh_algo_register(valeurContexte,ASSH_SAFETY_WEAK,modeMéthode);
        if(!erreur)erreur=assh_service_register_va(valeurContexte,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *matériauTouche=touchePériphérique;
        if(!erreur)erreur=assh_key_load(valeurContexte,assh_context_keys(valeurContexte),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&matériauTouche,sizeof(touchePériphérique));
        if(erreur){valeurDiagnostic("SSH init error ",erreur);assh_context_release(valeurContexte);valeurContexte=0;return -5;}
    }
    int valeurPort=créerExtrémitéPriseRéseau(1);if(valeurPort<0)return valeurPort;adressePriseRéseauRéutiliser(valeurPort);
    int résultat=associerRéseauCourt(valeurPort,0,22);if(!résultat)résultat=écouterRéseauCourt(valeurPort);
    if(résultat<0){fermerRéseau(valeurPort);return résultat;}extrémitéÉcouteEnCours=valeurPort;return 0;
}
uintptr_t contrôleDistantCarteMatérielle(uintptr_t valeurGenre,uintptr_t action) {
    if(valeurGenre==1)return(uint32_t)présenterDistantContrôle(action);
    if(action==0){fermerConnexion();if(extrémitéÉcouteEnCours>=0)fermerRéseau(extrémitéÉcouteEnCours);extrémitéÉcouteEnCours=-1;return 0;}
    if(action==1){erreurDémarrage=préparerInterpréteurCommandes();return(uint32_t)erreurDémarrage;}
    return(uint32_t)(extrémitéÉcouteEnCours>=0?1:erreurDémarrage);
}
void préparerDistant(void){erreurDémarrage=préparerInterpréteurCommandes();présenterDistantContrôle(1);}
static int motConcordant(const struct assh_cbuffer_s *Données,const char *texteMot) {
    size_t longueur=strlen(texteMot);return Données->size==longueur&&!memcmp(Données->data,texteMot,longueur);
}
static int requêteTerminal(const struct assh_cbuffer_s *Données) {
    if(Données->size<24)return 0;
    const unsigned char *positionDonnées=Données->data;unsigned longueur=assh_load_u32(positionDonnées);
    if(longueur>128||Données->size<longueur+24)return 0;
    unsigned valeurMode=assh_load_u32(positionDonnées+4+longueur+16);
    return valeurMode<=2048&&Données->size==longueur+24+valeurMode;
}
static void requêtePoignée(struct assh_event_request_s *évènement) {
    if(!estAuthentifié||évènement->ch!=entréeÉlémentCanal||!entréeÉlémentCanal)return;
    if(motConcordant(&évènement->type,"pty-req")) {
        if(!démarréInterpréteurCommandes&&requêteTerminal(&évènement->rq_data))évènement->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(motConcordant(&évènement->type,"window-change")) {
        if(démarréInterpréteurCommandes&&évènement->rq_data.size==16)évènement->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(démarréInterpréteurCommandes||!attenteEnCoursInterpréteurCommandes)return;
    const unsigned char *commande=0;unsigned longueur=0;
    if(motConcordant(&évènement->type,"exec")) {
        if(évènement->rq_data.size<4)return;
        longueur=assh_load_u32(évènement->rq_data.data);
        if(!longueur||longueur>2048||évènement->rq_data.size!=longueur+4)return;
        commande=évènement->rq_data.data+4;
        for(unsigned indiceOrdinal=0;indiceOrdinal<longueur;indiceOrdinal++)if(!commande[indiceOrdinal])return;
        typeCommande=1;
    }else if(!motConcordant(&évènement->type,"shell")||évènement->rq_data.size)return;
    if(sizeof(ligneEntrée)-nombreÉlémentsEntrée<longueur+2)return;
    const unsigned char valeurEffacé=21,terminaison=13;
    entréeDistantAlimenter(&valeurEffacé,1);if(longueur)entréeDistantAlimenter(commande,longueur);entréeDistantAlimenter(&terminaison,1);
    démarréInterpréteurCommandes=1;évènement->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!typeCommande){const char *Guide="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*Guide)sortieDistant(*Guide++);}
}
void inspecterDistant(void) {
    inspecterPrésenterDistant();
    if(extrémitéÉcouteEnCours<0)return;
    uintptr_t valeurMaintenant=millisecondesÉcouléesCarteMatérielle();
    if(valeurPairRéseau<0){if(valeurMaintenant<tempsReconnecter)return;valeurPairRéseau=accepterRéseauCourt(extrémitéÉcouteEnCours);if(valeurPairRéseau<0)return;
        tempsConnexion=valeurMaintenant;assh_status_t erreur=assh_session_create(valeurContexte,&connexion);
        if(erreur){connexion=0;valeurDiagnostic("SSH session error ",erreur);fermerConnexion();return;}}
    if((!estAuthentifié&&valeurMaintenant-tempsConnexion>30000)||futurFermer==2||(futurFermer&&valeurMaintenant>=tempsFermetureEnCours)){fermerConnexion();return;}
    if(entréeÉlémentCanal&&démarréInterpréteurCommandes&&!futurFermer) {
        if(nombreÉlémentsSortie){size_t nombre=sizeof(ligneSortie)-têteSortie;if(nombre>nombreÉlémentsSortie)nombre=nombreÉlémentsSortie;if(nombre>2048)nombre=2048;
            assh_status_t erreur=assh_channel_data(entréeÉlémentCanal,ligneSortie+têteSortie,&nombre);
            if(!erreur){têteSortie=(têteSortie+nombre)%sizeof(ligneSortie);nombreÉlémentsSortie-=nombre;}
            else if(erreur!=ASSH_NO_DATA){fermerConnexion();return;}
        }
        if(étatValeurFin>=0&&!nombreÉlémentsSortie){unsigned char valeurÉtatValeur[4];assh_store_u32(valeurÉtatValeur,(uint32_t)étatValeurFin);
            if(assh_request(connexion,entréeÉlémentCanal,"exit-status",11,valeurÉtatValeur,4,0)||assh_channel_eof(entréeÉlémentCanal)||assh_channel_close(entréeÉlémentCanal)) {fermerConnexion();return;}
            futurFermer=1;tempsFermetureEnCours=valeurMaintenant+3000;
        }
    }
    for(unsigned valeurSéquence=0;valeurSéquence<16;valeurSéquence++) {
        struct assh_event_s évènement;
        if(!assh_event_get(connexion,&évènement,valeurMaintenant/1000)){fermerConnexion();return;}
        assh_status_t erreur=ASSH_OK;int brièvementReste=0,extrémitéDéconnecter=0;
        switch(évènement.id) {
        case ASSH_EVENT_READ: {
            int nombre=lireRéseauCourt(valeurPairRéseau,évènement.transport.read.buf.data,évènement.transport.read.buf.size);
            if(nombre>0)évènement.transport.read.transferred=nombre;
            else if(nombre==-11)brièvementReste=1;else extrémitéDéconnecter=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int nombre=écrireRéseauCourt(valeurPairRéseau,évènement.transport.write.buf.data,évènement.transport.write.buf.size);
            if(nombre>0)évènement.transport.write.transferred=nombre;
            else if(nombre==-11)brièvementReste=1;else extrémitéDéconnecter=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            évènement.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(évènement.userauth_server.methods.retries>3)évènement.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *Données=&évènement.userauth_server.password;
            if(motConcordant(&Données->username,"user")&&Données->password.size<=256&&!Données->new_password.size) {
                unsigned char valeurRésumé[32];résuméDistant(Données->password.data,Données->password.size,valeurRésumé);
                unsigned valeurDifférence=0;for(unsigned indiceOrdinal=0;indiceOrdinal<32;indiceOrdinal++)valeurDifférence|=valeurRésumé[indiceOrdinal]^résuméMotPasseInterpréteurCommandes[indiceOrdinal];memset(valeurRésumé,0,32);
                if(!valeurDifférence)Données->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: estAuthentifié=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *Données=&évènement.connection.channel_open;
            if(estAuthentifié&&!entréeÉlémentCanal&&attenteEnCoursInterpréteurCommandes&&motConcordant(&Données->type,"session")&&!Données->rq_data.size) {
                Données->reply=ASSH_CONNECTION_REPLY_SUCCESS;Données->pkt_size=4096;
                Données->win_size=-1;entréeÉlémentCanal=Données->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: requêtePoignée(&évènement.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *Données=&évènement.connection.channel_data;
            if(!démarréInterpréteurCommandes||Données->ch!=entréeÉlémentCanal||Données->ext){extrémitéDéconnecter=1;break;}
            unsigned nombre=Données->data.size;if(nombre>sizeof(ligneEntrée)-nombreÉlémentsEntrée)nombre=sizeof(ligneEntrée)-nombreÉlémentsEntrée;
            for(unsigned indiceOrdinal=0;indiceOrdinal<nombre;indiceOrdinal++)if(Données->data.data[indiceOrdinal]==4){étatValeurFin=0;nombre=indiceOrdinal;Données->transferred=Données->data.size;break;}
            entréeDistantAlimenter(Données->data.data,nombre);if(!Données->transferred)Données->transferred=nombre;
            if(!nombre&&étatValeurFin<0)brièvementReste=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: entréeÉlémentCanal=0;démarréInterpréteurCommandes=0;futurFermer=1;tempsFermetureEnCours=valeurMaintenant+1000;break;
        case ASSH_EVENT_SESSION_ERROR: estAuthentifié=démarréInterpréteurCommandes=0;valeurDiagnostic("SSH error ",évènement.session.error.code);extrémitéDéconnecter=1;break;
        case ASSH_EVENT_DISCONNECT: extrémitéDéconnecter=1;break;
        default: break;
        }
        assh_event_done(connexion,&évènement,erreur);
        if(extrémitéDéconnecter){fermerConnexion();return;}if(brièvementReste)return;
    }
}
