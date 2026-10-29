#include "../benennung/maschineBindenNamen.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "aufrufen.h"
#include "Paket.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char Daten[16384];static unsigned Länge,aktuellPosition;static int istUngültig;
static unsigned kennzeichenlisteListe[512],ersterWert[512],zweiterWert[512],konstanteVorratsbereich,aktuellKlasse;
static char Text[65536];static unsigned textGröße;
typedef struct {unsigned konfigurationBitliste,Name,deskriptorDaten,befehlswortFolge,größe,lokalVariablen,stapelSpeichergerät;} methodeEintrag;
static methodeEintrag deklariertMethoden[64];static unsigned deklariertMethodeAnzahl;
static unsigned feldName[64],feldDeskriptor[64],feldKonstante[64],deklariertFeldAnzahl;
static unsigned entnehmenWert(unsigned elementeintragAnzahl){if(aktuellPosition>Länge||elementeintragAnzahl>Länge-aktuellPosition){istUngültig=1;return 0;}unsigned datenPosition=aktuellPosition;aktuellPosition+=elementeintragAnzahl;return datenPosition;}
static unsigned byteDaten(void){unsigned datenPosition=entnehmenWert(1);return istUngültig?0:Daten[datenPosition];}
static unsigned halbWert(void){unsigned waagerechteKoordinateKoordinate=byteDaten();return waagerechteKoordinateKoordinate<<8|byteDaten();}
static uint32_t istVoll(void){uint32_t waagerechteKoordinateKoordinate=halbWert();return waagerechteKoordinateKoordinate<<16|halbWert();}
static int unicodeWert(unsigned ordnungszahlIndex,const char*zeichenketteDaten){return ordnungszahlIndex>0&&ordnungszahlIndex<konstanteVorratsbereich&&kennzeichenlisteListe[ordnungszahlIndex]==1&&strlen(zeichenketteDaten)==zweiterWert[ordnungszahlIndex]&&!memcmp(Daten+ersterWert[ordnungszahlIndex],zeichenketteDaten,zweiterWert[ordnungszahlIndex]);}
static int gleichText(unsigned waagerechteKoordinateKoordinate,unsigned senkrechteKoordinateKoordinate){return waagerechteKoordinateKoordinate>0&&waagerechteKoordinateKoordinate<konstanteVorratsbereich&&senkrechteKoordinateKoordinate>0&&senkrechteKoordinateKoordinate<konstanteVorratsbereich&&kennzeichenlisteListe[waagerechteKoordinateKoordinate]==1&&kennzeichenlisteListe[senkrechteKoordinateKoordinate]==1&&zweiterWert[waagerechteKoordinateKoordinate]==zweiterWert[senkrechteKoordinateKoordinate]&&!memcmp(Daten+ersterWert[waagerechteKoordinateKoordinate],Daten+ersterWert[senkrechteKoordinateKoordinate],zweiterWert[waagerechteKoordinateKoordinate]);}
static void wertAusgeben(const char*dateiEintrag,...){if(istUngültig)return;va_list argumentDatenfeld;va_start(argumentDatenfeld,dateiEintrag);int elementeintragAnzahl=vsnprintf(Text+textGröße,sizeof(Text)-textGröße,dateiEintrag,argumentDatenfeld);va_end(argumentDatenfeld);if(elementeintragAnzahl<0||(unsigned)elementeintragAnzahl>=sizeof(Text)-textGröße){istUngültig=1;return;}textGröße+=elementeintragAnzahl;}
static int deskriptorEintrag(unsigned bezeichnerWert,int*ergebnis){
    if(bezeichnerWert<1||bezeichnerWert>=konstanteVorratsbereich||kennzeichenlisteListe[bezeichnerWert]!=1)return -1;unsigned datenPosition=ersterWert[bezeichnerWert],endeVersatzwert=datenPosition+zweiterWert[bezeichnerWert];if(datenPosition>=endeVersatzwert||Daten[datenPosition++]!='(')return -1;int eintragAnzahl=0;
    while(datenPosition<endeVersatzwert&&Daten[datenPosition]!=')'){
        unsigned zeichenKode=Daten[datenPosition++];while(zeichenKode=='['&&datenPosition<endeVersatzwert)zeichenKode=Daten[datenPosition++];
        if(zeichenKode=='L'){while(datenPosition<endeVersatzwert&&Daten[datenPosition]!=';')datenPosition++;if(datenPosition==endeVersatzwert)return -1;datenPosition++;}
        else if(zeichenKode!='I'&&zeichenKode!='Z'&&zeichenKode!='B'&&zeichenKode!='C'&&zeichenKode!='S')return -1;
        if(++eintragAnzahl>16)return -1;
    }
    if(datenPosition+1>=endeVersatzwert||Daten[datenPosition++]!=')')return -1;*ergebnis=Daten[datenPosition]=='V'?0:1;
    if(Daten[datenPosition]=='J'||Daten[datenPosition]=='D'||Daten[datenPosition]=='F')return -1;return eintragAnzahl;
}
static void attributliste(void){unsigned elementeintragAnzahl=halbWert();for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<elementeintragAnzahl&&!istUngültig;ordnungszahlIndex++){halbWert();unsigned größe=istVoll();entnehmenWert(größe);}}
static int eingabeAnalysieren(void){
    if(istVoll()!=0xcafebabe)return -1;unsigned nebenversionVersion=halbWert(),versionNummer=halbWert();if(nebenversionVersion||versionNummer<45||versionNummer>52)return -1;
    konstanteVorratsbereich=halbWert();if(konstanteVorratsbereich<1||konstanteVorratsbereich>512)return -1;
    for(unsigned ordnungszahlIndex=1;ordnungszahlIndex<konstanteVorratsbereich&&!istUngültig;ordnungszahlIndex++){
        kennzeichenlisteListe[ordnungszahlIndex]=byteDaten();switch(kennzeichenlisteListe[ordnungszahlIndex]){
        case 1:zweiterWert[ordnungszahlIndex]=halbWert();ersterWert[ordnungszahlIndex]=entnehmenWert(zweiterWert[ordnungszahlIndex]);break;case 3:case 4:ersterWert[ordnungszahlIndex]=istVoll();break;
        case 5:case 6:entnehmenWert(8);if(++ordnungszahlIndex>=konstanteVorratsbereich)return -1;break;
        case 7:case 8:case 16:ersterWert[ordnungszahlIndex]=halbWert();break;
        case 9:case 10:case 11:case 12:case 18:ersterWert[ordnungszahlIndex]=halbWert();zweiterWert[ordnungszahlIndex]=halbWert();break;
        case 15:ersterWert[ordnungszahlIndex]=byteDaten();zweiterWert[ordnungszahlIndex]=halbWert();break;default:return -1;
        }
    }
    halbWert();aktuellKlasse=halbWert();halbWert();if(aktuellKlasse<1||aktuellKlasse>=konstanteVorratsbereich||kennzeichenlisteListe[aktuellKlasse]!=7||ersterWert[aktuellKlasse]<1||ersterWert[aktuellKlasse]>=konstanteVorratsbereich||kennzeichenlisteListe[ersterWert[aktuellKlasse]]!=1)return -1;unsigned schnittstellen=halbWert();entnehmenWert(schnittstellen*2);
    deklariertFeldAnzahl=halbWert();if(deklariertFeldAnzahl>64)return -1;
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<deklariertFeldAnzahl&&!istUngültig;ordnungszahlIndex++){
        unsigned konfigurationBitliste=halbWert();feldName[ordnungszahlIndex]=halbWert();feldDeskriptor[ordnungszahlIndex]=halbWert();
        if(!(konfigurationBitliste&8))return -1;
        unsigned eintragAnzahl=halbWert();for(unsigned innerlichOrdnungszahl=0;innerlichOrdnungszahl<eintragAnzahl&&!istUngültig;innerlichOrdnungszahl++){
            unsigned Name=halbWert(),größe=istVoll();
            if(unicodeWert(Name,"ConstantValue")){if(größe!=2)return -1;feldKonstante[ordnungszahlIndex]=halbWert();}
            else entnehmenWert(größe);
        }
    }
    deklariertMethodeAnzahl=halbWert();if(deklariertMethodeAnzahl>64)return -1;
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<deklariertMethodeAnzahl&&!istUngültig;ordnungszahlIndex++){
        methodeEintrag*gruppeGröße=deklariertMethoden+ordnungszahlIndex;gruppeGröße->konfigurationBitliste=halbWert();gruppeGröße->Name=halbWert();gruppeGröße->deskriptorDaten=halbWert();unsigned eintragAnzahl=halbWert();
        for(unsigned innerlichOrdnungszahl=0;innerlichOrdnungszahl<eintragAnzahl&&!istUngültig;innerlichOrdnungszahl++){
            unsigned Name=halbWert(),größe=istVoll(),ausführenVorgang=aktuellPosition;
            if(größe>Länge-aktuellPosition)return -1;
            if(unicodeWert(Name,"Code")){
                gruppeGröße->stapelSpeichergerät=halbWert();gruppeGröße->lokalVariablen=halbWert();gruppeGröße->größe=istVoll();gruppeGröße->befehlswortFolge=entnehmenWert(gruppeGröße->größe);
                if(gruppeGröße->stapelSpeichergerät>128||gruppeGröße->lokalVariablen>128||gruppeGröße->größe>8192||halbWert())return -1;attributliste();
            }else entnehmenWert(größe);
            if(aktuellPosition!=ausführenVorgang+größe)return -1;
        }
        if(!unicodeWert(gruppeGröße->Name,"<init>")&&(!(gruppeGröße->konfigurationBitliste&8)||(gruppeGröße->konfigurationBitliste&(0x100|0x20))||!gruppeGröße->größe))return -1;
    }
    attributliste();return istUngültig||aktuellPosition!=Länge?-1:0;
}
static void konstanteWert(unsigned bezeichnerWert){
    if(!bezeichnerWert||bezeichnerWert>=konstanteVorratsbereich){istUngültig=1;return;}
    if(kennzeichenlisteListe[bezeichnerWert]==3)wertAusgeben("P(%uU);",ersterWert[bezeichnerWert]);
    else if(kennzeichenlisteListe[bezeichnerWert]==8)wertAusgeben("P((W)k%u);",bezeichnerWert);else istUngültig=1;
}
static void aufrufen(unsigned bezeichnerWert,int virtuellAufrufVorgang){
    if(bezeichnerWert<1||bezeichnerWert>=konstanteVorratsbereich||(kennzeichenlisteListe[bezeichnerWert]!=10&&kennzeichenlisteListe[bezeichnerWert]!=11)||ersterWert[bezeichnerWert]<1||ersterWert[bezeichnerWert]>=konstanteVorratsbereich||kennzeichenlisteListe[ersterWert[bezeichnerWert]]!=7||zweiterWert[bezeichnerWert]<1||zweiterWert[bezeichnerWert]>=konstanteVorratsbereich||kennzeichenlisteListe[zweiterWert[bezeichnerWert]]!=12){istUngültig=1;return;}
    unsigned eigentümerObjekt=ersterWert[ersterWert[bezeichnerWert]],Name=ersterWert[zweiterWert[bezeichnerWert]],deskriptorDaten=zweiterWert[zweiterWert[bezeichnerWert]];int ergebnis=0,elementeintragAnzahl=deskriptorEintrag(deskriptorDaten,&ergebnis);if(elementeintragAnzahl<0){istUngültig=1;return;}
    for(int ordnungszahlIndex=elementeintragAnzahl;ordnungszahlIndex>0;ordnungszahlIndex--)wertAusgeben("x[%d]=Q();",ordnungszahlIndex-1);if(virtuellAufrufVorgang)wertAusgeben("Q();");
    if(!virtuellAufrufVorgang&&gleichText(eigentümerObjekt,ersterWert[aktuellKlasse])){
        unsigned gruppeGröße=0;for(;gruppeGröße<deklariertMethodeAnzahl;gruppeGröße++)if(gleichText(Name,deklariertMethoden[gruppeGröße].Name)&&gleichText(deskriptorDaten,deklariertMethoden[gruppeGröße].deskriptorDaten))break;
        if(gruppeGröße==deklariertMethodeAnzahl||!(deklariertMethoden[gruppeGröße].konfigurationBitliste&8)){istUngültig=1;return;}
        if(ergebnis)wertAusgeben("P(");wertAusgeben("m%u(",gruppeGröße);for(int ordnungszahlIndex=0;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++)wertAusgeben(ordnungszahlIndex?",x[%d]":"x[%d]",ordnungszahlIndex);wertAusgeben(ergebnis?"));":" );");return;
    }
    if((virtuellAufrufVorgang&&unicodeWert(eigentümerObjekt,"java/io/PrintStream")&& (unicodeWert(Name,"print")||unicodeWert(Name,"println")))||(!virtuellAufrufVorgang&&unicodeWert(eigentümerObjekt,"Deutsch/eigen/Ausgabe"))){
        if(unicodeWert(deskriptorDaten,"(I)V")&&(unicodeWert(Name,"print")||unicodeWert(Name,"println")||unicodeWert(Name,"nummerSchreiben"))){wertAusgeben("jprint(x[0],1,%d);",unicodeWert(Name,"print")?0:1);return;}
        if(unicodeWert(deskriptorDaten,"(Ljava/lang/String;)V")&&(unicodeWert(Name,"print")||unicodeWert(Name,"println")||unicodeWert(Name,"schreiben")||unicodeWert(Name,"zeileSchreiben"))){wertAusgeben("jprint(x[0],0,%d);",unicodeWert(Name,"print")||unicodeWert(Name,"schreiben")?0:1);return;}
        if(unicodeWert(deskriptorDaten,"()V")&&unicodeWert(Name,"println")){wertAusgeben("jprint((W)\"\",0,1);");return;}
    }
    if(!virtuellAufrufVorgang&&unicodeWert(eigentümerObjekt,"Deutsch/eigen/Datei")){
        if(unicodeWert(Name,"schreiben")&&unicodeWert(deskriptorDaten,"(Ljava/lang/String;Ljava/lang/String;)V")){wertAusgeben("jfwrite(x[0],x[1]);");return;}
        if(unicodeWert(Name,"lesen")&&unicodeWert(deskriptorDaten,"(Ljava/lang/String;)Ljava/lang/String;")){wertAusgeben("P(jfread(x[0]));");return;}
    }
    istUngültig=1;
}
static void methodeÜbersetzen(unsigned nachschlagenIndex){
    methodeEintrag*gruppeGröße=deklariertMethoden+nachschlagenIndex;if(unicodeWert(gruppeGröße->Name,"<init>"))return;int ergebnis,elementeintragAnzahl=deskriptorEintrag(gruppeGröße->deskriptorDaten,&ergebnis);if(elementeintragAnzahl<0){istUngültig=1;return;}
    wertAusgeben("static W m%u(",nachschlagenIndex);for(int ordnungszahlIndex=0;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++)wertAusgeben(ordnungszahlIndex?",W a%d":"W a%d",ordnungszahlIndex);if(!elementeintragAnzahl)wertAusgeben("void");
    if((unsigned)elementeintragAnzahl>gruppeGröße->lokalVariablen){istUngültig=1;return;}
    wertAusgeben("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",gruppeGröße->lokalVariablen?gruppeGröße->lokalVariablen:1);for(int ordnungszahlIndex=0;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++)wertAusgeben("v[%d]=a%d;",ordnungszahlIndex,ordnungszahlIndex);
    unsigned gespeichert=Länge;Länge=gruppeGröße->befehlswortFolge+gruppeGröße->größe;aktuellPosition=gruppeGröße->befehlswortFolge;
    while(aktuellPosition<Länge&&!istUngültig){unsigned befehlPosition=aktuellPosition-gruppeGröße->befehlswortFolge,vorgangWert=byteDaten();wertAusgeben("L%u:;",befehlPosition);
        if(vorgangWert==0){}
        else if(vorgangWert==1)wertAusgeben("P(0);");
        else if(vorgangWert>=2&&vorgangWert<=8)wertAusgeben("P(%uU);",vorgangWert-3);
        else if(vorgangWert==16){int Wert=(int8_t)byteDaten();wertAusgeben("P(%uU);",(unsigned)Wert);}
        else if(vorgangWert==17){int Wert=(int16_t)halbWert();wertAusgeben("P(%uU);",(unsigned)Wert);}
        else if(vorgangWert==18||vorgangWert==19)konstanteWert(vorgangWert==18?byteDaten():halbWert());
        else if(vorgangWert==21||vorgangWert==25){unsigned ordnungszahlIndex=byteDaten();if(ordnungszahlIndex>=gruppeGröße->lokalVariablen)istUngültig=1;wertAusgeben("P(v[%u]);",ordnungszahlIndex);}
        else if((vorgangWert>=26&&vorgangWert<=29)||(vorgangWert>=42&&vorgangWert<=45)){unsigned ordnungszahlIndex=vorgangWert>=42?vorgangWert-42:vorgangWert-26;if(ordnungszahlIndex>=gruppeGröße->lokalVariablen)istUngültig=1;wertAusgeben("P(v[%u]);",ordnungszahlIndex);}
        else if(vorgangWert==54||vorgangWert==58){unsigned ordnungszahlIndex=byteDaten();if(ordnungszahlIndex>=gruppeGröße->lokalVariablen)istUngültig=1;wertAusgeben("v[%u]=Q();",ordnungszahlIndex);}
        else if((vorgangWert>=59&&vorgangWert<=62)||(vorgangWert>=75&&vorgangWert<=78)){unsigned ordnungszahlIndex=vorgangWert>=75?vorgangWert-75:vorgangWert-59;if(ordnungszahlIndex>=gruppeGröße->lokalVariablen)istUngültig=1;wertAusgeben("v[%u]=Q();",ordnungszahlIndex);}
        else if(vorgangWert==46||vorgangWert==50||vorgangWert==51||vorgangWert==52||vorgangWert==53)wertAusgeben("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(vorgangWert==79||vorgangWert==83||vorgangWert==84||vorgangWert==85||vorgangWert==86)wertAusgeben("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",vorgangWert==84?"(unsigned)(signed char)q":vorgangWert==85?"(unsigned short)q":vorgangWert==86?"(unsigned)(short)q":"q");
        else if(vorgangWert==87)wertAusgeben("Q();");
        else if(vorgangWert==89)wertAusgeben("q=Q();P(q);P(q);");
        else if(vorgangWert==90)wertAusgeben("q=Q();r=Q();P(q);P(r);P(q);");
        else if(vorgangWert==95)wertAusgeben("q=Q();r=Q();P(q);P(r);");
        else if(vorgangWert==96||vorgangWert==100||vorgangWert==104||vorgangWert==120||vorgangWert==124||vorgangWert==126||vorgangWert==128||vorgangWert==130){const char*kodierungWert=vorgangWert==96?"+":vorgangWert==100?"-":vorgangWert==104?"*":vorgangWert==120?"<<":vorgangWert==124?">>":vorgangWert==126?"&":vorgangWert==128?"|":"^";wertAusgeben("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kodierungWert,vorgangWert==120||vorgangWert==124?"%32":"");}
        else if(vorgangWert==108||vorgangWert==112)wertAusgeben("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",vorgangWert==112);
        else if(vorgangWert==116)wertAusgeben("P(0U-(unsigned)Q());");
        else if(vorgangWert==122)wertAusgeben("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(vorgangWert==132){unsigned ordnungszahlIndex=byteDaten();int unterschiedWert=(int8_t)byteDaten();if(ordnungszahlIndex>=gruppeGröße->lokalVariablen)istUngültig=1;wertAusgeben("v[%u]=(unsigned)v[%u]+%uU;",ordnungszahlIndex,ordnungszahlIndex,(unsigned)unterschiedWert);}
        else if(vorgangWert>=145&&vorgangWert<=147)wertAusgeben("P((unsigned)(%s)Q());",vorgangWert==145?"signed char":vorgangWert==146?"unsigned short":"short");
        else if(vorgangWert>=153&&vorgangWert<=166){int zielobjektWert=(int)befehlPosition+(int16_t)halbWert();const char*vergleichWert[]={"==","!=","<",">=",">","<="};if(zielobjektWert<0||zielobjektWert>=(int)gruppeGröße->größe){istUngültig=1;break;}if(vorgangWert<159)wertAusgeben("if((int)Q()%s0)goto L%d;",vergleichWert[vorgangWert-153],zielobjektWert);else if(vorgangWert<165)wertAusgeben("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",vergleichWert[vorgangWert-159],zielobjektWert);else wertAusgeben("q=Q();r=Q();if(r%sq)goto L%d;",vorgangWert==165?"==":"!=",zielobjektWert);}
        else if(vorgangWert==167){int zielobjektWert=(int)befehlPosition+(int16_t)halbWert();if(zielobjektWert<0||zielobjektWert>=(int)gruppeGröße->größe)istUngültig=1;wertAusgeben("goto L%d;",zielobjektWert);}
        else if(vorgangWert==172||vorgangWert==176)wertAusgeben("return Q();");else if(vorgangWert==177)wertAusgeben("return 0;");
        else if(vorgangWert==178||vorgangWert==179){unsigned bezeichnerWert=halbWert();if(bezeichnerWert<1||bezeichnerWert>=konstanteVorratsbereich||kennzeichenlisteListe[bezeichnerWert]!=9||ersterWert[bezeichnerWert]>=konstanteVorratsbereich||zweiterWert[bezeichnerWert]>=konstanteVorratsbereich||kennzeichenlisteListe[ersterWert[bezeichnerWert]]!=7||kennzeichenlisteListe[zweiterWert[bezeichnerWert]]!=12){istUngültig=1;break;}unsigned eigentümerObjekt=ersterWert[ersterWert[bezeichnerWert]],Name=ersterWert[zweiterWert[bezeichnerWert]],deskriptorDaten=zweiterWert[zweiterWert[bezeichnerWert]];
            if(vorgangWert==178&&unicodeWert(eigentümerObjekt,"java/lang/System")&&unicodeWert(Name,"out")&&unicodeWert(deskriptorDaten,"Ljava/io/PrintStream;"))wertAusgeben("P(1);");
            else {unsigned dateiEintrag=0;while(dateiEintrag<deklariertFeldAnzahl&&(!gleichText(Name,feldName[dateiEintrag])||!gleichText(deskriptorDaten,feldDeskriptor[dateiEintrag])))dateiEintrag++;if(!gleichText(eigentümerObjekt,ersterWert[aktuellKlasse])||dateiEintrag==deklariertFeldAnzahl){istUngültig=1;break;}wertAusgeben(vorgangWert==178?"P(fields[%u]);":"fields[%u]=Q();",dateiEintrag);}}
        else if(vorgangWert==182||vorgangWert==184)aufrufen(halbWert(),vorgangWert==182);
        else if(vorgangWert==188){unsigned typKategorie=byteDaten();if(typKategorie!=4&&typKategorie!=5&&typKategorie!=8&&typKategorie!=9&&typKategorie!=10)istUngültig=1;wertAusgeben("P(jarray((int)Q()));");}
        else if(vorgangWert==190)wertAusgeben("P(jlength(Q()));");
        else if(vorgangWert==198||vorgangWert==199){int zielobjektWert=(int)befehlPosition+(int16_t)halbWert();if(zielobjektWert<0||zielobjektWert>=(int)gruppeGröße->größe)istUngültig=1;wertAusgeben("if(Q()%s0)goto L%d;",vorgangWert==198?"==":"!=",zielobjektWert);}
        else istUngültig=1;
        if(istUngültig)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",nachschlagenIndex,vorgangWert,befehlPosition);
        wertAusgeben("\n");
    }
    Länge=gespeichert;wertAusgeben("jfail();return 0;}\n");
}
static unsigned zeichenketteEinheit(unsigned *datenPosition,unsigned endeVersatzwert){
    if(*datenPosition>=endeVersatzwert){istUngültig=1;return 0;}unsigned zeichenKode=Daten[(*datenPosition)++];
    if(zeichenKode<128)return zeichenKode;
    unsigned elementeintragAnzahl=zeichenKode>=0xc0&&zeichenKode<=0xdf?1:zeichenKode>=0xe0&&zeichenKode<=0xef?2:3;
    if(elementeintragAnzahl==3||elementeintragAnzahl>endeVersatzwert-*datenPosition){istUngültig=1;return 0;}unsigned Wert=zeichenKode&((1u<<(6-elementeintragAnzahl))-1);
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++){unsigned nächsterElementeintrag=Daten[(*datenPosition)++];if((nächsterElementeintrag&0xc0)!=0x80)istUngültig=1;Wert=Wert<<6|(nächsterElementeintrag&63);}
    if((elementeintragAnzahl==1&&Wert<128&&Wert!=0)||(elementeintragAnzahl==2&&Wert<2048))istUngültig=1;return Wert;
}
static void zeichenketteKonstante(unsigned bezeichnerWert){
    unsigned vorzeichenlosWert=ersterWert[bezeichnerWert];if(vorzeichenlosWert<1||vorzeichenlosWert>=konstanteVorratsbereich||kennzeichenlisteListe[vorzeichenlosWert]!=1){istUngültig=1;return;}wertAusgeben("static const unsigned char k%u[]={",bezeichnerWert);
    unsigned datenPosition=ersterWert[vorzeichenlosWert],endeVersatzwert=datenPosition+zweiterWert[vorzeichenlosWert];
    while(datenPosition<endeVersatzwert&&!istUngültig){unsigned zeichenKode=zeichenketteEinheit(&datenPosition,endeVersatzwert);
        if(zeichenKode>=0xd800&&zeichenKode<=0xdbff){unsigned niedrigTeil=zeichenketteEinheit(&datenPosition,endeVersatzwert);if(niedrigTeil<0xdc00||niedrigTeil>0xdfff){istUngültig=1;break;}zeichenKode=0x10000+((zeichenKode-0xd800)<<10)+niedrigTeil-0xdc00;}
        else if(zeichenKode>=0xdc00&&zeichenKode<=0xdfff){istUngültig=1;break;}
        if(!zeichenKode){printf("jaot: embedded NUL string needs JVM mode\n");istUngültig=1;break;}
        if(zeichenKode<128)wertAusgeben("%u,",zeichenKode);
        else{unsigned elementeintragAnzahl=zeichenKode<2048?2:zeichenKode<65536?3:4;wertAusgeben("%u,",(elementeintragAnzahl==2?0xc0:elementeintragAnzahl==3?0xe0:0xf0)|(zeichenKode>>(6*(elementeintragAnzahl-1))));for(unsigned ordnungszahlIndex=elementeintragAnzahl-1;ordnungszahlIndex;ordnungszahlIndex--)wertAusgeben("%u,",0x80|((zeichenKode>>(6*(ordnungszahlIndex-1)))&63));}
    }wertAusgeben("0};\n");
}
const char *javaVorabübersetzungQuelltext(const char*Name){
    size_t elementeintragAnzahl=strlen(Name);
    if(elementeintragAnzahl>4&&!strcmp(Name+elementeintragAnzahl-4,".jar")){
        if(jARÖffnen(Name)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char pfad[256];const char*eintragMethode=jARHauptvorgang();elementeintragAnzahl=strlen(eintragMethode);if(elementeintragAnzahl+6>=sizeof(pfad))return 0;
        for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++)pfad[ordnungszahlIndex]=eintragMethode[ordnungszahlIndex]=='.'?'/':eintragMethode[ordnungszahlIndex];strcpy(pfad+elementeintragAnzahl,".class");int eintragAnzahl=jARLesen(pfad,Daten,sizeof(Daten));if(eintragAnzahl<0)return 0;Länge=eintragAnzahl;
    }else{intptr_t dateiKennwert=benutzerAufrufen(3,(uintptr_t)Name,0,0,0,0,0);if(dateiKennwert<0)return 0;intptr_t eintragAnzahl=benutzerAufrufen(9,dateiKennwert,0,0,0,0,0);if(eintragAnzahl<0||eintragAnzahl>sizeof(Daten)){benutzerAufrufen(4,dateiKennwert,0,0,0,0,0);return 0;}intptr_t empfangenWertAnzahl=benutzerAufrufen(2,dateiKennwert,(uintptr_t)Daten,eintragAnzahl,0,0,0);benutzerAufrufen(4,dateiKennwert,0,0,0,0,0);if(empfangenWertAnzahl!=eintragAnzahl)return 0;Länge=eintragAnzahl;}
    if(eingabeAnalysieren()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    wertAusgeben("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned ordnungszahlIndex=1;ordnungszahlIndex<konstanteVorratsbereich&&!istUngültig;ordnungszahlIndex++)if(kennzeichenlisteListe[ordnungszahlIndex]==8)zeichenketteKonstante(ordnungszahlIndex);
    if(istUngültig)return 0;
    int eintragPunkt=-1,anfänglichWert=-1;
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<deklariertMethodeAnzahl;ordnungszahlIndex++)if(!unicodeWert(deklariertMethoden[ordnungszahlIndex].Name,"<init>")){
        int ergebnis,eintragAnzahl=deskriptorEintrag(deklariertMethoden[ordnungszahlIndex].deskriptorDaten,&ergebnis);if(eintragAnzahl<0)return 0;wertAusgeben("static W m%u(",ordnungszahlIndex);for(int innerlichOrdnungszahl=0;innerlichOrdnungszahl<eintragAnzahl;innerlichOrdnungszahl++)wertAusgeben(innerlichOrdnungszahl?",W":"W");if(!eintragAnzahl)wertAusgeben("void");wertAusgeben(");\n");
        if(unicodeWert(deklariertMethoden[ordnungszahlIndex].Name,"main")&&unicodeWert(deklariertMethoden[ordnungszahlIndex].deskriptorDaten,"([Ljava/lang/String;)V")&&(deklariertMethoden[ordnungszahlIndex].konfigurationBitliste&9)==9)eintragPunkt=ordnungszahlIndex;
        if(unicodeWert(deklariertMethoden[ordnungszahlIndex].Name,"<clinit>"))anfänglichWert=ordnungszahlIndex;
    }
    if(eintragPunkt<0)return 0;for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<deklariertMethodeAnzahl&&!istUngültig;ordnungszahlIndex++)methodeÜbersetzen(ordnungszahlIndex);
    wertAusgeben("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<deklariertFeldAnzahl;ordnungszahlIndex++)if(feldKonstante[ordnungszahlIndex]){
        unsigned zeichenKode=feldKonstante[ordnungszahlIndex];if(zeichenKode>=konstanteVorratsbereich)return 0;
        if(kennzeichenlisteListe[zeichenKode]==3)wertAusgeben("fields[%u]=%uU;",ordnungszahlIndex,ersterWert[zeichenKode]);else if(kennzeichenlisteListe[zeichenKode]==8)wertAusgeben("fields[%u]=(W)k%u;",ordnungszahlIndex,zeichenKode);else return 0;
    }
    if(anfänglichWert>=0)wertAusgeben("m%d();",anfänglichWert);wertAusgeben("m%d((W)a);return 0;}\n",eintragPunkt);
    return istUngültig?0:Text;
}
