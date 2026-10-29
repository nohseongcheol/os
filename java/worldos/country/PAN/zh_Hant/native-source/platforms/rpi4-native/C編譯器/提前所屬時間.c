#include "../命名/計算機連接名稱列.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "調用.h"
#include "軟件包.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char 資料[16384];static unsigned 長度,當前位置;static int 是否無效;
static unsigned 標記列表[512],首位值[512],第二值[512],常量池,當前類別;
static char 文本[65536];static unsigned 文本大小;
typedef struct {unsigned 配置項位元列,名稱,描述符資料,指令序列,大小,局部變量列,棧存儲裝置;} 方法條目;
static 方法條目 已聲明方法列[64];static unsigned 已聲明方法個數;
static unsigned 字段名稱[64],字段描述符[64],字段常量[64],已聲明字段個數;
static unsigned 取用值(unsigned 項目個數){if(當前位置>長度||項目個數>長度-當前位置){是否無效=1;return 0;}unsigned 資料位置=當前位置;當前位置+=項目個數;return 資料位置;}
static unsigned 位元組資料(void){unsigned 資料位置=取用值(1);return 是否無效?0:資料[資料位置];}
static unsigned 一半值(void){unsigned 橫座標座標=位元組資料();return 橫座標座標<<8|位元組資料();}
static uint32_t 是否全滿(void){uint32_t 橫座標座標=一半值();return 橫座標座標<<16|一半值();}
static int Unicode值(unsigned 序數索引,const char*字符串資料){return 序數索引>0&&序數索引<常量池&&標記列表[序數索引]==1&&strlen(字符串資料)==第二值[序數索引]&&!memcmp(資料+首位值[序數索引],字符串資料,第二值[序數索引]);}
static int 相等文本(unsigned 橫座標座標,unsigned Y_按鈕座標){return 橫座標座標>0&&橫座標座標<常量池&&Y_按鈕座標>0&&Y_按鈕座標<常量池&&標記列表[橫座標座標]==1&&標記列表[Y_按鈕座標]==1&&第二值[橫座標座標]==第二值[Y_按鈕座標]&&!memcmp(資料+首位值[橫座標座標],資料+首位值[Y_按鈕座標],第二值[橫座標座標]);}
static void 發射值(const char*檔案條目,...){if(是否無效)return;va_list 實際參數陣列;va_start(實際參數陣列,檔案條目);int 項目個數=vsnprintf(文本+文本大小,sizeof(文本)-文本大小,檔案條目,實際參數陣列);va_end(實際參數陣列);if(項目個數<0||(unsigned)項目個數>=sizeof(文本)-文本大小){是否無效=1;return;}文本大小+=項目個數;}
static int 描述符條目(unsigned 標識符值,int*結果){
    if(標識符值<1||標識符值>=常量池||標記列表[標識符值]!=1)return -1;unsigned 資料位置=首位值[標識符值],結束偏移=資料位置+第二值[標識符值];if(資料位置>=結束偏移||資料[資料位置++]!='(')return -1;int 條目個數=0;
    while(資料位置<結束偏移&&資料[資料位置]!=')'){
        unsigned 字元程式碼=資料[資料位置++];while(字元程式碼=='['&&資料位置<結束偏移)字元程式碼=資料[資料位置++];
        if(字元程式碼=='L'){while(資料位置<結束偏移&&資料[資料位置]!=';')資料位置++;if(資料位置==結束偏移)return -1;資料位置++;}
        else if(字元程式碼!='I'&&字元程式碼!='Z'&&字元程式碼!='B'&&字元程式碼!='C'&&字元程式碼!='S')return -1;
        if(++條目個數>16)return -1;
    }
    if(資料位置+1>=結束偏移||資料[資料位置++]!=')')return -1;*結果=資料[資料位置]=='V'?0:1;
    if(資料[資料位置]=='J'||資料[資料位置]=='D'||資料[資料位置]=='F')return -1;return 條目個數;
}
static void 屬性集(void){unsigned 項目個數=一半值();for(unsigned 序數索引=0;序數索引<項目個數&&!是否無效;序數索引++){一半值();unsigned 大小=是否全滿();取用值(大小);}}
static int 解析輸入(void){
    if(是否全滿()!=0xcafebabe)return -1;unsigned 次版本版本=一半值(),版本編號=一半值();if(次版本版本||版本編號<45||版本編號>52)return -1;
    常量池=一半值();if(常量池<1||常量池>512)return -1;
    for(unsigned 序數索引=1;序數索引<常量池&&!是否無效;序數索引++){
        標記列表[序數索引]=位元組資料();switch(標記列表[序數索引]){
        case 1:第二值[序數索引]=一半值();首位值[序數索引]=取用值(第二值[序數索引]);break;case 3:case 4:首位值[序數索引]=是否全滿();break;
        case 5:case 6:取用值(8);if(++序數索引>=常量池)return -1;break;
        case 7:case 8:case 16:首位值[序數索引]=一半值();break;
        case 9:case 10:case 11:case 12:case 18:首位值[序數索引]=一半值();第二值[序數索引]=一半值();break;
        case 15:首位值[序數索引]=位元組資料();第二值[序數索引]=一半值();break;default:return -1;
        }
    }
    一半值();當前類別=一半值();一半值();if(當前類別<1||當前類別>=常量池||標記列表[當前類別]!=7||首位值[當前類別]<1||首位值[當前類別]>=常量池||標記列表[首位值[當前類別]]!=1)return -1;unsigned 接口列=一半值();取用值(接口列*2);
    已聲明字段個數=一半值();if(已聲明字段個數>64)return -1;
    for(unsigned 序數索引=0;序數索引<已聲明字段個數&&!是否無效;序數索引++){
        unsigned 配置項位元列=一半值();字段名稱[序數索引]=一半值();字段描述符[序數索引]=一半值();
        if(!(配置項位元列&8))return -1;
        unsigned 條目個數=一半值();for(unsigned 內部側序數=0;內部側序數<條目個數&&!是否無效;內部側序數++){
            unsigned 名稱=一半值(),大小=是否全滿();
            if(Unicode值(名稱,"ConstantValue")){if(大小!=2)return -1;字段常量[序數索引]=一半值();}
            else 取用值(大小);
        }
    }
    已聲明方法個數=一半值();if(已聲明方法個數>64)return -1;
    for(unsigned 序數索引=0;序數索引<已聲明方法個數&&!是否無效;序數索引++){
        方法條目*組大小=已聲明方法列+序數索引;組大小->配置項位元列=一半值();組大小->名稱=一半值();組大小->描述符資料=一半值();unsigned 條目個數=一半值();
        for(unsigned 內部側序數=0;內部側序數<條目個數&&!是否無效;內部側序數++){
            unsigned 名稱=一半值(),大小=是否全滿(),運行=當前位置;
            if(大小>長度-當前位置)return -1;
            if(Unicode值(名稱,"Code")){
                組大小->棧存儲裝置=一半值();組大小->局部變量列=一半值();組大小->大小=是否全滿();組大小->指令序列=取用值(組大小->大小);
                if(組大小->棧存儲裝置>128||組大小->局部變量列>128||組大小->大小>8192||一半值())return -1;屬性集();
            }else 取用值(大小);
            if(當前位置!=運行+大小)return -1;
        }
        if(!Unicode值(組大小->名稱,"<init>")&&(!(組大小->配置項位元列&8)||(組大小->配置項位元列&(0x100|0x20))||!組大小->大小))return -1;
    }
    屬性集();return 是否無效||當前位置!=長度?-1:0;
}
static void 常量值(unsigned 標識符值){
    if(!標識符值||標識符值>=常量池){是否無效=1;return;}
    if(標記列表[標識符值]==3)發射值("P(%uU);",首位值[標識符值]);
    else if(標記列表[標識符值]==8)發射值("P((W)k%u);",標識符值);else 是否無效=1;
}
static void 調用(unsigned 標識符值,int 虛擬呼叫){
    if(標識符值<1||標識符值>=常量池||(標記列表[標識符值]!=10&&標記列表[標識符值]!=11)||首位值[標識符值]<1||首位值[標識符值]>=常量池||標記列表[首位值[標識符值]]!=7||第二值[標識符值]<1||第二值[標識符值]>=常量池||標記列表[第二值[標識符值]]!=12){是否無效=1;return;}
    unsigned 所有者物件=首位值[首位值[標識符值]],名稱=首位值[第二值[標識符值]],描述符資料=第二值[第二值[標識符值]];int 結果=0,項目個數=描述符條目(描述符資料,&結果);if(項目個數<0){是否無效=1;return;}
    for(int 序數索引=項目個數;序數索引>0;序數索引--)發射值("x[%d]=Q();",序數索引-1);if(虛擬呼叫)發射值("Q();");
    if(!虛擬呼叫&&相等文本(所有者物件,首位值[當前類別])){
        unsigned 組大小=0;for(;組大小<已聲明方法個數;組大小++)if(相等文本(名稱,已聲明方法列[組大小].名稱)&&相等文本(描述符資料,已聲明方法列[組大小].描述符資料))break;
        if(組大小==已聲明方法個數||!(已聲明方法列[組大小].配置項位元列&8)){是否無效=1;return;}
        if(結果)發射值("P(");發射值("m%u(",組大小);for(int 序數索引=0;序數索引<項目個數;序數索引++)發射值(序數索引?",x[%d]":"x[%d]",序數索引);發射值(結果?"));":" );");return;
    }
    if((虛擬呼叫&&Unicode值(所有者物件,"java/io/PrintStream")&& (Unicode值(名稱,"print")||Unicode值(名稱,"println")))||(!虛擬呼叫&&Unicode值(所有者物件,"中文/內建/輸出"))){
        if(Unicode值(描述符資料,"(I)V")&&(Unicode值(名稱,"print")||Unicode值(名稱,"println")||Unicode值(名稱,"寫入編號"))){發射值("jprint(x[0],1,%d);",Unicode值(名稱,"print")?0:1);return;}
        if(Unicode值(描述符資料,"(Ljava/lang/String;)V")&&(Unicode值(名稱,"print")||Unicode值(名稱,"println")||Unicode值(名稱,"寫入")||Unicode值(名稱,"寫入行"))){發射值("jprint(x[0],0,%d);",Unicode值(名稱,"print")||Unicode值(名稱,"寫入")?0:1);return;}
        if(Unicode值(描述符資料,"()V")&&Unicode值(名稱,"println")){發射值("jprint((W)\"\",0,1);");return;}
    }
    if(!虛擬呼叫&&Unicode值(所有者物件,"中文/內建/檔案")){
        if(Unicode值(名稱,"寫入")&&Unicode值(描述符資料,"(Ljava/lang/String;Ljava/lang/String;)V")){發射值("jfwrite(x[0],x[1]);");return;}
        if(Unicode值(名稱,"讀取")&&Unicode值(描述符資料,"(Ljava/lang/String;)Ljava/lang/String;")){發射值("P(jfread(x[0]));");return;}
    }
    是否無效=1;
}
static void 編譯方法(unsigned 查找索引){
    方法條目*組大小=已聲明方法列+查找索引;if(Unicode值(組大小->名稱,"<init>"))return;int 結果,項目個數=描述符條目(組大小->描述符資料,&結果);if(項目個數<0){是否無效=1;return;}
    發射值("static W m%u(",查找索引);for(int 序數索引=0;序數索引<項目個數;序數索引++)發射值(序數索引?",W a%d":"W a%d",序數索引);if(!項目個數)發射值("void");
    if((unsigned)項目個數>組大小->局部變量列){是否無效=1;return;}
    發射值("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",組大小->局部變量列?組大小->局部變量列:1);for(int 序數索引=0;序數索引<項目個數;序數索引++)發射值("v[%d]=a%d;",序數索引,序數索引);
    unsigned 已保存=長度;長度=組大小->指令序列+組大小->大小;當前位置=組大小->指令序列;
    while(當前位置<長度&&!是否無效){unsigned 命令位置=當前位置-組大小->指令序列,操作值=位元組資料();發射值("L%u:;",命令位置);
        if(操作值==0){}
        else if(操作值==1)發射值("P(0);");
        else if(操作值>=2&&操作值<=8)發射值("P(%uU);",操作值-3);
        else if(操作值==16){int 值=(int8_t)位元組資料();發射值("P(%uU);",(unsigned)值);}
        else if(操作值==17){int 值=(int16_t)一半值();發射值("P(%uU);",(unsigned)值);}
        else if(操作值==18||操作值==19)常量值(操作值==18?位元組資料():一半值());
        else if(操作值==21||操作值==25){unsigned 序數索引=位元組資料();if(序數索引>=組大小->局部變量列)是否無效=1;發射值("P(v[%u]);",序數索引);}
        else if((操作值>=26&&操作值<=29)||(操作值>=42&&操作值<=45)){unsigned 序數索引=操作值>=42?操作值-42:操作值-26;if(序數索引>=組大小->局部變量列)是否無效=1;發射值("P(v[%u]);",序數索引);}
        else if(操作值==54||操作值==58){unsigned 序數索引=位元組資料();if(序數索引>=組大小->局部變量列)是否無效=1;發射值("v[%u]=Q();",序數索引);}
        else if((操作值>=59&&操作值<=62)||(操作值>=75&&操作值<=78)){unsigned 序數索引=操作值>=75?操作值-75:操作值-59;if(序數索引>=組大小->局部變量列)是否無效=1;發射值("v[%u]=Q();",序數索引);}
        else if(操作值==46||操作值==50||操作值==51||操作值==52||操作值==53)發射值("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(操作值==79||操作值==83||操作值==84||操作值==85||操作值==86)發射值("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",操作值==84?"(unsigned)(signed char)q":操作值==85?"(unsigned short)q":操作值==86?"(unsigned)(short)q":"q");
        else if(操作值==87)發射值("Q();");
        else if(操作值==89)發射值("q=Q();P(q);P(q);");
        else if(操作值==90)發射值("q=Q();r=Q();P(q);P(r);P(q);");
        else if(操作值==95)發射值("q=Q();r=Q();P(q);P(r);");
        else if(操作值==96||操作值==100||操作值==104||操作值==120||操作值==124||操作值==126||操作值==128||操作值==130){const char*編碼狀態值=操作值==96?"+":操作值==100?"-":操作值==104?"*":操作值==120?"<<":操作值==124?">>":操作值==126?"&":操作值==128?"|":"^";發射值("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",編碼狀態值,操作值==120||操作值==124?"%32":"");}
        else if(操作值==108||操作值==112)發射值("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",操作值==112);
        else if(操作值==116)發射值("P(0U-(unsigned)Q());");
        else if(操作值==122)發射值("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(操作值==132){unsigned 序數索引=位元組資料();int 差異值=(int8_t)位元組資料();if(序數索引>=組大小->局部變量列)是否無效=1;發射值("v[%u]=(unsigned)v[%u]+%uU;",序數索引,序數索引,(unsigned)差異值);}
        else if(操作值>=145&&操作值<=147)發射值("P((unsigned)(%s)Q());",操作值==145?"signed char":操作值==146?"unsigned short":"short");
        else if(操作值>=153&&操作值<=166){int 目標值=(int)命令位置+(int16_t)一半值();const char*比較值[]={"==","!=","<",">=",">","<="};if(目標值<0||目標值>=(int)組大小->大小){是否無效=1;break;}if(操作值<159)發射值("if((int)Q()%s0)goto L%d;",比較值[操作值-153],目標值);else if(操作值<165)發射值("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",比較值[操作值-159],目標值);else 發射值("q=Q();r=Q();if(r%sq)goto L%d;",操作值==165?"==":"!=",目標值);}
        else if(操作值==167){int 目標值=(int)命令位置+(int16_t)一半值();if(目標值<0||目標值>=(int)組大小->大小)是否無效=1;發射值("goto L%d;",目標值);}
        else if(操作值==172||操作值==176)發射值("return Q();");else if(操作值==177)發射值("return 0;");
        else if(操作值==178||操作值==179){unsigned 標識符值=一半值();if(標識符值<1||標識符值>=常量池||標記列表[標識符值]!=9||首位值[標識符值]>=常量池||第二值[標識符值]>=常量池||標記列表[首位值[標識符值]]!=7||標記列表[第二值[標識符值]]!=12){是否無效=1;break;}unsigned 所有者物件=首位值[首位值[標識符值]],名稱=首位值[第二值[標識符值]],描述符資料=第二值[第二值[標識符值]];
            if(操作值==178&&Unicode值(所有者物件,"java/lang/System")&&Unicode值(名稱,"out")&&Unicode值(描述符資料,"Ljava/io/PrintStream;"))發射值("P(1);");
            else {unsigned 檔案條目=0;while(檔案條目<已聲明字段個數&&(!相等文本(名稱,字段名稱[檔案條目])||!相等文本(描述符資料,字段描述符[檔案條目])))檔案條目++;if(!相等文本(所有者物件,首位值[當前類別])||檔案條目==已聲明字段個數){是否無效=1;break;}發射值(操作值==178?"P(fields[%u]);":"fields[%u]=Q();",檔案條目);}}
        else if(操作值==182||操作值==184)調用(一半值(),操作值==182);
        else if(操作值==188){unsigned 類型分類=位元組資料();if(類型分類!=4&&類型分類!=5&&類型分類!=8&&類型分類!=9&&類型分類!=10)是否無效=1;發射值("P(jarray((int)Q()));");}
        else if(操作值==190)發射值("P(jlength(Q()));");
        else if(操作值==198||操作值==199){int 目標值=(int)命令位置+(int16_t)一半值();if(目標值<0||目標值>=(int)組大小->大小)是否無效=1;發射值("if(Q()%s0)goto L%d;",操作值==198?"==":"!=",目標值);}
        else 是否無效=1;
        if(是否無效)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",查找索引,操作值,命令位置);
        發射值("\n");
    }
    長度=已保存;發射值("jfail();return 0;}\n");
}
static unsigned 字符串單位(unsigned *資料位置,unsigned 結束偏移){
    if(*資料位置>=結束偏移){是否無效=1;return 0;}unsigned 字元程式碼=資料[(*資料位置)++];
    if(字元程式碼<128)return 字元程式碼;
    unsigned 項目個數=字元程式碼>=0xc0&&字元程式碼<=0xdf?1:字元程式碼>=0xe0&&字元程式碼<=0xef?2:3;
    if(項目個數==3||項目個數>結束偏移-*資料位置){是否無效=1;return 0;}unsigned 值=字元程式碼&((1u<<(6-項目個數))-1);
    for(unsigned 序數索引=0;序數索引<項目個數;序數索引++){unsigned 下一項目=資料[(*資料位置)++];if((下一項目&0xc0)!=0x80)是否無效=1;值=值<<6|(下一項目&63);}
    if((項目個數==1&&值<128&&值!=0)||(項目個數==2&&值<2048))是否無效=1;return 值;
}
static void 字符串常量(unsigned 標識符值){
    unsigned 無符號值=首位值[標識符值];if(無符號值<1||無符號值>=常量池||標記列表[無符號值]!=1){是否無效=1;return;}發射值("static const unsigned char k%u[]={",標識符值);
    unsigned 資料位置=首位值[無符號值],結束偏移=資料位置+第二值[無符號值];
    while(資料位置<結束偏移&&!是否無效){unsigned 字元程式碼=字符串單位(&資料位置,結束偏移);
        if(字元程式碼>=0xd800&&字元程式碼<=0xdbff){unsigned 低位部分=字符串單位(&資料位置,結束偏移);if(低位部分<0xdc00||低位部分>0xdfff){是否無效=1;break;}字元程式碼=0x10000+((字元程式碼-0xd800)<<10)+低位部分-0xdc00;}
        else if(字元程式碼>=0xdc00&&字元程式碼<=0xdfff){是否無效=1;break;}
        if(!字元程式碼){printf("jaot: embedded NUL string needs JVM mode\n");是否無效=1;break;}
        if(字元程式碼<128)發射值("%u,",字元程式碼);
        else{unsigned 項目個數=字元程式碼<2048?2:字元程式碼<65536?3:4;發射值("%u,",(項目個數==2?0xc0:項目個數==3?0xe0:0xf0)|(字元程式碼>>(6*(項目個數-1))));for(unsigned 序數索引=項目個數-1;序數索引;序數索引--)發射值("%u,",0x80|((字元程式碼>>(6*(序數索引-1)))&63));}
    }發射值("0};\n");
}
const char *Java提前編譯原始碼(const char*名稱){
    size_t 項目個數=strlen(名稱);
    if(項目個數>4&&!strcmp(名稱+項目個數-4,".jar")){
        if(JAR打開(名稱)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char 路徑[256];const char*條目方法=JAR主操作();項目個數=strlen(條目方法);if(項目個數+6>=sizeof(路徑))return 0;
        for(unsigned 序數索引=0;序數索引<項目個數;序數索引++)路徑[序數索引]=條目方法[序數索引]=='.'?'/':條目方法[序數索引];strcpy(路徑+項目個數,".class");int 條目個數=JAR讀取(路徑,資料,sizeof(資料));if(條目個數<0)return 0;長度=條目個數;
    }else{intptr_t 檔案句柄=用戶調用(3,(uintptr_t)名稱,0,0,0,0,0);if(檔案句柄<0)return 0;intptr_t 條目個數=用戶調用(9,檔案句柄,0,0,0,0,0);if(條目個數<0||條目個數>sizeof(資料)){用戶調用(4,檔案句柄,0,0,0,0,0);return 0;}intptr_t 已接收個數=用戶調用(2,檔案句柄,(uintptr_t)資料,條目個數,0,0,0);用戶調用(4,檔案句柄,0,0,0,0,0);if(已接收個數!=條目個數)return 0;長度=條目個數;}
    if(解析輸入()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    發射值("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 序數索引=1;序數索引<常量池&&!是否無效;序數索引++)if(標記列表[序數索引]==8)字符串常量(序數索引);
    if(是否無效)return 0;
    int 條目分=-1,初始值=-1;
    for(unsigned 序數索引=0;序數索引<已聲明方法個數;序數索引++)if(!Unicode值(已聲明方法列[序數索引].名稱,"<init>")){
        int 結果,條目個數=描述符條目(已聲明方法列[序數索引].描述符資料,&結果);if(條目個數<0)return 0;發射值("static W m%u(",序數索引);for(int 內部側序數=0;內部側序數<條目個數;內部側序數++)發射值(內部側序數?",W":"W");if(!條目個數)發射值("void");發射值(");\n");
        if(Unicode值(已聲明方法列[序數索引].名稱,"main")&&Unicode值(已聲明方法列[序數索引].描述符資料,"([Ljava/lang/String;)V")&&(已聲明方法列[序數索引].配置項位元列&9)==9)條目分=序數索引;
        if(Unicode值(已聲明方法列[序數索引].名稱,"<clinit>"))初始值=序數索引;
    }
    if(條目分<0)return 0;for(unsigned 序數索引=0;序數索引<已聲明方法個數&&!是否無效;序數索引++)編譯方法(序數索引);
    發射值("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 序數索引=0;序數索引<已聲明字段個數;序數索引++)if(字段常量[序數索引]){
        unsigned 字元程式碼=字段常量[序數索引];if(字元程式碼>=常量池)return 0;
        if(標記列表[字元程式碼]==3)發射值("fields[%u]=%uU;",序數索引,首位值[字元程式碼]);else if(標記列表[字元程式碼]==8)發射值("fields[%u]=(W)k%u;",序數索引,字元程式碼);else return 0;
    }
    if(初始值>=0)發射值("m%d();",初始值);發射值("m%d((W)a);return 0;}\n",條目分);
    return 是否無效?0:文本;
}
