// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "呼出.h"
#include "通信網ABI.h"
static intptr_t 検査済み(intptr_t 結果) { if (結果 < 0) mp_raise_OSError(-結果); return 結果; }
static const char *経路引数(mp_obj_t 値) {
    size_t 項目個数; const char *経路 = mp_obj_str_get_data(値, &項目個数);
    if (!項目個数 || 項目個数 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 序数添字 = 0; 序数添字 < 項目個数; 序数添字++) if (!経路[序数添字]) mp_raise_OSError(MP_EINVAL);
    return 経路;
}
static mp_obj_t ファイル読取(mp_obj_t 名前) {
    intptr_t ファイル取扱い = 検査済み(利用者呼出(3, (uintptr_t)経路引数(名前), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 非該当局所復帰;
    if (nlr_push(&非該当局所復帰) == 0) {
        size_t 容量 = 検査済み(利用者呼出(9, ファイル取扱い, 0, 0, 0, 0, 0));
        vstr_t データ; vstr_init_len(&データ, 容量);
        intptr_t 結果 = 利用者呼出(2, ファイル取扱い, (uintptr_t)データ.buf, 容量, 0, 0, 0);
        検査済み(結果); データ.len = 結果;
        mp_obj_t 値 = mp_obj_new_bytes_from_vstr(&データ);
        nlr_pop(); 利用者呼出(4, ファイル取扱い, 0, 0, 0, 0, 0); return 値;
    }
    利用者呼出(4, ファイル取扱い, 0, 0, 0, 0, 0); nlr_jump(非該当局所復帰.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ファイル読取器オブジェクト, ファイル読取);
static mp_obj_t 標準入力読取(mp_obj_t 容積上限) {
    mp_int_t 容量=mp_obj_get_int(容積上限);
    if(容量<0||容量>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t データ; vstr_init_len(&データ,容量);
    intptr_t 項目個数=利用者呼出(2,0,(uintptr_t)データ.buf,容量,0,0,0);
    if(項目個数<0) { vstr_clear(&データ); 検査済み(項目個数); }
    データ.len=項目個数; return mp_obj_new_bytes_from_vstr(&データ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(標準入力読取器オブジェクト, 標準入力読取);
static mp_obj_t ファイル書込(mp_obj_t 名前, mp_obj_t 内容物値) {
    const char *経路 = 経路引数(名前);
    mp_buffer_info_t データ; mp_get_buffer_raise(内容物値, &データ, MP_BUFFER_READ);
    if (データ.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ファイル取扱い = 検査済み(利用者呼出(3, (uintptr_t)経路, 577, 0, 0, 0, 0));
    intptr_t 入口個数 = 利用者呼出(1, ファイル取扱い, (uintptr_t)データ.buf, データ.len, 0, 0, 0);
    利用者呼出(4, ファイル取扱い, 0, 0, 0, 0, 0); return mp_obj_new_int(検査済み(入口個数));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ファイル書込器オブジェクト, ファイル書込);
static mp_obj_t ファイル除去(mp_obj_t 名前) { 検査済み(利用者呼出(11, (uintptr_t)経路引数(名前), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(ファイル除去器オブジェクト, ファイル除去);
static mp_obj_t 塗装矩形(size_t 項目個数, const mp_obj_t *引数配列) {
    (void)項目個数; unsigned 先頭位置値[5]; for (unsigned 序数添字 = 0; 序数添字 < 5; 序数添字++) 先頭位置値[序数添字] = mp_obj_get_int(引数配列[序数添字]);
    検査済み(画面矩形(先頭位置値[0], 先頭位置値[1], 先頭位置値[2], 先頭位置値[3], 先頭位置値[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(矩形オブジェクト, 5, 5, 塗装矩形);
static mp_obj_t 画面容量読取(void) {
    mp_obj_t 容量[2] = {mp_obj_new_int(検査済み(画面幅読取())), mp_obj_new_int(検査済み(画面高さ読取()))};
    return mp_obj_new_tuple(2, 容量);
}
static MP_DEFINE_CONST_FUN_OBJ_0(画面容量オブジェクト, 画面容量読取);
static mp_obj_t 対象画面入力待合(void) { return mp_obj_new_int(検査済み(対象画面キー待合())); }
static MP_DEFINE_CONST_FUN_OBJ_0(画面待合オブジェクト, 対象画面入力待合);
static mp_obj_t 時計値(void) { return mp_obj_new_int_from_uint(利用者呼出(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(時計オブジェクト, 時計値);
static mp_obj_t UDP開放(mp_obj_t ポート番号) {
    int データ位置 = mp_obj_get_int(ポート番号); if (データ位置 < 0 || データ位置 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ファイル取扱い = 検査済み(利用者呼出(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 先頭位置値 = {0}; 先頭位置値.sin_family = AF_INET; 先頭位置値.sin_port = pk_htons(データ位置); 先頭位置値.sin_addr.s_addr = 0;
    intptr_t 結果 = 利用者呼出(33, ファイル取扱い, (uintptr_t)&先頭位置値, sizeof(先頭位置値), 0, 0, 0);
    if (結果 < 0) { 利用者呼出(4, ファイル取扱い, 0, 0, 0, 0, 0); 検査済み(結果); }
    return mp_obj_new_int(ファイル取扱い);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP開放対象物, UDP開放);
static mp_obj_t UDP送信(mp_obj_t ファイル取扱い, mp_obj_t ポート番号, mp_obj_t 内容物値) {
    int データ位置 = mp_obj_get_int(ポート番号); if (データ位置 < 1 || データ位置 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t データ; mp_get_buffer_raise(内容物値, &データ, MP_BUFFER_READ);
    struct pk_sockaddr_in 先頭位置値 = {0}; 先頭位置値.sin_family = AF_INET; 先頭位置値.sin_port = pk_htons(データ位置); 先頭位置値.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(検査済み(利用者呼出(34, mp_obj_get_int(ファイル取扱い), (uintptr_t)データ.buf, データ.len, 0, (uintptr_t)&先頭位置値, sizeof(先頭位置値))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP送信対象物, UDP送信);
static uint32_t インターネット番地読取(mp_obj_t 値) {
    size_t 長さ; const char *文=mp_obj_str_get_data(値,&長さ);
    unsigned 現在位置=0; uint32_t 番地=0;
    for(unsigned 部分要素値=0;部分要素値<4;部分要素値++) {
        unsigned 値=0,桁個数=0;
        while(現在位置<長さ&&文[現在位置]>='0'&&文[現在位置]<='9') {
            値=値*10+文[現在位置++]-'0'; if(++桁個数>3||値>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!桁個数)mp_raise_OSError(MP_EINVAL);
        番地=番地<<8|値;
        if(部分要素値<3&&(現在位置>=長さ||文[現在位置++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(現在位置!=長さ)mp_raise_OSError(MP_EINVAL);
    return 番地;
}
static mp_obj_t UDP宛先送信(size_t 入口個数, const mp_obj_t *引数配列) {
    (void)入口個数; uint32_t 番地=インターネット番地読取(引数配列[1]);
    int ポート番号=mp_obj_get_int(引数配列[2]);if(ポート番号<1||ポート番号>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t データ;mp_get_buffer_raise(引数配列[3],&データ,MP_BUFFER_READ);
    struct pk_sockaddr_in 対象値={0};対象値.sin_family=AF_INET;対象値.sin_port=pk_htons(ポート番号);対象値.sin_addr.s_addr=pk_htonl(番地);
    return mp_obj_new_int(検査済み(利用者呼出(34,mp_obj_get_int(引数配列[0]),(uintptr_t)データ.buf,データ.len,0,(uintptr_t)&対象値,sizeof(対象値))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(UDP宛先送信対象物,4,4,UDP宛先送信);
static mp_obj_t UDP受信処理(mp_obj_t ファイル取扱い) {
    unsigned char データ[512]; struct pk_sockaddr_in 通信相手値; pk_socklen_t 長さデータ = sizeof(通信相手値);
    intptr_t 容量 = 検査済み(利用者呼出(35, mp_obj_get_int(ファイル取扱い), (uintptr_t)データ, 512, 0, (uintptr_t)&通信相手値, (uintptr_t)&長さデータ));
    mp_obj_t 値一覧[2] = {mp_obj_new_bytes(データ, 容量), MP_OBJ_NEW_SMALL_INT(pk_htons(通信相手値.sin_port))};
    return mp_obj_new_tuple(2, 値一覧);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP受信処理対象物, UDP受信処理);
static mp_obj_t UDP閉鎖(mp_obj_t ファイル取扱い) { 検査済み(利用者呼出(4, mp_obj_get_int(ファイル取扱い), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP閉鎖対象物, UDP閉鎖);
static mp_obj_t ストリーム開放(void) {
    return mp_obj_new_int(検査済み(利用者呼出(32,インターネット体系,ストリーム通信網,ストリーム輸送通信規約,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(ストリーム開放器オブジェクト,ストリーム開放);
static mp_obj_t ストリーム接続(mp_obj_t 通信端点,mp_obj_t 番地本文,mp_obj_t 番号) {
    int ポート番号=mp_obj_get_int(番号); if(ポート番号<1||ポート番号>65535)mp_raise_OSError(MP_EINVAL);
    struct インターネットソケット番地 番地={0}; 番地.番地体系=インターネット体系;
    番地.ポート番号=通信網短整数(ポート番号); 番地.インターネット番地.番地値=通信網整数値(インターネット番地読取(番地本文));
    検査済み(利用者呼出(37,mp_obj_get_int(通信端点),(uintptr_t)&番地,sizeof(番地),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ストリーム接続器オブジェクト,ストリーム接続);
static mp_obj_t ストリーム読取(mp_obj_t 通信端点,mp_obj_t 容積上限) {
    int 長さ=mp_obj_get_int(容積上限); if(長さ<1||長さ>512)mp_raise_OSError(MP_EINVAL);
    unsigned char データ[512];
    intptr_t 項目個数=検査済み(利用者呼出(2,mp_obj_get_int(通信端点),(uintptr_t)データ,長さ,0,0,0));
    return mp_obj_new_bytes(データ,項目個数);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ストリーム読取器オブジェクト,ストリーム読取);
static mp_obj_t ストリーム書込(mp_obj_t 通信端点,mp_obj_t 内容物値) {
    mp_buffer_info_t データ; mp_get_buffer_raise(内容物値,&データ,MP_BUFFER_READ);
    return mp_obj_new_int(検査済み(利用者呼出(1,mp_obj_get_int(通信端点),(uintptr_t)データ.buf,データ.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ストリーム書込器オブジェクト,ストリーム書込);
static mp_obj_t 一時的に待合(mp_obj_t 時間値) {
    検査済み(利用者呼出(17,mp_obj_get_int(時間値),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(オブジェクト待合,一時的に待合);
static mp_obj_t 入口種別(mp_obj_t 名前) {
    return mp_obj_new_int(検査済み(利用者呼出(18,(uintptr_t)経路引数(名前),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(入口種別オブジェクト,入口種別);
static mp_obj_t ディレクトリ作成(mp_obj_t 名前) {
    検査済み(利用者呼出(18,(uintptr_t)経路引数(名前),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(ディレクトリ作成器オブジェクト,ディレクトリ作成);
static mp_obj_t ディレクトリ除去(mp_obj_t 名前) {
    検査済み(利用者呼出(18,(uintptr_t)経路引数(名前),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(ディレクトリ除去器オブジェクト,ディレクトリ除去);
static const mp_rom_map_elem_t モジュール名前一覧[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&ストリーム開放器オブジェクト) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ストリーム接続器オブジェクト) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ストリーム読取器オブジェクト) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&ストリーム書込器オブジェクト) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&オブジェクト待合) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&入口種別オブジェクト) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&ディレクトリ作成器オブジェクト) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&ディレクトリ除去器オブジェクト) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&標準入力読取器オブジェクト) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ファイル読取器オブジェクト) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ファイル書込器オブジェクト) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&ファイル除去器オブジェクト) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&矩形オブジェクト) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&画面容量オブジェクト) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&画面待合オブジェクト) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&時計オブジェクト) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP開放対象物) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP送信対象物) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&UDP宛先送信対象物) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&UDP受信処理対象物) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP閉鎖対象物) },
};
static MP_DEFINE_CONST_DICT(モジュール大域変数一覧, モジュール名前一覧);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&モジュール大域変数一覧 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
