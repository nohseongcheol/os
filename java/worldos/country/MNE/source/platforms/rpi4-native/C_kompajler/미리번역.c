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
static unsigned char podaci[16384];static unsigned 길이,aktuelno_pozicija;static int informatičko_odeljenje_nevažeći;
static unsigned Kategorije_Lista[512],첫째값[512],SECOND_VALUE[512],konstanta_ukupan_broj,aktuelno_Razred;
static char SMS[65536];static unsigned Veličina_teksta;
typedef struct {unsigned konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini,ime,서술값,명령열,promeniti_veličinu,지역변수들,stek_Skladište;} metod_stavka;
static metod_stavka 메소드목록[64];static unsigned 메소드개수;
static unsigned ime_polja[64],필드서술[64],polje_konstanta[64],필드개수;
static unsigned TAKE_VALUE(unsigned stavka_COUNT){if(aktuelno_pozicija>길이||stavka_COUNT>길이-aktuelno_pozicija){informatičko_odeljenje_nevažeći=1;return 0;}unsigned podaci_pozicija=aktuelno_pozicija;aktuelno_pozicija+=stavka_COUNT;return podaci_pozicija;}
static unsigned bajt_podaci(void){unsigned podaci_pozicija=TAKE_VALUE(1);return informatičko_odeljenje_nevažeći?0:podaci[podaci_pozicija];}
static unsigned 절반값(void){unsigned x_koordinata=bajt_podaci();return x_koordinata<<8|bajt_podaci();}
static uint32_t 가득참(void){uint32_t x_koordinata=절반값();return x_koordinata<<16|절반값();}
static int Unikod_VALUE(unsigned 순번,const char*niska_podaci){return 순번>0&&순번<konstanta_ukupan_broj&&Kategorije_Lista[순번]==1&&strlen(niska_podaci)==SECOND_VALUE[순번]&&!memcmp(podaci+첫째값[순번],niska_podaci,SECOND_VALUE[순번]);}
static int 같음(unsigned x_koordinata,unsigned 세로좌표){return x_koordinata>0&&x_koordinata<konstanta_ukupan_broj&&세로좌표>0&&세로좌표<konstanta_ukupan_broj&&Kategorije_Lista[x_koordinata]==1&&Kategorije_Lista[세로좌표]==1&&SECOND_VALUE[x_koordinata]==SECOND_VALUE[세로좌표]&&!memcmp(podaci+첫째값[x_koordinata],podaci+첫째값[세로좌표],SECOND_VALUE[x_koordinata]);}
static void 내보내기(const char*Datoteka_stavka,...){if(informatičko_odeljenje_nevažeći)return;va_list argument_niz;va_start(argument_niz,Datoteka_stavka);int stavka_COUNT=vsnprintf(SMS+Veličina_teksta,sizeof(SMS)-Veličina_teksta,Datoteka_stavka,argument_niz);va_end(argument_niz);if(stavka_COUNT<0||(unsigned)stavka_COUNT>=sizeof(SMS)-Veličina_teksta){informatičko_odeljenje_nevažeći=1;return;}Veličina_teksta+=stavka_COUNT;}
static int 서술자(unsigned identifikator_VALUE,int*KR){
    if(identifikator_VALUE<1||identifikator_VALUE>=konstanta_ukupan_broj||Kategorije_Lista[identifikator_VALUE]!=1)return -1;unsigned podaci_pozicija=첫째값[identifikator_VALUE],završiti_razgovor_Pomak=podaci_pozicija+SECOND_VALUE[identifikator_VALUE];if(podaci_pozicija>=završiti_razgovor_Pomak||podaci[podaci_pozicija++]!='(')return -1;int stavka_COUNT_8f7753a1=0;
    while(podaci_pozicija<završiti_razgovor_Pomak&&podaci[podaci_pozicija]!=')'){
        unsigned kôd_znaka=podaci[podaci_pozicija++];while(kôd_znaka=='['&&podaci_pozicija<završiti_razgovor_Pomak)kôd_znaka=podaci[podaci_pozicija++];
        if(kôd_znaka=='L'){while(podaci_pozicija<završiti_razgovor_Pomak&&podaci[podaci_pozicija]!=';')podaci_pozicija++;if(podaci_pozicija==završiti_razgovor_Pomak)return -1;podaci_pozicija++;}
        else if(kôd_znaka!='I'&&kôd_znaka!='Z'&&kôd_znaka!='B'&&kôd_znaka!='C'&&kôd_znaka!='S')return -1;
        if(++stavka_COUNT_8f7753a1>16)return -1;
    }
    if(podaci_pozicija+1>=završiti_razgovor_Pomak||podaci[podaci_pozicija++]!=')')return -1;*KR=podaci[podaci_pozicija]=='V'?0:1;
    if(podaci[podaci_pozicija]=='J'||podaci[podaci_pozicija]=='D'||podaci[podaci_pozicija]=='F')return -1;return stavka_COUNT_8f7753a1;
}
static void karakteristike(void){unsigned stavka_COUNT=절반값();for(unsigned 순번=0;순번<stavka_COUNT&&!informatičko_odeljenje_nevažeći;순번++){절반값();unsigned promeniti_veličinu=가득참();TAKE_VALUE(promeniti_veličinu);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned međuverzija=절반값(),broj_verzije=절반값();if(međuverzija||broj_verzije<45||broj_verzije>52)return -1;
    konstanta_ukupan_broj=절반값();if(konstanta_ukupan_broj<1||konstanta_ukupan_broj>512)return -1;
    for(unsigned 순번=1;순번<konstanta_ukupan_broj&&!informatičko_odeljenje_nevažeći;순번++){
        Kategorije_Lista[순번]=bajt_podaci();switch(Kategorije_Lista[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=konstanta_ukupan_broj)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=bajt_podaci();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();aktuelno_Razred=절반값();절반값();if(aktuelno_Razred<1||aktuelno_Razred>=konstanta_ukupan_broj||Kategorije_Lista[aktuelno_Razred]!=7||첫째값[aktuelno_Razred]<1||첫째값[aktuelno_Razred]>=konstanta_ukupan_broj||Kategorije_Lista[첫째값[aktuelno_Razred]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!informatičko_odeljenje_nevažeći;순번++){
        unsigned konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini=절반값();ime_polja[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini&8))return -1;
        unsigned stavka_COUNT_8f7753a1=절반값();for(unsigned 안쪽순번=0;안쪽순번<stavka_COUNT_8f7753a1&&!informatičko_odeljenje_nevažeći;안쪽순번++){
            unsigned ime=절반값(),promeniti_veličinu=가득참();
            if(Unikod_VALUE(ime,"ConstantValue")){if(promeniti_veličinu!=2)return -1;polje_konstanta[순번]=절반값();}
            else TAKE_VALUE(promeniti_veličinu);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!informatičko_odeljenje_nevažeći;순번++){
        metod_stavka*Grupa_promeniti_veličinu=메소드목록+순번;Grupa_promeniti_veličinu->konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini=절반값();Grupa_promeniti_veličinu->ime=절반값();Grupa_promeniti_veličinu->서술값=절반값();unsigned stavka_COUNT_8f7753a1=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<stavka_COUNT_8f7753a1&&!informatičko_odeljenje_nevažeći;안쪽순번++){
            unsigned ime=절반값(),promeniti_veličinu=가득참(),koristiti=aktuelno_pozicija;
            if(promeniti_veličinu>길이-aktuelno_pozicija)return -1;
            if(Unikod_VALUE(ime,"Code")){
                Grupa_promeniti_veličinu->stek_Skladište=절반값();Grupa_promeniti_veličinu->지역변수들=절반값();Grupa_promeniti_veličinu->promeniti_veličinu=가득참();Grupa_promeniti_veličinu->명령열=TAKE_VALUE(Grupa_promeniti_veličinu->promeniti_veličinu);
                if(Grupa_promeniti_veličinu->stek_Skladište>128||Grupa_promeniti_veličinu->지역변수들>128||Grupa_promeniti_veličinu->promeniti_veličinu>8192||절반값())return -1;karakteristike();
            }else TAKE_VALUE(promeniti_veličinu);
            if(aktuelno_pozicija!=koristiti+promeniti_veličinu)return -1;
        }
        if(!Unikod_VALUE(Grupa_promeniti_veličinu->ime,"<init>")&&(!(Grupa_promeniti_veličinu->konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini&8)||(Grupa_promeniti_veličinu->konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini&(0x100|0x20))||!Grupa_promeniti_veličinu->promeniti_veličinu))return -1;
    }
    karakteristike();return informatičko_odeljenje_nevažeći||aktuelno_pozicija!=길이?-1:0;
}
static void konstanta_VALUE(unsigned identifikator_VALUE){
    if(!identifikator_VALUE||identifikator_VALUE>=konstanta_ukupan_broj){informatičko_odeljenje_nevažeći=1;return;}
    if(Kategorije_Lista[identifikator_VALUE]==3)내보내기("P(%uU);",첫째값[identifikator_VALUE]);
    else if(Kategorije_Lista[identifikator_VALUE]==8)내보내기("P((W)k%u);",identifikator_VALUE);else informatičko_odeljenje_nevažeći=1;
}
static void 호출(unsigned identifikator_VALUE,int 가상호출){
    if(identifikator_VALUE<1||identifikator_VALUE>=konstanta_ukupan_broj||(Kategorije_Lista[identifikator_VALUE]!=10&&Kategorije_Lista[identifikator_VALUE]!=11)||첫째값[identifikator_VALUE]<1||첫째값[identifikator_VALUE]>=konstanta_ukupan_broj||Kategorije_Lista[첫째값[identifikator_VALUE]]!=7||SECOND_VALUE[identifikator_VALUE]<1||SECOND_VALUE[identifikator_VALUE]>=konstanta_ukupan_broj||Kategorije_Lista[SECOND_VALUE[identifikator_VALUE]]!=12){informatičko_odeljenje_nevažeći=1;return;}
    unsigned vlasnik_objekat=첫째값[첫째값[identifikator_VALUE]],ime=첫째값[SECOND_VALUE[identifikator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikator_VALUE]];int KR=0,stavka_COUNT=서술자(서술값,&KR);if(stavka_COUNT<0){informatičko_odeljenje_nevažeći=1;return;}
    for(int 순번=stavka_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(가상호출)내보내기("Q();");
    if(!가상호출&&같음(vlasnik_objekat,첫째값[aktuelno_Razred])){
        unsigned Grupa_promeniti_veličinu=0;for(;Grupa_promeniti_veličinu<메소드개수;Grupa_promeniti_veličinu++)if(같음(ime,메소드목록[Grupa_promeniti_veličinu].ime)&&같음(서술값,메소드목록[Grupa_promeniti_veličinu].서술값))break;
        if(Grupa_promeniti_veličinu==메소드개수||!(메소드목록[Grupa_promeniti_veličinu].konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini&8)){informatičko_odeljenje_nevažeći=1;return;}
        if(KR)내보내기("P(");내보내기("m%u(",Grupa_promeniti_veličinu);for(int 순번=0;순번<stavka_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(KR?"));":" );");return;
    }
    if((가상호출&&Unikod_VALUE(vlasnik_objekat,"java/io/PrintStream")&& (Unikod_VALUE(ime,"print")||Unikod_VALUE(ime,"println")))||(!가상호출&&Unikod_VALUE(vlasnik_objekat,"한국어/자체/출력"))){
        if(Unikod_VALUE(서술값,"(I)V")&&(Unikod_VALUE(ime,"print")||Unikod_VALUE(ime,"println")||Unikod_VALUE(ime,"수쓰기"))){내보내기("jprint(x[0],1,%d);",Unikod_VALUE(ime,"print")?0:1);return;}
        if(Unikod_VALUE(서술값,"(Ljava/lang/String;)V")&&(Unikod_VALUE(ime,"print")||Unikod_VALUE(ime,"println")||Unikod_VALUE(ime,"쓰기")||Unikod_VALUE(ime,"줄쓰기"))){내보내기("jprint(x[0],0,%d);",Unikod_VALUE(ime,"print")||Unikod_VALUE(ime,"쓰기")?0:1);return;}
        if(Unikod_VALUE(서술값,"()V")&&Unikod_VALUE(ime,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!가상호출&&Unikod_VALUE(vlasnik_objekat,"한국어/자체/Datoteka")){
        if(Unikod_VALUE(ime,"쓰기")&&Unikod_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(Unikod_VALUE(ime,"읽기")&&Unikod_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    informatičko_odeljenje_nevažeći=1;
}
static void kompajlirati_metod(unsigned LOOKUP_INDEX){
    metod_stavka*Grupa_promeniti_veličinu=메소드목록+LOOKUP_INDEX;if(Unikod_VALUE(Grupa_promeniti_veličinu->ime,"<init>"))return;int KR,stavka_COUNT=서술자(Grupa_promeniti_veličinu->서술값,&KR);if(stavka_COUNT<0){informatičko_odeljenje_nevažeći=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<stavka_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!stavka_COUNT)내보내기("void");
    if((unsigned)stavka_COUNT>Grupa_promeniti_veličinu->지역변수들){informatičko_odeljenje_nevažeći=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Grupa_promeniti_veličinu->지역변수들?Grupa_promeniti_veličinu->지역변수들:1);for(int 순번=0;순번<stavka_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=길이;길이=Grupa_promeniti_veličinu->명령열+Grupa_promeniti_veličinu->promeniti_veličinu;aktuelno_pozicija=Grupa_promeniti_veličinu->명령열;
    while(aktuelno_pozicija<길이&&!informatičko_odeljenje_nevažeći){unsigned komanda_pozicija=aktuelno_pozicija-Grupa_promeniti_veličinu->명령열,operacija_VALUE=bajt_podaci();내보내기("L%u:;",komanda_pozicija);
        if(operacija_VALUE==0){}
        else if(operacija_VALUE==1)내보내기("P(0);");
        else if(operacija_VALUE>=2&&operacija_VALUE<=8)내보내기("P(%uU);",operacija_VALUE-3);
        else if(operacija_VALUE==16){int VALUE=(int8_t)bajt_podaci();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operacija_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operacija_VALUE==18||operacija_VALUE==19)konstanta_VALUE(operacija_VALUE==18?bajt_podaci():절반값());
        else if(operacija_VALUE==21||operacija_VALUE==25){unsigned 순번=bajt_podaci();if(순번>=Grupa_promeniti_veličinu->지역변수들)informatičko_odeljenje_nevažeći=1;내보내기("P(v[%u]);",순번);}
        else if((operacija_VALUE>=26&&operacija_VALUE<=29)||(operacija_VALUE>=42&&operacija_VALUE<=45)){unsigned 순번=operacija_VALUE>=42?operacija_VALUE-42:operacija_VALUE-26;if(순번>=Grupa_promeniti_veličinu->지역변수들)informatičko_odeljenje_nevažeći=1;내보내기("P(v[%u]);",순번);}
        else if(operacija_VALUE==54||operacija_VALUE==58){unsigned 순번=bajt_podaci();if(순번>=Grupa_promeniti_veličinu->지역변수들)informatičko_odeljenje_nevažeći=1;내보내기("v[%u]=Q();",순번);}
        else if((operacija_VALUE>=59&&operacija_VALUE<=62)||(operacija_VALUE>=75&&operacija_VALUE<=78)){unsigned 순번=operacija_VALUE>=75?operacija_VALUE-75:operacija_VALUE-59;if(순번>=Grupa_promeniti_veličinu->지역변수들)informatičko_odeljenje_nevažeći=1;내보내기("v[%u]=Q();",순번);}
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
        else if(operacija_VALUE==132){unsigned 순번=bajt_podaci();int 차이=(int8_t)bajt_podaci();if(순번>=Grupa_promeniti_veličinu->지역변수들)informatičko_odeljenje_nevažeći=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operacija_VALUE>=145&&operacija_VALUE<=147)내보내기("P((unsigned)(%s)Q());",operacija_VALUE==145?"signed char":operacija_VALUE==146?"unsigned short":"short");
        else if(operacija_VALUE>=153&&operacija_VALUE<=166){int cilj=(int)komanda_pozicija+(int16_t)절반값();const char*Poređenje_VALUE[]={"==","!=","<",">=",">","<="};if(cilj<0||cilj>=(int)Grupa_promeniti_veličinu->promeniti_veličinu){informatičko_odeljenje_nevažeći=1;break;}if(operacija_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Poređenje_VALUE[operacija_VALUE-153],cilj);else if(operacija_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Poređenje_VALUE[operacija_VALUE-159],cilj);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operacija_VALUE==165?"==":"!=",cilj);}
        else if(operacija_VALUE==167){int cilj=(int)komanda_pozicija+(int16_t)절반값();if(cilj<0||cilj>=(int)Grupa_promeniti_veličinu->promeniti_veličinu)informatičko_odeljenje_nevažeći=1;내보내기("goto L%d;",cilj);}
        else if(operacija_VALUE==172||operacija_VALUE==176)내보내기("return Q();");else if(operacija_VALUE==177)내보내기("return 0;");
        else if(operacija_VALUE==178||operacija_VALUE==179){unsigned identifikator_VALUE=절반값();if(identifikator_VALUE<1||identifikator_VALUE>=konstanta_ukupan_broj||Kategorije_Lista[identifikator_VALUE]!=9||첫째값[identifikator_VALUE]>=konstanta_ukupan_broj||SECOND_VALUE[identifikator_VALUE]>=konstanta_ukupan_broj||Kategorije_Lista[첫째값[identifikator_VALUE]]!=7||Kategorije_Lista[SECOND_VALUE[identifikator_VALUE]]!=12){informatičko_odeljenje_nevažeći=1;break;}unsigned vlasnik_objekat=첫째값[첫째값[identifikator_VALUE]],ime=첫째값[SECOND_VALUE[identifikator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikator_VALUE]];
            if(operacija_VALUE==178&&Unikod_VALUE(vlasnik_objekat,"java/lang/System")&&Unikod_VALUE(ime,"out")&&Unikod_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Datoteka_stavka=0;while(Datoteka_stavka<필드개수&&(!같음(ime,ime_polja[Datoteka_stavka])||!같음(서술값,필드서술[Datoteka_stavka])))Datoteka_stavka++;if(!같음(vlasnik_objekat,첫째값[aktuelno_Razred])||Datoteka_stavka==필드개수){informatičko_odeljenje_nevažeći=1;break;}내보내기(operacija_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",Datoteka_stavka);}}
        else if(operacija_VALUE==182||operacija_VALUE==184)호출(절반값(),operacija_VALUE==182);
        else if(operacija_VALUE==188){unsigned tip_oblast=bajt_podaci();if(tip_oblast!=4&&tip_oblast!=5&&tip_oblast!=8&&tip_oblast!=9&&tip_oblast!=10)informatičko_odeljenje_nevažeći=1;내보내기("P(jarray((int)Q()));");}
        else if(operacija_VALUE==190)내보내기("P(jlength(Q()));");
        else if(operacija_VALUE==198||operacija_VALUE==199){int cilj=(int)komanda_pozicija+(int16_t)절반값();if(cilj<0||cilj>=(int)Grupa_promeniti_veličinu->promeniti_veličinu)informatičko_odeljenje_nevažeći=1;내보내기("if(Q()%s0)goto L%d;",operacija_VALUE==198?"==":"!=",cilj);}
        else informatičko_odeljenje_nevažeći=1;
        if(informatičko_odeljenje_nevažeći)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,operacija_VALUE,komanda_pozicija);
        내보내기("\n");
    }
    길이=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned niska_lekcija(unsigned *podaci_pozicija,unsigned završiti_razgovor_Pomak){
    if(*podaci_pozicija>=završiti_razgovor_Pomak){informatičko_odeljenje_nevažeći=1;return 0;}unsigned kôd_znaka=podaci[(*podaci_pozicija)++];
    if(kôd_znaka<128)return kôd_znaka;
    unsigned stavka_COUNT=kôd_znaka>=0xc0&&kôd_znaka<=0xdf?1:kôd_znaka>=0xe0&&kôd_znaka<=0xef?2:3;
    if(stavka_COUNT==3||stavka_COUNT>završiti_razgovor_Pomak-*podaci_pozicija){informatičko_odeljenje_nevažeći=1;return 0;}unsigned VALUE=kôd_znaka&((1u<<(6-stavka_COUNT))-1);
    for(unsigned 순번=0;순번<stavka_COUNT;순번++){unsigned Dalje_stavka=podaci[(*podaci_pozicija)++];if((Dalje_stavka&0xc0)!=0x80)informatičko_odeljenje_nevažeći=1;VALUE=VALUE<<6|(Dalje_stavka&63);}
    if((stavka_COUNT==1&&VALUE<128&&VALUE!=0)||(stavka_COUNT==2&&VALUE<2048))informatičko_odeljenje_nevažeći=1;return VALUE;
}
static void niska_konstanta(unsigned identifikator_VALUE){
    unsigned 부호없는값=첫째값[identifikator_VALUE];if(부호없는값<1||부호없는값>=konstanta_ukupan_broj||Kategorije_Lista[부호없는값]!=1){informatičko_odeljenje_nevažeći=1;return;}내보내기("static const unsigned char k%u[]={",identifikator_VALUE);
    unsigned podaci_pozicija=첫째값[부호없는값],završiti_razgovor_Pomak=podaci_pozicija+SECOND_VALUE[부호없는값];
    while(podaci_pozicija<završiti_razgovor_Pomak&&!informatičko_odeljenje_nevažeći){unsigned kôd_znaka=niska_lekcija(&podaci_pozicija,završiti_razgovor_Pomak);
        if(kôd_znaka>=0xd800&&kôd_znaka<=0xdbff){unsigned 낮은부분=niska_lekcija(&podaci_pozicija,završiti_razgovor_Pomak);if(낮은부분<0xdc00||낮은부분>0xdfff){informatičko_odeljenje_nevažeći=1;break;}kôd_znaka=0x10000+((kôd_znaka-0xd800)<<10)+낮은부분-0xdc00;}
        else if(kôd_znaka>=0xdc00&&kôd_znaka<=0xdfff){informatičko_odeljenje_nevažeći=1;break;}
        if(!kôd_znaka){printf("jaot: embedded NUL string needs JVM mode\n");informatičko_odeljenje_nevažeći=1;break;}
        if(kôd_znaka<128)내보내기("%u,",kôd_znaka);
        else{unsigned stavka_COUNT=kôd_znaka<2048?2:kôd_znaka<65536?3:4;내보내기("%u,",(stavka_COUNT==2?0xc0:stavka_COUNT==3?0xe0:0xf0)|(kôd_znaka>>(6*(stavka_COUNT-1))));for(unsigned 순번=stavka_COUNT-1;순번;순번--)내보내기("%u,",0x80|((kôd_znaka>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*ime){
    size_t stavka_COUNT=strlen(ime);
    if(stavka_COUNT>4&&!strcmp(ime+stavka_COUNT-4,".jar")){
        if(꾸러미열기(ime)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char putanja[256];const char*stavka_metod=꾸러미진입클래스();stavka_COUNT=strlen(stavka_metod);if(stavka_COUNT+6>=sizeof(putanja))return 0;
        for(unsigned 순번=0;순번<stavka_COUNT;순번++)putanja[순번]=stavka_metod[순번]=='.'?'/':stavka_metod[순번];strcpy(putanja+stavka_COUNT,".class");int stavka_COUNT_8f7753a1=꾸러미읽기(putanja,podaci,sizeof(podaci));if(stavka_COUNT_8f7753a1<0)return 0;길이=stavka_COUNT_8f7753a1;
    }else{intptr_t Datoteka_pokazivač=사용자호출(3,(uintptr_t)ime,0,0,0,0,0);if(Datoteka_pokazivač<0)return 0;intptr_t stavka_COUNT_8f7753a1=사용자호출(9,Datoteka_pokazivač,0,0,0,0,0);if(stavka_COUNT_8f7753a1<0||stavka_COUNT_8f7753a1>sizeof(podaci)){사용자호출(4,Datoteka_pokazivač,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,Datoteka_pokazivač,(uintptr_t)podaci,stavka_COUNT_8f7753a1,0,0,0);사용자호출(4,Datoteka_pokazivač,0,0,0,0,0);if(RECEIVED_COUNT!=stavka_COUNT_8f7753a1)return 0;길이=stavka_COUNT_8f7753a1;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstanta_ukupan_broj&&!informatičko_odeljenje_nevažeći;순번++)if(Kategorije_Lista[순번]==8)niska_konstanta(순번);
    if(informatičko_odeljenje_nevažeći)return 0;
    int stavka_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!Unikod_VALUE(메소드목록[순번].ime,"<init>")){
        int KR,stavka_COUNT_8f7753a1=서술자(메소드목록[순번].서술값,&KR);if(stavka_COUNT_8f7753a1<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<stavka_COUNT_8f7753a1;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!stavka_COUNT_8f7753a1)내보내기("void");내보내기(");\n");
        if(Unikod_VALUE(메소드목록[순번].ime,"main")&&Unikod_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini&9)==9)stavka_p=순번;
        if(Unikod_VALUE(메소드목록[순번].ime,"<clinit>"))초기값=순번;
    }
    if(stavka_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!informatičko_odeljenje_nevažeći;순번++)kompajlirati_metod(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(polje_konstanta[순번]){
        unsigned kôd_znaka=polje_konstanta[순번];if(kôd_znaka>=konstanta_ukupan_broj)return 0;
        if(Kategorije_Lista[kôd_znaka]==3)내보내기("fields[%u]=%uU;",순번,첫째값[kôd_znaka]);else if(Kategorije_Lista[kôd_znaka]==8)내보내기("fields[%u]=(W)k%u;",순번,kôd_znaka);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",stavka_p);
    return informatičko_odeljenje_nevažeći?0:SMS;
}
