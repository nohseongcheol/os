#include "../benennung/maschineBindenNamen.h"
#include "aufrufen.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *cAusgabe(size_t *);
extern const char *javaVorabübersetzungQuelltext(const char *);
typedef struct { unsigned char bezeichnerWert[16];uint16_t typKategorie,maschineTyp;uint32_t versionNummer;uint64_t eintragPunkt,programmKopfVersatzwert,abschnittKopfVersatzwert;uint32_t konfigurationBitliste;uint16_t größe,programmKopfGröße,programmKopfAnzahl,abschnittKopfGröße,abschnittKopfAnzahl,abschnittNameTabelle; } kopfbereichWert;
typedef struct {uint32_t typKategorie,konfigurationBitliste;uint64_t versatzwertWert,adresse,physischAdresse,dateibereichsgröße,speicherbereichsgröße,ausrichtenGrenzstelle;} segmentWert;
static unsigned char abbild[16384];
static int veröffentlichenEintrag(const char *Name){
    size_t elementeintragAnzahl;const unsigned char*ursprünglichDaten=cAusgabe(&elementeintragAnzahl);if(elementeintragAnzahl<sizeof(kopfbereichWert))return -1;
    kopfbereichWert ausführdateiKopf;memcpy(&ausführdateiKopf,ursprünglichDaten,sizeof(ausführdateiKopf));
    if(ausführdateiKopf.typKategorie!=2||ausführdateiKopf.maschineTyp!=183||ausführdateiKopf.programmKopfGröße!=sizeof(segmentWert)||!ausführdateiKopf.programmKopfAnzahl||ausführdateiKopf.programmKopfAnzahl>16||ausführdateiKopf.programmKopfVersatzwert>elementeintragAnzahl||ausführdateiKopf.programmKopfAnzahl*sizeof(segmentWert)>elementeintragAnzahl-ausführdateiKopf.programmKopfVersatzwert)return -1;
    ausführdateiKopf.programmKopfVersatzwert=sizeof(ausführdateiKopf);ausführdateiKopf.abschnittKopfVersatzwert=ausführdateiKopf.abschnittKopfAnzahl=ausführdateiKopf.abschnittKopfGröße=ausführdateiKopf.abschnittNameTabelle=0;memcpy(abbild,&ausführdateiKopf,sizeof(ausführdateiKopf));
    size_t hilfsInformation=sizeof(ausführdateiKopf)+ausführdateiKopf.programmKopfAnzahl*sizeof(segmentWert),nächsterElementeintrag=4096;unsigned char seiteListe[3072]={0};int gültigEintragPunkt=0;
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<ausführdateiKopf.programmKopfAnzahl;ordnungszahlIndex++){
        segmentWert datenPosition;kopfbereichWert ursprünglich;memcpy(&ursprünglich,ursprünglichDaten,sizeof(ursprünglich));memcpy(&datenPosition,ursprünglichDaten+ursprünglich.programmKopfVersatzwert+ordnungszahlIndex*sizeof(datenPosition),sizeof(datenPosition));
        if(datenPosition.versatzwertWert>elementeintragAnzahl||datenPosition.dateibereichsgröße>elementeintragAnzahl-datenPosition.versatzwertWert||datenPosition.dateibereichsgröße>datenPosition.speicherbereichsgröße)return -1;
        if(datenPosition.typKategorie==1){
            if((datenPosition.konfigurationBitliste&~7u)||!(datenPosition.konfigurationBitliste&4)||(datenPosition.konfigurationBitliste&3)==3||datenPosition.adresse<0x02000000||datenPosition.adresse>0x02c00000||datenPosition.speicherbereichsgröße>0x02c00000-datenPosition.adresse)return -1;
            if((datenPosition.konfigurationBitliste&1)&&ausführdateiKopf.eintragPunkt>=datenPosition.adresse&&ausführdateiKopf.eintragPunkt-datenPosition.adresse<datenPosition.dateibereichsgröße&&!(ausführdateiKopf.eintragPunkt&3))gültigEintragPunkt=1;
            size_t vorangehendWert=datenPosition.adresse&4095,byteWerte=datenPosition.dateibereichsgröße?vorangehendWert+datenPosition.dateibereichsgröße:0;
            if(nächsterElementeintrag>sizeof(abbild)||byteWerte>sizeof(abbild)-nächsterElementeintrag){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(nächsterElementeintrag+byteWerte),(unsigned)sizeof(abbild));return -1;}
            if(byteWerte)memcpy(abbild+nächsterElementeintrag+vorangehendWert,ursprünglichDaten+datenPosition.versatzwertWert,datenPosition.dateibereichsgröße);
            datenPosition.adresse-=vorangehendWert;datenPosition.physischAdresse=datenPosition.adresse;datenPosition.speicherbereichsgröße+=vorangehendWert;datenPosition.dateibereichsgröße=byteWerte;datenPosition.versatzwertWert=nächsterElementeintrag;datenPosition.ausrichtenGrenzstelle=4096;
            for(uint64_t seiteWert=datenPosition.adresse;seiteWert<datenPosition.adresse+datenPosition.speicherbereichsgröße;seiteWert+=4096){unsigned nachschlagenIndex=(seiteWert-0x02000000)/4096;if(nachschlagenIndex>=sizeof(seiteListe)||seiteListe[nachschlagenIndex]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}seiteListe[nachschlagenIndex]=1;}
            nächsterElementeintrag+=(byteWerte+4095)&~(size_t)4095;
        }else if(datenPosition.typKategorie==4){if(datenPosition.dateibereichsgröße>4096-hilfsInformation)return -1;memcpy(abbild+hilfsInformation,ursprünglichDaten+datenPosition.versatzwertWert,datenPosition.dateibereichsgröße);datenPosition.versatzwertWert=hilfsInformation;hilfsInformation+=datenPosition.dateibereichsgröße;}
        else if(datenPosition.typKategorie!=0&&datenPosition.typKategorie!=6&&datenPosition.typKategorie!=0x6474e551)return -1;
        memcpy(abbild+ausführdateiKopf.programmKopfVersatzwert+ordnungszahlIndex*sizeof(datenPosition),&datenPosition,sizeof(datenPosition));
    }
    if(!gültigEintragPunkt)return -1;
    intptr_t dateiKennwert=benutzerAufrufen(3,(uintptr_t)Name,577,0600,0,0,0);if(dateiKennwert<0){printf("cc: cannot create output file, error %d\n",(int)dateiKennwert);return -1;}
    intptr_t geschrieben=benutzerAufrufen(1,dateiKennwert,(uintptr_t)abbild,nächsterElementeintrag,0,0,0);benutzerAufrufen(4,dateiKennwert,0,0,0,0,0);return geschrieben==(intptr_t)nächsterElementeintrag?0:-1;
}
int benutzerProgrammStarten(int methodeBetriebsart){
    char eingabe[256],ausgewähltEintrag[256],ausgabe[256]="a.elf";
    int argumenteAnzahl=benutzerAufrufen(15,UINTPTR_MAX,0,0,0,0,0);
    if(argumenteAnzahl!=1&&argumenteAnzahl!=3){printf(methodeBetriebsart?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(benutzerAufrufen(15,0,(uintptr_t)eingabe,sizeof(eingabe),0,0,0)<0)return 2;
    if(argumenteAnzahl==1&&(!strcmp(eingabe,"--version")||!strcmp(eingabe,"-version"))){printf(methodeBetriebsart?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(argumenteAnzahl==3){benutzerAufrufen(15,1,(uintptr_t)ausgewähltEintrag,sizeof(ausgewähltEintrag),0,0,0);if(strcmp(ausgewähltEintrag,"-o")||benutzerAufrufen(15,2,(uintptr_t)ausgabe,sizeof(ausgabe),0,0,0)<0)return 2;}
    if(!strcmp(eingabe,ausgabe)){printf("cc: input and output must differ\n");return 2;}
    TCCState*zeichenketteDaten=tcc_new();if(!zeichenketteDaten)return 1;
    tcc_undefine_symbol(zeichenketteDaten,"__linux__");tcc_undefine_symbol(zeichenketteDaten,"__linux");tcc_undefine_symbol(zeichenketteDaten,"linux");
    tcc_undefine_symbol(zeichenketteDaten,"__unix__");tcc_undefine_symbol(zeichenketteDaten,"__unix");tcc_undefine_symbol(zeichenketteDaten,"unix");
    tcc_undefine_symbol(zeichenketteDaten,"__STDC_HOSTED__");tcc_define_symbol(zeichenketteDaten,"__STDC_HOSTED__","0");tcc_define_symbol(zeichenketteDaten,"__JKOROS__","1");
    tcc_set_options(zeichenketteDaten,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(zeichenketteDaten,"/sdk/include");
    int zurückgegebenWert=tcc_set_output_type(zeichenketteDaten,TCC_OUTPUT_EXE);
    if(!zurückgegebenWert){if(methodeBetriebsart){const char*ursprünglichDaten=javaVorabübersetzungQuelltext(eingabe);zurückgegebenWert=ursprünglichDaten?tcc_compile_string(zeichenketteDaten,ursprünglichDaten):-1;}else zurückgegebenWert=tcc_add_file(zeichenketteDaten,eingabe);}
    if(!zurückgegebenWert)zurückgegebenWert=tcc_add_file(zeichenketteDaten,"/sdk/lib/start.o");
    if(!zurückgegebenWert)zurückgegebenWert=tcc_add_file(zeichenketteDaten,"/sdk/lib/crt.o");
    if(!zurückgegebenWert&&methodeBetriebsart)zurückgegebenWert=tcc_add_file(zeichenketteDaten,"/sdk/lib/aot-runtime.o");
    if(!zurückgegebenWert)zurückgegebenWert=tcc_add_file(zeichenketteDaten,"/sdk/lib/libposix-kor-user.a");
    if(!zurückgegebenWert)zurückgegebenWert=tcc_output_file(zeichenketteDaten,"/@cc-output");
    if(!zurückgegebenWert)zurückgegebenWert=veröffentlichenEintrag(ausgabe);
    tcc_delete(zeichenketteDaten);
    if(zurückgegebenWert){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(methodeBetriebsart?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",ausgabe);return 0;
}
