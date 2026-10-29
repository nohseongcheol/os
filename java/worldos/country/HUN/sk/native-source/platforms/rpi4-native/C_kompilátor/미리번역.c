#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "zväzok.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char údaje[16384];static unsigned dĺžka_VALUE,v_termíne_splatnosti_pozícia;static int Informačné_systémy_neplatné;
static unsigned Kategórie_Zoznam[512],첫째값[512],SECOND_VALUE[512],konštanta_fond,v_termíne_splatnosti_lekcia;
static char Spracovanie_textu[65536];static unsigned Veľkosť_textu;
typedef struct {unsigned konfigurácia_Background_Intelligent_Transfer_Service,Názov,서술값,inštrukcia_SEQUENCE,Veľkosť,지역변수들,Vrstvy_Úložisko;} metóda_položka;
static metóda_položka 메소드목록[64];static unsigned 메소드개수;
static unsigned názov_poľa[64],필드서술[64],pole_konštanta[64],필드개수;
static unsigned TAKE_VALUE(unsigned položka_COUNT){if(v_termíne_splatnosti_pozícia>dĺžka_VALUE||položka_COUNT>dĺžka_VALUE-v_termíne_splatnosti_pozícia){Informačné_systémy_neplatné=1;return 0;}unsigned údaje_pozícia=v_termíne_splatnosti_pozícia;v_termíne_splatnosti_pozícia+=položka_COUNT;return údaje_pozícia;}
static unsigned Byte_údaje(void){unsigned údaje_pozícia=TAKE_VALUE(1);return Informačné_systémy_neplatné?0:údaje[údaje_pozícia];}
static unsigned 절반값(void){unsigned X_súradnica=Byte_údaje();return X_súradnica<<8|Byte_údaje();}
static uint32_t 가득참(void){uint32_t X_súradnica=절반값();return X_súradnica<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*reťazec_údaje){return 순번>0&&순번<konštanta_fond&&Kategórie_Zoznam[순번]==1&&strlen(reťazec_údaje)==SECOND_VALUE[순번]&&!memcmp(údaje+첫째값[순번],reťazec_údaje,SECOND_VALUE[순번]);}
static int 같음(unsigned X_súradnica,unsigned Y_súradnica){return X_súradnica>0&&X_súradnica<konštanta_fond&&Y_súradnica>0&&Y_súradnica<konštanta_fond&&Kategórie_Zoznam[X_súradnica]==1&&Kategórie_Zoznam[Y_súradnica]==1&&SECOND_VALUE[X_súradnica]==SECOND_VALUE[Y_súradnica]&&!memcmp(údaje+첫째값[X_súradnica],údaje+첫째값[Y_súradnica],SECOND_VALUE[X_súradnica]);}
static void 내보내기(const char*Súbor_položka,...){if(Informačné_systémy_neplatné)return;va_list argument_pole;va_start(argument_pole,Súbor_položka);int položka_COUNT=vsnprintf(Spracovanie_textu+Veľkosť_textu,sizeof(Spracovanie_textu)-Veľkosť_textu,Súbor_položka,argument_pole);va_end(argument_pole);if(položka_COUNT<0||(unsigned)položka_COUNT>=sizeof(Spracovanie_textu)-Veľkosť_textu){Informačné_systémy_neplatné=1;return;}Veľkosť_textu+=položka_COUNT;}
static int 서술자(unsigned identifikátor_VALUE,int*KR){
    if(identifikátor_VALUE<1||identifikátor_VALUE>=konštanta_fond||Kategórie_Zoznam[identifikátor_VALUE]!=1)return -1;unsigned údaje_pozícia=첫째값[identifikátor_VALUE],ukončiť_hovor_Posun=údaje_pozícia+SECOND_VALUE[identifikátor_VALUE];if(údaje_pozícia>=ukončiť_hovor_Posun||údaje[údaje_pozícia++]!='(')return -1;int položka_COUNT_8f7753a1=0;
    while(údaje_pozícia<ukončiť_hovor_Posun&&údaje[údaje_pozícia]!=')'){
        unsigned bod_kódu=údaje[údaje_pozícia++];while(bod_kódu=='['&&údaje_pozícia<ukončiť_hovor_Posun)bod_kódu=údaje[údaje_pozícia++];
        if(bod_kódu=='L'){while(údaje_pozícia<ukončiť_hovor_Posun&&údaje[údaje_pozícia]!=';')údaje_pozícia++;if(údaje_pozícia==ukončiť_hovor_Posun)return -1;údaje_pozícia++;}
        else if(bod_kódu!='I'&&bod_kódu!='Z'&&bod_kódu!='B'&&bod_kódu!='C'&&bod_kódu!='S')return -1;
        if(++položka_COUNT_8f7753a1>16)return -1;
    }
    if(údaje_pozícia+1>=ukončiť_hovor_Posun||údaje[údaje_pozícia++]!=')')return -1;*KR=údaje[údaje_pozícia]=='V'?0:1;
    if(údaje[údaje_pozícia]=='J'||údaje[údaje_pozícia]=='D'||údaje[údaje_pozícia]=='F')return -1;return položka_COUNT_8f7753a1;
}
static void atribúty(void){unsigned položka_COUNT=절반값();for(unsigned 순번=0;순번<položka_COUNT&&!Informačné_systémy_neplatné;순번++){절반값();unsigned Veľkosť=가득참();TAKE_VALUE(Veľkosť);}}
static int analyzovať_vstup(void){
    if(가득참()!=0xcafebabe)return -1;unsigned vedľajšia_verzia=절반값(),číslo_verzie=절반값();if(vedľajšia_verzia||číslo_verzie<45||číslo_verzie>52)return -1;
    konštanta_fond=절반값();if(konštanta_fond<1||konštanta_fond>512)return -1;
    for(unsigned 순번=1;순번<konštanta_fond&&!Informačné_systémy_neplatné;순번++){
        Kategórie_Zoznam[순번]=Byte_údaje();switch(Kategórie_Zoznam[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=konštanta_fond)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=Byte_údaje();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();v_termíne_splatnosti_lekcia=절반값();절반값();if(v_termíne_splatnosti_lekcia<1||v_termíne_splatnosti_lekcia>=konštanta_fond||Kategórie_Zoznam[v_termíne_splatnosti_lekcia]!=7||첫째값[v_termíne_splatnosti_lekcia]<1||첫째값[v_termíne_splatnosti_lekcia]>=konštanta_fond||Kategórie_Zoznam[첫째값[v_termíne_splatnosti_lekcia]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!Informačné_systémy_neplatné;순번++){
        unsigned konfigurácia_Background_Intelligent_Transfer_Service=절반값();názov_poľa[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfigurácia_Background_Intelligent_Transfer_Service&8))return -1;
        unsigned položka_COUNT_8f7753a1=절반값();for(unsigned 안쪽순번=0;안쪽순번<položka_COUNT_8f7753a1&&!Informačné_systémy_neplatné;안쪽순번++){
            unsigned Názov=절반값(),Veľkosť=가득참();
            if(UNICODE_VALUE(Názov,"ConstantValue")){if(Veľkosť!=2)return -1;pole_konštanta[순번]=절반값();}
            else TAKE_VALUE(Veľkosť);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!Informačné_systémy_neplatné;순번++){
        metóda_položka*Skupina_zmeniť_veľkosť=메소드목록+순번;Skupina_zmeniť_veľkosť->konfigurácia_Background_Intelligent_Transfer_Service=절반값();Skupina_zmeniť_veľkosť->Názov=절반값();Skupina_zmeniť_veľkosť->서술값=절반값();unsigned položka_COUNT_8f7753a1=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<položka_COUNT_8f7753a1&&!Informačné_systémy_neplatné;안쪽순번++){
            unsigned Názov=절반값(),Veľkosť=가득참(),Spustiť_2=v_termíne_splatnosti_pozícia;
            if(Veľkosť>dĺžka_VALUE-v_termíne_splatnosti_pozícia)return -1;
            if(UNICODE_VALUE(Názov,"Code")){
                Skupina_zmeniť_veľkosť->Vrstvy_Úložisko=절반값();Skupina_zmeniť_veľkosť->지역변수들=절반값();Skupina_zmeniť_veľkosť->Veľkosť=가득참();Skupina_zmeniť_veľkosť->inštrukcia_SEQUENCE=TAKE_VALUE(Skupina_zmeniť_veľkosť->Veľkosť);
                if(Skupina_zmeniť_veľkosť->Vrstvy_Úložisko>128||Skupina_zmeniť_veľkosť->지역변수들>128||Skupina_zmeniť_veľkosť->Veľkosť>8192||절반값())return -1;atribúty();
            }else TAKE_VALUE(Veľkosť);
            if(v_termíne_splatnosti_pozícia!=Spustiť_2+Veľkosť)return -1;
        }
        if(!UNICODE_VALUE(Skupina_zmeniť_veľkosť->Názov,"<init>")&&(!(Skupina_zmeniť_veľkosť->konfigurácia_Background_Intelligent_Transfer_Service&8)||(Skupina_zmeniť_veľkosť->konfigurácia_Background_Intelligent_Transfer_Service&(0x100|0x20))||!Skupina_zmeniť_veľkosť->Veľkosť))return -1;
    }
    atribúty();return Informačné_systémy_neplatné||v_termíne_splatnosti_pozícia!=dĺžka_VALUE?-1:0;
}
static void konštanta_VALUE(unsigned identifikátor_VALUE){
    if(!identifikátor_VALUE||identifikátor_VALUE>=konštanta_fond){Informačné_systémy_neplatné=1;return;}
    if(Kategórie_Zoznam[identifikátor_VALUE]==3)내보내기("P(%uU);",첫째값[identifikátor_VALUE]);
    else if(Kategórie_Zoznam[identifikátor_VALUE]==8)내보내기("P((W)k%u);",identifikátor_VALUE);else Informačné_systémy_neplatné=1;
}
static void 호출(unsigned identifikátor_VALUE,int virtuálny_CALL){
    if(identifikátor_VALUE<1||identifikátor_VALUE>=konštanta_fond||(Kategórie_Zoznam[identifikátor_VALUE]!=10&&Kategórie_Zoznam[identifikátor_VALUE]!=11)||첫째값[identifikátor_VALUE]<1||첫째값[identifikátor_VALUE]>=konštanta_fond||Kategórie_Zoznam[첫째값[identifikátor_VALUE]]!=7||SECOND_VALUE[identifikátor_VALUE]<1||SECOND_VALUE[identifikátor_VALUE]>=konštanta_fond||Kategórie_Zoznam[SECOND_VALUE[identifikátor_VALUE]]!=12){Informačné_systémy_neplatné=1;return;}
    unsigned vlastník_objekt=첫째값[첫째값[identifikátor_VALUE]],Názov=첫째값[SECOND_VALUE[identifikátor_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikátor_VALUE]];int KR=0,položka_COUNT=서술자(서술값,&KR);if(položka_COUNT<0){Informačné_systémy_neplatné=1;return;}
    for(int 순번=položka_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtuálny_CALL)내보내기("Q();");
    if(!virtuálny_CALL&&같음(vlastník_objekt,첫째값[v_termíne_splatnosti_lekcia])){
        unsigned Skupina_zmeniť_veľkosť=0;for(;Skupina_zmeniť_veľkosť<메소드개수;Skupina_zmeniť_veľkosť++)if(같음(Názov,메소드목록[Skupina_zmeniť_veľkosť].Názov)&&같음(서술값,메소드목록[Skupina_zmeniť_veľkosť].서술값))break;
        if(Skupina_zmeniť_veľkosť==메소드개수||!(메소드목록[Skupina_zmeniť_veľkosť].konfigurácia_Background_Intelligent_Transfer_Service&8)){Informačné_systémy_neplatné=1;return;}
        if(KR)내보내기("P(");내보내기("m%u(",Skupina_zmeniť_veľkosť);for(int 순번=0;순번<položka_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(KR?"));":" );");return;
    }
    if((virtuálny_CALL&&UNICODE_VALUE(vlastník_objekt,"java/io/PrintStream")&& (UNICODE_VALUE(Názov,"print")||UNICODE_VALUE(Názov,"println")))||(!virtuálny_CALL&&UNICODE_VALUE(vlastník_objekt,"Slovenský/vlastné/Výstup"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Názov,"print")||UNICODE_VALUE(Názov,"println")||UNICODE_VALUE(Názov,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Názov,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Názov,"print")||UNICODE_VALUE(Názov,"println")||UNICODE_VALUE(Názov,"Zápis")||UNICODE_VALUE(Názov,"zapísať_linka"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Názov,"print")||UNICODE_VALUE(Názov,"Zápis")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Názov,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtuálny_CALL&&UNICODE_VALUE(vlastník_objekt,"Slovenský/vlastné/Súbor")){
        if(UNICODE_VALUE(Názov,"Zápis")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Názov,"Čítanie")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    Informačné_systémy_neplatné=1;
}
static void kompilovať_metóda(unsigned LOOKUP_INDEX){
    metóda_položka*Skupina_zmeniť_veľkosť=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(Skupina_zmeniť_veľkosť->Názov,"<init>"))return;int KR,položka_COUNT=서술자(Skupina_zmeniť_veľkosť->서술값,&KR);if(položka_COUNT<0){Informačné_systémy_neplatné=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<položka_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!položka_COUNT)내보내기("void");
    if((unsigned)položka_COUNT>Skupina_zmeniť_veľkosť->지역변수들){Informačné_systémy_neplatné=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Skupina_zmeniť_veľkosť->지역변수들?Skupina_zmeniť_veľkosť->지역변수들:1);for(int 순번=0;순번<položka_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=dĺžka_VALUE;dĺžka_VALUE=Skupina_zmeniť_veľkosť->inštrukcia_SEQUENCE+Skupina_zmeniť_veľkosť->Veľkosť;v_termíne_splatnosti_pozícia=Skupina_zmeniť_veľkosť->inštrukcia_SEQUENCE;
    while(v_termíne_splatnosti_pozícia<dĺžka_VALUE&&!Informačné_systémy_neplatné){unsigned príkaz_pozícia=v_termíne_splatnosti_pozícia-Skupina_zmeniť_veľkosť->inštrukcia_SEQUENCE,operácia_VALUE=Byte_údaje();내보내기("L%u:;",príkaz_pozícia);
        if(operácia_VALUE==0){}
        else if(operácia_VALUE==1)내보내기("P(0);");
        else if(operácia_VALUE>=2&&operácia_VALUE<=8)내보내기("P(%uU);",operácia_VALUE-3);
        else if(operácia_VALUE==16){int VALUE=(int8_t)Byte_údaje();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operácia_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operácia_VALUE==18||operácia_VALUE==19)konštanta_VALUE(operácia_VALUE==18?Byte_údaje():절반값());
        else if(operácia_VALUE==21||operácia_VALUE==25){unsigned 순번=Byte_údaje();if(순번>=Skupina_zmeniť_veľkosť->지역변수들)Informačné_systémy_neplatné=1;내보내기("P(v[%u]);",순번);}
        else if((operácia_VALUE>=26&&operácia_VALUE<=29)||(operácia_VALUE>=42&&operácia_VALUE<=45)){unsigned 순번=operácia_VALUE>=42?operácia_VALUE-42:operácia_VALUE-26;if(순번>=Skupina_zmeniť_veľkosť->지역변수들)Informačné_systémy_neplatné=1;내보내기("P(v[%u]);",순번);}
        else if(operácia_VALUE==54||operácia_VALUE==58){unsigned 순번=Byte_údaje();if(순번>=Skupina_zmeniť_veľkosť->지역변수들)Informačné_systémy_neplatné=1;내보내기("v[%u]=Q();",순번);}
        else if((operácia_VALUE>=59&&operácia_VALUE<=62)||(operácia_VALUE>=75&&operácia_VALUE<=78)){unsigned 순번=operácia_VALUE>=75?operácia_VALUE-75:operácia_VALUE-59;if(순번>=Skupina_zmeniť_veľkosť->지역변수들)Informačné_systémy_neplatné=1;내보내기("v[%u]=Q();",순번);}
        else if(operácia_VALUE==46||operácia_VALUE==50||operácia_VALUE==51||operácia_VALUE==52||operácia_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operácia_VALUE==79||operácia_VALUE==83||operácia_VALUE==84||operácia_VALUE==85||operácia_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operácia_VALUE==84?"(unsigned)(signed char)q":operácia_VALUE==85?"(unsigned short)q":operácia_VALUE==86?"(unsigned)(short)q":"q");
        else if(operácia_VALUE==87)내보내기("Q();");
        else if(operácia_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(operácia_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operácia_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(operácia_VALUE==96||operácia_VALUE==100||operácia_VALUE==104||operácia_VALUE==120||operácia_VALUE==124||operácia_VALUE==126||operácia_VALUE==128||operácia_VALUE==130){const char*kódovanie_VALUE=operácia_VALUE==96?"+":operácia_VALUE==100?"-":operácia_VALUE==104?"*":operácia_VALUE==120?"<<":operácia_VALUE==124?">>":operácia_VALUE==126?"&":operácia_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kódovanie_VALUE,operácia_VALUE==120||operácia_VALUE==124?"%32":"");}
        else if(operácia_VALUE==108||operácia_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operácia_VALUE==112);
        else if(operácia_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(operácia_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operácia_VALUE==132){unsigned 순번=Byte_údaje();int 차이=(int8_t)Byte_údaje();if(순번>=Skupina_zmeniť_veľkosť->지역변수들)Informačné_systémy_neplatné=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operácia_VALUE>=145&&operácia_VALUE<=147)내보내기("P((unsigned)(%s)Q());",operácia_VALUE==145?"signed char":operácia_VALUE==146?"unsigned short":"short");
        else if(operácia_VALUE>=153&&operácia_VALUE<=166){int cieľová_hodnota=(int)príkaz_pozícia+(int16_t)절반값();const char*Porovnanie_VALUE[]={"==","!=","<",">=",">","<="};if(cieľová_hodnota<0||cieľová_hodnota>=(int)Skupina_zmeniť_veľkosť->Veľkosť){Informačné_systémy_neplatné=1;break;}if(operácia_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Porovnanie_VALUE[operácia_VALUE-153],cieľová_hodnota);else if(operácia_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Porovnanie_VALUE[operácia_VALUE-159],cieľová_hodnota);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operácia_VALUE==165?"==":"!=",cieľová_hodnota);}
        else if(operácia_VALUE==167){int cieľová_hodnota=(int)príkaz_pozícia+(int16_t)절반값();if(cieľová_hodnota<0||cieľová_hodnota>=(int)Skupina_zmeniť_veľkosť->Veľkosť)Informačné_systémy_neplatné=1;내보내기("goto L%d;",cieľová_hodnota);}
        else if(operácia_VALUE==172||operácia_VALUE==176)내보내기("return Q();");else if(operácia_VALUE==177)내보내기("return 0;");
        else if(operácia_VALUE==178||operácia_VALUE==179){unsigned identifikátor_VALUE=절반값();if(identifikátor_VALUE<1||identifikátor_VALUE>=konštanta_fond||Kategórie_Zoznam[identifikátor_VALUE]!=9||첫째값[identifikátor_VALUE]>=konštanta_fond||SECOND_VALUE[identifikátor_VALUE]>=konštanta_fond||Kategórie_Zoznam[첫째값[identifikátor_VALUE]]!=7||Kategórie_Zoznam[SECOND_VALUE[identifikátor_VALUE]]!=12){Informačné_systémy_neplatné=1;break;}unsigned vlastník_objekt=첫째값[첫째값[identifikátor_VALUE]],Názov=첫째값[SECOND_VALUE[identifikátor_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikátor_VALUE]];
            if(operácia_VALUE==178&&UNICODE_VALUE(vlastník_objekt,"java/lang/System")&&UNICODE_VALUE(Názov,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Súbor_položka=0;while(Súbor_položka<필드개수&&(!같음(Názov,názov_poľa[Súbor_položka])||!같음(서술값,필드서술[Súbor_položka])))Súbor_položka++;if(!같음(vlastník_objekt,첫째값[v_termíne_splatnosti_lekcia])||Súbor_položka==필드개수){Informačné_systémy_neplatné=1;break;}내보내기(operácia_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",Súbor_položka);}}
        else if(operácia_VALUE==182||operácia_VALUE==184)호출(절반값(),operácia_VALUE==182);
        else if(operácia_VALUE==188){unsigned Typ_oblasť=Byte_údaje();if(Typ_oblasť!=4&&Typ_oblasť!=5&&Typ_oblasť!=8&&Typ_oblasť!=9&&Typ_oblasť!=10)Informačné_systémy_neplatné=1;내보내기("P(jarray((int)Q()));");}
        else if(operácia_VALUE==190)내보내기("P(jlength(Q()));");
        else if(operácia_VALUE==198||operácia_VALUE==199){int cieľová_hodnota=(int)príkaz_pozícia+(int16_t)절반값();if(cieľová_hodnota<0||cieľová_hodnota>=(int)Skupina_zmeniť_veľkosť->Veľkosť)Informačné_systémy_neplatné=1;내보내기("if(Q()%s0)goto L%d;",operácia_VALUE==198?"==":"!=",cieľová_hodnota);}
        else Informačné_systémy_neplatné=1;
        if(Informačné_systémy_neplatné)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,operácia_VALUE,príkaz_pozícia);
        내보내기("\n");
    }
    dĺžka_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned reťazec_lekcia(unsigned *údaje_pozícia,unsigned ukončiť_hovor_Posun){
    if(*údaje_pozícia>=ukončiť_hovor_Posun){Informačné_systémy_neplatné=1;return 0;}unsigned bod_kódu=údaje[(*údaje_pozícia)++];
    if(bod_kódu<128)return bod_kódu;
    unsigned položka_COUNT=bod_kódu>=0xc0&&bod_kódu<=0xdf?1:bod_kódu>=0xe0&&bod_kódu<=0xef?2:3;
    if(položka_COUNT==3||položka_COUNT>ukončiť_hovor_Posun-*údaje_pozícia){Informačné_systémy_neplatné=1;return 0;}unsigned VALUE=bod_kódu&((1u<<(6-položka_COUNT))-1);
    for(unsigned 순번=0;순번<položka_COUNT;순번++){unsigned Ďalej_položka=údaje[(*údaje_pozícia)++];if((Ďalej_položka&0xc0)!=0x80)Informačné_systémy_neplatné=1;VALUE=VALUE<<6|(Ďalej_položka&63);}
    if((položka_COUNT==1&&VALUE<128&&VALUE!=0)||(položka_COUNT==2&&VALUE<2048))Informačné_systémy_neplatné=1;return VALUE;
}
static void reťazec_konštanta(unsigned identifikátor_VALUE){
    unsigned 부호없는값=첫째값[identifikátor_VALUE];if(부호없는값<1||부호없는값>=konštanta_fond||Kategórie_Zoznam[부호없는값]!=1){Informačné_systémy_neplatné=1;return;}내보내기("static const unsigned char k%u[]={",identifikátor_VALUE);
    unsigned údaje_pozícia=첫째값[부호없는값],ukončiť_hovor_Posun=údaje_pozícia+SECOND_VALUE[부호없는값];
    while(údaje_pozícia<ukončiť_hovor_Posun&&!Informačné_systémy_neplatné){unsigned bod_kódu=reťazec_lekcia(&údaje_pozícia,ukončiť_hovor_Posun);
        if(bod_kódu>=0xd800&&bod_kódu<=0xdbff){unsigned 낮은부분=reťazec_lekcia(&údaje_pozícia,ukončiť_hovor_Posun);if(낮은부분<0xdc00||낮은부분>0xdfff){Informačné_systémy_neplatné=1;break;}bod_kódu=0x10000+((bod_kódu-0xd800)<<10)+낮은부분-0xdc00;}
        else if(bod_kódu>=0xdc00&&bod_kódu<=0xdfff){Informačné_systémy_neplatné=1;break;}
        if(!bod_kódu){printf("jaot: embedded NUL string needs JVM mode\n");Informačné_systémy_neplatné=1;break;}
        if(bod_kódu<128)내보내기("%u,",bod_kódu);
        else{unsigned položka_COUNT=bod_kódu<2048?2:bod_kódu<65536?3:4;내보내기("%u,",(položka_COUNT==2?0xc0:položka_COUNT==3?0xe0:0xf0)|(bod_kódu>>(6*(položka_COUNT-1))));for(unsigned 순번=položka_COUNT-1;순번;순번--)내보내기("%u,",0x80|((bod_kódu>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Názov){
    size_t položka_COUNT=strlen(Názov);
    if(položka_COUNT>4&&!strcmp(Názov+položka_COUNT-4,".jar")){
        if(꾸러미열기(Názov)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Cesta[256];const char*položka_metóda=꾸러미진입클래스();položka_COUNT=strlen(položka_metóda);if(položka_COUNT+6>=sizeof(Cesta))return 0;
        for(unsigned 순번=0;순번<položka_COUNT;순번++)Cesta[순번]=položka_metóda[순번]=='.'?'/':položka_metóda[순번];strcpy(Cesta+položka_COUNT,".class");int položka_COUNT_8f7753a1=꾸러미읽기(Cesta,údaje,sizeof(údaje));if(položka_COUNT_8f7753a1<0)return 0;dĺžka_VALUE=položka_COUNT_8f7753a1;
    }else{intptr_t Súbor_rukoväť=사용자호출(3,(uintptr_t)Názov,0,0,0,0,0);if(Súbor_rukoväť<0)return 0;intptr_t položka_COUNT_8f7753a1=사용자호출(9,Súbor_rukoväť,0,0,0,0,0);if(položka_COUNT_8f7753a1<0||položka_COUNT_8f7753a1>sizeof(údaje)){사용자호출(4,Súbor_rukoväť,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,Súbor_rukoväť,(uintptr_t)údaje,položka_COUNT_8f7753a1,0,0,0);사용자호출(4,Súbor_rukoväť,0,0,0,0,0);if(RECEIVED_COUNT!=položka_COUNT_8f7753a1)return 0;dĺžka_VALUE=položka_COUNT_8f7753a1;}
    if(analyzovať_vstup()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konštanta_fond&&!Informačné_systémy_neplatné;순번++)if(Kategórie_Zoznam[순번]==8)reťazec_konštanta(순번);
    if(Informačné_systémy_neplatné)return 0;
    int položka_bod=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Názov,"<init>")){
        int KR,položka_COUNT_8f7753a1=서술자(메소드목록[순번].서술값,&KR);if(položka_COUNT_8f7753a1<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<položka_COUNT_8f7753a1;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!položka_COUNT_8f7753a1)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Názov,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfigurácia_Background_Intelligent_Transfer_Service&9)==9)položka_bod=순번;
        if(UNICODE_VALUE(메소드목록[순번].Názov,"<clinit>"))초기값=순번;
    }
    if(položka_bod<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!Informačné_systémy_neplatné;순번++)kompilovať_metóda(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(pole_konštanta[순번]){
        unsigned bod_kódu=pole_konštanta[순번];if(bod_kódu>=konštanta_fond)return 0;
        if(Kategórie_Zoznam[bod_kódu]==3)내보내기("fields[%u]=%uU;",순번,첫째값[bod_kódu]);else if(Kategórie_Zoznam[bod_kódu]==8)내보내기("fields[%u]=(W)k%u;",순번,bod_kódu);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",položka_bod);
    return Informačné_systémy_neplatné?0:Spracovanie_textu;
}
