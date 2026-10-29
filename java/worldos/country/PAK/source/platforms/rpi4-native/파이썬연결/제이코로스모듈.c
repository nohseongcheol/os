// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t پیمائش) { if (پیمائش < 0) mp_raise_OSError(-پیمائش); return پیمائش; }
static const char *راہ_دلائل(mp_obj_t قدر) {
    size_t 개수; const char *راستہ_2 = mp_obj_str_get_data(قدر, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!راستہ_2[순번]) mp_raise_OSError(MP_EINVAL);
    return راستہ_2;
}
static mp_obj_t 파일읽기(mp_obj_t نام) {
    intptr_t فائل_ہینڈل = 결과검사(사용자호출(3, (uintptr_t)راہ_دلائل(نام), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t حجم = 결과검사(사용자호출(9, فائل_ہینڈل, 0, 0, 0, 0, 0));
        vstr_t کوائف; vstr_init_len(&کوائف, حجم);
        intptr_t پیمائش = 사용자호출(2, فائل_ہینڈل, (uintptr_t)کوائف.buf, حجم, 0, 0, 0);
        결과검사(پیمائش); کوائف.len = پیمائش;
        mp_obj_t قدر = mp_obj_new_bytes_from_vstr(&کوائف);
        nlr_pop(); 사용자호출(4, فائل_ہینڈل, 0, 0, 0, 0, 0); return قدر;
    }
    사용자호출(4, فائل_ہینڈل, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(فائل_ریڈر_آبجیکٹ, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t حجم=mp_obj_get_int(한도);
    if(حجم<0||حجم>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t کوائف; vstr_init_len(&کوائف,حجم);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)کوائف.buf,حجم,0,0,0);
    if(개수<0) { vstr_clear(&کوائف); 결과검사(개수); }
    کوائف.len=개수; return mp_obj_new_bytes_from_vstr(&کوائف);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t لکھیں_فائل(mp_obj_t نام, mp_obj_t مشمول_قدر) {
    const char *راستہ_2 = راہ_دلائل(نام);
    mp_buffer_info_t کوائف; mp_get_buffer_raise(مشمول_قدر, &کوائف, MP_BUFFER_READ);
    if (کوائف.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t فائل_ہینڈل = 결과검사(사용자호출(3, (uintptr_t)راستہ_2, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, فائل_ہینڈل, (uintptr_t)کوائف.buf, کوائف.len, 0, 0, 0);
    사용자호출(4, فائل_ہینڈل, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(فائل_مصنف_آبجیکٹ, لکھیں_فائل);
static mp_obj_t ہٹائیں_فائل(mp_obj_t نام) { 결과검사(사용자호출(11, (uintptr_t)راہ_دلائل(نام), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ہٹائیں_فائل);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *دلائل_لڑی) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(دلائل_لڑی[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t حجم[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, حجم);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t کلاک_قدر(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(کلاک_آبجیکٹ, کلاک_قدر);
static mp_obj_t 전문열기(mp_obj_t دہانہ_نمبر) {
    int کوائف_پوزیشن_ٹھیک_کریں = mp_obj_get_int(دہانہ_نمبر); if (کوائف_پوزیشن_ٹھیک_کریں < 0 || کوائف_پوزیشن_ٹھیک_کریں > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t فائل_ہینڈل = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(کوائف_پوزیشن_ٹھیک_کریں); 첫째값.sin_addr.s_addr = 0;
    intptr_t پیمائش = 사용자호출(33, فائل_ہینڈل, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (پیمائش < 0) { 사용자호출(4, فائل_ہینڈل, 0, 0, 0, 0, 0); 결과검사(پیمائش); }
    return mp_obj_new_int(فائل_ہینڈل);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t فائل_ہینڈل, mp_obj_t دہانہ_نمبر, mp_obj_t مشمول_قدر) {
    int کوائف_پوزیشن_ٹھیک_کریں = mp_obj_get_int(دہانہ_نمبر); if (کوائف_پوزیشن_ٹھیک_کریں < 1 || کوائف_پوزیشن_ٹھیک_کریں > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t کوائف; mp_get_buffer_raise(مشمول_قدر, &کوائف, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(کوائف_پوزیشن_ٹھیک_کریں); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(فائل_ہینڈل), (uintptr_t)کوائف.buf, کوائف.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t قدر) {
    size_t لمبا_ئی_قدر; const char *متن=mp_obj_str_get_data(قدر,&لمبا_ئی_قدر);
    unsigned 현재위치=0; uint32_t پتہ=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned قدر=0,숫자수=0;
        while(현재위치<لمبا_ئی_قدر&&متن[현재위치]>='0'&&متن[현재위치]<='9') {
            قدر=قدر*10+متن[현재위치++]-'0'; if(++숫자수>3||قدر>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        پتہ=پتہ<<8|قدر;
        if(부분<3&&(현재위치>=لمبا_ئی_قدر||متن[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=لمبا_ئی_قدر)mp_raise_OSError(MP_EINVAL);
    return پتہ;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *دلائل_لڑی) {
    (void)항목수; uint32_t پتہ=인터넷주소읽기(دلائل_لڑی[1]);
    int دہانہ_نمبر=mp_obj_get_int(دلائل_لڑی[2]);if(دہانہ_نمبر<1||دہانہ_نمبر>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t کوائف;mp_get_buffer_raise(دلائل_لڑی[3],&کوائف,MP_BUFFER_READ);
    struct pk_sockaddr_in ہدف={0};ہدف.sin_family=AF_INET;ہدف.sin_port=pk_htons(دہانہ_نمبر);ہدف.sin_addr.s_addr=pk_htonl(پتہ);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(دلائل_لڑی[0]),(uintptr_t)کوائف.buf,کوائف.len,0,(uintptr_t)&ہدف,sizeof(ہدف))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t فائل_ہینڈل) {
    unsigned char کوائف[512]; struct pk_sockaddr_in ساتھی_قدر; pk_socklen_t لمبا_ئی_کوائف = sizeof(ساتھی_قدر);
    intptr_t حجم = 결과검사(사용자호출(35, mp_obj_get_int(فائل_ہینڈل), (uintptr_t)کوائف, 512, 0, (uintptr_t)&ساتھی_قدر, (uintptr_t)&لمبا_ئی_کوائف));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(کوائف, حجم), MP_OBJ_NEW_SMALL_INT(pk_htons(ساتھی_قدر.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t فائل_ہینڈل) { 결과검사(사용자호출(4, mp_obj_get_int(فائل_ہینڈل), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t بنائیں_بہاؤ(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,بادل_خاندان,بہاؤ_نیٹ_ورک,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,بنائیں_بہاؤ);
static mp_obj_t جڑیں_بہاؤ(mp_obj_t 종단,mp_obj_t پتہ_متن,mp_obj_t اشاریہ) {
    int دہانہ_نمبر=mp_obj_get_int(اشاریہ); if(دہانہ_نمبر<1||دہانہ_نمبر>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 پتہ={0}; پتہ.پتہ_خاندان=بادل_خاندان;
    پتہ.دہانہ_نمبر=망차례짧은수(دہانہ_نمبر); پتہ.انٹرنیٹ_پتہ.پتہ_قدر=نیٹ_ورک_سالم_عدد(인터넷주소읽기(پتہ_متن));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&پتہ,sizeof(پتہ),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(بہاؤ_کنکٹر_آبجیکٹ,جڑیں_بہاؤ);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int لمبا_ئی_قدر=mp_obj_get_int(한도); if(لمبا_ئی_قدر<1||لمبا_ئی_قدر>512)mp_raise_OSError(MP_EINVAL);
    unsigned char کوائف[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)کوائف,لمبا_ئی_قدر,0,0,0));
    return mp_obj_new_bytes(کوائف,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(بہاؤ_ریڈر_آبجیکٹ,흐름읽기);
static mp_obj_t لکھیں_بہاؤ(mp_obj_t 종단,mp_obj_t مشمول_قدر) {
    mp_buffer_info_t کوائف; mp_get_buffer_raise(مشمول_قدر,&کوائف,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)کوائف.buf,کوائف.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(بہاؤ_مصنف_آبجیکٹ,لکھیں_بہاؤ);
static mp_obj_t 잠시기다리기(mp_obj_t وقت_قدر) {
    결과검사(사용자호출(17,mp_obj_get_int(وقت_قدر),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(انتظار_آبجیکٹ,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t نام) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)راہ_دلائل(نام),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t بنائیں_ڈائریکٹری(mp_obj_t نام) {
    결과검사(사용자호출(18,(uintptr_t)راہ_دلائل(نام),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(ڈائریکٹری_تخلیق_کنندہ_آبجیکٹ,بنائیں_ڈائریکٹری);
static mp_obj_t ہٹائیں_ڈائریکٹری(mp_obj_t نام) {
    결과검사(사용자호출(18,(uintptr_t)راہ_دلائل(نام),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ہٹائیں_ڈائریکٹری);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&بہاؤ_کنکٹر_آبجیکٹ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&بہاؤ_ریڈر_آبجیکٹ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&بہاؤ_مصنف_آبجیکٹ) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&انتظار_آبجیکٹ) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&ڈائریکٹری_تخلیق_کنندہ_آبجیکٹ) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&فائل_ریڈر_آبجیکٹ) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&فائل_مصنف_آبجیکٹ) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&کلاک_آبجیکٹ) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
