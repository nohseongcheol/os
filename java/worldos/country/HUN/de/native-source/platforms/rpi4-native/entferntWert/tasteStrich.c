#include "entferntWert.h"
#include <string.h>
#include "zweiSetzenTastaturTabelle.h"
static unsigned steuerungWert,verschiebenTaste,HangulText;
typedef struct {unsigned ersterElementeintrag,mitte,endung;} zusammensetzungStatuswert;
static zusammensetzungStatuswert Zusammenstellung,protokolldateiAufzeichnung[16];
static unsigned protokolldateiAnzahl;
void bestätigenEntferntTaste(void){memset(&Zusammenstellung,0,sizeof(Zusammenstellung));protokolldateiAnzahl=0;}
void entferntTasteStrichInitialisieren(void){steuerungWert=verschiebenTaste=HangulText=0;bestätigenEntferntTaste();}
static void textAblegen(unsigned Wert){
    unsigned char Text[4];unsigned Zahl;
    if(Wert<128){Text[0]=Wert;Zahl=1;}else if(Wert<2048){Text[0]=0xc0|(Wert>>6);Text[1]=0x80|(Wert&63);Zahl=2;}
    else if(Wert<65536){Text[0]=0xe0|(Wert>>12);Text[1]=0x80|((Wert>>6)&63);Text[2]=0x80|(Wert&63);Zahl=3;}
    else{Text[0]=0xf0|(Wert>>18);Text[1]=0x80|((Wert>>12)&63);Text[2]=0x80|((Wert>>6)&63);Text[3]=0x80|(Wert&63);Zahl=4;}
    zuführenEntferntEingabe(Text,Zahl);
}
static int eintragFinden(const unsigned *eintragListe,unsigned Zahl,unsigned Wert){for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<Zahl;ordnungszahlIndex++)if(eintragListe[ordnungszahlIndex]==Wert)return ordnungszahlIndex;return -1;}
static unsigned duplikatFinden(const unsigned Tabelle[][3],unsigned Zahl,unsigned ersterOperand,unsigned zweiterOperand){for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<Zahl;ordnungszahlIndex++)if(Tabelle[ordnungszahlIndex][0]==ersterOperand&&Tabelle[ordnungszahlIndex][1]==zweiterOperand)return Tabelle[ordnungszahlIndex][2];return 0;}
static unsigned zusammengesetztText(void){
    if(Zusammenstellung.ersterElementeintrag&&Zusammenstellung.mitte)return 0xac00+(eintragFinden(anfänglichHangulBuchstabeTabelle,19,Zusammenstellung.ersterElementeintrag)*21+eintragFinden(mittellautHangulBuchstabeTabelle,21,Zusammenstellung.mitte))*28+(Zusammenstellung.endung?eintragFinden(abschließendHangulBuchstabeTabelle,28,Zusammenstellung.endung):0);
    return Zusammenstellung.ersterElementeintrag?Zusammenstellung.ersterElementeintrag:Zusammenstellung.mitte;
}
static int zuführenHangul(unsigned tasteStrich){
    unsigned hangulBuchstabeWert=0;for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<sizeof(tasteAnordnung)/sizeof(tasteAnordnung[0]);ordnungszahlIndex++)if(tasteAnordnung[ordnungszahlIndex][0]==tasteStrich)hangulBuchstabeWert=tasteAnordnung[ordnungszahlIndex][1];
    if(!hangulBuchstabeWert&&tasteStrich>='A'&&tasteStrich<='Z')return zuführenHangul(tasteStrich+32);if(!hangulBuchstabeWert)return 0;
    unsigned vorherigElementeintrag=zusammengesetztText(),bestätigenWert=0;zusammensetzungStatuswert davorWert=Zusammenstellung;
    if(protokolldateiAnzahl<16)protokolldateiAufzeichnung[protokolldateiAnzahl++]=davorWert;
    if(eintragFinden(anfänglichHangulBuchstabeTabelle,19,hangulBuchstabeWert)>=0){
        if(Zusammenstellung.ersterElementeintrag&&Zusammenstellung.mitte&&!Zusammenstellung.endung&&eintragFinden(abschließendHangulBuchstabeTabelle,28,hangulBuchstabeWert)>=0)Zusammenstellung.endung=hangulBuchstabeWert;
        else{unsigned überlagernWert=duplikatFinden(zusammengesetztesWortAbschließendHangulBuchstabe,11,Zusammenstellung.endung,hangulBuchstabeWert);if(Zusammenstellung.endung&&überlagernWert)Zusammenstellung.endung=überlagernWert;
            else{bestätigenWert=vorherigElementeintrag;bestätigenEntferntTaste();Zusammenstellung.ersterElementeintrag=hangulBuchstabeWert;protokolldateiAnzahl=1;memset(protokolldateiAufzeichnung,0,sizeof(zusammensetzungStatuswert));}}
    }else if(Zusammenstellung.endung){
        unsigned linksSeiteRand=0,rechts=Zusammenstellung.endung;for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<11;ordnungszahlIndex++)if(zusammengesetztesWortAbschließendHangulBuchstabe[ordnungszahlIndex][2]==Zusammenstellung.endung){linksSeiteRand=zusammengesetztesWortAbschließendHangulBuchstabe[ordnungszahlIndex][0];rechts=zusammengesetztesWortAbschließendHangulBuchstabe[ordnungszahlIndex][1];break;}
        Zusammenstellung.endung=linksSeiteRand;bestätigenWert=zusammengesetztText();bestätigenEntferntTaste();Zusammenstellung.ersterElementeintrag=rechts;Zusammenstellung.mitte=hangulBuchstabeWert;protokolldateiAnzahl=2;
        memset(protokolldateiAufzeichnung,0,2*sizeof(zusammensetzungStatuswert));protokolldateiAufzeichnung[1].ersterElementeintrag=rechts;
    }else if(Zusammenstellung.mitte){unsigned überlagernWert=duplikatFinden(zusammengesetztesWortMittellautHangulBuchstabe,7,Zusammenstellung.mitte,hangulBuchstabeWert);
        if(überlagernWert)Zusammenstellung.mitte=überlagernWert;else{bestätigenWert=vorherigElementeintrag;bestätigenEntferntTaste();Zusammenstellung.mitte=hangulBuchstabeWert;protokolldateiAnzahl=1;memset(protokolldateiAufzeichnung,0,sizeof(zusammensetzungStatuswert));}
    }else Zusammenstellung.mitte=hangulBuchstabeWert;
    if(vorherigElementeintrag)textAblegen(127);if(bestätigenWert)textAblegen(bestätigenWert);unsigned jetztWert=zusammengesetztText();if(jetztWert)textAblegen(jetztWert);return 1;
}
void entferntTasteStrich(unsigned symbol,int drückenWert){
    if(symbol==0xffe3||symbol==0xffe4){steuerungWert=drückenWert;return;}
    if(symbol==0xffe1||symbol==0xffe2){verschiebenTaste=drückenWert;return;}
    if(!drückenWert)return;
    if(symbol==0xffc6||symbol==0xff31||(symbol==32&&verschiebenTaste&&!steuerungWert)){
        bestätigenEntferntTaste();HangulText=!HangulText;unsigned char ereignis[]={30,3,HangulText,0,0,0,0};zuführenEntferntEingabe(ereignis,7);return;
    }
    if(symbol==0xff08&&HangulText&&!steuerungWert&&protokolldateiAnzahl){Zusammenstellung=protokolldateiAufzeichnung[--protokolldateiAnzahl];textAblegen(127);unsigned Text=zusammengesetztText();if(Text)textAblegen(Text);return;}
    if(HangulText&&!steuerungWert&&symbol<128&&zuführenHangul(symbol))return;
    bestätigenEntferntTaste();
    if((steuerungWert&&verschiebenTaste&&(symbol=='t'||symbol=='T'))||symbol==0xffc3||symbol==0xffc9){unsigned char ereignis[]={30,2,symbol==0xffc3?2:symbol==0xffc9?3:1,0,0,0,0};zuführenEntferntEingabe(ereignis,7);return;}
    const char *besondersWert=symbol==0xff08?"\177":symbol==0xff09?"\t":symbol==0xff0d?"\r":symbol==0xff1b?"\033":
        symbol==0xffff?"\033[3~":symbol==0xff50?"\033[H":symbol==0xff57?"\033[F":symbol==0xff51?"\033[D":
        symbol==0xff52?"\033[A":symbol==0xff53?"\033[C":symbol==0xff54?"\033[B":symbol==0xff55?"\033[5~":symbol==0xff56?"\033[6~":0;
    if(besondersWert){zuführenEntferntEingabe((const unsigned char*)besondersWert,strlen(besondersWert));return;}
    unsigned Wert=(symbol&0xff000000)==0x01000000?symbol&0xffffff:symbol;
    if(Wert>0x10ffff||(Wert>=0xd800&&Wert<=0xdfff)||(symbol>=0xff00&&symbol<0x1000000))return;
    if(steuerungWert){if(Wert>='a'&&Wert<='z')Wert-=96;else if(Wert>='A'&&Wert<='Z')Wert-=64;}
    textAblegen(Wert);
}
