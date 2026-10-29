// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t سنجش) { if (سنجش < 0) mp_raise_OSError(-سنجش); return سنجش; }
static const char *مسیر_آرگومان(mp_obj_t مقدار) {
    size_t 개수; const char *مسیر = mp_obj_str_get_data(مقدار, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!مسیر[순번]) mp_raise_OSError(MP_EINVAL);
    return مسیر;
}
static mp_obj_t 파일읽기(mp_obj_t نام) {
    intptr_t فایل_دستگیره = 결과검사(사용자호출(3, (uintptr_t)مسیر_آرگومان(نام), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t اندازه = 결과검사(사용자호출(9, فایل_دستگیره, 0, 0, 0, 0, 0));
        vstr_t داده_ها; vstr_init_len(&داده_ها, اندازه);
        intptr_t سنجش = 사용자호출(2, فایل_دستگیره, (uintptr_t)داده_ها.buf, اندازه, 0, 0, 0);
        결과검사(سنجش); داده_ها.len = سنجش;
        mp_obj_t مقدار = mp_obj_new_bytes_from_vstr(&داده_ها);
        nlr_pop(); 사용자호출(4, فایل_دستگیره, 0, 0, 0, 0, 0); return مقدار;
    }
    사용자호출(4, فایل_دستگیره, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(فایل_خواننده_شئ, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t اندازه=mp_obj_get_int(한도);
    if(اندازه<0||اندازه>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t داده_ها; vstr_init_len(&داده_ها,اندازه);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)داده_ها.buf,اندازه,0,0,0);
    if(개수<0) { vstr_clear(&داده_ها); 결과검사(개수); }
    داده_ها.len=개수; return mp_obj_new_bytes_from_vstr(&داده_ها);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t نوشتن_فایل(mp_obj_t نام, mp_obj_t محتوا_مقدار) {
    const char *مسیر = مسیر_آرگومان(نام);
    mp_buffer_info_t داده_ها; mp_get_buffer_raise(محتوا_مقدار, &داده_ها, MP_BUFFER_READ);
    if (داده_ها.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t فایل_دستگیره = 결과검사(사용자호출(3, (uintptr_t)مسیر, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, فایل_دستگیره, (uintptr_t)داده_ها.buf, داده_ها.len, 0, 0, 0);
    사용자호출(4, فایل_دستگیره, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(فایل_نگارنده_شئ, نوشتن_فایل);
static mp_obj_t حذف_فایل(mp_obj_t نام) { 결과검사(사용자호출(11, (uintptr_t)مسیر_آرگومان(نام), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, حذف_فایل);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *آرگومان_آرايه) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(آرگومان_آرايه[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t اندازه[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, اندازه);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t ساعت_مقدار(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(ساعت_شئ, ساعت_مقدار);
static mp_obj_t پروتکل_داده_نگار_کاربر_ایجاد(mp_obj_t شماره_درگاه) {
    int داده_ها_مرتب_کردن = mp_obj_get_int(شماره_درگاه); if (داده_ها_مرتب_کردن < 0 || داده_ها_مرتب_کردن > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t فایل_دستگیره = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(داده_ها_مرتب_کردن); 첫째값.sin_addr.s_addr = 0;
    intptr_t سنجش = 사용자호출(33, فایل_دستگیره, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (سنجش < 0) { 사용자호출(4, فایل_دستگیره, 0, 0, 0, 0, 0); 결과검사(سنجش); }
    return mp_obj_new_int(فایل_دستگیره);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, پروتکل_داده_نگار_کاربر_ایجاد);
static mp_obj_t پروتکل_داده_نگار_کاربر_ارسال(mp_obj_t فایل_دستگیره, mp_obj_t شماره_درگاه, mp_obj_t محتوا_مقدار) {
    int داده_ها_مرتب_کردن = mp_obj_get_int(شماره_درگاه); if (داده_ها_مرتب_کردن < 1 || داده_ها_مرتب_کردن > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t داده_ها; mp_get_buffer_raise(محتوا_مقدار, &داده_ها, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(داده_ها_مرتب_کردن); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(فایل_دستگیره), (uintptr_t)داده_ها.buf, داده_ها.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, پروتکل_داده_نگار_کاربر_ارسال);
static uint32_t 인터넷주소읽기(mp_obj_t مقدار) {
    size_t طول_مقدار; const char *متن=mp_obj_str_get_data(مقدار,&طول_مقدار);
    unsigned 현재위치=0; uint32_t آدرس=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned مقدار=0,숫자수=0;
        while(현재위치<طول_مقدار&&متن[현재위치]>='0'&&متن[현재위치]<='9') {
            مقدار=مقدار*10+متن[현재위치++]-'0'; if(++숫자수>3||مقدار>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        آدرس=آدرس<<8|مقدار;
        if(부분<3&&(현재위치>=طول_مقدار||متن[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=طول_مقدار)mp_raise_OSError(MP_EINVAL);
    return آدرس;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *آرگومان_آرايه) {
    (void)항목수; uint32_t آدرس=인터넷주소읽기(آرگومان_آرايه[1]);
    int شماره_درگاه=mp_obj_get_int(آرگومان_آرايه[2]);if(شماره_درگاه<1||شماره_درگاه>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t داده_ها;mp_get_buffer_raise(آرگومان_آرايه[3],&داده_ها,MP_BUFFER_READ);
    struct pk_sockaddr_in هدف={0};هدف.sin_family=AF_INET;هدف.sin_port=pk_htons(شماره_درگاه);هدف.sin_addr.s_addr=pk_htonl(آدرس);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(آرگومان_آرايه[0]),(uintptr_t)داده_ها.buf,داده_ها.len,0,(uintptr_t)&هدف,sizeof(هدف))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t فایل_دستگیره) {
    unsigned char داده_ها[512]; struct pk_sockaddr_in مشابه_مقدار; pk_socklen_t طول_داده_ها = sizeof(مشابه_مقدار);
    intptr_t اندازه = 결과검사(사용자호출(35, mp_obj_get_int(فایل_دستگیره), (uintptr_t)داده_ها, 512, 0, (uintptr_t)&مشابه_مقدار, (uintptr_t)&طول_داده_ها));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(داده_ها, اندازه), MP_OBJ_NEW_SMALL_INT(pk_htons(مشابه_مقدار.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t پروتکل_داده_نگار_کاربر_بستن(mp_obj_t فایل_دستگیره) { 결과검사(사용자호출(4, mp_obj_get_int(فایل_دستگیره), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, پروتکل_داده_نگار_کاربر_بستن);
static mp_obj_t ایجاد_جریان(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,ابری_خانواده,جریان_شبکه,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ایجاد_جریان);
static mp_obj_t اتصال_جریان(mp_obj_t 종단,mp_obj_t آدرس_متن,mp_obj_t فهرست) {
    int شماره_درگاه=mp_obj_get_int(فهرست); if(شماره_درگاه<1||شماره_درگاه>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 آدرس={0}; آدرس.آدرس_خانواده=ابری_خانواده;
    آدرس.شماره_درگاه=망차례짧은수(شماره_درگاه); آدرس.آدرس_اینترنتی.آدرس_مقدار=شبکه_عدد_صحیح(인터넷주소읽기(آدرس_متن));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&آدرس,sizeof(آدرس),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(جریان_رابط_شئ,اتصال_جریان);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int طول_مقدار=mp_obj_get_int(한도); if(طول_مقدار<1||طول_مقدار>512)mp_raise_OSError(MP_EINVAL);
    unsigned char داده_ها[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)داده_ها,طول_مقدار,0,0,0));
    return mp_obj_new_bytes(داده_ها,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(جریان_خواننده_شئ,흐름읽기);
static mp_obj_t نوشتن_جریان(mp_obj_t 종단,mp_obj_t محتوا_مقدار) {
    mp_buffer_info_t داده_ها; mp_get_buffer_raise(محتوا_مقدار,&داده_ها,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)داده_ها.buf,داده_ها.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(جریان_نگارنده_شئ,نوشتن_جریان);
static mp_obj_t 잠시기다리기(mp_obj_t زمان_مقدار) {
    결과검사(사용자호출(17,mp_obj_get_int(زمان_مقدار),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(منتظر_ماندن_شئ,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t نام) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)مسیر_آرگومان(نام),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t ایجاد_فهرست(mp_obj_t نام) {
    결과검사(사용자호출(18,(uintptr_t)مسیر_آرگومان(نام),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(فهرست_ایجاد_کننده_شئ,ایجاد_فهرست);
static mp_obj_t حذف_فهرست(mp_obj_t نام) {
    결과검사(사용자호출(18,(uintptr_t)مسیر_آرگومان(نام),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,حذف_فهرست);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&جریان_رابط_شئ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&جریان_خواننده_شئ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&جریان_نگارنده_شئ) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&منتظر_ماندن_شئ) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&فهرست_ایجاد_کننده_شئ) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&فایل_خواننده_شئ) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&فایل_نگارنده_شئ) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&ساعت_شئ) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
