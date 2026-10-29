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
static unsigned char keɓe[16384];static unsigned njuuteendi_njaru,현재위치;static int 잘못됨;
static unsigned Tage_Doggol[512],첫째값[512],둘째값[512],상수모음,현재클래스;
static char binndi[65536];static unsigned binndi_waylude_etannde;
typedef struct {unsigned 설정비트,innde,서술값,명령열,waylude_etannde,지역변수들,쌓임공간;} 메소드;
static 메소드 메소드목록[64];static unsigned 메소드개수;
static unsigned suudu_innde[64],필드서술[64],필드상수[64],필드개수;
static unsigned 가져오기(unsigned 개수){if(현재위치>njuuteendi_njaru||개수>njuuteendi_njaru-현재위치){잘못됨=1;return 0;}unsigned 자료위치=현재위치;현재위치+=개수;return 자료위치;}
static unsigned oktee_keɓe(void){unsigned 자료위치=가져오기(1);return 잘못됨?0:keɓe[자료위치];}
static unsigned 절반값(void){unsigned 가로좌표=oktee_keɓe();return 가로좌표<<8|oktee_keɓe();}
static uint32_t 가득참(void){uint32_t 가로좌표=절반값();return 가로좌표<<16|절반값();}
static int Unicode_njaru(unsigned 순번,const char*ɓoggol_keɓe){return 순번>0&&순번<상수모음&&Tage_Doggol[순번]==1&&strlen(ɓoggol_keɓe)==둘째값[순번]&&!memcmp(keɓe+첫째값[순번],ɓoggol_keɓe,둘째값[순번]);}
static int 같음(unsigned 가로좌표,unsigned 세로좌표){return 가로좌표>0&&가로좌표<상수모음&&세로좌표>0&&세로좌표<상수모음&&Tage_Doggol[가로좌표]==1&&Tage_Doggol[세로좌표]==1&&둘째값[가로좌표]==둘째값[세로좌표]&&!memcmp(keɓe+첫째값[가로좌표],keɓe+첫째값[세로좌표],둘째값[가로좌표]);}
static void 내보내기(const char*fiilde_naatnugol,...){if(잘못됨)return;va_list 인수배열;va_start(인수배열,fiilde_naatnugol);int 개수=vsnprintf(binndi+binndi_waylude_etannde,sizeof(binndi)-binndi_waylude_etannde,fiilde_naatnugol,인수배열);va_end(인수배열);if(개수<0||(unsigned)개수>=sizeof(binndi)-binndi_waylude_etannde){잘못됨=1;return;}binndi_waylude_etannde+=개수;}
static int 서술자(unsigned 식별자,int*결과){
    if(식별자<1||식별자>=상수모음||Tage_Doggol[식별자]!=1)return -1;unsigned 자료위치=첫째값[식별자],끝위치=자료위치+둘째값[식별자];if(자료위치>=끝위치||keɓe[자료위치++]!='(')return -1;int 항목수=0;
    while(자료위치<끝위치&&keɓe[자료위치]!=')'){
        unsigned 문자값=keɓe[자료위치++];while(문자값=='['&&자료위치<끝위치)문자값=keɓe[자료위치++];
        if(문자값=='L'){while(자료위치<끝위치&&keɓe[자료위치]!=';')자료위치++;if(자료위치==끝위치)return -1;자료위치++;}
        else if(문자값!='I'&&문자값!='Z'&&문자값!='B'&&문자값!='C'&&문자값!='S')return -1;
        if(++항목수>16)return -1;
    }
    if(자료위치+1>=끝위치||keɓe[자료위치++]!=')')return -1;*결과=keɓe[자료위치]=='V'?0:1;
    if(keɓe[자료위치]=='J'||keɓe[자료위치]=='D'||keɓe[자료위치]=='F')return -1;return 항목수;
}
static void 속성들(void){unsigned 개수=절반값();for(unsigned 순번=0;순번<개수&&!잘못됨;순번++){절반값();unsigned waylude_etannde=가득참();가져오기(waylude_etannde);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned 부버전=절반값(),판번호=절반값();if(부버전||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        Tage_Doggol[순번]=oktee_keɓe();switch(Tage_Doggol[순번]){
        case 1:둘째값[순번]=절반값();첫째값[순번]=가져오기(둘째값[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:가져오기(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();둘째값[순번]=절반값();break;
        case 15:첫째값[순번]=oktee_keɓe();둘째값[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Tage_Doggol[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Tage_Doggol[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();가져오기(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();suudu_innde[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned 항목수=절반값();for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned innde=절반값(),waylude_etannde=가득참();
            if(Unicode_njaru(innde,"ConstantValue")){if(waylude_etannde!=2)return -1;필드상수[순번]=절반값();}
            else 가져오기(waylude_etannde);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        메소드*seto_waylude_etannde=메소드목록+순번;seto_waylude_etannde->설정비트=절반값();seto_waylude_etannde->innde=절반값();seto_waylude_etannde->서술값=절반값();unsigned 항목수=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned innde=절반값(),waylude_etannde=가득참(),huutoraade=현재위치;
            if(waylude_etannde>njuuteendi_njaru-현재위치)return -1;
            if(Unicode_njaru(innde,"Code")){
                seto_waylude_etannde->쌓임공간=절반값();seto_waylude_etannde->지역변수들=절반값();seto_waylude_etannde->waylude_etannde=가득참();seto_waylude_etannde->명령열=가져오기(seto_waylude_etannde->waylude_etannde);
                if(seto_waylude_etannde->쌓임공간>128||seto_waylude_etannde->지역변수들>128||seto_waylude_etannde->waylude_etannde>8192||절반값())return -1;속성들();
            }else 가져오기(waylude_etannde);
            if(현재위치!=huutoraade+waylude_etannde)return -1;
        }
        if(!Unicode_njaru(seto_waylude_etannde->innde,"<init>")&&(!(seto_waylude_etannde->설정비트&8)||(seto_waylude_etannde->설정비트&(0x100|0x20))||!seto_waylude_etannde->waylude_etannde))return -1;
    }
    속성들();return 잘못됨||현재위치!=njuuteendi_njaru?-1:0;
}
static void 상수(unsigned 식별자){
    if(!식별자||식별자>=상수모음){잘못됨=1;return;}
    if(Tage_Doggol[식별자]==3)내보내기("P(%uU);",첫째값[식별자]);
    else if(Tage_Doggol[식별자]==8)내보내기("P((W)k%u);",식별자);else 잘못됨=1;
}
static void 호출(unsigned 식별자,int paayaalo_noddude){
    if(식별자<1||식별자>=상수모음||(Tage_Doggol[식별자]!=10&&Tage_Doggol[식별자]!=11)||첫째값[식별자]<1||첫째값[식별자]>=상수모음||Tage_Doggol[첫째값[식별자]]!=7||둘째값[식별자]<1||둘째값[식별자]>=상수모음||Tage_Doggol[둘째값[식별자]]!=12){잘못됨=1;return;}
    unsigned 소유자=첫째값[첫째값[식별자]],innde=첫째값[둘째값[식별자]],서술값=둘째값[둘째값[식별자]];int 결과=0,개수=서술자(서술값,&결과);if(개수<0){잘못됨=1;return;}
    for(int 순번=개수;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(paayaalo_noddude)내보내기("Q();");
    if(!paayaalo_noddude&&같음(소유자,첫째값[현재클래스])){
        unsigned seto_waylude_etannde=0;for(;seto_waylude_etannde<메소드개수;seto_waylude_etannde++)if(같음(innde,메소드목록[seto_waylude_etannde].innde)&&같음(서술값,메소드목록[seto_waylude_etannde].서술값))break;
        if(seto_waylude_etannde==메소드개수||!(메소드목록[seto_waylude_etannde].설정비트&8)){잘못됨=1;return;}
        if(결과)내보내기("P(");내보내기("m%u(",seto_waylude_etannde);for(int 순번=0;순번<개수;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(결과?"));":" );");return;
    }
    if((paayaalo_noddude&&Unicode_njaru(소유자,"java/io/PrintStream")&& (Unicode_njaru(innde,"print")||Unicode_njaru(innde,"println")))||(!paayaalo_noddude&&Unicode_njaru(소유자,"한국어/자체/출력"))){
        if(Unicode_njaru(서술값,"(I)V")&&(Unicode_njaru(innde,"print")||Unicode_njaru(innde,"println")||Unicode_njaru(innde,"수쓰기"))){내보내기("jprint(x[0],1,%d);",Unicode_njaru(innde,"print")?0:1);return;}
        if(Unicode_njaru(서술값,"(Ljava/lang/String;)V")&&(Unicode_njaru(innde,"print")||Unicode_njaru(innde,"println")||Unicode_njaru(innde,"winndude")||Unicode_njaru(innde,"winndude_diidol"))){내보내기("jprint(x[0],0,%d);",Unicode_njaru(innde,"print")||Unicode_njaru(innde,"winndude")?0:1);return;}
        if(Unicode_njaru(서술값,"()V")&&Unicode_njaru(innde,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!paayaalo_noddude&&Unicode_njaru(소유자,"한국어/자체/fiilde")){
        if(Unicode_njaru(innde,"winndude")&&Unicode_njaru(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(Unicode_njaru(innde,"읽기")&&Unicode_njaru(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void 메소드번역(unsigned 색인){
    메소드*seto_waylude_etannde=메소드목록+색인;if(Unicode_njaru(seto_waylude_etannde->innde,"<init>"))return;int 결과,개수=서술자(seto_waylude_etannde->서술값,&결과);if(개수<0){잘못됨=1;return;}
    내보내기("static W m%u(",색인);for(int 순번=0;순번<개수;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!개수)내보내기("void");
    if((unsigned)개수>seto_waylude_etannde->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",seto_waylude_etannde->지역변수들?seto_waylude_etannde->지역변수들:1);for(int 순번=0;순번<개수;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=njuuteendi_njaru;njuuteendi_njaru=seto_waylude_etannde->명령열+seto_waylude_etannde->waylude_etannde;현재위치=seto_waylude_etannde->명령열;
    while(현재위치<njuuteendi_njaru&&!잘못됨){unsigned 명령위치=현재위치-seto_waylude_etannde->명령열,hiisoore_njaru=oktee_keɓe();내보내기("L%u:;",명령위치);
        if(hiisoore_njaru==0){}
        else if(hiisoore_njaru==1)내보내기("P(0);");
        else if(hiisoore_njaru>=2&&hiisoore_njaru<=8)내보내기("P(%uU);",hiisoore_njaru-3);
        else if(hiisoore_njaru==16){int njaru=(int8_t)oktee_keɓe();내보내기("P(%uU);",(unsigned)njaru);}
        else if(hiisoore_njaru==17){int njaru=(int16_t)절반값();내보내기("P(%uU);",(unsigned)njaru);}
        else if(hiisoore_njaru==18||hiisoore_njaru==19)상수(hiisoore_njaru==18?oktee_keɓe():절반값());
        else if(hiisoore_njaru==21||hiisoore_njaru==25){unsigned 순번=oktee_keɓe();if(순번>=seto_waylude_etannde->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((hiisoore_njaru>=26&&hiisoore_njaru<=29)||(hiisoore_njaru>=42&&hiisoore_njaru<=45)){unsigned 순번=hiisoore_njaru>=42?hiisoore_njaru-42:hiisoore_njaru-26;if(순번>=seto_waylude_etannde->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(hiisoore_njaru==54||hiisoore_njaru==58){unsigned 순번=oktee_keɓe();if(순번>=seto_waylude_etannde->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((hiisoore_njaru>=59&&hiisoore_njaru<=62)||(hiisoore_njaru>=75&&hiisoore_njaru<=78)){unsigned 순번=hiisoore_njaru>=75?hiisoore_njaru-75:hiisoore_njaru-59;if(순번>=seto_waylude_etannde->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(hiisoore_njaru==46||hiisoore_njaru==50||hiisoore_njaru==51||hiisoore_njaru==52||hiisoore_njaru==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(hiisoore_njaru==79||hiisoore_njaru==83||hiisoore_njaru==84||hiisoore_njaru==85||hiisoore_njaru==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",hiisoore_njaru==84?"(unsigned)(signed char)q":hiisoore_njaru==85?"(unsigned short)q":hiisoore_njaru==86?"(unsigned)(short)q":"q");
        else if(hiisoore_njaru==87)내보내기("Q();");
        else if(hiisoore_njaru==89)내보내기("q=Q();P(q);P(q);");
        else if(hiisoore_njaru==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(hiisoore_njaru==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(hiisoore_njaru==96||hiisoore_njaru==100||hiisoore_njaru==104||hiisoore_njaru==120||hiisoore_njaru==124||hiisoore_njaru==126||hiisoore_njaru==128||hiisoore_njaru==130){const char*dokkagol_njaru=hiisoore_njaru==96?"+":hiisoore_njaru==100?"-":hiisoore_njaru==104?"*":hiisoore_njaru==120?"<<":hiisoore_njaru==124?">>":hiisoore_njaru==126?"&":hiisoore_njaru==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",dokkagol_njaru,hiisoore_njaru==120||hiisoore_njaru==124?"%32":"");}
        else if(hiisoore_njaru==108||hiisoore_njaru==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",hiisoore_njaru==112);
        else if(hiisoore_njaru==116)내보내기("P(0U-(unsigned)Q());");
        else if(hiisoore_njaru==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(hiisoore_njaru==132){unsigned 순번=oktee_keɓe();int 차이=(int8_t)oktee_keɓe();if(순번>=seto_waylude_etannde->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(hiisoore_njaru>=145&&hiisoore_njaru<=147)내보내기("P((unsigned)(%s)Q());",hiisoore_njaru==145?"signed char":hiisoore_njaru==146?"unsigned short":"short");
        else if(hiisoore_njaru>=153&&hiisoore_njaru<=166){int faandaare=(int)명령위치+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(faandaare<0||faandaare>=(int)seto_waylude_etannde->waylude_etannde){잘못됨=1;break;}if(hiisoore_njaru<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[hiisoore_njaru-153],faandaare);else if(hiisoore_njaru<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[hiisoore_njaru-159],faandaare);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",hiisoore_njaru==165?"==":"!=",faandaare);}
        else if(hiisoore_njaru==167){int faandaare=(int)명령위치+(int16_t)절반값();if(faandaare<0||faandaare>=(int)seto_waylude_etannde->waylude_etannde)잘못됨=1;내보내기("goto L%d;",faandaare);}
        else if(hiisoore_njaru==172||hiisoore_njaru==176)내보내기("return Q();");else if(hiisoore_njaru==177)내보내기("return 0;");
        else if(hiisoore_njaru==178||hiisoore_njaru==179){unsigned 식별자=절반값();if(식별자<1||식별자>=상수모음||Tage_Doggol[식별자]!=9||첫째값[식별자]>=상수모음||둘째값[식별자]>=상수모음||Tage_Doggol[첫째값[식별자]]!=7||Tage_Doggol[둘째값[식별자]]!=12){잘못됨=1;break;}unsigned 소유자=첫째값[첫째값[식별자]],innde=첫째값[둘째값[식별자]],서술값=둘째값[둘째값[식별자]];
            if(hiisoore_njaru==178&&Unicode_njaru(소유자,"java/lang/System")&&Unicode_njaru(innde,"out")&&Unicode_njaru(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned fiilde_naatnugol=0;while(fiilde_naatnugol<필드개수&&(!같음(innde,suudu_innde[fiilde_naatnugol])||!같음(서술값,필드서술[fiilde_naatnugol])))fiilde_naatnugol++;if(!같음(소유자,첫째값[현재클래스])||fiilde_naatnugol==필드개수){잘못됨=1;break;}내보내기(hiisoore_njaru==178?"P(fields[%u]);":"fields[%u]=Q();",fiilde_naatnugol);}}
        else if(hiisoore_njaru==182||hiisoore_njaru==184)호출(절반값(),hiisoore_njaru==182);
        else if(hiisoore_njaru==188){unsigned 유형=oktee_keɓe();if(유형!=4&&유형!=5&&유형!=8&&유형!=9&&유형!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(hiisoore_njaru==190)내보내기("P(jlength(Q()));");
        else if(hiisoore_njaru==198||hiisoore_njaru==199){int faandaare=(int)명령위치+(int16_t)절반값();if(faandaare<0||faandaare>=(int)seto_waylude_etannde->waylude_etannde)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",hiisoore_njaru==198?"==":"!=",faandaare);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",색인,hiisoore_njaru,명령위치);
        내보내기("\n");
    }
    njuuteendi_njaru=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned ɓoggol_ngootoñ(unsigned *자료위치,unsigned 끝위치){
    if(*자료위치>=끝위치){잘못됨=1;return 0;}unsigned 문자값=keɓe[(*자료위치)++];
    if(문자값<128)return 문자값;
    unsigned 개수=문자값>=0xc0&&문자값<=0xdf?1:문자값>=0xe0&&문자값<=0xef?2:3;
    if(개수==3||개수>끝위치-*자료위치){잘못됨=1;return 0;}unsigned njaru=문자값&((1u<<(6-개수))-1);
    for(unsigned 순번=0;순번<개수;순번++){unsigned 다음=keɓe[(*자료위치)++];if((다음&0xc0)!=0x80)잘못됨=1;njaru=njaru<<6|(다음&63);}
    if((개수==1&&njaru<128&&njaru!=0)||(개수==2&&njaru<2048))잘못됨=1;return njaru;
}
static void 문자열상수(unsigned 식별자){
    unsigned 부호없는값=첫째값[식별자];if(부호없는값<1||부호없는값>=상수모음||Tage_Doggol[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",식별자);
    unsigned 자료위치=첫째값[부호없는값],끝위치=자료위치+둘째값[부호없는값];
    while(자료위치<끝위치&&!잘못됨){unsigned 문자값=ɓoggol_ngootoñ(&자료위치,끝위치);
        if(문자값>=0xd800&&문자값<=0xdbff){unsigned 낮은부분=ɓoggol_ngootoñ(&자료위치,끝위치);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}문자값=0x10000+((문자값-0xd800)<<10)+낮은부분-0xdc00;}
        else if(문자값>=0xdc00&&문자값<=0xdfff){잘못됨=1;break;}
        if(!문자값){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(문자값<128)내보내기("%u,",문자값);
        else{unsigned 개수=문자값<2048?2:문자값<65536?3:4;내보내기("%u,",(개수==2?0xc0:개수==3?0xe0:0xf0)|(문자값>>(6*(개수-1))));for(unsigned 순번=개수-1;순번;순번--)내보내기("%u,",0x80|((문자값>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*innde){
    size_t 개수=strlen(innde);
    if(개수>4&&!strcmp(innde+개수-4,".jar")){
        if(꾸러미열기(innde)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char laawol[256];const char*진입함수=꾸러미진입클래스();개수=strlen(진입함수);if(개수+6>=sizeof(laawol))return 0;
        for(unsigned 순번=0;순번<개수;순번++)laawol[순번]=진입함수[순번]=='.'?'/':진입함수[순번];strcpy(laawol+개수,".class");int 항목수=꾸러미읽기(laawol,keɓe,sizeof(keɓe));if(항목수<0)return 0;njuuteendi_njaru=항목수;
    }else{intptr_t fiilde_jaggoode=사용자호출(3,(uintptr_t)innde,0,0,0,0,0);if(fiilde_jaggoode<0)return 0;intptr_t 항목수=사용자호출(9,fiilde_jaggoode,0,0,0,0,0);if(항목수<0||항목수>sizeof(keɓe)){사용자호출(4,fiilde_jaggoode,0,0,0,0,0);return 0;}intptr_t 받은수=사용자호출(2,fiilde_jaggoode,(uintptr_t)keɓe,항목수,0,0,0);사용자호출(4,fiilde_jaggoode,0,0,0,0,0);if(받은수!=항목수)return 0;njuuteendi_njaru=항목수;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(Tage_Doggol[순번]==8)문자열상수(순번);
    if(잘못됨)return 0;
    int naatnugol_toɓɓere=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!Unicode_njaru(메소드목록[순번].innde,"<init>")){
        int 결과,항목수=서술자(메소드목록[순번].서술값,&결과);if(항목수<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<항목수;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!항목수)내보내기("void");내보내기(");\n");
        if(Unicode_njaru(메소드목록[순번].innde,"main")&&Unicode_njaru(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)naatnugol_toɓɓere=순번;
        if(Unicode_njaru(메소드목록[순번].innde,"<clinit>"))초기값=순번;
    }
    if(naatnugol_toɓɓere<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)메소드번역(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(필드상수[순번]){
        unsigned 문자값=필드상수[순번];if(문자값>=상수모음)return 0;
        if(Tage_Doggol[문자값]==3)내보내기("fields[%u]=%uU;",순번,첫째값[문자값]);else if(Tage_Doggol[문자값]==8)내보내기("fields[%u]=(W)k%u;",순번,문자값);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",naatnugol_toɓɓere);
    return 잘못됨?0:binndi;
}
