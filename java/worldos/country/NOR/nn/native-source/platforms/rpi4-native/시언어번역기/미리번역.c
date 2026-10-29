#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "bunt.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char data[16384];static unsigned lengd_VALUE,betalt_plassere;static int informasjonsteknologi_ugyldig;
static unsigned Merke_Liste[512],첫째값[512],SECOND_VALUE[512],konstant_pulje,betalt_time;
static char Tekst[65536];static unsigned Tekststorleik;
typedef struct {unsigned 설정비트,Namn,서술값,instruksjon_SEQUENCE,Storleik,지역변수들,Stabel_Lagring;} metode_oppføring;
static metode_oppføring 메소드목록[64];static unsigned 메소드개수;
static unsigned feltnamn[64],필드서술[64],felt_konstant[64],필드개수;
static unsigned TAKE_VALUE(unsigned vare_COUNT){if(betalt_plassere>lengd_VALUE||vare_COUNT>lengd_VALUE-betalt_plassere){informasjonsteknologi_ugyldig=1;return 0;}unsigned data_plassere=betalt_plassere;betalt_plassere+=vare_COUNT;return data_plassere;}
static unsigned byte_data(void){unsigned data_plassere=TAKE_VALUE(1);return informasjonsteknologi_ugyldig?0:data[data_plassere];}
static unsigned 절반값(void){unsigned x_koordinat=byte_data();return x_koordinat<<8|byte_data();}
static uint32_t 가득참(void){uint32_t x_koordinat=절반값();return x_koordinat<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*streng_data){return 순번>0&&순번<konstant_pulje&&Merke_Liste[순번]==1&&strlen(streng_data)==SECOND_VALUE[순번]&&!memcmp(data+첫째값[순번],streng_data,SECOND_VALUE[순번]);}
static int 같음(unsigned x_koordinat,unsigned Y_koordinat){return x_koordinat>0&&x_koordinat<konstant_pulje&&Y_koordinat>0&&Y_koordinat<konstant_pulje&&Merke_Liste[x_koordinat]==1&&Merke_Liste[Y_koordinat]==1&&SECOND_VALUE[x_koordinat]==SECOND_VALUE[Y_koordinat]&&!memcmp(data+첫째값[x_koordinat],data+첫째값[Y_koordinat],SECOND_VALUE[x_koordinat]);}
static void 내보내기(const char*fil_oppføring,...){if(informasjonsteknologi_ugyldig)return;va_list argument_ARRAY;va_start(argument_ARRAY,fil_oppføring);int vare_COUNT=vsnprintf(Tekst+Tekststorleik,sizeof(Tekst)-Tekststorleik,fil_oppføring,argument_ARRAY);va_end(argument_ARRAY);if(vare_COUNT<0||(unsigned)vare_COUNT>=sizeof(Tekst)-Tekststorleik){informasjonsteknologi_ugyldig=1;return;}Tekststorleik+=vare_COUNT;}
static int 서술자(unsigned identifikator_VALUE,int*forretningsmål){
    if(identifikator_VALUE<1||identifikator_VALUE>=konstant_pulje||Merke_Liste[identifikator_VALUE]!=1)return -1;unsigned data_plassere=첫째값[identifikator_VALUE],avslutte_OFFSET=data_plassere+SECOND_VALUE[identifikator_VALUE];if(data_plassere>=avslutte_OFFSET||data[data_plassere++]!='(')return -1;int oppføring_COUNT=0;
    while(data_plassere<avslutte_OFFSET&&data[data_plassere]!=')'){
        unsigned teiknkode=data[data_plassere++];while(teiknkode=='['&&data_plassere<avslutte_OFFSET)teiknkode=data[data_plassere++];
        if(teiknkode=='L'){while(data_plassere<avslutte_OFFSET&&data[data_plassere]!=';')data_plassere++;if(data_plassere==avslutte_OFFSET)return -1;data_plassere++;}
        else if(teiknkode!='I'&&teiknkode!='Z'&&teiknkode!='B'&&teiknkode!='C'&&teiknkode!='S')return -1;
        if(++oppføring_COUNT>16)return -1;
    }
    if(data_plassere+1>=avslutte_OFFSET||data[data_plassere++]!=')')return -1;*forretningsmål=data[data_plassere]=='V'?0:1;
    if(data[data_plassere]=='J'||data[data_plassere]=='D'||data[data_plassere]=='F')return -1;return oppføring_COUNT;
}
static void attributt(void){unsigned vare_COUNT=절반값();for(unsigned 순번=0;순번<vare_COUNT&&!informasjonsteknologi_ugyldig;순번++){절반값();unsigned Storleik=가득참();TAKE_VALUE(Storleik);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned mindreårig_versjon=절반값(),판번호=절반값();if(mindreårig_versjon||판번호<45||판번호>52)return -1;
    konstant_pulje=절반값();if(konstant_pulje<1||konstant_pulje>512)return -1;
    for(unsigned 순번=1;순번<konstant_pulje&&!informasjonsteknologi_ugyldig;순번++){
        Merke_Liste[순번]=byte_data();switch(Merke_Liste[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=konstant_pulje)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=byte_data();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();betalt_time=절반값();절반값();if(betalt_time<1||betalt_time>=konstant_pulje||Merke_Liste[betalt_time]!=7||첫째값[betalt_time]<1||첫째값[betalt_time]>=konstant_pulje||Merke_Liste[첫째값[betalt_time]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!informasjonsteknologi_ugyldig;순번++){
        unsigned 설정비트=절반값();feltnamn[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned oppføring_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<oppføring_COUNT&&!informasjonsteknologi_ugyldig;안쪽순번++){
            unsigned Namn=절반값(),Storleik=가득참();
            if(UNICODE_VALUE(Namn,"ConstantValue")){if(Storleik!=2)return -1;felt_konstant[순번]=절반값();}
            else TAKE_VALUE(Storleik);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!informasjonsteknologi_ugyldig;순번++){
        metode_oppføring*gruppe_endre_storleik=메소드목록+순번;gruppe_endre_storleik->설정비트=절반값();gruppe_endre_storleik->Namn=절반값();gruppe_endre_storleik->서술값=절반값();unsigned oppføring_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<oppføring_COUNT&&!informasjonsteknologi_ugyldig;안쪽순번++){
            unsigned Namn=절반값(),Storleik=가득참(),Køyr_2=betalt_plassere;
            if(Storleik>lengd_VALUE-betalt_plassere)return -1;
            if(UNICODE_VALUE(Namn,"Code")){
                gruppe_endre_storleik->Stabel_Lagring=절반값();gruppe_endre_storleik->지역변수들=절반값();gruppe_endre_storleik->Storleik=가득참();gruppe_endre_storleik->instruksjon_SEQUENCE=TAKE_VALUE(gruppe_endre_storleik->Storleik);
                if(gruppe_endre_storleik->Stabel_Lagring>128||gruppe_endre_storleik->지역변수들>128||gruppe_endre_storleik->Storleik>8192||절반값())return -1;attributt();
            }else TAKE_VALUE(Storleik);
            if(betalt_plassere!=Køyr_2+Storleik)return -1;
        }
        if(!UNICODE_VALUE(gruppe_endre_storleik->Namn,"<init>")&&(!(gruppe_endre_storleik->설정비트&8)||(gruppe_endre_storleik->설정비트&(0x100|0x20))||!gruppe_endre_storleik->Storleik))return -1;
    }
    attributt();return informasjonsteknologi_ugyldig||betalt_plassere!=lengd_VALUE?-1:0;
}
static void konstant_VALUE(unsigned identifikator_VALUE){
    if(!identifikator_VALUE||identifikator_VALUE>=konstant_pulje){informasjonsteknologi_ugyldig=1;return;}
    if(Merke_Liste[identifikator_VALUE]==3)내보내기("P(%uU);",첫째값[identifikator_VALUE]);
    else if(Merke_Liste[identifikator_VALUE]==8)내보내기("P((W)k%u);",identifikator_VALUE);else informasjonsteknologi_ugyldig=1;
}
static void 호출(unsigned identifikator_VALUE,int virtuell_CALL){
    if(identifikator_VALUE<1||identifikator_VALUE>=konstant_pulje||(Merke_Liste[identifikator_VALUE]!=10&&Merke_Liste[identifikator_VALUE]!=11)||첫째값[identifikator_VALUE]<1||첫째값[identifikator_VALUE]>=konstant_pulje||Merke_Liste[첫째값[identifikator_VALUE]]!=7||SECOND_VALUE[identifikator_VALUE]<1||SECOND_VALUE[identifikator_VALUE]>=konstant_pulje||Merke_Liste[SECOND_VALUE[identifikator_VALUE]]!=12){informasjonsteknologi_ugyldig=1;return;}
    unsigned eigar_objekt=첫째값[첫째값[identifikator_VALUE]],Namn=첫째값[SECOND_VALUE[identifikator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikator_VALUE]];int forretningsmål=0,vare_COUNT=서술자(서술값,&forretningsmål);if(vare_COUNT<0){informasjonsteknologi_ugyldig=1;return;}
    for(int 순번=vare_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtuell_CALL)내보내기("Q();");
    if(!virtuell_CALL&&같음(eigar_objekt,첫째값[betalt_time])){
        unsigned gruppe_endre_storleik=0;for(;gruppe_endre_storleik<메소드개수;gruppe_endre_storleik++)if(같음(Namn,메소드목록[gruppe_endre_storleik].Namn)&&같음(서술값,메소드목록[gruppe_endre_storleik].서술값))break;
        if(gruppe_endre_storleik==메소드개수||!(메소드목록[gruppe_endre_storleik].설정비트&8)){informasjonsteknologi_ugyldig=1;return;}
        if(forretningsmål)내보내기("P(");내보내기("m%u(",gruppe_endre_storleik);for(int 순번=0;순번<vare_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(forretningsmål?"));":" );");return;
    }
    if((virtuell_CALL&&UNICODE_VALUE(eigar_objekt,"java/io/PrintStream")&& (UNICODE_VALUE(Namn,"print")||UNICODE_VALUE(Namn,"println")))||(!virtuell_CALL&&UNICODE_VALUE(eigar_objekt,"한국어/자체/Utdata"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Namn,"print")||UNICODE_VALUE(Namn,"println")||UNICODE_VALUE(Namn,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Namn,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Namn,"print")||UNICODE_VALUE(Namn,"println")||UNICODE_VALUE(Namn,"Skriv")||UNICODE_VALUE(Namn,"skrive_line"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Namn,"print")||UNICODE_VALUE(Namn,"Skriv")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Namn,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtuell_CALL&&UNICODE_VALUE(eigar_objekt,"한국어/자체/Fil")){
        if(UNICODE_VALUE(Namn,"Skriv")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Namn,"Les")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    informasjonsteknologi_ugyldig=1;
}
static void byggje_metode(unsigned LOOKUP_INDEX){
    metode_oppføring*gruppe_endre_storleik=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(gruppe_endre_storleik->Namn,"<init>"))return;int forretningsmål,vare_COUNT=서술자(gruppe_endre_storleik->서술값,&forretningsmål);if(vare_COUNT<0){informasjonsteknologi_ugyldig=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<vare_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!vare_COUNT)내보내기("void");
    if((unsigned)vare_COUNT>gruppe_endre_storleik->지역변수들){informasjonsteknologi_ugyldig=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",gruppe_endre_storleik->지역변수들?gruppe_endre_storleik->지역변수들:1);for(int 순번=0;순번<vare_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=lengd_VALUE;lengd_VALUE=gruppe_endre_storleik->instruksjon_SEQUENCE+gruppe_endre_storleik->Storleik;betalt_plassere=gruppe_endre_storleik->instruksjon_SEQUENCE;
    while(betalt_plassere<lengd_VALUE&&!informasjonsteknologi_ugyldig){unsigned kommando_plassere=betalt_plassere-gruppe_endre_storleik->instruksjon_SEQUENCE,operasjon_VALUE=byte_data();내보내기("L%u:;",kommando_plassere);
        if(operasjon_VALUE==0){}
        else if(operasjon_VALUE==1)내보내기("P(0);");
        else if(operasjon_VALUE>=2&&operasjon_VALUE<=8)내보내기("P(%uU);",operasjon_VALUE-3);
        else if(operasjon_VALUE==16){int VALUE=(int8_t)byte_data();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operasjon_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operasjon_VALUE==18||operasjon_VALUE==19)konstant_VALUE(operasjon_VALUE==18?byte_data():절반값());
        else if(operasjon_VALUE==21||operasjon_VALUE==25){unsigned 순번=byte_data();if(순번>=gruppe_endre_storleik->지역변수들)informasjonsteknologi_ugyldig=1;내보내기("P(v[%u]);",순번);}
        else if((operasjon_VALUE>=26&&operasjon_VALUE<=29)||(operasjon_VALUE>=42&&operasjon_VALUE<=45)){unsigned 순번=operasjon_VALUE>=42?operasjon_VALUE-42:operasjon_VALUE-26;if(순번>=gruppe_endre_storleik->지역변수들)informasjonsteknologi_ugyldig=1;내보내기("P(v[%u]);",순번);}
        else if(operasjon_VALUE==54||operasjon_VALUE==58){unsigned 순번=byte_data();if(순번>=gruppe_endre_storleik->지역변수들)informasjonsteknologi_ugyldig=1;내보내기("v[%u]=Q();",순번);}
        else if((operasjon_VALUE>=59&&operasjon_VALUE<=62)||(operasjon_VALUE>=75&&operasjon_VALUE<=78)){unsigned 순번=operasjon_VALUE>=75?operasjon_VALUE-75:operasjon_VALUE-59;if(순번>=gruppe_endre_storleik->지역변수들)informasjonsteknologi_ugyldig=1;내보내기("v[%u]=Q();",순번);}
        else if(operasjon_VALUE==46||operasjon_VALUE==50||operasjon_VALUE==51||operasjon_VALUE==52||operasjon_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operasjon_VALUE==79||operasjon_VALUE==83||operasjon_VALUE==84||operasjon_VALUE==85||operasjon_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operasjon_VALUE==84?"(unsigned)(signed char)q":operasjon_VALUE==85?"(unsigned short)q":operasjon_VALUE==86?"(unsigned)(short)q":"q");
        else if(operasjon_VALUE==87)내보내기("Q();");
        else if(operasjon_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(operasjon_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operasjon_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(operasjon_VALUE==96||operasjon_VALUE==100||operasjon_VALUE==104||operasjon_VALUE==120||operasjon_VALUE==124||operasjon_VALUE==126||operasjon_VALUE==128||operasjon_VALUE==130){const char*koding_VALUE=operasjon_VALUE==96?"+":operasjon_VALUE==100?"-":operasjon_VALUE==104?"*":operasjon_VALUE==120?"<<":operasjon_VALUE==124?">>":operasjon_VALUE==126?"&":operasjon_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",koding_VALUE,operasjon_VALUE==120||operasjon_VALUE==124?"%32":"");}
        else if(operasjon_VALUE==108||operasjon_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operasjon_VALUE==112);
        else if(operasjon_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(operasjon_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operasjon_VALUE==132){unsigned 순번=byte_data();int 차이=(int8_t)byte_data();if(순번>=gruppe_endre_storleik->지역변수들)informasjonsteknologi_ugyldig=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operasjon_VALUE>=145&&operasjon_VALUE<=147)내보내기("P((unsigned)(%s)Q());",operasjon_VALUE==145?"signed char":operasjon_VALUE==146?"unsigned short":"short");
        else if(operasjon_VALUE>=153&&operasjon_VALUE<=166){int mål=(int)kommando_plassere+(int16_t)절반값();const char*Samanlikning_VALUE[]={"==","!=","<",">=",">","<="};if(mål<0||mål>=(int)gruppe_endre_storleik->Storleik){informasjonsteknologi_ugyldig=1;break;}if(operasjon_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Samanlikning_VALUE[operasjon_VALUE-153],mål);else if(operasjon_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Samanlikning_VALUE[operasjon_VALUE-159],mål);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operasjon_VALUE==165?"==":"!=",mål);}
        else if(operasjon_VALUE==167){int mål=(int)kommando_plassere+(int16_t)절반값();if(mål<0||mål>=(int)gruppe_endre_storleik->Storleik)informasjonsteknologi_ugyldig=1;내보내기("goto L%d;",mål);}
        else if(operasjon_VALUE==172||operasjon_VALUE==176)내보내기("return Q();");else if(operasjon_VALUE==177)내보내기("return 0;");
        else if(operasjon_VALUE==178||operasjon_VALUE==179){unsigned identifikator_VALUE=절반값();if(identifikator_VALUE<1||identifikator_VALUE>=konstant_pulje||Merke_Liste[identifikator_VALUE]!=9||첫째값[identifikator_VALUE]>=konstant_pulje||SECOND_VALUE[identifikator_VALUE]>=konstant_pulje||Merke_Liste[첫째값[identifikator_VALUE]]!=7||Merke_Liste[SECOND_VALUE[identifikator_VALUE]]!=12){informasjonsteknologi_ugyldig=1;break;}unsigned eigar_objekt=첫째값[첫째값[identifikator_VALUE]],Namn=첫째값[SECOND_VALUE[identifikator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikator_VALUE]];
            if(operasjon_VALUE==178&&UNICODE_VALUE(eigar_objekt,"java/lang/System")&&UNICODE_VALUE(Namn,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned fil_oppføring=0;while(fil_oppføring<필드개수&&(!같음(Namn,feltnamn[fil_oppføring])||!같음(서술값,필드서술[fil_oppføring])))fil_oppføring++;if(!같음(eigar_objekt,첫째값[betalt_time])||fil_oppføring==필드개수){informasjonsteknologi_ugyldig=1;break;}내보내기(operasjon_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",fil_oppføring);}}
        else if(operasjon_VALUE==182||operasjon_VALUE==184)호출(절반값(),operasjon_VALUE==182);
        else if(operasjon_VALUE==188){unsigned TYPE_kategori=byte_data();if(TYPE_kategori!=4&&TYPE_kategori!=5&&TYPE_kategori!=8&&TYPE_kategori!=9&&TYPE_kategori!=10)informasjonsteknologi_ugyldig=1;내보내기("P(jarray((int)Q()));");}
        else if(operasjon_VALUE==190)내보내기("P(jlength(Q()));");
        else if(operasjon_VALUE==198||operasjon_VALUE==199){int mål=(int)kommando_plassere+(int16_t)절반값();if(mål<0||mål>=(int)gruppe_endre_storleik->Storleik)informasjonsteknologi_ugyldig=1;내보내기("if(Q()%s0)goto L%d;",operasjon_VALUE==198?"==":"!=",mål);}
        else informasjonsteknologi_ugyldig=1;
        if(informasjonsteknologi_ugyldig)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,operasjon_VALUE,kommando_plassere);
        내보내기("\n");
    }
    lengd_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned streng_leksjon(unsigned *data_plassere,unsigned avslutte_OFFSET){
    if(*data_plassere>=avslutte_OFFSET){informasjonsteknologi_ugyldig=1;return 0;}unsigned teiknkode=data[(*data_plassere)++];
    if(teiknkode<128)return teiknkode;
    unsigned vare_COUNT=teiknkode>=0xc0&&teiknkode<=0xdf?1:teiknkode>=0xe0&&teiknkode<=0xef?2:3;
    if(vare_COUNT==3||vare_COUNT>avslutte_OFFSET-*data_plassere){informasjonsteknologi_ugyldig=1;return 0;}unsigned VALUE=teiknkode&((1u<<(6-vare_COUNT))-1);
    for(unsigned 순번=0;순번<vare_COUNT;순번++){unsigned Neste_vare=data[(*data_plassere)++];if((Neste_vare&0xc0)!=0x80)informasjonsteknologi_ugyldig=1;VALUE=VALUE<<6|(Neste_vare&63);}
    if((vare_COUNT==1&&VALUE<128&&VALUE!=0)||(vare_COUNT==2&&VALUE<2048))informasjonsteknologi_ugyldig=1;return VALUE;
}
static void streng_konstant(unsigned identifikator_VALUE){
    unsigned 부호없는값=첫째값[identifikator_VALUE];if(부호없는값<1||부호없는값>=konstant_pulje||Merke_Liste[부호없는값]!=1){informasjonsteknologi_ugyldig=1;return;}내보내기("static const unsigned char k%u[]={",identifikator_VALUE);
    unsigned data_plassere=첫째값[부호없는값],avslutte_OFFSET=data_plassere+SECOND_VALUE[부호없는값];
    while(data_plassere<avslutte_OFFSET&&!informasjonsteknologi_ugyldig){unsigned teiknkode=streng_leksjon(&data_plassere,avslutte_OFFSET);
        if(teiknkode>=0xd800&&teiknkode<=0xdbff){unsigned 낮은부분=streng_leksjon(&data_plassere,avslutte_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){informasjonsteknologi_ugyldig=1;break;}teiknkode=0x10000+((teiknkode-0xd800)<<10)+낮은부분-0xdc00;}
        else if(teiknkode>=0xdc00&&teiknkode<=0xdfff){informasjonsteknologi_ugyldig=1;break;}
        if(!teiknkode){printf("jaot: embedded NUL string needs JVM mode\n");informasjonsteknologi_ugyldig=1;break;}
        if(teiknkode<128)내보내기("%u,",teiknkode);
        else{unsigned vare_COUNT=teiknkode<2048?2:teiknkode<65536?3:4;내보내기("%u,",(vare_COUNT==2?0xc0:vare_COUNT==3?0xe0:0xf0)|(teiknkode>>(6*(vare_COUNT-1))));for(unsigned 순번=vare_COUNT-1;순번;순번--)내보내기("%u,",0x80|((teiknkode>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Namn){
    size_t vare_COUNT=strlen(Namn);
    if(vare_COUNT>4&&!strcmp(Namn+vare_COUNT-4,".jar")){
        if(꾸러미열기(Namn)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char STIGE[256];const char*oppføring_metode=꾸러미진입클래스();vare_COUNT=strlen(oppføring_metode);if(vare_COUNT+6>=sizeof(STIGE))return 0;
        for(unsigned 순번=0;순번<vare_COUNT;순번++)STIGE[순번]=oppføring_metode[순번]=='.'?'/':oppføring_metode[순번];strcpy(STIGE+vare_COUNT,".class");int oppføring_COUNT=꾸러미읽기(STIGE,data,sizeof(data));if(oppføring_COUNT<0)return 0;lengd_VALUE=oppføring_COUNT;
    }else{intptr_t fil_handtak=사용자호출(3,(uintptr_t)Namn,0,0,0,0,0);if(fil_handtak<0)return 0;intptr_t oppføring_COUNT=사용자호출(9,fil_handtak,0,0,0,0,0);if(oppføring_COUNT<0||oppføring_COUNT>sizeof(data)){사용자호출(4,fil_handtak,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,fil_handtak,(uintptr_t)data,oppføring_COUNT,0,0,0);사용자호출(4,fil_handtak,0,0,0,0,0);if(RECEIVED_COUNT!=oppføring_COUNT)return 0;lengd_VALUE=oppføring_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstant_pulje&&!informasjonsteknologi_ugyldig;순번++)if(Merke_Liste[순번]==8)streng_konstant(순번);
    if(informasjonsteknologi_ugyldig)return 0;
    int oppføring_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Namn,"<init>")){
        int forretningsmål,oppføring_COUNT=서술자(메소드목록[순번].서술값,&forretningsmål);if(oppføring_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<oppføring_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!oppføring_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Namn,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)oppføring_p=순번;
        if(UNICODE_VALUE(메소드목록[순번].Namn,"<clinit>"))초기값=순번;
    }
    if(oppføring_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!informasjonsteknologi_ugyldig;순번++)byggje_metode(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(felt_konstant[순번]){
        unsigned teiknkode=felt_konstant[순번];if(teiknkode>=konstant_pulje)return 0;
        if(Merke_Liste[teiknkode]==3)내보내기("fields[%u]=%uU;",순번,첫째값[teiknkode]);else if(Merke_Liste[teiknkode]==8)내보내기("fields[%u]=(W)k%u;",순번,teiknkode);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",oppføring_p);
    return informasjonsteknologi_ugyldig?0:Tekst;
}
