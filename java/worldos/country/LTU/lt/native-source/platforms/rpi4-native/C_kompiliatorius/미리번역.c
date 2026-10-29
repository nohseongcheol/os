#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "paketas.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char duomenys[16384];static unsigned 길이,dabartinis_padėtis;static int informacinės_technologijos_neleistinas;
static unsigned Žymės_Sąrašas[512],첫째값[512],SECOND_VALUE[512],konstanta_telkinys,dabartinis_klasė;
static char Tekstas[65536];static unsigned Teksto_dydis;
typedef struct {unsigned konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba,Pavadinimas_2,서술값,명령열,Dydis,지역변수들,eilė_Saugykla;} metodas_įrašas;
static metodas_įrašas 메소드목록[64];static unsigned 메소드개수;
static unsigned lauko_pavadinimas[64],필드서술[64],laukas_konstanta[64],필드개수;
static unsigned TAKE_VALUE(unsigned prekė_COUNT){if(dabartinis_padėtis>길이||prekė_COUNT>길이-dabartinis_padėtis){informacinės_technologijos_neleistinas=1;return 0;}unsigned duomenys_padėtis=dabartinis_padėtis;dabartinis_padėtis+=prekė_COUNT;return duomenys_padėtis;}
static unsigned baitas_duomenys(void){unsigned duomenys_padėtis=TAKE_VALUE(1);return informacinės_technologijos_neleistinas?0:duomenys[duomenys_padėtis];}
static unsigned 절반값(void){unsigned x_koordinatė=baitas_duomenys();return x_koordinatė<<8|baitas_duomenys();}
static uint32_t 가득참(void){uint32_t x_koordinatė=절반값();return x_koordinatė<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*eilutė_duomenys){return 순번>0&&순번<konstanta_telkinys&&Žymės_Sąrašas[순번]==1&&strlen(eilutė_duomenys)==SECOND_VALUE[순번]&&!memcmp(duomenys+첫째값[순번],eilutė_duomenys,SECOND_VALUE[순번]);}
static int 같음(unsigned x_koordinatė,unsigned 세로좌표){return x_koordinatė>0&&x_koordinatė<konstanta_telkinys&&세로좌표>0&&세로좌표<konstanta_telkinys&&Žymės_Sąrašas[x_koordinatė]==1&&Žymės_Sąrašas[세로좌표]==1&&SECOND_VALUE[x_koordinatė]==SECOND_VALUE[세로좌표]&&!memcmp(duomenys+첫째값[x_koordinatė],duomenys+첫째값[세로좌표],SECOND_VALUE[x_koordinatė]);}
static void 내보내기(const char*Failas_įrašas,...){if(informacinės_technologijos_neleistinas)return;va_list argumentas_ARRAY;va_start(argumentas_ARRAY,Failas_įrašas);int prekė_COUNT=vsnprintf(Tekstas+Teksto_dydis,sizeof(Tekstas)-Teksto_dydis,Failas_įrašas,argumentas_ARRAY);va_end(argumentas_ARRAY);if(prekė_COUNT<0||(unsigned)prekė_COUNT>=sizeof(Tekstas)-Teksto_dydis){informacinės_technologijos_neleistinas=1;return;}Teksto_dydis+=prekė_COUNT;}
static int 서술자(unsigned identifikatorius_VALUE,int*REZULTATAS){
    if(identifikatorius_VALUE<1||identifikatorius_VALUE>=konstanta_telkinys||Žymės_Sąrašas[identifikatorius_VALUE]!=1)return -1;unsigned duomenys_padėtis=첫째값[identifikatorius_VALUE],baigti_pokalbį_OFFSET=duomenys_padėtis+SECOND_VALUE[identifikatorius_VALUE];if(duomenys_padėtis>=baigti_pokalbį_OFFSET||duomenys[duomenys_padėtis++]!='(')return -1;int įrašas_COUNT=0;
    while(duomenys_padėtis<baigti_pokalbį_OFFSET&&duomenys[duomenys_padėtis]!=')'){
        unsigned simbolio_kodas=duomenys[duomenys_padėtis++];while(simbolio_kodas=='['&&duomenys_padėtis<baigti_pokalbį_OFFSET)simbolio_kodas=duomenys[duomenys_padėtis++];
        if(simbolio_kodas=='L'){while(duomenys_padėtis<baigti_pokalbį_OFFSET&&duomenys[duomenys_padėtis]!=';')duomenys_padėtis++;if(duomenys_padėtis==baigti_pokalbį_OFFSET)return -1;duomenys_padėtis++;}
        else if(simbolio_kodas!='I'&&simbolio_kodas!='Z'&&simbolio_kodas!='B'&&simbolio_kodas!='C'&&simbolio_kodas!='S')return -1;
        if(++įrašas_COUNT>16)return -1;
    }
    if(duomenys_padėtis+1>=baigti_pokalbį_OFFSET||duomenys[duomenys_padėtis++]!=')')return -1;*REZULTATAS=duomenys[duomenys_padėtis]=='V'?0:1;
    if(duomenys[duomenys_padėtis]=='J'||duomenys[duomenys_padėtis]=='D'||duomenys[duomenys_padėtis]=='F')return -1;return įrašas_COUNT;
}
static void duomenys_ee823f36(void){unsigned prekė_COUNT=절반값();for(unsigned 순번=0;순번<prekė_COUNT&&!informacinės_technologijos_neleistinas;순번++){절반값();unsigned Dydis=가득참();TAKE_VALUE(Dydis);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned papildoma_versija=절반값(),versijos_numeris=절반값();if(papildoma_versija||versijos_numeris<45||versijos_numeris>52)return -1;
    konstanta_telkinys=절반값();if(konstanta_telkinys<1||konstanta_telkinys>512)return -1;
    for(unsigned 순번=1;순번<konstanta_telkinys&&!informacinės_technologijos_neleistinas;순번++){
        Žymės_Sąrašas[순번]=baitas_duomenys();switch(Žymės_Sąrašas[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=konstanta_telkinys)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=baitas_duomenys();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();dabartinis_klasė=절반값();절반값();if(dabartinis_klasė<1||dabartinis_klasė>=konstanta_telkinys||Žymės_Sąrašas[dabartinis_klasė]!=7||첫째값[dabartinis_klasė]<1||첫째값[dabartinis_klasė]>=konstanta_telkinys||Žymės_Sąrašas[첫째값[dabartinis_klasė]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!informacinės_technologijos_neleistinas;순번++){
        unsigned konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba=절반값();lauko_pavadinimas[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba&8))return -1;
        unsigned įrašas_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<įrašas_COUNT&&!informacinės_technologijos_neleistinas;안쪽순번++){
            unsigned Pavadinimas_2=절반값(),Dydis=가득참();
            if(UNICODE_VALUE(Pavadinimas_2,"ConstantValue")){if(Dydis!=2)return -1;laukas_konstanta[순번]=절반값();}
            else TAKE_VALUE(Dydis);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!informacinės_technologijos_neleistinas;순번++){
        metodas_įrašas*Grupė_dydis=메소드목록+순번;Grupė_dydis->konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba=절반값();Grupė_dydis->Pavadinimas_2=절반값();Grupė_dydis->서술값=절반값();unsigned įrašas_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<įrašas_COUNT&&!informacinės_technologijos_neleistinas;안쪽순번++){
            unsigned Pavadinimas_2=절반값(),Dydis=가득참(),Paleisti=dabartinis_padėtis;
            if(Dydis>길이-dabartinis_padėtis)return -1;
            if(UNICODE_VALUE(Pavadinimas_2,"Code")){
                Grupė_dydis->eilė_Saugykla=절반값();Grupė_dydis->지역변수들=절반값();Grupė_dydis->Dydis=가득참();Grupė_dydis->명령열=TAKE_VALUE(Grupė_dydis->Dydis);
                if(Grupė_dydis->eilė_Saugykla>128||Grupė_dydis->지역변수들>128||Grupė_dydis->Dydis>8192||절반값())return -1;duomenys_ee823f36();
            }else TAKE_VALUE(Dydis);
            if(dabartinis_padėtis!=Paleisti+Dydis)return -1;
        }
        if(!UNICODE_VALUE(Grupė_dydis->Pavadinimas_2,"<init>")&&(!(Grupė_dydis->konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba&8)||(Grupė_dydis->konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba&(0x100|0x20))||!Grupė_dydis->Dydis))return -1;
    }
    duomenys_ee823f36();return informacinės_technologijos_neleistinas||dabartinis_padėtis!=길이?-1:0;
}
static void konstanta_VALUE(unsigned identifikatorius_VALUE){
    if(!identifikatorius_VALUE||identifikatorius_VALUE>=konstanta_telkinys){informacinės_technologijos_neleistinas=1;return;}
    if(Žymės_Sąrašas[identifikatorius_VALUE]==3)내보내기("P(%uU);",첫째값[identifikatorius_VALUE]);
    else if(Žymės_Sąrašas[identifikatorius_VALUE]==8)내보내기("P((W)k%u);",identifikatorius_VALUE);else informacinės_technologijos_neleistinas=1;
}
static void 호출(unsigned identifikatorius_VALUE,int 가상호출){
    if(identifikatorius_VALUE<1||identifikatorius_VALUE>=konstanta_telkinys||(Žymės_Sąrašas[identifikatorius_VALUE]!=10&&Žymės_Sąrašas[identifikatorius_VALUE]!=11)||첫째값[identifikatorius_VALUE]<1||첫째값[identifikatorius_VALUE]>=konstanta_telkinys||Žymės_Sąrašas[첫째값[identifikatorius_VALUE]]!=7||SECOND_VALUE[identifikatorius_VALUE]<1||SECOND_VALUE[identifikatorius_VALUE]>=konstanta_telkinys||Žymės_Sąrašas[SECOND_VALUE[identifikatorius_VALUE]]!=12){informacinės_technologijos_neleistinas=1;return;}
    unsigned savininkas_objektas=첫째값[첫째값[identifikatorius_VALUE]],Pavadinimas_2=첫째값[SECOND_VALUE[identifikatorius_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikatorius_VALUE]];int REZULTATAS=0,prekė_COUNT=서술자(서술값,&REZULTATAS);if(prekė_COUNT<0){informacinės_technologijos_neleistinas=1;return;}
    for(int 순번=prekė_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(가상호출)내보내기("Q();");
    if(!가상호출&&같음(savininkas_objektas,첫째값[dabartinis_klasė])){
        unsigned Grupė_dydis=0;for(;Grupė_dydis<메소드개수;Grupė_dydis++)if(같음(Pavadinimas_2,메소드목록[Grupė_dydis].Pavadinimas_2)&&같음(서술값,메소드목록[Grupė_dydis].서술값))break;
        if(Grupė_dydis==메소드개수||!(메소드목록[Grupė_dydis].konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba&8)){informacinės_technologijos_neleistinas=1;return;}
        if(REZULTATAS)내보내기("P(");내보내기("m%u(",Grupė_dydis);for(int 순번=0;순번<prekė_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(REZULTATAS?"));":" );");return;
    }
    if((가상호출&&UNICODE_VALUE(savininkas_objektas,"java/io/PrintStream")&& (UNICODE_VALUE(Pavadinimas_2,"print")||UNICODE_VALUE(Pavadinimas_2,"println")))||(!가상호출&&UNICODE_VALUE(savininkas_objektas,"Lietuvių/savas/Išvestis"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Pavadinimas_2,"print")||UNICODE_VALUE(Pavadinimas_2,"println")||UNICODE_VALUE(Pavadinimas_2,"rašymas_numeris"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Pavadinimas_2,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Pavadinimas_2,"print")||UNICODE_VALUE(Pavadinimas_2,"println")||UNICODE_VALUE(Pavadinimas_2,"Rašymas")||UNICODE_VALUE(Pavadinimas_2,"rašymas_eilutė"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Pavadinimas_2,"print")||UNICODE_VALUE(Pavadinimas_2,"Rašymas")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Pavadinimas_2,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!가상호출&&UNICODE_VALUE(savininkas_objektas,"Lietuvių/savas/Failas")){
        if(UNICODE_VALUE(Pavadinimas_2,"Rašymas")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Pavadinimas_2,"Skaitymas")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    informacinės_technologijos_neleistinas=1;
}
static void kompiliuoti_metodas(unsigned LOOKUP_INDEX){
    metodas_įrašas*Grupė_dydis=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(Grupė_dydis->Pavadinimas_2,"<init>"))return;int REZULTATAS,prekė_COUNT=서술자(Grupė_dydis->서술값,&REZULTATAS);if(prekė_COUNT<0){informacinės_technologijos_neleistinas=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<prekė_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!prekė_COUNT)내보내기("void");
    if((unsigned)prekė_COUNT>Grupė_dydis->지역변수들){informacinės_technologijos_neleistinas=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Grupė_dydis->지역변수들?Grupė_dydis->지역변수들:1);for(int 순번=0;순번<prekė_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=길이;길이=Grupė_dydis->명령열+Grupė_dydis->Dydis;dabartinis_padėtis=Grupė_dydis->명령열;
    while(dabartinis_padėtis<길이&&!informacinės_technologijos_neleistinas){unsigned komanda_padėtis=dabartinis_padėtis-Grupė_dydis->명령열,operacija_VALUE=baitas_duomenys();내보내기("L%u:;",komanda_padėtis);
        if(operacija_VALUE==0){}
        else if(operacija_VALUE==1)내보내기("P(0);");
        else if(operacija_VALUE>=2&&operacija_VALUE<=8)내보내기("P(%uU);",operacija_VALUE-3);
        else if(operacija_VALUE==16){int VALUE=(int8_t)baitas_duomenys();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operacija_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operacija_VALUE==18||operacija_VALUE==19)konstanta_VALUE(operacija_VALUE==18?baitas_duomenys():절반값());
        else if(operacija_VALUE==21||operacija_VALUE==25){unsigned 순번=baitas_duomenys();if(순번>=Grupė_dydis->지역변수들)informacinės_technologijos_neleistinas=1;내보내기("P(v[%u]);",순번);}
        else if((operacija_VALUE>=26&&operacija_VALUE<=29)||(operacija_VALUE>=42&&operacija_VALUE<=45)){unsigned 순번=operacija_VALUE>=42?operacija_VALUE-42:operacija_VALUE-26;if(순번>=Grupė_dydis->지역변수들)informacinės_technologijos_neleistinas=1;내보내기("P(v[%u]);",순번);}
        else if(operacija_VALUE==54||operacija_VALUE==58){unsigned 순번=baitas_duomenys();if(순번>=Grupė_dydis->지역변수들)informacinės_technologijos_neleistinas=1;내보내기("v[%u]=Q();",순번);}
        else if((operacija_VALUE>=59&&operacija_VALUE<=62)||(operacija_VALUE>=75&&operacija_VALUE<=78)){unsigned 순번=operacija_VALUE>=75?operacija_VALUE-75:operacija_VALUE-59;if(순번>=Grupė_dydis->지역변수들)informacinės_technologijos_neleistinas=1;내보내기("v[%u]=Q();",순번);}
        else if(operacija_VALUE==46||operacija_VALUE==50||operacija_VALUE==51||operacija_VALUE==52||operacija_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operacija_VALUE==79||operacija_VALUE==83||operacija_VALUE==84||operacija_VALUE==85||operacija_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operacija_VALUE==84?"(unsigned)(signed char)q":operacija_VALUE==85?"(unsigned short)q":operacija_VALUE==86?"(unsigned)(short)q":"q");
        else if(operacija_VALUE==87)내보내기("Q();");
        else if(operacija_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(operacija_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operacija_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(operacija_VALUE==96||operacija_VALUE==100||operacija_VALUE==104||operacija_VALUE==120||operacija_VALUE==124||operacija_VALUE==126||operacija_VALUE==128||operacija_VALUE==130){const char*kodavimas_VALUE=operacija_VALUE==96?"+":operacija_VALUE==100?"-":operacija_VALUE==104?"*":operacija_VALUE==120?"<<":operacija_VALUE==124?">>":operacija_VALUE==126?"&":operacija_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kodavimas_VALUE,operacija_VALUE==120||operacija_VALUE==124?"%32":"");}
        else if(operacija_VALUE==108||operacija_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operacija_VALUE==112);
        else if(operacija_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(operacija_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operacija_VALUE==132){unsigned 순번=baitas_duomenys();int 차이=(int8_t)baitas_duomenys();if(순번>=Grupė_dydis->지역변수들)informacinės_technologijos_neleistinas=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operacija_VALUE>=145&&operacija_VALUE<=147)내보내기("P((unsigned)(%s)Q());",operacija_VALUE==145?"signed char":operacija_VALUE==146?"unsigned short":"short");
        else if(operacija_VALUE>=153&&operacija_VALUE<=166){int tikslas=(int)komanda_padėtis+(int16_t)절반값();const char*Palyginimas_VALUE[]={"==","!=","<",">=",">","<="};if(tikslas<0||tikslas>=(int)Grupė_dydis->Dydis){informacinės_technologijos_neleistinas=1;break;}if(operacija_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Palyginimas_VALUE[operacija_VALUE-153],tikslas);else if(operacija_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Palyginimas_VALUE[operacija_VALUE-159],tikslas);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operacija_VALUE==165?"==":"!=",tikslas);}
        else if(operacija_VALUE==167){int tikslas=(int)komanda_padėtis+(int16_t)절반값();if(tikslas<0||tikslas>=(int)Grupė_dydis->Dydis)informacinės_technologijos_neleistinas=1;내보내기("goto L%d;",tikslas);}
        else if(operacija_VALUE==172||operacija_VALUE==176)내보내기("return Q();");else if(operacija_VALUE==177)내보내기("return 0;");
        else if(operacija_VALUE==178||operacija_VALUE==179){unsigned identifikatorius_VALUE=절반값();if(identifikatorius_VALUE<1||identifikatorius_VALUE>=konstanta_telkinys||Žymės_Sąrašas[identifikatorius_VALUE]!=9||첫째값[identifikatorius_VALUE]>=konstanta_telkinys||SECOND_VALUE[identifikatorius_VALUE]>=konstanta_telkinys||Žymės_Sąrašas[첫째값[identifikatorius_VALUE]]!=7||Žymės_Sąrašas[SECOND_VALUE[identifikatorius_VALUE]]!=12){informacinės_technologijos_neleistinas=1;break;}unsigned savininkas_objektas=첫째값[첫째값[identifikatorius_VALUE]],Pavadinimas_2=첫째값[SECOND_VALUE[identifikatorius_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikatorius_VALUE]];
            if(operacija_VALUE==178&&UNICODE_VALUE(savininkas_objektas,"java/lang/System")&&UNICODE_VALUE(Pavadinimas_2,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Failas_įrašas=0;while(Failas_įrašas<필드개수&&(!같음(Pavadinimas_2,lauko_pavadinimas[Failas_įrašas])||!같음(서술값,필드서술[Failas_įrašas])))Failas_įrašas++;if(!같음(savininkas_objektas,첫째값[dabartinis_klasė])||Failas_įrašas==필드개수){informacinės_technologijos_neleistinas=1;break;}내보내기(operacija_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",Failas_įrašas);}}
        else if(operacija_VALUE==182||operacija_VALUE==184)호출(절반값(),operacija_VALUE==182);
        else if(operacija_VALUE==188){unsigned TYPE_sritis=baitas_duomenys();if(TYPE_sritis!=4&&TYPE_sritis!=5&&TYPE_sritis!=8&&TYPE_sritis!=9&&TYPE_sritis!=10)informacinės_technologijos_neleistinas=1;내보내기("P(jarray((int)Q()));");}
        else if(operacija_VALUE==190)내보내기("P(jlength(Q()));");
        else if(operacija_VALUE==198||operacija_VALUE==199){int tikslas=(int)komanda_padėtis+(int16_t)절반값();if(tikslas<0||tikslas>=(int)Grupė_dydis->Dydis)informacinės_technologijos_neleistinas=1;내보내기("if(Q()%s0)goto L%d;",operacija_VALUE==198?"==":"!=",tikslas);}
        else informacinės_technologijos_neleistinas=1;
        if(informacinės_technologijos_neleistinas)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,operacija_VALUE,komanda_padėtis);
        내보내기("\n");
    }
    길이=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned eilutė_pamoka(unsigned *duomenys_padėtis,unsigned baigti_pokalbį_OFFSET){
    if(*duomenys_padėtis>=baigti_pokalbį_OFFSET){informacinės_technologijos_neleistinas=1;return 0;}unsigned simbolio_kodas=duomenys[(*duomenys_padėtis)++];
    if(simbolio_kodas<128)return simbolio_kodas;
    unsigned prekė_COUNT=simbolio_kodas>=0xc0&&simbolio_kodas<=0xdf?1:simbolio_kodas>=0xe0&&simbolio_kodas<=0xef?2:3;
    if(prekė_COUNT==3||prekė_COUNT>baigti_pokalbį_OFFSET-*duomenys_padėtis){informacinės_technologijos_neleistinas=1;return 0;}unsigned VALUE=simbolio_kodas&((1u<<(6-prekė_COUNT))-1);
    for(unsigned 순번=0;순번<prekė_COUNT;순번++){unsigned toliau_prekė=duomenys[(*duomenys_padėtis)++];if((toliau_prekė&0xc0)!=0x80)informacinės_technologijos_neleistinas=1;VALUE=VALUE<<6|(toliau_prekė&63);}
    if((prekė_COUNT==1&&VALUE<128&&VALUE!=0)||(prekė_COUNT==2&&VALUE<2048))informacinės_technologijos_neleistinas=1;return VALUE;
}
static void eilutė_konstanta(unsigned identifikatorius_VALUE){
    unsigned 부호없는값=첫째값[identifikatorius_VALUE];if(부호없는값<1||부호없는값>=konstanta_telkinys||Žymės_Sąrašas[부호없는값]!=1){informacinės_technologijos_neleistinas=1;return;}내보내기("static const unsigned char k%u[]={",identifikatorius_VALUE);
    unsigned duomenys_padėtis=첫째값[부호없는값],baigti_pokalbį_OFFSET=duomenys_padėtis+SECOND_VALUE[부호없는값];
    while(duomenys_padėtis<baigti_pokalbį_OFFSET&&!informacinės_technologijos_neleistinas){unsigned simbolio_kodas=eilutė_pamoka(&duomenys_padėtis,baigti_pokalbį_OFFSET);
        if(simbolio_kodas>=0xd800&&simbolio_kodas<=0xdbff){unsigned 낮은부분=eilutė_pamoka(&duomenys_padėtis,baigti_pokalbį_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){informacinės_technologijos_neleistinas=1;break;}simbolio_kodas=0x10000+((simbolio_kodas-0xd800)<<10)+낮은부분-0xdc00;}
        else if(simbolio_kodas>=0xdc00&&simbolio_kodas<=0xdfff){informacinės_technologijos_neleistinas=1;break;}
        if(!simbolio_kodas){printf("jaot: embedded NUL string needs JVM mode\n");informacinės_technologijos_neleistinas=1;break;}
        if(simbolio_kodas<128)내보내기("%u,",simbolio_kodas);
        else{unsigned prekė_COUNT=simbolio_kodas<2048?2:simbolio_kodas<65536?3:4;내보내기("%u,",(prekė_COUNT==2?0xc0:prekė_COUNT==3?0xe0:0xf0)|(simbolio_kodas>>(6*(prekė_COUNT-1))));for(unsigned 순번=prekė_COUNT-1;순번;순번--)내보내기("%u,",0x80|((simbolio_kodas>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Pavadinimas_2){
    size_t prekė_COUNT=strlen(Pavadinimas_2);
    if(prekė_COUNT>4&&!strcmp(Pavadinimas_2+prekė_COUNT-4,".jar")){
        if(꾸러미열기(Pavadinimas_2)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char KELIAS[256];const char*įrašas_metodas=꾸러미진입클래스();prekė_COUNT=strlen(įrašas_metodas);if(prekė_COUNT+6>=sizeof(KELIAS))return 0;
        for(unsigned 순번=0;순번<prekė_COUNT;순번++)KELIAS[순번]=įrašas_metodas[순번]=='.'?'/':įrašas_metodas[순번];strcpy(KELIAS+prekė_COUNT,".class");int įrašas_COUNT=꾸러미읽기(KELIAS,duomenys,sizeof(duomenys));if(įrašas_COUNT<0)return 0;길이=įrašas_COUNT;
    }else{intptr_t Failas_rodyklė=사용자호출(3,(uintptr_t)Pavadinimas_2,0,0,0,0,0);if(Failas_rodyklė<0)return 0;intptr_t įrašas_COUNT=사용자호출(9,Failas_rodyklė,0,0,0,0,0);if(įrašas_COUNT<0||įrašas_COUNT>sizeof(duomenys)){사용자호출(4,Failas_rodyklė,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,Failas_rodyklė,(uintptr_t)duomenys,įrašas_COUNT,0,0,0);사용자호출(4,Failas_rodyklė,0,0,0,0,0);if(RECEIVED_COUNT!=įrašas_COUNT)return 0;길이=įrašas_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstanta_telkinys&&!informacinės_technologijos_neleistinas;순번++)if(Žymės_Sąrašas[순번]==8)eilutė_konstanta(순번);
    if(informacinės_technologijos_neleistinas)return 0;
    int įrašas_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Pavadinimas_2,"<init>")){
        int REZULTATAS,įrašas_COUNT=서술자(메소드목록[순번].서술값,&REZULTATAS);if(įrašas_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<įrašas_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!įrašas_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Pavadinimas_2,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba&9)==9)įrašas_p=순번;
        if(UNICODE_VALUE(메소드목록[순번].Pavadinimas_2,"<clinit>"))초기값=순번;
    }
    if(įrašas_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!informacinės_technologijos_neleistinas;순번++)kompiliuoti_metodas(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(laukas_konstanta[순번]){
        unsigned simbolio_kodas=laukas_konstanta[순번];if(simbolio_kodas>=konstanta_telkinys)return 0;
        if(Žymės_Sąrašas[simbolio_kodas]==3)내보내기("fields[%u]=%uU;",순번,첫째값[simbolio_kodas]);else if(Žymės_Sąrašas[simbolio_kodas]==8)내보내기("fields[%u]=(W)k%u;",순번,simbolio_kodas);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",įrašas_p);
    return informacinės_technologijos_neleistinas?0:Tekstas;
}
