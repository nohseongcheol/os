#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "пакет.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char мәгълүмат[16384];static unsigned озынлык_VALUE,현재위치;static int 잘못됨;
static unsigned Тамгалар_Исемлек[512],첫째값[512],SECOND_VALUE[512],상수모음,현재클래스;
static char Mäten[65536];static unsigned текст_үлчәме;
typedef struct {unsigned 설정비트,исем,서술값,инструкция_SEQUENCE,үлчәмен_үзгәртү,지역변수들,Стәк_Саклагыч;} ысул_кертү;
static ысул_кертү 메소드목록[64];static unsigned 메소드개수;
static unsigned кыр_исеме[64],필드서술[64],кыр_константа[64],필드개수;
static unsigned TAKE_VALUE(unsigned элемент_COUNT){if(현재위치>озынлык_VALUE||элемент_COUNT>озынлык_VALUE-현재위치){잘못됨=1;return 0;}unsigned мәгълүмат_урнаштыру=현재위치;현재위치+=элемент_COUNT;return мәгълүмат_урнаштыру;}
static unsigned байт_мәгълүмат(void){unsigned мәгълүмат_урнаштыру=TAKE_VALUE(1);return 잘못됨?0:мәгълүмат[мәгълүмат_урнаштыру];}
static unsigned 절반값(void){unsigned X_координатасы=байт_мәгълүмат();return X_координатасы<<8|байт_мәгълүмат();}
static uint32_t 가득참(void){uint32_t X_координатасы=절반값();return X_координатасы<<16|절반값();}
static int Юникод_VALUE(unsigned 순번,const char*юл_мәгълүмат){return 순번>0&&순번<상수모음&&Тамгалар_Исемлек[순번]==1&&strlen(юл_мәгълүмат)==SECOND_VALUE[순번]&&!memcmp(мәгълүмат+첫째값[순번],юл_мәгълүмат,SECOND_VALUE[순번]);}
static int 같음(unsigned X_координатасы,unsigned 세로좌표){return X_координатасы>0&&X_координатасы<상수모음&&세로좌표>0&&세로좌표<상수모음&&Тамгалар_Исемлек[X_координатасы]==1&&Тамгалар_Исемлек[세로좌표]==1&&SECOND_VALUE[X_координатасы]==SECOND_VALUE[세로좌표]&&!memcmp(мәгълүмат+첫째값[X_координатасы],мәгълүмат+첫째값[세로좌표],SECOND_VALUE[X_координатасы]);}
static void 내보내기(const char*файл_кертү,...){if(잘못됨)return;va_list аргумент_МАССИВ;va_start(аргумент_МАССИВ,файл_кертү);int элемент_COUNT=vsnprintf(Mäten+текст_үлчәме,sizeof(Mäten)-текст_үлчәме,файл_кертү,аргумент_МАССИВ);va_end(аргумент_МАССИВ);if(элемент_COUNT<0||(unsigned)элемент_COUNT>=sizeof(Mäten)-текст_үлчәме){잘못됨=1;return;}текст_үлчәме+=элемент_COUNT;}
static int 서술자(unsigned күрсәткеч_VALUE,int*үлчәм){
    if(күрсәткеч_VALUE<1||күрсәткеч_VALUE>=상수모음||Тамгалар_Исемлек[күрсәткеч_VALUE]!=1)return -1;unsigned мәгълүмат_урнаштыру=첫째값[күрсәткеч_VALUE],тәмамлау_OFFSET=мәгълүмат_урнаштыру+SECOND_VALUE[күрсәткеч_VALUE];if(мәгълүмат_урнаштыру>=тәмамлау_OFFSET||мәгълүмат[мәгълүмат_урнаштыру++]!='(')return -1;int кертү_COUNT=0;
    while(мәгълүмат_урнаштыру<тәмамлау_OFFSET&&мәгълүмат[мәгълүмат_урнаштыру]!=')'){
        unsigned символ_коды=мәгълүмат[мәгълүмат_урнаштыру++];while(символ_коды=='['&&мәгълүмат_урнаштыру<тәмамлау_OFFSET)символ_коды=мәгълүмат[мәгълүмат_урнаштыру++];
        if(символ_коды=='L'){while(мәгълүмат_урнаштыру<тәмамлау_OFFSET&&мәгълүмат[мәгълүмат_урнаштыру]!=';')мәгълүмат_урнаштыру++;if(мәгълүмат_урнаштыру==тәмамлау_OFFSET)return -1;мәгълүмат_урнаштыру++;}
        else if(символ_коды!='I'&&символ_коды!='Z'&&символ_коды!='B'&&символ_коды!='C'&&символ_коды!='S')return -1;
        if(++кертү_COUNT>16)return -1;
    }
    if(мәгълүмат_урнаштыру+1>=тәмамлау_OFFSET||мәгълүмат[мәгълүмат_урнаштыру++]!=')')return -1;*үлчәм=мәгълүмат[мәгълүмат_урнаштыру]=='V'?0:1;
    if(мәгълүмат[мәгълүмат_урнаштыру]=='J'||мәгълүмат[мәгълүмат_урнаштыру]=='D'||мәгълүмат[мәгълүмат_урнаштыру]=='F')return -1;return кертү_COUNT;
}
static void 속성들(void){unsigned элемент_COUNT=절반값();for(unsigned 순번=0;순번<элемент_COUNT&&!잘못됨;순번++){절반값();unsigned үлчәмен_үзгәртү=가득참();TAKE_VALUE(үлчәмен_үзгәртү);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned балигъ_булмаган_версия=절반값(),판번호=절반값();if(балигъ_булмаган_версия||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        Тамгалар_Исемлек[순번]=байт_мәгълүмат();switch(Тамгалар_Исемлек[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=байт_мәгълүмат();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Тамгалар_Исемлек[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Тамгалар_Исемлек[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();кыр_исеме[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned кертү_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<кертү_COUNT&&!잘못됨;안쪽순번++){
            unsigned исем=절반값(),үлчәмен_үзгәртү=가득참();
            if(Юникод_VALUE(исем,"ConstantValue")){if(үлчәмен_үзгәртү!=2)return -1;кыр_константа[순번]=절반값();}
            else TAKE_VALUE(үлчәмен_үзгәртү);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        ысул_кертү*төркем_үлчәмен_үзгәртү=메소드목록+순번;төркем_үлчәмен_үзгәртү->설정비트=절반값();төркем_үлчәмен_үзгәртү->исем=절반값();төркем_үлчәмен_үзгәртү->서술값=절반값();unsigned кертү_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<кертү_COUNT&&!잘못됨;안쪽순번++){
            unsigned исем=절반값(),үлчәмен_үзгәртү=가득참(),эшләтү=현재위치;
            if(үлчәмен_үзгәртү>озынлык_VALUE-현재위치)return -1;
            if(Юникод_VALUE(исем,"Code")){
                төркем_үлчәмен_үзгәртү->Стәк_Саклагыч=절반값();төркем_үлчәмен_үзгәртү->지역변수들=절반값();төркем_үлчәмен_үзгәртү->үлчәмен_үзгәртү=가득참();төркем_үлчәмен_үзгәртү->инструкция_SEQUENCE=TAKE_VALUE(төркем_үлчәмен_үзгәртү->үлчәмен_үзгәртү);
                if(төркем_үлчәмен_үзгәртү->Стәк_Саклагыч>128||төркем_үлчәмен_үзгәртү->지역변수들>128||төркем_үлчәмен_үзгәртү->үлчәмен_үзгәртү>8192||절반값())return -1;속성들();
            }else TAKE_VALUE(үлчәмен_үзгәртү);
            if(현재위치!=эшләтү+үлчәмен_үзгәртү)return -1;
        }
        if(!Юникод_VALUE(төркем_үлчәмен_үзгәртү->исем,"<init>")&&(!(төркем_үлчәмен_үзгәртү->설정비트&8)||(төркем_үлчәмен_үзгәртү->설정비트&(0x100|0x20))||!төркем_үлчәмен_үзгәртү->үлчәмен_үзгәртү))return -1;
    }
    속성들();return 잘못됨||현재위치!=озынлык_VALUE?-1:0;
}
static void константа_VALUE(unsigned күрсәткеч_VALUE){
    if(!күрсәткеч_VALUE||күрсәткеч_VALUE>=상수모음){잘못됨=1;return;}
    if(Тамгалар_Исемлек[күрсәткеч_VALUE]==3)내보내기("P(%uU);",첫째값[күрсәткеч_VALUE]);
    else if(Тамгалар_Исемлек[күрсәткеч_VALUE]==8)내보내기("P((W)k%u);",күрсәткеч_VALUE);else 잘못됨=1;
}
static void 호출(unsigned күрсәткеч_VALUE,int виртуаль_CALL){
    if(күрсәткеч_VALUE<1||күрсәткеч_VALUE>=상수모음||(Тамгалар_Исемлек[күрсәткеч_VALUE]!=10&&Тамгалар_Исемлек[күрсәткеч_VALUE]!=11)||첫째값[күрсәткеч_VALUE]<1||첫째값[күрсәткеч_VALUE]>=상수모음||Тамгалар_Исемлек[첫째값[күрсәткеч_VALUE]]!=7||SECOND_VALUE[күрсәткеч_VALUE]<1||SECOND_VALUE[күрсәткеч_VALUE]>=상수모음||Тамгалар_Исемлек[SECOND_VALUE[күрсәткеч_VALUE]]!=12){잘못됨=1;return;}
    unsigned биләүче_объект=첫째값[첫째값[күрсәткеч_VALUE]],исем=첫째값[SECOND_VALUE[күрсәткеч_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[күрсәткеч_VALUE]];int үлчәм=0,элемент_COUNT=서술자(서술값,&үлчәм);if(элемент_COUNT<0){잘못됨=1;return;}
    for(int 순번=элемент_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(виртуаль_CALL)내보내기("Q();");
    if(!виртуаль_CALL&&같음(биләүче_объект,첫째값[현재클래스])){
        unsigned төркем_үлчәмен_үзгәртү=0;for(;төркем_үлчәмен_үзгәртү<메소드개수;төркем_үлчәмен_үзгәртү++)if(같음(исем,메소드목록[төркем_үлчәмен_үзгәртү].исем)&&같음(서술값,메소드목록[төркем_үлчәмен_үзгәртү].서술값))break;
        if(төркем_үлчәмен_үзгәртү==메소드개수||!(메소드목록[төркем_үлчәмен_үзгәртү].설정비트&8)){잘못됨=1;return;}
        if(үлчәм)내보내기("P(");내보내기("m%u(",төркем_үлчәмен_үзгәртү);for(int 순번=0;순번<элемент_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(үлчәм?"));":" );");return;
    }
    if((виртуаль_CALL&&Юникод_VALUE(биләүче_объект,"java/io/PrintStream")&& (Юникод_VALUE(исем,"print")||Юникод_VALUE(исем,"println")))||(!виртуаль_CALL&&Юникод_VALUE(биләүче_объект,"Татарча/자체/출력"))){
        if(Юникод_VALUE(서술값,"(I)V")&&(Юникод_VALUE(исем,"print")||Юникод_VALUE(исем,"println")||Юникод_VALUE(исем,"수쓰기"))){내보내기("jprint(x[0],1,%d);",Юникод_VALUE(исем,"print")?0:1);return;}
        if(Юникод_VALUE(서술값,"(Ljava/lang/String;)V")&&(Юникод_VALUE(исем,"print")||Юникод_VALUE(исем,"println")||Юникод_VALUE(исем,"язу")||Юникод_VALUE(исем,"язу_юл"))){내보내기("jprint(x[0],0,%d);",Юникод_VALUE(исем,"print")||Юникод_VALUE(исем,"язу")?0:1);return;}
        if(Юникод_VALUE(서술값,"()V")&&Юникод_VALUE(исем,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!виртуаль_CALL&&Юникод_VALUE(биләүче_объект,"Татарча/자체/Birem")){
        if(Юникод_VALUE(исем,"язу")&&Юникод_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(Юникод_VALUE(исем,"읽기")&&Юникод_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void төзү_ысул(unsigned Эзләү_INDEX){
    ысул_кертү*төркем_үлчәмен_үзгәртү=메소드목록+Эзләү_INDEX;if(Юникод_VALUE(төркем_үлчәмен_үзгәртү->исем,"<init>"))return;int үлчәм,элемент_COUNT=서술자(төркем_үлчәмен_үзгәртү->서술값,&үлчәм);if(элемент_COUNT<0){잘못됨=1;return;}
    내보내기("static W m%u(",Эзләү_INDEX);for(int 순번=0;순번<элемент_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!элемент_COUNT)내보내기("void");
    if((unsigned)элемент_COUNT>төркем_үлчәмен_үзгәртү->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",төркем_үлчәмен_үзгәртү->지역변수들?төркем_үлчәмен_үзгәртү->지역변수들:1);for(int 순번=0;순번<элемент_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=озынлык_VALUE;озынлык_VALUE=төркем_үлчәмен_үзгәртү->инструкция_SEQUENCE+төркем_үлчәмен_үзгәртү->үлчәмен_үзгәртү;현재위치=төркем_үлчәмен_үзгәртү->инструкция_SEQUENCE;
    while(현재위치<озынлык_VALUE&&!잘못됨){unsigned команда_урнаштыру=현재위치-төркем_үлчәмен_үзгәртү->инструкция_SEQUENCE,гамәл_VALUE=байт_мәгълүмат();내보내기("L%u:;",команда_урнаштыру);
        if(гамәл_VALUE==0){}
        else if(гамәл_VALUE==1)내보내기("P(0);");
        else if(гамәл_VALUE>=2&&гамәл_VALUE<=8)내보내기("P(%uU);",гамәл_VALUE-3);
        else if(гамәл_VALUE==16){int VALUE=(int8_t)байт_мәгълүмат();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(гамәл_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(гамәл_VALUE==18||гамәл_VALUE==19)константа_VALUE(гамәл_VALUE==18?байт_мәгълүмат():절반값());
        else if(гамәл_VALUE==21||гамәл_VALUE==25){unsigned 순번=байт_мәгълүмат();if(순번>=төркем_үлчәмен_үзгәртү->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((гамәл_VALUE>=26&&гамәл_VALUE<=29)||(гамәл_VALUE>=42&&гамәл_VALUE<=45)){unsigned 순번=гамәл_VALUE>=42?гамәл_VALUE-42:гамәл_VALUE-26;if(순번>=төркем_үлчәмен_үзгәртү->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(гамәл_VALUE==54||гамәл_VALUE==58){unsigned 순번=байт_мәгълүмат();if(순번>=төркем_үлчәмен_үзгәртү->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((гамәл_VALUE>=59&&гамәл_VALUE<=62)||(гамәл_VALUE>=75&&гамәл_VALUE<=78)){unsigned 순번=гамәл_VALUE>=75?гамәл_VALUE-75:гамәл_VALUE-59;if(순번>=төркем_үлчәмен_үзгәртү->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(гамәл_VALUE==46||гамәл_VALUE==50||гамәл_VALUE==51||гамәл_VALUE==52||гамәл_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(гамәл_VALUE==79||гамәл_VALUE==83||гамәл_VALUE==84||гамәл_VALUE==85||гамәл_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",гамәл_VALUE==84?"(unsigned)(signed char)q":гамәл_VALUE==85?"(unsigned short)q":гамәл_VALUE==86?"(unsigned)(short)q":"q");
        else if(гамәл_VALUE==87)내보내기("Q();");
        else if(гамәл_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(гамәл_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(гамәл_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(гамәл_VALUE==96||гамәл_VALUE==100||гамәл_VALUE==104||гамәл_VALUE==120||гамәл_VALUE==124||гамәл_VALUE==126||гамәл_VALUE==128||гамәл_VALUE==130){const char*кодлау_VALUE=гамәл_VALUE==96?"+":гамәл_VALUE==100?"-":гамәл_VALUE==104?"*":гамәл_VALUE==120?"<<":гамәл_VALUE==124?">>":гамәл_VALUE==126?"&":гамәл_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",кодлау_VALUE,гамәл_VALUE==120||гамәл_VALUE==124?"%32":"");}
        else if(гамәл_VALUE==108||гамәл_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",гамәл_VALUE==112);
        else if(гамәл_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(гамәл_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(гамәл_VALUE==132){unsigned 순번=байт_мәгълүмат();int 차이=(int8_t)байт_мәгълүмат();if(순번>=төркем_үлчәмен_үзгәртү->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(гамәл_VALUE>=145&&гамәл_VALUE<=147)내보내기("P((unsigned)(%s)Q());",гамәл_VALUE==145?"signed char":гамәл_VALUE==146?"unsigned short":"short");
        else if(гамәл_VALUE>=153&&гамәл_VALUE<=166){int максат_кыйммәт=(int)команда_урнаштыру+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(максат_кыйммәт<0||максат_кыйммәт>=(int)төркем_үлчәмен_үзгәртү->үлчәмен_үзгәртү){잘못됨=1;break;}if(гамәл_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[гамәл_VALUE-153],максат_кыйммәт);else if(гамәл_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[гамәл_VALUE-159],максат_кыйммәт);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",гамәл_VALUE==165?"==":"!=",максат_кыйммәт);}
        else if(гамәл_VALUE==167){int максат_кыйммәт=(int)команда_урнаштыру+(int16_t)절반값();if(максат_кыйммәт<0||максат_кыйммәт>=(int)төркем_үлчәмен_үзгәртү->үлчәмен_үзгәртү)잘못됨=1;내보내기("goto L%d;",максат_кыйммәт);}
        else if(гамәл_VALUE==172||гамәл_VALUE==176)내보내기("return Q();");else if(гамәл_VALUE==177)내보내기("return 0;");
        else if(гамәл_VALUE==178||гамәл_VALUE==179){unsigned күрсәткеч_VALUE=절반값();if(күрсәткеч_VALUE<1||күрсәткеч_VALUE>=상수모음||Тамгалар_Исемлек[күрсәткеч_VALUE]!=9||첫째값[күрсәткеч_VALUE]>=상수모음||SECOND_VALUE[күрсәткеч_VALUE]>=상수모음||Тамгалар_Исемлек[첫째값[күрсәткеч_VALUE]]!=7||Тамгалар_Исемлек[SECOND_VALUE[күрсәткеч_VALUE]]!=12){잘못됨=1;break;}unsigned биләүче_объект=첫째값[첫째값[күрсәткеч_VALUE]],исем=첫째값[SECOND_VALUE[күрсәткеч_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[күрсәткеч_VALUE]];
            if(гамәл_VALUE==178&&Юникод_VALUE(биләүче_объект,"java/lang/System")&&Юникод_VALUE(исем,"out")&&Юникод_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned файл_кертү=0;while(файл_кертү<필드개수&&(!같음(исем,кыр_исеме[файл_кертү])||!같음(서술값,필드서술[файл_кертү])))файл_кертү++;if(!같음(биләүче_объект,첫째값[현재클래스])||файл_кертү==필드개수){잘못됨=1;break;}내보내기(гамәл_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",файл_кертү);}}
        else if(гамәл_VALUE==182||гамәл_VALUE==184)호출(절반값(),гамәл_VALUE==182);
        else if(гамәл_VALUE==188){unsigned TYPE_категория=байт_мәгълүмат();if(TYPE_категория!=4&&TYPE_категория!=5&&TYPE_категория!=8&&TYPE_категория!=9&&TYPE_категория!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(гамәл_VALUE==190)내보내기("P(jlength(Q()));");
        else if(гамәл_VALUE==198||гамәл_VALUE==199){int максат_кыйммәт=(int)команда_урнаштыру+(int16_t)절반값();if(максат_кыйммәт<0||максат_кыйммәт>=(int)төркем_үлчәмен_үзгәртү->үлчәмен_үзгәртү)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",гамәл_VALUE==198?"==":"!=",максат_кыйммәт);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",Эзләү_INDEX,гамәл_VALUE,команда_урнаштыру);
        내보내기("\n");
    }
    озынлык_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned юл_дәрес(unsigned *мәгълүмат_урнаштыру,unsigned тәмамлау_OFFSET){
    if(*мәгълүмат_урнаштыру>=тәмамлау_OFFSET){잘못됨=1;return 0;}unsigned символ_коды=мәгълүмат[(*мәгълүмат_урнаштыру)++];
    if(символ_коды<128)return символ_коды;
    unsigned элемент_COUNT=символ_коды>=0xc0&&символ_коды<=0xdf?1:символ_коды>=0xe0&&символ_коды<=0xef?2:3;
    if(элемент_COUNT==3||элемент_COUNT>тәмамлау_OFFSET-*мәгълүмат_урнаштыру){잘못됨=1;return 0;}unsigned VALUE=символ_коды&((1u<<(6-элемент_COUNT))-1);
    for(unsigned 순번=0;순번<элемент_COUNT;순번++){unsigned Киләсе_элемент=мәгълүмат[(*мәгълүмат_урнаштыру)++];if((Киләсе_элемент&0xc0)!=0x80)잘못됨=1;VALUE=VALUE<<6|(Киләсе_элемент&63);}
    if((элемент_COUNT==1&&VALUE<128&&VALUE!=0)||(элемент_COUNT==2&&VALUE<2048))잘못됨=1;return VALUE;
}
static void юл_константа(unsigned күрсәткеч_VALUE){
    unsigned 부호없는값=첫째값[күрсәткеч_VALUE];if(부호없는값<1||부호없는값>=상수모음||Тамгалар_Исемлек[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",күрсәткеч_VALUE);
    unsigned мәгълүмат_урнаштыру=첫째값[부호없는값],тәмамлау_OFFSET=мәгълүмат_урнаштыру+SECOND_VALUE[부호없는값];
    while(мәгълүмат_урнаштыру<тәмамлау_OFFSET&&!잘못됨){unsigned символ_коды=юл_дәрес(&мәгълүмат_урнаштыру,тәмамлау_OFFSET);
        if(символ_коды>=0xd800&&символ_коды<=0xdbff){unsigned 낮은부분=юл_дәрес(&мәгълүмат_урнаштыру,тәмамлау_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}символ_коды=0x10000+((символ_коды-0xd800)<<10)+낮은부분-0xdc00;}
        else if(символ_коды>=0xdc00&&символ_коды<=0xdfff){잘못됨=1;break;}
        if(!символ_коды){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(символ_коды<128)내보내기("%u,",символ_коды);
        else{unsigned элемент_COUNT=символ_коды<2048?2:символ_коды<65536?3:4;내보내기("%u,",(элемент_COUNT==2?0xc0:элемент_COUNT==3?0xe0:0xf0)|(символ_коды>>(6*(элемент_COUNT-1))));for(unsigned 순번=элемент_COUNT-1;순번;순번--)내보내기("%u,",0x80|((символ_коды>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*исем){
    size_t элемент_COUNT=strlen(исем);
    if(элемент_COUNT>4&&!strcmp(исем+элемент_COUNT-4,".jar")){
        if(꾸러미열기(исем)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Yul[256];const char*кертү_ысул=꾸러미진입클래스();элемент_COUNT=strlen(кертү_ысул);if(элемент_COUNT+6>=sizeof(Yul))return 0;
        for(unsigned 순번=0;순번<элемент_COUNT;순번++)Yul[순번]=кертү_ысул[순번]=='.'?'/':кертү_ысул[순번];strcpy(Yul+элемент_COUNT,".class");int кертү_COUNT=꾸러미읽기(Yul,мәгълүмат,sizeof(мәгълүмат));if(кертү_COUNT<0)return 0;озынлык_VALUE=кертү_COUNT;
    }else{intptr_t файл_дескриптор=사용자호출(3,(uintptr_t)исем,0,0,0,0,0);if(файл_дескриптор<0)return 0;intptr_t кертү_COUNT=사용자호출(9,файл_дескриптор,0,0,0,0,0);if(кертү_COUNT<0||кертү_COUNT>sizeof(мәгълүмат)){사용자호출(4,файл_дескриптор,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,файл_дескриптор,(uintptr_t)мәгълүмат,кертү_COUNT,0,0,0);사용자호출(4,файл_дескриптор,0,0,0,0,0);if(RECEIVED_COUNT!=кертү_COUNT)return 0;озынлык_VALUE=кертү_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(Тамгалар_Исемлек[순번]==8)юл_константа(순번);
    if(잘못됨)return 0;
    int кертү_балл=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!Юникод_VALUE(메소드목록[순번].исем,"<init>")){
        int үлчәм,кертү_COUNT=서술자(메소드목록[순번].서술값,&үлчәм);if(кертү_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<кертү_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!кертү_COUNT)내보내기("void");내보내기(");\n");
        if(Юникод_VALUE(메소드목록[순번].исем,"main")&&Юникод_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)кертү_балл=순번;
        if(Юникод_VALUE(메소드목록[순번].исем,"<clinit>"))초기값=순번;
    }
    if(кертү_балл<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)төзү_ысул(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(кыр_константа[순번]){
        unsigned символ_коды=кыр_константа[순번];if(символ_коды>=상수모음)return 0;
        if(Тамгалар_Исемлек[символ_коды]==3)내보내기("fields[%u]=%uU;",순번,첫째값[символ_коды]);else if(Тамгалар_Исемлек[символ_коды]==8)내보내기("fields[%u]=(W)k%u;",순번,символ_коды);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",кертү_балл);
    return 잘못됨?0:Mäten;
}
