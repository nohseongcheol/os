// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t પરિમાણ) { if (પરિમાણ < 0) mp_raise_OSError(-પરિમાણ); return પરિમાણ; }
static const char *પાથ_દલીલ(mp_obj_t મૂલ્ય) {
    size_t 개수; const char *પથ = mp_obj_str_get_data(મૂલ્ય, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!પથ[순번]) mp_raise_OSError(MP_EINVAL);
    return પથ;
}
static mp_obj_t 파일읽기(mp_obj_t નામ) {
    intptr_t ફાઇલ_હેન્ડલ = 결과검사(사용자호출(3, (uintptr_t)પાથ_દલીલ(નામ), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t માપ = 결과검사(사용자호출(9, ફાઇલ_હેન્ડલ, 0, 0, 0, 0, 0));
        vstr_t ડેટા; vstr_init_len(&ડેટા, માપ);
        intptr_t પરિમાણ = 사용자호출(2, ફાઇલ_હેન્ડલ, (uintptr_t)ડેટા.buf, માપ, 0, 0, 0);
        결과검사(પરિમાણ); ડેટા.len = પરિમાણ;
        mp_obj_t મૂલ્ય = mp_obj_new_bytes_from_vstr(&ડેટા);
        nlr_pop(); 사용자호출(4, ફાઇલ_હેન્ડલ, 0, 0, 0, 0, 0); return મૂલ્ય;
    }
    사용자호출(4, ફાઇલ_હેન્ડલ, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ફાઇલ_રીડર_ઑબ્જેક્ટ, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t માપ=mp_obj_get_int(한도);
    if(માપ<0||માપ>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t ડેટા; vstr_init_len(&ડેટા,માપ);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)ડેટા.buf,માપ,0,0,0);
    if(개수<0) { vstr_clear(&ડેટા); 결과검사(개수); }
    ડેટા.len=개수; return mp_obj_new_bytes_from_vstr(&ડેટા);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t લખો_ફાઇલ(mp_obj_t નામ, mp_obj_t સામગ્રી_મૂલ્ય) {
    const char *પથ = પાથ_દલીલ(નામ);
    mp_buffer_info_t ડેટા; mp_get_buffer_raise(સામગ્રી_મૂલ્ય, &ડેટા, MP_BUFFER_READ);
    if (ડેટા.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ફાઇલ_હેન્ડલ = 결과검사(사용자호출(3, (uintptr_t)પથ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ફાઇલ_હેન્ડલ, (uintptr_t)ડેટા.buf, ડેટા.len, 0, 0, 0);
    사용자호출(4, ફાઇલ_હેન્ડલ, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(파일쓰기객체, લખો_ફાઇલ);
static mp_obj_t કાઢી_નાંખો_ફાઇલ(mp_obj_t નામ) { 결과검사(사용자호출(11, (uintptr_t)પાથ_દલીલ(નામ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, કાઢી_નાંખો_ફાઇલ);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *દલીલ_અરે) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(દલીલ_અરે[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t માપ[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, માપ);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t ઘડિયાળ_મૂલ્ય(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(ઘડિયાળ_ઑબ્જેક્ટ, ઘડિયાળ_મૂલ્ય);
static mp_obj_t 전문열기(mp_obj_t પોર્ટ_નંબર) {
    int ડેટા_સ્થિતિ = mp_obj_get_int(પોર્ટ_નંબર); if (ડેટા_સ્થિતિ < 0 || ડેટા_સ્થિતિ > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ફાઇલ_હેન્ડલ = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ડેટા_સ્થિતિ); 첫째값.sin_addr.s_addr = 0;
    intptr_t પરિમાણ = 사용자호출(33, ફાઇલ_હેન્ડલ, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (પરિમાણ < 0) { 사용자호출(4, ફાઇલ_હેન્ડલ, 0, 0, 0, 0, 0); 결과검사(પરિમાણ); }
    return mp_obj_new_int(ફાઇલ_હેન્ડલ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ફાઇલ_હેન્ડલ, mp_obj_t પોર્ટ_નંબર, mp_obj_t સામગ્રી_મૂલ્ય) {
    int ડેટા_સ્થિતિ = mp_obj_get_int(પોર્ટ_નંબર); if (ડેટા_સ્થિતિ < 1 || ડેટા_સ્થિતિ > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ડેટા; mp_get_buffer_raise(સામગ્રી_મૂલ્ય, &ડેટા, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ડેટા_સ્થિતિ); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ફાઇલ_હેન્ડલ), (uintptr_t)ડેટા.buf, ડેટા.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t મૂલ્ય) {
    size_t લંબાઈ_મૂલ્ય; const char *લખાણ=mp_obj_str_get_data(મૂલ્ય,&લંબાઈ_મૂલ્ય);
    unsigned 현재위치=0; uint32_t સરનામું=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned મૂલ્ય=0,숫자수=0;
        while(현재위치<લંબાઈ_મૂલ્ય&&લખાણ[현재위치]>='0'&&લખાણ[현재위치]<='9') {
            મૂલ્ય=મૂલ્ય*10+લખાણ[현재위치++]-'0'; if(++숫자수>3||મૂલ્ય>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        સરનામું=સરનામું<<8|મૂલ્ય;
        if(부분<3&&(현재위치>=લંબાઈ_મૂલ્ય||લખાણ[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=લંબાઈ_મૂલ્ય)mp_raise_OSError(MP_EINVAL);
    return સરનામું;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *દલીલ_અરે) {
    (void)항목수; uint32_t સરનામું=인터넷주소읽기(દલીલ_અરે[1]);
    int પોર્ટ_નંબર=mp_obj_get_int(દલીલ_અરે[2]);if(પોર્ટ_નંબર<1||પોર્ટ_નંબર>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ડેટા;mp_get_buffer_raise(દલીલ_અરે[3],&ડેટા,MP_BUFFER_READ);
    struct pk_sockaddr_in લક્ષ્ય={0};લક્ષ્ય.sin_family=AF_INET;લક્ષ્ય.sin_port=pk_htons(પોર્ટ_નંબર);લક્ષ્ય.sin_addr.s_addr=pk_htonl(સરનામું);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(દલીલ_અરે[0]),(uintptr_t)ડેટા.buf,ડેટા.len,0,(uintptr_t)&લક્ષ્ય,sizeof(લક્ષ્ય))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ફાઇલ_હેન્ડલ) {
    unsigned char ડેટા[512]; struct pk_sockaddr_in પીઅર_મૂલ્ય; pk_socklen_t લંબાઈ_ડેટા = sizeof(પીઅર_મૂલ્ય);
    intptr_t માપ = 결과검사(사용자호출(35, mp_obj_get_int(ફાઇલ_હેન્ડલ), (uintptr_t)ડેટા, 512, 0, (uintptr_t)&પીઅર_મૂલ્ય, (uintptr_t)&લંબાઈ_ડેટા));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(ડેટા, માપ), MP_OBJ_NEW_SMALL_INT(pk_htons(પીઅર_મૂલ્ય.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ફાઇલ_હેન્ડલ) { 결과검사(사용자호출(4, mp_obj_get_int(ફાઇલ_હેન્ડલ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t બનાવો_સ્ટ્રીમ(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,ક્લાઉડ_કુટુંબ,સ્ટ્રીમ_નેટવર્ક,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,બનાવો_સ્ટ્રીમ);
static mp_obj_t કનેક્ટ_સ્ટ્રીમ(mp_obj_t 종단,mp_obj_t સરનામું_પાઠ,mp_obj_t અનુક્રમણિકા) {
    int પોર્ટ_નંબર=mp_obj_get_int(અનુક્રમણિકા); if(પોર્ટ_નંબર<1||પોર્ટ_નંબર>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 સરનામું={0}; સરનામું.સરનામું_કુટુંબ=ક્લાઉડ_કુટુંબ;
    સરનામું.પોર્ટ_નંબર=망차례짧은수(પોર્ટ_નંબર); સરનામું.ઇન્ટરનેટ_સરનામું.સરનામું_મૂલ્ય=નેટવર્ક_પૂર્ણાંક(인터넷주소읽기(સરનામું_પાઠ));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&સરનામું,sizeof(સરનામું),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(સ્ટ્રીમ_કનેક્ટર_ઑબ્જેક્ટ,કનેક્ટ_સ્ટ્રીમ);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int લંબાઈ_મૂલ્ય=mp_obj_get_int(한도); if(લંબાઈ_મૂલ્ય<1||લંબાઈ_મૂલ્ય>512)mp_raise_OSError(MP_EINVAL);
    unsigned char ડેટા[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)ડેટા,લંબાઈ_મૂલ્ય,0,0,0));
    return mp_obj_new_bytes(ડેટા,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(સ્ટ્રીમ_રીડર_ઑબ્જેક્ટ,흐름읽기);
static mp_obj_t લખો_સ્ટ્રીમ(mp_obj_t 종단,mp_obj_t સામગ્રી_મૂલ્ય) {
    mp_buffer_info_t ડેટા; mp_get_buffer_raise(સામગ્રી_મૂલ્ય,&ડેટા,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)ડેટા.buf,ડેટા.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(흐름쓰기객체,લખો_સ્ટ્રીમ);
static mp_obj_t 잠시기다리기(mp_obj_t સમય_મૂલ્ય) {
    결과검사(사용자호출(17,mp_obj_get_int(સમય_મૂલ્ય),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(પ્રતીક્ષા_ઑબ્જેક્ટ,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t નામ) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)પાથ_દલીલ(નામ),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t બનાવો_નિર્દેશિકા(mp_obj_t નામ) {
    결과검사(사용자호출(18,(uintptr_t)પાથ_દલીલ(નામ),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(નિર્દેશિકા_ક્રિએટર_ઑબ્જેક્ટ,બનાવો_નિર્દેશિકા);
static mp_obj_t કાઢી_નાંખો_નિર્દેશિકા(mp_obj_t નામ) {
    결과검사(사용자호출(18,(uintptr_t)પાથ_દલીલ(નામ),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,કાઢી_નાંખો_નિર્દેશિકા);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&સ્ટ્રીમ_કનેક્ટર_ઑબ્જેક્ટ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&સ્ટ્રીમ_રીડર_ઑબ્જેક્ટ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&흐름쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&પ્રતીક્ષા_ઑબ્જેક્ટ) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&નિર્દેશિકા_ક્રિએટર_ઑબ્જેક્ટ) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ફાઇલ_રીડર_ઑબ્જેક્ટ) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&파일쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&ઘડિયાળ_ઑબ્જેક્ટ) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
