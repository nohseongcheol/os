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
static unsigned char 자료[16384];static unsigned 길이,현재위치;static int 잘못됨;
static unsigned 꼬리표들[512],첫째값[512],둘째값[512],상수모음,현재클래스;
static char Soratra[65536];static unsigned 글크기;
typedef struct {unsigned 설정비트,Anarana,서술값,명령열,Habe,지역변수들,쌓임공간;} 메소드;
static 메소드 메소드목록[64];static unsigned 메소드개수;
static unsigned 필드이름[64],필드서술[64],필드상수[64],필드개수;
static unsigned 가져오기(unsigned 개수){if(현재위치>길이||개수>길이-현재위치){잘못됨=1;return 0;}unsigned 자료위치=현재위치;현재위치+=개수;return 자료위치;}
static unsigned 바이트값(void){unsigned 자료위치=가져오기(1);return 잘못됨?0:자료[자료위치];}
static unsigned 절반값(void){unsigned 가로좌표=바이트값();return 가로좌표<<8|바이트값();}
static uint32_t 가득참(void){uint32_t 가로좌표=절반값();return 가로좌표<<16|절반값();}
static int 유니코드(unsigned 순번,const char*문자열값){return 순번>0&&순번<상수모음&&꼬리표들[순번]==1&&strlen(문자열값)==둘째값[순번]&&!memcmp(자료+첫째값[순번],문자열값,둘째값[순번]);}
static int 같음(unsigned 가로좌표,unsigned 세로좌표){return 가로좌표>0&&가로좌표<상수모음&&세로좌표>0&&세로좌표<상수모음&&꼬리표들[가로좌표]==1&&꼬리표들[세로좌표]==1&&둘째값[가로좌표]==둘째값[세로좌표]&&!memcmp(자료+첫째값[가로좌표],자료+첫째값[세로좌표],둘째값[가로좌표]);}
static void 내보내기(const char*파일항목,...){if(잘못됨)return;va_list 인수배열;va_start(인수배열,파일항목);int 개수=vsnprintf(Soratra+글크기,sizeof(Soratra)-글크기,파일항목,인수배열);va_end(인수배열);if(개수<0||(unsigned)개수>=sizeof(Soratra)-글크기){잘못됨=1;return;}글크기+=개수;}
static int 서술자(unsigned 식별자,int*결과){
    if(식별자<1||식별자>=상수모음||꼬리표들[식별자]!=1)return -1;unsigned 자료위치=첫째값[식별자],끝위치=자료위치+둘째값[식별자];if(자료위치>=끝위치||자료[자료위치++]!='(')return -1;int 항목수=0;
    while(자료위치<끝위치&&자료[자료위치]!=')'){
        unsigned 문자값=자료[자료위치++];while(문자값=='['&&자료위치<끝위치)문자값=자료[자료위치++];
        if(문자값=='L'){while(자료위치<끝위치&&자료[자료위치]!=';')자료위치++;if(자료위치==끝위치)return -1;자료위치++;}
        else if(문자값!='I'&&문자값!='Z'&&문자값!='B'&&문자값!='C'&&문자값!='S')return -1;
        if(++항목수>16)return -1;
    }
    if(자료위치+1>=끝위치||자료[자료위치++]!=')')return -1;*결과=자료[자료위치]=='V'?0:1;
    if(자료[자료위치]=='J'||자료[자료위치]=='D'||자료[자료위치]=='F')return -1;return 항목수;
}
static void 속성들(void){unsigned 개수=절반값();for(unsigned 순번=0;순번<개수&&!잘못됨;순번++){절반값();unsigned Habe=가득참();가져오기(Habe);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned 부버전=절반값(),판번호=절반값();if(부버전||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        꼬리표들[순번]=바이트값();switch(꼬리표들[순번]){
        case 1:둘째값[순번]=절반값();첫째값[순번]=가져오기(둘째값[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:가져오기(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();둘째값[순번]=절반값();break;
        case 15:첫째값[순번]=바이트값();둘째값[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||꼬리표들[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||꼬리표들[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();가져오기(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();필드이름[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned 항목수=절반값();for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Anarana=절반값(),Habe=가득참();
            if(유니코드(Anarana,"ConstantValue")){if(Habe!=2)return -1;필드상수[순번]=절반값();}
            else 가져오기(Habe);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        메소드*묶음수=메소드목록+순번;묶음수->설정비트=절반값();묶음수->Anarana=절반값();묶음수->서술값=절반값();unsigned 항목수=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Anarana=절반값(),Habe=가득참(),Alefaso=현재위치;
            if(Habe>길이-현재위치)return -1;
            if(유니코드(Anarana,"Code")){
                묶음수->쌓임공간=절반값();묶음수->지역변수들=절반값();묶음수->Habe=가득참();묶음수->명령열=가져오기(묶음수->Habe);
                if(묶음수->쌓임공간>128||묶음수->지역변수들>128||묶음수->Habe>8192||절반값())return -1;속성들();
            }else 가져오기(Habe);
            if(현재위치!=Alefaso+Habe)return -1;
        }
        if(!유니코드(묶음수->Anarana,"<init>")&&(!(묶음수->설정비트&8)||(묶음수->설정비트&(0x100|0x20))||!묶음수->Habe))return -1;
    }
    속성들();return 잘못됨||현재위치!=길이?-1:0;
}
static void 상수(unsigned 식별자){
    if(!식별자||식별자>=상수모음){잘못됨=1;return;}
    if(꼬리표들[식별자]==3)내보내기("P(%uU);",첫째값[식별자]);
    else if(꼬리표들[식별자]==8)내보내기("P((W)k%u);",식별자);else 잘못됨=1;
}
static void 호출(unsigned 식별자,int 가상호출){
    if(식별자<1||식별자>=상수모음||(꼬리표들[식별자]!=10&&꼬리표들[식별자]!=11)||첫째값[식별자]<1||첫째값[식별자]>=상수모음||꼬리표들[첫째값[식별자]]!=7||둘째값[식별자]<1||둘째값[식별자]>=상수모음||꼬리표들[둘째값[식별자]]!=12){잘못됨=1;return;}
    unsigned 소유자=첫째값[첫째값[식별자]],Anarana=첫째값[둘째값[식별자]],서술값=둘째값[둘째값[식별자]];int 결과=0,개수=서술자(서술값,&결과);if(개수<0){잘못됨=1;return;}
    for(int 순번=개수;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(가상호출)내보내기("Q();");
    if(!가상호출&&같음(소유자,첫째값[현재클래스])){
        unsigned 묶음수=0;for(;묶음수<메소드개수;묶음수++)if(같음(Anarana,메소드목록[묶음수].Anarana)&&같음(서술값,메소드목록[묶음수].서술값))break;
        if(묶음수==메소드개수||!(메소드목록[묶음수].설정비트&8)){잘못됨=1;return;}
        if(결과)내보내기("P(");내보내기("m%u(",묶음수);for(int 순번=0;순번<개수;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(결과?"));":" );");return;
    }
    if((가상호출&&유니코드(소유자,"java/io/PrintStream")&& (유니코드(Anarana,"print")||유니코드(Anarana,"println")))||(!가상호출&&유니코드(소유자,"한국어/자체/출력"))){
        if(유니코드(서술값,"(I)V")&&(유니코드(Anarana,"print")||유니코드(Anarana,"println")||유니코드(Anarana,"수쓰기"))){내보내기("jprint(x[0],1,%d);",유니코드(Anarana,"print")?0:1);return;}
        if(유니코드(서술값,"(Ljava/lang/String;)V")&&(유니코드(Anarana,"print")||유니코드(Anarana,"println")||유니코드(Anarana,"Manoratra")||유니코드(Anarana,"줄쓰기"))){내보내기("jprint(x[0],0,%d);",유니코드(Anarana,"print")||유니코드(Anarana,"Manoratra")?0:1);return;}
        if(유니코드(서술값,"()V")&&유니코드(Anarana,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!가상호출&&유니코드(소유자,"한국어/자체/Rakitra")){
        if(유니코드(Anarana,"Manoratra")&&유니코드(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(유니코드(Anarana,"Mamaky")&&유니코드(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void 메소드번역(unsigned 색인){
    메소드*묶음수=메소드목록+색인;if(유니코드(묶음수->Anarana,"<init>"))return;int 결과,개수=서술자(묶음수->서술값,&결과);if(개수<0){잘못됨=1;return;}
    내보내기("static W m%u(",색인);for(int 순번=0;순번<개수;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!개수)내보내기("void");
    if((unsigned)개수>묶음수->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",묶음수->지역변수들?묶음수->지역변수들:1);for(int 순번=0;순번<개수;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=길이;길이=묶음수->명령열+묶음수->Habe;현재위치=묶음수->명령열;
    while(현재위치<길이&&!잘못됨){unsigned 명령위치=현재위치-묶음수->명령열,연산=바이트값();내보내기("L%u:;",명령위치);
        if(연산==0){}
        else if(연산==1)내보내기("P(0);");
        else if(연산>=2&&연산<=8)내보내기("P(%uU);",연산-3);
        else if(연산==16){int 값=(int8_t)바이트값();내보내기("P(%uU);",(unsigned)값);}
        else if(연산==17){int 값=(int16_t)절반값();내보내기("P(%uU);",(unsigned)값);}
        else if(연산==18||연산==19)상수(연산==18?바이트값():절반값());
        else if(연산==21||연산==25){unsigned 순번=바이트값();if(순번>=묶음수->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((연산>=26&&연산<=29)||(연산>=42&&연산<=45)){unsigned 순번=연산>=42?연산-42:연산-26;if(순번>=묶음수->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(연산==54||연산==58){unsigned 순번=바이트값();if(순번>=묶음수->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((연산>=59&&연산<=62)||(연산>=75&&연산<=78)){unsigned 순번=연산>=75?연산-75:연산-59;if(순번>=묶음수->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(연산==46||연산==50||연산==51||연산==52||연산==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(연산==79||연산==83||연산==84||연산==85||연산==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",연산==84?"(unsigned)(signed char)q":연산==85?"(unsigned short)q":연산==86?"(unsigned)(short)q":"q");
        else if(연산==87)내보내기("Q();");
        else if(연산==89)내보내기("q=Q();P(q);P(q);");
        else if(연산==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(연산==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(연산==96||연산==100||연산==104||연산==120||연산==124||연산==126||연산==128||연산==130){const char*부호=연산==96?"+":연산==100?"-":연산==104?"*":연산==120?"<<":연산==124?">>":연산==126?"&":연산==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",부호,연산==120||연산==124?"%32":"");}
        else if(연산==108||연산==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",연산==112);
        else if(연산==116)내보내기("P(0U-(unsigned)Q());");
        else if(연산==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(연산==132){unsigned 순번=바이트값();int 차이=(int8_t)바이트값();if(순번>=묶음수->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(연산>=145&&연산<=147)내보내기("P((unsigned)(%s)Q());",연산==145?"signed char":연산==146?"unsigned short":"short");
        else if(연산>=153&&연산<=166){int 대상=(int)명령위치+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(대상<0||대상>=(int)묶음수->Habe){잘못됨=1;break;}if(연산<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[연산-153],대상);else if(연산<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[연산-159],대상);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",연산==165?"==":"!=",대상);}
        else if(연산==167){int 대상=(int)명령위치+(int16_t)절반값();if(대상<0||대상>=(int)묶음수->Habe)잘못됨=1;내보내기("goto L%d;",대상);}
        else if(연산==172||연산==176)내보내기("return Q();");else if(연산==177)내보내기("return 0;");
        else if(연산==178||연산==179){unsigned 식별자=절반값();if(식별자<1||식별자>=상수모음||꼬리표들[식별자]!=9||첫째값[식별자]>=상수모음||둘째값[식별자]>=상수모음||꼬리표들[첫째값[식별자]]!=7||꼬리표들[둘째값[식별자]]!=12){잘못됨=1;break;}unsigned 소유자=첫째값[첫째값[식별자]],Anarana=첫째값[둘째값[식별자]],서술값=둘째값[둘째값[식별자]];
            if(연산==178&&유니코드(소유자,"java/lang/System")&&유니코드(Anarana,"out")&&유니코드(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned 파일항목=0;while(파일항목<필드개수&&(!같음(Anarana,필드이름[파일항목])||!같음(서술값,필드서술[파일항목])))파일항목++;if(!같음(소유자,첫째값[현재클래스])||파일항목==필드개수){잘못됨=1;break;}내보내기(연산==178?"P(fields[%u]);":"fields[%u]=Q();",파일항목);}}
        else if(연산==182||연산==184)호출(절반값(),연산==182);
        else if(연산==188){unsigned 유형=바이트값();if(유형!=4&&유형!=5&&유형!=8&&유형!=9&&유형!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(연산==190)내보내기("P(jlength(Q()));");
        else if(연산==198||연산==199){int 대상=(int)명령위치+(int16_t)절반값();if(대상<0||대상>=(int)묶음수->Habe)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",연산==198?"==":"!=",대상);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",색인,연산,명령위치);
        내보내기("\n");
    }
    길이=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned 문자열단위(unsigned *자료위치,unsigned 끝위치){
    if(*자료위치>=끝위치){잘못됨=1;return 0;}unsigned 문자값=자료[(*자료위치)++];
    if(문자값<128)return 문자값;
    unsigned 개수=문자값>=0xc0&&문자값<=0xdf?1:문자값>=0xe0&&문자값<=0xef?2:3;
    if(개수==3||개수>끝위치-*자료위치){잘못됨=1;return 0;}unsigned 값=문자값&((1u<<(6-개수))-1);
    for(unsigned 순번=0;순번<개수;순번++){unsigned 다음=자료[(*자료위치)++];if((다음&0xc0)!=0x80)잘못됨=1;값=값<<6|(다음&63);}
    if((개수==1&&값<128&&값!=0)||(개수==2&&값<2048))잘못됨=1;return 값;
}
static void 문자열상수(unsigned 식별자){
    unsigned 부호없는값=첫째값[식별자];if(부호없는값<1||부호없는값>=상수모음||꼬리표들[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",식별자);
    unsigned 자료위치=첫째값[부호없는값],끝위치=자료위치+둘째값[부호없는값];
    while(자료위치<끝위치&&!잘못됨){unsigned 문자값=문자열단위(&자료위치,끝위치);
        if(문자값>=0xd800&&문자값<=0xdbff){unsigned 낮은부분=문자열단위(&자료위치,끝위치);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}문자값=0x10000+((문자값-0xd800)<<10)+낮은부분-0xdc00;}
        else if(문자값>=0xdc00&&문자값<=0xdfff){잘못됨=1;break;}
        if(!문자값){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(문자값<128)내보내기("%u,",문자값);
        else{unsigned 개수=문자값<2048?2:문자값<65536?3:4;내보내기("%u,",(개수==2?0xc0:개수==3?0xe0:0xf0)|(문자값>>(6*(개수-1))));for(unsigned 순번=개수-1;순번;순번--)내보내기("%u,",0x80|((문자값>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Anarana){
    size_t 개수=strlen(Anarana);
    if(개수>4&&!strcmp(Anarana+개수-4,".jar")){
        if(꾸러미열기(Anarana)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char LALANA[256];const char*진입함수=꾸러미진입클래스();개수=strlen(진입함수);if(개수+6>=sizeof(LALANA))return 0;
        for(unsigned 순번=0;순번<개수;순번++)LALANA[순번]=진입함수[순번]=='.'?'/':진입함수[순번];strcpy(LALANA+개수,".class");int 항목수=꾸러미읽기(LALANA,자료,sizeof(자료));if(항목수<0)return 0;길이=항목수;
    }else{intptr_t 파일기술자=사용자호출(3,(uintptr_t)Anarana,0,0,0,0,0);if(파일기술자<0)return 0;intptr_t 항목수=사용자호출(9,파일기술자,0,0,0,0,0);if(항목수<0||항목수>sizeof(자료)){사용자호출(4,파일기술자,0,0,0,0,0);return 0;}intptr_t 받은수=사용자호출(2,파일기술자,(uintptr_t)자료,항목수,0,0,0);사용자호출(4,파일기술자,0,0,0,0,0);if(받은수!=항목수)return 0;길이=항목수;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(꼬리표들[순번]==8)문자열상수(순번);
    if(잘못됨)return 0;
    int 진입점=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!유니코드(메소드목록[순번].Anarana,"<init>")){
        int 결과,항목수=서술자(메소드목록[순번].서술값,&결과);if(항목수<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<항목수;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!항목수)내보내기("void");내보내기(");\n");
        if(유니코드(메소드목록[순번].Anarana,"main")&&유니코드(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)진입점=순번;
        if(유니코드(메소드목록[순번].Anarana,"<clinit>"))초기값=순번;
    }
    if(진입점<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)메소드번역(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(필드상수[순번]){
        unsigned 문자값=필드상수[순번];if(문자값>=상수모음)return 0;
        if(꼬리표들[문자값]==3)내보내기("fields[%u]=%uU;",순번,첫째값[문자값]);else if(꼬리표들[문자값]==8)내보내기("fields[%u]=(W)k%u;",순번,문자값);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",진입점);
    return 잘못됨?0:Soratra;
}
