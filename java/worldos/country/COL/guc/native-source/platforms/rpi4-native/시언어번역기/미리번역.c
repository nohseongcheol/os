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
static unsigned char atijaaya[16384];static unsigned akaliaa_ajutuu,현재위치;static int 잘못됨;
static unsigned 꼬리표들[512],첫째값[512],둘째값[512],상수모음,현재클래스;
static char 글[65536];static unsigned 글크기;
typedef struct {unsigned 설정비트,이름,서술값,명령열,크기,지역변수들,쌓임공간;} 메소드;
static 메소드 메소드목록[64];static unsigned 메소드개수;
static unsigned 필드이름[64],필드서술[64],apülajanaa_waneepiajutu[64],필드개수;
static unsigned 가져오기(unsigned 개수){if(현재위치>akaliaa_ajutuu||개수>akaliaa_ajutuu-현재위치){잘못됨=1;return 0;}unsigned 자료위치=현재위치;현재위치+=개수;return 자료위치;}
static unsigned waai_atijaaya(void){unsigned 자료위치=가져오기(1);return 잘못됨?0:atijaaya[자료위치];}
static unsigned 절반값(void){unsigned 가로좌표=waai_atijaaya();return 가로좌표<<8|waai_atijaaya();}
static uint32_t 가득참(void){uint32_t 가로좌표=절반값();return 가로좌표<<16|절반값();}
static int Unikoote_ajutuu(unsigned 순번,const char*kaleena_atijaaya){return 순번>0&&순번<상수모음&&꼬리표들[순번]==1&&strlen(kaleena_atijaaya)==둘째값[순번]&&!memcmp(atijaaya+첫째값[순번],kaleena_atijaaya,둘째값[순번]);}
static int 같음(unsigned 가로좌표,unsigned 세로좌표){return 가로좌표>0&&가로좌표<상수모음&&세로좌표>0&&세로좌표<상수모음&&꼬리표들[가로좌표]==1&&꼬리표들[세로좌표]==1&&둘째값[가로좌표]==둘째값[세로좌표]&&!memcmp(atijaaya+첫째값[가로좌표],atijaaya+첫째값[세로좌표],둘째값[가로좌표]);}
static void 내보내기(const char*anaajaalaa_ekeroliaa,...){if(잘못됨)return;va_list ajutuu_matüriisü;va_start(ajutuu_matüriisü,anaajaalaa_ekeroliaa);int 개수=vsnprintf(글+글크기,sizeof(글)-글크기,anaajaalaa_ekeroliaa,ajutuu_matüriisü);va_end(ajutuu_matüriisü);if(개수<0||(unsigned)개수>=sizeof(글)-글크기){잘못됨=1;return;}글크기+=개수;}
static int 서술자(unsigned 식별자,int*결과){
    if(식별자<1||식별자>=상수모음||꼬리표들[식별자]!=1)return -1;unsigned 자료위치=첫째값[식별자],끝위치=자료위치+둘째값[식별자];if(자료위치>=끝위치||atijaaya[자료위치++]!='(')return -1;int 항목수=0;
    while(자료위치<끝위치&&atijaaya[자료위치]!=')'){
        unsigned 문자값=atijaaya[자료위치++];while(문자값=='['&&자료위치<끝위치)문자값=atijaaya[자료위치++];
        if(문자값=='L'){while(자료위치<끝위치&&atijaaya[자료위치]!=';')자료위치++;if(자료위치==끝위치)return -1;자료위치++;}
        else if(문자값!='I'&&문자값!='Z'&&문자값!='B'&&문자값!='C'&&문자값!='S')return -1;
        if(++항목수>16)return -1;
    }
    if(자료위치+1>=끝위치||atijaaya[자료위치++]!=')')return -1;*결과=atijaaya[자료위치]=='V'?0:1;
    if(atijaaya[자료위치]=='J'||atijaaya[자료위치]=='D'||atijaaya[자료위치]=='F')return -1;return 항목수;
}
static void 속성들(void){unsigned 개수=절반값();for(unsigned 순번=0;순번<개수&&!잘못됨;순번++){절반값();unsigned 크기=가득참();가져오기(크기);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned 부버전=절반값(),판번호=절반값();if(부버전||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        꼬리표들[순번]=waai_atijaaya();switch(꼬리표들[순번]){
        case 1:둘째값[순번]=절반값();첫째값[순번]=가져오기(둘째값[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:가져오기(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();둘째값[순번]=절반값();break;
        case 15:첫째값[순번]=waai_atijaaya();둘째값[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||꼬리표들[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||꼬리표들[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();가져오기(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();필드이름[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned 항목수=절반값();for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned 이름=절반값(),크기=가득참();
            if(Unikoote_ajutuu(이름,"ConstantValue")){if(크기!=2)return -1;apülajanaa_waneepiajutu[순번]=절반값();}
            else 가져오기(크기);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        메소드*묶음수=메소드목록+순번;묶음수->설정비트=절반값();묶음수->이름=절반값();묶음수->서술값=절반값();unsigned 항목수=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned 이름=절반값(),크기=가득참(),시작=현재위치;
            if(크기>akaliaa_ajutuu-현재위치)return -1;
            if(Unikoote_ajutuu(이름,"Code")){
                묶음수->쌓임공간=절반값();묶음수->지역변수들=절반값();묶음수->크기=가득참();묶음수->명령열=가져오기(묶음수->크기);
                if(묶음수->쌓임공간>128||묶음수->지역변수들>128||묶음수->크기>8192||절반값())return -1;속성들();
            }else 가져오기(크기);
            if(현재위치!=시작+크기)return -1;
        }
        if(!Unikoote_ajutuu(묶음수->이름,"<init>")&&(!(묶음수->설정비트&8)||(묶음수->설정비트&(0x100|0x20))||!묶음수->크기))return -1;
    }
    속성들();return 잘못됨||현재위치!=akaliaa_ajutuu?-1:0;
}
static void waneepiajutu_ajutuu(unsigned 식별자){
    if(!식별자||식별자>=상수모음){잘못됨=1;return;}
    if(꼬리표들[식별자]==3)내보내기("P(%uU);",첫째값[식별자]);
    else if(꼬리표들[식별자]==8)내보내기("P((W)k%u);",식별자);else 잘못됨=1;
}
static void 호출(unsigned 식별자,int mepettujusalü_ounekaa){
    if(식별자<1||식별자>=상수모음||(꼬리표들[식별자]!=10&&꼬리표들[식별자]!=11)||첫째값[식별자]<1||첫째값[식별자]>=상수모음||꼬리표들[첫째값[식별자]]!=7||둘째값[식별자]<1||둘째값[식별자]>=상수모음||꼬리표들[둘째값[식별자]]!=12){잘못됨=1;return;}
    unsigned 소유자=첫째값[첫째값[식별자]],이름=첫째값[둘째값[식별자]],서술값=둘째값[둘째값[식별자]];int 결과=0,개수=서술자(서술값,&결과);if(개수<0){잘못됨=1;return;}
    for(int 순번=개수;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(mepettujusalü_ounekaa)내보내기("Q();");
    if(!mepettujusalü_ounekaa&&같음(소유자,첫째값[현재클래스])){
        unsigned 묶음수=0;for(;묶음수<메소드개수;묶음수++)if(같음(이름,메소드목록[묶음수].이름)&&같음(서술값,메소드목록[묶음수].서술값))break;
        if(묶음수==메소드개수||!(메소드목록[묶음수].설정비트&8)){잘못됨=1;return;}
        if(결과)내보내기("P(");내보내기("m%u(",묶음수);for(int 순번=0;순번<개수;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(결과?"));":" );");return;
    }
    if((mepettujusalü_ounekaa&&Unikoote_ajutuu(소유자,"java/io/PrintStream")&& (Unikoote_ajutuu(이름,"print")||Unikoote_ajutuu(이름,"println")))||(!mepettujusalü_ounekaa&&Unikoote_ajutuu(소유자,"한국어/자체/출력"))){
        if(Unikoote_ajutuu(서술값,"(I)V")&&(Unikoote_ajutuu(이름,"print")||Unikoote_ajutuu(이름,"println")||Unikoote_ajutuu(이름,"수쓰기"))){내보내기("jprint(x[0],1,%d);",Unikoote_ajutuu(이름,"print")?0:1);return;}
        if(Unikoote_ajutuu(서술값,"(Ljava/lang/String;)V")&&(Unikoote_ajutuu(이름,"print")||Unikoote_ajutuu(이름,"println")||Unikoote_ajutuu(이름,"ashajaa")||Unikoote_ajutuu(이름,"ashajaa_liinia"))){내보내기("jprint(x[0],0,%d);",Unikoote_ajutuu(이름,"print")||Unikoote_ajutuu(이름,"ashajaa")?0:1);return;}
        if(Unikoote_ajutuu(서술값,"()V")&&Unikoote_ajutuu(이름,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!mepettujusalü_ounekaa&&Unikoote_ajutuu(소유자,"한국어/자체/anaajaalaa")){
        if(Unikoote_ajutuu(이름,"ashajaa")&&Unikoote_ajutuu(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(Unikoote_ajutuu(이름,"읽기")&&Unikoote_ajutuu(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void 메소드번역(unsigned 색인){
    메소드*묶음수=메소드목록+색인;if(Unikoote_ajutuu(묶음수->이름,"<init>"))return;int 결과,개수=서술자(묶음수->서술값,&결과);if(개수<0){잘못됨=1;return;}
    내보내기("static W m%u(",색인);for(int 순번=0;순번<개수;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!개수)내보내기("void");
    if((unsigned)개수>묶음수->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",묶음수->지역변수들?묶음수->지역변수들:1);for(int 순번=0;순번<개수;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=akaliaa_ajutuu;akaliaa_ajutuu=묶음수->명령열+묶음수->크기;현재위치=묶음수->명령열;
    while(현재위치<akaliaa_ajutuu&&!잘못됨){unsigned 명령위치=현재위치-묶음수->명령열,akumajiraa_ajutuu=waai_atijaaya();내보내기("L%u:;",명령위치);
        if(akumajiraa_ajutuu==0){}
        else if(akumajiraa_ajutuu==1)내보내기("P(0);");
        else if(akumajiraa_ajutuu>=2&&akumajiraa_ajutuu<=8)내보내기("P(%uU);",akumajiraa_ajutuu-3);
        else if(akumajiraa_ajutuu==16){int ajutuu=(int8_t)waai_atijaaya();내보내기("P(%uU);",(unsigned)ajutuu);}
        else if(akumajiraa_ajutuu==17){int ajutuu=(int16_t)절반값();내보내기("P(%uU);",(unsigned)ajutuu);}
        else if(akumajiraa_ajutuu==18||akumajiraa_ajutuu==19)waneepiajutu_ajutuu(akumajiraa_ajutuu==18?waai_atijaaya():절반값());
        else if(akumajiraa_ajutuu==21||akumajiraa_ajutuu==25){unsigned 순번=waai_atijaaya();if(순번>=묶음수->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((akumajiraa_ajutuu>=26&&akumajiraa_ajutuu<=29)||(akumajiraa_ajutuu>=42&&akumajiraa_ajutuu<=45)){unsigned 순번=akumajiraa_ajutuu>=42?akumajiraa_ajutuu-42:akumajiraa_ajutuu-26;if(순번>=묶음수->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(akumajiraa_ajutuu==54||akumajiraa_ajutuu==58){unsigned 순번=waai_atijaaya();if(순번>=묶음수->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((akumajiraa_ajutuu>=59&&akumajiraa_ajutuu<=62)||(akumajiraa_ajutuu>=75&&akumajiraa_ajutuu<=78)){unsigned 순번=akumajiraa_ajutuu>=75?akumajiraa_ajutuu-75:akumajiraa_ajutuu-59;if(순번>=묶음수->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(akumajiraa_ajutuu==46||akumajiraa_ajutuu==50||akumajiraa_ajutuu==51||akumajiraa_ajutuu==52||akumajiraa_ajutuu==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(akumajiraa_ajutuu==79||akumajiraa_ajutuu==83||akumajiraa_ajutuu==84||akumajiraa_ajutuu==85||akumajiraa_ajutuu==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",akumajiraa_ajutuu==84?"(unsigned)(signed char)q":akumajiraa_ajutuu==85?"(unsigned short)q":akumajiraa_ajutuu==86?"(unsigned)(short)q":"q");
        else if(akumajiraa_ajutuu==87)내보내기("Q();");
        else if(akumajiraa_ajutuu==89)내보내기("q=Q();P(q);P(q);");
        else if(akumajiraa_ajutuu==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(akumajiraa_ajutuu==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(akumajiraa_ajutuu==96||akumajiraa_ajutuu==100||akumajiraa_ajutuu==104||akumajiraa_ajutuu==120||akumajiraa_ajutuu==124||akumajiraa_ajutuu==126||akumajiraa_ajutuu==128||akumajiraa_ajutuu==130){const char*atijitaalüjiaa_ajutuu=akumajiraa_ajutuu==96?"+":akumajiraa_ajutuu==100?"-":akumajiraa_ajutuu==104?"*":akumajiraa_ajutuu==120?"<<":akumajiraa_ajutuu==124?">>":akumajiraa_ajutuu==126?"&":akumajiraa_ajutuu==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",atijitaalüjiaa_ajutuu,akumajiraa_ajutuu==120||akumajiraa_ajutuu==124?"%32":"");}
        else if(akumajiraa_ajutuu==108||akumajiraa_ajutuu==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",akumajiraa_ajutuu==112);
        else if(akumajiraa_ajutuu==116)내보내기("P(0U-(unsigned)Q());");
        else if(akumajiraa_ajutuu==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(akumajiraa_ajutuu==132){unsigned 순번=waai_atijaaya();int 차이=(int8_t)waai_atijaaya();if(순번>=묶음수->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(akumajiraa_ajutuu>=145&&akumajiraa_ajutuu<=147)내보내기("P((unsigned)(%s)Q());",akumajiraa_ajutuu==145?"signed char":akumajiraa_ajutuu==146?"unsigned short":"short");
        else if(akumajiraa_ajutuu>=153&&akumajiraa_ajutuu<=166){int 대상=(int)명령위치+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(대상<0||대상>=(int)묶음수->크기){잘못됨=1;break;}if(akumajiraa_ajutuu<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[akumajiraa_ajutuu-153],대상);else if(akumajiraa_ajutuu<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[akumajiraa_ajutuu-159],대상);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",akumajiraa_ajutuu==165?"==":"!=",대상);}
        else if(akumajiraa_ajutuu==167){int 대상=(int)명령위치+(int16_t)절반값();if(대상<0||대상>=(int)묶음수->크기)잘못됨=1;내보내기("goto L%d;",대상);}
        else if(akumajiraa_ajutuu==172||akumajiraa_ajutuu==176)내보내기("return Q();");else if(akumajiraa_ajutuu==177)내보내기("return 0;");
        else if(akumajiraa_ajutuu==178||akumajiraa_ajutuu==179){unsigned 식별자=절반값();if(식별자<1||식별자>=상수모음||꼬리표들[식별자]!=9||첫째값[식별자]>=상수모음||둘째값[식별자]>=상수모음||꼬리표들[첫째값[식별자]]!=7||꼬리표들[둘째값[식별자]]!=12){잘못됨=1;break;}unsigned 소유자=첫째값[첫째값[식별자]],이름=첫째값[둘째값[식별자]],서술값=둘째값[둘째값[식별자]];
            if(akumajiraa_ajutuu==178&&Unikoote_ajutuu(소유자,"java/lang/System")&&Unikoote_ajutuu(이름,"out")&&Unikoote_ajutuu(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned anaajaalaa_ekeroliaa=0;while(anaajaalaa_ekeroliaa<필드개수&&(!같음(이름,필드이름[anaajaalaa_ekeroliaa])||!같음(서술값,필드서술[anaajaalaa_ekeroliaa])))anaajaalaa_ekeroliaa++;if(!같음(소유자,첫째값[현재클래스])||anaajaalaa_ekeroliaa==필드개수){잘못됨=1;break;}내보내기(akumajiraa_ajutuu==178?"P(fields[%u]);":"fields[%u]=Q();",anaajaalaa_ekeroliaa);}}
        else if(akumajiraa_ajutuu==182||akumajiraa_ajutuu==184)호출(절반값(),akumajiraa_ajutuu==182);
        else if(akumajiraa_ajutuu==188){unsigned 유형=waai_atijaaya();if(유형!=4&&유형!=5&&유형!=8&&유형!=9&&유형!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(akumajiraa_ajutuu==190)내보내기("P(jlength(Q()));");
        else if(akumajiraa_ajutuu==198||akumajiraa_ajutuu==199){int 대상=(int)명령위치+(int16_t)절반값();if(대상<0||대상>=(int)묶음수->크기)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",akumajiraa_ajutuu==198?"==":"!=",대상);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",색인,akumajiraa_ajutuu,명령위치);
        내보내기("\n");
    }
    akaliaa_ajutuu=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned 문자열단위(unsigned *자료위치,unsigned 끝위치){
    if(*자료위치>=끝위치){잘못됨=1;return 0;}unsigned 문자값=atijaaya[(*자료위치)++];
    if(문자값<128)return 문자값;
    unsigned 개수=문자값>=0xc0&&문자값<=0xdf?1:문자값>=0xe0&&문자값<=0xef?2:3;
    if(개수==3||개수>끝위치-*자료위치){잘못됨=1;return 0;}unsigned ajutuu=문자값&((1u<<(6-개수))-1);
    for(unsigned 순번=0;순번<개수;순번++){unsigned 다음=atijaaya[(*자료위치)++];if((다음&0xc0)!=0x80)잘못됨=1;ajutuu=ajutuu<<6|(다음&63);}
    if((개수==1&&ajutuu<128&&ajutuu!=0)||(개수==2&&ajutuu<2048))잘못됨=1;return ajutuu;
}
static void kaleena_waneepiajutu(unsigned 식별자){
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
const char *자바미리번역원문(const char*이름){
    size_t 개수=strlen(이름);
    if(개수>4&&!strcmp(이름+개수-4,".jar")){
        if(꾸러미열기(이름)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char wopu_a_ttaaleemüin[256];const char*진입함수=꾸러미진입클래스();개수=strlen(진입함수);if(개수+6>=sizeof(wopu_a_ttaaleemüin))return 0;
        for(unsigned 순번=0;순번<개수;순번++)wopu_a_ttaaleemüin[순번]=진입함수[순번]=='.'?'/':진입함수[순번];strcpy(wopu_a_ttaaleemüin+개수,".class");int 항목수=꾸러미읽기(wopu_a_ttaaleemüin,atijaaya,sizeof(atijaaya));if(항목수<0)return 0;akaliaa_ajutuu=항목수;
    }else{intptr_t anaajaalaa_aapaaya=사용자호출(3,(uintptr_t)이름,0,0,0,0,0);if(anaajaalaa_aapaaya<0)return 0;intptr_t 항목수=사용자호출(9,anaajaalaa_aapaaya,0,0,0,0,0);if(항목수<0||항목수>sizeof(atijaaya)){사용자호출(4,anaajaalaa_aapaaya,0,0,0,0,0);return 0;}intptr_t 받은수=사용자호출(2,anaajaalaa_aapaaya,(uintptr_t)atijaaya,항목수,0,0,0);사용자호출(4,anaajaalaa_aapaaya,0,0,0,0,0);if(받은수!=항목수)return 0;akaliaa_ajutuu=항목수;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(꼬리표들[순번]==8)kaleena_waneepiajutu(순번);
    if(잘못됨)return 0;
    int ekeroliaa_o_uchikanain=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!Unikoote_ajutuu(메소드목록[순번].이름,"<init>")){
        int 결과,항목수=서술자(메소드목록[순번].서술값,&결과);if(항목수<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<항목수;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!항목수)내보내기("void");내보내기(");\n");
        if(Unikoote_ajutuu(메소드목록[순번].이름,"main")&&Unikoote_ajutuu(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)ekeroliaa_o_uchikanain=순번;
        if(Unikoote_ajutuu(메소드목록[순번].이름,"<clinit>"))초기값=순번;
    }
    if(ekeroliaa_o_uchikanain<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)메소드번역(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(apülajanaa_waneepiajutu[순번]){
        unsigned 문자값=apülajanaa_waneepiajutu[순번];if(문자값>=상수모음)return 0;
        if(꼬리표들[문자값]==3)내보내기("fields[%u]=%uU;",순번,첫째값[문자값]);else if(꼬리표들[문자값]==8)내보내기("fields[%u]=(W)k%u;",순번,문자값);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",ekeroliaa_o_uchikanain);
    return 잘못됨?0:글;
}
