// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *راہ_دلیل(mp_obj_t قدر) {
    size_t 개수; const char *راہ = mp_obj_str_get_data(قدر, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!راہ[순번]) mp_raise_OSError(MP_EINVAL);
    return راہ;
}
static mp_obj_t 파일읽기(mp_obj_t ناں) {
    intptr_t فائل_نبٹنا = 결과검사(사용자호출(3, (uintptr_t)راہ_دلیل(ناں), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t سائز = 결과검사(사용자호출(9, فائل_نبٹنا, 0, 0, 0, 0, 0));
        vstr_t کوائف; vstr_init_len(&کوائف, سائز);
        intptr_t 결과 = 사용자호출(2, فائل_نبٹنا, (uintptr_t)کوائف.buf, سائز, 0, 0, 0);
        결과검사(결과); کوائف.len = 결과;
        mp_obj_t قدر = mp_obj_new_bytes_from_vstr(&کوائف);
        nlr_pop(); 사용자호출(4, فائل_نبٹنا, 0, 0, 0, 0, 0); return قدر;
    }
    사용자호출(4, فائل_نبٹنا, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(فائل_پڑھن_والا_آبجیکٹ, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t سائز=mp_obj_get_int(한도);
    if(سائز<0||سائز>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t کوائف; vstr_init_len(&کوائف,سائز);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)کوائف.buf,سائز,0,0,0);
    if(개수<0) { vstr_clear(&کوائف); 결과검사(개수); }
    کوائف.len=개수; return mp_obj_new_bytes_from_vstr(&کوائف);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t لکھو_فائل(mp_obj_t ناں, mp_obj_t اجزاء_قدر) {
    const char *راہ = راہ_دلیل(ناں);
    mp_buffer_info_t کوائف; mp_get_buffer_raise(اجزاء_قدر, &کوائف, MP_BUFFER_READ);
    if (کوائف.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t فائل_نبٹنا = 결과검사(사용자호출(3, (uintptr_t)راہ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, فائل_نبٹنا, (uintptr_t)کوائف.buf, کوائف.len, 0, 0, 0);
    사용자호출(4, فائل_نبٹنا, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(فائل_رائٹر_آبجیکٹ, لکھو_فائل);
static mp_obj_t ہٹاؤ_فائل(mp_obj_t ناں) { 결과검사(사용자호출(11, (uintptr_t)راہ_دلیل(ناں), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ہٹاؤ_فائل);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *دلیل_ایرے) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(دلیل_ایرے[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t سائز[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, سائز);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t گھڑی_قدر(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(گھڑی_آبجیکٹ, گھڑی_قدر);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t فائل_نبٹنا = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, فائل_نبٹنا, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, فائل_نبٹنا, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(فائل_نبٹنا);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t فائل_نبٹنا, mp_obj_t 접속번호, mp_obj_t اجزاء_قدر) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t کوائف; mp_get_buffer_raise(اجزاء_قدر, &کوائف, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(فائل_نبٹنا), (uintptr_t)کوائف.buf, کوائف.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t قدر) {
    size_t لمبائی_قدر; const char *متن=mp_obj_str_get_data(قدر,&لمبائی_قدر);
    unsigned 현재위치=0; uint32_t پتا=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned قدر=0,숫자수=0;
        while(현재위치<لمبائی_قدر&&متن[현재위치]>='0'&&متن[현재위치]<='9') {
            قدر=قدر*10+متن[현재위치++]-'0'; if(++숫자수>3||قدر>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        پتا=پتا<<8|قدر;
        if(부분<3&&(현재위치>=لمبائی_قدر||متن[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=لمبائی_قدر)mp_raise_OSError(MP_EINVAL);
    return پتا;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *دلیل_ایرے) {
    (void)항목수; uint32_t پتا=인터넷주소읽기(دلیل_ایرے[1]);
    int 접속번호=mp_obj_get_int(دلیل_ایرے[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t کوائف;mp_get_buffer_raise(دلیل_ایرے[3],&کوائف,MP_BUFFER_READ);
    struct pk_sockaddr_in ہدف={0};ہدف.sin_family=AF_INET;ہدف.sin_port=pk_htons(접속번호);ہدف.sin_addr.s_addr=pk_htonl(پتا);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(دلیل_ایرے[0]),(uintptr_t)کوائف.buf,کوائف.len,0,(uintptr_t)&ہدف,sizeof(ہدف))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t فائل_نبٹنا) {
    unsigned char کوائف[512]; struct pk_sockaddr_in ہم_سر_قدر; pk_socklen_t لمبائی_کوائف = sizeof(ہم_سر_قدر);
    intptr_t سائز = 결과검사(사용자호출(35, mp_obj_get_int(فائل_نبٹنا), (uintptr_t)کوائف, 512, 0, (uintptr_t)&ہم_سر_قدر, (uintptr_t)&لمبائی_کوائف));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(کوائف, سائز), MP_OBJ_NEW_SMALL_INT(pk_htons(ہم_سر_قدر.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t فائل_نبٹنا) { 결과검사(사용자호출(4, mp_obj_get_int(فائل_نبٹنا), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t بنڑاؤ_سٹریم(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,بدّل_خاندان,سٹریم_نیٹ_ورک,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,بنڑاؤ_سٹریم);
static mp_obj_t جڑو_سٹریم(mp_obj_t 종단,mp_obj_t پتا_متن,mp_obj_t اشاریہ) {
    int 접속번호=mp_obj_get_int(اشاریہ); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 پتا={0}; پتا.پتا_خاندان=بدّل_خاندان;
    پتا.접속번호=망차례짧은수(접속번호); پتا.انٹرنیٹ_پتا.پتا_قدر=نیٹ_ورک_عدد(인터넷주소읽기(پتا_متن));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&پتا,sizeof(پتا),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(سٹریم_کنکٹر_آبجیکٹ,جڑو_سٹریم);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int لمبائی_قدر=mp_obj_get_int(한도); if(لمبائی_قدر<1||لمبائی_قدر>512)mp_raise_OSError(MP_EINVAL);
    unsigned char کوائف[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)کوائف,لمبائی_قدر,0,0,0));
    return mp_obj_new_bytes(کوائف,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(سٹریم_پڑھن_والا_آبجیکٹ,흐름읽기);
static mp_obj_t لکھو_سٹریم(mp_obj_t 종단,mp_obj_t اجزاء_قدر) {
    mp_buffer_info_t کوائف; mp_get_buffer_raise(اجزاء_قدر,&کوائف,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)کوائف.buf,کوائف.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(سٹریم_رائٹر_آبجیکٹ,لکھو_سٹریم);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t ناں) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)راہ_دلیل(ناں),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t بنڑاؤ_ڈائریکٹری(mp_obj_t ناں) {
    결과검사(사용자호출(18,(uintptr_t)راہ_دلیل(ناں),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,بنڑاؤ_ڈائریکٹری);
static mp_obj_t ہٹاؤ_ڈائریکٹری(mp_obj_t ناں) {
    결과검사(사용자호출(18,(uintptr_t)راہ_دلیل(ناں),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ہٹاؤ_ڈائریکٹری);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&سٹریم_کنکٹر_آبجیکٹ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&سٹریم_پڑھن_والا_آبجیکٹ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&سٹریم_رائٹر_آبجیکٹ) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&فائل_پڑھن_والا_آبجیکٹ) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&فائل_رائٹر_آبجیکٹ) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&گھڑی_آبجیکٹ) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
