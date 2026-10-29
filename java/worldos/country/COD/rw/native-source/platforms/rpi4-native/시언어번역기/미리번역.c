#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "ipaki.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char amakurushingiro[16384];static unsigned uburebure_agaciro,현재위치;static int 잘못됨;
static unsigned Ibyiciro_Urutonde[512],첫째값[512],둘째값[512],상수모음,현재클래스;
static char Umwandiko[65536];static unsigned ingano_y_umwandiko;
typedef struct {unsigned 설정비트,Izina,서술값,ibwiriza_URUKURIKIRANE,Ingano,지역변수들,Ikirundo_Ububiko;} uburyo_icyinjizwa;
static uburyo_icyinjizwa 메소드목록[64];static unsigned 메소드개수;
static unsigned umwanya_izina_98daa19b[64],필드서술[64],umwanya_kidahinduka[64],필드개수;
static unsigned 가져오기(unsigned 개수){if(현재위치>uburebure_agaciro||개수>uburebure_agaciro-현재위치){잘못됨=1;return 0;}unsigned 자료위치=현재위치;현재위치+=개수;return 자료위치;}
static unsigned bayiti_amakurushingiro(void){unsigned 자료위치=가져오기(1);return 잘못됨?0:amakurushingiro[자료위치];}
static unsigned 절반값(void){unsigned Ihuza_rya_x=bayiti_amakurushingiro();return Ihuza_rya_x<<8|bayiti_amakurushingiro();}
static uint32_t 가득참(void){uint32_t Ihuza_rya_x=절반값();return Ihuza_rya_x<<16|절반값();}
static int inikode_agaciro(unsigned 순번,const char*igicenteruro_amakurushingiro){return 순번>0&&순번<상수모음&&Ibyiciro_Urutonde[순번]==1&&strlen(igicenteruro_amakurushingiro)==둘째값[순번]&&!memcmp(amakurushingiro+첫째값[순번],igicenteruro_amakurushingiro,둘째값[순번]);}
static int 같음(unsigned Ihuza_rya_x,unsigned 세로좌표){return Ihuza_rya_x>0&&Ihuza_rya_x<상수모음&&세로좌표>0&&세로좌표<상수모음&&Ibyiciro_Urutonde[Ihuza_rya_x]==1&&Ibyiciro_Urutonde[세로좌표]==1&&둘째값[Ihuza_rya_x]==둘째값[세로좌표]&&!memcmp(amakurushingiro+첫째값[Ihuza_rya_x],amakurushingiro+첫째값[세로좌표],둘째값[Ihuza_rya_x]);}
static void 내보내기(const char*dosiye_icyinjizwa,...){if(잘못됨)return;va_list ingingo_ARRAY;va_start(ingingo_ARRAY,dosiye_icyinjizwa);int 개수=vsnprintf(Umwandiko+ingano_y_umwandiko,sizeof(Umwandiko)-ingano_y_umwandiko,dosiye_icyinjizwa,ingingo_ARRAY);va_end(ingingo_ARRAY);if(개수<0||(unsigned)개수>=sizeof(Umwandiko)-ingano_y_umwandiko){잘못됨=1;return;}ingano_y_umwandiko+=개수;}
static int 서술자(unsigned indanga_agaciro,int*결과){
    if(indanga_agaciro<1||indanga_agaciro>=상수모음||Ibyiciro_Urutonde[indanga_agaciro]!=1)return -1;unsigned 자료위치=첫째값[indanga_agaciro],kurangiza_Ofuseti=자료위치+둘째값[indanga_agaciro];if(자료위치>=kurangiza_Ofuseti||amakurushingiro[자료위치++]!='(')return -1;int 항목수=0;
    while(자료위치<kurangiza_Ofuseti&&amakurushingiro[자료위치]!=')'){
        unsigned 문자값=amakurushingiro[자료위치++];while(문자값=='['&&자료위치<kurangiza_Ofuseti)문자값=amakurushingiro[자료위치++];
        if(문자값=='L'){while(자료위치<kurangiza_Ofuseti&&amakurushingiro[자료위치]!=';')자료위치++;if(자료위치==kurangiza_Ofuseti)return -1;자료위치++;}
        else if(문자값!='I'&&문자값!='Z'&&문자값!='B'&&문자값!='C'&&문자값!='S')return -1;
        if(++항목수>16)return -1;
    }
    if(자료위치+1>=kurangiza_Ofuseti||amakurushingiro[자료위치++]!=')')return -1;*결과=amakurushingiro[자료위치]=='V'?0:1;
    if(amakurushingiro[자료위치]=='J'||amakurushingiro[자료위치]=='D'||amakurushingiro[자료위치]=='F')return -1;return 항목수;
}
static void 속성들(void){unsigned 개수=절반값();for(unsigned 순번=0;순번<개수&&!잘못됨;순번++){절반값();unsigned Ingano=가득참();가져오기(Ingano);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned umwana_verisiyo=절반값(),판번호=절반값();if(umwana_verisiyo||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        Ibyiciro_Urutonde[순번]=bayiti_amakurushingiro();switch(Ibyiciro_Urutonde[순번]){
        case 1:둘째값[순번]=절반값();첫째값[순번]=가져오기(둘째값[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:가져오기(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();둘째값[순번]=절반값();break;
        case 15:첫째값[순번]=bayiti_amakurushingiro();둘째값[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Ibyiciro_Urutonde[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Ibyiciro_Urutonde[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();가져오기(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();umwanya_izina_98daa19b[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned 항목수=절반값();for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Izina=절반값(),Ingano=가득참();
            if(inikode_agaciro(Izina,"ConstantValue")){if(Ingano!=2)return -1;umwanya_kidahinduka[순번]=절반값();}
            else 가져오기(Ingano);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        uburyo_icyinjizwa*itsinda_ingano=메소드목록+순번;itsinda_ingano->설정비트=절반값();itsinda_ingano->Izina=절반값();itsinda_ingano->서술값=절반값();unsigned 항목수=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Izina=절반값(),Ingano=가득참(),ihuriro=현재위치;
            if(Ingano>uburebure_agaciro-현재위치)return -1;
            if(inikode_agaciro(Izina,"Code")){
                itsinda_ingano->Ikirundo_Ububiko=절반값();itsinda_ingano->지역변수들=절반값();itsinda_ingano->Ingano=가득참();itsinda_ingano->ibwiriza_URUKURIKIRANE=가져오기(itsinda_ingano->Ingano);
                if(itsinda_ingano->Ikirundo_Ububiko>128||itsinda_ingano->지역변수들>128||itsinda_ingano->Ingano>8192||절반값())return -1;속성들();
            }else 가져오기(Ingano);
            if(현재위치!=ihuriro+Ingano)return -1;
        }
        if(!inikode_agaciro(itsinda_ingano->Izina,"<init>")&&(!(itsinda_ingano->설정비트&8)||(itsinda_ingano->설정비트&(0x100|0x20))||!itsinda_ingano->Ingano))return -1;
    }
    속성들();return 잘못됨||현재위치!=uburebure_agaciro?-1:0;
}
static void kidahinduka_agaciro(unsigned indanga_agaciro){
    if(!indanga_agaciro||indanga_agaciro>=상수모음){잘못됨=1;return;}
    if(Ibyiciro_Urutonde[indanga_agaciro]==3)내보내기("P(%uU);",첫째값[indanga_agaciro]);
    else if(Ibyiciro_Urutonde[indanga_agaciro]==8)내보내기("P((W)k%u);",indanga_agaciro);else 잘못됨=1;
}
static void 호출(unsigned indanga_agaciro,int kidafatika_Hamagara){
    if(indanga_agaciro<1||indanga_agaciro>=상수모음||(Ibyiciro_Urutonde[indanga_agaciro]!=10&&Ibyiciro_Urutonde[indanga_agaciro]!=11)||첫째값[indanga_agaciro]<1||첫째값[indanga_agaciro]>=상수모음||Ibyiciro_Urutonde[첫째값[indanga_agaciro]]!=7||둘째값[indanga_agaciro]<1||둘째값[indanga_agaciro]>=상수모음||Ibyiciro_Urutonde[둘째값[indanga_agaciro]]!=12){잘못됨=1;return;}
    unsigned nyirayo_ikintu=첫째값[첫째값[indanga_agaciro]],Izina=첫째값[둘째값[indanga_agaciro]],서술값=둘째값[둘째값[indanga_agaciro]];int 결과=0,개수=서술자(서술값,&결과);if(개수<0){잘못됨=1;return;}
    for(int 순번=개수;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(kidafatika_Hamagara)내보내기("Q();");
    if(!kidafatika_Hamagara&&같음(nyirayo_ikintu,첫째값[현재클래스])){
        unsigned itsinda_ingano=0;for(;itsinda_ingano<메소드개수;itsinda_ingano++)if(같음(Izina,메소드목록[itsinda_ingano].Izina)&&같음(서술값,메소드목록[itsinda_ingano].서술값))break;
        if(itsinda_ingano==메소드개수||!(메소드목록[itsinda_ingano].설정비트&8)){잘못됨=1;return;}
        if(결과)내보내기("P(");내보내기("m%u(",itsinda_ingano);for(int 순번=0;순번<개수;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(결과?"));":" );");return;
    }
    if((kidafatika_Hamagara&&inikode_agaciro(nyirayo_ikintu,"java/io/PrintStream")&& (inikode_agaciro(Izina,"print")||inikode_agaciro(Izina,"println")))||(!kidafatika_Hamagara&&inikode_agaciro(nyirayo_ikintu,"Ikinyarwanda/자체/출력"))){
        if(inikode_agaciro(서술값,"(I)V")&&(inikode_agaciro(Izina,"print")||inikode_agaciro(Izina,"println")||inikode_agaciro(Izina,"수쓰기"))){내보내기("jprint(x[0],1,%d);",inikode_agaciro(Izina,"print")?0:1);return;}
        if(inikode_agaciro(서술값,"(Ljava/lang/String;)V")&&(inikode_agaciro(Izina,"print")||inikode_agaciro(Izina,"println")||inikode_agaciro(Izina,"kwandika")||inikode_agaciro(Izina,"kwandika_umurongo"))){내보내기("jprint(x[0],0,%d);",inikode_agaciro(Izina,"print")||inikode_agaciro(Izina,"kwandika")?0:1);return;}
        if(inikode_agaciro(서술값,"()V")&&inikode_agaciro(Izina,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!kidafatika_Hamagara&&inikode_agaciro(nyirayo_ikintu,"Ikinyarwanda/자체/Idosiye")){
        if(inikode_agaciro(Izina,"kwandika")&&inikode_agaciro(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(inikode_agaciro(Izina,"읽기")&&inikode_agaciro(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void gusohora_uburyo(unsigned 색인){
    uburyo_icyinjizwa*itsinda_ingano=메소드목록+색인;if(inikode_agaciro(itsinda_ingano->Izina,"<init>"))return;int 결과,개수=서술자(itsinda_ingano->서술값,&결과);if(개수<0){잘못됨=1;return;}
    내보내기("static W m%u(",색인);for(int 순번=0;순번<개수;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!개수)내보내기("void");
    if((unsigned)개수>itsinda_ingano->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",itsinda_ingano->지역변수들?itsinda_ingano->지역변수들:1);for(int 순번=0;순번<개수;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=uburebure_agaciro;uburebure_agaciro=itsinda_ingano->ibwiriza_URUKURIKIRANE+itsinda_ingano->Ingano;현재위치=itsinda_ingano->ibwiriza_URUKURIKIRANE;
    while(현재위치<uburebure_agaciro&&!잘못됨){unsigned 명령위치=현재위치-itsinda_ingano->ibwiriza_URUKURIKIRANE,igikorwa_agaciro=bayiti_amakurushingiro();내보내기("L%u:;",명령위치);
        if(igikorwa_agaciro==0){}
        else if(igikorwa_agaciro==1)내보내기("P(0);");
        else if(igikorwa_agaciro>=2&&igikorwa_agaciro<=8)내보내기("P(%uU);",igikorwa_agaciro-3);
        else if(igikorwa_agaciro==16){int agaciro=(int8_t)bayiti_amakurushingiro();내보내기("P(%uU);",(unsigned)agaciro);}
        else if(igikorwa_agaciro==17){int agaciro=(int16_t)절반값();내보내기("P(%uU);",(unsigned)agaciro);}
        else if(igikorwa_agaciro==18||igikorwa_agaciro==19)kidahinduka_agaciro(igikorwa_agaciro==18?bayiti_amakurushingiro():절반값());
        else if(igikorwa_agaciro==21||igikorwa_agaciro==25){unsigned 순번=bayiti_amakurushingiro();if(순번>=itsinda_ingano->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((igikorwa_agaciro>=26&&igikorwa_agaciro<=29)||(igikorwa_agaciro>=42&&igikorwa_agaciro<=45)){unsigned 순번=igikorwa_agaciro>=42?igikorwa_agaciro-42:igikorwa_agaciro-26;if(순번>=itsinda_ingano->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(igikorwa_agaciro==54||igikorwa_agaciro==58){unsigned 순번=bayiti_amakurushingiro();if(순번>=itsinda_ingano->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((igikorwa_agaciro>=59&&igikorwa_agaciro<=62)||(igikorwa_agaciro>=75&&igikorwa_agaciro<=78)){unsigned 순번=igikorwa_agaciro>=75?igikorwa_agaciro-75:igikorwa_agaciro-59;if(순번>=itsinda_ingano->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(igikorwa_agaciro==46||igikorwa_agaciro==50||igikorwa_agaciro==51||igikorwa_agaciro==52||igikorwa_agaciro==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(igikorwa_agaciro==79||igikorwa_agaciro==83||igikorwa_agaciro==84||igikorwa_agaciro==85||igikorwa_agaciro==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",igikorwa_agaciro==84?"(unsigned)(signed char)q":igikorwa_agaciro==85?"(unsigned short)q":igikorwa_agaciro==86?"(unsigned)(short)q":"q");
        else if(igikorwa_agaciro==87)내보내기("Q();");
        else if(igikorwa_agaciro==89)내보내기("q=Q();P(q);P(q);");
        else if(igikorwa_agaciro==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(igikorwa_agaciro==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(igikorwa_agaciro==96||igikorwa_agaciro==100||igikorwa_agaciro==104||igikorwa_agaciro==120||igikorwa_agaciro==124||igikorwa_agaciro==126||igikorwa_agaciro==128||igikorwa_agaciro==130){const char*gusobeka_agaciro=igikorwa_agaciro==96?"+":igikorwa_agaciro==100?"-":igikorwa_agaciro==104?"*":igikorwa_agaciro==120?"<<":igikorwa_agaciro==124?">>":igikorwa_agaciro==126?"&":igikorwa_agaciro==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",gusobeka_agaciro,igikorwa_agaciro==120||igikorwa_agaciro==124?"%32":"");}
        else if(igikorwa_agaciro==108||igikorwa_agaciro==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",igikorwa_agaciro==112);
        else if(igikorwa_agaciro==116)내보내기("P(0U-(unsigned)Q());");
        else if(igikorwa_agaciro==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(igikorwa_agaciro==132){unsigned 순번=bayiti_amakurushingiro();int 차이=(int8_t)bayiti_amakurushingiro();if(순번>=itsinda_ingano->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(igikorwa_agaciro>=145&&igikorwa_agaciro<=147)내보내기("P((unsigned)(%s)Q());",igikorwa_agaciro==145?"signed char":igikorwa_agaciro==146?"unsigned short":"short");
        else if(igikorwa_agaciro>=153&&igikorwa_agaciro<=166){int gusimbuza_igishya=(int)명령위치+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(gusimbuza_igishya<0||gusimbuza_igishya>=(int)itsinda_ingano->Ingano){잘못됨=1;break;}if(igikorwa_agaciro<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[igikorwa_agaciro-153],gusimbuza_igishya);else if(igikorwa_agaciro<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[igikorwa_agaciro-159],gusimbuza_igishya);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",igikorwa_agaciro==165?"==":"!=",gusimbuza_igishya);}
        else if(igikorwa_agaciro==167){int gusimbuza_igishya=(int)명령위치+(int16_t)절반값();if(gusimbuza_igishya<0||gusimbuza_igishya>=(int)itsinda_ingano->Ingano)잘못됨=1;내보내기("goto L%d;",gusimbuza_igishya);}
        else if(igikorwa_agaciro==172||igikorwa_agaciro==176)내보내기("return Q();");else if(igikorwa_agaciro==177)내보내기("return 0;");
        else if(igikorwa_agaciro==178||igikorwa_agaciro==179){unsigned indanga_agaciro=절반값();if(indanga_agaciro<1||indanga_agaciro>=상수모음||Ibyiciro_Urutonde[indanga_agaciro]!=9||첫째값[indanga_agaciro]>=상수모음||둘째값[indanga_agaciro]>=상수모음||Ibyiciro_Urutonde[첫째값[indanga_agaciro]]!=7||Ibyiciro_Urutonde[둘째값[indanga_agaciro]]!=12){잘못됨=1;break;}unsigned nyirayo_ikintu=첫째값[첫째값[indanga_agaciro]],Izina=첫째값[둘째값[indanga_agaciro]],서술값=둘째값[둘째값[indanga_agaciro]];
            if(igikorwa_agaciro==178&&inikode_agaciro(nyirayo_ikintu,"java/lang/System")&&inikode_agaciro(Izina,"out")&&inikode_agaciro(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned dosiye_icyinjizwa=0;while(dosiye_icyinjizwa<필드개수&&(!같음(Izina,umwanya_izina_98daa19b[dosiye_icyinjizwa])||!같음(서술값,필드서술[dosiye_icyinjizwa])))dosiye_icyinjizwa++;if(!같음(nyirayo_ikintu,첫째값[현재클래스])||dosiye_icyinjizwa==필드개수){잘못됨=1;break;}내보내기(igikorwa_agaciro==178?"P(fields[%u]);":"fields[%u]=Q();",dosiye_icyinjizwa);}}
        else if(igikorwa_agaciro==182||igikorwa_agaciro==184)호출(절반값(),igikorwa_agaciro==182);
        else if(igikorwa_agaciro==188){unsigned 유형=bayiti_amakurushingiro();if(유형!=4&&유형!=5&&유형!=8&&유형!=9&&유형!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(igikorwa_agaciro==190)내보내기("P(jlength(Q()));");
        else if(igikorwa_agaciro==198||igikorwa_agaciro==199){int gusimbuza_igishya=(int)명령위치+(int16_t)절반값();if(gusimbuza_igishya<0||gusimbuza_igishya>=(int)itsinda_ingano->Ingano)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",igikorwa_agaciro==198?"==":"!=",gusimbuza_igishya);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",색인,igikorwa_agaciro,명령위치);
        내보내기("\n");
    }
    uburebure_agaciro=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned igicenteruro_ibinyabumwe(unsigned *자료위치,unsigned kurangiza_Ofuseti){
    if(*자료위치>=kurangiza_Ofuseti){잘못됨=1;return 0;}unsigned 문자값=amakurushingiro[(*자료위치)++];
    if(문자값<128)return 문자값;
    unsigned 개수=문자값>=0xc0&&문자값<=0xdf?1:문자값>=0xe0&&문자값<=0xef?2:3;
    if(개수==3||개수>kurangiza_Ofuseti-*자료위치){잘못됨=1;return 0;}unsigned agaciro=문자값&((1u<<(6-개수))-1);
    for(unsigned 순번=0;순번<개수;순번++){unsigned 다음=amakurushingiro[(*자료위치)++];if((다음&0xc0)!=0x80)잘못됨=1;agaciro=agaciro<<6|(다음&63);}
    if((개수==1&&agaciro<128&&agaciro!=0)||(개수==2&&agaciro<2048))잘못됨=1;return agaciro;
}
static void igicenteruro_kidahinduka(unsigned indanga_agaciro){
    unsigned 부호없는값=첫째값[indanga_agaciro];if(부호없는값<1||부호없는값>=상수모음||Ibyiciro_Urutonde[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",indanga_agaciro);
    unsigned 자료위치=첫째값[부호없는값],kurangiza_Ofuseti=자료위치+둘째값[부호없는값];
    while(자료위치<kurangiza_Ofuseti&&!잘못됨){unsigned 문자값=igicenteruro_ibinyabumwe(&자료위치,kurangiza_Ofuseti);
        if(문자값>=0xd800&&문자값<=0xdbff){unsigned 낮은부분=igicenteruro_ibinyabumwe(&자료위치,kurangiza_Ofuseti);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}문자값=0x10000+((문자값-0xd800)<<10)+낮은부분-0xdc00;}
        else if(문자값>=0xdc00&&문자값<=0xdfff){잘못됨=1;break;}
        if(!문자값){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(문자값<128)내보내기("%u,",문자값);
        else{unsigned 개수=문자값<2048?2:문자값<65536?3:4;내보내기("%u,",(개수==2?0xc0:개수==3?0xe0:0xf0)|(문자값>>(6*(개수-1))));for(unsigned 순번=개수-1;순번;순번--)내보내기("%u,",0x80|((문자값>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Izina){
    size_t 개수=strlen(Izina);
    if(개수>4&&!strcmp(Izina+개수-4,".jar")){
        if(꾸러미열기(Izina)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Inzira[256];const char*icyinjizwa_uburyo=꾸러미진입클래스();개수=strlen(icyinjizwa_uburyo);if(개수+6>=sizeof(Inzira))return 0;
        for(unsigned 순번=0;순번<개수;순번++)Inzira[순번]=icyinjizwa_uburyo[순번]=='.'?'/':icyinjizwa_uburyo[순번];strcpy(Inzira+개수,".class");int 항목수=꾸러미읽기(Inzira,amakurushingiro,sizeof(amakurushingiro));if(항목수<0)return 0;uburebure_agaciro=항목수;
    }else{intptr_t dosiye_umukondo=사용자호출(3,(uintptr_t)Izina,0,0,0,0,0);if(dosiye_umukondo<0)return 0;intptr_t 항목수=사용자호출(9,dosiye_umukondo,0,0,0,0,0);if(항목수<0||항목수>sizeof(amakurushingiro)){사용자호출(4,dosiye_umukondo,0,0,0,0,0);return 0;}intptr_t 받은수=사용자호출(2,dosiye_umukondo,(uintptr_t)amakurushingiro,항목수,0,0,0);사용자호출(4,dosiye_umukondo,0,0,0,0,0);if(받은수!=항목수)return 0;uburebure_agaciro=항목수;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(Ibyiciro_Urutonde[순번]==8)igicenteruro_kidahinduka(순번);
    if(잘못됨)return 0;
    int icyinjizwa_inota=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!inikode_agaciro(메소드목록[순번].Izina,"<init>")){
        int 결과,항목수=서술자(메소드목록[순번].서술값,&결과);if(항목수<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<항목수;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!항목수)내보내기("void");내보내기(");\n");
        if(inikode_agaciro(메소드목록[순번].Izina,"main")&&inikode_agaciro(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)icyinjizwa_inota=순번;
        if(inikode_agaciro(메소드목록[순번].Izina,"<clinit>"))초기값=순번;
    }
    if(icyinjizwa_inota<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)gusohora_uburyo(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(umwanya_kidahinduka[순번]){
        unsigned 문자값=umwanya_kidahinduka[순번];if(문자값>=상수모음)return 0;
        if(Ibyiciro_Urutonde[문자값]==3)내보내기("fields[%u]=%uU;",순번,첫째값[문자값]);else if(Ibyiciro_Urutonde[문자값]==8)내보내기("fields[%u]=(W)k%u;",순번,문자값);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",icyinjizwa_inota);
    return 잘못됨?0:Umwandiko;
}
