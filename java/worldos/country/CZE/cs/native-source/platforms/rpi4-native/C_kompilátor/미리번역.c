#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "sada.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char data[16384];static unsigned délka_HODNOTA,dobrá_pozice;static int informační_systémy_neplatný;
static unsigned Značky_Seznam[512],첫째값[512],SEKUNDA_HODNOTA[512],konstanta_fond,dobrá_Třída;
static char text[65536];static unsigned Velikost_textu;
typedef struct {unsigned konfigurace_BITS,Název,popisovač_data,명령열,Velikost,지역변수들,paměť_zásobníku;} metoda_položka;
static metoda_položka 메소드목록[64];static unsigned 메소드개수;
static unsigned název_pole_98daa19b[64],pole_popisovač[64],pole_konstanta[64],필드개수;
static unsigned VZÍT_HODNOTA(unsigned zboží_POČET){if(dobrá_pozice>délka_HODNOTA||zboží_POČET>délka_HODNOTA-dobrá_pozice){informační_systémy_neplatný=1;return 0;}unsigned data_pozice=dobrá_pozice;dobrá_pozice+=zboží_POČET;return data_pozice;}
static unsigned bajt_data(void){unsigned data_pozice=VZÍT_HODNOTA(1);return informační_systémy_neplatný?0:data[data_pozice];}
static unsigned 절반값(void){unsigned souřadnice_x=bajt_data();return souřadnice_x<<8|bajt_data();}
static uint32_t 가득참(void){uint32_t souřadnice_x=절반값();return souřadnice_x<<16|절반값();}
static int UNICODE_HODNOTA(unsigned 순번,const char*řetězec_data){return 순번>0&&순번<konstanta_fond&&Značky_Seznam[순번]==1&&strlen(řetězec_data)==SEKUNDA_HODNOTA[순번]&&!memcmp(data+첫째값[순번],řetězec_data,SEKUNDA_HODNOTA[순번]);}
static int 같음(unsigned souřadnice_x,unsigned Y_souřadnice){return souřadnice_x>0&&souřadnice_x<konstanta_fond&&Y_souřadnice>0&&Y_souřadnice<konstanta_fond&&Značky_Seznam[souřadnice_x]==1&&Značky_Seznam[Y_souřadnice]==1&&SEKUNDA_HODNOTA[souřadnice_x]==SEKUNDA_HODNOTA[Y_souřadnice]&&!memcmp(data+첫째값[souřadnice_x],data+첫째값[Y_souřadnice],SEKUNDA_HODNOTA[souřadnice_x]);}
static void 내보내기(const char*Soubor_položka,...){if(informační_systémy_neplatný)return;va_list argument_pole;va_start(argument_pole,Soubor_položka);int zboží_POČET=vsnprintf(text+Velikost_textu,sizeof(text)-Velikost_textu,Soubor_položka,argument_pole);va_end(argument_pole);if(zboží_POČET<0||(unsigned)zboží_POČET>=sizeof(text)-Velikost_textu){informační_systémy_neplatný=1;return;}Velikost_textu+=zboží_POČET;}
static int popisovač_položka(unsigned identifikátor_HODNOTA,int*VÝSLEDEK){
    if(identifikátor_HODNOTA<1||identifikátor_HODNOTA>=konstanta_fond||Značky_Seznam[identifikátor_HODNOTA]!=1)return -1;unsigned data_pozice=첫째값[identifikátor_HODNOTA],konec_POSUN=data_pozice+SEKUNDA_HODNOTA[identifikátor_HODNOTA];if(data_pozice>=konec_POSUN||data[data_pozice++]!='(')return -1;int položka_POČET=0;
    while(data_pozice<konec_POSUN&&data[data_pozice]!=')'){
        unsigned bod_kódu=data[data_pozice++];while(bod_kódu=='['&&data_pozice<konec_POSUN)bod_kódu=data[data_pozice++];
        if(bod_kódu=='L'){while(data_pozice<konec_POSUN&&data[data_pozice]!=';')data_pozice++;if(data_pozice==konec_POSUN)return -1;data_pozice++;}
        else if(bod_kódu!='I'&&bod_kódu!='Z'&&bod_kódu!='B'&&bod_kódu!='C'&&bod_kódu!='S')return -1;
        if(++položka_POČET>16)return -1;
    }
    if(data_pozice+1>=konec_POSUN||data[data_pozice++]!=')')return -1;*VÝSLEDEK=data[data_pozice]=='V'?0:1;
    if(data[data_pozice]=='J'||data[data_pozice]=='D'||data[data_pozice]=='F')return -1;return položka_POČET;
}
static void atributy(void){unsigned zboží_POČET=절반값();for(unsigned 순번=0;순번<zboží_POČET&&!informační_systémy_neplatný;순번++){절반값();unsigned Velikost=가득참();VZÍT_HODNOTA(Velikost);}}
static int parsovat_vstup(void){
    if(가득참()!=0xcafebabe)return -1;unsigned podverze=절반값(),číslo_verze=절반값();if(podverze||číslo_verze<45||číslo_verze>52)return -1;
    konstanta_fond=절반값();if(konstanta_fond<1||konstanta_fond>512)return -1;
    for(unsigned 순번=1;순번<konstanta_fond&&!informační_systémy_neplatný;순번++){
        Značky_Seznam[순번]=bajt_data();switch(Značky_Seznam[순번]){
        case 1:SEKUNDA_HODNOTA[순번]=절반값();첫째값[순번]=VZÍT_HODNOTA(SEKUNDA_HODNOTA[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:VZÍT_HODNOTA(8);if(++순번>=konstanta_fond)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SEKUNDA_HODNOTA[순번]=절반값();break;
        case 15:첫째값[순번]=bajt_data();SEKUNDA_HODNOTA[순번]=절반값();break;default:return -1;
        }
    }
    절반값();dobrá_Třída=절반값();절반값();if(dobrá_Třída<1||dobrá_Třída>=konstanta_fond||Značky_Seznam[dobrá_Třída]!=7||첫째값[dobrá_Třída]<1||첫째값[dobrá_Třída]>=konstanta_fond||Značky_Seznam[첫째값[dobrá_Třída]]!=1)return -1;unsigned 인터페이스목록=절반값();VZÍT_HODNOTA(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!informační_systémy_neplatný;순번++){
        unsigned konfigurace_BITS=절반값();název_pole_98daa19b[순번]=절반값();pole_popisovač[순번]=절반값();
        if(!(konfigurace_BITS&8))return -1;
        unsigned položka_POČET=절반값();for(unsigned 안쪽순번=0;안쪽순번<položka_POČET&&!informační_systémy_neplatný;안쪽순번++){
            unsigned Název=절반값(),Velikost=가득참();
            if(UNICODE_HODNOTA(Název,"ConstantValue")){if(Velikost!=2)return -1;pole_konstanta[순번]=절반값();}
            else VZÍT_HODNOTA(Velikost);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!informační_systémy_neplatný;순번++){
        metoda_položka*Skupina_změnit_velikost=메소드목록+순번;Skupina_změnit_velikost->konfigurace_BITS=절반값();Skupina_změnit_velikost->Název=절반값();Skupina_změnit_velikost->popisovač_data=절반값();unsigned položka_POČET=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<položka_POČET&&!informační_systémy_neplatný;안쪽순번++){
            unsigned Název=절반값(),Velikost=가득참(),Spustit_2=dobrá_pozice;
            if(Velikost>délka_HODNOTA-dobrá_pozice)return -1;
            if(UNICODE_HODNOTA(Název,"Code")){
                Skupina_změnit_velikost->paměť_zásobníku=절반값();Skupina_změnit_velikost->지역변수들=절반값();Skupina_změnit_velikost->Velikost=가득참();Skupina_změnit_velikost->명령열=VZÍT_HODNOTA(Skupina_změnit_velikost->Velikost);
                if(Skupina_změnit_velikost->paměť_zásobníku>128||Skupina_změnit_velikost->지역변수들>128||Skupina_změnit_velikost->Velikost>8192||절반값())return -1;atributy();
            }else VZÍT_HODNOTA(Velikost);
            if(dobrá_pozice!=Spustit_2+Velikost)return -1;
        }
        if(!UNICODE_HODNOTA(Skupina_změnit_velikost->Název,"<init>")&&(!(Skupina_změnit_velikost->konfigurace_BITS&8)||(Skupina_změnit_velikost->konfigurace_BITS&(0x100|0x20))||!Skupina_změnit_velikost->Velikost))return -1;
    }
    atributy();return informační_systémy_neplatný||dobrá_pozice!=délka_HODNOTA?-1:0;
}
static void konstanta_HODNOTA(unsigned identifikátor_HODNOTA){
    if(!identifikátor_HODNOTA||identifikátor_HODNOTA>=konstanta_fond){informační_systémy_neplatný=1;return;}
    if(Značky_Seznam[identifikátor_HODNOTA]==3)내보내기("P(%uU);",첫째값[identifikátor_HODNOTA]);
    else if(Značky_Seznam[identifikátor_HODNOTA]==8)내보내기("P((W)k%u);",identifikátor_HODNOTA);else informační_systémy_neplatný=1;
}
static void 호출(unsigned identifikátor_HODNOTA,int virtuální_VOLAT){
    if(identifikátor_HODNOTA<1||identifikátor_HODNOTA>=konstanta_fond||(Značky_Seznam[identifikátor_HODNOTA]!=10&&Značky_Seznam[identifikátor_HODNOTA]!=11)||첫째값[identifikátor_HODNOTA]<1||첫째값[identifikátor_HODNOTA]>=konstanta_fond||Značky_Seznam[첫째값[identifikátor_HODNOTA]]!=7||SEKUNDA_HODNOTA[identifikátor_HODNOTA]<1||SEKUNDA_HODNOTA[identifikátor_HODNOTA]>=konstanta_fond||Značky_Seznam[SEKUNDA_HODNOTA[identifikátor_HODNOTA]]!=12){informační_systémy_neplatný=1;return;}
    unsigned vlastník_objekt=첫째값[첫째값[identifikátor_HODNOTA]],Název=첫째값[SEKUNDA_HODNOTA[identifikátor_HODNOTA]],popisovač_data=SEKUNDA_HODNOTA[SEKUNDA_HODNOTA[identifikátor_HODNOTA]];int VÝSLEDEK=0,zboží_POČET=popisovač_položka(popisovač_data,&VÝSLEDEK);if(zboží_POČET<0){informační_systémy_neplatný=1;return;}
    for(int 순번=zboží_POČET;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtuální_VOLAT)내보내기("Q();");
    if(!virtuální_VOLAT&&같음(vlastník_objekt,첫째값[dobrá_Třída])){
        unsigned Skupina_změnit_velikost=0;for(;Skupina_změnit_velikost<메소드개수;Skupina_změnit_velikost++)if(같음(Název,메소드목록[Skupina_změnit_velikost].Název)&&같음(popisovač_data,메소드목록[Skupina_změnit_velikost].popisovač_data))break;
        if(Skupina_změnit_velikost==메소드개수||!(메소드목록[Skupina_změnit_velikost].konfigurace_BITS&8)){informační_systémy_neplatný=1;return;}
        if(VÝSLEDEK)내보내기("P(");내보내기("m%u(",Skupina_změnit_velikost);for(int 순번=0;순번<zboží_POČET;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(VÝSLEDEK?"));":" );");return;
    }
    if((virtuální_VOLAT&&UNICODE_HODNOTA(vlastník_objekt,"java/io/PrintStream")&& (UNICODE_HODNOTA(Název,"print")||UNICODE_HODNOTA(Název,"println")))||(!virtuální_VOLAT&&UNICODE_HODNOTA(vlastník_objekt,"čeština/vlastní/výstupní_pozice"))){
        if(UNICODE_HODNOTA(popisovač_data,"(I)V")&&(UNICODE_HODNOTA(Název,"print")||UNICODE_HODNOTA(Název,"println")||UNICODE_HODNOTA(Název,"zápis_číslo"))){내보내기("jprint(x[0],1,%d);",UNICODE_HODNOTA(Název,"print")?0:1);return;}
        if(UNICODE_HODNOTA(popisovač_data,"(Ljava/lang/String;)V")&&(UNICODE_HODNOTA(Název,"print")||UNICODE_HODNOTA(Název,"println")||UNICODE_HODNOTA(Název,"Zápis")||UNICODE_HODNOTA(Název,"zápis_čára"))){내보내기("jprint(x[0],0,%d);",UNICODE_HODNOTA(Název,"print")||UNICODE_HODNOTA(Název,"Zápis")?0:1);return;}
        if(UNICODE_HODNOTA(popisovač_data,"()V")&&UNICODE_HODNOTA(Název,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtuální_VOLAT&&UNICODE_HODNOTA(vlastník_objekt,"čeština/vlastní/název_souboru")){
        if(UNICODE_HODNOTA(Název,"Zápis")&&UNICODE_HODNOTA(popisovač_data,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_HODNOTA(Název,"Čtení")&&UNICODE_HODNOTA(popisovač_data,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    informační_systémy_neplatný=1;
}
static void kompilovat_metoda(unsigned VYHLEDAT_INDEX){
    metoda_položka*Skupina_změnit_velikost=메소드목록+VYHLEDAT_INDEX;if(UNICODE_HODNOTA(Skupina_změnit_velikost->Název,"<init>"))return;int VÝSLEDEK,zboží_POČET=popisovač_položka(Skupina_změnit_velikost->popisovač_data,&VÝSLEDEK);if(zboží_POČET<0){informační_systémy_neplatný=1;return;}
    내보내기("static W m%u(",VYHLEDAT_INDEX);for(int 순번=0;순번<zboží_POČET;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!zboží_POČET)내보내기("void");
    if((unsigned)zboží_POČET>Skupina_změnit_velikost->지역변수들){informační_systémy_neplatný=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Skupina_změnit_velikost->지역변수들?Skupina_změnit_velikost->지역변수들:1);for(int 순번=0;순번<zboží_POČET;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=délka_HODNOTA;délka_HODNOTA=Skupina_změnit_velikost->명령열+Skupina_změnit_velikost->Velikost;dobrá_pozice=Skupina_změnit_velikost->명령열;
    while(dobrá_pozice<délka_HODNOTA&&!informační_systémy_neplatný){unsigned příkaz_pozice=dobrá_pozice-Skupina_změnit_velikost->명령열,operace_HODNOTA=bajt_data();내보내기("L%u:;",příkaz_pozice);
        if(operace_HODNOTA==0){}
        else if(operace_HODNOTA==1)내보내기("P(0);");
        else if(operace_HODNOTA>=2&&operace_HODNOTA<=8)내보내기("P(%uU);",operace_HODNOTA-3);
        else if(operace_HODNOTA==16){int HODNOTA=(int8_t)bajt_data();내보내기("P(%uU);",(unsigned)HODNOTA);}
        else if(operace_HODNOTA==17){int HODNOTA=(int16_t)절반값();내보내기("P(%uU);",(unsigned)HODNOTA);}
        else if(operace_HODNOTA==18||operace_HODNOTA==19)konstanta_HODNOTA(operace_HODNOTA==18?bajt_data():절반값());
        else if(operace_HODNOTA==21||operace_HODNOTA==25){unsigned 순번=bajt_data();if(순번>=Skupina_změnit_velikost->지역변수들)informační_systémy_neplatný=1;내보내기("P(v[%u]);",순번);}
        else if((operace_HODNOTA>=26&&operace_HODNOTA<=29)||(operace_HODNOTA>=42&&operace_HODNOTA<=45)){unsigned 순번=operace_HODNOTA>=42?operace_HODNOTA-42:operace_HODNOTA-26;if(순번>=Skupina_změnit_velikost->지역변수들)informační_systémy_neplatný=1;내보내기("P(v[%u]);",순번);}
        else if(operace_HODNOTA==54||operace_HODNOTA==58){unsigned 순번=bajt_data();if(순번>=Skupina_změnit_velikost->지역변수들)informační_systémy_neplatný=1;내보내기("v[%u]=Q();",순번);}
        else if((operace_HODNOTA>=59&&operace_HODNOTA<=62)||(operace_HODNOTA>=75&&operace_HODNOTA<=78)){unsigned 순번=operace_HODNOTA>=75?operace_HODNOTA-75:operace_HODNOTA-59;if(순번>=Skupina_změnit_velikost->지역변수들)informační_systémy_neplatný=1;내보내기("v[%u]=Q();",순번);}
        else if(operace_HODNOTA==46||operace_HODNOTA==50||operace_HODNOTA==51||operace_HODNOTA==52||operace_HODNOTA==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operace_HODNOTA==79||operace_HODNOTA==83||operace_HODNOTA==84||operace_HODNOTA==85||operace_HODNOTA==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operace_HODNOTA==84?"(unsigned)(signed char)q":operace_HODNOTA==85?"(unsigned short)q":operace_HODNOTA==86?"(unsigned)(short)q":"q");
        else if(operace_HODNOTA==87)내보내기("Q();");
        else if(operace_HODNOTA==89)내보내기("q=Q();P(q);P(q);");
        else if(operace_HODNOTA==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operace_HODNOTA==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(operace_HODNOTA==96||operace_HODNOTA==100||operace_HODNOTA==104||operace_HODNOTA==120||operace_HODNOTA==124||operace_HODNOTA==126||operace_HODNOTA==128||operace_HODNOTA==130){const char*Encoding_HODNOTA=operace_HODNOTA==96?"+":operace_HODNOTA==100?"-":operace_HODNOTA==104?"*":operace_HODNOTA==120?"<<":operace_HODNOTA==124?">>":operace_HODNOTA==126?"&":operace_HODNOTA==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",Encoding_HODNOTA,operace_HODNOTA==120||operace_HODNOTA==124?"%32":"");}
        else if(operace_HODNOTA==108||operace_HODNOTA==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operace_HODNOTA==112);
        else if(operace_HODNOTA==116)내보내기("P(0U-(unsigned)Q());");
        else if(operace_HODNOTA==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operace_HODNOTA==132){unsigned 순번=bajt_data();int 차이=(int8_t)bajt_data();if(순번>=Skupina_změnit_velikost->지역변수들)informační_systémy_neplatný=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operace_HODNOTA>=145&&operace_HODNOTA<=147)내보내기("P((unsigned)(%s)Q());",operace_HODNOTA==145?"signed char":operace_HODNOTA==146?"unsigned short":"short");
        else if(operace_HODNOTA>=153&&operace_HODNOTA<=166){int cílová_úroveň=(int)příkaz_pozice+(int16_t)절반값();const char*Porovnání_HODNOTA[]={"==","!=","<",">=",">","<="};if(cílová_úroveň<0||cílová_úroveň>=(int)Skupina_změnit_velikost->Velikost){informační_systémy_neplatný=1;break;}if(operace_HODNOTA<159)내보내기("if((int)Q()%s0)goto L%d;",Porovnání_HODNOTA[operace_HODNOTA-153],cílová_úroveň);else if(operace_HODNOTA<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Porovnání_HODNOTA[operace_HODNOTA-159],cílová_úroveň);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operace_HODNOTA==165?"==":"!=",cílová_úroveň);}
        else if(operace_HODNOTA==167){int cílová_úroveň=(int)příkaz_pozice+(int16_t)절반값();if(cílová_úroveň<0||cílová_úroveň>=(int)Skupina_změnit_velikost->Velikost)informační_systémy_neplatný=1;내보내기("goto L%d;",cílová_úroveň);}
        else if(operace_HODNOTA==172||operace_HODNOTA==176)내보내기("return Q();");else if(operace_HODNOTA==177)내보내기("return 0;");
        else if(operace_HODNOTA==178||operace_HODNOTA==179){unsigned identifikátor_HODNOTA=절반값();if(identifikátor_HODNOTA<1||identifikátor_HODNOTA>=konstanta_fond||Značky_Seznam[identifikátor_HODNOTA]!=9||첫째값[identifikátor_HODNOTA]>=konstanta_fond||SEKUNDA_HODNOTA[identifikátor_HODNOTA]>=konstanta_fond||Značky_Seznam[첫째값[identifikátor_HODNOTA]]!=7||Značky_Seznam[SEKUNDA_HODNOTA[identifikátor_HODNOTA]]!=12){informační_systémy_neplatný=1;break;}unsigned vlastník_objekt=첫째값[첫째값[identifikátor_HODNOTA]],Název=첫째값[SEKUNDA_HODNOTA[identifikátor_HODNOTA]],popisovač_data=SEKUNDA_HODNOTA[SEKUNDA_HODNOTA[identifikátor_HODNOTA]];
            if(operace_HODNOTA==178&&UNICODE_HODNOTA(vlastník_objekt,"java/lang/System")&&UNICODE_HODNOTA(Název,"out")&&UNICODE_HODNOTA(popisovač_data,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Soubor_položka=0;while(Soubor_položka<필드개수&&(!같음(Název,název_pole_98daa19b[Soubor_položka])||!같음(popisovač_data,pole_popisovač[Soubor_položka])))Soubor_položka++;if(!같음(vlastník_objekt,첫째값[dobrá_Třída])||Soubor_položka==필드개수){informační_systémy_neplatný=1;break;}내보내기(operace_HODNOTA==178?"P(fields[%u]);":"fields[%u]=Q();",Soubor_položka);}}
        else if(operace_HODNOTA==182||operace_HODNOTA==184)호출(절반값(),operace_HODNOTA==182);
        else if(operace_HODNOTA==188){unsigned TYP_oblast=bajt_data();if(TYP_oblast!=4&&TYP_oblast!=5&&TYP_oblast!=8&&TYP_oblast!=9&&TYP_oblast!=10)informační_systémy_neplatný=1;내보내기("P(jarray((int)Q()));");}
        else if(operace_HODNOTA==190)내보내기("P(jlength(Q()));");
        else if(operace_HODNOTA==198||operace_HODNOTA==199){int cílová_úroveň=(int)příkaz_pozice+(int16_t)절반값();if(cílová_úroveň<0||cílová_úroveň>=(int)Skupina_změnit_velikost->Velikost)informační_systémy_neplatný=1;내보내기("if(Q()%s0)goto L%d;",operace_HODNOTA==198?"==":"!=",cílová_úroveň);}
        else informační_systémy_neplatný=1;
        if(informační_systémy_neplatný)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",VYHLEDAT_INDEX,operace_HODNOTA,příkaz_pozice);
        내보내기("\n");
    }
    délka_HODNOTA=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned řetězec_lekce(unsigned *data_pozice,unsigned konec_POSUN){
    if(*data_pozice>=konec_POSUN){informační_systémy_neplatný=1;return 0;}unsigned bod_kódu=data[(*data_pozice)++];
    if(bod_kódu<128)return bod_kódu;
    unsigned zboží_POČET=bod_kódu>=0xc0&&bod_kódu<=0xdf?1:bod_kódu>=0xe0&&bod_kódu<=0xef?2:3;
    if(zboží_POČET==3||zboží_POČET>konec_POSUN-*data_pozice){informační_systémy_neplatný=1;return 0;}unsigned HODNOTA=bod_kódu&((1u<<(6-zboží_POČET))-1);
    for(unsigned 순번=0;순번<zboží_POČET;순번++){unsigned Další_zboží=data[(*data_pozice)++];if((Další_zboží&0xc0)!=0x80)informační_systémy_neplatný=1;HODNOTA=HODNOTA<<6|(Další_zboží&63);}
    if((zboží_POČET==1&&HODNOTA<128&&HODNOTA!=0)||(zboží_POČET==2&&HODNOTA<2048))informační_systémy_neplatný=1;return HODNOTA;
}
static void řetězec_konstanta(unsigned identifikátor_HODNOTA){
    unsigned 부호없는값=첫째값[identifikátor_HODNOTA];if(부호없는값<1||부호없는값>=konstanta_fond||Značky_Seznam[부호없는값]!=1){informační_systémy_neplatný=1;return;}내보내기("static const unsigned char k%u[]={",identifikátor_HODNOTA);
    unsigned data_pozice=첫째값[부호없는값],konec_POSUN=data_pozice+SEKUNDA_HODNOTA[부호없는값];
    while(data_pozice<konec_POSUN&&!informační_systémy_neplatný){unsigned bod_kódu=řetězec_lekce(&data_pozice,konec_POSUN);
        if(bod_kódu>=0xd800&&bod_kódu<=0xdbff){unsigned 낮은부분=řetězec_lekce(&data_pozice,konec_POSUN);if(낮은부분<0xdc00||낮은부분>0xdfff){informační_systémy_neplatný=1;break;}bod_kódu=0x10000+((bod_kódu-0xd800)<<10)+낮은부분-0xdc00;}
        else if(bod_kódu>=0xdc00&&bod_kódu<=0xdfff){informační_systémy_neplatný=1;break;}
        if(!bod_kódu){printf("jaot: embedded NUL string needs JVM mode\n");informační_systémy_neplatný=1;break;}
        if(bod_kódu<128)내보내기("%u,",bod_kódu);
        else{unsigned zboží_POČET=bod_kódu<2048?2:bod_kódu<65536?3:4;내보내기("%u,",(zboží_POČET==2?0xc0:zboží_POČET==3?0xe0:0xf0)|(bod_kódu>>(6*(zboží_POČET-1))));for(unsigned 순번=zboží_POČET-1;순번;순번--)내보내기("%u,",0x80|((bod_kódu>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Název){
    size_t zboží_POČET=strlen(Název);
    if(zboží_POČET>4&&!strcmp(Název+zboží_POČET-4,".jar")){
        if(꾸러미열기(Název)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char cesta_2[256];const char*položka_metoda=꾸러미진입클래스();zboží_POČET=strlen(položka_metoda);if(zboží_POČET+6>=sizeof(cesta_2))return 0;
        for(unsigned 순번=0;순번<zboží_POČET;순번++)cesta_2[순번]=položka_metoda[순번]=='.'?'/':položka_metoda[순번];strcpy(cesta_2+zboží_POČET,".class");int položka_POČET=꾸러미읽기(cesta_2,data,sizeof(data));if(položka_POČET<0)return 0;délka_HODNOTA=položka_POČET;
    }else{intptr_t popisovač_souboru=사용자호출(3,(uintptr_t)Název,0,0,0,0,0);if(popisovač_souboru<0)return 0;intptr_t položka_POČET=사용자호출(9,popisovač_souboru,0,0,0,0,0);if(položka_POČET<0||položka_POČET>sizeof(data)){사용자호출(4,popisovač_souboru,0,0,0,0,0);return 0;}intptr_t RECEIVED_POČET=사용자호출(2,popisovač_souboru,(uintptr_t)data,položka_POČET,0,0,0);사용자호출(4,popisovač_souboru,0,0,0,0,0);if(RECEIVED_POČET!=položka_POČET)return 0;délka_HODNOTA=položka_POČET;}
    if(parsovat_vstup()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstanta_fond&&!informační_systémy_neplatný;순번++)if(Značky_Seznam[순번]==8)řetězec_konstanta(순번);
    if(informační_systémy_neplatný)return 0;
    int vstupní_bod=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_HODNOTA(메소드목록[순번].Název,"<init>")){
        int VÝSLEDEK,položka_POČET=popisovač_položka(메소드목록[순번].popisovač_data,&VÝSLEDEK);if(položka_POČET<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<položka_POČET;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!položka_POČET)내보내기("void");내보내기(");\n");
        if(UNICODE_HODNOTA(메소드목록[순번].Název,"main")&&UNICODE_HODNOTA(메소드목록[순번].popisovač_data,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfigurace_BITS&9)==9)vstupní_bod=순번;
        if(UNICODE_HODNOTA(메소드목록[순번].Název,"<clinit>"))초기값=순번;
    }
    if(vstupní_bod<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!informační_systémy_neplatný;순번++)kompilovat_metoda(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(pole_konstanta[순번]){
        unsigned bod_kódu=pole_konstanta[순번];if(bod_kódu>=konstanta_fond)return 0;
        if(Značky_Seznam[bod_kódu]==3)내보내기("fields[%u]=%uU;",순번,첫째값[bod_kódu]);else if(Značky_Seznam[bod_kódu]==8)내보내기("fields[%u]=(W)k%u;",순번,bod_kódu);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",vstupní_bod);
    return informační_systémy_neplatný?0:text;
}
