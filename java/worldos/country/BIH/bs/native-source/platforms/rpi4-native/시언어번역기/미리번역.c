#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "paket.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char podaci[16384];static unsigned dužina_VALUE,trenutno_položaj;static int odjel_za_informacijske_tehnologije_nevažeće;
static unsigned Kategorije_spisak[512],첫째값[512],SECOND_VALUE[512],konstanta_ukupan_broj,trenutno_klasa;
static char Tekst[65536];static unsigned Veličina_teksta;
typedef struct {unsigned 설정비트,Naziv,서술값,programska_naredba_SEQUENCE,Veličina,지역변수들,snop_Pohrana;} metoda_unos;
static metoda_unos 메소드목록[64];static unsigned 메소드개수;
static unsigned naziv_polja[64],필드서술[64],polje_konstanta[64],필드개수;
static unsigned TAKE_VALUE(unsigned stavka_COUNT){if(trenutno_položaj>dužina_VALUE||stavka_COUNT>dužina_VALUE-trenutno_položaj){odjel_za_informacijske_tehnologije_nevažeće=1;return 0;}unsigned podaci_položaj=trenutno_položaj;trenutno_položaj+=stavka_COUNT;return podaci_položaj;}
static unsigned bajt_podaci(void){unsigned podaci_položaj=TAKE_VALUE(1);return odjel_za_informacijske_tehnologije_nevažeće?0:podaci[podaci_položaj];}
static unsigned 절반값(void){unsigned koordinata_x=bajt_podaci();return koordinata_x<<8|bajt_podaci();}
static uint32_t 가득참(void){uint32_t koordinata_x=절반값();return koordinata_x<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*string_podaci){return 순번>0&&순번<konstanta_ukupan_broj&&Kategorije_spisak[순번]==1&&strlen(string_podaci)==SECOND_VALUE[순번]&&!memcmp(podaci+첫째값[순번],string_podaci,SECOND_VALUE[순번]);}
static int 같음(unsigned koordinata_x,unsigned Y_koordinata){return koordinata_x>0&&koordinata_x<konstanta_ukupan_broj&&Y_koordinata>0&&Y_koordinata<konstanta_ukupan_broj&&Kategorije_spisak[koordinata_x]==1&&Kategorije_spisak[Y_koordinata]==1&&SECOND_VALUE[koordinata_x]==SECOND_VALUE[Y_koordinata]&&!memcmp(podaci+첫째값[koordinata_x],podaci+첫째값[Y_koordinata],SECOND_VALUE[koordinata_x]);}
static void 내보내기(const char*fajl_unos,...){if(odjel_za_informacijske_tehnologije_nevažeće)return;va_list argument_niz;va_start(argument_niz,fajl_unos);int stavka_COUNT=vsnprintf(Tekst+Veličina_teksta,sizeof(Tekst)-Veličina_teksta,fajl_unos,argument_niz);va_end(argument_niz);if(stavka_COUNT<0||(unsigned)stavka_COUNT>=sizeof(Tekst)-Veličina_teksta){odjel_za_informacijske_tehnologije_nevažeće=1;return;}Veličina_teksta+=stavka_COUNT;}
static int 서술자(unsigned identifikator_VALUE,int*mjera){
    if(identifikator_VALUE<1||identifikator_VALUE>=konstanta_ukupan_broj||Kategorije_spisak[identifikator_VALUE]!=1)return -1;unsigned podaci_položaj=첫째값[identifikator_VALUE],završiti_Pomak=podaci_položaj+SECOND_VALUE[identifikator_VALUE];if(podaci_položaj>=završiti_Pomak||podaci[podaci_položaj++]!='(')return -1;int unos_COUNT=0;
    while(podaci_položaj<završiti_Pomak&&podaci[podaci_položaj]!=')'){
        unsigned kôd_znaka=podaci[podaci_položaj++];while(kôd_znaka=='['&&podaci_položaj<završiti_Pomak)kôd_znaka=podaci[podaci_položaj++];
        if(kôd_znaka=='L'){while(podaci_položaj<završiti_Pomak&&podaci[podaci_položaj]!=';')podaci_položaj++;if(podaci_položaj==završiti_Pomak)return -1;podaci_položaj++;}
        else if(kôd_znaka!='I'&&kôd_znaka!='Z'&&kôd_znaka!='B'&&kôd_znaka!='C'&&kôd_znaka!='S')return -1;
        if(++unos_COUNT>16)return -1;
    }
    if(podaci_položaj+1>=završiti_Pomak||podaci[podaci_položaj++]!=')')return -1;*mjera=podaci[podaci_položaj]=='V'?0:1;
    if(podaci[podaci_položaj]=='J'||podaci[podaci_položaj]=='D'||podaci[podaci_položaj]=='F')return -1;return unos_COUNT;
}
static void atributi(void){unsigned stavka_COUNT=절반값();for(unsigned 순번=0;순번<stavka_COUNT&&!odjel_za_informacijske_tehnologije_nevažeće;순번++){절반값();unsigned Veličina=가득참();TAKE_VALUE(Veličina);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned međuverzija=절반값(),broj_verzije=절반값();if(međuverzija||broj_verzije<45||broj_verzije>52)return -1;
    konstanta_ukupan_broj=절반값();if(konstanta_ukupan_broj<1||konstanta_ukupan_broj>512)return -1;
    for(unsigned 순번=1;순번<konstanta_ukupan_broj&&!odjel_za_informacijske_tehnologije_nevažeće;순번++){
        Kategorije_spisak[순번]=bajt_podaci();switch(Kategorije_spisak[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=konstanta_ukupan_broj)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=bajt_podaci();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();trenutno_klasa=절반값();절반값();if(trenutno_klasa<1||trenutno_klasa>=konstanta_ukupan_broj||Kategorije_spisak[trenutno_klasa]!=7||첫째값[trenutno_klasa]<1||첫째값[trenutno_klasa]>=konstanta_ukupan_broj||Kategorije_spisak[첫째값[trenutno_klasa]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!odjel_za_informacijske_tehnologije_nevažeće;순번++){
        unsigned 설정비트=절반값();naziv_polja[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned unos_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<unos_COUNT&&!odjel_za_informacijske_tehnologije_nevažeće;안쪽순번++){
            unsigned Naziv=절반값(),Veličina=가득참();
            if(UNICODE_VALUE(Naziv,"ConstantValue")){if(Veličina!=2)return -1;polje_konstanta[순번]=절반값();}
            else TAKE_VALUE(Veličina);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!odjel_za_informacijske_tehnologije_nevažeće;순번++){
        metoda_unos*Grupa_podesiti_veličinu=메소드목록+순번;Grupa_podesiti_veličinu->설정비트=절반값();Grupa_podesiti_veličinu->Naziv=절반값();Grupa_podesiti_veličinu->서술값=절반값();unsigned unos_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<unos_COUNT&&!odjel_za_informacijske_tehnologije_nevažeće;안쪽순번++){
            unsigned Naziv=절반값(),Veličina=가득참(),Pokreni=trenutno_položaj;
            if(Veličina>dužina_VALUE-trenutno_položaj)return -1;
            if(UNICODE_VALUE(Naziv,"Code")){
                Grupa_podesiti_veličinu->snop_Pohrana=절반값();Grupa_podesiti_veličinu->지역변수들=절반값();Grupa_podesiti_veličinu->Veličina=가득참();Grupa_podesiti_veličinu->programska_naredba_SEQUENCE=TAKE_VALUE(Grupa_podesiti_veličinu->Veličina);
                if(Grupa_podesiti_veličinu->snop_Pohrana>128||Grupa_podesiti_veličinu->지역변수들>128||Grupa_podesiti_veličinu->Veličina>8192||절반값())return -1;atributi();
            }else TAKE_VALUE(Veličina);
            if(trenutno_položaj!=Pokreni+Veličina)return -1;
        }
        if(!UNICODE_VALUE(Grupa_podesiti_veličinu->Naziv,"<init>")&&(!(Grupa_podesiti_veličinu->설정비트&8)||(Grupa_podesiti_veličinu->설정비트&(0x100|0x20))||!Grupa_podesiti_veličinu->Veličina))return -1;
    }
    atributi();return odjel_za_informacijske_tehnologije_nevažeće||trenutno_položaj!=dužina_VALUE?-1:0;
}
static void konstanta_VALUE(unsigned identifikator_VALUE){
    if(!identifikator_VALUE||identifikator_VALUE>=konstanta_ukupan_broj){odjel_za_informacijske_tehnologije_nevažeće=1;return;}
    if(Kategorije_spisak[identifikator_VALUE]==3)내보내기("P(%uU);",첫째값[identifikator_VALUE]);
    else if(Kategorije_spisak[identifikator_VALUE]==8)내보내기("P((W)k%u);",identifikator_VALUE);else odjel_za_informacijske_tehnologije_nevažeće=1;
}
static void 호출(unsigned identifikator_VALUE,int virtualno_CALL){
    if(identifikator_VALUE<1||identifikator_VALUE>=konstanta_ukupan_broj||(Kategorije_spisak[identifikator_VALUE]!=10&&Kategorije_spisak[identifikator_VALUE]!=11)||첫째값[identifikator_VALUE]<1||첫째값[identifikator_VALUE]>=konstanta_ukupan_broj||Kategorije_spisak[첫째값[identifikator_VALUE]]!=7||SECOND_VALUE[identifikator_VALUE]<1||SECOND_VALUE[identifikator_VALUE]>=konstanta_ukupan_broj||Kategorije_spisak[SECOND_VALUE[identifikator_VALUE]]!=12){odjel_za_informacijske_tehnologije_nevažeće=1;return;}
    unsigned vlasnik_objekt=첫째값[첫째값[identifikator_VALUE]],Naziv=첫째값[SECOND_VALUE[identifikator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikator_VALUE]];int mjera=0,stavka_COUNT=서술자(서술값,&mjera);if(stavka_COUNT<0){odjel_za_informacijske_tehnologije_nevažeće=1;return;}
    for(int 순번=stavka_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtualno_CALL)내보내기("Q();");
    if(!virtualno_CALL&&같음(vlasnik_objekt,첫째값[trenutno_klasa])){
        unsigned Grupa_podesiti_veličinu=0;for(;Grupa_podesiti_veličinu<메소드개수;Grupa_podesiti_veličinu++)if(같음(Naziv,메소드목록[Grupa_podesiti_veličinu].Naziv)&&같음(서술값,메소드목록[Grupa_podesiti_veličinu].서술값))break;
        if(Grupa_podesiti_veličinu==메소드개수||!(메소드목록[Grupa_podesiti_veličinu].설정비트&8)){odjel_za_informacijske_tehnologije_nevažeće=1;return;}
        if(mjera)내보내기("P(");내보내기("m%u(",Grupa_podesiti_veličinu);for(int 순번=0;순번<stavka_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(mjera?"));":" );");return;
    }
    if((virtualno_CALL&&UNICODE_VALUE(vlasnik_objekt,"java/io/PrintStream")&& (UNICODE_VALUE(Naziv,"print")||UNICODE_VALUE(Naziv,"println")))||(!virtualno_CALL&&UNICODE_VALUE(vlasnik_objekt,"한국어/자체/Ispis"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Naziv,"print")||UNICODE_VALUE(Naziv,"println")||UNICODE_VALUE(Naziv,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Naziv,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Naziv,"print")||UNICODE_VALUE(Naziv,"println")||UNICODE_VALUE(Naziv,"Piši")||UNICODE_VALUE(Naziv,"pisati_redak"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Naziv,"print")||UNICODE_VALUE(Naziv,"Piši")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Naziv,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtualno_CALL&&UNICODE_VALUE(vlasnik_objekt,"한국어/자체/Fajl")){
        if(UNICODE_VALUE(Naziv,"Piši")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Naziv,"Čitaj")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    odjel_za_informacijske_tehnologije_nevažeće=1;
}
static void napraviti_metoda(unsigned LOOKUP_INDEX){
    metoda_unos*Grupa_podesiti_veličinu=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(Grupa_podesiti_veličinu->Naziv,"<init>"))return;int mjera,stavka_COUNT=서술자(Grupa_podesiti_veličinu->서술값,&mjera);if(stavka_COUNT<0){odjel_za_informacijske_tehnologije_nevažeće=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<stavka_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!stavka_COUNT)내보내기("void");
    if((unsigned)stavka_COUNT>Grupa_podesiti_veličinu->지역변수들){odjel_za_informacijske_tehnologije_nevažeće=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Grupa_podesiti_veličinu->지역변수들?Grupa_podesiti_veličinu->지역변수들:1);for(int 순번=0;순번<stavka_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=dužina_VALUE;dužina_VALUE=Grupa_podesiti_veličinu->programska_naredba_SEQUENCE+Grupa_podesiti_veličinu->Veličina;trenutno_položaj=Grupa_podesiti_veličinu->programska_naredba_SEQUENCE;
    while(trenutno_položaj<dužina_VALUE&&!odjel_za_informacijske_tehnologije_nevažeće){unsigned komanda_položaj=trenutno_položaj-Grupa_podesiti_veličinu->programska_naredba_SEQUENCE,operacija_VALUE=bajt_podaci();내보내기("L%u:;",komanda_položaj);
        if(operacija_VALUE==0){}
        else if(operacija_VALUE==1)내보내기("P(0);");
        else if(operacija_VALUE>=2&&operacija_VALUE<=8)내보내기("P(%uU);",operacija_VALUE-3);
        else if(operacija_VALUE==16){int VALUE=(int8_t)bajt_podaci();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operacija_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operacija_VALUE==18||operacija_VALUE==19)konstanta_VALUE(operacija_VALUE==18?bajt_podaci():절반값());
        else if(operacija_VALUE==21||operacija_VALUE==25){unsigned 순번=bajt_podaci();if(순번>=Grupa_podesiti_veličinu->지역변수들)odjel_za_informacijske_tehnologije_nevažeće=1;내보내기("P(v[%u]);",순번);}
        else if((operacija_VALUE>=26&&operacija_VALUE<=29)||(operacija_VALUE>=42&&operacija_VALUE<=45)){unsigned 순번=operacija_VALUE>=42?operacija_VALUE-42:operacija_VALUE-26;if(순번>=Grupa_podesiti_veličinu->지역변수들)odjel_za_informacijske_tehnologije_nevažeće=1;내보내기("P(v[%u]);",순번);}
        else if(operacija_VALUE==54||operacija_VALUE==58){unsigned 순번=bajt_podaci();if(순번>=Grupa_podesiti_veličinu->지역변수들)odjel_za_informacijske_tehnologije_nevažeće=1;내보내기("v[%u]=Q();",순번);}
        else if((operacija_VALUE>=59&&operacija_VALUE<=62)||(operacija_VALUE>=75&&operacija_VALUE<=78)){unsigned 순번=operacija_VALUE>=75?operacija_VALUE-75:operacija_VALUE-59;if(순번>=Grupa_podesiti_veličinu->지역변수들)odjel_za_informacijske_tehnologije_nevažeće=1;내보내기("v[%u]=Q();",순번);}
        else if(operacija_VALUE==46||operacija_VALUE==50||operacija_VALUE==51||operacija_VALUE==52||operacija_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operacija_VALUE==79||operacija_VALUE==83||operacija_VALUE==84||operacija_VALUE==85||operacija_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operacija_VALUE==84?"(unsigned)(signed char)q":operacija_VALUE==85?"(unsigned short)q":operacija_VALUE==86?"(unsigned)(short)q":"q");
        else if(operacija_VALUE==87)내보내기("Q();");
        else if(operacija_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(operacija_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operacija_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(operacija_VALUE==96||operacija_VALUE==100||operacija_VALUE==104||operacija_VALUE==120||operacija_VALUE==124||operacija_VALUE==126||operacija_VALUE==128||operacija_VALUE==130){const char*kodiranje_VALUE=operacija_VALUE==96?"+":operacija_VALUE==100?"-":operacija_VALUE==104?"*":operacija_VALUE==120?"<<":operacija_VALUE==124?">>":operacija_VALUE==126?"&":operacija_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kodiranje_VALUE,operacija_VALUE==120||operacija_VALUE==124?"%32":"");}
        else if(operacija_VALUE==108||operacija_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operacija_VALUE==112);
        else if(operacija_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(operacija_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operacija_VALUE==132){unsigned 순번=bajt_podaci();int 차이=(int8_t)bajt_podaci();if(순번>=Grupa_podesiti_veličinu->지역변수들)odjel_za_informacijske_tehnologije_nevažeće=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operacija_VALUE>=145&&operacija_VALUE<=147)내보내기("P((unsigned)(%s)Q());",operacija_VALUE==145?"signed char":operacija_VALUE==146?"unsigned short":"short");
        else if(operacija_VALUE>=153&&operacija_VALUE<=166){int cilj=(int)komanda_položaj+(int16_t)절반값();const char*Poređenje_VALUE[]={"==","!=","<",">=",">","<="};if(cilj<0||cilj>=(int)Grupa_podesiti_veličinu->Veličina){odjel_za_informacijske_tehnologije_nevažeće=1;break;}if(operacija_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Poređenje_VALUE[operacija_VALUE-153],cilj);else if(operacija_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Poređenje_VALUE[operacija_VALUE-159],cilj);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operacija_VALUE==165?"==":"!=",cilj);}
        else if(operacija_VALUE==167){int cilj=(int)komanda_položaj+(int16_t)절반값();if(cilj<0||cilj>=(int)Grupa_podesiti_veličinu->Veličina)odjel_za_informacijske_tehnologije_nevažeće=1;내보내기("goto L%d;",cilj);}
        else if(operacija_VALUE==172||operacija_VALUE==176)내보내기("return Q();");else if(operacija_VALUE==177)내보내기("return 0;");
        else if(operacija_VALUE==178||operacija_VALUE==179){unsigned identifikator_VALUE=절반값();if(identifikator_VALUE<1||identifikator_VALUE>=konstanta_ukupan_broj||Kategorije_spisak[identifikator_VALUE]!=9||첫째값[identifikator_VALUE]>=konstanta_ukupan_broj||SECOND_VALUE[identifikator_VALUE]>=konstanta_ukupan_broj||Kategorije_spisak[첫째값[identifikator_VALUE]]!=7||Kategorije_spisak[SECOND_VALUE[identifikator_VALUE]]!=12){odjel_za_informacijske_tehnologije_nevažeće=1;break;}unsigned vlasnik_objekt=첫째값[첫째값[identifikator_VALUE]],Naziv=첫째값[SECOND_VALUE[identifikator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikator_VALUE]];
            if(operacija_VALUE==178&&UNICODE_VALUE(vlasnik_objekt,"java/lang/System")&&UNICODE_VALUE(Naziv,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned fajl_unos=0;while(fajl_unos<필드개수&&(!같음(Naziv,naziv_polja[fajl_unos])||!같음(서술값,필드서술[fajl_unos])))fajl_unos++;if(!같음(vlasnik_objekt,첫째값[trenutno_klasa])||fajl_unos==필드개수){odjel_za_informacijske_tehnologije_nevažeće=1;break;}내보내기(operacija_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",fajl_unos);}}
        else if(operacija_VALUE==182||operacija_VALUE==184)호출(절반값(),operacija_VALUE==182);
        else if(operacija_VALUE==188){unsigned TYPE_oblast=bajt_podaci();if(TYPE_oblast!=4&&TYPE_oblast!=5&&TYPE_oblast!=8&&TYPE_oblast!=9&&TYPE_oblast!=10)odjel_za_informacijske_tehnologije_nevažeće=1;내보내기("P(jarray((int)Q()));");}
        else if(operacija_VALUE==190)내보내기("P(jlength(Q()));");
        else if(operacija_VALUE==198||operacija_VALUE==199){int cilj=(int)komanda_položaj+(int16_t)절반값();if(cilj<0||cilj>=(int)Grupa_podesiti_veličinu->Veličina)odjel_za_informacijske_tehnologije_nevažeće=1;내보내기("if(Q()%s0)goto L%d;",operacija_VALUE==198?"==":"!=",cilj);}
        else odjel_za_informacijske_tehnologije_nevažeće=1;
        if(odjel_za_informacijske_tehnologije_nevažeće)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,operacija_VALUE,komanda_položaj);
        내보내기("\n");
    }
    dužina_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned string_lekcija(unsigned *podaci_položaj,unsigned završiti_Pomak){
    if(*podaci_položaj>=završiti_Pomak){odjel_za_informacijske_tehnologije_nevažeće=1;return 0;}unsigned kôd_znaka=podaci[(*podaci_položaj)++];
    if(kôd_znaka<128)return kôd_znaka;
    unsigned stavka_COUNT=kôd_znaka>=0xc0&&kôd_znaka<=0xdf?1:kôd_znaka>=0xe0&&kôd_znaka<=0xef?2:3;
    if(stavka_COUNT==3||stavka_COUNT>završiti_Pomak-*podaci_položaj){odjel_za_informacijske_tehnologije_nevažeće=1;return 0;}unsigned VALUE=kôd_znaka&((1u<<(6-stavka_COUNT))-1);
    for(unsigned 순번=0;순번<stavka_COUNT;순번++){unsigned Dalje_stavka=podaci[(*podaci_položaj)++];if((Dalje_stavka&0xc0)!=0x80)odjel_za_informacijske_tehnologije_nevažeće=1;VALUE=VALUE<<6|(Dalje_stavka&63);}
    if((stavka_COUNT==1&&VALUE<128&&VALUE!=0)||(stavka_COUNT==2&&VALUE<2048))odjel_za_informacijske_tehnologije_nevažeće=1;return VALUE;
}
static void string_konstanta(unsigned identifikator_VALUE){
    unsigned 부호없는값=첫째값[identifikator_VALUE];if(부호없는값<1||부호없는값>=konstanta_ukupan_broj||Kategorije_spisak[부호없는값]!=1){odjel_za_informacijske_tehnologije_nevažeće=1;return;}내보내기("static const unsigned char k%u[]={",identifikator_VALUE);
    unsigned podaci_položaj=첫째값[부호없는값],završiti_Pomak=podaci_položaj+SECOND_VALUE[부호없는값];
    while(podaci_položaj<završiti_Pomak&&!odjel_za_informacijske_tehnologije_nevažeće){unsigned kôd_znaka=string_lekcija(&podaci_položaj,završiti_Pomak);
        if(kôd_znaka>=0xd800&&kôd_znaka<=0xdbff){unsigned 낮은부분=string_lekcija(&podaci_položaj,završiti_Pomak);if(낮은부분<0xdc00||낮은부분>0xdfff){odjel_za_informacijske_tehnologije_nevažeće=1;break;}kôd_znaka=0x10000+((kôd_znaka-0xd800)<<10)+낮은부분-0xdc00;}
        else if(kôd_znaka>=0xdc00&&kôd_znaka<=0xdfff){odjel_za_informacijske_tehnologije_nevažeće=1;break;}
        if(!kôd_znaka){printf("jaot: embedded NUL string needs JVM mode\n");odjel_za_informacijske_tehnologije_nevažeće=1;break;}
        if(kôd_znaka<128)내보내기("%u,",kôd_znaka);
        else{unsigned stavka_COUNT=kôd_znaka<2048?2:kôd_znaka<65536?3:4;내보내기("%u,",(stavka_COUNT==2?0xc0:stavka_COUNT==3?0xe0:0xf0)|(kôd_znaka>>(6*(stavka_COUNT-1))));for(unsigned 순번=stavka_COUNT-1;순번;순번--)내보내기("%u,",0x80|((kôd_znaka>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Naziv){
    size_t stavka_COUNT=strlen(Naziv);
    if(stavka_COUNT>4&&!strcmp(Naziv+stavka_COUNT-4,".jar")){
        if(꾸러미열기(Naziv)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Putanja[256];const char*unos_metoda=꾸러미진입클래스();stavka_COUNT=strlen(unos_metoda);if(stavka_COUNT+6>=sizeof(Putanja))return 0;
        for(unsigned 순번=0;순번<stavka_COUNT;순번++)Putanja[순번]=unos_metoda[순번]=='.'?'/':unos_metoda[순번];strcpy(Putanja+stavka_COUNT,".class");int unos_COUNT=꾸러미읽기(Putanja,podaci,sizeof(podaci));if(unos_COUNT<0)return 0;dužina_VALUE=unos_COUNT;
    }else{intptr_t fajl_hvatište=사용자호출(3,(uintptr_t)Naziv,0,0,0,0,0);if(fajl_hvatište<0)return 0;intptr_t unos_COUNT=사용자호출(9,fajl_hvatište,0,0,0,0,0);if(unos_COUNT<0||unos_COUNT>sizeof(podaci)){사용자호출(4,fajl_hvatište,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,fajl_hvatište,(uintptr_t)podaci,unos_COUNT,0,0,0);사용자호출(4,fajl_hvatište,0,0,0,0,0);if(RECEIVED_COUNT!=unos_COUNT)return 0;dužina_VALUE=unos_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstanta_ukupan_broj&&!odjel_za_informacijske_tehnologije_nevažeće;순번++)if(Kategorije_spisak[순번]==8)string_konstanta(순번);
    if(odjel_za_informacijske_tehnologije_nevažeće)return 0;
    int unos_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Naziv,"<init>")){
        int mjera,unos_COUNT=서술자(메소드목록[순번].서술값,&mjera);if(unos_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<unos_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!unos_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Naziv,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)unos_p=순번;
        if(UNICODE_VALUE(메소드목록[순번].Naziv,"<clinit>"))초기값=순번;
    }
    if(unos_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!odjel_za_informacijske_tehnologije_nevažeće;순번++)napraviti_metoda(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(polje_konstanta[순번]){
        unsigned kôd_znaka=polje_konstanta[순번];if(kôd_znaka>=konstanta_ukupan_broj)return 0;
        if(Kategorije_spisak[kôd_znaka]==3)내보내기("fields[%u]=%uU;",순번,첫째값[kôd_znaka]);else if(Kategorije_spisak[kôd_znaka]==8)내보내기("fields[%u]=(W)k%u;",순번,kôd_znaka);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",unos_p);
    return odjel_za_informacijske_tehnologije_nevažeće?0:Tekst;
}
