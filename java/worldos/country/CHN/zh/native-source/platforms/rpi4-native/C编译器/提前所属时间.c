#include "../命名/计算机连接名称列.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "调用.h"
#include "软件包.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char 数据[16384];static unsigned 长度,当前位置;static int 是否无效;
static unsigned 标记列表[512],首位值[512],第二值[512],常量池,当前类;
static char 文本[65536];static unsigned 文本大小;
typedef struct {unsigned 配置项位列,名称,描述符数据,指令序列,大小,局部变量列,栈存储装置;} 方法条目;
static 方法条目 已声明方法列[64];static unsigned 已声明方法个数;
static unsigned 字段名称[64],字段描述符[64],字段常量[64],已声明字段个数;
static unsigned 取用值(unsigned 项目个数){if(当前位置>长度||项目个数>长度-当前位置){是否无效=1;return 0;}unsigned 数据位置=当前位置;当前位置+=项目个数;return 数据位置;}
static unsigned 字节数据(void){unsigned 数据位置=取用值(1);return 是否无效?0:数据[数据位置];}
static unsigned 一半值(void){unsigned 横坐标坐标=字节数据();return 横坐标坐标<<8|字节数据();}
static uint32_t 是否全满(void){uint32_t 横坐标坐标=一半值();return 横坐标坐标<<16|一半值();}
static int Unicode值(unsigned 序数索引,const char*字符串数据){return 序数索引>0&&序数索引<常量池&&标记列表[序数索引]==1&&strlen(字符串数据)==第二值[序数索引]&&!memcmp(数据+首位值[序数索引],字符串数据,第二值[序数索引]);}
static int 相等文本(unsigned 横坐标坐标,unsigned Y_按钮坐标){return 横坐标坐标>0&&横坐标坐标<常量池&&Y_按钮坐标>0&&Y_按钮坐标<常量池&&标记列表[横坐标坐标]==1&&标记列表[Y_按钮坐标]==1&&第二值[横坐标坐标]==第二值[Y_按钮坐标]&&!memcmp(数据+首位值[横坐标坐标],数据+首位值[Y_按钮坐标],第二值[横坐标坐标]);}
static void 发射值(const char*文件条目,...){if(是否无效)return;va_list 参数数组;va_start(参数数组,文件条目);int 项目个数=vsnprintf(文本+文本大小,sizeof(文本)-文本大小,文件条目,参数数组);va_end(参数数组);if(项目个数<0||(unsigned)项目个数>=sizeof(文本)-文本大小){是否无效=1;return;}文本大小+=项目个数;}
static int 描述符条目(unsigned 标识符值,int*结果){
    if(标识符值<1||标识符值>=常量池||标记列表[标识符值]!=1)return -1;unsigned 数据位置=首位值[标识符值],结束偏移=数据位置+第二值[标识符值];if(数据位置>=结束偏移||数据[数据位置++]!='(')return -1;int 条目个数=0;
    while(数据位置<结束偏移&&数据[数据位置]!=')'){
        unsigned 字符代码=数据[数据位置++];while(字符代码=='['&&数据位置<结束偏移)字符代码=数据[数据位置++];
        if(字符代码=='L'){while(数据位置<结束偏移&&数据[数据位置]!=';')数据位置++;if(数据位置==结束偏移)return -1;数据位置++;}
        else if(字符代码!='I'&&字符代码!='Z'&&字符代码!='B'&&字符代码!='C'&&字符代码!='S')return -1;
        if(++条目个数>16)return -1;
    }
    if(数据位置+1>=结束偏移||数据[数据位置++]!=')')return -1;*结果=数据[数据位置]=='V'?0:1;
    if(数据[数据位置]=='J'||数据[数据位置]=='D'||数据[数据位置]=='F')return -1;return 条目个数;
}
static void 属性集(void){unsigned 项目个数=一半值();for(unsigned 序数索引=0;序数索引<项目个数&&!是否无效;序数索引++){一半值();unsigned 大小=是否全满();取用值(大小);}}
static int 解析输入(void){
    if(是否全满()!=0xcafebabe)return -1;unsigned 次版本版本=一半值(),版本编号=一半值();if(次版本版本||版本编号<45||版本编号>52)return -1;
    常量池=一半值();if(常量池<1||常量池>512)return -1;
    for(unsigned 序数索引=1;序数索引<常量池&&!是否无效;序数索引++){
        标记列表[序数索引]=字节数据();switch(标记列表[序数索引]){
        case 1:第二值[序数索引]=一半值();首位值[序数索引]=取用值(第二值[序数索引]);break;case 3:case 4:首位值[序数索引]=是否全满();break;
        case 5:case 6:取用值(8);if(++序数索引>=常量池)return -1;break;
        case 7:case 8:case 16:首位值[序数索引]=一半值();break;
        case 9:case 10:case 11:case 12:case 18:首位值[序数索引]=一半值();第二值[序数索引]=一半值();break;
        case 15:首位值[序数索引]=字节数据();第二值[序数索引]=一半值();break;default:return -1;
        }
    }
    一半值();当前类=一半值();一半值();if(当前类<1||当前类>=常量池||标记列表[当前类]!=7||首位值[当前类]<1||首位值[当前类]>=常量池||标记列表[首位值[当前类]]!=1)return -1;unsigned 接口列=一半值();取用值(接口列*2);
    已声明字段个数=一半值();if(已声明字段个数>64)return -1;
    for(unsigned 序数索引=0;序数索引<已声明字段个数&&!是否无效;序数索引++){
        unsigned 配置项位列=一半值();字段名称[序数索引]=一半值();字段描述符[序数索引]=一半值();
        if(!(配置项位列&8))return -1;
        unsigned 条目个数=一半值();for(unsigned 内部侧序数=0;内部侧序数<条目个数&&!是否无效;内部侧序数++){
            unsigned 名称=一半值(),大小=是否全满();
            if(Unicode值(名称,"ConstantValue")){if(大小!=2)return -1;字段常量[序数索引]=一半值();}
            else 取用值(大小);
        }
    }
    已声明方法个数=一半值();if(已声明方法个数>64)return -1;
    for(unsigned 序数索引=0;序数索引<已声明方法个数&&!是否无效;序数索引++){
        方法条目*组大小=已声明方法列+序数索引;组大小->配置项位列=一半值();组大小->名称=一半值();组大小->描述符数据=一半值();unsigned 条目个数=一半值();
        for(unsigned 内部侧序数=0;内部侧序数<条目个数&&!是否无效;内部侧序数++){
            unsigned 名称=一半值(),大小=是否全满(),运行=当前位置;
            if(大小>长度-当前位置)return -1;
            if(Unicode值(名称,"Code")){
                组大小->栈存储装置=一半值();组大小->局部变量列=一半值();组大小->大小=是否全满();组大小->指令序列=取用值(组大小->大小);
                if(组大小->栈存储装置>128||组大小->局部变量列>128||组大小->大小>8192||一半值())return -1;属性集();
            }else 取用值(大小);
            if(当前位置!=运行+大小)return -1;
        }
        if(!Unicode值(组大小->名称,"<init>")&&(!(组大小->配置项位列&8)||(组大小->配置项位列&(0x100|0x20))||!组大小->大小))return -1;
    }
    属性集();return 是否无效||当前位置!=长度?-1:0;
}
static void 常量值(unsigned 标识符值){
    if(!标识符值||标识符值>=常量池){是否无效=1;return;}
    if(标记列表[标识符值]==3)发射值("P(%uU);",首位值[标识符值]);
    else if(标记列表[标识符值]==8)发射值("P((W)k%u);",标识符值);else 是否无效=1;
}
static void 调用(unsigned 标识符值,int 虚拟调用){
    if(标识符值<1||标识符值>=常量池||(标记列表[标识符值]!=10&&标记列表[标识符值]!=11)||首位值[标识符值]<1||首位值[标识符值]>=常量池||标记列表[首位值[标识符值]]!=7||第二值[标识符值]<1||第二值[标识符值]>=常量池||标记列表[第二值[标识符值]]!=12){是否无效=1;return;}
    unsigned 所有者对象=首位值[首位值[标识符值]],名称=首位值[第二值[标识符值]],描述符数据=第二值[第二值[标识符值]];int 结果=0,项目个数=描述符条目(描述符数据,&结果);if(项目个数<0){是否无效=1;return;}
    for(int 序数索引=项目个数;序数索引>0;序数索引--)发射值("x[%d]=Q();",序数索引-1);if(虚拟调用)发射值("Q();");
    if(!虚拟调用&&相等文本(所有者对象,首位值[当前类])){
        unsigned 组大小=0;for(;组大小<已声明方法个数;组大小++)if(相等文本(名称,已声明方法列[组大小].名称)&&相等文本(描述符数据,已声明方法列[组大小].描述符数据))break;
        if(组大小==已声明方法个数||!(已声明方法列[组大小].配置项位列&8)){是否无效=1;return;}
        if(结果)发射值("P(");发射值("m%u(",组大小);for(int 序数索引=0;序数索引<项目个数;序数索引++)发射值(序数索引?",x[%d]":"x[%d]",序数索引);发射值(结果?"));":" );");return;
    }
    if((虚拟调用&&Unicode值(所有者对象,"java/io/PrintStream")&& (Unicode值(名称,"print")||Unicode值(名称,"println")))||(!虚拟调用&&Unicode值(所有者对象,"中文/内置/输出"))){
        if(Unicode值(描述符数据,"(I)V")&&(Unicode值(名称,"print")||Unicode值(名称,"println")||Unicode值(名称,"写入编号"))){发射值("jprint(x[0],1,%d);",Unicode值(名称,"print")?0:1);return;}
        if(Unicode值(描述符数据,"(Ljava/lang/String;)V")&&(Unicode值(名称,"print")||Unicode值(名称,"println")||Unicode值(名称,"写入")||Unicode值(名称,"写入行"))){发射值("jprint(x[0],0,%d);",Unicode值(名称,"print")||Unicode值(名称,"写入")?0:1);return;}
        if(Unicode值(描述符数据,"()V")&&Unicode值(名称,"println")){发射值("jprint((W)\"\",0,1);");return;}
    }
    if(!虚拟调用&&Unicode值(所有者对象,"中文/内置/文件")){
        if(Unicode值(名称,"写入")&&Unicode值(描述符数据,"(Ljava/lang/String;Ljava/lang/String;)V")){发射值("jfwrite(x[0],x[1]);");return;}
        if(Unicode值(名称,"读取")&&Unicode值(描述符数据,"(Ljava/lang/String;)Ljava/lang/String;")){发射值("P(jfread(x[0]));");return;}
    }
    是否无效=1;
}
static void 编译方法(unsigned 查找索引){
    方法条目*组大小=已声明方法列+查找索引;if(Unicode值(组大小->名称,"<init>"))return;int 结果,项目个数=描述符条目(组大小->描述符数据,&结果);if(项目个数<0){是否无效=1;return;}
    发射值("static W m%u(",查找索引);for(int 序数索引=0;序数索引<项目个数;序数索引++)发射值(序数索引?",W a%d":"W a%d",序数索引);if(!项目个数)发射值("void");
    if((unsigned)项目个数>组大小->局部变量列){是否无效=1;return;}
    发射值("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",组大小->局部变量列?组大小->局部变量列:1);for(int 序数索引=0;序数索引<项目个数;序数索引++)发射值("v[%d]=a%d;",序数索引,序数索引);
    unsigned 已保存=长度;长度=组大小->指令序列+组大小->大小;当前位置=组大小->指令序列;
    while(当前位置<长度&&!是否无效){unsigned 命令位置=当前位置-组大小->指令序列,操作值=字节数据();发射值("L%u:;",命令位置);
        if(操作值==0){}
        else if(操作值==1)发射值("P(0);");
        else if(操作值>=2&&操作值<=8)发射值("P(%uU);",操作值-3);
        else if(操作值==16){int 值=(int8_t)字节数据();发射值("P(%uU);",(unsigned)值);}
        else if(操作值==17){int 值=(int16_t)一半值();发射值("P(%uU);",(unsigned)值);}
        else if(操作值==18||操作值==19)常量值(操作值==18?字节数据():一半值());
        else if(操作值==21||操作值==25){unsigned 序数索引=字节数据();if(序数索引>=组大小->局部变量列)是否无效=1;发射值("P(v[%u]);",序数索引);}
        else if((操作值>=26&&操作值<=29)||(操作值>=42&&操作值<=45)){unsigned 序数索引=操作值>=42?操作值-42:操作值-26;if(序数索引>=组大小->局部变量列)是否无效=1;发射值("P(v[%u]);",序数索引);}
        else if(操作值==54||操作值==58){unsigned 序数索引=字节数据();if(序数索引>=组大小->局部变量列)是否无效=1;发射值("v[%u]=Q();",序数索引);}
        else if((操作值>=59&&操作值<=62)||(操作值>=75&&操作值<=78)){unsigned 序数索引=操作值>=75?操作值-75:操作值-59;if(序数索引>=组大小->局部变量列)是否无效=1;发射值("v[%u]=Q();",序数索引);}
        else if(操作值==46||操作值==50||操作值==51||操作值==52||操作值==53)发射值("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(操作值==79||操作值==83||操作值==84||操作值==85||操作值==86)发射值("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",操作值==84?"(unsigned)(signed char)q":操作值==85?"(unsigned short)q":操作值==86?"(unsigned)(short)q":"q");
        else if(操作值==87)发射值("Q();");
        else if(操作值==89)发射值("q=Q();P(q);P(q);");
        else if(操作值==90)发射值("q=Q();r=Q();P(q);P(r);P(q);");
        else if(操作值==95)发射值("q=Q();r=Q();P(q);P(r);");
        else if(操作值==96||操作值==100||操作值==104||操作值==120||操作值==124||操作值==126||操作值==128||操作值==130){const char*编码状态值=操作值==96?"+":操作值==100?"-":操作值==104?"*":操作值==120?"<<":操作值==124?">>":操作值==126?"&":操作值==128?"|":"^";发射值("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",编码状态值,操作值==120||操作值==124?"%32":"");}
        else if(操作值==108||操作值==112)发射值("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",操作值==112);
        else if(操作值==116)发射值("P(0U-(unsigned)Q());");
        else if(操作值==122)发射值("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(操作值==132){unsigned 序数索引=字节数据();int 差异值=(int8_t)字节数据();if(序数索引>=组大小->局部变量列)是否无效=1;发射值("v[%u]=(unsigned)v[%u]+%uU;",序数索引,序数索引,(unsigned)差异值);}
        else if(操作值>=145&&操作值<=147)发射值("P((unsigned)(%s)Q());",操作值==145?"signed char":操作值==146?"unsigned short":"short");
        else if(操作值>=153&&操作值<=166){int 目标值=(int)命令位置+(int16_t)一半值();const char*比较值[]={"==","!=","<",">=",">","<="};if(目标值<0||目标值>=(int)组大小->大小){是否无效=1;break;}if(操作值<159)发射值("if((int)Q()%s0)goto L%d;",比较值[操作值-153],目标值);else if(操作值<165)发射值("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",比较值[操作值-159],目标值);else 发射值("q=Q();r=Q();if(r%sq)goto L%d;",操作值==165?"==":"!=",目标值);}
        else if(操作值==167){int 目标值=(int)命令位置+(int16_t)一半值();if(目标值<0||目标值>=(int)组大小->大小)是否无效=1;发射值("goto L%d;",目标值);}
        else if(操作值==172||操作值==176)发射值("return Q();");else if(操作值==177)发射值("return 0;");
        else if(操作值==178||操作值==179){unsigned 标识符值=一半值();if(标识符值<1||标识符值>=常量池||标记列表[标识符值]!=9||首位值[标识符值]>=常量池||第二值[标识符值]>=常量池||标记列表[首位值[标识符值]]!=7||标记列表[第二值[标识符值]]!=12){是否无效=1;break;}unsigned 所有者对象=首位值[首位值[标识符值]],名称=首位值[第二值[标识符值]],描述符数据=第二值[第二值[标识符值]];
            if(操作值==178&&Unicode值(所有者对象,"java/lang/System")&&Unicode值(名称,"out")&&Unicode值(描述符数据,"Ljava/io/PrintStream;"))发射值("P(1);");
            else {unsigned 文件条目=0;while(文件条目<已声明字段个数&&(!相等文本(名称,字段名称[文件条目])||!相等文本(描述符数据,字段描述符[文件条目])))文件条目++;if(!相等文本(所有者对象,首位值[当前类])||文件条目==已声明字段个数){是否无效=1;break;}发射值(操作值==178?"P(fields[%u]);":"fields[%u]=Q();",文件条目);}}
        else if(操作值==182||操作值==184)调用(一半值(),操作值==182);
        else if(操作值==188){unsigned 类型分类=字节数据();if(类型分类!=4&&类型分类!=5&&类型分类!=8&&类型分类!=9&&类型分类!=10)是否无效=1;发射值("P(jarray((int)Q()));");}
        else if(操作值==190)发射值("P(jlength(Q()));");
        else if(操作值==198||操作值==199){int 目标值=(int)命令位置+(int16_t)一半值();if(目标值<0||目标值>=(int)组大小->大小)是否无效=1;发射值("if(Q()%s0)goto L%d;",操作值==198?"==":"!=",目标值);}
        else 是否无效=1;
        if(是否无效)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",查找索引,操作值,命令位置);
        发射值("\n");
    }
    长度=已保存;发射值("jfail();return 0;}\n");
}
static unsigned 字符串单位(unsigned *数据位置,unsigned 结束偏移){
    if(*数据位置>=结束偏移){是否无效=1;return 0;}unsigned 字符代码=数据[(*数据位置)++];
    if(字符代码<128)return 字符代码;
    unsigned 项目个数=字符代码>=0xc0&&字符代码<=0xdf?1:字符代码>=0xe0&&字符代码<=0xef?2:3;
    if(项目个数==3||项目个数>结束偏移-*数据位置){是否无效=1;return 0;}unsigned 值=字符代码&((1u<<(6-项目个数))-1);
    for(unsigned 序数索引=0;序数索引<项目个数;序数索引++){unsigned 下一项目=数据[(*数据位置)++];if((下一项目&0xc0)!=0x80)是否无效=1;值=值<<6|(下一项目&63);}
    if((项目个数==1&&值<128&&值!=0)||(项目个数==2&&值<2048))是否无效=1;return 值;
}
static void 字符串常量(unsigned 标识符值){
    unsigned 无符号值=首位值[标识符值];if(无符号值<1||无符号值>=常量池||标记列表[无符号值]!=1){是否无效=1;return;}发射值("static const unsigned char k%u[]={",标识符值);
    unsigned 数据位置=首位值[无符号值],结束偏移=数据位置+第二值[无符号值];
    while(数据位置<结束偏移&&!是否无效){unsigned 字符代码=字符串单位(&数据位置,结束偏移);
        if(字符代码>=0xd800&&字符代码<=0xdbff){unsigned 低位部分=字符串单位(&数据位置,结束偏移);if(低位部分<0xdc00||低位部分>0xdfff){是否无效=1;break;}字符代码=0x10000+((字符代码-0xd800)<<10)+低位部分-0xdc00;}
        else if(字符代码>=0xdc00&&字符代码<=0xdfff){是否无效=1;break;}
        if(!字符代码){printf("jaot: embedded NUL string needs JVM mode\n");是否无效=1;break;}
        if(字符代码<128)发射值("%u,",字符代码);
        else{unsigned 项目个数=字符代码<2048?2:字符代码<65536?3:4;发射值("%u,",(项目个数==2?0xc0:项目个数==3?0xe0:0xf0)|(字符代码>>(6*(项目个数-1))));for(unsigned 序数索引=项目个数-1;序数索引;序数索引--)发射值("%u,",0x80|((字符代码>>(6*(序数索引-1)))&63));}
    }发射值("0};\n");
}
const char *Java提前编译源代码(const char*名称){
    size_t 项目个数=strlen(名称);
    if(项目个数>4&&!strcmp(名称+项目个数-4,".jar")){
        if(JAR打开(名称)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char 路径[256];const char*条目方法=JAR主操作();项目个数=strlen(条目方法);if(项目个数+6>=sizeof(路径))return 0;
        for(unsigned 序数索引=0;序数索引<项目个数;序数索引++)路径[序数索引]=条目方法[序数索引]=='.'?'/':条目方法[序数索引];strcpy(路径+项目个数,".class");int 条目个数=JAR读取(路径,数据,sizeof(数据));if(条目个数<0)return 0;长度=条目个数;
    }else{intptr_t 文件句柄=用户调用(3,(uintptr_t)名称,0,0,0,0,0);if(文件句柄<0)return 0;intptr_t 条目个数=用户调用(9,文件句柄,0,0,0,0,0);if(条目个数<0||条目个数>sizeof(数据)){用户调用(4,文件句柄,0,0,0,0,0);return 0;}intptr_t 已接收个数=用户调用(2,文件句柄,(uintptr_t)数据,条目个数,0,0,0);用户调用(4,文件句柄,0,0,0,0,0);if(已接收个数!=条目个数)return 0;长度=条目个数;}
    if(解析输入()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    发射值("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 序数索引=1;序数索引<常量池&&!是否无效;序数索引++)if(标记列表[序数索引]==8)字符串常量(序数索引);
    if(是否无效)return 0;
    int 条目分=-1,初始值=-1;
    for(unsigned 序数索引=0;序数索引<已声明方法个数;序数索引++)if(!Unicode值(已声明方法列[序数索引].名称,"<init>")){
        int 结果,条目个数=描述符条目(已声明方法列[序数索引].描述符数据,&结果);if(条目个数<0)return 0;发射值("static W m%u(",序数索引);for(int 内部侧序数=0;内部侧序数<条目个数;内部侧序数++)发射值(内部侧序数?",W":"W");if(!条目个数)发射值("void");发射值(");\n");
        if(Unicode值(已声明方法列[序数索引].名称,"main")&&Unicode值(已声明方法列[序数索引].描述符数据,"([Ljava/lang/String;)V")&&(已声明方法列[序数索引].配置项位列&9)==9)条目分=序数索引;
        if(Unicode值(已声明方法列[序数索引].名称,"<clinit>"))初始值=序数索引;
    }
    if(条目分<0)return 0;for(unsigned 序数索引=0;序数索引<已声明方法个数&&!是否无效;序数索引++)编译方法(序数索引);
    发射值("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 序数索引=0;序数索引<已声明字段个数;序数索引++)if(字段常量[序数索引]){
        unsigned 字符代码=字段常量[序数索引];if(字符代码>=常量池)return 0;
        if(标记列表[字符代码]==3)发射值("fields[%u]=%uU;",序数索引,首位值[字符代码]);else if(标记列表[字符代码]==8)发射值("fields[%u]=(W)k%u;",序数索引,字符代码);else return 0;
    }
    if(初始值>=0)发射值("m%d();",初始值);发射值("m%d((W)a);return 0;}\n",条目分);
    return 是否无效?0:文本;
}
