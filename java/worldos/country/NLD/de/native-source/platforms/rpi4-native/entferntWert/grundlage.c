/* betriebskernWert 전용 할당기와 passwortWert 난수 공급. Benutzer ELF의 libc와 별개이다. */
#include "kryptographieUnterstützung.h"
#include "../benennung/maschineBindenNamen.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t platineVergangeneMillisekunden(void);
typedef struct speicherBlock { size_t Länge; struct speicherBlock *nächsterElementeintrag; int benutzenWert; } speicherBlock;
static unsigned char speicherSammelbereich[2*1024*1024] __attribute__((aligned(16)));
static speicherBlock *ersterFragmentWert;
void *entferntZuteilen(size_t Länge) {
    if (!Länge || Länge>sizeof(speicherSammelbereich)-64) return 0;
    Länge=(Länge+15)&~(size_t)15;
    if(!ersterFragmentWert){ersterFragmentWert=(void*)speicherSammelbereich;ersterFragmentWert->Länge=sizeof(speicherSammelbereich)-32;}
    for(speicherBlock *fragmentWert=ersterFragmentWert;fragmentWert;fragmentWert=fragmentWert->nächsterElementeintrag)if(!fragmentWert->benutzenWert&&fragmentWert->Länge>=Länge){
        if(fragmentWert->Länge>=Länge+64){speicherBlock *neuFragment=(void*)((char*)fragmentWert+32+Länge);
            neuFragment->Länge=fragmentWert->Länge-Länge-32;neuFragment->nächsterElementeintrag=fragmentWert->nächsterElementeintrag;neuFragment->benutzenWert=0;fragmentWert->nächsterElementeintrag=neuFragment;fragmentWert->Länge=Länge;}
        fragmentWert->benutzenWert=1;return(char*)fragmentWert+32;
    }return 0;
}
void entferntFreigeben(void *adresse) {
    if(!adresse)return;speicherBlock *fragmentWert=(void*)((char*)adresse-32);
    volatile unsigned char *gelöschtWert=adresse;for(size_t ordnungszahlIndex=0;ordnungszahlIndex<fragmentWert->Länge;ordnungszahlIndex++)gelöschtWert[ordnungszahlIndex]=0;
    fragmentWert->benutzenWert=0;
    for(fragmentWert=ersterFragmentWert;fragmentWert&&fragmentWert->nächsterElementeintrag;){if(!fragmentWert->benutzenWert&&!fragmentWert->nächsterElementeintrag->benutzenWert){fragmentWert->Länge+=32+fragmentWert->nächsterElementeintrag->Länge;fragmentWert->nächsterElementeintrag=fragmentWert->nächsterElementeintrag->nächsterElementeintrag;}else fragmentWert=fragmentWert->nächsterElementeintrag;}
}
void *entferntNeuzuteilen(void *adresse,size_t Länge){
    if(!adresse)return entferntZuteilen(Länge);if(!Länge){entferntFreigeben(adresse);return 0;}
    speicherBlock *fragmentWert=(void*)((char*)adresse-32);void *neuAdresse=entferntZuteilen(Länge);
    if(neuAdresse){memcpy(neuAdresse,adresse,Länge<fragmentWert->Länge?Länge:fragmentWert->Länge);entferntFreigeben(adresse);}return neuAdresse;
}
int strcmp(const char *ersterOperand,const char *zweiterOperand){while(*ersterOperand&&*ersterOperand==*zweiterOperand){ersterOperand++;zweiterOperand++;}return(unsigned char)*ersterOperand-(unsigned char)*zweiterOperand;}
char *strchr(const char *maschinenwortText,int zeichenWert){for(;;maschinenwortText++){if(*maschinenwortText==(char)zeichenWert)return(char*)maschinenwortText;if(!*maschinenwortText)return 0;}}
char *strstr(const char *maschinenwortText,const char *gefundenWert){size_t Länge=strlen(gefundenWert);for(;*maschinenwortText;maschinenwortText++)if(!strncmp(maschinenwortText,gefundenWert,Länge))return(char*)maschinenwortText;return Länge?0:(char*)maschinenwortText;}
char *strncpy(char *zielWert,const char *ursprünglich,size_t Länge){size_t ordnungszahlIndex=0;for(;ordnungszahlIndex<Länge&&ursprünglich[ordnungszahlIndex];ordnungszahlIndex++)zielWert[ordnungszahlIndex]=ursprünglich[ordnungszahlIndex];for(;ordnungszahlIndex<Länge;ordnungszahlIndex++)zielWert[ordnungszahlIndex]=0;return zielWert;}
char *strncat(char *zielWert,const char *ursprünglich,size_t Länge){char *endung=zielWert+strlen(zielWert);while(Länge--&&*ursprünglich)*endung++=*ursprünglich++;*endung=0;return zielWert;}
int strncasecmp(const char *ersterOperand,const char *zweiterOperand,size_t Länge){while(Länge--){unsigned ersterZeichen=*ersterOperand++,zweiterZeichen=*zweiterOperand++;if(ersterZeichen>='A'&&ersterZeichen<='Z')ersterZeichen+=32;if(zweiterZeichen>='A'&&zweiterZeichen<='Z')zweiterZeichen+=32;if(ersterZeichen!=zweiterZeichen)return(int)ersterZeichen-(int)zweiterZeichen;if(!ersterZeichen)break;}return 0;}
int strcasecmp(const char *ersterOperand,const char *zweiterOperand){return strncasecmp(ersterOperand,zweiterOperand,(size_t)-1);}
char *strtok_r(char *maschinenwortText,const char *trennzeichenWert,char **nächsterElementeintrag){if(!maschinenwortText)maschinenwortText=*nächsterElementeintrag;while(*maschinenwortText&&strchr(trennzeichenWert,*maschinenwortText))maschinenwortText++;if(!*maschinenwortText){*nächsterElementeintrag=maschinenwortText;return 0;}char *anfänglichElementeintrag=maschinenwortText;while(*maschinenwortText&&!strchr(trennzeichenWert,*maschinenwortText))maschinenwortText++;if(*maschinenwortText)*maschinenwortText++=0;*nächsterElementeintrag=maschinenwortText;return anfänglichElementeintrag;}
unsigned long strtoul(const char *maschinenwortText, char **endung, int basisWert) {
    const char *Quelltext=maschinenwortText;unsigned long Wert=0;int negativWert=0,überlaufWert=0;
    while(*maschinenwortText==' '||(*maschinenwortText>=9&&*maschinenwortText<=13))maschinenwortText++;
    if(*maschinenwortText=='-'||*maschinenwortText=='+')negativWert=*maschinenwortText++=='-';
    if((basisWert==0||basisWert==16)&&maschinenwortText[0]=='0'&&(maschinenwortText[1]=='x'||maschinenwortText[1]=='X')&&
       ((maschinenwortText[2]>='0'&&maschinenwortText[2]<='9')||(maschinenwortText[2]>='a'&&maschinenwortText[2]<='f')||(maschinenwortText[2]>='A'&&maschinenwortText[2]<='F'))) {basisWert=16;maschinenwortText+=2;}
    if(!basisWert)basisWert=*maschinenwortText=='0'?8:10;
    if(basisWert<2||basisWert>36){if(endung)*endung=(char*)Quelltext;return 0;}
    const char *anfänglichElementeintrag=maschinenwortText;
    for(;;maschinenwortText++) {
        unsigned zeichenWert=(unsigned char)*maschinenwortText;
        unsigned Zahl=zeichenWert>='0'&&zeichenWert<='9'?zeichenWert-'0':zeichenWert>='a'&&zeichenWert<='z'?zeichenWert-'a'+10:zeichenWert>='A'&&zeichenWert<='Z'?zeichenWert-'A'+10:36;
        if(Zahl>=(unsigned)basisWert)break;
        if(Wert>(~0ul-Zahl)/(unsigned)basisWert)überlaufWert=1;
        if(!überlaufWert)Wert=Wert*(unsigned)basisWert+Zahl;
    }
    if(endung)*endung=(char*)(maschinenwortText==anfänglichElementeintrag?Quelltext:maschinenwortText);
    return überlaufWert?~0ul:negativWert?0ul-Wert:Wert;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char attrappeStartwert[32];
static int startwertStatuswert;
void entferntZusammenfassung(const void *Daten, size_t Länge, unsigned char ergebnis[32]) {
    br_sha256_context kontextWert;
    br_sha256_init(&kontextWert); br_sha256_update(&kontextWert, Daten, Länge); br_sha256_out(&kontextWert, ergebnis);
    memset(&kontextWert, 0, sizeof(kontextWert));
}
#define zufälligRegisterliste(position) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(position)))
int entferntZufällig(unsigned char *zielWert,unsigned Länge){
    if(!startwertStatuswert){volatile unsigned char *Daten=(void*)0x01ff0000ul;const char *markierungWert="JKRENRG1";unsigned unterschiedWert=0;
        for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<8;ordnungszahlIndex++)unterschiedWert|=Daten[ordnungszahlIndex]^(unsigned char)markierungWert[ordnungszahlIndex];
        if(!unterschiedWert){for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<32;ordnungszahlIndex++)attrappeStartwert[ordnungszahlIndex]=Daten[8+ordnungszahlIndex];for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<40;ordnungszahlIndex++)Daten[ordnungszahlIndex]=0;startwertStatuswert=2;}
        else {startwertStatuswert=1;zufälligRegisterliste(0)=(zufälligRegisterliste(0)&~0x1fffu)|1;}
    }
    if(startwertStatuswert==2){while(Länge){unsigned char nächsterElementeintrag[32],Eingabewert[33];memcpy(Eingabewert,attrappeStartwert,32);Eingabewert[32]=0;entferntZusammenfassung(Eingabewert,33,nächsterElementeintrag);
        Eingabewert[32]=1;entferntZusammenfassung(Eingabewert,33,attrappeStartwert);memset(Eingabewert,0,33);
        unsigned Zahl=Länge<32?Länge:32;memcpy(zielWert,nächsterElementeintrag,Zahl);memset(nächsterElementeintrag,0,32);zielWert+=Zahl;Länge-=Zahl;}return 0;}
    uintptr_t grenzwertWert=platineVergangeneMillisekunden()+1000;
    while(Länge){if((zufälligRegisterliste(0x18)&0x80000020u)||platineVergangeneMillisekunden()>grenzwertWert)return -1;
        if(!(zufälligRegisterliste(0x24)&255))continue;uint32_t Wert=zufälligRegisterliste(0x20);
        for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<4&&Länge;ordnungszahlIndex++,Länge--){*zielWert++=Wert&255;Wert>>=8;}}
    return 0;
}
