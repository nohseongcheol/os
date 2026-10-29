#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "bondel.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char data[16384];static unsigned lengte_VALUE,현재위치;static int 잘못됨;
static unsigned Merkers_Lys[512],첫째값[512],SECOND_VALUE[512],konstante_poel,현재클래스;
static char Teks[65536];static unsigned teksgrootte;
typedef struct {unsigned konfigurasie_Agtergrond_intelligente_oordragdiens,Naam,서술값,instruksie_SEQUENCE,Grootte,지역변수들,Stapel_Berging;} metode_inskrywing;
static metode_inskrywing 메소드목록[64];static unsigned 메소드개수;
static unsigned veldnaam[64],필드서술[64],veld_konstante[64],필드개수;
static unsigned TAKE_VALUE(unsigned item_COUNT){if(현재위치>lengte_VALUE||item_COUNT>lengte_VALUE-현재위치){잘못됨=1;return 0;}unsigned data_plaas=현재위치;현재위치+=item_COUNT;return data_plaas;}
static unsigned greep_data(void){unsigned data_plaas=TAKE_VALUE(1);return 잘못됨?0:data[data_plaas];}
static unsigned 절반값(void){unsigned x_koördinaat=greep_data();return x_koördinaat<<8|greep_data();}
static uint32_t 가득참(void){uint32_t x_koördinaat=절반값();return x_koördinaat<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*string_data){return 순번>0&&순번<konstante_poel&&Merkers_Lys[순번]==1&&strlen(string_data)==SECOND_VALUE[순번]&&!memcmp(data+첫째값[순번],string_data,SECOND_VALUE[순번]);}
static int 같음(unsigned x_koördinaat,unsigned Y_koördinaat){return x_koördinaat>0&&x_koördinaat<konstante_poel&&Y_koördinaat>0&&Y_koördinaat<konstante_poel&&Merkers_Lys[x_koördinaat]==1&&Merkers_Lys[Y_koördinaat]==1&&SECOND_VALUE[x_koördinaat]==SECOND_VALUE[Y_koördinaat]&&!memcmp(data+첫째값[x_koördinaat],data+첫째값[Y_koördinaat],SECOND_VALUE[x_koördinaat]);}
static void 내보내기(const char*lêer_inskrywing,...){if(잘못됨)return;va_list argument_ARRAY;va_start(argument_ARRAY,lêer_inskrywing);int item_COUNT=vsnprintf(Teks+teksgrootte,sizeof(Teks)-teksgrootte,lêer_inskrywing,argument_ARRAY);va_end(argument_ARRAY);if(item_COUNT<0||(unsigned)item_COUNT>=sizeof(Teks)-teksgrootte){잘못됨=1;return;}teksgrootte+=item_COUNT;}
static int 서술자(unsigned waarde_VALUE,int*maatreël){
    if(waarde_VALUE<1||waarde_VALUE>=konstante_poel||Merkers_Lys[waarde_VALUE]!=1)return -1;unsigned data_plaas=첫째값[waarde_VALUE],beëindig_OFFSET=data_plaas+SECOND_VALUE[waarde_VALUE];if(data_plaas>=beëindig_OFFSET||data[data_plaas++]!='(')return -1;int inskrywing_COUNT=0;
    while(data_plaas<beëindig_OFFSET&&data[data_plaas]!=')'){
        unsigned karakterkode=data[data_plaas++];while(karakterkode=='['&&data_plaas<beëindig_OFFSET)karakterkode=data[data_plaas++];
        if(karakterkode=='L'){while(data_plaas<beëindig_OFFSET&&data[data_plaas]!=';')data_plaas++;if(data_plaas==beëindig_OFFSET)return -1;data_plaas++;}
        else if(karakterkode!='I'&&karakterkode!='Z'&&karakterkode!='B'&&karakterkode!='C'&&karakterkode!='S')return -1;
        if(++inskrywing_COUNT>16)return -1;
    }
    if(data_plaas+1>=beëindig_OFFSET||data[data_plaas++]!=')')return -1;*maatreël=data[data_plaas]=='V'?0:1;
    if(data[data_plaas]=='J'||data[data_plaas]=='D'||data[data_plaas]=='F')return -1;return inskrywing_COUNT;
}
static void kenmerke(void){unsigned item_COUNT=절반값();for(unsigned 순번=0;순번<item_COUNT&&!잘못됨;순번++){절반값();unsigned Grootte=가득참();TAKE_VALUE(Grootte);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned minderjarige_weergawe=절반값(),판번호=절반값();if(minderjarige_weergawe||판번호<45||판번호>52)return -1;
    konstante_poel=절반값();if(konstante_poel<1||konstante_poel>512)return -1;
    for(unsigned 순번=1;순번<konstante_poel&&!잘못됨;순번++){
        Merkers_Lys[순번]=greep_data();switch(Merkers_Lys[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=konstante_poel)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=greep_data();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=konstante_poel||Merkers_Lys[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=konstante_poel||Merkers_Lys[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned konfigurasie_Agtergrond_intelligente_oordragdiens=절반값();veldnaam[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfigurasie_Agtergrond_intelligente_oordragdiens&8))return -1;
        unsigned inskrywing_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<inskrywing_COUNT&&!잘못됨;안쪽순번++){
            unsigned Naam=절반값(),Grootte=가득참();
            if(UNICODE_VALUE(Naam,"ConstantValue")){if(Grootte!=2)return -1;veld_konstante[순번]=절반값();}
            else TAKE_VALUE(Grootte);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        metode_inskrywing*Groep_verstel=메소드목록+순번;Groep_verstel->konfigurasie_Agtergrond_intelligente_oordragdiens=절반값();Groep_verstel->Naam=절반값();Groep_verstel->서술값=절반값();unsigned inskrywing_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<inskrywing_COUNT&&!잘못됨;안쪽순번++){
            unsigned Naam=절반값(),Grootte=가득참(),Loop=현재위치;
            if(Grootte>lengte_VALUE-현재위치)return -1;
            if(UNICODE_VALUE(Naam,"Code")){
                Groep_verstel->Stapel_Berging=절반값();Groep_verstel->지역변수들=절반값();Groep_verstel->Grootte=가득참();Groep_verstel->instruksie_SEQUENCE=TAKE_VALUE(Groep_verstel->Grootte);
                if(Groep_verstel->Stapel_Berging>128||Groep_verstel->지역변수들>128||Groep_verstel->Grootte>8192||절반값())return -1;kenmerke();
            }else TAKE_VALUE(Grootte);
            if(현재위치!=Loop+Grootte)return -1;
        }
        if(!UNICODE_VALUE(Groep_verstel->Naam,"<init>")&&(!(Groep_verstel->konfigurasie_Agtergrond_intelligente_oordragdiens&8)||(Groep_verstel->konfigurasie_Agtergrond_intelligente_oordragdiens&(0x100|0x20))||!Groep_verstel->Grootte))return -1;
    }
    kenmerke();return 잘못됨||현재위치!=lengte_VALUE?-1:0;
}
static void konstante_VALUE(unsigned waarde_VALUE){
    if(!waarde_VALUE||waarde_VALUE>=konstante_poel){잘못됨=1;return;}
    if(Merkers_Lys[waarde_VALUE]==3)내보내기("P(%uU);",첫째값[waarde_VALUE]);
    else if(Merkers_Lys[waarde_VALUE]==8)내보내기("P((W)k%u);",waarde_VALUE);else 잘못됨=1;
}
static void 호출(unsigned waarde_VALUE,int virtueel_Bel){
    if(waarde_VALUE<1||waarde_VALUE>=konstante_poel||(Merkers_Lys[waarde_VALUE]!=10&&Merkers_Lys[waarde_VALUE]!=11)||첫째값[waarde_VALUE]<1||첫째값[waarde_VALUE]>=konstante_poel||Merkers_Lys[첫째값[waarde_VALUE]]!=7||SECOND_VALUE[waarde_VALUE]<1||SECOND_VALUE[waarde_VALUE]>=konstante_poel||Merkers_Lys[SECOND_VALUE[waarde_VALUE]]!=12){잘못됨=1;return;}
    unsigned eienaar_objek=첫째값[첫째값[waarde_VALUE]],Naam=첫째값[SECOND_VALUE[waarde_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[waarde_VALUE]];int maatreël=0,item_COUNT=서술자(서술값,&maatreël);if(item_COUNT<0){잘못됨=1;return;}
    for(int 순번=item_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtueel_Bel)내보내기("Q();");
    if(!virtueel_Bel&&같음(eienaar_objek,첫째값[현재클래스])){
        unsigned Groep_verstel=0;for(;Groep_verstel<메소드개수;Groep_verstel++)if(같음(Naam,메소드목록[Groep_verstel].Naam)&&같음(서술값,메소드목록[Groep_verstel].서술값))break;
        if(Groep_verstel==메소드개수||!(메소드목록[Groep_verstel].konfigurasie_Agtergrond_intelligente_oordragdiens&8)){잘못됨=1;return;}
        if(maatreël)내보내기("P(");내보내기("m%u(",Groep_verstel);for(int 순번=0;순번<item_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(maatreël?"));":" );");return;
    }
    if((virtueel_Bel&&UNICODE_VALUE(eienaar_objek,"java/io/PrintStream")&& (UNICODE_VALUE(Naam,"print")||UNICODE_VALUE(Naam,"println")))||(!virtueel_Bel&&UNICODE_VALUE(eienaar_objek,"한국어/자체/Afvoer"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Naam,"print")||UNICODE_VALUE(Naam,"println")||UNICODE_VALUE(Naam,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Naam,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Naam,"print")||UNICODE_VALUE(Naam,"println")||UNICODE_VALUE(Naam,"Skryf")||UNICODE_VALUE(Naam,"skryf_lyn"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Naam,"print")||UNICODE_VALUE(Naam,"Skryf")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Naam,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtueel_Bel&&UNICODE_VALUE(eienaar_objek,"한국어/자체/Lêer")){
        if(UNICODE_VALUE(Naam,"Skryf")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Naam,"Lees")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void bou_metode(unsigned LOOKUP_INDEX){
    metode_inskrywing*Groep_verstel=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(Groep_verstel->Naam,"<init>"))return;int maatreël,item_COUNT=서술자(Groep_verstel->서술값,&maatreël);if(item_COUNT<0){잘못됨=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<item_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!item_COUNT)내보내기("void");
    if((unsigned)item_COUNT>Groep_verstel->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Groep_verstel->지역변수들?Groep_verstel->지역변수들:1);for(int 순번=0;순번<item_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=lengte_VALUE;lengte_VALUE=Groep_verstel->instruksie_SEQUENCE+Groep_verstel->Grootte;현재위치=Groep_verstel->instruksie_SEQUENCE;
    while(현재위치<lengte_VALUE&&!잘못됨){unsigned bevel_plaas=현재위치-Groep_verstel->instruksie_SEQUENCE,werking_VALUE=greep_data();내보내기("L%u:;",bevel_plaas);
        if(werking_VALUE==0){}
        else if(werking_VALUE==1)내보내기("P(0);");
        else if(werking_VALUE>=2&&werking_VALUE<=8)내보내기("P(%uU);",werking_VALUE-3);
        else if(werking_VALUE==16){int VALUE=(int8_t)greep_data();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(werking_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(werking_VALUE==18||werking_VALUE==19)konstante_VALUE(werking_VALUE==18?greep_data():절반값());
        else if(werking_VALUE==21||werking_VALUE==25){unsigned 순번=greep_data();if(순번>=Groep_verstel->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((werking_VALUE>=26&&werking_VALUE<=29)||(werking_VALUE>=42&&werking_VALUE<=45)){unsigned 순번=werking_VALUE>=42?werking_VALUE-42:werking_VALUE-26;if(순번>=Groep_verstel->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(werking_VALUE==54||werking_VALUE==58){unsigned 순번=greep_data();if(순번>=Groep_verstel->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((werking_VALUE>=59&&werking_VALUE<=62)||(werking_VALUE>=75&&werking_VALUE<=78)){unsigned 순번=werking_VALUE>=75?werking_VALUE-75:werking_VALUE-59;if(순번>=Groep_verstel->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(werking_VALUE==46||werking_VALUE==50||werking_VALUE==51||werking_VALUE==52||werking_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(werking_VALUE==79||werking_VALUE==83||werking_VALUE==84||werking_VALUE==85||werking_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",werking_VALUE==84?"(unsigned)(signed char)q":werking_VALUE==85?"(unsigned short)q":werking_VALUE==86?"(unsigned)(short)q":"q");
        else if(werking_VALUE==87)내보내기("Q();");
        else if(werking_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(werking_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(werking_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(werking_VALUE==96||werking_VALUE==100||werking_VALUE==104||werking_VALUE==120||werking_VALUE==124||werking_VALUE==126||werking_VALUE==128||werking_VALUE==130){const char*enkodering_VALUE=werking_VALUE==96?"+":werking_VALUE==100?"-":werking_VALUE==104?"*":werking_VALUE==120?"<<":werking_VALUE==124?">>":werking_VALUE==126?"&":werking_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",enkodering_VALUE,werking_VALUE==120||werking_VALUE==124?"%32":"");}
        else if(werking_VALUE==108||werking_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",werking_VALUE==112);
        else if(werking_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(werking_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(werking_VALUE==132){unsigned 순번=greep_data();int 차이=(int8_t)greep_data();if(순번>=Groep_verstel->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(werking_VALUE>=145&&werking_VALUE<=147)내보내기("P((unsigned)(%s)Q());",werking_VALUE==145?"signed char":werking_VALUE==146?"unsigned short":"short");
        else if(werking_VALUE>=153&&werking_VALUE<=166){int teiken=(int)bevel_plaas+(int16_t)절반값();const char*Vergelyking_VALUE[]={"==","!=","<",">=",">","<="};if(teiken<0||teiken>=(int)Groep_verstel->Grootte){잘못됨=1;break;}if(werking_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Vergelyking_VALUE[werking_VALUE-153],teiken);else if(werking_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Vergelyking_VALUE[werking_VALUE-159],teiken);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",werking_VALUE==165?"==":"!=",teiken);}
        else if(werking_VALUE==167){int teiken=(int)bevel_plaas+(int16_t)절반값();if(teiken<0||teiken>=(int)Groep_verstel->Grootte)잘못됨=1;내보내기("goto L%d;",teiken);}
        else if(werking_VALUE==172||werking_VALUE==176)내보내기("return Q();");else if(werking_VALUE==177)내보내기("return 0;");
        else if(werking_VALUE==178||werking_VALUE==179){unsigned waarde_VALUE=절반값();if(waarde_VALUE<1||waarde_VALUE>=konstante_poel||Merkers_Lys[waarde_VALUE]!=9||첫째값[waarde_VALUE]>=konstante_poel||SECOND_VALUE[waarde_VALUE]>=konstante_poel||Merkers_Lys[첫째값[waarde_VALUE]]!=7||Merkers_Lys[SECOND_VALUE[waarde_VALUE]]!=12){잘못됨=1;break;}unsigned eienaar_objek=첫째값[첫째값[waarde_VALUE]],Naam=첫째값[SECOND_VALUE[waarde_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[waarde_VALUE]];
            if(werking_VALUE==178&&UNICODE_VALUE(eienaar_objek,"java/lang/System")&&UNICODE_VALUE(Naam,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned lêer_inskrywing=0;while(lêer_inskrywing<필드개수&&(!같음(Naam,veldnaam[lêer_inskrywing])||!같음(서술값,필드서술[lêer_inskrywing])))lêer_inskrywing++;if(!같음(eienaar_objek,첫째값[현재클래스])||lêer_inskrywing==필드개수){잘못됨=1;break;}내보내기(werking_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",lêer_inskrywing);}}
        else if(werking_VALUE==182||werking_VALUE==184)호출(절반값(),werking_VALUE==182);
        else if(werking_VALUE==188){unsigned TYPE_kategorie=greep_data();if(TYPE_kategorie!=4&&TYPE_kategorie!=5&&TYPE_kategorie!=8&&TYPE_kategorie!=9&&TYPE_kategorie!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(werking_VALUE==190)내보내기("P(jlength(Q()));");
        else if(werking_VALUE==198||werking_VALUE==199){int teiken=(int)bevel_plaas+(int16_t)절반값();if(teiken<0||teiken>=(int)Groep_verstel->Grootte)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",werking_VALUE==198?"==":"!=",teiken);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,werking_VALUE,bevel_plaas);
        내보내기("\n");
    }
    lengte_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned string_les(unsigned *data_plaas,unsigned beëindig_OFFSET){
    if(*data_plaas>=beëindig_OFFSET){잘못됨=1;return 0;}unsigned karakterkode=data[(*data_plaas)++];
    if(karakterkode<128)return karakterkode;
    unsigned item_COUNT=karakterkode>=0xc0&&karakterkode<=0xdf?1:karakterkode>=0xe0&&karakterkode<=0xef?2:3;
    if(item_COUNT==3||item_COUNT>beëindig_OFFSET-*data_plaas){잘못됨=1;return 0;}unsigned VALUE=karakterkode&((1u<<(6-item_COUNT))-1);
    for(unsigned 순번=0;순번<item_COUNT;순번++){unsigned Volgende_item=data[(*data_plaas)++];if((Volgende_item&0xc0)!=0x80)잘못됨=1;VALUE=VALUE<<6|(Volgende_item&63);}
    if((item_COUNT==1&&VALUE<128&&VALUE!=0)||(item_COUNT==2&&VALUE<2048))잘못됨=1;return VALUE;
}
static void string_konstante(unsigned waarde_VALUE){
    unsigned 부호없는값=첫째값[waarde_VALUE];if(부호없는값<1||부호없는값>=konstante_poel||Merkers_Lys[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",waarde_VALUE);
    unsigned data_plaas=첫째값[부호없는값],beëindig_OFFSET=data_plaas+SECOND_VALUE[부호없는값];
    while(data_plaas<beëindig_OFFSET&&!잘못됨){unsigned karakterkode=string_les(&data_plaas,beëindig_OFFSET);
        if(karakterkode>=0xd800&&karakterkode<=0xdbff){unsigned 낮은부분=string_les(&data_plaas,beëindig_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}karakterkode=0x10000+((karakterkode-0xd800)<<10)+낮은부분-0xdc00;}
        else if(karakterkode>=0xdc00&&karakterkode<=0xdfff){잘못됨=1;break;}
        if(!karakterkode){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(karakterkode<128)내보내기("%u,",karakterkode);
        else{unsigned item_COUNT=karakterkode<2048?2:karakterkode<65536?3:4;내보내기("%u,",(item_COUNT==2?0xc0:item_COUNT==3?0xe0:0xf0)|(karakterkode>>(6*(item_COUNT-1))));for(unsigned 순번=item_COUNT-1;순번;순번--)내보내기("%u,",0x80|((karakterkode>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Naam){
    size_t item_COUNT=strlen(Naam);
    if(item_COUNT>4&&!strcmp(Naam+item_COUNT-4,".jar")){
        if(꾸러미열기(Naam)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Pad[256];const char*inskrywing_metode=꾸러미진입클래스();item_COUNT=strlen(inskrywing_metode);if(item_COUNT+6>=sizeof(Pad))return 0;
        for(unsigned 순번=0;순번<item_COUNT;순번++)Pad[순번]=inskrywing_metode[순번]=='.'?'/':inskrywing_metode[순번];strcpy(Pad+item_COUNT,".class");int inskrywing_COUNT=꾸러미읽기(Pad,data,sizeof(data));if(inskrywing_COUNT<0)return 0;lengte_VALUE=inskrywing_COUNT;
    }else{intptr_t lêer_handvatsel=사용자호출(3,(uintptr_t)Naam,0,0,0,0,0);if(lêer_handvatsel<0)return 0;intptr_t inskrywing_COUNT=사용자호출(9,lêer_handvatsel,0,0,0,0,0);if(inskrywing_COUNT<0||inskrywing_COUNT>sizeof(data)){사용자호출(4,lêer_handvatsel,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,lêer_handvatsel,(uintptr_t)data,inskrywing_COUNT,0,0,0);사용자호출(4,lêer_handvatsel,0,0,0,0,0);if(RECEIVED_COUNT!=inskrywing_COUNT)return 0;lengte_VALUE=inskrywing_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstante_poel&&!잘못됨;순번++)if(Merkers_Lys[순번]==8)string_konstante(순번);
    if(잘못됨)return 0;
    int inskrywing_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Naam,"<init>")){
        int maatreël,inskrywing_COUNT=서술자(메소드목록[순번].서술값,&maatreël);if(inskrywing_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<inskrywing_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!inskrywing_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Naam,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfigurasie_Agtergrond_intelligente_oordragdiens&9)==9)inskrywing_p=순번;
        if(UNICODE_VALUE(메소드목록[순번].Naam,"<clinit>"))초기값=순번;
    }
    if(inskrywing_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)bou_metode(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(veld_konstante[순번]){
        unsigned karakterkode=veld_konstante[순번];if(karakterkode>=konstante_poel)return 0;
        if(Merkers_Lys[karakterkode]==3)내보내기("fields[%u]=%uU;",순번,첫째값[karakterkode]);else if(Merkers_Lys[karakterkode]==8)내보내기("fields[%u]=(W)k%u;",순번,karakterkode);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",inskrywing_p);
    return 잘못됨?0:Teks;
}
