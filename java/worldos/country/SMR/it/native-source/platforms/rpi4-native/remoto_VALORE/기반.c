/* kernel_VALORE 전용 할당기와 password_VALORE 난수 공급. spazio_utente ELF의 libc와 별개이다. */
#include "crittografia_Supporto.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Memoria_Blocca { size_t durata_VALORE; struct Memoria_Blocca *Avanti_articolo; int usare_VALORE; } Memoria_Blocca;
static unsigned char Memoria_Arena[2*1024*1024] __attribute__((aligned(16)));
static Memoria_Blocca *첫조각;
void *allocare_remoto(size_t durata_VALORE) {
    if (!durata_VALORE || durata_VALORE>sizeof(Memoria_Arena)-64) return 0;
    durata_VALORE=(durata_VALORE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Memoria_Arena;첫조각->durata_VALORE=sizeof(Memoria_Arena)-32;}
    for(Memoria_Blocca *blocco_VALORE_652d4b53=첫조각;blocco_VALORE_652d4b53;blocco_VALORE_652d4b53=blocco_VALORE_652d4b53->Avanti_articolo)if(!blocco_VALORE_652d4b53->usare_VALORE&&blocco_VALORE_652d4b53->durata_VALORE>=durata_VALORE){
        if(blocco_VALORE_652d4b53->durata_VALORE>=durata_VALORE+64){Memoria_Blocca *새조각=(void*)((char*)blocco_VALORE_652d4b53+32+durata_VALORE);
            새조각->durata_VALORE=blocco_VALORE_652d4b53->durata_VALORE-durata_VALORE-32;새조각->Avanti_articolo=blocco_VALORE_652d4b53->Avanti_articolo;새조각->usare_VALORE=0;blocco_VALORE_652d4b53->Avanti_articolo=새조각;blocco_VALORE_652d4b53->durata_VALORE=durata_VALORE;}
        blocco_VALORE_652d4b53->usare_VALORE=1;return(char*)blocco_VALORE_652d4b53+32;
    }return 0;
}
void release_remoto(void *e_mail) {
    if(!e_mail)return;Memoria_Blocca *blocco_VALORE_652d4b53=(void*)((char*)e_mail-32);
    volatile unsigned char *지움=e_mail;for(size_t 순번=0;순번<blocco_VALORE_652d4b53->durata_VALORE;순번++)지움[순번]=0;
    blocco_VALORE_652d4b53->usare_VALORE=0;
    for(blocco_VALORE_652d4b53=첫조각;blocco_VALORE_652d4b53&&blocco_VALORE_652d4b53->Avanti_articolo;){if(!blocco_VALORE_652d4b53->usare_VALORE&&!blocco_VALORE_652d4b53->Avanti_articolo->usare_VALORE){blocco_VALORE_652d4b53->durata_VALORE+=32+blocco_VALORE_652d4b53->Avanti_articolo->durata_VALORE;blocco_VALORE_652d4b53->Avanti_articolo=blocco_VALORE_652d4b53->Avanti_articolo->Avanti_articolo;}else blocco_VALORE_652d4b53=blocco_VALORE_652d4b53->Avanti_articolo;}
}
void *원격재할당(void *e_mail,size_t durata_VALORE){
    if(!e_mail)return allocare_remoto(durata_VALORE);if(!durata_VALORE){release_remoto(e_mail);return 0;}
    Memoria_Blocca *blocco_VALORE_652d4b53=(void*)((char*)e_mail-32);void *새주소=allocare_remoto(durata_VALORE);
    if(새주소){memcpy(새주소,e_mail,durata_VALORE<blocco_VALORE_652d4b53->durata_VALORE?durata_VALORE:blocco_VALORE_652d4b53->durata_VALORE);release_remoto(e_mail);}return 새주소;
}
int strcmp(const char *가,const char *SECONDO_operando){while(*가&&*가==*SECONDO_operando){가++;SECONDO_operando++;}return(unsigned char)*가-(unsigned char)*SECONDO_operando;}
char *strchr(const char *Word_SMS,int carattere_VALORE){for(;;Word_SMS++){if(*Word_SMS==(char)carattere_VALORE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t durata_VALORE=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,durata_VALORE))return(char*)Word_SMS;return durata_VALORE?0:(char*)Word_SMS;}
char *strncpy(char *meta_VALORE,const char *원본,size_t durata_VALORE){size_t 순번=0;for(;순번<durata_VALORE&&원본[순번];순번++)meta_VALORE[순번]=원본[순번];for(;순번<durata_VALORE;순번++)meta_VALORE[순번]=0;return meta_VALORE;}
char *strncat(char *meta_VALORE,const char *원본,size_t durata_VALORE){char *끝=meta_VALORE+strlen(meta_VALORE);while(durata_VALORE--&&*원본)*끝++=*원본++;*끝=0;return meta_VALORE;}
int strncasecmp(const char *가,const char *SECONDO_operando,size_t durata_VALORE){while(durata_VALORE--){unsigned 첫글자=*가++,SECONDO_carattere=*SECONDO_operando++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECONDO_carattere>='A'&&SECONDO_carattere<='Z')SECONDO_carattere+=32;if(첫글자!=SECONDO_carattere)return(int)첫글자-(int)SECONDO_carattere;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SECONDO_operando){return strncasecmp(가,SECONDO_operando,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *delimitatore_VALORE,char **Avanti_articolo){if(!Word_SMS)Word_SMS=*Avanti_articolo;while(*Word_SMS&&strchr(delimitatore_VALORE,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Avanti_articolo=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(delimitatore_VALORE,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Avanti_articolo=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALORE) {
    const char *codiceSorgente=Word_SMS;unsigned long VALORE=0;int negativo_VALORE=0,overflow_VALORE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')negativo_VALORE=*Word_SMS++=='-';
    if((BASE_VALORE==0||BASE_VALORE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALORE=16;Word_SMS+=2;}
    if(!BASE_VALORE)BASE_VALORE=*Word_SMS=='0'?8:10;
    if(BASE_VALORE<2||BASE_VALORE>36){if(끝)*끝=(char*)codiceSorgente;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned carattere_VALORE=(unsigned char)*Word_SMS;
        unsigned numero=carattere_VALORE>='0'&&carattere_VALORE<='9'?carattere_VALORE-'0':carattere_VALORE>='a'&&carattere_VALORE<='z'?carattere_VALORE-'a'+10:carattere_VALORE>='A'&&carattere_VALORE<='Z'?carattere_VALORE-'A'+10:36;
        if(numero>=(unsigned)BASE_VALORE)break;
        if(VALORE>(~0ul-numero)/(unsigned)BASE_VALORE)overflow_VALORE=1;
        if(!overflow_VALORE)VALORE=VALORE*(unsigned)BASE_VALORE+numero;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?codiceSorgente:Word_SMS);
    return overflow_VALORE?~0ul:negativo_VALORE?0ul-VALORE:VALORE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int seme_Stato;
void remoto_riepilogo(const void *dati, size_t durata_VALORE, unsigned char risultato[32]) {
    br_sha256_context contesto_VALORE;
    br_sha256_init(&contesto_VALORE); br_sha256_update(&contesto_VALORE, dati, durata_VALORE); br_sha256_out(&contesto_VALORE, risultato);
    memset(&contesto_VALORE, 0, sizeof(contesto_VALORE));
}
#define 난수저장기(posizione) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(posizione)))
int remoto_casuale(unsigned char *meta_VALORE,unsigned durata_VALORE){
    if(!seme_Stato){volatile unsigned char *dati=(void*)0x01ff0000ul;const char *marcatore_VALORE="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=dati[순번]^(unsigned char)marcatore_VALORE[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=dati[8+순번];for(unsigned 순번=0;순번<40;순번++)dati[순번]=0;seme_Stato=2;}
        else {seme_Stato=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(seme_Stato==2){while(durata_VALORE){unsigned char Avanti_articolo[32],input_VALORE[33];memcpy(input_VALORE,모의씨앗,32);input_VALORE[32]=0;remoto_riepilogo(input_VALORE,33,Avanti_articolo);
        input_VALORE[32]=1;remoto_riepilogo(input_VALORE,33,모의씨앗);memset(input_VALORE,0,33);
        unsigned numero=durata_VALORE<32?durata_VALORE:32;memcpy(meta_VALORE,Avanti_articolo,numero);memset(Avanti_articolo,0,32);meta_VALORE+=numero;durata_VALORE-=numero;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(durata_VALORE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALORE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&durata_VALORE;순번++,durata_VALORE--){*meta_VALORE++=VALORE&255;VALORE>>=8;}}
    return 0;
}
