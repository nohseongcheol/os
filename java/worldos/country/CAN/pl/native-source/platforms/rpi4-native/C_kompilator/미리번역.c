#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "pakiet.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char dane[16384];static unsigned długość_WARTOŚĆ,bieżący_stanowisko;static int systemy_informacyjne_nieważny;
static unsigned Tagi_Lista[512],첫째값[512],SEKUNDA_WARTOŚĆ[512],stała_pula,bieżący_Klasa;
static char tekst[65536];static unsigned Rozmiar_tekstu;
typedef struct {unsigned konfiguracja_BITS,Nazwa,deskryptor_dane,instrukcja_SEKWENCJA,Rozmiar,지역변수들,pamięć_stosu;} metoda_wpis;
static metoda_wpis 메소드목록[64];static unsigned 메소드개수;
static unsigned nazwa_pola[64],pole_deskryptor[64],pole_stała[64],필드개수;
static unsigned WYCINEK_WARTOŚĆ(unsigned towar_ILE_LICZB){if(bieżący_stanowisko>długość_WARTOŚĆ||towar_ILE_LICZB>długość_WARTOŚĆ-bieżący_stanowisko){systemy_informacyjne_nieważny=1;return 0;}unsigned dane_stanowisko=bieżący_stanowisko;bieżący_stanowisko+=towar_ILE_LICZB;return dane_stanowisko;}
static unsigned bajt_dane(void){unsigned dane_stanowisko=WYCINEK_WARTOŚĆ(1);return systemy_informacyjne_nieważny?0:dane[dane_stanowisko];}
static unsigned 절반값(void){unsigned współrzędna_X=bajt_dane();return współrzędna_X<<8|bajt_dane();}
static uint32_t 가득참(void){uint32_t współrzędna_X=절반값();return współrzędna_X<<16|절반값();}
static int UNICODE_WARTOŚĆ(unsigned 순번,const char*ciąg_dane){return 순번>0&&순번<stała_pula&&Tagi_Lista[순번]==1&&strlen(ciąg_dane)==SEKUNDA_WARTOŚĆ[순번]&&!memcmp(dane+첫째값[순번],ciąg_dane,SEKUNDA_WARTOŚĆ[순번]);}
static int 같음(unsigned współrzędna_X,unsigned Y_współrzędna){return współrzędna_X>0&&współrzędna_X<stała_pula&&Y_współrzędna>0&&Y_współrzędna<stała_pula&&Tagi_Lista[współrzędna_X]==1&&Tagi_Lista[Y_współrzędna]==1&&SEKUNDA_WARTOŚĆ[współrzędna_X]==SEKUNDA_WARTOŚĆ[Y_współrzędna]&&!memcmp(dane+첫째값[współrzędna_X],dane+첫째값[Y_współrzędna],SEKUNDA_WARTOŚĆ[współrzędna_X]);}
static void 내보내기(const char*Plik_wpis,...){if(systemy_informacyjne_nieważny)return;va_list argument_TABLICA;va_start(argument_TABLICA,Plik_wpis);int towar_ILE_LICZB=vsnprintf(tekst+Rozmiar_tekstu,sizeof(tekst)-Rozmiar_tekstu,Plik_wpis,argument_TABLICA);va_end(argument_TABLICA);if(towar_ILE_LICZB<0||(unsigned)towar_ILE_LICZB>=sizeof(tekst)-Rozmiar_tekstu){systemy_informacyjne_nieważny=1;return;}Rozmiar_tekstu+=towar_ILE_LICZB;}
static int deskryptor_wpis(unsigned identyfikator_WARTOŚĆ,int*WYNIK){
    if(identyfikator_WARTOŚĆ<1||identyfikator_WARTOŚĆ>=stała_pula||Tagi_Lista[identyfikator_WARTOŚĆ]!=1)return -1;unsigned dane_stanowisko=첫째값[identyfikator_WARTOŚĆ],Koniec_przesunąć=dane_stanowisko+SEKUNDA_WARTOŚĆ[identyfikator_WARTOŚĆ];if(dane_stanowisko>=Koniec_przesunąć||dane[dane_stanowisko++]!='(')return -1;int wpis_ILE_LICZB=0;
    while(dane_stanowisko<Koniec_przesunąć&&dane[dane_stanowisko]!=')'){
        unsigned kod_znaku=dane[dane_stanowisko++];while(kod_znaku=='['&&dane_stanowisko<Koniec_przesunąć)kod_znaku=dane[dane_stanowisko++];
        if(kod_znaku=='L'){while(dane_stanowisko<Koniec_przesunąć&&dane[dane_stanowisko]!=';')dane_stanowisko++;if(dane_stanowisko==Koniec_przesunąć)return -1;dane_stanowisko++;}
        else if(kod_znaku!='I'&&kod_znaku!='Z'&&kod_znaku!='B'&&kod_znaku!='C'&&kod_znaku!='S')return -1;
        if(++wpis_ILE_LICZB>16)return -1;
    }
    if(dane_stanowisko+1>=Koniec_przesunąć||dane[dane_stanowisko++]!=')')return -1;*WYNIK=dane[dane_stanowisko]=='V'?0:1;
    if(dane[dane_stanowisko]=='J'||dane[dane_stanowisko]=='D'||dane[dane_stanowisko]=='F')return -1;return wpis_ILE_LICZB;
}
static void atrybuty(void){unsigned towar_ILE_LICZB=절반값();for(unsigned 순번=0;순번<towar_ILE_LICZB&&!systemy_informacyjne_nieważny;순번++){절반값();unsigned Rozmiar=가득참();WYCINEK_WARTOŚĆ(Rozmiar);}}
static int analizować_wejście(void){
    if(가득참()!=0xcafebabe)return -1;unsigned wersja_pomocnicza=절반값(),numer_wersji=절반값();if(wersja_pomocnicza||numer_wersji<45||numer_wersji>52)return -1;
    stała_pula=절반값();if(stała_pula<1||stała_pula>512)return -1;
    for(unsigned 순번=1;순번<stała_pula&&!systemy_informacyjne_nieważny;순번++){
        Tagi_Lista[순번]=bajt_dane();switch(Tagi_Lista[순번]){
        case 1:SEKUNDA_WARTOŚĆ[순번]=절반값();첫째값[순번]=WYCINEK_WARTOŚĆ(SEKUNDA_WARTOŚĆ[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:WYCINEK_WARTOŚĆ(8);if(++순번>=stała_pula)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SEKUNDA_WARTOŚĆ[순번]=절반값();break;
        case 15:첫째값[순번]=bajt_dane();SEKUNDA_WARTOŚĆ[순번]=절반값();break;default:return -1;
        }
    }
    절반값();bieżący_Klasa=절반값();절반값();if(bieżący_Klasa<1||bieżący_Klasa>=stała_pula||Tagi_Lista[bieżący_Klasa]!=7||첫째값[bieżący_Klasa]<1||첫째값[bieżący_Klasa]>=stała_pula||Tagi_Lista[첫째값[bieżący_Klasa]]!=1)return -1;unsigned 인터페이스목록=절반값();WYCINEK_WARTOŚĆ(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!systemy_informacyjne_nieważny;순번++){
        unsigned konfiguracja_BITS=절반값();nazwa_pola[순번]=절반값();pole_deskryptor[순번]=절반값();
        if(!(konfiguracja_BITS&8))return -1;
        unsigned wpis_ILE_LICZB=절반값();for(unsigned 안쪽순번=0;안쪽순번<wpis_ILE_LICZB&&!systemy_informacyjne_nieważny;안쪽순번++){
            unsigned Nazwa=절반값(),Rozmiar=가득참();
            if(UNICODE_WARTOŚĆ(Nazwa,"ConstantValue")){if(Rozmiar!=2)return -1;pole_stała[순번]=절반값();}
            else WYCINEK_WARTOŚĆ(Rozmiar);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!systemy_informacyjne_nieważny;순번++){
        metoda_wpis*grupa_zmienić_rozmiar=메소드목록+순번;grupa_zmienić_rozmiar->konfiguracja_BITS=절반값();grupa_zmienić_rozmiar->Nazwa=절반값();grupa_zmienić_rozmiar->deskryptor_dane=절반값();unsigned wpis_ILE_LICZB=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<wpis_ILE_LICZB&&!systemy_informacyjne_nieważny;안쪽순번++){
            unsigned Nazwa=절반값(),Rozmiar=가득참(),Uruchom_2=bieżący_stanowisko;
            if(Rozmiar>długość_WARTOŚĆ-bieżący_stanowisko)return -1;
            if(UNICODE_WARTOŚĆ(Nazwa,"Code")){
                grupa_zmienić_rozmiar->pamięć_stosu=절반값();grupa_zmienić_rozmiar->지역변수들=절반값();grupa_zmienić_rozmiar->Rozmiar=가득참();grupa_zmienić_rozmiar->instrukcja_SEKWENCJA=WYCINEK_WARTOŚĆ(grupa_zmienić_rozmiar->Rozmiar);
                if(grupa_zmienić_rozmiar->pamięć_stosu>128||grupa_zmienić_rozmiar->지역변수들>128||grupa_zmienić_rozmiar->Rozmiar>8192||절반값())return -1;atrybuty();
            }else WYCINEK_WARTOŚĆ(Rozmiar);
            if(bieżący_stanowisko!=Uruchom_2+Rozmiar)return -1;
        }
        if(!UNICODE_WARTOŚĆ(grupa_zmienić_rozmiar->Nazwa,"<init>")&&(!(grupa_zmienić_rozmiar->konfiguracja_BITS&8)||(grupa_zmienić_rozmiar->konfiguracja_BITS&(0x100|0x20))||!grupa_zmienić_rozmiar->Rozmiar))return -1;
    }
    atrybuty();return systemy_informacyjne_nieważny||bieżący_stanowisko!=długość_WARTOŚĆ?-1:0;
}
static void stała_WARTOŚĆ(unsigned identyfikator_WARTOŚĆ){
    if(!identyfikator_WARTOŚĆ||identyfikator_WARTOŚĆ>=stała_pula){systemy_informacyjne_nieważny=1;return;}
    if(Tagi_Lista[identyfikator_WARTOŚĆ]==3)내보내기("P(%uU);",첫째값[identyfikator_WARTOŚĆ]);
    else if(Tagi_Lista[identyfikator_WARTOŚĆ]==8)내보내기("P((W)k%u);",identyfikator_WARTOŚĆ);else systemy_informacyjne_nieważny=1;
}
static void 호출(unsigned identyfikator_WARTOŚĆ,int wirtualny_Połącz){
    if(identyfikator_WARTOŚĆ<1||identyfikator_WARTOŚĆ>=stała_pula||(Tagi_Lista[identyfikator_WARTOŚĆ]!=10&&Tagi_Lista[identyfikator_WARTOŚĆ]!=11)||첫째값[identyfikator_WARTOŚĆ]<1||첫째값[identyfikator_WARTOŚĆ]>=stała_pula||Tagi_Lista[첫째값[identyfikator_WARTOŚĆ]]!=7||SEKUNDA_WARTOŚĆ[identyfikator_WARTOŚĆ]<1||SEKUNDA_WARTOŚĆ[identyfikator_WARTOŚĆ]>=stała_pula||Tagi_Lista[SEKUNDA_WARTOŚĆ[identyfikator_WARTOŚĆ]]!=12){systemy_informacyjne_nieważny=1;return;}
    unsigned właściciel_obiekt=첫째값[첫째값[identyfikator_WARTOŚĆ]],Nazwa=첫째값[SEKUNDA_WARTOŚĆ[identyfikator_WARTOŚĆ]],deskryptor_dane=SEKUNDA_WARTOŚĆ[SEKUNDA_WARTOŚĆ[identyfikator_WARTOŚĆ]];int WYNIK=0,towar_ILE_LICZB=deskryptor_wpis(deskryptor_dane,&WYNIK);if(towar_ILE_LICZB<0){systemy_informacyjne_nieważny=1;return;}
    for(int 순번=towar_ILE_LICZB;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(wirtualny_Połącz)내보내기("Q();");
    if(!wirtualny_Połącz&&같음(właściciel_obiekt,첫째값[bieżący_Klasa])){
        unsigned grupa_zmienić_rozmiar=0;for(;grupa_zmienić_rozmiar<메소드개수;grupa_zmienić_rozmiar++)if(같음(Nazwa,메소드목록[grupa_zmienić_rozmiar].Nazwa)&&같음(deskryptor_dane,메소드목록[grupa_zmienić_rozmiar].deskryptor_dane))break;
        if(grupa_zmienić_rozmiar==메소드개수||!(메소드목록[grupa_zmienić_rozmiar].konfiguracja_BITS&8)){systemy_informacyjne_nieważny=1;return;}
        if(WYNIK)내보내기("P(");내보내기("m%u(",grupa_zmienić_rozmiar);for(int 순번=0;순번<towar_ILE_LICZB;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(WYNIK?"));":" );");return;
    }
    if((wirtualny_Połącz&&UNICODE_WARTOŚĆ(właściciel_obiekt,"java/io/PrintStream")&& (UNICODE_WARTOŚĆ(Nazwa,"print")||UNICODE_WARTOŚĆ(Nazwa,"println")))||(!wirtualny_Połącz&&UNICODE_WARTOŚĆ(właściciel_obiekt,"polski/własny/pozycja_wyjścia"))){
        if(UNICODE_WARTOŚĆ(deskryptor_dane,"(I)V")&&(UNICODE_WARTOŚĆ(Nazwa,"print")||UNICODE_WARTOŚĆ(Nazwa,"println")||UNICODE_WARTOŚĆ(Nazwa,"zapis_identyfikator"))){내보내기("jprint(x[0],1,%d);",UNICODE_WARTOŚĆ(Nazwa,"print")?0:1);return;}
        if(UNICODE_WARTOŚĆ(deskryptor_dane,"(Ljava/lang/String;)V")&&(UNICODE_WARTOŚĆ(Nazwa,"print")||UNICODE_WARTOŚĆ(Nazwa,"println")||UNICODE_WARTOŚĆ(Nazwa,"Zapis")||UNICODE_WARTOŚĆ(Nazwa,"zapis_linia"))){내보내기("jprint(x[0],0,%d);",UNICODE_WARTOŚĆ(Nazwa,"print")||UNICODE_WARTOŚĆ(Nazwa,"Zapis")?0:1);return;}
        if(UNICODE_WARTOŚĆ(deskryptor_dane,"()V")&&UNICODE_WARTOŚĆ(Nazwa,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!wirtualny_Połącz&&UNICODE_WARTOŚĆ(właściciel_obiekt,"polski/własny/nazwa_pliku")){
        if(UNICODE_WARTOŚĆ(Nazwa,"Zapis")&&UNICODE_WARTOŚĆ(deskryptor_dane,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_WARTOŚĆ(Nazwa,"Odczyt")&&UNICODE_WARTOŚĆ(deskryptor_dane,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    systemy_informacyjne_nieważny=1;
}
static void kompilować_metoda(unsigned WYSZUKAJ_INDEKS){
    metoda_wpis*grupa_zmienić_rozmiar=메소드목록+WYSZUKAJ_INDEKS;if(UNICODE_WARTOŚĆ(grupa_zmienić_rozmiar->Nazwa,"<init>"))return;int WYNIK,towar_ILE_LICZB=deskryptor_wpis(grupa_zmienić_rozmiar->deskryptor_dane,&WYNIK);if(towar_ILE_LICZB<0){systemy_informacyjne_nieważny=1;return;}
    내보내기("static W m%u(",WYSZUKAJ_INDEKS);for(int 순번=0;순번<towar_ILE_LICZB;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!towar_ILE_LICZB)내보내기("void");
    if((unsigned)towar_ILE_LICZB>grupa_zmienić_rozmiar->지역변수들){systemy_informacyjne_nieważny=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",grupa_zmienić_rozmiar->지역변수들?grupa_zmienić_rozmiar->지역변수들:1);for(int 순번=0;순번<towar_ILE_LICZB;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=długość_WARTOŚĆ;długość_WARTOŚĆ=grupa_zmienić_rozmiar->instrukcja_SEKWENCJA+grupa_zmienić_rozmiar->Rozmiar;bieżący_stanowisko=grupa_zmienić_rozmiar->instrukcja_SEKWENCJA;
    while(bieżący_stanowisko<długość_WARTOŚĆ&&!systemy_informacyjne_nieważny){unsigned polecenie_stanowisko=bieżący_stanowisko-grupa_zmienić_rozmiar->instrukcja_SEKWENCJA,zabieg_WARTOŚĆ=bajt_dane();내보내기("L%u:;",polecenie_stanowisko);
        if(zabieg_WARTOŚĆ==0){}
        else if(zabieg_WARTOŚĆ==1)내보내기("P(0);");
        else if(zabieg_WARTOŚĆ>=2&&zabieg_WARTOŚĆ<=8)내보내기("P(%uU);",zabieg_WARTOŚĆ-3);
        else if(zabieg_WARTOŚĆ==16){int WARTOŚĆ=(int8_t)bajt_dane();내보내기("P(%uU);",(unsigned)WARTOŚĆ);}
        else if(zabieg_WARTOŚĆ==17){int WARTOŚĆ=(int16_t)절반값();내보내기("P(%uU);",(unsigned)WARTOŚĆ);}
        else if(zabieg_WARTOŚĆ==18||zabieg_WARTOŚĆ==19)stała_WARTOŚĆ(zabieg_WARTOŚĆ==18?bajt_dane():절반값());
        else if(zabieg_WARTOŚĆ==21||zabieg_WARTOŚĆ==25){unsigned 순번=bajt_dane();if(순번>=grupa_zmienić_rozmiar->지역변수들)systemy_informacyjne_nieważny=1;내보내기("P(v[%u]);",순번);}
        else if((zabieg_WARTOŚĆ>=26&&zabieg_WARTOŚĆ<=29)||(zabieg_WARTOŚĆ>=42&&zabieg_WARTOŚĆ<=45)){unsigned 순번=zabieg_WARTOŚĆ>=42?zabieg_WARTOŚĆ-42:zabieg_WARTOŚĆ-26;if(순번>=grupa_zmienić_rozmiar->지역변수들)systemy_informacyjne_nieważny=1;내보내기("P(v[%u]);",순번);}
        else if(zabieg_WARTOŚĆ==54||zabieg_WARTOŚĆ==58){unsigned 순번=bajt_dane();if(순번>=grupa_zmienić_rozmiar->지역변수들)systemy_informacyjne_nieważny=1;내보내기("v[%u]=Q();",순번);}
        else if((zabieg_WARTOŚĆ>=59&&zabieg_WARTOŚĆ<=62)||(zabieg_WARTOŚĆ>=75&&zabieg_WARTOŚĆ<=78)){unsigned 순번=zabieg_WARTOŚĆ>=75?zabieg_WARTOŚĆ-75:zabieg_WARTOŚĆ-59;if(순번>=grupa_zmienić_rozmiar->지역변수들)systemy_informacyjne_nieważny=1;내보내기("v[%u]=Q();",순번);}
        else if(zabieg_WARTOŚĆ==46||zabieg_WARTOŚĆ==50||zabieg_WARTOŚĆ==51||zabieg_WARTOŚĆ==52||zabieg_WARTOŚĆ==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(zabieg_WARTOŚĆ==79||zabieg_WARTOŚĆ==83||zabieg_WARTOŚĆ==84||zabieg_WARTOŚĆ==85||zabieg_WARTOŚĆ==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",zabieg_WARTOŚĆ==84?"(unsigned)(signed char)q":zabieg_WARTOŚĆ==85?"(unsigned short)q":zabieg_WARTOŚĆ==86?"(unsigned)(short)q":"q");
        else if(zabieg_WARTOŚĆ==87)내보내기("Q();");
        else if(zabieg_WARTOŚĆ==89)내보내기("q=Q();P(q);P(q);");
        else if(zabieg_WARTOŚĆ==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(zabieg_WARTOŚĆ==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(zabieg_WARTOŚĆ==96||zabieg_WARTOŚĆ==100||zabieg_WARTOŚĆ==104||zabieg_WARTOŚĆ==120||zabieg_WARTOŚĆ==124||zabieg_WARTOŚĆ==126||zabieg_WARTOŚĆ==128||zabieg_WARTOŚĆ==130){const char*Encoding_WARTOŚĆ=zabieg_WARTOŚĆ==96?"+":zabieg_WARTOŚĆ==100?"-":zabieg_WARTOŚĆ==104?"*":zabieg_WARTOŚĆ==120?"<<":zabieg_WARTOŚĆ==124?">>":zabieg_WARTOŚĆ==126?"&":zabieg_WARTOŚĆ==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",Encoding_WARTOŚĆ,zabieg_WARTOŚĆ==120||zabieg_WARTOŚĆ==124?"%32":"");}
        else if(zabieg_WARTOŚĆ==108||zabieg_WARTOŚĆ==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",zabieg_WARTOŚĆ==112);
        else if(zabieg_WARTOŚĆ==116)내보내기("P(0U-(unsigned)Q());");
        else if(zabieg_WARTOŚĆ==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(zabieg_WARTOŚĆ==132){unsigned 순번=bajt_dane();int 차이=(int8_t)bajt_dane();if(순번>=grupa_zmienić_rozmiar->지역변수들)systemy_informacyjne_nieważny=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(zabieg_WARTOŚĆ>=145&&zabieg_WARTOŚĆ<=147)내보내기("P((unsigned)(%s)Q());",zabieg_WARTOŚĆ==145?"signed char":zabieg_WARTOŚĆ==146?"unsigned short":"short");
        else if(zabieg_WARTOŚĆ>=153&&zabieg_WARTOŚĆ<=166){int wartość_docelowa=(int)polecenie_stanowisko+(int16_t)절반값();const char*Porównanie_WARTOŚĆ[]={"==","!=","<",">=",">","<="};if(wartość_docelowa<0||wartość_docelowa>=(int)grupa_zmienić_rozmiar->Rozmiar){systemy_informacyjne_nieważny=1;break;}if(zabieg_WARTOŚĆ<159)내보내기("if((int)Q()%s0)goto L%d;",Porównanie_WARTOŚĆ[zabieg_WARTOŚĆ-153],wartość_docelowa);else if(zabieg_WARTOŚĆ<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Porównanie_WARTOŚĆ[zabieg_WARTOŚĆ-159],wartość_docelowa);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",zabieg_WARTOŚĆ==165?"==":"!=",wartość_docelowa);}
        else if(zabieg_WARTOŚĆ==167){int wartość_docelowa=(int)polecenie_stanowisko+(int16_t)절반값();if(wartość_docelowa<0||wartość_docelowa>=(int)grupa_zmienić_rozmiar->Rozmiar)systemy_informacyjne_nieważny=1;내보내기("goto L%d;",wartość_docelowa);}
        else if(zabieg_WARTOŚĆ==172||zabieg_WARTOŚĆ==176)내보내기("return Q();");else if(zabieg_WARTOŚĆ==177)내보내기("return 0;");
        else if(zabieg_WARTOŚĆ==178||zabieg_WARTOŚĆ==179){unsigned identyfikator_WARTOŚĆ=절반값();if(identyfikator_WARTOŚĆ<1||identyfikator_WARTOŚĆ>=stała_pula||Tagi_Lista[identyfikator_WARTOŚĆ]!=9||첫째값[identyfikator_WARTOŚĆ]>=stała_pula||SEKUNDA_WARTOŚĆ[identyfikator_WARTOŚĆ]>=stała_pula||Tagi_Lista[첫째값[identyfikator_WARTOŚĆ]]!=7||Tagi_Lista[SEKUNDA_WARTOŚĆ[identyfikator_WARTOŚĆ]]!=12){systemy_informacyjne_nieważny=1;break;}unsigned właściciel_obiekt=첫째값[첫째값[identyfikator_WARTOŚĆ]],Nazwa=첫째값[SEKUNDA_WARTOŚĆ[identyfikator_WARTOŚĆ]],deskryptor_dane=SEKUNDA_WARTOŚĆ[SEKUNDA_WARTOŚĆ[identyfikator_WARTOŚĆ]];
            if(zabieg_WARTOŚĆ==178&&UNICODE_WARTOŚĆ(właściciel_obiekt,"java/lang/System")&&UNICODE_WARTOŚĆ(Nazwa,"out")&&UNICODE_WARTOŚĆ(deskryptor_dane,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Plik_wpis=0;while(Plik_wpis<필드개수&&(!같음(Nazwa,nazwa_pola[Plik_wpis])||!같음(deskryptor_dane,pole_deskryptor[Plik_wpis])))Plik_wpis++;if(!같음(właściciel_obiekt,첫째값[bieżący_Klasa])||Plik_wpis==필드개수){systemy_informacyjne_nieważny=1;break;}내보내기(zabieg_WARTOŚĆ==178?"P(fields[%u]);":"fields[%u]=Q();",Plik_wpis);}}
        else if(zabieg_WARTOŚĆ==182||zabieg_WARTOŚĆ==184)호출(절반값(),zabieg_WARTOŚĆ==182);
        else if(zabieg_WARTOŚĆ==188){unsigned TYP_obszar=bajt_dane();if(TYP_obszar!=4&&TYP_obszar!=5&&TYP_obszar!=8&&TYP_obszar!=9&&TYP_obszar!=10)systemy_informacyjne_nieważny=1;내보내기("P(jarray((int)Q()));");}
        else if(zabieg_WARTOŚĆ==190)내보내기("P(jlength(Q()));");
        else if(zabieg_WARTOŚĆ==198||zabieg_WARTOŚĆ==199){int wartość_docelowa=(int)polecenie_stanowisko+(int16_t)절반값();if(wartość_docelowa<0||wartość_docelowa>=(int)grupa_zmienić_rozmiar->Rozmiar)systemy_informacyjne_nieważny=1;내보내기("if(Q()%s0)goto L%d;",zabieg_WARTOŚĆ==198?"==":"!=",wartość_docelowa);}
        else systemy_informacyjne_nieważny=1;
        if(systemy_informacyjne_nieważny)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",WYSZUKAJ_INDEKS,zabieg_WARTOŚĆ,polecenie_stanowisko);
        내보내기("\n");
    }
    długość_WARTOŚĆ=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned ciąg_lekcja(unsigned *dane_stanowisko,unsigned Koniec_przesunąć){
    if(*dane_stanowisko>=Koniec_przesunąć){systemy_informacyjne_nieważny=1;return 0;}unsigned kod_znaku=dane[(*dane_stanowisko)++];
    if(kod_znaku<128)return kod_znaku;
    unsigned towar_ILE_LICZB=kod_znaku>=0xc0&&kod_znaku<=0xdf?1:kod_znaku>=0xe0&&kod_znaku<=0xef?2:3;
    if(towar_ILE_LICZB==3||towar_ILE_LICZB>Koniec_przesunąć-*dane_stanowisko){systemy_informacyjne_nieważny=1;return 0;}unsigned WARTOŚĆ=kod_znaku&((1u<<(6-towar_ILE_LICZB))-1);
    for(unsigned 순번=0;순번<towar_ILE_LICZB;순번++){unsigned Dalej_towar=dane[(*dane_stanowisko)++];if((Dalej_towar&0xc0)!=0x80)systemy_informacyjne_nieważny=1;WARTOŚĆ=WARTOŚĆ<<6|(Dalej_towar&63);}
    if((towar_ILE_LICZB==1&&WARTOŚĆ<128&&WARTOŚĆ!=0)||(towar_ILE_LICZB==2&&WARTOŚĆ<2048))systemy_informacyjne_nieważny=1;return WARTOŚĆ;
}
static void ciąg_stała(unsigned identyfikator_WARTOŚĆ){
    unsigned 부호없는값=첫째값[identyfikator_WARTOŚĆ];if(부호없는값<1||부호없는값>=stała_pula||Tagi_Lista[부호없는값]!=1){systemy_informacyjne_nieważny=1;return;}내보내기("static const unsigned char k%u[]={",identyfikator_WARTOŚĆ);
    unsigned dane_stanowisko=첫째값[부호없는값],Koniec_przesunąć=dane_stanowisko+SEKUNDA_WARTOŚĆ[부호없는값];
    while(dane_stanowisko<Koniec_przesunąć&&!systemy_informacyjne_nieważny){unsigned kod_znaku=ciąg_lekcja(&dane_stanowisko,Koniec_przesunąć);
        if(kod_znaku>=0xd800&&kod_znaku<=0xdbff){unsigned 낮은부분=ciąg_lekcja(&dane_stanowisko,Koniec_przesunąć);if(낮은부분<0xdc00||낮은부분>0xdfff){systemy_informacyjne_nieważny=1;break;}kod_znaku=0x10000+((kod_znaku-0xd800)<<10)+낮은부분-0xdc00;}
        else if(kod_znaku>=0xdc00&&kod_znaku<=0xdfff){systemy_informacyjne_nieważny=1;break;}
        if(!kod_znaku){printf("jaot: embedded NUL string needs JVM mode\n");systemy_informacyjne_nieważny=1;break;}
        if(kod_znaku<128)내보내기("%u,",kod_znaku);
        else{unsigned towar_ILE_LICZB=kod_znaku<2048?2:kod_znaku<65536?3:4;내보내기("%u,",(towar_ILE_LICZB==2?0xc0:towar_ILE_LICZB==3?0xe0:0xf0)|(kod_znaku>>(6*(towar_ILE_LICZB-1))));for(unsigned 순번=towar_ILE_LICZB-1;순번;순번--)내보내기("%u,",0x80|((kod_znaku>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Nazwa){
    size_t towar_ILE_LICZB=strlen(Nazwa);
    if(towar_ILE_LICZB>4&&!strcmp(Nazwa+towar_ILE_LICZB-4,".jar")){
        if(꾸러미열기(Nazwa)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char ścieżka_2[256];const char*wpis_metoda=꾸러미진입클래스();towar_ILE_LICZB=strlen(wpis_metoda);if(towar_ILE_LICZB+6>=sizeof(ścieżka_2))return 0;
        for(unsigned 순번=0;순번<towar_ILE_LICZB;순번++)ścieżka_2[순번]=wpis_metoda[순번]=='.'?'/':wpis_metoda[순번];strcpy(ścieżka_2+towar_ILE_LICZB,".class");int wpis_ILE_LICZB=꾸러미읽기(ścieżka_2,dane,sizeof(dane));if(wpis_ILE_LICZB<0)return 0;długość_WARTOŚĆ=wpis_ILE_LICZB;
    }else{intptr_t dojście_do_pliku=사용자호출(3,(uintptr_t)Nazwa,0,0,0,0,0);if(dojście_do_pliku<0)return 0;intptr_t wpis_ILE_LICZB=사용자호출(9,dojście_do_pliku,0,0,0,0,0);if(wpis_ILE_LICZB<0||wpis_ILE_LICZB>sizeof(dane)){사용자호출(4,dojście_do_pliku,0,0,0,0,0);return 0;}intptr_t KWOTA_WYKUP_ILE_LICZB=사용자호출(2,dojście_do_pliku,(uintptr_t)dane,wpis_ILE_LICZB,0,0,0);사용자호출(4,dojście_do_pliku,0,0,0,0,0);if(KWOTA_WYKUP_ILE_LICZB!=wpis_ILE_LICZB)return 0;długość_WARTOŚĆ=wpis_ILE_LICZB;}
    if(analizować_wejście()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<stała_pula&&!systemy_informacyjne_nieważny;순번++)if(Tagi_Lista[순번]==8)ciąg_stała(순번);
    if(systemy_informacyjne_nieważny)return 0;
    int punkt_wejścia=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_WARTOŚĆ(메소드목록[순번].Nazwa,"<init>")){
        int WYNIK,wpis_ILE_LICZB=deskryptor_wpis(메소드목록[순번].deskryptor_dane,&WYNIK);if(wpis_ILE_LICZB<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<wpis_ILE_LICZB;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!wpis_ILE_LICZB)내보내기("void");내보내기(");\n");
        if(UNICODE_WARTOŚĆ(메소드목록[순번].Nazwa,"main")&&UNICODE_WARTOŚĆ(메소드목록[순번].deskryptor_dane,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfiguracja_BITS&9)==9)punkt_wejścia=순번;
        if(UNICODE_WARTOŚĆ(메소드목록[순번].Nazwa,"<clinit>"))초기값=순번;
    }
    if(punkt_wejścia<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!systemy_informacyjne_nieważny;순번++)kompilować_metoda(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(pole_stała[순번]){
        unsigned kod_znaku=pole_stała[순번];if(kod_znaku>=stała_pula)return 0;
        if(Tagi_Lista[kod_znaku]==3)내보내기("fields[%u]=%uU;",순번,첫째값[kod_znaku]);else if(Tagi_Lista[kod_znaku]==8)내보내기("fields[%u]=(W)k%u;",순번,kod_znaku);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",punkt_wejścia);
    return systemy_informacyjne_nieważny?0:tekst;
}
