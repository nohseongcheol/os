#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "set.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char date[16384];static unsigned lungime_VALUE,curent_poziție;static int sisteme_de_informații_nul;
static unsigned Etichete_Listă[512],첫째값[512],SECOND_VALUE[512],constantă_grup,curent_Clasă;
static char SMS[65536];static unsigned Dimensiune_text;
typedef struct {unsigned configurație_Serviciu_de_transfer_inteligent_în_fundal,Nume,서술값,명령열,Mărime,지역변수들,Teanc_Stocare;} metodă_intrare;
static metodă_intrare 메소드목록[64];static unsigned 메소드개수;
static unsigned nume_de_câmp[64],필드서술[64],câmp_constantă[64],필드개수;
static unsigned TAKE_VALUE(unsigned element_COUNT){if(curent_poziție>lungime_VALUE||element_COUNT>lungime_VALUE-curent_poziție){sisteme_de_informații_nul=1;return 0;}unsigned date_poziție=curent_poziție;curent_poziție+=element_COUNT;return date_poziție;}
static unsigned byte_date(void){unsigned date_poziție=TAKE_VALUE(1);return sisteme_de_informații_nul?0:date[date_poziție];}
static unsigned 절반값(void){unsigned coordonata_X=byte_date();return coordonata_X<<8|byte_date();}
static uint32_t 가득참(void){uint32_t coordonata_X=절반값();return coordonata_X<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*șir_date){return 순번>0&&순번<constantă_grup&&Etichete_Listă[순번]==1&&strlen(șir_date)==SECOND_VALUE[순번]&&!memcmp(date+첫째값[순번],șir_date,SECOND_VALUE[순번]);}
static int 같음(unsigned coordonata_X,unsigned 세로좌표){return coordonata_X>0&&coordonata_X<constantă_grup&&세로좌표>0&&세로좌표<constantă_grup&&Etichete_Listă[coordonata_X]==1&&Etichete_Listă[세로좌표]==1&&SECOND_VALUE[coordonata_X]==SECOND_VALUE[세로좌표]&&!memcmp(date+첫째값[coordonata_X],date+첫째값[세로좌표],SECOND_VALUE[coordonata_X]);}
static void 내보내기(const char*Fișier_intrare,...){if(sisteme_de_informații_nul)return;va_list argument_ARRAY;va_start(argument_ARRAY,Fișier_intrare);int element_COUNT=vsnprintf(SMS+Dimensiune_text,sizeof(SMS)-Dimensiune_text,Fișier_intrare,argument_ARRAY);va_end(argument_ARRAY);if(element_COUNT<0||(unsigned)element_COUNT>=sizeof(SMS)-Dimensiune_text){sisteme_de_informații_nul=1;return;}Dimensiune_text+=element_COUNT;}
static int 서술자(unsigned identificator_VALUE,int*KR){
    if(identificator_VALUE<1||identificator_VALUE>=constantă_grup||Etichete_Listă[identificator_VALUE]!=1)return -1;unsigned date_poziție=첫째값[identificator_VALUE],termina_un_apel_OFFSET=date_poziție+SECOND_VALUE[identificator_VALUE];if(date_poziție>=termina_un_apel_OFFSET||date[date_poziție++]!='(')return -1;int intrare_COUNT=0;
    while(date_poziție<termina_un_apel_OFFSET&&date[date_poziție]!=')'){
        unsigned cod_caracter=date[date_poziție++];while(cod_caracter=='['&&date_poziție<termina_un_apel_OFFSET)cod_caracter=date[date_poziție++];
        if(cod_caracter=='L'){while(date_poziție<termina_un_apel_OFFSET&&date[date_poziție]!=';')date_poziție++;if(date_poziție==termina_un_apel_OFFSET)return -1;date_poziție++;}
        else if(cod_caracter!='I'&&cod_caracter!='Z'&&cod_caracter!='B'&&cod_caracter!='C'&&cod_caracter!='S')return -1;
        if(++intrare_COUNT>16)return -1;
    }
    if(date_poziție+1>=termina_un_apel_OFFSET||date[date_poziție++]!=')')return -1;*KR=date[date_poziție]=='V'?0:1;
    if(date[date_poziție]=='J'||date[date_poziție]=='D'||date[date_poziție]=='F')return -1;return intrare_COUNT;
}
static void atribute(void){unsigned element_COUNT=절반값();for(unsigned 순번=0;순번<element_COUNT&&!sisteme_de_informații_nul;순번++){절반값();unsigned Mărime=가득참();TAKE_VALUE(Mărime);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned versiune_minoră=절반값(),număr_de_versiune=절반값();if(versiune_minoră||număr_de_versiune<45||număr_de_versiune>52)return -1;
    constantă_grup=절반값();if(constantă_grup<1||constantă_grup>512)return -1;
    for(unsigned 순번=1;순번<constantă_grup&&!sisteme_de_informații_nul;순번++){
        Etichete_Listă[순번]=byte_date();switch(Etichete_Listă[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=constantă_grup)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=byte_date();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();curent_Clasă=절반값();절반값();if(curent_Clasă<1||curent_Clasă>=constantă_grup||Etichete_Listă[curent_Clasă]!=7||첫째값[curent_Clasă]<1||첫째값[curent_Clasă]>=constantă_grup||Etichete_Listă[첫째값[curent_Clasă]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!sisteme_de_informații_nul;순번++){
        unsigned configurație_Serviciu_de_transfer_inteligent_în_fundal=절반값();nume_de_câmp[순번]=절반값();필드서술[순번]=절반값();
        if(!(configurație_Serviciu_de_transfer_inteligent_în_fundal&8))return -1;
        unsigned intrare_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<intrare_COUNT&&!sisteme_de_informații_nul;안쪽순번++){
            unsigned Nume=절반값(),Mărime=가득참();
            if(UNICODE_VALUE(Nume,"ConstantValue")){if(Mărime!=2)return -1;câmp_constantă[순번]=절반값();}
            else TAKE_VALUE(Mărime);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!sisteme_de_informații_nul;순번++){
        metodă_intrare*grup_dimensiona=메소드목록+순번;grup_dimensiona->configurație_Serviciu_de_transfer_inteligent_în_fundal=절반값();grup_dimensiona->Nume=절반값();grup_dimensiona->서술값=절반값();unsigned intrare_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<intrare_COUNT&&!sisteme_de_informații_nul;안쪽순번++){
            unsigned Nume=절반값(),Mărime=가득참(),Pornește=curent_poziție;
            if(Mărime>lungime_VALUE-curent_poziție)return -1;
            if(UNICODE_VALUE(Nume,"Code")){
                grup_dimensiona->Teanc_Stocare=절반값();grup_dimensiona->지역변수들=절반값();grup_dimensiona->Mărime=가득참();grup_dimensiona->명령열=TAKE_VALUE(grup_dimensiona->Mărime);
                if(grup_dimensiona->Teanc_Stocare>128||grup_dimensiona->지역변수들>128||grup_dimensiona->Mărime>8192||절반값())return -1;atribute();
            }else TAKE_VALUE(Mărime);
            if(curent_poziție!=Pornește+Mărime)return -1;
        }
        if(!UNICODE_VALUE(grup_dimensiona->Nume,"<init>")&&(!(grup_dimensiona->configurație_Serviciu_de_transfer_inteligent_în_fundal&8)||(grup_dimensiona->configurație_Serviciu_de_transfer_inteligent_în_fundal&(0x100|0x20))||!grup_dimensiona->Mărime))return -1;
    }
    atribute();return sisteme_de_informații_nul||curent_poziție!=lungime_VALUE?-1:0;
}
static void constantă_VALUE(unsigned identificator_VALUE){
    if(!identificator_VALUE||identificator_VALUE>=constantă_grup){sisteme_de_informații_nul=1;return;}
    if(Etichete_Listă[identificator_VALUE]==3)내보내기("P(%uU);",첫째값[identificator_VALUE]);
    else if(Etichete_Listă[identificator_VALUE]==8)내보내기("P((W)k%u);",identificator_VALUE);else sisteme_de_informații_nul=1;
}
static void 호출(unsigned identificator_VALUE,int 가상호출){
    if(identificator_VALUE<1||identificator_VALUE>=constantă_grup||(Etichete_Listă[identificator_VALUE]!=10&&Etichete_Listă[identificator_VALUE]!=11)||첫째값[identificator_VALUE]<1||첫째값[identificator_VALUE]>=constantă_grup||Etichete_Listă[첫째값[identificator_VALUE]]!=7||SECOND_VALUE[identificator_VALUE]<1||SECOND_VALUE[identificator_VALUE]>=constantă_grup||Etichete_Listă[SECOND_VALUE[identificator_VALUE]]!=12){sisteme_de_informații_nul=1;return;}
    unsigned proprietar_obiect=첫째값[첫째값[identificator_VALUE]],Nume=첫째값[SECOND_VALUE[identificator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identificator_VALUE]];int KR=0,element_COUNT=서술자(서술값,&KR);if(element_COUNT<0){sisteme_de_informații_nul=1;return;}
    for(int 순번=element_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(가상호출)내보내기("Q();");
    if(!가상호출&&같음(proprietar_obiect,첫째값[curent_Clasă])){
        unsigned grup_dimensiona=0;for(;grup_dimensiona<메소드개수;grup_dimensiona++)if(같음(Nume,메소드목록[grup_dimensiona].Nume)&&같음(서술값,메소드목록[grup_dimensiona].서술값))break;
        if(grup_dimensiona==메소드개수||!(메소드목록[grup_dimensiona].configurație_Serviciu_de_transfer_inteligent_în_fundal&8)){sisteme_de_informații_nul=1;return;}
        if(KR)내보내기("P(");내보내기("m%u(",grup_dimensiona);for(int 순번=0;순번<element_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(KR?"));":" );");return;
    }
    if((가상호출&&UNICODE_VALUE(proprietar_obiect,"java/io/PrintStream")&& (UNICODE_VALUE(Nume,"print")||UNICODE_VALUE(Nume,"println")))||(!가상호출&&UNICODE_VALUE(proprietar_obiect,"Română/propriu/Rezultat"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Nume,"print")||UNICODE_VALUE(Nume,"println")||UNICODE_VALUE(Nume,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Nume,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Nume,"print")||UNICODE_VALUE(Nume,"println")||UNICODE_VALUE(Nume,"Scriere")||UNICODE_VALUE(Nume,"scriere_linie"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Nume,"print")||UNICODE_VALUE(Nume,"Scriere")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Nume,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!가상호출&&UNICODE_VALUE(proprietar_obiect,"Română/propriu/Fișier")){
        if(UNICODE_VALUE(Nume,"Scriere")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Nume,"Citire")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    sisteme_de_informații_nul=1;
}
static void compilare_metodă(unsigned LOOKUP_INDEX){
    metodă_intrare*grup_dimensiona=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(grup_dimensiona->Nume,"<init>"))return;int KR,element_COUNT=서술자(grup_dimensiona->서술값,&KR);if(element_COUNT<0){sisteme_de_informații_nul=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<element_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!element_COUNT)내보내기("void");
    if((unsigned)element_COUNT>grup_dimensiona->지역변수들){sisteme_de_informații_nul=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",grup_dimensiona->지역변수들?grup_dimensiona->지역변수들:1);for(int 순번=0;순번<element_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=lungime_VALUE;lungime_VALUE=grup_dimensiona->명령열+grup_dimensiona->Mărime;curent_poziție=grup_dimensiona->명령열;
    while(curent_poziție<lungime_VALUE&&!sisteme_de_informații_nul){unsigned comandă_poziție=curent_poziție-grup_dimensiona->명령열,operație_VALUE=byte_date();내보내기("L%u:;",comandă_poziție);
        if(operație_VALUE==0){}
        else if(operație_VALUE==1)내보내기("P(0);");
        else if(operație_VALUE>=2&&operație_VALUE<=8)내보내기("P(%uU);",operație_VALUE-3);
        else if(operație_VALUE==16){int VALUE=(int8_t)byte_date();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operație_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operație_VALUE==18||operație_VALUE==19)constantă_VALUE(operație_VALUE==18?byte_date():절반값());
        else if(operație_VALUE==21||operație_VALUE==25){unsigned 순번=byte_date();if(순번>=grup_dimensiona->지역변수들)sisteme_de_informații_nul=1;내보내기("P(v[%u]);",순번);}
        else if((operație_VALUE>=26&&operație_VALUE<=29)||(operație_VALUE>=42&&operație_VALUE<=45)){unsigned 순번=operație_VALUE>=42?operație_VALUE-42:operație_VALUE-26;if(순번>=grup_dimensiona->지역변수들)sisteme_de_informații_nul=1;내보내기("P(v[%u]);",순번);}
        else if(operație_VALUE==54||operație_VALUE==58){unsigned 순번=byte_date();if(순번>=grup_dimensiona->지역변수들)sisteme_de_informații_nul=1;내보내기("v[%u]=Q();",순번);}
        else if((operație_VALUE>=59&&operație_VALUE<=62)||(operație_VALUE>=75&&operație_VALUE<=78)){unsigned 순번=operație_VALUE>=75?operație_VALUE-75:operație_VALUE-59;if(순번>=grup_dimensiona->지역변수들)sisteme_de_informații_nul=1;내보내기("v[%u]=Q();",순번);}
        else if(operație_VALUE==46||operație_VALUE==50||operație_VALUE==51||operație_VALUE==52||operație_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operație_VALUE==79||operație_VALUE==83||operație_VALUE==84||operație_VALUE==85||operație_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operație_VALUE==84?"(unsigned)(signed char)q":operație_VALUE==85?"(unsigned short)q":operație_VALUE==86?"(unsigned)(short)q":"q");
        else if(operație_VALUE==87)내보내기("Q();");
        else if(operație_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(operație_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operație_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(operație_VALUE==96||operație_VALUE==100||operație_VALUE==104||operație_VALUE==120||operație_VALUE==124||operație_VALUE==126||operație_VALUE==128||operație_VALUE==130){const char*codificare_VALUE=operație_VALUE==96?"+":operație_VALUE==100?"-":operație_VALUE==104?"*":operație_VALUE==120?"<<":operație_VALUE==124?">>":operație_VALUE==126?"&":operație_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",codificare_VALUE,operație_VALUE==120||operație_VALUE==124?"%32":"");}
        else if(operație_VALUE==108||operație_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operație_VALUE==112);
        else if(operație_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(operație_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operație_VALUE==132){unsigned 순번=byte_date();int 차이=(int8_t)byte_date();if(순번>=grup_dimensiona->지역변수들)sisteme_de_informații_nul=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operație_VALUE>=145&&operație_VALUE<=147)내보내기("P((unsigned)(%s)Q());",operație_VALUE==145?"signed char":operație_VALUE==146?"unsigned short":"short");
        else if(operație_VALUE>=153&&operație_VALUE<=166){int țintă=(int)comandă_poziție+(int16_t)절반값();const char*Comparație_VALUE[]={"==","!=","<",">=",">","<="};if(țintă<0||țintă>=(int)grup_dimensiona->Mărime){sisteme_de_informații_nul=1;break;}if(operație_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Comparație_VALUE[operație_VALUE-153],țintă);else if(operație_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Comparație_VALUE[operație_VALUE-159],țintă);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operație_VALUE==165?"==":"!=",țintă);}
        else if(operație_VALUE==167){int țintă=(int)comandă_poziție+(int16_t)절반값();if(țintă<0||țintă>=(int)grup_dimensiona->Mărime)sisteme_de_informații_nul=1;내보내기("goto L%d;",țintă);}
        else if(operație_VALUE==172||operație_VALUE==176)내보내기("return Q();");else if(operație_VALUE==177)내보내기("return 0;");
        else if(operație_VALUE==178||operație_VALUE==179){unsigned identificator_VALUE=절반값();if(identificator_VALUE<1||identificator_VALUE>=constantă_grup||Etichete_Listă[identificator_VALUE]!=9||첫째값[identificator_VALUE]>=constantă_grup||SECOND_VALUE[identificator_VALUE]>=constantă_grup||Etichete_Listă[첫째값[identificator_VALUE]]!=7||Etichete_Listă[SECOND_VALUE[identificator_VALUE]]!=12){sisteme_de_informații_nul=1;break;}unsigned proprietar_obiect=첫째값[첫째값[identificator_VALUE]],Nume=첫째값[SECOND_VALUE[identificator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identificator_VALUE]];
            if(operație_VALUE==178&&UNICODE_VALUE(proprietar_obiect,"java/lang/System")&&UNICODE_VALUE(Nume,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Fișier_intrare=0;while(Fișier_intrare<필드개수&&(!같음(Nume,nume_de_câmp[Fișier_intrare])||!같음(서술값,필드서술[Fișier_intrare])))Fișier_intrare++;if(!같음(proprietar_obiect,첫째값[curent_Clasă])||Fișier_intrare==필드개수){sisteme_de_informații_nul=1;break;}내보내기(operație_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",Fișier_intrare);}}
        else if(operație_VALUE==182||operație_VALUE==184)호출(절반값(),operație_VALUE==182);
        else if(operație_VALUE==188){unsigned Tip_zonă=byte_date();if(Tip_zonă!=4&&Tip_zonă!=5&&Tip_zonă!=8&&Tip_zonă!=9&&Tip_zonă!=10)sisteme_de_informații_nul=1;내보내기("P(jarray((int)Q()));");}
        else if(operație_VALUE==190)내보내기("P(jlength(Q()));");
        else if(operație_VALUE==198||operație_VALUE==199){int țintă=(int)comandă_poziție+(int16_t)절반값();if(țintă<0||țintă>=(int)grup_dimensiona->Mărime)sisteme_de_informații_nul=1;내보내기("if(Q()%s0)goto L%d;",operație_VALUE==198?"==":"!=",țintă);}
        else sisteme_de_informații_nul=1;
        if(sisteme_de_informații_nul)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,operație_VALUE,comandă_poziție);
        내보내기("\n");
    }
    lungime_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned șir_lecție(unsigned *date_poziție,unsigned termina_un_apel_OFFSET){
    if(*date_poziție>=termina_un_apel_OFFSET){sisteme_de_informații_nul=1;return 0;}unsigned cod_caracter=date[(*date_poziție)++];
    if(cod_caracter<128)return cod_caracter;
    unsigned element_COUNT=cod_caracter>=0xc0&&cod_caracter<=0xdf?1:cod_caracter>=0xe0&&cod_caracter<=0xef?2:3;
    if(element_COUNT==3||element_COUNT>termina_un_apel_OFFSET-*date_poziție){sisteme_de_informații_nul=1;return 0;}unsigned VALUE=cod_caracter&((1u<<(6-element_COUNT))-1);
    for(unsigned 순번=0;순번<element_COUNT;순번++){unsigned Următorul_element=date[(*date_poziție)++];if((Următorul_element&0xc0)!=0x80)sisteme_de_informații_nul=1;VALUE=VALUE<<6|(Următorul_element&63);}
    if((element_COUNT==1&&VALUE<128&&VALUE!=0)||(element_COUNT==2&&VALUE<2048))sisteme_de_informații_nul=1;return VALUE;
}
static void șir_constantă(unsigned identificator_VALUE){
    unsigned 부호없는값=첫째값[identificator_VALUE];if(부호없는값<1||부호없는값>=constantă_grup||Etichete_Listă[부호없는값]!=1){sisteme_de_informații_nul=1;return;}내보내기("static const unsigned char k%u[]={",identificator_VALUE);
    unsigned date_poziție=첫째값[부호없는값],termina_un_apel_OFFSET=date_poziție+SECOND_VALUE[부호없는값];
    while(date_poziție<termina_un_apel_OFFSET&&!sisteme_de_informații_nul){unsigned cod_caracter=șir_lecție(&date_poziție,termina_un_apel_OFFSET);
        if(cod_caracter>=0xd800&&cod_caracter<=0xdbff){unsigned 낮은부분=șir_lecție(&date_poziție,termina_un_apel_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){sisteme_de_informații_nul=1;break;}cod_caracter=0x10000+((cod_caracter-0xd800)<<10)+낮은부분-0xdc00;}
        else if(cod_caracter>=0xdc00&&cod_caracter<=0xdfff){sisteme_de_informații_nul=1;break;}
        if(!cod_caracter){printf("jaot: embedded NUL string needs JVM mode\n");sisteme_de_informații_nul=1;break;}
        if(cod_caracter<128)내보내기("%u,",cod_caracter);
        else{unsigned element_COUNT=cod_caracter<2048?2:cod_caracter<65536?3:4;내보내기("%u,",(element_COUNT==2?0xc0:element_COUNT==3?0xe0:0xf0)|(cod_caracter>>(6*(element_COUNT-1))));for(unsigned 순번=element_COUNT-1;순번;순번--)내보내기("%u,",0x80|((cod_caracter>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Nume){
    size_t element_COUNT=strlen(Nume);
    if(element_COUNT>4&&!strcmp(Nume+element_COUNT-4,".jar")){
        if(꾸러미열기(Nume)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Cale[256];const char*intrare_metodă=꾸러미진입클래스();element_COUNT=strlen(intrare_metodă);if(element_COUNT+6>=sizeof(Cale))return 0;
        for(unsigned 순번=0;순번<element_COUNT;순번++)Cale[순번]=intrare_metodă[순번]=='.'?'/':intrare_metodă[순번];strcpy(Cale+element_COUNT,".class");int intrare_COUNT=꾸러미읽기(Cale,date,sizeof(date));if(intrare_COUNT<0)return 0;lungime_VALUE=intrare_COUNT;
    }else{intptr_t Fișier_handle=사용자호출(3,(uintptr_t)Nume,0,0,0,0,0);if(Fișier_handle<0)return 0;intptr_t intrare_COUNT=사용자호출(9,Fișier_handle,0,0,0,0,0);if(intrare_COUNT<0||intrare_COUNT>sizeof(date)){사용자호출(4,Fișier_handle,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,Fișier_handle,(uintptr_t)date,intrare_COUNT,0,0,0);사용자호출(4,Fișier_handle,0,0,0,0,0);if(RECEIVED_COUNT!=intrare_COUNT)return 0;lungime_VALUE=intrare_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<constantă_grup&&!sisteme_de_informații_nul;순번++)if(Etichete_Listă[순번]==8)șir_constantă(순번);
    if(sisteme_de_informații_nul)return 0;
    int intrare_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Nume,"<init>")){
        int KR,intrare_COUNT=서술자(메소드목록[순번].서술값,&KR);if(intrare_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<intrare_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!intrare_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Nume,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].configurație_Serviciu_de_transfer_inteligent_în_fundal&9)==9)intrare_p=순번;
        if(UNICODE_VALUE(메소드목록[순번].Nume,"<clinit>"))초기값=순번;
    }
    if(intrare_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!sisteme_de_informații_nul;순번++)compilare_metodă(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(câmp_constantă[순번]){
        unsigned cod_caracter=câmp_constantă[순번];if(cod_caracter>=constantă_grup)return 0;
        if(Etichete_Listă[cod_caracter]==3)내보내기("fields[%u]=%uU;",순번,첫째값[cod_caracter]);else if(Etichete_Listă[cod_caracter]==8)내보내기("fields[%u]=(W)k%u;",순번,cod_caracter);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",intrare_p);
    return sisteme_de_informații_nul?0:SMS;
}
