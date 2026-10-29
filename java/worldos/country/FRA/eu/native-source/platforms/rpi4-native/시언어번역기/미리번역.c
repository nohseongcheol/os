#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "multzo.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char datuak[16384];static unsigned luzera_balio,현재위치;static int informatika_baliogabe;
static unsigned Etiketak_Zerrenda[512],첫째값[512],SEGUNDOA_balio[512],konstante_multzo,현재클래스;
static char Testua[65536];static unsigned Testuaren_tamaina;
typedef struct {unsigned konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna,Izena,서술값,instrukzio_SEKUENTZIA,Tamaina,지역변수들,pila_biltegi;} 메소드;
static 메소드 메소드목록[64];static unsigned 메소드개수;
static unsigned eremu_izen[64],필드서술[64],eremu_konstante[64],필드개수;
static unsigned HARTU_balio(unsigned elementu_ZENBATU){if(현재위치>luzera_balio||elementu_ZENBATU>luzera_balio-현재위치){informatika_baliogabe=1;return 0;}unsigned datuak_kargu=현재위치;현재위치+=elementu_ZENBATU;return datuak_kargu;}
static unsigned byte_datuak(void){unsigned datuak_kargu=HARTU_balio(1);return informatika_baliogabe?0:datuak[datuak_kargu];}
static unsigned 절반값(void){unsigned X_koordenatu=byte_datuak();return X_koordenatu<<8|byte_datuak();}
static uint32_t 가득참(void){uint32_t X_koordenatu=절반값();return X_koordenatu<<16|절반값();}
static int UNICODE_balio(unsigned 순번,const char*kate_datuak){return 순번>0&&순번<konstante_multzo&&Etiketak_Zerrenda[순번]==1&&strlen(kate_datuak)==SEGUNDOA_balio[순번]&&!memcmp(datuak+첫째값[순번],kate_datuak,SEGUNDOA_balio[순번]);}
static int 같음(unsigned X_koordenatu,unsigned Y_koordenatu){return X_koordenatu>0&&X_koordenatu<konstante_multzo&&Y_koordenatu>0&&Y_koordenatu<konstante_multzo&&Etiketak_Zerrenda[X_koordenatu]==1&&Etiketak_Zerrenda[Y_koordenatu]==1&&SEGUNDOA_balio[X_koordenatu]==SEGUNDOA_balio[Y_koordenatu]&&!memcmp(datuak+첫째값[X_koordenatu],datuak+첫째값[Y_koordenatu],SEGUNDOA_balio[X_koordenatu]);}
static void 내보내기(const char*fitxategi_sarrera,...){if(informatika_baliogabe)return;va_list arg_matrize;va_start(arg_matrize,fitxategi_sarrera);int elementu_ZENBATU=vsnprintf(Testua+Testuaren_tamaina,sizeof(Testua)-Testuaren_tamaina,fitxategi_sarrera,arg_matrize);va_end(arg_matrize);if(elementu_ZENBATU<0||(unsigned)elementu_ZENBATU>=sizeof(Testua)-Testuaren_tamaina){informatika_baliogabe=1;return;}Testuaren_tamaina+=elementu_ZENBATU;}
static int 서술자(unsigned identifikatzaile_balio,int*EMAITZA){
    if(identifikatzaile_balio<1||identifikatzaile_balio>=konstante_multzo||Etiketak_Zerrenda[identifikatzaile_balio]!=1)return -1;unsigned datuak_kargu=첫째값[identifikatzaile_balio],amaitu_Geruzak=datuak_kargu+SEGUNDOA_balio[identifikatzaile_balio];if(datuak_kargu>=amaitu_Geruzak||datuak[datuak_kargu++]!='(')return -1;int sarrera_ZENBATU=0;
    while(datuak_kargu<amaitu_Geruzak&&datuak[datuak_kargu]!=')'){
        unsigned karaktere_kode=datuak[datuak_kargu++];while(karaktere_kode=='['&&datuak_kargu<amaitu_Geruzak)karaktere_kode=datuak[datuak_kargu++];
        if(karaktere_kode=='L'){while(datuak_kargu<amaitu_Geruzak&&datuak[datuak_kargu]!=';')datuak_kargu++;if(datuak_kargu==amaitu_Geruzak)return -1;datuak_kargu++;}
        else if(karaktere_kode!='I'&&karaktere_kode!='Z'&&karaktere_kode!='B'&&karaktere_kode!='C'&&karaktere_kode!='S')return -1;
        if(++sarrera_ZENBATU>16)return -1;
    }
    if(datuak_kargu+1>=amaitu_Geruzak||datuak[datuak_kargu++]!=')')return -1;*EMAITZA=datuak[datuak_kargu]=='V'?0:1;
    if(datuak[datuak_kargu]=='J'||datuak[datuak_kargu]=='D'||datuak[datuak_kargu]=='F')return -1;return sarrera_ZENBATU;
}
static void atributuak(void){unsigned elementu_ZENBATU=절반값();for(unsigned 순번=0;순번<elementu_ZENBATU&&!informatika_baliogabe;순번++){절반값();unsigned Tamaina=가득참();HARTU_balio(Tamaina);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned adingabe_bertsio=절반값(),판번호=절반값();if(adingabe_bertsio||판번호<45||판번호>52)return -1;
    konstante_multzo=절반값();if(konstante_multzo<1||konstante_multzo>512)return -1;
    for(unsigned 순번=1;순번<konstante_multzo&&!informatika_baliogabe;순번++){
        Etiketak_Zerrenda[순번]=byte_datuak();switch(Etiketak_Zerrenda[순번]){
        case 1:SEGUNDOA_balio[순번]=절반값();첫째값[순번]=HARTU_balio(SEGUNDOA_balio[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:HARTU_balio(8);if(++순번>=konstante_multzo)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SEGUNDOA_balio[순번]=절반값();break;
        case 15:첫째값[순번]=byte_datuak();SEGUNDOA_balio[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=konstante_multzo||Etiketak_Zerrenda[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=konstante_multzo||Etiketak_Zerrenda[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();HARTU_balio(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!informatika_baliogabe;순번++){
        unsigned konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna=절반값();eremu_izen[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna&8))return -1;
        unsigned sarrera_ZENBATU=절반값();for(unsigned 안쪽순번=0;안쪽순번<sarrera_ZENBATU&&!informatika_baliogabe;안쪽순번++){
            unsigned Izena=절반값(),Tamaina=가득참();
            if(UNICODE_balio(Izena,"ConstantValue")){if(Tamaina!=2)return -1;eremu_konstante[순번]=절반값();}
            else HARTU_balio(Tamaina);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!informatika_baliogabe;순번++){
        메소드*묶음수=메소드목록+순번;묶음수->konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna=절반값();묶음수->Izena=절반값();묶음수->서술값=절반값();unsigned sarrera_ZENBATU=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<sarrera_ZENBATU&&!informatika_baliogabe;안쪽순번++){
            unsigned Izena=절반값(),Tamaina=가득참(),Exekutatu_2=현재위치;
            if(Tamaina>luzera_balio-현재위치)return -1;
            if(UNICODE_balio(Izena,"Code")){
                묶음수->pila_biltegi=절반값();묶음수->지역변수들=절반값();묶음수->Tamaina=가득참();묶음수->instrukzio_SEKUENTZIA=HARTU_balio(묶음수->Tamaina);
                if(묶음수->pila_biltegi>128||묶음수->지역변수들>128||묶음수->Tamaina>8192||절반값())return -1;atributuak();
            }else HARTU_balio(Tamaina);
            if(현재위치!=Exekutatu_2+Tamaina)return -1;
        }
        if(!UNICODE_balio(묶음수->Izena,"<init>")&&(!(묶음수->konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna&8)||(묶음수->konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna&(0x100|0x20))||!묶음수->Tamaina))return -1;
    }
    atributuak();return informatika_baliogabe||현재위치!=luzera_balio?-1:0;
}
static void konstante_balio(unsigned identifikatzaile_balio){
    if(!identifikatzaile_balio||identifikatzaile_balio>=konstante_multzo){informatika_baliogabe=1;return;}
    if(Etiketak_Zerrenda[identifikatzaile_balio]==3)내보내기("P(%uU);",첫째값[identifikatzaile_balio]);
    else if(Etiketak_Zerrenda[identifikatzaile_balio]==8)내보내기("P((W)k%u);",identifikatzaile_balio);else informatika_baliogabe=1;
}
static void 호출(unsigned identifikatzaile_balio,int birtual_dei){
    if(identifikatzaile_balio<1||identifikatzaile_balio>=konstante_multzo||(Etiketak_Zerrenda[identifikatzaile_balio]!=10&&Etiketak_Zerrenda[identifikatzaile_balio]!=11)||첫째값[identifikatzaile_balio]<1||첫째값[identifikatzaile_balio]>=konstante_multzo||Etiketak_Zerrenda[첫째값[identifikatzaile_balio]]!=7||SEGUNDOA_balio[identifikatzaile_balio]<1||SEGUNDOA_balio[identifikatzaile_balio]>=konstante_multzo||Etiketak_Zerrenda[SEGUNDOA_balio[identifikatzaile_balio]]!=12){informatika_baliogabe=1;return;}
    unsigned jabe_objektu=첫째값[첫째값[identifikatzaile_balio]],Izena=첫째값[SEGUNDOA_balio[identifikatzaile_balio]],서술값=SEGUNDOA_balio[SEGUNDOA_balio[identifikatzaile_balio]];int EMAITZA=0,elementu_ZENBATU=서술자(서술값,&EMAITZA);if(elementu_ZENBATU<0){informatika_baliogabe=1;return;}
    for(int 순번=elementu_ZENBATU;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(birtual_dei)내보내기("Q();");
    if(!birtual_dei&&같음(jabe_objektu,첫째값[현재클래스])){
        unsigned 묶음수=0;for(;묶음수<메소드개수;묶음수++)if(같음(Izena,메소드목록[묶음수].Izena)&&같음(서술값,메소드목록[묶음수].서술값))break;
        if(묶음수==메소드개수||!(메소드목록[묶음수].konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna&8)){informatika_baliogabe=1;return;}
        if(EMAITZA)내보내기("P(");내보내기("m%u(",묶음수);for(int 순번=0;순번<elementu_ZENBATU;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(EMAITZA?"));":" );");return;
    }
    if((birtual_dei&&UNICODE_balio(jabe_objektu,"java/io/PrintStream")&& (UNICODE_balio(Izena,"print")||UNICODE_balio(Izena,"println")))||(!birtual_dei&&UNICODE_balio(jabe_objektu,"Euskara/자체/Irteera"))){
        if(UNICODE_balio(서술값,"(I)V")&&(UNICODE_balio(Izena,"print")||UNICODE_balio(Izena,"println")||UNICODE_balio(Izena,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_balio(Izena,"print")?0:1);return;}
        if(UNICODE_balio(서술값,"(Ljava/lang/String;)V")&&(UNICODE_balio(Izena,"print")||UNICODE_balio(Izena,"println")||UNICODE_balio(Izena,"Idatzi")||UNICODE_balio(Izena,"idatzi_lerro"))){내보내기("jprint(x[0],0,%d);",UNICODE_balio(Izena,"print")||UNICODE_balio(Izena,"Idatzi")?0:1);return;}
        if(UNICODE_balio(서술값,"()V")&&UNICODE_balio(Izena,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!birtual_dei&&UNICODE_balio(jabe_objektu,"Euskara/자체/Fitxategia")){
        if(UNICODE_balio(Izena,"Idatzi")&&UNICODE_balio(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_balio(Izena,"Irakurri")&&UNICODE_balio(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    informatika_baliogabe=1;
}
static void 메소드번역(unsigned BEGIRATU_INDIZE){
    메소드*묶음수=메소드목록+BEGIRATU_INDIZE;if(UNICODE_balio(묶음수->Izena,"<init>"))return;int EMAITZA,elementu_ZENBATU=서술자(묶음수->서술값,&EMAITZA);if(elementu_ZENBATU<0){informatika_baliogabe=1;return;}
    내보내기("static W m%u(",BEGIRATU_INDIZE);for(int 순번=0;순번<elementu_ZENBATU;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!elementu_ZENBATU)내보내기("void");
    if((unsigned)elementu_ZENBATU>묶음수->지역변수들){informatika_baliogabe=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",묶음수->지역변수들?묶음수->지역변수들:1);for(int 순번=0;순번<elementu_ZENBATU;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=luzera_balio;luzera_balio=묶음수->instrukzio_SEKUENTZIA+묶음수->Tamaina;현재위치=묶음수->instrukzio_SEKUENTZIA;
    while(현재위치<luzera_balio&&!informatika_baliogabe){unsigned komando_kargu=현재위치-묶음수->instrukzio_SEKUENTZIA,kirurgia_balio=byte_datuak();내보내기("L%u:;",komando_kargu);
        if(kirurgia_balio==0){}
        else if(kirurgia_balio==1)내보내기("P(0);");
        else if(kirurgia_balio>=2&&kirurgia_balio<=8)내보내기("P(%uU);",kirurgia_balio-3);
        else if(kirurgia_balio==16){int balio=(int8_t)byte_datuak();내보내기("P(%uU);",(unsigned)balio);}
        else if(kirurgia_balio==17){int balio=(int16_t)절반값();내보내기("P(%uU);",(unsigned)balio);}
        else if(kirurgia_balio==18||kirurgia_balio==19)konstante_balio(kirurgia_balio==18?byte_datuak():절반값());
        else if(kirurgia_balio==21||kirurgia_balio==25){unsigned 순번=byte_datuak();if(순번>=묶음수->지역변수들)informatika_baliogabe=1;내보내기("P(v[%u]);",순번);}
        else if((kirurgia_balio>=26&&kirurgia_balio<=29)||(kirurgia_balio>=42&&kirurgia_balio<=45)){unsigned 순번=kirurgia_balio>=42?kirurgia_balio-42:kirurgia_balio-26;if(순번>=묶음수->지역변수들)informatika_baliogabe=1;내보내기("P(v[%u]);",순번);}
        else if(kirurgia_balio==54||kirurgia_balio==58){unsigned 순번=byte_datuak();if(순번>=묶음수->지역변수들)informatika_baliogabe=1;내보내기("v[%u]=Q();",순번);}
        else if((kirurgia_balio>=59&&kirurgia_balio<=62)||(kirurgia_balio>=75&&kirurgia_balio<=78)){unsigned 순번=kirurgia_balio>=75?kirurgia_balio-75:kirurgia_balio-59;if(순번>=묶음수->지역변수들)informatika_baliogabe=1;내보내기("v[%u]=Q();",순번);}
        else if(kirurgia_balio==46||kirurgia_balio==50||kirurgia_balio==51||kirurgia_balio==52||kirurgia_balio==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(kirurgia_balio==79||kirurgia_balio==83||kirurgia_balio==84||kirurgia_balio==85||kirurgia_balio==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",kirurgia_balio==84?"(unsigned)(signed char)q":kirurgia_balio==85?"(unsigned short)q":kirurgia_balio==86?"(unsigned)(short)q":"q");
        else if(kirurgia_balio==87)내보내기("Q();");
        else if(kirurgia_balio==89)내보내기("q=Q();P(q);P(q);");
        else if(kirurgia_balio==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(kirurgia_balio==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(kirurgia_balio==96||kirurgia_balio==100||kirurgia_balio==104||kirurgia_balio==120||kirurgia_balio==124||kirurgia_balio==126||kirurgia_balio==128||kirurgia_balio==130){const char*kodeketa_balio=kirurgia_balio==96?"+":kirurgia_balio==100?"-":kirurgia_balio==104?"*":kirurgia_balio==120?"<<":kirurgia_balio==124?">>":kirurgia_balio==126?"&":kirurgia_balio==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kodeketa_balio,kirurgia_balio==120||kirurgia_balio==124?"%32":"");}
        else if(kirurgia_balio==108||kirurgia_balio==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",kirurgia_balio==112);
        else if(kirurgia_balio==116)내보내기("P(0U-(unsigned)Q());");
        else if(kirurgia_balio==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(kirurgia_balio==132){unsigned 순번=byte_datuak();int 차이=(int8_t)byte_datuak();if(순번>=묶음수->지역변수들)informatika_baliogabe=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(kirurgia_balio>=145&&kirurgia_balio<=147)내보내기("P((unsigned)(%s)Q());",kirurgia_balio==145?"signed char":kirurgia_balio==146?"unsigned short":"short");
        else if(kirurgia_balio>=153&&kirurgia_balio<=166){int helburu_balio=(int)komando_kargu+(int16_t)절반값();const char*Konparazioa_balio[]={"==","!=","<",">=",">","<="};if(helburu_balio<0||helburu_balio>=(int)묶음수->Tamaina){informatika_baliogabe=1;break;}if(kirurgia_balio<159)내보내기("if((int)Q()%s0)goto L%d;",Konparazioa_balio[kirurgia_balio-153],helburu_balio);else if(kirurgia_balio<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Konparazioa_balio[kirurgia_balio-159],helburu_balio);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",kirurgia_balio==165?"==":"!=",helburu_balio);}
        else if(kirurgia_balio==167){int helburu_balio=(int)komando_kargu+(int16_t)절반값();if(helburu_balio<0||helburu_balio>=(int)묶음수->Tamaina)informatika_baliogabe=1;내보내기("goto L%d;",helburu_balio);}
        else if(kirurgia_balio==172||kirurgia_balio==176)내보내기("return Q();");else if(kirurgia_balio==177)내보내기("return 0;");
        else if(kirurgia_balio==178||kirurgia_balio==179){unsigned identifikatzaile_balio=절반값();if(identifikatzaile_balio<1||identifikatzaile_balio>=konstante_multzo||Etiketak_Zerrenda[identifikatzaile_balio]!=9||첫째값[identifikatzaile_balio]>=konstante_multzo||SEGUNDOA_balio[identifikatzaile_balio]>=konstante_multzo||Etiketak_Zerrenda[첫째값[identifikatzaile_balio]]!=7||Etiketak_Zerrenda[SEGUNDOA_balio[identifikatzaile_balio]]!=12){informatika_baliogabe=1;break;}unsigned jabe_objektu=첫째값[첫째값[identifikatzaile_balio]],Izena=첫째값[SEGUNDOA_balio[identifikatzaile_balio]],서술값=SEGUNDOA_balio[SEGUNDOA_balio[identifikatzaile_balio]];
            if(kirurgia_balio==178&&UNICODE_balio(jabe_objektu,"java/lang/System")&&UNICODE_balio(Izena,"out")&&UNICODE_balio(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned fitxategi_sarrera=0;while(fitxategi_sarrera<필드개수&&(!같음(Izena,eremu_izen[fitxategi_sarrera])||!같음(서술값,필드서술[fitxategi_sarrera])))fitxategi_sarrera++;if(!같음(jabe_objektu,첫째값[현재클래스])||fitxategi_sarrera==필드개수){informatika_baliogabe=1;break;}내보내기(kirurgia_balio==178?"P(fields[%u]);":"fields[%u]=Q();",fitxategi_sarrera);}}
        else if(kirurgia_balio==182||kirurgia_balio==184)호출(절반값(),kirurgia_balio==182);
        else if(kirurgia_balio==188){unsigned MOTA_Kategoria=byte_datuak();if(MOTA_Kategoria!=4&&MOTA_Kategoria!=5&&MOTA_Kategoria!=8&&MOTA_Kategoria!=9&&MOTA_Kategoria!=10)informatika_baliogabe=1;내보내기("P(jarray((int)Q()));");}
        else if(kirurgia_balio==190)내보내기("P(jlength(Q()));");
        else if(kirurgia_balio==198||kirurgia_balio==199){int helburu_balio=(int)komando_kargu+(int16_t)절반값();if(helburu_balio<0||helburu_balio>=(int)묶음수->Tamaina)informatika_baliogabe=1;내보내기("if(Q()%s0)goto L%d;",kirurgia_balio==198?"==":"!=",helburu_balio);}
        else informatika_baliogabe=1;
        if(informatika_baliogabe)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",BEGIRATU_INDIZE,kirurgia_balio,komando_kargu);
        내보내기("\n");
    }
    luzera_balio=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned kate_unitate(unsigned *datuak_kargu,unsigned amaitu_Geruzak){
    if(*datuak_kargu>=amaitu_Geruzak){informatika_baliogabe=1;return 0;}unsigned karaktere_kode=datuak[(*datuak_kargu)++];
    if(karaktere_kode<128)return karaktere_kode;
    unsigned elementu_ZENBATU=karaktere_kode>=0xc0&&karaktere_kode<=0xdf?1:karaktere_kode>=0xe0&&karaktere_kode<=0xef?2:3;
    if(elementu_ZENBATU==3||elementu_ZENBATU>amaitu_Geruzak-*datuak_kargu){informatika_baliogabe=1;return 0;}unsigned balio=karaktere_kode&((1u<<(6-elementu_ZENBATU))-1);
    for(unsigned 순번=0;순번<elementu_ZENBATU;순번++){unsigned Hurrengoa_elementu=datuak[(*datuak_kargu)++];if((Hurrengoa_elementu&0xc0)!=0x80)informatika_baliogabe=1;balio=balio<<6|(Hurrengoa_elementu&63);}
    if((elementu_ZENBATU==1&&balio<128&&balio!=0)||(elementu_ZENBATU==2&&balio<2048))informatika_baliogabe=1;return balio;
}
static void kate_konstante(unsigned identifikatzaile_balio){
    unsigned 부호없는값=첫째값[identifikatzaile_balio];if(부호없는값<1||부호없는값>=konstante_multzo||Etiketak_Zerrenda[부호없는값]!=1){informatika_baliogabe=1;return;}내보내기("static const unsigned char k%u[]={",identifikatzaile_balio);
    unsigned datuak_kargu=첫째값[부호없는값],amaitu_Geruzak=datuak_kargu+SEGUNDOA_balio[부호없는값];
    while(datuak_kargu<amaitu_Geruzak&&!informatika_baliogabe){unsigned karaktere_kode=kate_unitate(&datuak_kargu,amaitu_Geruzak);
        if(karaktere_kode>=0xd800&&karaktere_kode<=0xdbff){unsigned 낮은부분=kate_unitate(&datuak_kargu,amaitu_Geruzak);if(낮은부분<0xdc00||낮은부분>0xdfff){informatika_baliogabe=1;break;}karaktere_kode=0x10000+((karaktere_kode-0xd800)<<10)+낮은부분-0xdc00;}
        else if(karaktere_kode>=0xdc00&&karaktere_kode<=0xdfff){informatika_baliogabe=1;break;}
        if(!karaktere_kode){printf("jaot: embedded NUL string needs JVM mode\n");informatika_baliogabe=1;break;}
        if(karaktere_kode<128)내보내기("%u,",karaktere_kode);
        else{unsigned elementu_ZENBATU=karaktere_kode<2048?2:karaktere_kode<65536?3:4;내보내기("%u,",(elementu_ZENBATU==2?0xc0:elementu_ZENBATU==3?0xe0:0xf0)|(karaktere_kode>>(6*(elementu_ZENBATU-1))));for(unsigned 순번=elementu_ZENBATU-1;순번;순번--)내보내기("%u,",0x80|((karaktere_kode>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Izena){
    size_t elementu_ZENBATU=strlen(Izena);
    if(elementu_ZENBATU>4&&!strcmp(Izena+elementu_ZENBATU-4,".jar")){
        if(꾸러미열기(Izena)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Bide_izena[256];const char*진입함수=꾸러미진입클래스();elementu_ZENBATU=strlen(진입함수);if(elementu_ZENBATU+6>=sizeof(Bide_izena))return 0;
        for(unsigned 순번=0;순번<elementu_ZENBATU;순번++)Bide_izena[순번]=진입함수[순번]=='.'?'/':진입함수[순번];strcpy(Bide_izena+elementu_ZENBATU,".class");int sarrera_ZENBATU=꾸러미읽기(Bide_izena,datuak,sizeof(datuak));if(sarrera_ZENBATU<0)return 0;luzera_balio=sarrera_ZENBATU;
    }else{intptr_t fitxategi_helduleku=사용자호출(3,(uintptr_t)Izena,0,0,0,0,0);if(fitxategi_helduleku<0)return 0;intptr_t sarrera_ZENBATU=사용자호출(9,fitxategi_helduleku,0,0,0,0,0);if(sarrera_ZENBATU<0||sarrera_ZENBATU>sizeof(datuak)){사용자호출(4,fitxategi_helduleku,0,0,0,0,0);return 0;}intptr_t RECEIVED_ZENBATU=사용자호출(2,fitxategi_helduleku,(uintptr_t)datuak,sarrera_ZENBATU,0,0,0);사용자호출(4,fitxategi_helduleku,0,0,0,0,0);if(RECEIVED_ZENBATU!=sarrera_ZENBATU)return 0;luzera_balio=sarrera_ZENBATU;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstante_multzo&&!informatika_baliogabe;순번++)if(Etiketak_Zerrenda[순번]==8)kate_konstante(순번);
    if(informatika_baliogabe)return 0;
    int sarrera_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_balio(메소드목록[순번].Izena,"<init>")){
        int EMAITZA,sarrera_ZENBATU=서술자(메소드목록[순번].서술값,&EMAITZA);if(sarrera_ZENBATU<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<sarrera_ZENBATU;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!sarrera_ZENBATU)내보내기("void");내보내기(");\n");
        if(UNICODE_balio(메소드목록[순번].Izena,"main")&&UNICODE_balio(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna&9)==9)sarrera_p=순번;
        if(UNICODE_balio(메소드목록[순번].Izena,"<clinit>"))초기값=순번;
    }
    if(sarrera_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!informatika_baliogabe;순번++)메소드번역(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(eremu_konstante[순번]){
        unsigned karaktere_kode=eremu_konstante[순번];if(karaktere_kode>=konstante_multzo)return 0;
        if(Etiketak_Zerrenda[karaktere_kode]==3)내보내기("fields[%u]=%uU;",순번,첫째값[karaktere_kode]);else if(Etiketak_Zerrenda[karaktere_kode]==8)내보내기("fields[%u]=(W)k%u;",순번,karaktere_kode);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",sarrera_p);
    return informatika_baliogabe?0:Testua;
}
