#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "toplum.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char maglumat[16384];static unsigned dowamlylyk_baha,현재위치;static int 잘못됨;
static unsigned Taglar_Sanaw[512],첫째값[512],둘째값[512],상수모음,현재클래스;
static char Metin[65536];static unsigned tekst_ölçegi;
typedef struct {unsigned 설정비트,Ad,서술값,instruksiýa_SEQUENCE,Ululyk,지역변수들,Desse_Ammar;} usul_girizmeklik;
static usul_girizmeklik 메소드목록[64];static unsigned 메소드개수;
static unsigned meýdanyň_ady[64],필드서술[64],meýdan_hemişelik[64],필드개수;
static unsigned 가져오기(unsigned 개수){if(현재위치>dowamlylyk_baha||개수>dowamlylyk_baha-현재위치){잘못됨=1;return 0;}unsigned 자료위치=현재위치;현재위치+=개수;return 자료위치;}
static unsigned baýt_maglumat(void){unsigned 자료위치=가져오기(1);return 잘못됨?0:maglumat[자료위치];}
static unsigned 절반값(void){unsigned x_koordinatasy=baýt_maglumat();return x_koordinatasy<<8|baýt_maglumat();}
static uint32_t 가득참(void){uint32_t x_koordinatasy=절반값();return x_koordinatasy<<16|절반값();}
static int Ýunikod_baha(unsigned 순번,const char*setir_maglumat){return 순번>0&&순번<상수모음&&Taglar_Sanaw[순번]==1&&strlen(setir_maglumat)==둘째값[순번]&&!memcmp(maglumat+첫째값[순번],setir_maglumat,둘째값[순번]);}
static int 같음(unsigned x_koordinatasy,unsigned 세로좌표){return x_koordinatasy>0&&x_koordinatasy<상수모음&&세로좌표>0&&세로좌표<상수모음&&Taglar_Sanaw[x_koordinatasy]==1&&Taglar_Sanaw[세로좌표]==1&&둘째값[x_koordinatasy]==둘째값[세로좌표]&&!memcmp(maglumat+첫째값[x_koordinatasy],maglumat+첫째값[세로좌표],둘째값[x_koordinatasy]);}
static void 내보내기(const char*faýl_girizmeklik,...){if(잘못됨)return;va_list argument_ARRAY;va_start(argument_ARRAY,faýl_girizmeklik);int 개수=vsnprintf(Metin+tekst_ölçegi,sizeof(Metin)-tekst_ölçegi,faýl_girizmeklik,argument_ARRAY);va_end(argument_ARRAY);if(개수<0||(unsigned)개수>=sizeof(Metin)-tekst_ölçegi){잘못됨=1;return;}tekst_ölçegi+=개수;}
static int 서술자(unsigned tanaýjy_baha,int*결과){
    if(tanaýjy_baha<1||tanaýjy_baha>=상수모음||Taglar_Sanaw[tanaýjy_baha]!=1)return -1;unsigned 자료위치=첫째값[tanaýjy_baha],tamamla_Süýşüriş=자료위치+둘째값[tanaýjy_baha];if(자료위치>=tamamla_Süýşüriş||maglumat[자료위치++]!='(')return -1;int 항목수=0;
    while(자료위치<tamamla_Süýşüriş&&maglumat[자료위치]!=')'){
        unsigned nyşanyň_kody=maglumat[자료위치++];while(nyşanyň_kody=='['&&자료위치<tamamla_Süýşüriş)nyşanyň_kody=maglumat[자료위치++];
        if(nyşanyň_kody=='L'){while(자료위치<tamamla_Süýşüriş&&maglumat[자료위치]!=';')자료위치++;if(자료위치==tamamla_Süýşüriş)return -1;자료위치++;}
        else if(nyşanyň_kody!='I'&&nyşanyň_kody!='Z'&&nyşanyň_kody!='B'&&nyşanyň_kody!='C'&&nyşanyň_kody!='S')return -1;
        if(++항목수>16)return -1;
    }
    if(자료위치+1>=tamamla_Süýşüriş||maglumat[자료위치++]!=')')return -1;*결과=maglumat[자료위치]=='V'?0:1;
    if(maglumat[자료위치]=='J'||maglumat[자료위치]=='D'||maglumat[자료위치]=='F')return -1;return 항목수;
}
static void 속성들(void){unsigned 개수=절반값();for(unsigned 순번=0;순번<개수&&!잘못됨;순번++){절반값();unsigned Ululyk=가득참();가져오기(Ululyk);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned kämillik_ýaşyna_ýetmedik_wersiýa=절반값(),판번호=절반값();if(kämillik_ýaşyna_ýetmedik_wersiýa||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        Taglar_Sanaw[순번]=baýt_maglumat();switch(Taglar_Sanaw[순번]){
        case 1:둘째값[순번]=절반값();첫째값[순번]=가져오기(둘째값[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:가져오기(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();둘째값[순번]=절반값();break;
        case 15:첫째값[순번]=baýt_maglumat();둘째값[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Taglar_Sanaw[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Taglar_Sanaw[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();가져오기(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();meýdanyň_ady[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned 항목수=절반값();for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Ad=절반값(),Ululyk=가득참();
            if(Ýunikod_baha(Ad,"ConstantValue")){if(Ululyk!=2)return -1;meýdan_hemişelik[순번]=절반값();}
            else 가져오기(Ululyk);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        usul_girizmeklik*topar_ölçegi_üýtget=메소드목록+순번;topar_ölçegi_üýtget->설정비트=절반값();topar_ölçegi_üýtget->Ad=절반값();topar_ölçegi_üýtget->서술값=절반값();unsigned 항목수=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Ad=절반값(),Ululyk=가득참(),Bitir=현재위치;
            if(Ululyk>dowamlylyk_baha-현재위치)return -1;
            if(Ýunikod_baha(Ad,"Code")){
                topar_ölçegi_üýtget->Desse_Ammar=절반값();topar_ölçegi_üýtget->지역변수들=절반값();topar_ölçegi_üýtget->Ululyk=가득참();topar_ölçegi_üýtget->instruksiýa_SEQUENCE=가져오기(topar_ölçegi_üýtget->Ululyk);
                if(topar_ölçegi_üýtget->Desse_Ammar>128||topar_ölçegi_üýtget->지역변수들>128||topar_ölçegi_üýtget->Ululyk>8192||절반값())return -1;속성들();
            }else 가져오기(Ululyk);
            if(현재위치!=Bitir+Ululyk)return -1;
        }
        if(!Ýunikod_baha(topar_ölçegi_üýtget->Ad,"<init>")&&(!(topar_ölçegi_üýtget->설정비트&8)||(topar_ölçegi_üýtget->설정비트&(0x100|0x20))||!topar_ölçegi_üýtget->Ululyk))return -1;
    }
    속성들();return 잘못됨||현재위치!=dowamlylyk_baha?-1:0;
}
static void hemişelik_baha(unsigned tanaýjy_baha){
    if(!tanaýjy_baha||tanaýjy_baha>=상수모음){잘못됨=1;return;}
    if(Taglar_Sanaw[tanaýjy_baha]==3)내보내기("P(%uU);",첫째값[tanaýjy_baha]);
    else if(Taglar_Sanaw[tanaýjy_baha]==8)내보내기("P((W)k%u);",tanaýjy_baha);else 잘못됨=1;
}
static void 호출(unsigned tanaýjy_baha,int hyýaly_Jaň){
    if(tanaýjy_baha<1||tanaýjy_baha>=상수모음||(Taglar_Sanaw[tanaýjy_baha]!=10&&Taglar_Sanaw[tanaýjy_baha]!=11)||첫째값[tanaýjy_baha]<1||첫째값[tanaýjy_baha]>=상수모음||Taglar_Sanaw[첫째값[tanaýjy_baha]]!=7||둘째값[tanaýjy_baha]<1||둘째값[tanaýjy_baha]>=상수모음||Taglar_Sanaw[둘째값[tanaýjy_baha]]!=12){잘못됨=1;return;}
    unsigned eýe_obýekt=첫째값[첫째값[tanaýjy_baha]],Ad=첫째값[둘째값[tanaýjy_baha]],서술값=둘째값[둘째값[tanaýjy_baha]];int 결과=0,개수=서술자(서술값,&결과);if(개수<0){잘못됨=1;return;}
    for(int 순번=개수;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(hyýaly_Jaň)내보내기("Q();");
    if(!hyýaly_Jaň&&같음(eýe_obýekt,첫째값[현재클래스])){
        unsigned topar_ölçegi_üýtget=0;for(;topar_ölçegi_üýtget<메소드개수;topar_ölçegi_üýtget++)if(같음(Ad,메소드목록[topar_ölçegi_üýtget].Ad)&&같음(서술값,메소드목록[topar_ölçegi_üýtget].서술값))break;
        if(topar_ölçegi_üýtget==메소드개수||!(메소드목록[topar_ölçegi_üýtget].설정비트&8)){잘못됨=1;return;}
        if(결과)내보내기("P(");내보내기("m%u(",topar_ölçegi_üýtget);for(int 순번=0;순번<개수;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(결과?"));":" );");return;
    }
    if((hyýaly_Jaň&&Ýunikod_baha(eýe_obýekt,"java/io/PrintStream")&& (Ýunikod_baha(Ad,"print")||Ýunikod_baha(Ad,"println")))||(!hyýaly_Jaň&&Ýunikod_baha(eýe_obýekt,"한국어/자체/출력"))){
        if(Ýunikod_baha(서술값,"(I)V")&&(Ýunikod_baha(Ad,"print")||Ýunikod_baha(Ad,"println")||Ýunikod_baha(Ad,"수쓰기"))){내보내기("jprint(x[0],1,%d);",Ýunikod_baha(Ad,"print")?0:1);return;}
        if(Ýunikod_baha(서술값,"(Ljava/lang/String;)V")&&(Ýunikod_baha(Ad,"print")||Ýunikod_baha(Ad,"println")||Ýunikod_baha(Ad,"Ýaz")||Ýunikod_baha(Ad,"ýaz_setir"))){내보내기("jprint(x[0],0,%d);",Ýunikod_baha(Ad,"print")||Ýunikod_baha(Ad,"Ýaz")?0:1);return;}
        if(Ýunikod_baha(서술값,"()V")&&Ýunikod_baha(Ad,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!hyýaly_Jaň&&Ýunikod_baha(eýe_obýekt,"한국어/자체/Faýl")){
        if(Ýunikod_baha(Ad,"Ýaz")&&Ýunikod_baha(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(Ýunikod_baha(Ad,"Oka")&&Ýunikod_baha(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void düz_usul(unsigned 색인){
    usul_girizmeklik*topar_ölçegi_üýtget=메소드목록+색인;if(Ýunikod_baha(topar_ölçegi_üýtget->Ad,"<init>"))return;int 결과,개수=서술자(topar_ölçegi_üýtget->서술값,&결과);if(개수<0){잘못됨=1;return;}
    내보내기("static W m%u(",색인);for(int 순번=0;순번<개수;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!개수)내보내기("void");
    if((unsigned)개수>topar_ölçegi_üýtget->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",topar_ölçegi_üýtget->지역변수들?topar_ölçegi_üýtget->지역변수들:1);for(int 순번=0;순번<개수;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=dowamlylyk_baha;dowamlylyk_baha=topar_ölçegi_üýtget->instruksiýa_SEQUENCE+topar_ölçegi_üýtget->Ululyk;현재위치=topar_ölçegi_üýtget->instruksiýa_SEQUENCE;
    while(현재위치<dowamlylyk_baha&&!잘못됨){unsigned 명령위치=현재위치-topar_ölçegi_üýtget->instruksiýa_SEQUENCE,amal_baha=baýt_maglumat();내보내기("L%u:;",명령위치);
        if(amal_baha==0){}
        else if(amal_baha==1)내보내기("P(0);");
        else if(amal_baha>=2&&amal_baha<=8)내보내기("P(%uU);",amal_baha-3);
        else if(amal_baha==16){int baha=(int8_t)baýt_maglumat();내보내기("P(%uU);",(unsigned)baha);}
        else if(amal_baha==17){int baha=(int16_t)절반값();내보내기("P(%uU);",(unsigned)baha);}
        else if(amal_baha==18||amal_baha==19)hemişelik_baha(amal_baha==18?baýt_maglumat():절반값());
        else if(amal_baha==21||amal_baha==25){unsigned 순번=baýt_maglumat();if(순번>=topar_ölçegi_üýtget->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((amal_baha>=26&&amal_baha<=29)||(amal_baha>=42&&amal_baha<=45)){unsigned 순번=amal_baha>=42?amal_baha-42:amal_baha-26;if(순번>=topar_ölçegi_üýtget->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(amal_baha==54||amal_baha==58){unsigned 순번=baýt_maglumat();if(순번>=topar_ölçegi_üýtget->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((amal_baha>=59&&amal_baha<=62)||(amal_baha>=75&&amal_baha<=78)){unsigned 순번=amal_baha>=75?amal_baha-75:amal_baha-59;if(순번>=topar_ölçegi_üýtget->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(amal_baha==46||amal_baha==50||amal_baha==51||amal_baha==52||amal_baha==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(amal_baha==79||amal_baha==83||amal_baha==84||amal_baha==85||amal_baha==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",amal_baha==84?"(unsigned)(signed char)q":amal_baha==85?"(unsigned short)q":amal_baha==86?"(unsigned)(short)q":"q");
        else if(amal_baha==87)내보내기("Q();");
        else if(amal_baha==89)내보내기("q=Q();P(q);P(q);");
        else if(amal_baha==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(amal_baha==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(amal_baha==96||amal_baha==100||amal_baha==104||amal_baha==120||amal_baha==124||amal_baha==126||amal_baha==128||amal_baha==130){const char*kodlaşdyrma_baha=amal_baha==96?"+":amal_baha==100?"-":amal_baha==104?"*":amal_baha==120?"<<":amal_baha==124?">>":amal_baha==126?"&":amal_baha==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kodlaşdyrma_baha,amal_baha==120||amal_baha==124?"%32":"");}
        else if(amal_baha==108||amal_baha==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",amal_baha==112);
        else if(amal_baha==116)내보내기("P(0U-(unsigned)Q());");
        else if(amal_baha==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(amal_baha==132){unsigned 순번=baýt_maglumat();int 차이=(int8_t)baýt_maglumat();if(순번>=topar_ölçegi_üýtget->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(amal_baha>=145&&amal_baha<=147)내보내기("P((unsigned)(%s)Q());",amal_baha==145?"signed char":amal_baha==146?"unsigned short":"short");
        else if(amal_baha>=153&&amal_baha<=166){int niýet=(int)명령위치+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(niýet<0||niýet>=(int)topar_ölçegi_üýtget->Ululyk){잘못됨=1;break;}if(amal_baha<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[amal_baha-153],niýet);else if(amal_baha<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[amal_baha-159],niýet);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",amal_baha==165?"==":"!=",niýet);}
        else if(amal_baha==167){int niýet=(int)명령위치+(int16_t)절반값();if(niýet<0||niýet>=(int)topar_ölçegi_üýtget->Ululyk)잘못됨=1;내보내기("goto L%d;",niýet);}
        else if(amal_baha==172||amal_baha==176)내보내기("return Q();");else if(amal_baha==177)내보내기("return 0;");
        else if(amal_baha==178||amal_baha==179){unsigned tanaýjy_baha=절반값();if(tanaýjy_baha<1||tanaýjy_baha>=상수모음||Taglar_Sanaw[tanaýjy_baha]!=9||첫째값[tanaýjy_baha]>=상수모음||둘째값[tanaýjy_baha]>=상수모음||Taglar_Sanaw[첫째값[tanaýjy_baha]]!=7||Taglar_Sanaw[둘째값[tanaýjy_baha]]!=12){잘못됨=1;break;}unsigned eýe_obýekt=첫째값[첫째값[tanaýjy_baha]],Ad=첫째값[둘째값[tanaýjy_baha]],서술값=둘째값[둘째값[tanaýjy_baha]];
            if(amal_baha==178&&Ýunikod_baha(eýe_obýekt,"java/lang/System")&&Ýunikod_baha(Ad,"out")&&Ýunikod_baha(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned faýl_girizmeklik=0;while(faýl_girizmeklik<필드개수&&(!같음(Ad,meýdanyň_ady[faýl_girizmeklik])||!같음(서술값,필드서술[faýl_girizmeklik])))faýl_girizmeklik++;if(!같음(eýe_obýekt,첫째값[현재클래스])||faýl_girizmeklik==필드개수){잘못됨=1;break;}내보내기(amal_baha==178?"P(fields[%u]);":"fields[%u]=Q();",faýl_girizmeklik);}}
        else if(amal_baha==182||amal_baha==184)호출(절반값(),amal_baha==182);
        else if(amal_baha==188){unsigned ýaz_kategoriýa=baýt_maglumat();if(ýaz_kategoriýa!=4&&ýaz_kategoriýa!=5&&ýaz_kategoriýa!=8&&ýaz_kategoriýa!=9&&ýaz_kategoriýa!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(amal_baha==190)내보내기("P(jlength(Q()));");
        else if(amal_baha==198||amal_baha==199){int niýet=(int)명령위치+(int16_t)절반값();if(niýet<0||niýet>=(int)topar_ölçegi_üýtget->Ululyk)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",amal_baha==198?"==":"!=",niýet);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",색인,amal_baha,명령위치);
        내보내기("\n");
    }
    dowamlylyk_baha=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned setir_sapak(unsigned *자료위치,unsigned tamamla_Süýşüriş){
    if(*자료위치>=tamamla_Süýşüriş){잘못됨=1;return 0;}unsigned nyşanyň_kody=maglumat[(*자료위치)++];
    if(nyşanyň_kody<128)return nyşanyň_kody;
    unsigned 개수=nyşanyň_kody>=0xc0&&nyşanyň_kody<=0xdf?1:nyşanyň_kody>=0xe0&&nyşanyň_kody<=0xef?2:3;
    if(개수==3||개수>tamamla_Süýşüriş-*자료위치){잘못됨=1;return 0;}unsigned baha=nyşanyň_kody&((1u<<(6-개수))-1);
    for(unsigned 순번=0;순번<개수;순번++){unsigned 다음=maglumat[(*자료위치)++];if((다음&0xc0)!=0x80)잘못됨=1;baha=baha<<6|(다음&63);}
    if((개수==1&&baha<128&&baha!=0)||(개수==2&&baha<2048))잘못됨=1;return baha;
}
static void setir_hemişelik(unsigned tanaýjy_baha){
    unsigned 부호없는값=첫째값[tanaýjy_baha];if(부호없는값<1||부호없는값>=상수모음||Taglar_Sanaw[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",tanaýjy_baha);
    unsigned 자료위치=첫째값[부호없는값],tamamla_Süýşüriş=자료위치+둘째값[부호없는값];
    while(자료위치<tamamla_Süýşüriş&&!잘못됨){unsigned nyşanyň_kody=setir_sapak(&자료위치,tamamla_Süýşüriş);
        if(nyşanyň_kody>=0xd800&&nyşanyň_kody<=0xdbff){unsigned 낮은부분=setir_sapak(&자료위치,tamamla_Süýşüriş);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}nyşanyň_kody=0x10000+((nyşanyň_kody-0xd800)<<10)+낮은부분-0xdc00;}
        else if(nyşanyň_kody>=0xdc00&&nyşanyň_kody<=0xdfff){잘못됨=1;break;}
        if(!nyşanyň_kody){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(nyşanyň_kody<128)내보내기("%u,",nyşanyň_kody);
        else{unsigned 개수=nyşanyň_kody<2048?2:nyşanyň_kody<65536?3:4;내보내기("%u,",(개수==2?0xc0:개수==3?0xe0:0xf0)|(nyşanyň_kody>>(6*(개수-1))));for(unsigned 순번=개수-1;순번;순번--)내보내기("%u,",0x80|((nyşanyň_kody>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Ad){
    size_t 개수=strlen(Ad);
    if(개수>4&&!strcmp(Ad+개수-4,".jar")){
        if(꾸러미열기(Ad)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Ýol[256];const char*girizmeklik_usul=꾸러미진입클래스();개수=strlen(girizmeklik_usul);if(개수+6>=sizeof(Ýol))return 0;
        for(unsigned 순번=0;순번<개수;순번++)Ýol[순번]=girizmeklik_usul[순번]=='.'?'/':girizmeklik_usul[순번];strcpy(Ýol+개수,".class");int 항목수=꾸러미읽기(Ýol,maglumat,sizeof(maglumat));if(항목수<0)return 0;dowamlylyk_baha=항목수;
    }else{intptr_t faýl_ryçag=사용자호출(3,(uintptr_t)Ad,0,0,0,0,0);if(faýl_ryçag<0)return 0;intptr_t 항목수=사용자호출(9,faýl_ryçag,0,0,0,0,0);if(항목수<0||항목수>sizeof(maglumat)){사용자호출(4,faýl_ryçag,0,0,0,0,0);return 0;}intptr_t 받은수=사용자호출(2,faýl_ryçag,(uintptr_t)maglumat,항목수,0,0,0);사용자호출(4,faýl_ryçag,0,0,0,0,0);if(받은수!=항목수)return 0;dowamlylyk_baha=항목수;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(Taglar_Sanaw[순번]==8)setir_hemişelik(순번);
    if(잘못됨)return 0;
    int girizmeklik_utuk=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!Ýunikod_baha(메소드목록[순번].Ad,"<init>")){
        int 결과,항목수=서술자(메소드목록[순번].서술값,&결과);if(항목수<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<항목수;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!항목수)내보내기("void");내보내기(");\n");
        if(Ýunikod_baha(메소드목록[순번].Ad,"main")&&Ýunikod_baha(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)girizmeklik_utuk=순번;
        if(Ýunikod_baha(메소드목록[순번].Ad,"<clinit>"))초기값=순번;
    }
    if(girizmeklik_utuk<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)düz_usul(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(meýdan_hemişelik[순번]){
        unsigned nyşanyň_kody=meýdan_hemişelik[순번];if(nyşanyň_kody>=상수모음)return 0;
        if(Taglar_Sanaw[nyşanyň_kody]==3)내보내기("fields[%u]=%uU;",순번,첫째값[nyşanyň_kody]);else if(Taglar_Sanaw[nyşanyň_kody]==8)내보내기("fields[%u]=(W)k%u;",순번,nyşanyň_kody);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",girizmeklik_utuk);
    return 잘못됨?0:Metin;
}
