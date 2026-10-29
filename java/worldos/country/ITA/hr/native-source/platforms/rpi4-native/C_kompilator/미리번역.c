#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "komplet.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char podaci[16384];static unsigned 길이,redovno_položaj;static int odjel_informacijske_tehnologije_nevaljan;
static unsigned Kategorije_Popis[512],첫째값[512],SECOND_VALUE[512],konstanta_ukupan_broj,redovno_poduka;
static char Tekst[65536];static unsigned veličina_teksta;
typedef struct {unsigned konfiguracija_Pozadinski_pametni_servis_za_transfer,Ime,서술값,명령열,Veličina,지역변수들,hrpa_Pohrana;} postupak_unos;
static postupak_unos 메소드목록[64];static unsigned 메소드개수;
static unsigned naziv_polja[64],필드서술[64],polje_konstanta[64],필드개수;
static unsigned TAKE_VALUE(unsigned artikl_COUNT){if(redovno_položaj>길이||artikl_COUNT>길이-redovno_položaj){odjel_informacijske_tehnologije_nevaljan=1;return 0;}unsigned podaci_položaj=redovno_položaj;redovno_položaj+=artikl_COUNT;return podaci_položaj;}
static unsigned bajt_podaci(void){unsigned podaci_položaj=TAKE_VALUE(1);return odjel_informacijske_tehnologije_nevaljan?0:podaci[podaci_položaj];}
static unsigned 절반값(void){unsigned koordinata_x=bajt_podaci();return koordinata_x<<8|bajt_podaci();}
static uint32_t 가득참(void){uint32_t koordinata_x=절반값();return koordinata_x<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*niz_podaci){return 순번>0&&순번<konstanta_ukupan_broj&&Kategorije_Popis[순번]==1&&strlen(niz_podaci)==SECOND_VALUE[순번]&&!memcmp(podaci+첫째값[순번],niz_podaci,SECOND_VALUE[순번]);}
static int 같음(unsigned koordinata_x,unsigned 세로좌표){return koordinata_x>0&&koordinata_x<konstanta_ukupan_broj&&세로좌표>0&&세로좌표<konstanta_ukupan_broj&&Kategorije_Popis[koordinata_x]==1&&Kategorije_Popis[세로좌표]==1&&SECOND_VALUE[koordinata_x]==SECOND_VALUE[세로좌표]&&!memcmp(podaci+첫째값[koordinata_x],podaci+첫째값[세로좌표],SECOND_VALUE[koordinata_x]);}
static void 내보내기(const char*Datoteka_unos,...){if(odjel_informacijske_tehnologije_nevaljan)return;va_list argument_ARRAY;va_start(argument_ARRAY,Datoteka_unos);int artikl_COUNT=vsnprintf(Tekst+veličina_teksta,sizeof(Tekst)-veličina_teksta,Datoteka_unos,argument_ARRAY);va_end(argument_ARRAY);if(artikl_COUNT<0||(unsigned)artikl_COUNT>=sizeof(Tekst)-veličina_teksta){odjel_informacijske_tehnologije_nevaljan=1;return;}veličina_teksta+=artikl_COUNT;}
static int 서술자(unsigned identifikator_VALUE,int*REZULTAT){
    if(identifikator_VALUE<1||identifikator_VALUE>=konstanta_ukupan_broj||Kategorije_Popis[identifikator_VALUE]!=1)return -1;unsigned podaci_položaj=첫째값[identifikator_VALUE],završiti_razgovor_pomak=podaci_položaj+SECOND_VALUE[identifikator_VALUE];if(podaci_položaj>=završiti_razgovor_pomak||podaci[podaci_položaj++]!='(')return -1;int unos_COUNT=0;
    while(podaci_položaj<završiti_razgovor_pomak&&podaci[podaci_položaj]!=')'){
        unsigned kodna_točka=podaci[podaci_položaj++];while(kodna_točka=='['&&podaci_položaj<završiti_razgovor_pomak)kodna_točka=podaci[podaci_položaj++];
        if(kodna_točka=='L'){while(podaci_položaj<završiti_razgovor_pomak&&podaci[podaci_položaj]!=';')podaci_položaj++;if(podaci_položaj==završiti_razgovor_pomak)return -1;podaci_položaj++;}
        else if(kodna_točka!='I'&&kodna_točka!='Z'&&kodna_točka!='B'&&kodna_točka!='C'&&kodna_točka!='S')return -1;
        if(++unos_COUNT>16)return -1;
    }
    if(podaci_položaj+1>=završiti_razgovor_pomak||podaci[podaci_položaj++]!=')')return -1;*REZULTAT=podaci[podaci_položaj]=='V'?0:1;
    if(podaci[podaci_položaj]=='J'||podaci[podaci_položaj]=='D'||podaci[podaci_položaj]=='F')return -1;return unos_COUNT;
}
static void karakteristike(void){unsigned artikl_COUNT=절반값();for(unsigned 순번=0;순번<artikl_COUNT&&!odjel_informacijske_tehnologije_nevaljan;순번++){절반값();unsigned Veličina=가득참();TAKE_VALUE(Veličina);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned radna_verzija=절반값(),broj_verzije=절반값();if(radna_verzija||broj_verzije<45||broj_verzije>52)return -1;
    konstanta_ukupan_broj=절반값();if(konstanta_ukupan_broj<1||konstanta_ukupan_broj>512)return -1;
    for(unsigned 순번=1;순번<konstanta_ukupan_broj&&!odjel_informacijske_tehnologije_nevaljan;순번++){
        Kategorije_Popis[순번]=bajt_podaci();switch(Kategorije_Popis[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=konstanta_ukupan_broj)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=bajt_podaci();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();redovno_poduka=절반값();절반값();if(redovno_poduka<1||redovno_poduka>=konstanta_ukupan_broj||Kategorije_Popis[redovno_poduka]!=7||첫째값[redovno_poduka]<1||첫째값[redovno_poduka]>=konstanta_ukupan_broj||Kategorije_Popis[첫째값[redovno_poduka]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!odjel_informacijske_tehnologije_nevaljan;순번++){
        unsigned konfiguracija_Pozadinski_pametni_servis_za_transfer=절반값();naziv_polja[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfiguracija_Pozadinski_pametni_servis_za_transfer&8))return -1;
        unsigned unos_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<unos_COUNT&&!odjel_informacijske_tehnologije_nevaljan;안쪽순번++){
            unsigned Ime=절반값(),Veličina=가득참();
            if(UNICODE_VALUE(Ime,"ConstantValue")){if(Veličina!=2)return -1;polje_konstanta[순번]=절반값();}
            else TAKE_VALUE(Veličina);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!odjel_informacijske_tehnologije_nevaljan;순번++){
        postupak_unos*Grupa_promijeniti_veličinu=메소드목록+순번;Grupa_promijeniti_veličinu->konfiguracija_Pozadinski_pametni_servis_za_transfer=절반값();Grupa_promijeniti_veličinu->Ime=절반값();Grupa_promijeniti_veličinu->서술값=절반값();unsigned unos_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<unos_COUNT&&!odjel_informacijske_tehnologije_nevaljan;안쪽순번++){
            unsigned Ime=절반값(),Veličina=가득참(),Pokreni=redovno_položaj;
            if(Veličina>길이-redovno_položaj)return -1;
            if(UNICODE_VALUE(Ime,"Code")){
                Grupa_promijeniti_veličinu->hrpa_Pohrana=절반값();Grupa_promijeniti_veličinu->지역변수들=절반값();Grupa_promijeniti_veličinu->Veličina=가득참();Grupa_promijeniti_veličinu->명령열=TAKE_VALUE(Grupa_promijeniti_veličinu->Veličina);
                if(Grupa_promijeniti_veličinu->hrpa_Pohrana>128||Grupa_promijeniti_veličinu->지역변수들>128||Grupa_promijeniti_veličinu->Veličina>8192||절반값())return -1;karakteristike();
            }else TAKE_VALUE(Veličina);
            if(redovno_položaj!=Pokreni+Veličina)return -1;
        }
        if(!UNICODE_VALUE(Grupa_promijeniti_veličinu->Ime,"<init>")&&(!(Grupa_promijeniti_veličinu->konfiguracija_Pozadinski_pametni_servis_za_transfer&8)||(Grupa_promijeniti_veličinu->konfiguracija_Pozadinski_pametni_servis_za_transfer&(0x100|0x20))||!Grupa_promijeniti_veličinu->Veličina))return -1;
    }
    karakteristike();return odjel_informacijske_tehnologije_nevaljan||redovno_položaj!=길이?-1:0;
}
static void konstanta_VALUE(unsigned identifikator_VALUE){
    if(!identifikator_VALUE||identifikator_VALUE>=konstanta_ukupan_broj){odjel_informacijske_tehnologije_nevaljan=1;return;}
    if(Kategorije_Popis[identifikator_VALUE]==3)내보내기("P(%uU);",첫째값[identifikator_VALUE]);
    else if(Kategorije_Popis[identifikator_VALUE]==8)내보내기("P((W)k%u);",identifikator_VALUE);else odjel_informacijske_tehnologije_nevaljan=1;
}
static void 호출(unsigned identifikator_VALUE,int 가상호출){
    if(identifikator_VALUE<1||identifikator_VALUE>=konstanta_ukupan_broj||(Kategorije_Popis[identifikator_VALUE]!=10&&Kategorije_Popis[identifikator_VALUE]!=11)||첫째값[identifikator_VALUE]<1||첫째값[identifikator_VALUE]>=konstanta_ukupan_broj||Kategorije_Popis[첫째값[identifikator_VALUE]]!=7||SECOND_VALUE[identifikator_VALUE]<1||SECOND_VALUE[identifikator_VALUE]>=konstanta_ukupan_broj||Kategorije_Popis[SECOND_VALUE[identifikator_VALUE]]!=12){odjel_informacijske_tehnologije_nevaljan=1;return;}
    unsigned vlasnik_objekt=첫째값[첫째값[identifikator_VALUE]],Ime=첫째값[SECOND_VALUE[identifikator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikator_VALUE]];int REZULTAT=0,artikl_COUNT=서술자(서술값,&REZULTAT);if(artikl_COUNT<0){odjel_informacijske_tehnologije_nevaljan=1;return;}
    for(int 순번=artikl_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(가상호출)내보내기("Q();");
    if(!가상호출&&같음(vlasnik_objekt,첫째값[redovno_poduka])){
        unsigned Grupa_promijeniti_veličinu=0;for(;Grupa_promijeniti_veličinu<메소드개수;Grupa_promijeniti_veličinu++)if(같음(Ime,메소드목록[Grupa_promijeniti_veličinu].Ime)&&같음(서술값,메소드목록[Grupa_promijeniti_veličinu].서술값))break;
        if(Grupa_promijeniti_veličinu==메소드개수||!(메소드목록[Grupa_promijeniti_veličinu].konfiguracija_Pozadinski_pametni_servis_za_transfer&8)){odjel_informacijske_tehnologije_nevaljan=1;return;}
        if(REZULTAT)내보내기("P(");내보내기("m%u(",Grupa_promijeniti_veličinu);for(int 순번=0;순번<artikl_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(REZULTAT?"));":" );");return;
    }
    if((가상호출&&UNICODE_VALUE(vlasnik_objekt,"java/io/PrintStream")&& (UNICODE_VALUE(Ime,"print")||UNICODE_VALUE(Ime,"println")))||(!가상호출&&UNICODE_VALUE(vlasnik_objekt,"hrvatski/vlastiti/Izlaz"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Ime,"print")||UNICODE_VALUE(Ime,"println")||UNICODE_VALUE(Ime,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Ime,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Ime,"print")||UNICODE_VALUE(Ime,"println")||UNICODE_VALUE(Ime,"Zapisuj")||UNICODE_VALUE(Ime,"zapisivanje_red"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Ime,"print")||UNICODE_VALUE(Ime,"Zapisuj")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Ime,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!가상호출&&UNICODE_VALUE(vlasnik_objekt,"hrvatski/vlastiti/Datoteka")){
        if(UNICODE_VALUE(Ime,"Zapisuj")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Ime,"Čitaj")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    odjel_informacijske_tehnologije_nevaljan=1;
}
static void programski_prevesti_postupak(unsigned LOOKUP_INDEX){
    postupak_unos*Grupa_promijeniti_veličinu=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(Grupa_promijeniti_veličinu->Ime,"<init>"))return;int REZULTAT,artikl_COUNT=서술자(Grupa_promijeniti_veličinu->서술값,&REZULTAT);if(artikl_COUNT<0){odjel_informacijske_tehnologije_nevaljan=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<artikl_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!artikl_COUNT)내보내기("void");
    if((unsigned)artikl_COUNT>Grupa_promijeniti_veličinu->지역변수들){odjel_informacijske_tehnologije_nevaljan=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Grupa_promijeniti_veličinu->지역변수들?Grupa_promijeniti_veličinu->지역변수들:1);for(int 순번=0;순번<artikl_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=길이;길이=Grupa_promijeniti_veličinu->명령열+Grupa_promijeniti_veličinu->Veličina;redovno_položaj=Grupa_promijeniti_veličinu->명령열;
    while(redovno_položaj<길이&&!odjel_informacijske_tehnologije_nevaljan){unsigned naredba_položaj=redovno_položaj-Grupa_promijeniti_veličinu->명령열,operacija_VALUE=bajt_podaci();내보내기("L%u:;",naredba_položaj);
        if(operacija_VALUE==0){}
        else if(operacija_VALUE==1)내보내기("P(0);");
        else if(operacija_VALUE>=2&&operacija_VALUE<=8)내보내기("P(%uU);",operacija_VALUE-3);
        else if(operacija_VALUE==16){int VALUE=(int8_t)bajt_podaci();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operacija_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operacija_VALUE==18||operacija_VALUE==19)konstanta_VALUE(operacija_VALUE==18?bajt_podaci():절반값());
        else if(operacija_VALUE==21||operacija_VALUE==25){unsigned 순번=bajt_podaci();if(순번>=Grupa_promijeniti_veličinu->지역변수들)odjel_informacijske_tehnologije_nevaljan=1;내보내기("P(v[%u]);",순번);}
        else if((operacija_VALUE>=26&&operacija_VALUE<=29)||(operacija_VALUE>=42&&operacija_VALUE<=45)){unsigned 순번=operacija_VALUE>=42?operacija_VALUE-42:operacija_VALUE-26;if(순번>=Grupa_promijeniti_veličinu->지역변수들)odjel_informacijske_tehnologije_nevaljan=1;내보내기("P(v[%u]);",순번);}
        else if(operacija_VALUE==54||operacija_VALUE==58){unsigned 순번=bajt_podaci();if(순번>=Grupa_promijeniti_veličinu->지역변수들)odjel_informacijske_tehnologije_nevaljan=1;내보내기("v[%u]=Q();",순번);}
        else if((operacija_VALUE>=59&&operacija_VALUE<=62)||(operacija_VALUE>=75&&operacija_VALUE<=78)){unsigned 순번=operacija_VALUE>=75?operacija_VALUE-75:operacija_VALUE-59;if(순번>=Grupa_promijeniti_veličinu->지역변수들)odjel_informacijske_tehnologije_nevaljan=1;내보내기("v[%u]=Q();",순번);}
        else if(operacija_VALUE==46||operacija_VALUE==50||operacija_VALUE==51||operacija_VALUE==52||operacija_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operacija_VALUE==79||operacija_VALUE==83||operacija_VALUE==84||operacija_VALUE==85||operacija_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operacija_VALUE==84?"(unsigned)(signed char)q":operacija_VALUE==85?"(unsigned short)q":operacija_VALUE==86?"(unsigned)(short)q":"q");
        else if(operacija_VALUE==87)내보내기("Q();");
        else if(operacija_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(operacija_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operacija_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(operacija_VALUE==96||operacija_VALUE==100||operacija_VALUE==104||operacija_VALUE==120||operacija_VALUE==124||operacija_VALUE==126||operacija_VALUE==128||operacija_VALUE==130){const char*šifriranje_VALUE=operacija_VALUE==96?"+":operacija_VALUE==100?"-":operacija_VALUE==104?"*":operacija_VALUE==120?"<<":operacija_VALUE==124?">>":operacija_VALUE==126?"&":operacija_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",šifriranje_VALUE,operacija_VALUE==120||operacija_VALUE==124?"%32":"");}
        else if(operacija_VALUE==108||operacija_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operacija_VALUE==112);
        else if(operacija_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(operacija_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operacija_VALUE==132){unsigned 순번=bajt_podaci();int 차이=(int8_t)bajt_podaci();if(순번>=Grupa_promijeniti_veličinu->지역변수들)odjel_informacijske_tehnologije_nevaljan=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operacija_VALUE>=145&&operacija_VALUE<=147)내보내기("P((unsigned)(%s)Q());",operacija_VALUE==145?"signed char":operacija_VALUE==146?"unsigned short":"short");
        else if(operacija_VALUE>=153&&operacija_VALUE<=166){int cilj=(int)naredba_položaj+(int16_t)절반값();const char*Usporedba_VALUE[]={"==","!=","<",">=",">","<="};if(cilj<0||cilj>=(int)Grupa_promijeniti_veličinu->Veličina){odjel_informacijske_tehnologije_nevaljan=1;break;}if(operacija_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Usporedba_VALUE[operacija_VALUE-153],cilj);else if(operacija_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Usporedba_VALUE[operacija_VALUE-159],cilj);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operacija_VALUE==165?"==":"!=",cilj);}
        else if(operacija_VALUE==167){int cilj=(int)naredba_položaj+(int16_t)절반값();if(cilj<0||cilj>=(int)Grupa_promijeniti_veličinu->Veličina)odjel_informacijske_tehnologije_nevaljan=1;내보내기("goto L%d;",cilj);}
        else if(operacija_VALUE==172||operacija_VALUE==176)내보내기("return Q();");else if(operacija_VALUE==177)내보내기("return 0;");
        else if(operacija_VALUE==178||operacija_VALUE==179){unsigned identifikator_VALUE=절반값();if(identifikator_VALUE<1||identifikator_VALUE>=konstanta_ukupan_broj||Kategorije_Popis[identifikator_VALUE]!=9||첫째값[identifikator_VALUE]>=konstanta_ukupan_broj||SECOND_VALUE[identifikator_VALUE]>=konstanta_ukupan_broj||Kategorije_Popis[첫째값[identifikator_VALUE]]!=7||Kategorije_Popis[SECOND_VALUE[identifikator_VALUE]]!=12){odjel_informacijske_tehnologije_nevaljan=1;break;}unsigned vlasnik_objekt=첫째값[첫째값[identifikator_VALUE]],Ime=첫째값[SECOND_VALUE[identifikator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikator_VALUE]];
            if(operacija_VALUE==178&&UNICODE_VALUE(vlasnik_objekt,"java/lang/System")&&UNICODE_VALUE(Ime,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Datoteka_unos=0;while(Datoteka_unos<필드개수&&(!같음(Ime,naziv_polja[Datoteka_unos])||!같음(서술값,필드서술[Datoteka_unos])))Datoteka_unos++;if(!같음(vlasnik_objekt,첫째값[redovno_poduka])||Datoteka_unos==필드개수){odjel_informacijske_tehnologije_nevaljan=1;break;}내보내기(operacija_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",Datoteka_unos);}}
        else if(operacija_VALUE==182||operacija_VALUE==184)호출(절반값(),operacija_VALUE==182);
        else if(operacija_VALUE==188){unsigned TYPE_područje=bajt_podaci();if(TYPE_područje!=4&&TYPE_područje!=5&&TYPE_područje!=8&&TYPE_područje!=9&&TYPE_područje!=10)odjel_informacijske_tehnologije_nevaljan=1;내보내기("P(jarray((int)Q()));");}
        else if(operacija_VALUE==190)내보내기("P(jlength(Q()));");
        else if(operacija_VALUE==198||operacija_VALUE==199){int cilj=(int)naredba_položaj+(int16_t)절반값();if(cilj<0||cilj>=(int)Grupa_promijeniti_veličinu->Veličina)odjel_informacijske_tehnologije_nevaljan=1;내보내기("if(Q()%s0)goto L%d;",operacija_VALUE==198?"==":"!=",cilj);}
        else odjel_informacijske_tehnologije_nevaljan=1;
        if(odjel_informacijske_tehnologije_nevaljan)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,operacija_VALUE,naredba_položaj);
        내보내기("\n");
    }
    길이=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned niz_lekcija(unsigned *podaci_položaj,unsigned završiti_razgovor_pomak){
    if(*podaci_položaj>=završiti_razgovor_pomak){odjel_informacijske_tehnologije_nevaljan=1;return 0;}unsigned kodna_točka=podaci[(*podaci_položaj)++];
    if(kodna_točka<128)return kodna_točka;
    unsigned artikl_COUNT=kodna_točka>=0xc0&&kodna_točka<=0xdf?1:kodna_točka>=0xe0&&kodna_točka<=0xef?2:3;
    if(artikl_COUNT==3||artikl_COUNT>završiti_razgovor_pomak-*podaci_položaj){odjel_informacijske_tehnologije_nevaljan=1;return 0;}unsigned VALUE=kodna_točka&((1u<<(6-artikl_COUNT))-1);
    for(unsigned 순번=0;순번<artikl_COUNT;순번++){unsigned Dalje_artikl=podaci[(*podaci_položaj)++];if((Dalje_artikl&0xc0)!=0x80)odjel_informacijske_tehnologije_nevaljan=1;VALUE=VALUE<<6|(Dalje_artikl&63);}
    if((artikl_COUNT==1&&VALUE<128&&VALUE!=0)||(artikl_COUNT==2&&VALUE<2048))odjel_informacijske_tehnologije_nevaljan=1;return VALUE;
}
static void niz_konstanta(unsigned identifikator_VALUE){
    unsigned 부호없는값=첫째값[identifikator_VALUE];if(부호없는값<1||부호없는값>=konstanta_ukupan_broj||Kategorije_Popis[부호없는값]!=1){odjel_informacijske_tehnologije_nevaljan=1;return;}내보내기("static const unsigned char k%u[]={",identifikator_VALUE);
    unsigned podaci_položaj=첫째값[부호없는값],završiti_razgovor_pomak=podaci_položaj+SECOND_VALUE[부호없는값];
    while(podaci_položaj<završiti_razgovor_pomak&&!odjel_informacijske_tehnologije_nevaljan){unsigned kodna_točka=niz_lekcija(&podaci_položaj,završiti_razgovor_pomak);
        if(kodna_točka>=0xd800&&kodna_točka<=0xdbff){unsigned 낮은부분=niz_lekcija(&podaci_položaj,završiti_razgovor_pomak);if(낮은부분<0xdc00||낮은부분>0xdfff){odjel_informacijske_tehnologije_nevaljan=1;break;}kodna_točka=0x10000+((kodna_točka-0xd800)<<10)+낮은부분-0xdc00;}
        else if(kodna_točka>=0xdc00&&kodna_točka<=0xdfff){odjel_informacijske_tehnologije_nevaljan=1;break;}
        if(!kodna_točka){printf("jaot: embedded NUL string needs JVM mode\n");odjel_informacijske_tehnologije_nevaljan=1;break;}
        if(kodna_točka<128)내보내기("%u,",kodna_točka);
        else{unsigned artikl_COUNT=kodna_točka<2048?2:kodna_točka<65536?3:4;내보내기("%u,",(artikl_COUNT==2?0xc0:artikl_COUNT==3?0xe0:0xf0)|(kodna_točka>>(6*(artikl_COUNT-1))));for(unsigned 순번=artikl_COUNT-1;순번;순번--)내보내기("%u,",0x80|((kodna_točka>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Ime){
    size_t artikl_COUNT=strlen(Ime);
    if(artikl_COUNT>4&&!strcmp(Ime+artikl_COUNT-4,".jar")){
        if(꾸러미열기(Ime)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char PUTANJA[256];const char*unos_postupak=꾸러미진입클래스();artikl_COUNT=strlen(unos_postupak);if(artikl_COUNT+6>=sizeof(PUTANJA))return 0;
        for(unsigned 순번=0;순번<artikl_COUNT;순번++)PUTANJA[순번]=unos_postupak[순번]=='.'?'/':unos_postupak[순번];strcpy(PUTANJA+artikl_COUNT,".class");int unos_COUNT=꾸러미읽기(PUTANJA,podaci,sizeof(podaci));if(unos_COUNT<0)return 0;길이=unos_COUNT;
    }else{intptr_t Datoteka_ustroj=사용자호출(3,(uintptr_t)Ime,0,0,0,0,0);if(Datoteka_ustroj<0)return 0;intptr_t unos_COUNT=사용자호출(9,Datoteka_ustroj,0,0,0,0,0);if(unos_COUNT<0||unos_COUNT>sizeof(podaci)){사용자호출(4,Datoteka_ustroj,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,Datoteka_ustroj,(uintptr_t)podaci,unos_COUNT,0,0,0);사용자호출(4,Datoteka_ustroj,0,0,0,0,0);if(RECEIVED_COUNT!=unos_COUNT)return 0;길이=unos_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstanta_ukupan_broj&&!odjel_informacijske_tehnologije_nevaljan;순번++)if(Kategorije_Popis[순번]==8)niz_konstanta(순번);
    if(odjel_informacijske_tehnologije_nevaljan)return 0;
    int unos_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Ime,"<init>")){
        int REZULTAT,unos_COUNT=서술자(메소드목록[순번].서술값,&REZULTAT);if(unos_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<unos_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!unos_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Ime,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfiguracija_Pozadinski_pametni_servis_za_transfer&9)==9)unos_p=순번;
        if(UNICODE_VALUE(메소드목록[순번].Ime,"<clinit>"))초기값=순번;
    }
    if(unos_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!odjel_informacijske_tehnologije_nevaljan;순번++)programski_prevesti_postupak(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(polje_konstanta[순번]){
        unsigned kodna_točka=polje_konstanta[순번];if(kodna_točka>=konstanta_ukupan_broj)return 0;
        if(Kategorije_Popis[kodna_točka]==3)내보내기("fields[%u]=%uU;",순번,첫째값[kodna_točka]);else if(Kategorije_Popis[kodna_točka]==8)내보내기("fields[%u]=(W)k%u;",순번,kodna_točka);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",unos_p);
    return odjel_informacijske_tehnologije_nevaljan?0:Tekst;
}
