// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t mesur) { if (mesur < 0) mp_raise_OSError(-mesur); return mesur; }
static const char *llwybr_arg(mp_obj_t VALUE) {
    size_t eitem_COUNT; const char *LLWYBR = mp_obj_str_get_data(VALUE, &eitem_COUNT);
    if (!eitem_COUNT || eitem_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < eitem_COUNT; 순번++) if (!LLWYBR[순번]) mp_raise_OSError(MP_EINVAL);
    return LLWYBR;
}
static mp_obj_t 파일읽기(mp_obj_t Enw) {
    intptr_t ffeil_dolen = 결과검사(사용자호출(3, (uintptr_t)llwybr_arg(Enw), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Maint = 결과검사(사용자호출(9, ffeil_dolen, 0, 0, 0, 0, 0));
        vstr_t data; vstr_init_len(&data, Maint);
        intptr_t mesur = 사용자호출(2, ffeil_dolen, (uintptr_t)data.buf, Maint, 0, 0, 0);
        결과검사(mesur); data.len = mesur;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&data);
        nlr_pop(); 사용자호출(4, ffeil_dolen, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, ffeil_dolen, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ffeil_darllenwr_gwrthrych, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Maint=mp_obj_get_int(한도);
    if(Maint<0||Maint>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t data; vstr_init_len(&data,Maint);
    intptr_t eitem_COUNT=사용자호출(2,0,(uintptr_t)data.buf,Maint,0,0,0);
    if(eitem_COUNT<0) { vstr_clear(&data); 결과검사(eitem_COUNT); }
    data.len=eitem_COUNT; return mp_obj_new_bytes_from_vstr(&data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t ysgrifennu_ffeil(mp_obj_t Enw, mp_obj_t Cynnwys_VALUE) {
    const char *LLWYBR = llwybr_arg(Enw);
    mp_buffer_info_t data; mp_get_buffer_raise(Cynnwys_VALUE, &data, MP_BUFFER_READ);
    if (data.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ffeil_dolen = 결과검사(사용자호출(3, (uintptr_t)LLWYBR, 577, 0, 0, 0, 0));
    intptr_t cofnod_COUNT = 사용자호출(1, ffeil_dolen, (uintptr_t)data.buf, data.len, 0, 0, 0);
    사용자호출(4, ffeil_dolen, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(cofnod_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ffeil_Writer_gwrthrych, ysgrifennu_ffeil);
static mp_obj_t tynnu_ffeil(mp_obj_t Enw) { 결과검사(사용자호출(11, (uintptr_t)llwybr_arg(Enw), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, tynnu_ffeil);
static mp_obj_t 사각형그리기(size_t eitem_COUNT, const mp_obj_t *arg_ARAE) {
    (void)eitem_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(arg_ARAE[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Maint[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Maint);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Cloc_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Cloc_gwrthrych, Cloc_VALUE);
static mp_obj_t UDP_agor(mp_obj_t rhif_porth) {
    int data_safle = mp_obj_get_int(rhif_porth); if (data_safle < 0 || data_safle > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ffeil_dolen = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_safle); 첫째값.sin_addr.s_addr = 0;
    intptr_t mesur = 사용자호출(33, ffeil_dolen, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (mesur < 0) { 사용자호출(4, ffeil_dolen, 0, 0, 0, 0, 0); 결과검사(mesur); }
    return mp_obj_new_int(ffeil_dolen);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, UDP_agor);
static mp_obj_t UDP_anfon(mp_obj_t ffeil_dolen, mp_obj_t rhif_porth, mp_obj_t Cynnwys_VALUE) {
    int data_safle = mp_obj_get_int(rhif_porth); if (data_safle < 1 || data_safle > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data; mp_get_buffer_raise(Cynnwys_VALUE, &data, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(data_safle); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ffeil_dolen), (uintptr_t)data.buf, data.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, UDP_anfon);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t hyd_VALUE; const char *Testun=mp_obj_str_get_data(VALUE,&hyd_VALUE);
    unsigned 현재위치=0; uint32_t ADDRESS=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,digid_COUNT=0;
        while(현재위치<hyd_VALUE&&Testun[현재위치]>='0'&&Testun[현재위치]<='9') {
            VALUE=VALUE*10+Testun[현재위치++]-'0'; if(++digid_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!digid_COUNT)mp_raise_OSError(MP_EINVAL);
        ADDRESS=ADDRESS<<8|VALUE;
        if(부분<3&&(현재위치>=hyd_VALUE||Testun[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=hyd_VALUE)mp_raise_OSError(MP_EINVAL);
    return ADDRESS;
}
static mp_obj_t 전문주소전송(size_t cofnod_COUNT, const mp_obj_t *arg_ARAE) {
    (void)cofnod_COUNT; uint32_t ADDRESS=인터넷주소읽기(arg_ARAE[1]);
    int rhif_porth=mp_obj_get_int(arg_ARAE[2]);if(rhif_porth<1||rhif_porth>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data;mp_get_buffer_raise(arg_ARAE[3],&data,MP_BUFFER_READ);
    struct pk_sockaddr_in targed={0};targed.sin_family=AF_INET;targed.sin_port=pk_htons(rhif_porth);targed.sin_addr.s_addr=pk_htonl(ADDRESS);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(arg_ARAE[0]),(uintptr_t)data.buf,data.len,0,(uintptr_t)&targed,sizeof(targed))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ffeil_dolen) {
    unsigned char data[512]; struct pk_sockaddr_in cymar_VALUE; pk_socklen_t hyd_data = sizeof(cymar_VALUE);
    intptr_t Maint = 결과검사(사용자호출(35, mp_obj_get_int(ffeil_dolen), (uintptr_t)data, 512, 0, (uintptr_t)&cymar_VALUE, (uintptr_t)&hyd_data));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(data, Maint), MP_OBJ_NEW_SMALL_INT(pk_htons(cymar_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_cau(mp_obj_t ffeil_dolen) { 결과검사(사용자호출(4, mp_obj_get_int(ffeil_dolen), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, UDP_cau);
static mp_obj_t agor_ffrwd(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,cwmwl_Teulu,ffrwd_Rhwydwaith,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,agor_ffrwd);
static mp_obj_t Cysylltu_ffrwd(mp_obj_t 종단,mp_obj_t ADDRESS_SMS,mp_obj_t INDEX) {
    int rhif_porth=mp_obj_get_int(INDEX); if(rhif_porth<1||rhif_porth>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ADDRESS={0}; ADDRESS.ADDRESS_Teulu=cwmwl_Teulu;
    ADDRESS.rhif_porth=망차례짧은수(rhif_porth); ADDRESS.cyfeiriad_rhyngrwyd.ADDRESS_VALUE=Rhwydwaith_cyfanrif(인터넷주소읽기(ADDRESS_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ADDRESS,sizeof(ADDRESS),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ffrwd_cysylltydd_gwrthrych,Cysylltu_ffrwd);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int hyd_VALUE=mp_obj_get_int(한도); if(hyd_VALUE<1||hyd_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char data[512];
    intptr_t eitem_COUNT=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)data,hyd_VALUE,0,0,0));
    return mp_obj_new_bytes(data,eitem_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ffrwd_darllenwr_gwrthrych,흐름읽기);
static mp_obj_t ysgrifennu_ffrwd(mp_obj_t 종단,mp_obj_t Cynnwys_VALUE) {
    mp_buffer_info_t data; mp_get_buffer_raise(Cynnwys_VALUE,&data,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)data.buf,data.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ffrwd_Writer_gwrthrych,ysgrifennu_ffrwd);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(aros_gwrthrych,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Enw) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)llwybr_arg(Enw),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t Creu_cyfeiriadur(mp_obj_t Enw) {
    결과검사(사용자호출(18,(uintptr_t)llwybr_arg(Enw),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(cyfeiriadur_crëwr_gwrthrych,Creu_cyfeiriadur);
static mp_obj_t tynnu_cyfeiriadur(mp_obj_t Enw) {
    결과검사(사용자호출(18,(uintptr_t)llwybr_arg(Enw),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,tynnu_cyfeiriadur);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ffrwd_cysylltydd_gwrthrych) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ffrwd_darllenwr_gwrthrych) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&ffrwd_Writer_gwrthrych) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&aros_gwrthrych) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&cyfeiriadur_crëwr_gwrthrych) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ffeil_darllenwr_gwrthrych) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ffeil_Writer_gwrthrych) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Cloc_gwrthrych) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
