#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "sveženj.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char podatki[16384];static unsigned 길이,sprotno_položaj;static int informacijska_tehnologija_neveljaven;
static unsigned Zvrsti_Seznam[512],첫째값[512],SECOND_VALUE[512],konstanta_seštevek,sprotno_Razred;
static char Besedilo[65536];static unsigned velikost_besedila;
typedef struct {unsigned konfiguracija_storitev_Background_Intelligent_Transfer_Service,Ime,서술값,navodilo_SEQUENCE,Velikost,지역변수들,Sklad_Senzor_prostora;} metoda_vnos;
static metoda_vnos 메소드목록[64];static unsigned 메소드개수;
static unsigned ime_polja[64],필드서술[64],polje_konstanta[64],필드개수;
static unsigned TAKE_VALUE(unsigned element_COUNT){if(sprotno_položaj>길이||element_COUNT>길이-sprotno_položaj){informacijska_tehnologija_neveljaven=1;return 0;}unsigned podatki_položaj=sprotno_položaj;sprotno_položaj+=element_COUNT;return podatki_položaj;}
static unsigned bajt_podatki(void){unsigned podatki_položaj=TAKE_VALUE(1);return informacijska_tehnologija_neveljaven?0:podatki[podatki_položaj];}
static unsigned 절반값(void){unsigned koordinata_x=bajt_podatki();return koordinata_x<<8|bajt_podatki();}
static uint32_t 가득참(void){uint32_t koordinata_x=절반값();return koordinata_x<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*niz_podatki){return 순번>0&&순번<konstanta_seštevek&&Zvrsti_Seznam[순번]==1&&strlen(niz_podatki)==SECOND_VALUE[순번]&&!memcmp(podatki+첫째값[순번],niz_podatki,SECOND_VALUE[순번]);}
static int 같음(unsigned koordinata_x,unsigned 세로좌표){return koordinata_x>0&&koordinata_x<konstanta_seštevek&&세로좌표>0&&세로좌표<konstanta_seštevek&&Zvrsti_Seznam[koordinata_x]==1&&Zvrsti_Seznam[세로좌표]==1&&SECOND_VALUE[koordinata_x]==SECOND_VALUE[세로좌표]&&!memcmp(podatki+첫째값[koordinata_x],podatki+첫째값[세로좌표],SECOND_VALUE[koordinata_x]);}
static void 내보내기(const char*Datoteka_vnos,...){if(informacijska_tehnologija_neveljaven)return;va_list argument_ARRAY;va_start(argument_ARRAY,Datoteka_vnos);int element_COUNT=vsnprintf(Besedilo+velikost_besedila,sizeof(Besedilo)-velikost_besedila,Datoteka_vnos,argument_ARRAY);va_end(argument_ARRAY);if(element_COUNT<0||(unsigned)element_COUNT>=sizeof(Besedilo)-velikost_besedila){informacijska_tehnologija_neveljaven=1;return;}velikost_besedila+=element_COUNT;}
static int 서술자(unsigned identifikator_VALUE,int*REZULTAT){
    if(identifikator_VALUE<1||identifikator_VALUE>=konstanta_seštevek||Zvrsti_Seznam[identifikator_VALUE]!=1)return -1;unsigned podatki_položaj=첫째값[identifikator_VALUE],končati_klic_odmik=podatki_položaj+SECOND_VALUE[identifikator_VALUE];if(podatki_položaj>=končati_klic_odmik||podatki[podatki_položaj++]!='(')return -1;int vnos_COUNT=0;
    while(podatki_položaj<končati_klic_odmik&&podatki[podatki_položaj]!=')'){
        unsigned koda_znaka=podatki[podatki_položaj++];while(koda_znaka=='['&&podatki_položaj<končati_klic_odmik)koda_znaka=podatki[podatki_položaj++];
        if(koda_znaka=='L'){while(podatki_položaj<končati_klic_odmik&&podatki[podatki_položaj]!=';')podatki_položaj++;if(podatki_položaj==končati_klic_odmik)return -1;podatki_položaj++;}
        else if(koda_znaka!='I'&&koda_znaka!='Z'&&koda_znaka!='B'&&koda_znaka!='C'&&koda_znaka!='S')return -1;
        if(++vnos_COUNT>16)return -1;
    }
    if(podatki_položaj+1>=končati_klic_odmik||podatki[podatki_položaj++]!=')')return -1;*REZULTAT=podatki[podatki_položaj]=='V'?0:1;
    if(podatki[podatki_položaj]=='J'||podatki[podatki_položaj]=='D'||podatki[podatki_položaj]=='F')return -1;return vnos_COUNT;
}
static void lastnosti(void){unsigned element_COUNT=절반값();for(unsigned 순번=0;순번<element_COUNT&&!informacijska_tehnologija_neveljaven;순번++){절반값();unsigned Velikost=가득참();TAKE_VALUE(Velikost);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned podrazličica=절반값(),številka_različice=절반값();if(podrazličica||številka_različice<45||številka_različice>52)return -1;
    konstanta_seštevek=절반값();if(konstanta_seštevek<1||konstanta_seštevek>512)return -1;
    for(unsigned 순번=1;순번<konstanta_seštevek&&!informacijska_tehnologija_neveljaven;순번++){
        Zvrsti_Seznam[순번]=bajt_podatki();switch(Zvrsti_Seznam[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=konstanta_seštevek)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=bajt_podatki();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();sprotno_Razred=절반값();절반값();if(sprotno_Razred<1||sprotno_Razred>=konstanta_seštevek||Zvrsti_Seznam[sprotno_Razred]!=7||첫째값[sprotno_Razred]<1||첫째값[sprotno_Razred]>=konstanta_seštevek||Zvrsti_Seznam[첫째값[sprotno_Razred]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!informacijska_tehnologija_neveljaven;순번++){
        unsigned konfiguracija_storitev_Background_Intelligent_Transfer_Service=절반값();ime_polja[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfiguracija_storitev_Background_Intelligent_Transfer_Service&8))return -1;
        unsigned vnos_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<vnos_COUNT&&!informacijska_tehnologija_neveljaven;안쪽순번++){
            unsigned Ime=절반값(),Velikost=가득참();
            if(UNICODE_VALUE(Ime,"ConstantValue")){if(Velikost!=2)return -1;polje_konstanta[순번]=절반값();}
            else TAKE_VALUE(Velikost);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!informacijska_tehnologija_neveljaven;순번++){
        metoda_vnos*Skupina_spremeniti_velikost=메소드목록+순번;Skupina_spremeniti_velikost->konfiguracija_storitev_Background_Intelligent_Transfer_Service=절반값();Skupina_spremeniti_velikost->Ime=절반값();Skupina_spremeniti_velikost->서술값=절반값();unsigned vnos_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<vnos_COUNT&&!informacijska_tehnologija_neveljaven;안쪽순번++){
            unsigned Ime=절반값(),Velikost=가득참(),Zaženi=sprotno_položaj;
            if(Velikost>길이-sprotno_položaj)return -1;
            if(UNICODE_VALUE(Ime,"Code")){
                Skupina_spremeniti_velikost->Sklad_Senzor_prostora=절반값();Skupina_spremeniti_velikost->지역변수들=절반값();Skupina_spremeniti_velikost->Velikost=가득참();Skupina_spremeniti_velikost->navodilo_SEQUENCE=TAKE_VALUE(Skupina_spremeniti_velikost->Velikost);
                if(Skupina_spremeniti_velikost->Sklad_Senzor_prostora>128||Skupina_spremeniti_velikost->지역변수들>128||Skupina_spremeniti_velikost->Velikost>8192||절반값())return -1;lastnosti();
            }else TAKE_VALUE(Velikost);
            if(sprotno_položaj!=Zaženi+Velikost)return -1;
        }
        if(!UNICODE_VALUE(Skupina_spremeniti_velikost->Ime,"<init>")&&(!(Skupina_spremeniti_velikost->konfiguracija_storitev_Background_Intelligent_Transfer_Service&8)||(Skupina_spremeniti_velikost->konfiguracija_storitev_Background_Intelligent_Transfer_Service&(0x100|0x20))||!Skupina_spremeniti_velikost->Velikost))return -1;
    }
    lastnosti();return informacijska_tehnologija_neveljaven||sprotno_položaj!=길이?-1:0;
}
static void konstanta_VALUE(unsigned identifikator_VALUE){
    if(!identifikator_VALUE||identifikator_VALUE>=konstanta_seštevek){informacijska_tehnologija_neveljaven=1;return;}
    if(Zvrsti_Seznam[identifikator_VALUE]==3)내보내기("P(%uU);",첫째값[identifikator_VALUE]);
    else if(Zvrsti_Seznam[identifikator_VALUE]==8)내보내기("P((W)k%u);",identifikator_VALUE);else informacijska_tehnologija_neveljaven=1;
}
static void 호출(unsigned identifikator_VALUE,int navidezen_CALL){
    if(identifikator_VALUE<1||identifikator_VALUE>=konstanta_seštevek||(Zvrsti_Seznam[identifikator_VALUE]!=10&&Zvrsti_Seznam[identifikator_VALUE]!=11)||첫째값[identifikator_VALUE]<1||첫째값[identifikator_VALUE]>=konstanta_seštevek||Zvrsti_Seznam[첫째값[identifikator_VALUE]]!=7||SECOND_VALUE[identifikator_VALUE]<1||SECOND_VALUE[identifikator_VALUE]>=konstanta_seštevek||Zvrsti_Seznam[SECOND_VALUE[identifikator_VALUE]]!=12){informacijska_tehnologija_neveljaven=1;return;}
    unsigned lastnik_predmet=첫째값[첫째값[identifikator_VALUE]],Ime=첫째값[SECOND_VALUE[identifikator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikator_VALUE]];int REZULTAT=0,element_COUNT=서술자(서술값,&REZULTAT);if(element_COUNT<0){informacijska_tehnologija_neveljaven=1;return;}
    for(int 순번=element_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(navidezen_CALL)내보내기("Q();");
    if(!navidezen_CALL&&같음(lastnik_predmet,첫째값[sprotno_Razred])){
        unsigned Skupina_spremeniti_velikost=0;for(;Skupina_spremeniti_velikost<메소드개수;Skupina_spremeniti_velikost++)if(같음(Ime,메소드목록[Skupina_spremeniti_velikost].Ime)&&같음(서술값,메소드목록[Skupina_spremeniti_velikost].서술값))break;
        if(Skupina_spremeniti_velikost==메소드개수||!(메소드목록[Skupina_spremeniti_velikost].konfiguracija_storitev_Background_Intelligent_Transfer_Service&8)){informacijska_tehnologija_neveljaven=1;return;}
        if(REZULTAT)내보내기("P(");내보내기("m%u(",Skupina_spremeniti_velikost);for(int 순번=0;순번<element_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(REZULTAT?"));":" );");return;
    }
    if((navidezen_CALL&&UNICODE_VALUE(lastnik_predmet,"java/io/PrintStream")&& (UNICODE_VALUE(Ime,"print")||UNICODE_VALUE(Ime,"println")))||(!navidezen_CALL&&UNICODE_VALUE(lastnik_predmet,"slovenščina/lastno/Izpis"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Ime,"print")||UNICODE_VALUE(Ime,"println")||UNICODE_VALUE(Ime,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Ime,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Ime,"print")||UNICODE_VALUE(Ime,"println")||UNICODE_VALUE(Ime,"Pisanje")||UNICODE_VALUE(Ime,"pisati_linija"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Ime,"print")||UNICODE_VALUE(Ime,"Pisanje")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Ime,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!navidezen_CALL&&UNICODE_VALUE(lastnik_predmet,"slovenščina/lastno/Datoteka")){
        if(UNICODE_VALUE(Ime,"Pisanje")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Ime,"Branje")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    informacijska_tehnologija_neveljaven=1;
}
static void prevajati_metoda(unsigned LOOKUP_INDEX){
    metoda_vnos*Skupina_spremeniti_velikost=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(Skupina_spremeniti_velikost->Ime,"<init>"))return;int REZULTAT,element_COUNT=서술자(Skupina_spremeniti_velikost->서술값,&REZULTAT);if(element_COUNT<0){informacijska_tehnologija_neveljaven=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<element_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!element_COUNT)내보내기("void");
    if((unsigned)element_COUNT>Skupina_spremeniti_velikost->지역변수들){informacijska_tehnologija_neveljaven=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Skupina_spremeniti_velikost->지역변수들?Skupina_spremeniti_velikost->지역변수들:1);for(int 순번=0;순번<element_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=길이;길이=Skupina_spremeniti_velikost->navodilo_SEQUENCE+Skupina_spremeniti_velikost->Velikost;sprotno_položaj=Skupina_spremeniti_velikost->navodilo_SEQUENCE;
    while(sprotno_položaj<길이&&!informacijska_tehnologija_neveljaven){unsigned ukaz_položaj=sprotno_položaj-Skupina_spremeniti_velikost->navodilo_SEQUENCE,postopek_VALUE=bajt_podatki();내보내기("L%u:;",ukaz_položaj);
        if(postopek_VALUE==0){}
        else if(postopek_VALUE==1)내보내기("P(0);");
        else if(postopek_VALUE>=2&&postopek_VALUE<=8)내보내기("P(%uU);",postopek_VALUE-3);
        else if(postopek_VALUE==16){int VALUE=(int8_t)bajt_podatki();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(postopek_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(postopek_VALUE==18||postopek_VALUE==19)konstanta_VALUE(postopek_VALUE==18?bajt_podatki():절반값());
        else if(postopek_VALUE==21||postopek_VALUE==25){unsigned 순번=bajt_podatki();if(순번>=Skupina_spremeniti_velikost->지역변수들)informacijska_tehnologija_neveljaven=1;내보내기("P(v[%u]);",순번);}
        else if((postopek_VALUE>=26&&postopek_VALUE<=29)||(postopek_VALUE>=42&&postopek_VALUE<=45)){unsigned 순번=postopek_VALUE>=42?postopek_VALUE-42:postopek_VALUE-26;if(순번>=Skupina_spremeniti_velikost->지역변수들)informacijska_tehnologija_neveljaven=1;내보내기("P(v[%u]);",순번);}
        else if(postopek_VALUE==54||postopek_VALUE==58){unsigned 순번=bajt_podatki();if(순번>=Skupina_spremeniti_velikost->지역변수들)informacijska_tehnologija_neveljaven=1;내보내기("v[%u]=Q();",순번);}
        else if((postopek_VALUE>=59&&postopek_VALUE<=62)||(postopek_VALUE>=75&&postopek_VALUE<=78)){unsigned 순번=postopek_VALUE>=75?postopek_VALUE-75:postopek_VALUE-59;if(순번>=Skupina_spremeniti_velikost->지역변수들)informacijska_tehnologija_neveljaven=1;내보내기("v[%u]=Q();",순번);}
        else if(postopek_VALUE==46||postopek_VALUE==50||postopek_VALUE==51||postopek_VALUE==52||postopek_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(postopek_VALUE==79||postopek_VALUE==83||postopek_VALUE==84||postopek_VALUE==85||postopek_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",postopek_VALUE==84?"(unsigned)(signed char)q":postopek_VALUE==85?"(unsigned short)q":postopek_VALUE==86?"(unsigned)(short)q":"q");
        else if(postopek_VALUE==87)내보내기("Q();");
        else if(postopek_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(postopek_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(postopek_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(postopek_VALUE==96||postopek_VALUE==100||postopek_VALUE==104||postopek_VALUE==120||postopek_VALUE==124||postopek_VALUE==126||postopek_VALUE==128||postopek_VALUE==130){const char*kodiranje_VALUE=postopek_VALUE==96?"+":postopek_VALUE==100?"-":postopek_VALUE==104?"*":postopek_VALUE==120?"<<":postopek_VALUE==124?">>":postopek_VALUE==126?"&":postopek_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kodiranje_VALUE,postopek_VALUE==120||postopek_VALUE==124?"%32":"");}
        else if(postopek_VALUE==108||postopek_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",postopek_VALUE==112);
        else if(postopek_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(postopek_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(postopek_VALUE==132){unsigned 순번=bajt_podatki();int 차이=(int8_t)bajt_podatki();if(순번>=Skupina_spremeniti_velikost->지역변수들)informacijska_tehnologija_neveljaven=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(postopek_VALUE>=145&&postopek_VALUE<=147)내보내기("P((unsigned)(%s)Q());",postopek_VALUE==145?"signed char":postopek_VALUE==146?"unsigned short":"short");
        else if(postopek_VALUE>=153&&postopek_VALUE<=166){int tarča=(int)ukaz_položaj+(int16_t)절반값();const char*Primerjava_VALUE[]={"==","!=","<",">=",">","<="};if(tarča<0||tarča>=(int)Skupina_spremeniti_velikost->Velikost){informacijska_tehnologija_neveljaven=1;break;}if(postopek_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Primerjava_VALUE[postopek_VALUE-153],tarča);else if(postopek_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Primerjava_VALUE[postopek_VALUE-159],tarča);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",postopek_VALUE==165?"==":"!=",tarča);}
        else if(postopek_VALUE==167){int tarča=(int)ukaz_položaj+(int16_t)절반값();if(tarča<0||tarča>=(int)Skupina_spremeniti_velikost->Velikost)informacijska_tehnologija_neveljaven=1;내보내기("goto L%d;",tarča);}
        else if(postopek_VALUE==172||postopek_VALUE==176)내보내기("return Q();");else if(postopek_VALUE==177)내보내기("return 0;");
        else if(postopek_VALUE==178||postopek_VALUE==179){unsigned identifikator_VALUE=절반값();if(identifikator_VALUE<1||identifikator_VALUE>=konstanta_seštevek||Zvrsti_Seznam[identifikator_VALUE]!=9||첫째값[identifikator_VALUE]>=konstanta_seštevek||SECOND_VALUE[identifikator_VALUE]>=konstanta_seštevek||Zvrsti_Seznam[첫째값[identifikator_VALUE]]!=7||Zvrsti_Seznam[SECOND_VALUE[identifikator_VALUE]]!=12){informacijska_tehnologija_neveljaven=1;break;}unsigned lastnik_predmet=첫째값[첫째값[identifikator_VALUE]],Ime=첫째값[SECOND_VALUE[identifikator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikator_VALUE]];
            if(postopek_VALUE==178&&UNICODE_VALUE(lastnik_predmet,"java/lang/System")&&UNICODE_VALUE(Ime,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Datoteka_vnos=0;while(Datoteka_vnos<필드개수&&(!같음(Ime,ime_polja[Datoteka_vnos])||!같음(서술값,필드서술[Datoteka_vnos])))Datoteka_vnos++;if(!같음(lastnik_predmet,첫째값[sprotno_Razred])||Datoteka_vnos==필드개수){informacijska_tehnologija_neveljaven=1;break;}내보내기(postopek_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",Datoteka_vnos);}}
        else if(postopek_VALUE==182||postopek_VALUE==184)호출(절반값(),postopek_VALUE==182);
        else if(postopek_VALUE==188){unsigned Tip_območje=bajt_podatki();if(Tip_območje!=4&&Tip_območje!=5&&Tip_območje!=8&&Tip_območje!=9&&Tip_območje!=10)informacijska_tehnologija_neveljaven=1;내보내기("P(jarray((int)Q()));");}
        else if(postopek_VALUE==190)내보내기("P(jlength(Q()));");
        else if(postopek_VALUE==198||postopek_VALUE==199){int tarča=(int)ukaz_položaj+(int16_t)절반값();if(tarča<0||tarča>=(int)Skupina_spremeniti_velikost->Velikost)informacijska_tehnologija_neveljaven=1;내보내기("if(Q()%s0)goto L%d;",postopek_VALUE==198?"==":"!=",tarča);}
        else informacijska_tehnologija_neveljaven=1;
        if(informacijska_tehnologija_neveljaven)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,postopek_VALUE,ukaz_položaj);
        내보내기("\n");
    }
    길이=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned niz_enota(unsigned *podatki_položaj,unsigned končati_klic_odmik){
    if(*podatki_položaj>=končati_klic_odmik){informacijska_tehnologija_neveljaven=1;return 0;}unsigned koda_znaka=podatki[(*podatki_položaj)++];
    if(koda_znaka<128)return koda_znaka;
    unsigned element_COUNT=koda_znaka>=0xc0&&koda_znaka<=0xdf?1:koda_znaka>=0xe0&&koda_znaka<=0xef?2:3;
    if(element_COUNT==3||element_COUNT>končati_klic_odmik-*podatki_položaj){informacijska_tehnologija_neveljaven=1;return 0;}unsigned VALUE=koda_znaka&((1u<<(6-element_COUNT))-1);
    for(unsigned 순번=0;순번<element_COUNT;순번++){unsigned Naprej_element=podatki[(*podatki_položaj)++];if((Naprej_element&0xc0)!=0x80)informacijska_tehnologija_neveljaven=1;VALUE=VALUE<<6|(Naprej_element&63);}
    if((element_COUNT==1&&VALUE<128&&VALUE!=0)||(element_COUNT==2&&VALUE<2048))informacijska_tehnologija_neveljaven=1;return VALUE;
}
static void niz_konstanta(unsigned identifikator_VALUE){
    unsigned 부호없는값=첫째값[identifikator_VALUE];if(부호없는값<1||부호없는값>=konstanta_seštevek||Zvrsti_Seznam[부호없는값]!=1){informacijska_tehnologija_neveljaven=1;return;}내보내기("static const unsigned char k%u[]={",identifikator_VALUE);
    unsigned podatki_položaj=첫째값[부호없는값],končati_klic_odmik=podatki_položaj+SECOND_VALUE[부호없는값];
    while(podatki_položaj<končati_klic_odmik&&!informacijska_tehnologija_neveljaven){unsigned koda_znaka=niz_enota(&podatki_položaj,končati_klic_odmik);
        if(koda_znaka>=0xd800&&koda_znaka<=0xdbff){unsigned 낮은부분=niz_enota(&podatki_položaj,končati_klic_odmik);if(낮은부분<0xdc00||낮은부분>0xdfff){informacijska_tehnologija_neveljaven=1;break;}koda_znaka=0x10000+((koda_znaka-0xd800)<<10)+낮은부분-0xdc00;}
        else if(koda_znaka>=0xdc00&&koda_znaka<=0xdfff){informacijska_tehnologija_neveljaven=1;break;}
        if(!koda_znaka){printf("jaot: embedded NUL string needs JVM mode\n");informacijska_tehnologija_neveljaven=1;break;}
        if(koda_znaka<128)내보내기("%u,",koda_znaka);
        else{unsigned element_COUNT=koda_znaka<2048?2:koda_znaka<65536?3:4;내보내기("%u,",(element_COUNT==2?0xc0:element_COUNT==3?0xe0:0xf0)|(koda_znaka>>(6*(element_COUNT-1))));for(unsigned 순번=element_COUNT-1;순번;순번--)내보내기("%u,",0x80|((koda_znaka>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Ime){
    size_t element_COUNT=strlen(Ime);
    if(element_COUNT>4&&!strcmp(Ime+element_COUNT-4,".jar")){
        if(꾸러미열기(Ime)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char POT[256];const char*vnos_metoda=꾸러미진입클래스();element_COUNT=strlen(vnos_metoda);if(element_COUNT+6>=sizeof(POT))return 0;
        for(unsigned 순번=0;순번<element_COUNT;순번++)POT[순번]=vnos_metoda[순번]=='.'?'/':vnos_metoda[순번];strcpy(POT+element_COUNT,".class");int vnos_COUNT=꾸러미읽기(POT,podatki,sizeof(podatki));if(vnos_COUNT<0)return 0;길이=vnos_COUNT;
    }else{intptr_t Datoteka_ročica=사용자호출(3,(uintptr_t)Ime,0,0,0,0,0);if(Datoteka_ročica<0)return 0;intptr_t vnos_COUNT=사용자호출(9,Datoteka_ročica,0,0,0,0,0);if(vnos_COUNT<0||vnos_COUNT>sizeof(podatki)){사용자호출(4,Datoteka_ročica,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,Datoteka_ročica,(uintptr_t)podatki,vnos_COUNT,0,0,0);사용자호출(4,Datoteka_ročica,0,0,0,0,0);if(RECEIVED_COUNT!=vnos_COUNT)return 0;길이=vnos_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstanta_seštevek&&!informacijska_tehnologija_neveljaven;순번++)if(Zvrsti_Seznam[순번]==8)niz_konstanta(순번);
    if(informacijska_tehnologija_neveljaven)return 0;
    int vnos_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Ime,"<init>")){
        int REZULTAT,vnos_COUNT=서술자(메소드목록[순번].서술값,&REZULTAT);if(vnos_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<vnos_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!vnos_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Ime,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfiguracija_storitev_Background_Intelligent_Transfer_Service&9)==9)vnos_p=순번;
        if(UNICODE_VALUE(메소드목록[순번].Ime,"<clinit>"))초기값=순번;
    }
    if(vnos_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!informacijska_tehnologija_neveljaven;순번++)prevajati_metoda(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(polje_konstanta[순번]){
        unsigned koda_znaka=polje_konstanta[순번];if(koda_znaka>=konstanta_seštevek)return 0;
        if(Zvrsti_Seznam[koda_znaka]==3)내보내기("fields[%u]=%uU;",순번,첫째값[koda_znaka]);else if(Zvrsti_Seznam[koda_znaka]==8)내보내기("fields[%u]=(W)k%u;",순번,koda_znaka);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",vnos_p);
    return informacijska_tehnologija_neveljaven?0:Besedilo;
}
