// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "調用.h"
#include "網路ABI.h"
static intptr_t 已檢查(intptr_t 結果) { if (結果 < 0) mp_raise_OSError(-結果); return 結果; }
static const char *路徑實際參數(mp_obj_t 值) {
    size_t 項目個數; const char *路徑 = mp_obj_str_get_data(值, &項目個數);
    if (!項目個數 || 項目個數 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 序數索引 = 0; 序數索引 < 項目個數; 序數索引++) if (!路徑[序數索引]) mp_raise_OSError(MP_EINVAL);
    return 路徑;
}
static mp_obj_t 讀取檔案(mp_obj_t 名稱) {
    intptr_t 檔案句柄 = 已檢查(用戶調用(3, (uintptr_t)路徑實際參數(名稱), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 非局部發回;
    if (nlr_push(&非局部發回) == 0) {
        size_t 大小 = 已檢查(用戶調用(9, 檔案句柄, 0, 0, 0, 0, 0));
        vstr_t 資料; vstr_init_len(&資料, 大小);
        intptr_t 結果 = 用戶調用(2, 檔案句柄, (uintptr_t)資料.buf, 大小, 0, 0, 0);
        已檢查(結果); 資料.len = 結果;
        mp_obj_t 值 = mp_obj_new_bytes_from_vstr(&資料);
        nlr_pop(); 用戶調用(4, 檔案句柄, 0, 0, 0, 0, 0); return 值;
    }
    用戶調用(4, 檔案句柄, 0, 0, 0, 0, 0); nlr_jump(非局部發回.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(檔案讀取器物件, 讀取檔案);
static mp_obj_t 讀取標準輸入(mp_obj_t 容量限制) {
    mp_int_t 大小=mp_obj_get_int(容量限制);
    if(大小<0||大小>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t 資料; vstr_init_len(&資料,大小);
    intptr_t 項目個數=用戶調用(2,0,(uintptr_t)資料.buf,大小,0,0,0);
    if(項目個數<0) { vstr_clear(&資料); 已檢查(項目個數); }
    資料.len=項目個數; return mp_obj_new_bytes_from_vstr(&資料);
}
static MP_DEFINE_CONST_FUN_OBJ_1(標準輸入讀取器物件, 讀取標準輸入);
static mp_obj_t 寫入檔案(mp_obj_t 名稱, mp_obj_t 內容值) {
    const char *路徑 = 路徑實際參數(名稱);
    mp_buffer_info_t 資料; mp_get_buffer_raise(內容值, &資料, MP_BUFFER_READ);
    if (資料.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t 檔案句柄 = 已檢查(用戶調用(3, (uintptr_t)路徑, 577, 0, 0, 0, 0));
    intptr_t 條目個數 = 用戶調用(1, 檔案句柄, (uintptr_t)資料.buf, 資料.len, 0, 0, 0);
    用戶調用(4, 檔案句柄, 0, 0, 0, 0, 0); return mp_obj_new_int(已檢查(條目個數));
}
static MP_DEFINE_CONST_FUN_OBJ_2(檔案寫入器物件, 寫入檔案);
static mp_obj_t 移除檔案(mp_obj_t 名稱) { 已檢查(用戶調用(11, (uintptr_t)路徑實際參數(名稱), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(檔案移除器物件, 移除檔案);
static mp_obj_t 畫圖矩形(size_t 項目個數, const mp_obj_t *實際參數陣列) {
    (void)項目個數; unsigned 首位值[5]; for (unsigned 序數索引 = 0; 序數索引 < 5; 序數索引++) 首位值[序數索引] = mp_obj_get_int(實際參數陣列[序數索引]);
    已檢查(屏幕矩形(首位值[0], 首位值[1], 首位值[2], 首位值[3], 首位值[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(矩形物件, 5, 5, 畫圖矩形);
static mp_obj_t 讀取屏幕大小(void) {
    mp_obj_t 大小[2] = {mp_obj_new_int(已檢查(讀取屏幕寬度())), mp_obj_new_int(已檢查(讀取屏幕高度()))};
    return mp_obj_new_tuple(2, 大小);
}
static MP_DEFINE_CONST_FUN_OBJ_0(屏幕大小物件, 讀取屏幕大小);
static mp_obj_t 等待狀態用於屏幕輸入(void) { return mp_obj_new_int(已檢查(等待狀態用於屏幕鍵())); }
static MP_DEFINE_CONST_FUN_OBJ_0(屏幕等待狀態物件, 等待狀態用於屏幕輸入);
static mp_obj_t 時鐘值(void) { return mp_obj_new_int_from_uint(用戶調用(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(時鐘物件, 時鐘值);
static mp_obj_t UDP打開(mp_obj_t 埠編號) {
    int 資料位置 = mp_obj_get_int(埠編號); if (資料位置 < 0 || 資料位置 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t 檔案句柄 = 已檢查(用戶調用(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 首位值 = {0}; 首位值.sin_family = AF_INET; 首位值.sin_port = pk_htons(資料位置); 首位值.sin_addr.s_addr = 0;
    intptr_t 結果 = 用戶調用(33, 檔案句柄, (uintptr_t)&首位值, sizeof(首位值), 0, 0, 0);
    if (結果 < 0) { 用戶調用(4, 檔案句柄, 0, 0, 0, 0, 0); 已檢查(結果); }
    return mp_obj_new_int(檔案句柄);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP打開對象值, UDP打開);
static mp_obj_t UDP發送(mp_obj_t 檔案句柄, mp_obj_t 埠編號, mp_obj_t 內容值) {
    int 資料位置 = mp_obj_get_int(埠編號); if (資料位置 < 1 || 資料位置 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t 資料; mp_get_buffer_raise(內容值, &資料, MP_BUFFER_READ);
    struct pk_sockaddr_in 首位值 = {0}; 首位值.sin_family = AF_INET; 首位值.sin_port = pk_htons(資料位置); 首位值.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(已檢查(用戶調用(34, mp_obj_get_int(檔案句柄), (uintptr_t)資料.buf, 資料.len, 0, (uintptr_t)&首位值, sizeof(首位值))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP發送對象值, UDP發送);
static uint32_t 讀取互聯網地址(mp_obj_t 值) {
    size_t 長度; const char *文本=mp_obj_str_get_data(值,&長度);
    unsigned 當前位置=0; uint32_t 地址=0;
    for(unsigned 子部分值=0;子部分值<4;子部分值++) {
        unsigned 值=0,數字個數=0;
        while(當前位置<長度&&文本[當前位置]>='0'&&文本[當前位置]<='9') {
            值=值*10+文本[當前位置++]-'0'; if(++數字個數>3||值>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!數字個數)mp_raise_OSError(MP_EINVAL);
        地址=地址<<8|值;
        if(子部分值<3&&(當前位置>=長度||文本[當前位置++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(當前位置!=長度)mp_raise_OSError(MP_EINVAL);
    return 地址;
}
static mp_obj_t UDP定址發送(size_t 條目個數, const mp_obj_t *實際參數陣列) {
    (void)條目個數; uint32_t 地址=讀取互聯網地址(實際參數陣列[1]);
    int 埠編號=mp_obj_get_int(實際參數陣列[2]);if(埠編號<1||埠編號>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t 資料;mp_get_buffer_raise(實際參數陣列[3],&資料,MP_BUFFER_READ);
    struct pk_sockaddr_in 目標值={0};目標值.sin_family=AF_INET;目標值.sin_port=pk_htons(埠編號);目標值.sin_addr.s_addr=pk_htonl(地址);
    return mp_obj_new_int(已檢查(用戶調用(34,mp_obj_get_int(實際參數陣列[0]),(uintptr_t)資料.buf,資料.len,0,(uintptr_t)&目標值,sizeof(目標值))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(UDP定址發送對象值,4,4,UDP定址發送);
static mp_obj_t UDP接收操作(mp_obj_t 檔案句柄) {
    unsigned char 資料[512]; struct pk_sockaddr_in 對端值; pk_socklen_t 長度資料 = sizeof(對端值);
    intptr_t 大小 = 已檢查(用戶調用(35, mp_obj_get_int(檔案句柄), (uintptr_t)資料, 512, 0, (uintptr_t)&對端值, (uintptr_t)&長度資料));
    mp_obj_t 值列[2] = {mp_obj_new_bytes(資料, 大小), MP_OBJ_NEW_SMALL_INT(pk_htons(對端值.sin_port))};
    return mp_obj_new_tuple(2, 值列);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP接收操作對象值, UDP接收操作);
static mp_obj_t UDP關閉(mp_obj_t 檔案句柄) { 已檢查(用戶調用(4, mp_obj_get_int(檔案句柄), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP關閉對象值, UDP關閉);
static mp_obj_t 打開流(void) {
    return mp_obj_new_int(已檢查(用戶調用(32,互聯網族,流網路,流傳輸通訊協定,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(流打開器物件,打開流);
static mp_obj_t 連接流(mp_obj_t 端點,mp_obj_t 地址文本,mp_obj_t 編號) {
    int 埠編號=mp_obj_get_int(編號); if(埠編號<1||埠編號>65535)mp_raise_OSError(MP_EINVAL);
    struct 互聯網通訊端地址 地址={0}; 地址.地址族=互聯網族;
    地址.埠編號=網路短整數(埠編號); 地址.互聯網地址.地址值=網路整數(讀取互聯網地址(地址文本));
    已檢查(用戶調用(37,mp_obj_get_int(端點),(uintptr_t)&地址,sizeof(地址),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(流連接器物件,連接流);
static mp_obj_t 讀取流(mp_obj_t 端點,mp_obj_t 容量限制) {
    int 長度=mp_obj_get_int(容量限制); if(長度<1||長度>512)mp_raise_OSError(MP_EINVAL);
    unsigned char 資料[512];
    intptr_t 項目個數=已檢查(用戶調用(2,mp_obj_get_int(端點),(uintptr_t)資料,長度,0,0,0));
    return mp_obj_new_bytes(資料,項目個數);
}
static MP_DEFINE_CONST_FUN_OBJ_2(流讀取器物件,讀取流);
static mp_obj_t 寫入流(mp_obj_t 端點,mp_obj_t 內容值) {
    mp_buffer_info_t 資料; mp_get_buffer_raise(內容值,&資料,MP_BUFFER_READ);
    return mp_obj_new_int(已檢查(用戶調用(1,mp_obj_get_int(端點),(uintptr_t)資料.buf,資料.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(流寫入器物件,寫入流);
static mp_obj_t 等待狀態臨時地(mp_obj_t 時間值) {
    已檢查(用戶調用(17,mp_obj_get_int(時間值),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(等待狀態物件,等待狀態臨時地);
static mp_obj_t 條目種類(mp_obj_t 名稱) {
    return mp_obj_new_int(已檢查(用戶調用(18,(uintptr_t)路徑實際參數(名稱),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(條目種類物件,條目種類);
static mp_obj_t 創建目錄(mp_obj_t 名稱) {
    已檢查(用戶調用(18,(uintptr_t)路徑實際參數(名稱),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(目錄創建器物件,創建目錄);
static mp_obj_t 移除目錄(mp_obj_t 名稱) {
    已檢查(用戶調用(18,(uintptr_t)路徑實際參數(名稱),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(目錄移除器物件,移除目錄);
static const mp_rom_map_elem_t 模塊名稱列[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&流打開器物件) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&流連接器物件) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&流讀取器物件) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&流寫入器物件) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&等待狀態物件) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&條目種類物件) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&目錄創建器物件) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&目錄移除器物件) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&標準輸入讀取器物件) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&檔案讀取器物件) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&檔案寫入器物件) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&檔案移除器物件) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&矩形物件) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&屏幕大小物件) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&屏幕等待狀態物件) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&時鐘物件) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP打開對象值) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP發送對象值) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&UDP定址發送對象值) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&UDP接收操作對象值) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP關閉對象值) },
};
static MP_DEFINE_CONST_DICT(模塊全局變量列, 模塊名稱列);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&模塊全局變量列 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
