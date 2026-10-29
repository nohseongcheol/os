#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "saistīt.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char dati[16384];static unsigned 길이,pašreizējais_amats;static int informācijas_tehnoloģija_nederīgs;
static unsigned atzīmes_Saraksts[512],첫째값[512],SECOND_VALUE[512],konstante_kopa,pašreizējais_klase;
static char Teksts[65536];static unsigned teksta_lielums;
typedef struct {unsigned konfigurācija_Background_Intelligent_Transfer_Service,Nosaukums,서술값,명령열,Izmērs,지역변수들,kopa_Krātuve;} metode_ievade;
static metode_ievade 메소드목록[64];static unsigned 메소드개수;
static unsigned lauka_nosaukums[64],필드서술[64],lauks_konstante[64],필드개수;
static unsigned TAKE_VALUE(unsigned krājums_COUNT){if(pašreizējais_amats>길이||krājums_COUNT>길이-pašreizējais_amats){informācijas_tehnoloģija_nederīgs=1;return 0;}unsigned dati_amats=pašreizējais_amats;pašreizējais_amats+=krājums_COUNT;return dati_amats;}
static unsigned byte_dati(void){unsigned dati_amats=TAKE_VALUE(1);return informācijas_tehnoloģija_nederīgs?0:dati[dati_amats];}
static unsigned 절반값(void){unsigned x_koordināta=byte_dati();return x_koordināta<<8|byte_dati();}
static uint32_t 가득참(void){uint32_t x_koordināta=절반값();return x_koordināta<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*virkne_dati){return 순번>0&&순번<konstante_kopa&&atzīmes_Saraksts[순번]==1&&strlen(virkne_dati)==SECOND_VALUE[순번]&&!memcmp(dati+첫째값[순번],virkne_dati,SECOND_VALUE[순번]);}
static int 같음(unsigned x_koordināta,unsigned 세로좌표){return x_koordināta>0&&x_koordināta<konstante_kopa&&세로좌표>0&&세로좌표<konstante_kopa&&atzīmes_Saraksts[x_koordināta]==1&&atzīmes_Saraksts[세로좌표]==1&&SECOND_VALUE[x_koordināta]==SECOND_VALUE[세로좌표]&&!memcmp(dati+첫째값[x_koordināta],dati+첫째값[세로좌표],SECOND_VALUE[x_koordināta]);}
static void 내보내기(const char*Fails_ievade,...){if(informācijas_tehnoloģija_nederīgs)return;va_list arg_ARRAY;va_start(arg_ARRAY,Fails_ievade);int krājums_COUNT=vsnprintf(Teksts+teksta_lielums,sizeof(Teksts)-teksta_lielums,Fails_ievade,arg_ARRAY);va_end(arg_ARRAY);if(krājums_COUNT<0||(unsigned)krājums_COUNT>=sizeof(Teksts)-teksta_lielums){informācijas_tehnoloģija_nederīgs=1;return;}teksta_lielums+=krājums_COUNT;}
static int 서술자(unsigned identifikators_VALUE,int*mērs){
    if(identifikators_VALUE<1||identifikators_VALUE>=konstante_kopa||atzīmes_Saraksts[identifikators_VALUE]!=1)return -1;unsigned dati_amats=첫째값[identifikators_VALUE],beigt_zvanu_Nobīde=dati_amats+SECOND_VALUE[identifikators_VALUE];if(dati_amats>=beigt_zvanu_Nobīde||dati[dati_amats++]!='(')return -1;int ievade_COUNT=0;
    while(dati_amats<beigt_zvanu_Nobīde&&dati[dati_amats]!=')'){
        unsigned koda_punkts=dati[dati_amats++];while(koda_punkts=='['&&dati_amats<beigt_zvanu_Nobīde)koda_punkts=dati[dati_amats++];
        if(koda_punkts=='L'){while(dati_amats<beigt_zvanu_Nobīde&&dati[dati_amats]!=';')dati_amats++;if(dati_amats==beigt_zvanu_Nobīde)return -1;dati_amats++;}
        else if(koda_punkts!='I'&&koda_punkts!='Z'&&koda_punkts!='B'&&koda_punkts!='C'&&koda_punkts!='S')return -1;
        if(++ievade_COUNT>16)return -1;
    }
    if(dati_amats+1>=beigt_zvanu_Nobīde||dati[dati_amats++]!=')')return -1;*mērs=dati[dati_amats]=='V'?0:1;
    if(dati[dati_amats]=='J'||dati[dati_amats]=='D'||dati[dati_amats]=='F')return -1;return ievade_COUNT;
}
static void atribūti(void){unsigned krājums_COUNT=절반값();for(unsigned 순번=0;순번<krājums_COUNT&&!informācijas_tehnoloģija_nederīgs;순번++){절반값();unsigned Izmērs=가득참();TAKE_VALUE(Izmērs);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned papildversija=절반값(),versijas_numurs=절반값();if(papildversija||versijas_numurs<45||versijas_numurs>52)return -1;
    konstante_kopa=절반값();if(konstante_kopa<1||konstante_kopa>512)return -1;
    for(unsigned 순번=1;순번<konstante_kopa&&!informācijas_tehnoloģija_nederīgs;순번++){
        atzīmes_Saraksts[순번]=byte_dati();switch(atzīmes_Saraksts[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=konstante_kopa)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=byte_dati();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();pašreizējais_klase=절반값();절반값();if(pašreizējais_klase<1||pašreizējais_klase>=konstante_kopa||atzīmes_Saraksts[pašreizējais_klase]!=7||첫째값[pašreizējais_klase]<1||첫째값[pašreizējais_klase]>=konstante_kopa||atzīmes_Saraksts[첫째값[pašreizējais_klase]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!informācijas_tehnoloģija_nederīgs;순번++){
        unsigned konfigurācija_Background_Intelligent_Transfer_Service=절반값();lauka_nosaukums[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfigurācija_Background_Intelligent_Transfer_Service&8))return -1;
        unsigned ievade_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<ievade_COUNT&&!informācijas_tehnoloģija_nederīgs;안쪽순번++){
            unsigned Nosaukums=절반값(),Izmērs=가득참();
            if(UNICODE_VALUE(Nosaukums,"ConstantValue")){if(Izmērs!=2)return -1;lauks_konstante[순번]=절반값();}
            else TAKE_VALUE(Izmērs);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!informācijas_tehnoloģija_nederīgs;순번++){
        metode_ievade*Grupa_mainīt_izmērus=메소드목록+순번;Grupa_mainīt_izmērus->konfigurācija_Background_Intelligent_Transfer_Service=절반값();Grupa_mainīt_izmērus->Nosaukums=절반값();Grupa_mainīt_izmērus->서술값=절반값();unsigned ievade_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<ievade_COUNT&&!informācijas_tehnoloģija_nederīgs;안쪽순번++){
            unsigned Nosaukums=절반값(),Izmērs=가득참(),Palaist=pašreizējais_amats;
            if(Izmērs>길이-pašreizējais_amats)return -1;
            if(UNICODE_VALUE(Nosaukums,"Code")){
                Grupa_mainīt_izmērus->kopa_Krātuve=절반값();Grupa_mainīt_izmērus->지역변수들=절반값();Grupa_mainīt_izmērus->Izmērs=가득참();Grupa_mainīt_izmērus->명령열=TAKE_VALUE(Grupa_mainīt_izmērus->Izmērs);
                if(Grupa_mainīt_izmērus->kopa_Krātuve>128||Grupa_mainīt_izmērus->지역변수들>128||Grupa_mainīt_izmērus->Izmērs>8192||절반값())return -1;atribūti();
            }else TAKE_VALUE(Izmērs);
            if(pašreizējais_amats!=Palaist+Izmērs)return -1;
        }
        if(!UNICODE_VALUE(Grupa_mainīt_izmērus->Nosaukums,"<init>")&&(!(Grupa_mainīt_izmērus->konfigurācija_Background_Intelligent_Transfer_Service&8)||(Grupa_mainīt_izmērus->konfigurācija_Background_Intelligent_Transfer_Service&(0x100|0x20))||!Grupa_mainīt_izmērus->Izmērs))return -1;
    }
    atribūti();return informācijas_tehnoloģija_nederīgs||pašreizējais_amats!=길이?-1:0;
}
static void konstante_VALUE(unsigned identifikators_VALUE){
    if(!identifikators_VALUE||identifikators_VALUE>=konstante_kopa){informācijas_tehnoloģija_nederīgs=1;return;}
    if(atzīmes_Saraksts[identifikators_VALUE]==3)내보내기("P(%uU);",첫째값[identifikators_VALUE]);
    else if(atzīmes_Saraksts[identifikators_VALUE]==8)내보내기("P((W)k%u);",identifikators_VALUE);else informācijas_tehnoloģija_nederīgs=1;
}
static void 호출(unsigned identifikators_VALUE,int 가상호출){
    if(identifikators_VALUE<1||identifikators_VALUE>=konstante_kopa||(atzīmes_Saraksts[identifikators_VALUE]!=10&&atzīmes_Saraksts[identifikators_VALUE]!=11)||첫째값[identifikators_VALUE]<1||첫째값[identifikators_VALUE]>=konstante_kopa||atzīmes_Saraksts[첫째값[identifikators_VALUE]]!=7||SECOND_VALUE[identifikators_VALUE]<1||SECOND_VALUE[identifikators_VALUE]>=konstante_kopa||atzīmes_Saraksts[SECOND_VALUE[identifikators_VALUE]]!=12){informācijas_tehnoloģija_nederīgs=1;return;}
    unsigned īpašnieks_objekts=첫째값[첫째값[identifikators_VALUE]],Nosaukums=첫째값[SECOND_VALUE[identifikators_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikators_VALUE]];int mērs=0,krājums_COUNT=서술자(서술값,&mērs);if(krājums_COUNT<0){informācijas_tehnoloģija_nederīgs=1;return;}
    for(int 순번=krājums_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(가상호출)내보내기("Q();");
    if(!가상호출&&같음(īpašnieks_objekts,첫째값[pašreizējais_klase])){
        unsigned Grupa_mainīt_izmērus=0;for(;Grupa_mainīt_izmērus<메소드개수;Grupa_mainīt_izmērus++)if(같음(Nosaukums,메소드목록[Grupa_mainīt_izmērus].Nosaukums)&&같음(서술값,메소드목록[Grupa_mainīt_izmērus].서술값))break;
        if(Grupa_mainīt_izmērus==메소드개수||!(메소드목록[Grupa_mainīt_izmērus].konfigurācija_Background_Intelligent_Transfer_Service&8)){informācijas_tehnoloģija_nederīgs=1;return;}
        if(mērs)내보내기("P(");내보내기("m%u(",Grupa_mainīt_izmērus);for(int 순번=0;순번<krājums_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(mērs?"));":" );");return;
    }
    if((가상호출&&UNICODE_VALUE(īpašnieks_objekts,"java/io/PrintStream")&& (UNICODE_VALUE(Nosaukums,"print")||UNICODE_VALUE(Nosaukums,"println")))||(!가상호출&&UNICODE_VALUE(īpašnieks_objekts,"Latviešu/savs/Izvade"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Nosaukums,"print")||UNICODE_VALUE(Nosaukums,"println")||UNICODE_VALUE(Nosaukums,"rakstīšana_numurs"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Nosaukums,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Nosaukums,"print")||UNICODE_VALUE(Nosaukums,"println")||UNICODE_VALUE(Nosaukums,"Rakstīt")||UNICODE_VALUE(Nosaukums,"rakstīšana_līnija"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Nosaukums,"print")||UNICODE_VALUE(Nosaukums,"Rakstīt")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Nosaukums,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!가상호출&&UNICODE_VALUE(īpašnieks_objekts,"Latviešu/savs/Fails")){
        if(UNICODE_VALUE(Nosaukums,"Rakstīt")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Nosaukums,"Lasīt")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    informācijas_tehnoloģija_nederīgs=1;
}
static void kompilēt_metode(unsigned LOOKUP_INDEX){
    metode_ievade*Grupa_mainīt_izmērus=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(Grupa_mainīt_izmērus->Nosaukums,"<init>"))return;int mērs,krājums_COUNT=서술자(Grupa_mainīt_izmērus->서술값,&mērs);if(krājums_COUNT<0){informācijas_tehnoloģija_nederīgs=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<krājums_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!krājums_COUNT)내보내기("void");
    if((unsigned)krājums_COUNT>Grupa_mainīt_izmērus->지역변수들){informācijas_tehnoloģija_nederīgs=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Grupa_mainīt_izmērus->지역변수들?Grupa_mainīt_izmērus->지역변수들:1);for(int 순번=0;순번<krājums_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=길이;길이=Grupa_mainīt_izmērus->명령열+Grupa_mainīt_izmērus->Izmērs;pašreizējais_amats=Grupa_mainīt_izmērus->명령열;
    while(pašreizējais_amats<길이&&!informācijas_tehnoloģija_nederīgs){unsigned komanda_amats=pašreizējais_amats-Grupa_mainīt_izmērus->명령열,operācija_VALUE=byte_dati();내보내기("L%u:;",komanda_amats);
        if(operācija_VALUE==0){}
        else if(operācija_VALUE==1)내보내기("P(0);");
        else if(operācija_VALUE>=2&&operācija_VALUE<=8)내보내기("P(%uU);",operācija_VALUE-3);
        else if(operācija_VALUE==16){int VALUE=(int8_t)byte_dati();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operācija_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operācija_VALUE==18||operācija_VALUE==19)konstante_VALUE(operācija_VALUE==18?byte_dati():절반값());
        else if(operācija_VALUE==21||operācija_VALUE==25){unsigned 순번=byte_dati();if(순번>=Grupa_mainīt_izmērus->지역변수들)informācijas_tehnoloģija_nederīgs=1;내보내기("P(v[%u]);",순번);}
        else if((operācija_VALUE>=26&&operācija_VALUE<=29)||(operācija_VALUE>=42&&operācija_VALUE<=45)){unsigned 순번=operācija_VALUE>=42?operācija_VALUE-42:operācija_VALUE-26;if(순번>=Grupa_mainīt_izmērus->지역변수들)informācijas_tehnoloģija_nederīgs=1;내보내기("P(v[%u]);",순번);}
        else if(operācija_VALUE==54||operācija_VALUE==58){unsigned 순번=byte_dati();if(순번>=Grupa_mainīt_izmērus->지역변수들)informācijas_tehnoloģija_nederīgs=1;내보내기("v[%u]=Q();",순번);}
        else if((operācija_VALUE>=59&&operācija_VALUE<=62)||(operācija_VALUE>=75&&operācija_VALUE<=78)){unsigned 순번=operācija_VALUE>=75?operācija_VALUE-75:operācija_VALUE-59;if(순번>=Grupa_mainīt_izmērus->지역변수들)informācijas_tehnoloģija_nederīgs=1;내보내기("v[%u]=Q();",순번);}
        else if(operācija_VALUE==46||operācija_VALUE==50||operācija_VALUE==51||operācija_VALUE==52||operācija_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operācija_VALUE==79||operācija_VALUE==83||operācija_VALUE==84||operācija_VALUE==85||operācija_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operācija_VALUE==84?"(unsigned)(signed char)q":operācija_VALUE==85?"(unsigned short)q":operācija_VALUE==86?"(unsigned)(short)q":"q");
        else if(operācija_VALUE==87)내보내기("Q();");
        else if(operācija_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(operācija_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operācija_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(operācija_VALUE==96||operācija_VALUE==100||operācija_VALUE==104||operācija_VALUE==120||operācija_VALUE==124||operācija_VALUE==126||operācija_VALUE==128||operācija_VALUE==130){const char*kodēšana_VALUE=operācija_VALUE==96?"+":operācija_VALUE==100?"-":operācija_VALUE==104?"*":operācija_VALUE==120?"<<":operācija_VALUE==124?">>":operācija_VALUE==126?"&":operācija_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kodēšana_VALUE,operācija_VALUE==120||operācija_VALUE==124?"%32":"");}
        else if(operācija_VALUE==108||operācija_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operācija_VALUE==112);
        else if(operācija_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(operācija_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operācija_VALUE==132){unsigned 순번=byte_dati();int 차이=(int8_t)byte_dati();if(순번>=Grupa_mainīt_izmērus->지역변수들)informācijas_tehnoloģija_nederīgs=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operācija_VALUE>=145&&operācija_VALUE<=147)내보내기("P((unsigned)(%s)Q());",operācija_VALUE==145?"signed char":operācija_VALUE==146?"unsigned short":"short");
        else if(operācija_VALUE>=153&&operācija_VALUE<=166){int mērķis=(int)komanda_amats+(int16_t)절반값();const char*Salīdzinājums_VALUE[]={"==","!=","<",">=",">","<="};if(mērķis<0||mērķis>=(int)Grupa_mainīt_izmērus->Izmērs){informācijas_tehnoloģija_nederīgs=1;break;}if(operācija_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Salīdzinājums_VALUE[operācija_VALUE-153],mērķis);else if(operācija_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Salīdzinājums_VALUE[operācija_VALUE-159],mērķis);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operācija_VALUE==165?"==":"!=",mērķis);}
        else if(operācija_VALUE==167){int mērķis=(int)komanda_amats+(int16_t)절반값();if(mērķis<0||mērķis>=(int)Grupa_mainīt_izmērus->Izmērs)informācijas_tehnoloģija_nederīgs=1;내보내기("goto L%d;",mērķis);}
        else if(operācija_VALUE==172||operācija_VALUE==176)내보내기("return Q();");else if(operācija_VALUE==177)내보내기("return 0;");
        else if(operācija_VALUE==178||operācija_VALUE==179){unsigned identifikators_VALUE=절반값();if(identifikators_VALUE<1||identifikators_VALUE>=konstante_kopa||atzīmes_Saraksts[identifikators_VALUE]!=9||첫째값[identifikators_VALUE]>=konstante_kopa||SECOND_VALUE[identifikators_VALUE]>=konstante_kopa||atzīmes_Saraksts[첫째값[identifikators_VALUE]]!=7||atzīmes_Saraksts[SECOND_VALUE[identifikators_VALUE]]!=12){informācijas_tehnoloģija_nederīgs=1;break;}unsigned īpašnieks_objekts=첫째값[첫째값[identifikators_VALUE]],Nosaukums=첫째값[SECOND_VALUE[identifikators_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikators_VALUE]];
            if(operācija_VALUE==178&&UNICODE_VALUE(īpašnieks_objekts,"java/lang/System")&&UNICODE_VALUE(Nosaukums,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Fails_ievade=0;while(Fails_ievade<필드개수&&(!같음(Nosaukums,lauka_nosaukums[Fails_ievade])||!같음(서술값,필드서술[Fails_ievade])))Fails_ievade++;if(!같음(īpašnieks_objekts,첫째값[pašreizējais_klase])||Fails_ievade==필드개수){informācijas_tehnoloģija_nederīgs=1;break;}내보내기(operācija_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",Fails_ievade);}}
        else if(operācija_VALUE==182||operācija_VALUE==184)호출(절반값(),operācija_VALUE==182);
        else if(operācija_VALUE==188){unsigned TYPE_joma=byte_dati();if(TYPE_joma!=4&&TYPE_joma!=5&&TYPE_joma!=8&&TYPE_joma!=9&&TYPE_joma!=10)informācijas_tehnoloģija_nederīgs=1;내보내기("P(jarray((int)Q()));");}
        else if(operācija_VALUE==190)내보내기("P(jlength(Q()));");
        else if(operācija_VALUE==198||operācija_VALUE==199){int mērķis=(int)komanda_amats+(int16_t)절반값();if(mērķis<0||mērķis>=(int)Grupa_mainīt_izmērus->Izmērs)informācijas_tehnoloģija_nederīgs=1;내보내기("if(Q()%s0)goto L%d;",operācija_VALUE==198?"==":"!=",mērķis);}
        else informācijas_tehnoloģija_nederīgs=1;
        if(informācijas_tehnoloģija_nederīgs)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,operācija_VALUE,komanda_amats);
        내보내기("\n");
    }
    길이=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned virkne_vienība(unsigned *dati_amats,unsigned beigt_zvanu_Nobīde){
    if(*dati_amats>=beigt_zvanu_Nobīde){informācijas_tehnoloģija_nederīgs=1;return 0;}unsigned koda_punkts=dati[(*dati_amats)++];
    if(koda_punkts<128)return koda_punkts;
    unsigned krājums_COUNT=koda_punkts>=0xc0&&koda_punkts<=0xdf?1:koda_punkts>=0xe0&&koda_punkts<=0xef?2:3;
    if(krājums_COUNT==3||krājums_COUNT>beigt_zvanu_Nobīde-*dati_amats){informācijas_tehnoloģija_nederīgs=1;return 0;}unsigned VALUE=koda_punkts&((1u<<(6-krājums_COUNT))-1);
    for(unsigned 순번=0;순번<krājums_COUNT;순번++){unsigned Tālāk_krājums=dati[(*dati_amats)++];if((Tālāk_krājums&0xc0)!=0x80)informācijas_tehnoloģija_nederīgs=1;VALUE=VALUE<<6|(Tālāk_krājums&63);}
    if((krājums_COUNT==1&&VALUE<128&&VALUE!=0)||(krājums_COUNT==2&&VALUE<2048))informācijas_tehnoloģija_nederīgs=1;return VALUE;
}
static void virkne_konstante(unsigned identifikators_VALUE){
    unsigned 부호없는값=첫째값[identifikators_VALUE];if(부호없는값<1||부호없는값>=konstante_kopa||atzīmes_Saraksts[부호없는값]!=1){informācijas_tehnoloģija_nederīgs=1;return;}내보내기("static const unsigned char k%u[]={",identifikators_VALUE);
    unsigned dati_amats=첫째값[부호없는값],beigt_zvanu_Nobīde=dati_amats+SECOND_VALUE[부호없는값];
    while(dati_amats<beigt_zvanu_Nobīde&&!informācijas_tehnoloģija_nederīgs){unsigned koda_punkts=virkne_vienība(&dati_amats,beigt_zvanu_Nobīde);
        if(koda_punkts>=0xd800&&koda_punkts<=0xdbff){unsigned 낮은부분=virkne_vienība(&dati_amats,beigt_zvanu_Nobīde);if(낮은부분<0xdc00||낮은부분>0xdfff){informācijas_tehnoloģija_nederīgs=1;break;}koda_punkts=0x10000+((koda_punkts-0xd800)<<10)+낮은부분-0xdc00;}
        else if(koda_punkts>=0xdc00&&koda_punkts<=0xdfff){informācijas_tehnoloģija_nederīgs=1;break;}
        if(!koda_punkts){printf("jaot: embedded NUL string needs JVM mode\n");informācijas_tehnoloģija_nederīgs=1;break;}
        if(koda_punkts<128)내보내기("%u,",koda_punkts);
        else{unsigned krājums_COUNT=koda_punkts<2048?2:koda_punkts<65536?3:4;내보내기("%u,",(krājums_COUNT==2?0xc0:krājums_COUNT==3?0xe0:0xf0)|(koda_punkts>>(6*(krājums_COUNT-1))));for(unsigned 순번=krājums_COUNT-1;순번;순번--)내보내기("%u,",0x80|((koda_punkts>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Nosaukums){
    size_t krājums_COUNT=strlen(Nosaukums);
    if(krājums_COUNT>4&&!strcmp(Nosaukums+krājums_COUNT-4,".jar")){
        if(꾸러미열기(Nosaukums)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char CEĻŠ[256];const char*ievade_metode=꾸러미진입클래스();krājums_COUNT=strlen(ievade_metode);if(krājums_COUNT+6>=sizeof(CEĻŠ))return 0;
        for(unsigned 순번=0;순번<krājums_COUNT;순번++)CEĻŠ[순번]=ievade_metode[순번]=='.'?'/':ievade_metode[순번];strcpy(CEĻŠ+krājums_COUNT,".class");int ievade_COUNT=꾸러미읽기(CEĻŠ,dati,sizeof(dati));if(ievade_COUNT<0)return 0;길이=ievade_COUNT;
    }else{intptr_t Fails_turis=사용자호출(3,(uintptr_t)Nosaukums,0,0,0,0,0);if(Fails_turis<0)return 0;intptr_t ievade_COUNT=사용자호출(9,Fails_turis,0,0,0,0,0);if(ievade_COUNT<0||ievade_COUNT>sizeof(dati)){사용자호출(4,Fails_turis,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,Fails_turis,(uintptr_t)dati,ievade_COUNT,0,0,0);사용자호출(4,Fails_turis,0,0,0,0,0);if(RECEIVED_COUNT!=ievade_COUNT)return 0;길이=ievade_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstante_kopa&&!informācijas_tehnoloģija_nederīgs;순번++)if(atzīmes_Saraksts[순번]==8)virkne_konstante(순번);
    if(informācijas_tehnoloģija_nederīgs)return 0;
    int ieejas_punkts=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Nosaukums,"<init>")){
        int mērs,ievade_COUNT=서술자(메소드목록[순번].서술값,&mērs);if(ievade_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<ievade_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!ievade_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Nosaukums,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfigurācija_Background_Intelligent_Transfer_Service&9)==9)ieejas_punkts=순번;
        if(UNICODE_VALUE(메소드목록[순번].Nosaukums,"<clinit>"))초기값=순번;
    }
    if(ieejas_punkts<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!informācijas_tehnoloģija_nederīgs;순번++)kompilēt_metode(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(lauks_konstante[순번]){
        unsigned koda_punkts=lauks_konstante[순번];if(koda_punkts>=konstante_kopa)return 0;
        if(atzīmes_Saraksts[koda_punkts]==3)내보내기("fields[%u]=%uU;",순번,첫째값[koda_punkts]);else if(atzīmes_Saraksts[koda_punkts]==8)내보내기("fields[%u]=(W)k%u;",순번,koda_punkts);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",ieejas_punkts);
    return informācijas_tehnoloģija_nederīgs?0:Teksts;
}
