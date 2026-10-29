// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "调用.h"
#include "网络ABI.h"
static intptr_t 已检查(intptr_t 结果) { if (结果 < 0) mp_raise_OSError(-结果); return 结果; }
static const char *路径参数(mp_obj_t 值) {
    size_t 项目个数; const char *路径 = mp_obj_str_get_data(值, &项目个数);
    if (!项目个数 || 项目个数 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 序数索引 = 0; 序数索引 < 项目个数; 序数索引++) if (!路径[序数索引]) mp_raise_OSError(MP_EINVAL);
    return 路径;
}
static mp_obj_t 读取文件(mp_obj_t 名称) {
    intptr_t 文件句柄 = 已检查(用户调用(3, (uintptr_t)路径参数(名称), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 非局部发回;
    if (nlr_push(&非局部发回) == 0) {
        size_t 大小 = 已检查(用户调用(9, 文件句柄, 0, 0, 0, 0, 0));
        vstr_t 数据; vstr_init_len(&数据, 大小);
        intptr_t 结果 = 用户调用(2, 文件句柄, (uintptr_t)数据.buf, 大小, 0, 0, 0);
        已检查(结果); 数据.len = 结果;
        mp_obj_t 值 = mp_obj_new_bytes_from_vstr(&数据);
        nlr_pop(); 用户调用(4, 文件句柄, 0, 0, 0, 0, 0); return 值;
    }
    用户调用(4, 文件句柄, 0, 0, 0, 0, 0); nlr_jump(非局部发回.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(文件读取器对象, 读取文件);
static mp_obj_t 读取标准输入(mp_obj_t 容量限制) {
    mp_int_t 大小=mp_obj_get_int(容量限制);
    if(大小<0||大小>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t 数据; vstr_init_len(&数据,大小);
    intptr_t 项目个数=用户调用(2,0,(uintptr_t)数据.buf,大小,0,0,0);
    if(项目个数<0) { vstr_clear(&数据); 已检查(项目个数); }
    数据.len=项目个数; return mp_obj_new_bytes_from_vstr(&数据);
}
static MP_DEFINE_CONST_FUN_OBJ_1(标准输入读取器对象, 读取标准输入);
static mp_obj_t 写入文件(mp_obj_t 名称, mp_obj_t 内容值) {
    const char *路径 = 路径参数(名称);
    mp_buffer_info_t 数据; mp_get_buffer_raise(内容值, &数据, MP_BUFFER_READ);
    if (数据.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t 文件句柄 = 已检查(用户调用(3, (uintptr_t)路径, 577, 0, 0, 0, 0));
    intptr_t 条目个数 = 用户调用(1, 文件句柄, (uintptr_t)数据.buf, 数据.len, 0, 0, 0);
    用户调用(4, 文件句柄, 0, 0, 0, 0, 0); return mp_obj_new_int(已检查(条目个数));
}
static MP_DEFINE_CONST_FUN_OBJ_2(文件写入器对象, 写入文件);
static mp_obj_t 移除文件(mp_obj_t 名称) { 已检查(用户调用(11, (uintptr_t)路径参数(名称), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(文件移除器对象, 移除文件);
static mp_obj_t 画图矩形(size_t 项目个数, const mp_obj_t *参数数组) {
    (void)项目个数; unsigned 首位值[5]; for (unsigned 序数索引 = 0; 序数索引 < 5; 序数索引++) 首位值[序数索引] = mp_obj_get_int(参数数组[序数索引]);
    已检查(屏幕矩形(首位值[0], 首位值[1], 首位值[2], 首位值[3], 首位值[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(矩形对象, 5, 5, 画图矩形);
static mp_obj_t 读取屏幕大小(void) {
    mp_obj_t 大小[2] = {mp_obj_new_int(已检查(读取屏幕宽度())), mp_obj_new_int(已检查(读取屏幕高度()))};
    return mp_obj_new_tuple(2, 大小);
}
static MP_DEFINE_CONST_FUN_OBJ_0(屏幕大小对象, 读取屏幕大小);
static mp_obj_t 等待状态用于屏幕输入(void) { return mp_obj_new_int(已检查(等待状态用于屏幕键())); }
static MP_DEFINE_CONST_FUN_OBJ_0(屏幕等待状态对象, 等待状态用于屏幕输入);
static mp_obj_t 时钟值(void) { return mp_obj_new_int_from_uint(用户调用(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(时钟对象, 时钟值);
static mp_obj_t UDP打开(mp_obj_t 端口编号) {
    int 数据位置 = mp_obj_get_int(端口编号); if (数据位置 < 0 || 数据位置 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t 文件句柄 = 已检查(用户调用(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 首位值 = {0}; 首位值.sin_family = AF_INET; 首位值.sin_port = pk_htons(数据位置); 首位值.sin_addr.s_addr = 0;
    intptr_t 结果 = 用户调用(33, 文件句柄, (uintptr_t)&首位值, sizeof(首位值), 0, 0, 0);
    if (结果 < 0) { 用户调用(4, 文件句柄, 0, 0, 0, 0, 0); 已检查(结果); }
    return mp_obj_new_int(文件句柄);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP打开对象值, UDP打开);
static mp_obj_t UDP发送(mp_obj_t 文件句柄, mp_obj_t 端口编号, mp_obj_t 内容值) {
    int 数据位置 = mp_obj_get_int(端口编号); if (数据位置 < 1 || 数据位置 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t 数据; mp_get_buffer_raise(内容值, &数据, MP_BUFFER_READ);
    struct pk_sockaddr_in 首位值 = {0}; 首位值.sin_family = AF_INET; 首位值.sin_port = pk_htons(数据位置); 首位值.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(已检查(用户调用(34, mp_obj_get_int(文件句柄), (uintptr_t)数据.buf, 数据.len, 0, (uintptr_t)&首位值, sizeof(首位值))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP发送对象值, UDP发送);
static uint32_t 读取互联网地址(mp_obj_t 值) {
    size_t 长度; const char *文本=mp_obj_str_get_data(值,&长度);
    unsigned 当前位置=0; uint32_t 地址=0;
    for(unsigned 子部分值=0;子部分值<4;子部分值++) {
        unsigned 值=0,数字个数=0;
        while(当前位置<长度&&文本[当前位置]>='0'&&文本[当前位置]<='9') {
            值=值*10+文本[当前位置++]-'0'; if(++数字个数>3||值>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!数字个数)mp_raise_OSError(MP_EINVAL);
        地址=地址<<8|值;
        if(子部分值<3&&(当前位置>=长度||文本[当前位置++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(当前位置!=长度)mp_raise_OSError(MP_EINVAL);
    return 地址;
}
static mp_obj_t UDP定址发送(size_t 条目个数, const mp_obj_t *参数数组) {
    (void)条目个数; uint32_t 地址=读取互联网地址(参数数组[1]);
    int 端口编号=mp_obj_get_int(参数数组[2]);if(端口编号<1||端口编号>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t 数据;mp_get_buffer_raise(参数数组[3],&数据,MP_BUFFER_READ);
    struct pk_sockaddr_in 目标值={0};目标值.sin_family=AF_INET;目标值.sin_port=pk_htons(端口编号);目标值.sin_addr.s_addr=pk_htonl(地址);
    return mp_obj_new_int(已检查(用户调用(34,mp_obj_get_int(参数数组[0]),(uintptr_t)数据.buf,数据.len,0,(uintptr_t)&目标值,sizeof(目标值))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(UDP定址发送对象值,4,4,UDP定址发送);
static mp_obj_t UDP接收操作(mp_obj_t 文件句柄) {
    unsigned char 数据[512]; struct pk_sockaddr_in 对端值; pk_socklen_t 长度数据 = sizeof(对端值);
    intptr_t 大小 = 已检查(用户调用(35, mp_obj_get_int(文件句柄), (uintptr_t)数据, 512, 0, (uintptr_t)&对端值, (uintptr_t)&长度数据));
    mp_obj_t 值列[2] = {mp_obj_new_bytes(数据, 大小), MP_OBJ_NEW_SMALL_INT(pk_htons(对端值.sin_port))};
    return mp_obj_new_tuple(2, 值列);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP接收操作对象值, UDP接收操作);
static mp_obj_t UDP关闭(mp_obj_t 文件句柄) { 已检查(用户调用(4, mp_obj_get_int(文件句柄), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP关闭对象值, UDP关闭);
static mp_obj_t 打开流(void) {
    return mp_obj_new_int(已检查(用户调用(32,互联网族,流网络,流传输协议,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(流打开器对象,打开流);
static mp_obj_t 连接流(mp_obj_t 端点,mp_obj_t 地址文本,mp_obj_t 编号) {
    int 端口编号=mp_obj_get_int(编号); if(端口编号<1||端口编号>65535)mp_raise_OSError(MP_EINVAL);
    struct 互联网套接字地址 地址={0}; 地址.地址族=互联网族;
    地址.端口编号=网络短整数(端口编号); 地址.互联网地址.地址值=网络整数(读取互联网地址(地址文本));
    已检查(用户调用(37,mp_obj_get_int(端点),(uintptr_t)&地址,sizeof(地址),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(流连接器对象,连接流);
static mp_obj_t 读取流(mp_obj_t 端点,mp_obj_t 容量限制) {
    int 长度=mp_obj_get_int(容量限制); if(长度<1||长度>512)mp_raise_OSError(MP_EINVAL);
    unsigned char 数据[512];
    intptr_t 项目个数=已检查(用户调用(2,mp_obj_get_int(端点),(uintptr_t)数据,长度,0,0,0));
    return mp_obj_new_bytes(数据,项目个数);
}
static MP_DEFINE_CONST_FUN_OBJ_2(流读取器对象,读取流);
static mp_obj_t 写入流(mp_obj_t 端点,mp_obj_t 内容值) {
    mp_buffer_info_t 数据; mp_get_buffer_raise(内容值,&数据,MP_BUFFER_READ);
    return mp_obj_new_int(已检查(用户调用(1,mp_obj_get_int(端点),(uintptr_t)数据.buf,数据.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(流写入器对象,写入流);
static mp_obj_t 等待状态临时地(mp_obj_t 时间值) {
    已检查(用户调用(17,mp_obj_get_int(时间值),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(等待状态对象,等待状态临时地);
static mp_obj_t 条目种类(mp_obj_t 名称) {
    return mp_obj_new_int(已检查(用户调用(18,(uintptr_t)路径参数(名称),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(条目种类对象,条目种类);
static mp_obj_t 创建目录(mp_obj_t 名称) {
    已检查(用户调用(18,(uintptr_t)路径参数(名称),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(目录创建器对象,创建目录);
static mp_obj_t 移除目录(mp_obj_t 名称) {
    已检查(用户调用(18,(uintptr_t)路径参数(名称),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(目录移除器对象,移除目录);
static const mp_rom_map_elem_t 模块名称列[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&流打开器对象) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&流连接器对象) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&流读取器对象) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&流写入器对象) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&等待状态对象) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&条目种类对象) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&目录创建器对象) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&目录移除器对象) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&标准输入读取器对象) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&文件读取器对象) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&文件写入器对象) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&文件移除器对象) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&矩形对象) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&屏幕大小对象) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&屏幕等待状态对象) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&时钟对象) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP打开对象值) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP发送对象值) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&UDP定址发送对象值) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&UDP接收操作对象值) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP关闭对象值) },
};
static MP_DEFINE_CONST_DICT(模块全局变量列, 模块名称列);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&模块全局变量列 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
