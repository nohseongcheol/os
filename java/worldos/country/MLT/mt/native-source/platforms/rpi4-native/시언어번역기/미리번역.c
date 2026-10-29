#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "lott.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char data[16384];static unsigned tul_VALUE,현재위치;static int 잘못됨;
static unsigned Tags_Lista[512],첫째값[512],SECOND_VALUE[512],상수모음,현재클래스;
static char SMS[65536];static unsigned daqs_tat_test;
typedef struct {unsigned 설정비트,isem,서술값,istruzzjoni_SEQUENCE,daqqas,지역변수들,Munzell_Ħażna;} metodu_entrata;
static metodu_entrata 메소드목록[64];static unsigned 메소드개수;
static unsigned isem_il_qasam[64],필드서술[64],qasam_valur_fiss[64],필드개수;
static unsigned TAKE_VALUE(unsigned element_COUNT){if(현재위치>tul_VALUE||element_COUNT>tul_VALUE-현재위치){잘못됨=1;return 0;}unsigned data_pożizzjoni=현재위치;현재위치+=element_COUNT;return data_pożizzjoni;}
static unsigned byte_data(void){unsigned data_pożizzjoni=TAKE_VALUE(1);return 잘못됨?0:data[data_pożizzjoni];}
static unsigned 절반값(void){unsigned koordinat_x=byte_data();return koordinat_x<<8|byte_data();}
static uint32_t 가득참(void){uint32_t koordinat_x=절반값();return koordinat_x<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*string_data){return 순번>0&&순번<상수모음&&Tags_Lista[순번]==1&&strlen(string_data)==SECOND_VALUE[순번]&&!memcmp(data+첫째값[순번],string_data,SECOND_VALUE[순번]);}
static int 같음(unsigned koordinat_x,unsigned 세로좌표){return koordinat_x>0&&koordinat_x<상수모음&&세로좌표>0&&세로좌표<상수모음&&Tags_Lista[koordinat_x]==1&&Tags_Lista[세로좌표]==1&&SECOND_VALUE[koordinat_x]==SECOND_VALUE[세로좌표]&&!memcmp(data+첫째값[koordinat_x],data+첫째값[세로좌표],SECOND_VALUE[koordinat_x]);}
static void 내보내기(const char*fajl_entrata,...){if(잘못됨)return;va_list argument_ARRAY;va_start(argument_ARRAY,fajl_entrata);int element_COUNT=vsnprintf(SMS+daqs_tat_test,sizeof(SMS)-daqs_tat_test,fajl_entrata,argument_ARRAY);va_end(argument_ARRAY);if(element_COUNT<0||(unsigned)element_COUNT>=sizeof(SMS)-daqs_tat_test){잘못됨=1;return;}daqs_tat_test+=element_COUNT;}
static int 서술자(unsigned identifikatur_VALUE,int*miżura){
    if(identifikatur_VALUE<1||identifikatur_VALUE>=상수모음||Tags_Lista[identifikatur_VALUE]!=1)return -1;unsigned data_pożizzjoni=첫째값[identifikatur_VALUE],ttermina_OFFSET=data_pożizzjoni+SECOND_VALUE[identifikatur_VALUE];if(data_pożizzjoni>=ttermina_OFFSET||data[data_pożizzjoni++]!='(')return -1;int entrata_COUNT=0;
    while(data_pożizzjoni<ttermina_OFFSET&&data[data_pożizzjoni]!=')'){
        unsigned kodiċi_tal_karattru=data[data_pożizzjoni++];while(kodiċi_tal_karattru=='['&&data_pożizzjoni<ttermina_OFFSET)kodiċi_tal_karattru=data[data_pożizzjoni++];
        if(kodiċi_tal_karattru=='L'){while(data_pożizzjoni<ttermina_OFFSET&&data[data_pożizzjoni]!=';')data_pożizzjoni++;if(data_pożizzjoni==ttermina_OFFSET)return -1;data_pożizzjoni++;}
        else if(kodiċi_tal_karattru!='I'&&kodiċi_tal_karattru!='Z'&&kodiċi_tal_karattru!='B'&&kodiċi_tal_karattru!='C'&&kodiċi_tal_karattru!='S')return -1;
        if(++entrata_COUNT>16)return -1;
    }
    if(data_pożizzjoni+1>=ttermina_OFFSET||data[data_pożizzjoni++]!=')')return -1;*miżura=data[data_pożizzjoni]=='V'?0:1;
    if(data[data_pożizzjoni]=='J'||data[data_pożizzjoni]=='D'||data[data_pożizzjoni]=='F')return -1;return entrata_COUNT;
}
static void 속성들(void){unsigned element_COUNT=절반값();for(unsigned 순번=0;순번<element_COUNT&&!잘못됨;순번++){절반값();unsigned daqqas=가득참();TAKE_VALUE(daqqas);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned minorenni_verżjoni=절반값(),판번호=절반값();if(minorenni_verżjoni||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        Tags_Lista[순번]=byte_data();switch(Tags_Lista[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=byte_data();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Tags_Lista[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Tags_Lista[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();isem_il_qasam[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned entrata_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<entrata_COUNT&&!잘못됨;안쪽순번++){
            unsigned isem=절반값(),daqqas=가득참();
            if(UNICODE_VALUE(isem,"ConstantValue")){if(daqqas!=2)return -1;qasam_valur_fiss[순번]=절반값();}
            else TAKE_VALUE(daqqas);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        metodu_entrata*grupp_daqqas=메소드목록+순번;grupp_daqqas->설정비트=절반값();grupp_daqqas->isem=절반값();grupp_daqqas->서술값=절반값();unsigned entrata_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<entrata_COUNT&&!잘못됨;안쪽순번++){
            unsigned isem=절반값(),daqqas=가득참(),serje=현재위치;
            if(daqqas>tul_VALUE-현재위치)return -1;
            if(UNICODE_VALUE(isem,"Code")){
                grupp_daqqas->Munzell_Ħażna=절반값();grupp_daqqas->지역변수들=절반값();grupp_daqqas->daqqas=가득참();grupp_daqqas->istruzzjoni_SEQUENCE=TAKE_VALUE(grupp_daqqas->daqqas);
                if(grupp_daqqas->Munzell_Ħażna>128||grupp_daqqas->지역변수들>128||grupp_daqqas->daqqas>8192||절반값())return -1;속성들();
            }else TAKE_VALUE(daqqas);
            if(현재위치!=serje+daqqas)return -1;
        }
        if(!UNICODE_VALUE(grupp_daqqas->isem,"<init>")&&(!(grupp_daqqas->설정비트&8)||(grupp_daqqas->설정비트&(0x100|0x20))||!grupp_daqqas->daqqas))return -1;
    }
    속성들();return 잘못됨||현재위치!=tul_VALUE?-1:0;
}
static void valur_fiss_VALUE(unsigned identifikatur_VALUE){
    if(!identifikatur_VALUE||identifikatur_VALUE>=상수모음){잘못됨=1;return;}
    if(Tags_Lista[identifikatur_VALUE]==3)내보내기("P(%uU);",첫째값[identifikatur_VALUE]);
    else if(Tags_Lista[identifikatur_VALUE]==8)내보내기("P((W)k%u);",identifikatur_VALUE);else 잘못됨=1;
}
static void 호출(unsigned identifikatur_VALUE,int virtwali_CALL){
    if(identifikatur_VALUE<1||identifikatur_VALUE>=상수모음||(Tags_Lista[identifikatur_VALUE]!=10&&Tags_Lista[identifikatur_VALUE]!=11)||첫째값[identifikatur_VALUE]<1||첫째값[identifikatur_VALUE]>=상수모음||Tags_Lista[첫째값[identifikatur_VALUE]]!=7||SECOND_VALUE[identifikatur_VALUE]<1||SECOND_VALUE[identifikatur_VALUE]>=상수모음||Tags_Lista[SECOND_VALUE[identifikatur_VALUE]]!=12){잘못됨=1;return;}
    unsigned propjetarju_oġġett=첫째값[첫째값[identifikatur_VALUE]],isem=첫째값[SECOND_VALUE[identifikatur_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikatur_VALUE]];int miżura=0,element_COUNT=서술자(서술값,&miżura);if(element_COUNT<0){잘못됨=1;return;}
    for(int 순번=element_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtwali_CALL)내보내기("Q();");
    if(!virtwali_CALL&&같음(propjetarju_oġġett,첫째값[현재클래스])){
        unsigned grupp_daqqas=0;for(;grupp_daqqas<메소드개수;grupp_daqqas++)if(같음(isem,메소드목록[grupp_daqqas].isem)&&같음(서술값,메소드목록[grupp_daqqas].서술값))break;
        if(grupp_daqqas==메소드개수||!(메소드목록[grupp_daqqas].설정비트&8)){잘못됨=1;return;}
        if(miżura)내보내기("P(");내보내기("m%u(",grupp_daqqas);for(int 순번=0;순번<element_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(miżura?"));":" );");return;
    }
    if((virtwali_CALL&&UNICODE_VALUE(propjetarju_oġġett,"java/io/PrintStream")&& (UNICODE_VALUE(isem,"print")||UNICODE_VALUE(isem,"println")))||(!virtwali_CALL&&UNICODE_VALUE(propjetarju_oġġett,"Malti/자체/출력"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(isem,"print")||UNICODE_VALUE(isem,"println")||UNICODE_VALUE(isem,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(isem,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(isem,"print")||UNICODE_VALUE(isem,"println")||UNICODE_VALUE(isem,"kiteb")||UNICODE_VALUE(isem,"kiteb_linja"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(isem,"print")||UNICODE_VALUE(isem,"kiteb")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(isem,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtwali_CALL&&UNICODE_VALUE(propjetarju_oġġett,"Malti/자체/fajl")){
        if(UNICODE_VALUE(isem,"kiteb")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(isem,"읽기")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void bena_metodu(unsigned LOOKUP_INDEX){
    metodu_entrata*grupp_daqqas=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(grupp_daqqas->isem,"<init>"))return;int miżura,element_COUNT=서술자(grupp_daqqas->서술값,&miżura);if(element_COUNT<0){잘못됨=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<element_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!element_COUNT)내보내기("void");
    if((unsigned)element_COUNT>grupp_daqqas->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",grupp_daqqas->지역변수들?grupp_daqqas->지역변수들:1);for(int 순번=0;순번<element_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=tul_VALUE;tul_VALUE=grupp_daqqas->istruzzjoni_SEQUENCE+grupp_daqqas->daqqas;현재위치=grupp_daqqas->istruzzjoni_SEQUENCE;
    while(현재위치<tul_VALUE&&!잘못됨){unsigned kmand_pożizzjoni=현재위치-grupp_daqqas->istruzzjoni_SEQUENCE,operazzjoni_VALUE=byte_data();내보내기("L%u:;",kmand_pożizzjoni);
        if(operazzjoni_VALUE==0){}
        else if(operazzjoni_VALUE==1)내보내기("P(0);");
        else if(operazzjoni_VALUE>=2&&operazzjoni_VALUE<=8)내보내기("P(%uU);",operazzjoni_VALUE-3);
        else if(operazzjoni_VALUE==16){int VALUE=(int8_t)byte_data();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operazzjoni_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operazzjoni_VALUE==18||operazzjoni_VALUE==19)valur_fiss_VALUE(operazzjoni_VALUE==18?byte_data():절반값());
        else if(operazzjoni_VALUE==21||operazzjoni_VALUE==25){unsigned 순번=byte_data();if(순번>=grupp_daqqas->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((operazzjoni_VALUE>=26&&operazzjoni_VALUE<=29)||(operazzjoni_VALUE>=42&&operazzjoni_VALUE<=45)){unsigned 순번=operazzjoni_VALUE>=42?operazzjoni_VALUE-42:operazzjoni_VALUE-26;if(순번>=grupp_daqqas->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(operazzjoni_VALUE==54||operazzjoni_VALUE==58){unsigned 순번=byte_data();if(순번>=grupp_daqqas->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((operazzjoni_VALUE>=59&&operazzjoni_VALUE<=62)||(operazzjoni_VALUE>=75&&operazzjoni_VALUE<=78)){unsigned 순번=operazzjoni_VALUE>=75?operazzjoni_VALUE-75:operazzjoni_VALUE-59;if(순번>=grupp_daqqas->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(operazzjoni_VALUE==46||operazzjoni_VALUE==50||operazzjoni_VALUE==51||operazzjoni_VALUE==52||operazzjoni_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operazzjoni_VALUE==79||operazzjoni_VALUE==83||operazzjoni_VALUE==84||operazzjoni_VALUE==85||operazzjoni_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operazzjoni_VALUE==84?"(unsigned)(signed char)q":operazzjoni_VALUE==85?"(unsigned short)q":operazzjoni_VALUE==86?"(unsigned)(short)q":"q");
        else if(operazzjoni_VALUE==87)내보내기("Q();");
        else if(operazzjoni_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(operazzjoni_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operazzjoni_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(operazzjoni_VALUE==96||operazzjoni_VALUE==100||operazzjoni_VALUE==104||operazzjoni_VALUE==120||operazzjoni_VALUE==124||operazzjoni_VALUE==126||operazzjoni_VALUE==128||operazzjoni_VALUE==130){const char*kodifikar_VALUE=operazzjoni_VALUE==96?"+":operazzjoni_VALUE==100?"-":operazzjoni_VALUE==104?"*":operazzjoni_VALUE==120?"<<":operazzjoni_VALUE==124?">>":operazzjoni_VALUE==126?"&":operazzjoni_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kodifikar_VALUE,operazzjoni_VALUE==120||operazzjoni_VALUE==124?"%32":"");}
        else if(operazzjoni_VALUE==108||operazzjoni_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operazzjoni_VALUE==112);
        else if(operazzjoni_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(operazzjoni_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operazzjoni_VALUE==132){unsigned 순번=byte_data();int 차이=(int8_t)byte_data();if(순번>=grupp_daqqas->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operazzjoni_VALUE>=145&&operazzjoni_VALUE<=147)내보내기("P((unsigned)(%s)Q());",operazzjoni_VALUE==145?"signed char":operazzjoni_VALUE==146?"unsigned short":"short");
        else if(operazzjoni_VALUE>=153&&operazzjoni_VALUE<=166){int mira=(int)kmand_pożizzjoni+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(mira<0||mira>=(int)grupp_daqqas->daqqas){잘못됨=1;break;}if(operazzjoni_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[operazzjoni_VALUE-153],mira);else if(operazzjoni_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[operazzjoni_VALUE-159],mira);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operazzjoni_VALUE==165?"==":"!=",mira);}
        else if(operazzjoni_VALUE==167){int mira=(int)kmand_pożizzjoni+(int16_t)절반값();if(mira<0||mira>=(int)grupp_daqqas->daqqas)잘못됨=1;내보내기("goto L%d;",mira);}
        else if(operazzjoni_VALUE==172||operazzjoni_VALUE==176)내보내기("return Q();");else if(operazzjoni_VALUE==177)내보내기("return 0;");
        else if(operazzjoni_VALUE==178||operazzjoni_VALUE==179){unsigned identifikatur_VALUE=절반값();if(identifikatur_VALUE<1||identifikatur_VALUE>=상수모음||Tags_Lista[identifikatur_VALUE]!=9||첫째값[identifikatur_VALUE]>=상수모음||SECOND_VALUE[identifikatur_VALUE]>=상수모음||Tags_Lista[첫째값[identifikatur_VALUE]]!=7||Tags_Lista[SECOND_VALUE[identifikatur_VALUE]]!=12){잘못됨=1;break;}unsigned propjetarju_oġġett=첫째값[첫째값[identifikatur_VALUE]],isem=첫째값[SECOND_VALUE[identifikatur_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikatur_VALUE]];
            if(operazzjoni_VALUE==178&&UNICODE_VALUE(propjetarju_oġġett,"java/lang/System")&&UNICODE_VALUE(isem,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned fajl_entrata=0;while(fajl_entrata<필드개수&&(!같음(isem,isem_il_qasam[fajl_entrata])||!같음(서술값,필드서술[fajl_entrata])))fajl_entrata++;if(!같음(propjetarju_oġġett,첫째값[현재클래스])||fajl_entrata==필드개수){잘못됨=1;break;}내보내기(operazzjoni_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",fajl_entrata);}}
        else if(operazzjoni_VALUE==182||operazzjoni_VALUE==184)호출(절반값(),operazzjoni_VALUE==182);
        else if(operazzjoni_VALUE==188){unsigned TYPE_kategorija=byte_data();if(TYPE_kategorija!=4&&TYPE_kategorija!=5&&TYPE_kategorija!=8&&TYPE_kategorija!=9&&TYPE_kategorija!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(operazzjoni_VALUE==190)내보내기("P(jlength(Q()));");
        else if(operazzjoni_VALUE==198||operazzjoni_VALUE==199){int mira=(int)kmand_pożizzjoni+(int16_t)절반값();if(mira<0||mira>=(int)grupp_daqqas->daqqas)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",operazzjoni_VALUE==198?"==":"!=",mira);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,operazzjoni_VALUE,kmand_pożizzjoni);
        내보내기("\n");
    }
    tul_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned string_lezzjoni(unsigned *data_pożizzjoni,unsigned ttermina_OFFSET){
    if(*data_pożizzjoni>=ttermina_OFFSET){잘못됨=1;return 0;}unsigned kodiċi_tal_karattru=data[(*data_pożizzjoni)++];
    if(kodiċi_tal_karattru<128)return kodiċi_tal_karattru;
    unsigned element_COUNT=kodiċi_tal_karattru>=0xc0&&kodiċi_tal_karattru<=0xdf?1:kodiċi_tal_karattru>=0xe0&&kodiċi_tal_karattru<=0xef?2:3;
    if(element_COUNT==3||element_COUNT>ttermina_OFFSET-*data_pożizzjoni){잘못됨=1;return 0;}unsigned VALUE=kodiċi_tal_karattru&((1u<<(6-element_COUNT))-1);
    for(unsigned 순번=0;순번<element_COUNT;순번++){unsigned Li_Jmiss_element=data[(*data_pożizzjoni)++];if((Li_Jmiss_element&0xc0)!=0x80)잘못됨=1;VALUE=VALUE<<6|(Li_Jmiss_element&63);}
    if((element_COUNT==1&&VALUE<128&&VALUE!=0)||(element_COUNT==2&&VALUE<2048))잘못됨=1;return VALUE;
}
static void string_valur_fiss(unsigned identifikatur_VALUE){
    unsigned 부호없는값=첫째값[identifikatur_VALUE];if(부호없는값<1||부호없는값>=상수모음||Tags_Lista[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",identifikatur_VALUE);
    unsigned data_pożizzjoni=첫째값[부호없는값],ttermina_OFFSET=data_pożizzjoni+SECOND_VALUE[부호없는값];
    while(data_pożizzjoni<ttermina_OFFSET&&!잘못됨){unsigned kodiċi_tal_karattru=string_lezzjoni(&data_pożizzjoni,ttermina_OFFSET);
        if(kodiċi_tal_karattru>=0xd800&&kodiċi_tal_karattru<=0xdbff){unsigned 낮은부분=string_lezzjoni(&data_pożizzjoni,ttermina_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}kodiċi_tal_karattru=0x10000+((kodiċi_tal_karattru-0xd800)<<10)+낮은부분-0xdc00;}
        else if(kodiċi_tal_karattru>=0xdc00&&kodiċi_tal_karattru<=0xdfff){잘못됨=1;break;}
        if(!kodiċi_tal_karattru){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(kodiċi_tal_karattru<128)내보내기("%u,",kodiċi_tal_karattru);
        else{unsigned element_COUNT=kodiċi_tal_karattru<2048?2:kodiċi_tal_karattru<65536?3:4;내보내기("%u,",(element_COUNT==2?0xc0:element_COUNT==3?0xe0:0xf0)|(kodiċi_tal_karattru>>(6*(element_COUNT-1))));for(unsigned 순번=element_COUNT-1;순번;순번--)내보내기("%u,",0x80|((kodiċi_tal_karattru>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*isem){
    size_t element_COUNT=strlen(isem);
    if(element_COUNT>4&&!strcmp(isem+element_COUNT-4,".jar")){
        if(꾸러미열기(isem)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char mogħdija[256];const char*entrata_metodu=꾸러미진입클래스();element_COUNT=strlen(entrata_metodu);if(element_COUNT+6>=sizeof(mogħdija))return 0;
        for(unsigned 순번=0;순번<element_COUNT;순번++)mogħdija[순번]=entrata_metodu[순번]=='.'?'/':entrata_metodu[순번];strcpy(mogħdija+element_COUNT,".class");int entrata_COUNT=꾸러미읽기(mogħdija,data,sizeof(data));if(entrata_COUNT<0)return 0;tul_VALUE=entrata_COUNT;
    }else{intptr_t fajl_handle=사용자호출(3,(uintptr_t)isem,0,0,0,0,0);if(fajl_handle<0)return 0;intptr_t entrata_COUNT=사용자호출(9,fajl_handle,0,0,0,0,0);if(entrata_COUNT<0||entrata_COUNT>sizeof(data)){사용자호출(4,fajl_handle,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,fajl_handle,(uintptr_t)data,entrata_COUNT,0,0,0);사용자호출(4,fajl_handle,0,0,0,0,0);if(RECEIVED_COUNT!=entrata_COUNT)return 0;tul_VALUE=entrata_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(Tags_Lista[순번]==8)string_valur_fiss(순번);
    if(잘못됨)return 0;
    int entrata_punt=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].isem,"<init>")){
        int miżura,entrata_COUNT=서술자(메소드목록[순번].서술값,&miżura);if(entrata_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<entrata_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!entrata_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].isem,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)entrata_punt=순번;
        if(UNICODE_VALUE(메소드목록[순번].isem,"<clinit>"))초기값=순번;
    }
    if(entrata_punt<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)bena_metodu(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(qasam_valur_fiss[순번]){
        unsigned kodiċi_tal_karattru=qasam_valur_fiss[순번];if(kodiċi_tal_karattru>=상수모음)return 0;
        if(Tags_Lista[kodiċi_tal_karattru]==3)내보내기("fields[%u]=%uU;",순번,첫째값[kodiċi_tal_karattru]);else if(Tags_Lista[kodiċi_tal_karattru]==8)내보내기("fields[%u]=(W)k%u;",순번,kodiċi_tal_karattru);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",entrata_punt);
    return 잘못됨?0:SMS;
}
