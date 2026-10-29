#ifndef 原生网络头部
#define 原生网络头部
#include <stdint.h>
#include <stddef.h>
void 准备网络(void);
void 审查网络(void);
int 创建套接字端点(int 类型分类);
int 网络层绑定(int 文件句柄, uint32_t 地址, unsigned 端口编号);
int 网络层侦听(int 文件句柄);
void 复用套接字地址(int 文件句柄);
int 网络层连接(int 文件句柄, uint32_t 地址, unsigned 端口编号);
int 网络层接受(int 文件句柄);
int 网络层读取(int 文件句柄, void *数据, unsigned 项目个数);
int 网络层写入(int 文件句柄, const void *数据, unsigned 项目个数);
int 发送数据报(int 文件句柄, const void *数据, unsigned 项目个数, uint32_t 地址, unsigned 端口编号);
int 接收数据报(int 文件句柄, void *数据, unsigned 项目个数);
unsigned 网络端口编号(int 文件句柄);
unsigned 对端端口编号(int 文件句柄);
uint32_t 网络层对端地址(int 文件句柄);
void 关闭网络(int 文件句柄);
int 文件传送控制(int 动作);
void 审查文件传送(void);
uint32_t 读取网络运行状态(unsigned 条目值, unsigned 编号);
int 设定配置网络(unsigned 动作, uint32_t 地址, uint32_t 掩码值, uint32_t 网关值);
int 开始响应测试(uint32_t 地址, unsigned 排序值);
int 读取响应测试(unsigned 条目值);
#endif
