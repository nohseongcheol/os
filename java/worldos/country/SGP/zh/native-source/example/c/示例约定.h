#ifndef 原生示例头部
#define 原生示例头部
#include <文件ABI.h>
#include <屏幕ABI.h>
static int 文本长度(const char *文本) { int 长度=0;while(文本[长度])长度++;return 长度; }
static int 输出(const char *文本) { int 长度=文本长度(文本);return 写入文件数据(1,文本,长度)==长度?0:1; }
#endif
