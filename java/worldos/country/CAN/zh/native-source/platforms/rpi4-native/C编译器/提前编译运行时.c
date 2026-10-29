#include "../命名/计算机连接名称列.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "调用.h"
#include "文件ABI.h"
typedef unsigned long 计算机机器字;
static 计算机机器字 堆存储装置[8192];static unsigned 已使用容量;
void Java失败(void){const char 文本[]="AOT runtime error\n";写入文件数据(2,文本,sizeof(文本)-1);用户调用(6,1,0,0,0,0,0);for(;;){}}
void Java压栈(计算机机器字 *栈存储装置,int *深度值,计算机机器字 值){if(*深度值<0||*深度值>=128)Java失败();栈存储装置[(*深度值)++]=值;}
计算机机器字 Java弹栈值(计算机机器字 *栈存储装置,int *深度值){if(*深度值<=0||*深度值>128)Java失败();return 栈存储装置[--*深度值];}
计算机机器字 Java数组(int 项目个数){if(项目个数<0||(unsigned)项目个数+1>8192-已使用容量)Java失败();计算机机器字*数据位置=堆存储装置+已使用容量;已使用容量+=项目个数+1;数据位置[0]=项目个数;return (计算机机器字)数据位置;}
计算机机器字 *Java索引(计算机机器字 对象引用,int 项目个数){计算机机器字*数据位置=(计算机机器字*)对象引用;if(!数据位置||项目个数<0||(计算机机器字)项目个数>=数据位置[0])Java失败();return 数据位置+项目个数+1;}
int Java长度(计算机机器字 对象引用){if(!对象引用)Java失败();return *(计算机机器字*)对象引用;}
int Java除法(int 横坐标坐标,int Y_按钮坐标,int 余数值){if(!Y_按钮坐标)Java失败();if(横坐标坐标==(-2147483647-1)&&Y_按钮坐标==-1)return 余数值?0:横坐标坐标;return 余数值?横坐标坐标%Y_按钮坐标:横坐标坐标/Y_按钮坐标;}
static unsigned 长度(const char*字符串数据){unsigned 项目个数=0;if(!字符串数据)Java失败();while(字符串数据[项目个数])项目个数++;return 项目个数;}
void Java输出(计算机机器字 数据位置,int 数值值,int 换行){
    if(数值值){char 第二值[16];unsigned 项目个数=0;int 值=(int)数据位置;unsigned 无符号值=值<0?0-(unsigned)值:值;do{第二值[项目个数++]='0'+无符号值%10;无符号值/=10;}while(无符号值);if(值<0)第二值[项目个数++]='-';while(项目个数)写入文件数据(1,第二值+--项目个数,1);}
    else{const char*字符串数据=数据位置?(const char*)数据位置:"null";写入文件数据(1,字符串数据,长度(字符串数据));}if(换行)写入文件数据(1,"\n",1);
}
计算机机器字 Java文件写入(计算机机器字 路径,计算机机器字 值){const char*字符串数据=(const char*)值;unsigned 项目个数=长度(字符串数据);int 文件句柄=打开文件((const char*)路径,写入仅用值|创建条件缺失|截断内容,0600);if(文件句柄<0)Java失败();int 已返回值=写入文件数据(文件句柄,字符串数据,项目个数);关闭文件(文件句柄);if(已返回值!=(int)项目个数)Java失败();return 0;}
计算机机器字 Java文件读取(计算机机器字 路径){int 文件句柄=打开文件((const char*)路径,读取仅用值,0);if(文件句柄<0)Java失败();int 项目个数=文件大小(文件句柄);if(项目个数<0||项目个数>16384||(unsigned)(项目个数+8)/8>8192-已使用容量)Java失败();char*数据位置=(char*)(堆存储装置+已使用容量);已使用容量+=(项目个数+8)/8;int 已返回值=读取文件数据(文件句柄,数据位置,项目个数);关闭文件(文件句柄);if(已返回值!=项目个数)Java失败();数据位置[项目个数]=0;return (计算机机器字)数据位置;}
