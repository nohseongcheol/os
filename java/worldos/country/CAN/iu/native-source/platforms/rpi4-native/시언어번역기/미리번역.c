#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "꾸러미.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char titiqqat[16384];static unsigned takininga_atuutilik,현재위치;static int 잘못됨;
static unsigned Ataqatigiit_Titiqpalliagaq[512],첫째값[512],둘째값[512],상수모음,현재클래스;
static char titiqqaq[65536];static unsigned titiqqaq_anininga;
typedef struct {unsigned 설정비트,atiq,서술값,명령열,anininga,지역변수들,쌓임공간;} 메소드;
static 메소드 메소드목록[64];static unsigned 메소드개수;
static unsigned kisumuungaviup_atinga[64],필드서술[64],kisumuungavik_surragunnangittuq[64],필드개수;
static unsigned 가져오기(unsigned 개수){if(현재위치>takininga_atuutilik||개수>takininga_atuutilik-현재위치){잘못됨=1;return 0;}unsigned 자료위치=현재위치;현재위치+=개수;return 자료위치;}
static unsigned byte_titiqqat(void){unsigned 자료위치=가져오기(1);return 잘못됨?0:titiqqat[자료위치];}
static unsigned 절반값(void){unsigned 가로좌표=byte_titiqqat();return 가로좌표<<8|byte_titiqqat();}
static uint32_t 가득참(void){uint32_t 가로좌표=절반값();return 가로좌표<<16|절반값();}
static int Unicode_atuutilik(unsigned 순번,const char*qimiaq_titiqqat){return 순번>0&&순번<상수모음&&Ataqatigiit_Titiqpalliagaq[순번]==1&&strlen(qimiaq_titiqqat)==둘째값[순번]&&!memcmp(titiqqat+첫째값[순번],qimiaq_titiqqat,둘째값[순번]);}
static int 같음(unsigned 가로좌표,unsigned 세로좌표){return 가로좌표>0&&가로좌표<상수모음&&세로좌표>0&&세로좌표<상수모음&&Ataqatigiit_Titiqpalliagaq[가로좌표]==1&&Ataqatigiit_Titiqpalliagaq[세로좌표]==1&&둘째값[가로좌표]==둘째값[세로좌표]&&!memcmp(titiqqat+첫째값[가로좌표],titiqqat+첫째값[세로좌표],둘째값[가로좌표]);}
static void 내보내기(const char*ini_Iliniku,...){if(잘못됨)return;va_list aturniqarnirainiq_array;va_start(aturniqarnirainiq_array,ini_Iliniku);int 개수=vsnprintf(titiqqaq+titiqqaq_anininga,sizeof(titiqqaq)-titiqqaq_anininga,ini_Iliniku,aturniqarnirainiq_array);va_end(aturniqarnirainiq_array);if(개수<0||(unsigned)개수>=sizeof(titiqqaq)-titiqqaq_anininga){잘못됨=1;return;}titiqqaq_anininga+=개수;}
static int 서술자(unsigned 식별자,int*결과){
    if(식별자<1||식별자>=상수모음||Ataqatigiit_Titiqpalliagaq[식별자]!=1)return -1;unsigned 자료위치=첫째값[식별자],끝위치=자료위치+둘째값[식별자];if(자료위치>=끝위치||titiqqat[자료위치++]!='(')return -1;int 항목수=0;
    while(자료위치<끝위치&&titiqqat[자료위치]!=')'){
        unsigned immikkuuqtumut_nalunaikkut=titiqqat[자료위치++];while(immikkuuqtumut_nalunaikkut=='['&&자료위치<끝위치)immikkuuqtumut_nalunaikkut=titiqqat[자료위치++];
        if(immikkuuqtumut_nalunaikkut=='L'){while(자료위치<끝위치&&titiqqat[자료위치]!=';')자료위치++;if(자료위치==끝위치)return -1;자료위치++;}
        else if(immikkuuqtumut_nalunaikkut!='I'&&immikkuuqtumut_nalunaikkut!='Z'&&immikkuuqtumut_nalunaikkut!='B'&&immikkuuqtumut_nalunaikkut!='C'&&immikkuuqtumut_nalunaikkut!='S')return -1;
        if(++항목수>16)return -1;
    }
    if(자료위치+1>=끝위치||titiqqat[자료위치++]!=')')return -1;*결과=titiqqat[자료위치]=='V'?0:1;
    if(titiqqat[자료위치]=='J'||titiqqat[자료위치]=='D'||titiqqat[자료위치]=='F')return -1;return 항목수;
}
static void 속성들(void){unsigned 개수=절반값();for(unsigned 순번=0;순번<개수&&!잘못됨;순번++){절반값();unsigned anininga=가득참();가져오기(anininga);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned 부버전=절반값(),판번호=절반값();if(부버전||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        Ataqatigiit_Titiqpalliagaq[순번]=byte_titiqqat();switch(Ataqatigiit_Titiqpalliagaq[순번]){
        case 1:둘째값[순번]=절반값();첫째값[순번]=가져오기(둘째값[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:가져오기(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();둘째값[순번]=절반값();break;
        case 15:첫째값[순번]=byte_titiqqat();둘째값[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Ataqatigiit_Titiqpalliagaq[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Ataqatigiit_Titiqpalliagaq[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();가져오기(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();kisumuungaviup_atinga[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned 항목수=절반값();for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned atiq=절반값(),anininga=가득참();
            if(Unicode_atuutilik(atiq,"ConstantValue")){if(anininga!=2)return -1;kisumuungavik_surragunnangittuq[순번]=절반값();}
            else 가져오기(anininga);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        메소드*katinngajut_anininga=메소드목록+순번;katinngajut_anininga->설정비트=절반값();katinngajut_anininga->atiq=절반값();katinngajut_anininga->서술값=절반값();unsigned 항목수=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned atiq=절반값(),anininga=가득참(),시작=현재위치;
            if(anininga>takininga_atuutilik-현재위치)return -1;
            if(Unicode_atuutilik(atiq,"Code")){
                katinngajut_anininga->쌓임공간=절반값();katinngajut_anininga->지역변수들=절반값();katinngajut_anininga->anininga=가득참();katinngajut_anininga->명령열=가져오기(katinngajut_anininga->anininga);
                if(katinngajut_anininga->쌓임공간>128||katinngajut_anininga->지역변수들>128||katinngajut_anininga->anininga>8192||절반값())return -1;속성들();
            }else 가져오기(anininga);
            if(현재위치!=시작+anininga)return -1;
        }
        if(!Unicode_atuutilik(katinngajut_anininga->atiq,"<init>")&&(!(katinngajut_anininga->설정비트&8)||(katinngajut_anininga->설정비트&(0x100|0x20))||!katinngajut_anininga->anininga))return -1;
    }
    속성들();return 잘못됨||현재위치!=takininga_atuutilik?-1:0;
}
static void surragunnangittuq_atuutilik(unsigned 식별자){
    if(!식별자||식별자>=상수모음){잘못됨=1;return;}
    if(Ataqatigiit_Titiqpalliagaq[식별자]==3)내보내기("P(%uU);",첫째값[식별자]);
    else if(Ataqatigiit_Titiqpalliagaq[식별자]==8)내보내기("P((W)k%u);",식별자);else 잘못됨=1;
}
static void 호출(unsigned 식별자,int saqqijaanganngittuq_Uqaalaniq){
    if(식별자<1||식별자>=상수모음||(Ataqatigiit_Titiqpalliagaq[식별자]!=10&&Ataqatigiit_Titiqpalliagaq[식별자]!=11)||첫째값[식별자]<1||첫째값[식별자]>=상수모음||Ataqatigiit_Titiqpalliagaq[첫째값[식별자]]!=7||둘째값[식별자]<1||둘째값[식별자]>=상수모음||Ataqatigiit_Titiqpalliagaq[둘째값[식별자]]!=12){잘못됨=1;return;}
    unsigned 소유자=첫째값[첫째값[식별자]],atiq=첫째값[둘째값[식별자]],서술값=둘째값[둘째값[식별자]];int 결과=0,개수=서술자(서술값,&결과);if(개수<0){잘못됨=1;return;}
    for(int 순번=개수;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(saqqijaanganngittuq_Uqaalaniq)내보내기("Q();");
    if(!saqqijaanganngittuq_Uqaalaniq&&같음(소유자,첫째값[현재클래스])){
        unsigned katinngajut_anininga=0;for(;katinngajut_anininga<메소드개수;katinngajut_anininga++)if(같음(atiq,메소드목록[katinngajut_anininga].atiq)&&같음(서술값,메소드목록[katinngajut_anininga].서술값))break;
        if(katinngajut_anininga==메소드개수||!(메소드목록[katinngajut_anininga].설정비트&8)){잘못됨=1;return;}
        if(결과)내보내기("P(");내보내기("m%u(",katinngajut_anininga);for(int 순번=0;순번<개수;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(결과?"));":" );");return;
    }
    if((saqqijaanganngittuq_Uqaalaniq&&Unicode_atuutilik(소유자,"java/io/PrintStream")&& (Unicode_atuutilik(atiq,"print")||Unicode_atuutilik(atiq,"println")))||(!saqqijaanganngittuq_Uqaalaniq&&Unicode_atuutilik(소유자,"한국어/자체/출력"))){
        if(Unicode_atuutilik(서술값,"(I)V")&&(Unicode_atuutilik(atiq,"print")||Unicode_atuutilik(atiq,"println")||Unicode_atuutilik(atiq,"수쓰기"))){내보내기("jprint(x[0],1,%d);",Unicode_atuutilik(atiq,"print")?0:1);return;}
        if(Unicode_atuutilik(서술값,"(Ljava/lang/String;)V")&&(Unicode_atuutilik(atiq,"print")||Unicode_atuutilik(atiq,"println")||Unicode_atuutilik(atiq,"titiraq")||Unicode_atuutilik(atiq,"titiraq_titikutaak"))){내보내기("jprint(x[0],0,%d);",Unicode_atuutilik(atiq,"print")||Unicode_atuutilik(atiq,"titiraq")?0:1);return;}
        if(Unicode_atuutilik(서술값,"()V")&&Unicode_atuutilik(atiq,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!saqqijaanganngittuq_Uqaalaniq&&Unicode_atuutilik(소유자,"한국어/자체/ini")){
        if(Unicode_atuutilik(atiq,"titiraq")&&Unicode_atuutilik(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(Unicode_atuutilik(atiq,"읽기")&&Unicode_atuutilik(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void 메소드번역(unsigned 색인){
    메소드*katinngajut_anininga=메소드목록+색인;if(Unicode_atuutilik(katinngajut_anininga->atiq,"<init>"))return;int 결과,개수=서술자(katinngajut_anininga->서술값,&결과);if(개수<0){잘못됨=1;return;}
    내보내기("static W m%u(",색인);for(int 순번=0;순번<개수;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!개수)내보내기("void");
    if((unsigned)개수>katinngajut_anininga->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",katinngajut_anininga->지역변수들?katinngajut_anininga->지역변수들:1);for(int 순번=0;순번<개수;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=takininga_atuutilik;takininga_atuutilik=katinngajut_anininga->명령열+katinngajut_anininga->anininga;현재위치=katinngajut_anininga->명령열;
    while(현재위치<takininga_atuutilik&&!잘못됨){unsigned 명령위치=현재위치-katinngajut_anininga->명령열,aulattiniq_atuutilik=byte_titiqqat();내보내기("L%u:;",명령위치);
        if(aulattiniq_atuutilik==0){}
        else if(aulattiniq_atuutilik==1)내보내기("P(0);");
        else if(aulattiniq_atuutilik>=2&&aulattiniq_atuutilik<=8)내보내기("P(%uU);",aulattiniq_atuutilik-3);
        else if(aulattiniq_atuutilik==16){int atuutilik=(int8_t)byte_titiqqat();내보내기("P(%uU);",(unsigned)atuutilik);}
        else if(aulattiniq_atuutilik==17){int atuutilik=(int16_t)절반값();내보내기("P(%uU);",(unsigned)atuutilik);}
        else if(aulattiniq_atuutilik==18||aulattiniq_atuutilik==19)surragunnangittuq_atuutilik(aulattiniq_atuutilik==18?byte_titiqqat():절반값());
        else if(aulattiniq_atuutilik==21||aulattiniq_atuutilik==25){unsigned 순번=byte_titiqqat();if(순번>=katinngajut_anininga->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((aulattiniq_atuutilik>=26&&aulattiniq_atuutilik<=29)||(aulattiniq_atuutilik>=42&&aulattiniq_atuutilik<=45)){unsigned 순번=aulattiniq_atuutilik>=42?aulattiniq_atuutilik-42:aulattiniq_atuutilik-26;if(순번>=katinngajut_anininga->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(aulattiniq_atuutilik==54||aulattiniq_atuutilik==58){unsigned 순번=byte_titiqqat();if(순번>=katinngajut_anininga->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((aulattiniq_atuutilik>=59&&aulattiniq_atuutilik<=62)||(aulattiniq_atuutilik>=75&&aulattiniq_atuutilik<=78)){unsigned 순번=aulattiniq_atuutilik>=75?aulattiniq_atuutilik-75:aulattiniq_atuutilik-59;if(순번>=katinngajut_anininga->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(aulattiniq_atuutilik==46||aulattiniq_atuutilik==50||aulattiniq_atuutilik==51||aulattiniq_atuutilik==52||aulattiniq_atuutilik==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(aulattiniq_atuutilik==79||aulattiniq_atuutilik==83||aulattiniq_atuutilik==84||aulattiniq_atuutilik==85||aulattiniq_atuutilik==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",aulattiniq_atuutilik==84?"(unsigned)(signed char)q":aulattiniq_atuutilik==85?"(unsigned short)q":aulattiniq_atuutilik==86?"(unsigned)(short)q":"q");
        else if(aulattiniq_atuutilik==87)내보내기("Q();");
        else if(aulattiniq_atuutilik==89)내보내기("q=Q();P(q);P(q);");
        else if(aulattiniq_atuutilik==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(aulattiniq_atuutilik==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(aulattiniq_atuutilik==96||aulattiniq_atuutilik==100||aulattiniq_atuutilik==104||aulattiniq_atuutilik==120||aulattiniq_atuutilik==124||aulattiniq_atuutilik==126||aulattiniq_atuutilik==128||aulattiniq_atuutilik==130){const char*tukiniktiri_atuutilik=aulattiniq_atuutilik==96?"+":aulattiniq_atuutilik==100?"-":aulattiniq_atuutilik==104?"*":aulattiniq_atuutilik==120?"<<":aulattiniq_atuutilik==124?">>":aulattiniq_atuutilik==126?"&":aulattiniq_atuutilik==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",tukiniktiri_atuutilik,aulattiniq_atuutilik==120||aulattiniq_atuutilik==124?"%32":"");}
        else if(aulattiniq_atuutilik==108||aulattiniq_atuutilik==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",aulattiniq_atuutilik==112);
        else if(aulattiniq_atuutilik==116)내보내기("P(0U-(unsigned)Q());");
        else if(aulattiniq_atuutilik==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(aulattiniq_atuutilik==132){unsigned 순번=byte_titiqqat();int 차이=(int8_t)byte_titiqqat();if(순번>=katinngajut_anininga->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(aulattiniq_atuutilik>=145&&aulattiniq_atuutilik<=147)내보내기("P((unsigned)(%s)Q());",aulattiniq_atuutilik==145?"signed char":aulattiniq_atuutilik==146?"unsigned short":"short");
        else if(aulattiniq_atuutilik>=153&&aulattiniq_atuutilik<=166){int turaagaq=(int)명령위치+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(turaagaq<0||turaagaq>=(int)katinngajut_anininga->anininga){잘못됨=1;break;}if(aulattiniq_atuutilik<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[aulattiniq_atuutilik-153],turaagaq);else if(aulattiniq_atuutilik<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[aulattiniq_atuutilik-159],turaagaq);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",aulattiniq_atuutilik==165?"==":"!=",turaagaq);}
        else if(aulattiniq_atuutilik==167){int turaagaq=(int)명령위치+(int16_t)절반값();if(turaagaq<0||turaagaq>=(int)katinngajut_anininga->anininga)잘못됨=1;내보내기("goto L%d;",turaagaq);}
        else if(aulattiniq_atuutilik==172||aulattiniq_atuutilik==176)내보내기("return Q();");else if(aulattiniq_atuutilik==177)내보내기("return 0;");
        else if(aulattiniq_atuutilik==178||aulattiniq_atuutilik==179){unsigned 식별자=절반값();if(식별자<1||식별자>=상수모음||Ataqatigiit_Titiqpalliagaq[식별자]!=9||첫째값[식별자]>=상수모음||둘째값[식별자]>=상수모음||Ataqatigiit_Titiqpalliagaq[첫째값[식별자]]!=7||Ataqatigiit_Titiqpalliagaq[둘째값[식별자]]!=12){잘못됨=1;break;}unsigned 소유자=첫째값[첫째값[식별자]],atiq=첫째값[둘째값[식별자]],서술값=둘째값[둘째값[식별자]];
            if(aulattiniq_atuutilik==178&&Unicode_atuutilik(소유자,"java/lang/System")&&Unicode_atuutilik(atiq,"out")&&Unicode_atuutilik(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned ini_Iliniku=0;while(ini_Iliniku<필드개수&&(!같음(atiq,kisumuungaviup_atinga[ini_Iliniku])||!같음(서술값,필드서술[ini_Iliniku])))ini_Iliniku++;if(!같음(소유자,첫째값[현재클래스])||ini_Iliniku==필드개수){잘못됨=1;break;}내보내기(aulattiniq_atuutilik==178?"P(fields[%u]);":"fields[%u]=Q();",ini_Iliniku);}}
        else if(aulattiniq_atuutilik==182||aulattiniq_atuutilik==184)호출(절반값(),aulattiniq_atuutilik==182);
        else if(aulattiniq_atuutilik==188){unsigned qanuittuuninga_Ataqatigiivvik=byte_titiqqat();if(qanuittuuninga_Ataqatigiivvik!=4&&qanuittuuninga_Ataqatigiivvik!=5&&qanuittuuninga_Ataqatigiivvik!=8&&qanuittuuninga_Ataqatigiivvik!=9&&qanuittuuninga_Ataqatigiivvik!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(aulattiniq_atuutilik==190)내보내기("P(jlength(Q()));");
        else if(aulattiniq_atuutilik==198||aulattiniq_atuutilik==199){int turaagaq=(int)명령위치+(int16_t)절반값();if(turaagaq<0||turaagaq>=(int)katinngajut_anininga->anininga)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",aulattiniq_atuutilik==198?"==":"!=",turaagaq);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",색인,aulattiniq_atuutilik,명령위치);
        내보내기("\n");
    }
    takininga_atuutilik=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned qimiaq_atauttimiittut(unsigned *자료위치,unsigned 끝위치){
    if(*자료위치>=끝위치){잘못됨=1;return 0;}unsigned immikkuuqtumut_nalunaikkut=titiqqat[(*자료위치)++];
    if(immikkuuqtumut_nalunaikkut<128)return immikkuuqtumut_nalunaikkut;
    unsigned 개수=immikkuuqtumut_nalunaikkut>=0xc0&&immikkuuqtumut_nalunaikkut<=0xdf?1:immikkuuqtumut_nalunaikkut>=0xe0&&immikkuuqtumut_nalunaikkut<=0xef?2:3;
    if(개수==3||개수>끝위치-*자료위치){잘못됨=1;return 0;}unsigned atuutilik=immikkuuqtumut_nalunaikkut&((1u<<(6-개수))-1);
    for(unsigned 순번=0;순번<개수;순번++){unsigned 다음=titiqqat[(*자료위치)++];if((다음&0xc0)!=0x80)잘못됨=1;atuutilik=atuutilik<<6|(다음&63);}
    if((개수==1&&atuutilik<128&&atuutilik!=0)||(개수==2&&atuutilik<2048))잘못됨=1;return atuutilik;
}
static void qimiaq_surragunnangittuq(unsigned 식별자){
    unsigned 부호없는값=첫째값[식별자];if(부호없는값<1||부호없는값>=상수모음||Ataqatigiit_Titiqpalliagaq[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",식별자);
    unsigned 자료위치=첫째값[부호없는값],끝위치=자료위치+둘째값[부호없는값];
    while(자료위치<끝위치&&!잘못됨){unsigned immikkuuqtumut_nalunaikkut=qimiaq_atauttimiittut(&자료위치,끝위치);
        if(immikkuuqtumut_nalunaikkut>=0xd800&&immikkuuqtumut_nalunaikkut<=0xdbff){unsigned 낮은부분=qimiaq_atauttimiittut(&자료위치,끝위치);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}immikkuuqtumut_nalunaikkut=0x10000+((immikkuuqtumut_nalunaikkut-0xd800)<<10)+낮은부분-0xdc00;}
        else if(immikkuuqtumut_nalunaikkut>=0xdc00&&immikkuuqtumut_nalunaikkut<=0xdfff){잘못됨=1;break;}
        if(!immikkuuqtumut_nalunaikkut){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(immikkuuqtumut_nalunaikkut<128)내보내기("%u,",immikkuuqtumut_nalunaikkut);
        else{unsigned 개수=immikkuuqtumut_nalunaikkut<2048?2:immikkuuqtumut_nalunaikkut<65536?3:4;내보내기("%u,",(개수==2?0xc0:개수==3?0xe0:0xf0)|(immikkuuqtumut_nalunaikkut>>(6*(개수-1))));for(unsigned 순번=개수-1;순번;순번--)내보내기("%u,",0x80|((immikkuuqtumut_nalunaikkut>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*atiq){
    size_t 개수=strlen(atiq);
    if(개수>4&&!strcmp(atiq+개수-4,".jar")){
        if(꾸러미열기(atiq)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char aqqut[256];const char*진입함수=꾸러미진입클래스();개수=strlen(진입함수);if(개수+6>=sizeof(aqqut))return 0;
        for(unsigned 순번=0;순번<개수;순번++)aqqut[순번]=진입함수[순번]=='.'?'/':진입함수[순번];strcpy(aqqut+개수,".class");int 항목수=꾸러미읽기(aqqut,titiqqat,sizeof(titiqqat));if(항목수<0)return 0;takininga_atuutilik=항목수;
    }else{intptr_t ini_nuuttarut=사용자호출(3,(uintptr_t)atiq,0,0,0,0,0);if(ini_nuuttarut<0)return 0;intptr_t 항목수=사용자호출(9,ini_nuuttarut,0,0,0,0,0);if(항목수<0||항목수>sizeof(titiqqat)){사용자호출(4,ini_nuuttarut,0,0,0,0,0);return 0;}intptr_t 받은수=사용자호출(2,ini_nuuttarut,(uintptr_t)titiqqat,항목수,0,0,0);사용자호출(4,ini_nuuttarut,0,0,0,0,0);if(받은수!=항목수)return 0;takininga_atuutilik=항목수;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(Ataqatigiit_Titiqpalliagaq[순번]==8)qimiaq_surragunnangittuq(순번);
    if(잘못됨)return 0;
    int Iliniku_puinti=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!Unicode_atuutilik(메소드목록[순번].atiq,"<init>")){
        int 결과,항목수=서술자(메소드목록[순번].서술값,&결과);if(항목수<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<항목수;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!항목수)내보내기("void");내보내기(");\n");
        if(Unicode_atuutilik(메소드목록[순번].atiq,"main")&&Unicode_atuutilik(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)Iliniku_puinti=순번;
        if(Unicode_atuutilik(메소드목록[순번].atiq,"<clinit>"))초기값=순번;
    }
    if(Iliniku_puinti<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)메소드번역(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(kisumuungavik_surragunnangittuq[순번]){
        unsigned immikkuuqtumut_nalunaikkut=kisumuungavik_surragunnangittuq[순번];if(immikkuuqtumut_nalunaikkut>=상수모음)return 0;
        if(Ataqatigiit_Titiqpalliagaq[immikkuuqtumut_nalunaikkut]==3)내보내기("fields[%u]=%uU;",순번,첫째값[immikkuuqtumut_nalunaikkut]);else if(Ataqatigiit_Titiqpalliagaq[immikkuuqtumut_nalunaikkut]==8)내보내기("fields[%u]=(W)k%u;",순번,immikkuuqtumut_nalunaikkut);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",Iliniku_puinti);
    return 잘못됨?0:titiqqaq;
}
