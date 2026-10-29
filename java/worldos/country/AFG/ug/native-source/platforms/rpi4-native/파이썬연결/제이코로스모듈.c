// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t ئۆلچەم) { if (ئۆلچەم < 0) mp_raise_OSError(-ئۆلچەم); return ئۆلچەم; }
static const char *يول_دەلىل(mp_obj_t قىممىتى) {
    size_t 개수; const char *يول = mp_obj_str_get_data(قىممىتى, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!يول[순번]) mp_raise_OSError(MP_EINVAL);
    return يول;
}
static mp_obj_t 파일읽기(mp_obj_t ئاتى) {
    intptr_t ھۆججەت_تۇتقۇچ = 결과검사(사용자호출(3, (uintptr_t)يول_دەلىل(ئاتى), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t چوڭلۇقى = 결과검사(사용자호출(9, ھۆججەت_تۇتقۇچ, 0, 0, 0, 0, 0));
        vstr_t مەلۇمات; vstr_init_len(&مەلۇمات, چوڭلۇقى);
        intptr_t ئۆلچەم = 사용자호출(2, ھۆججەت_تۇتقۇچ, (uintptr_t)مەلۇمات.buf, چوڭلۇقى, 0, 0, 0);
        결과검사(ئۆلچەم); مەلۇمات.len = ئۆلچەم;
        mp_obj_t قىممىتى = mp_obj_new_bytes_from_vstr(&مەلۇمات);
        nlr_pop(); 사용자호출(4, ھۆججەت_تۇتقۇچ, 0, 0, 0, 0, 0); return قىممىتى;
    }
    사용자호출(4, ھۆججەت_تۇتقۇچ, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ھۆججەت_ئوقۇغۇچ_ئوبيېكت, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t چوڭلۇقى=mp_obj_get_int(한도);
    if(چوڭلۇقى<0||چوڭلۇقى>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t مەلۇمات; vstr_init_len(&مەلۇمات,چوڭلۇقى);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)مەلۇمات.buf,چوڭلۇقى,0,0,0);
    if(개수<0) { vstr_clear(&مەلۇمات); 결과검사(개수); }
    مەلۇمات.len=개수; return mp_obj_new_bytes_from_vstr(&مەلۇمات);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t يازماق_ھۆججەت(mp_obj_t ئاتى, mp_obj_t مەزمۇن_قىممىتى) {
    const char *يول = يول_دەلىل(ئاتى);
    mp_buffer_info_t مەلۇمات; mp_get_buffer_raise(مەزمۇن_قىممىتى, &مەلۇمات, MP_BUFFER_READ);
    if (مەلۇمات.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ھۆججەت_تۇتقۇچ = 결과검사(사용자호출(3, (uintptr_t)يول, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ھۆججەت_تۇتقۇچ, (uintptr_t)مەلۇمات.buf, مەلۇمات.len, 0, 0, 0);
    사용자호출(4, ھۆججەت_تۇتقۇچ, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ھۆججەت_يازغۇچ_ئوبيېكت, يازماق_ھۆججەت);
static mp_obj_t چىقىرىۋەتمەك_ھۆججەت(mp_obj_t ئاتى) { 결과검사(사용자호출(11, (uintptr_t)يول_دەلىل(ئاتى), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, چىقىرىۋەتمەك_ھۆججەت);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *دەلىل_رەت) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(دەلىل_رەت[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t چوڭلۇقى[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, چوڭلۇقى);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t سائەت_قىممىتى(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(سائەت_ئوبيېكت, سائەت_قىممىتى);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int مەلۇمات_ئورۇنلاشتۇرۇش = mp_obj_get_int(접속번호); if (مەلۇمات_ئورۇنلاشتۇرۇش < 0 || مەلۇمات_ئورۇنلاشتۇرۇش > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ھۆججەت_تۇتقۇچ = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(مەلۇمات_ئورۇنلاشتۇرۇش); 첫째값.sin_addr.s_addr = 0;
    intptr_t ئۆلچەم = 사용자호출(33, ھۆججەت_تۇتقۇچ, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (ئۆلچەم < 0) { 사용자호출(4, ھۆججەت_تۇتقۇچ, 0, 0, 0, 0, 0); 결과검사(ئۆلچەم); }
    return mp_obj_new_int(ھۆججەت_تۇتقۇچ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ھۆججەت_تۇتقۇچ, mp_obj_t 접속번호, mp_obj_t مەزمۇن_قىممىتى) {
    int مەلۇمات_ئورۇنلاشتۇرۇش = mp_obj_get_int(접속번호); if (مەلۇمات_ئورۇنلاشتۇرۇش < 1 || مەلۇمات_ئورۇنلاشتۇرۇش > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t مەلۇمات; mp_get_buffer_raise(مەزمۇن_قىممىتى, &مەلۇمات, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(مەلۇمات_ئورۇنلاشتۇرۇش); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ھۆججەت_تۇتقۇچ), (uintptr_t)مەلۇمات.buf, مەلۇمات.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t قىممىتى) {
    size_t ئۇزۇنلۇق_قىممىتى; const char *تېكىست=mp_obj_str_get_data(قىممىتى,&ئۇزۇنلۇق_قىممىتى);
    unsigned 현재위치=0; uint32_t ئادرېس=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned قىممىتى=0,숫자수=0;
        while(현재위치<ئۇزۇنلۇق_قىممىتى&&تېكىست[현재위치]>='0'&&تېكىست[현재위치]<='9') {
            قىممىتى=قىممىتى*10+تېكىست[현재위치++]-'0'; if(++숫자수>3||قىممىتى>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        ئادرېس=ئادرېس<<8|قىممىتى;
        if(부분<3&&(현재위치>=ئۇزۇنلۇق_قىممىتى||تېكىست[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=ئۇزۇنلۇق_قىممىتى)mp_raise_OSError(MP_EINVAL);
    return ئادرېس;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *دەلىل_رەت) {
    (void)항목수; uint32_t ئادرېس=인터넷주소읽기(دەلىل_رەت[1]);
    int 접속번호=mp_obj_get_int(دەلىل_رەت[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t مەلۇمات;mp_get_buffer_raise(دەلىل_رەت[3],&مەلۇمات,MP_BUFFER_READ);
    struct pk_sockaddr_in نىشان={0};نىشان.sin_family=AF_INET;نىشان.sin_port=pk_htons(접속번호);نىشان.sin_addr.s_addr=pk_htonl(ئادرېس);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(دەلىل_رەت[0]),(uintptr_t)مەلۇمات.buf,مەلۇمات.len,0,(uintptr_t)&نىشان,sizeof(نىشان))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ھۆججەت_تۇتقۇچ) {
    unsigned char مەلۇمات[512]; struct pk_sockaddr_in باراۋەرلىك_قىممىتى; pk_socklen_t ئۇزۇنلۇق_مەلۇمات = sizeof(باراۋەرلىك_قىممىتى);
    intptr_t چوڭلۇقى = 결과검사(사용자호출(35, mp_obj_get_int(ھۆججەت_تۇتقۇچ), (uintptr_t)مەلۇمات, 512, 0, (uintptr_t)&باراۋەرلىك_قىممىتى, (uintptr_t)&ئۇزۇنلۇق_مەلۇمات));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(مەلۇمات, چوڭلۇقى), MP_OBJ_NEW_SMALL_INT(pk_htons(باراۋەرلىك_قىممىتى.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ھۆججەت_تۇتقۇچ) { 결과검사(사용자호출(4, mp_obj_get_int(ھۆججەت_تۇتقۇچ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t قۇرۇش_ئېقىم(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,بۇلۇت_ئائىلە,ئېقىم_تور,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,قۇرۇش_ئېقىم);
static mp_obj_t ئۇلاش_ئېقىم(mp_obj_t 종단,mp_obj_t ئادرېس_تېكست,mp_obj_t ئىندېكس) {
    int 접속번호=mp_obj_get_int(ئىندېكس); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ئادرېس={0}; ئادرېس.ئادرېس_ئائىلە=بۇلۇت_ئائىلە;
    ئادرېس.접속번호=망차례짧은수(접속번호); ئادرېس.ئىنتېرنېت_ئادرېسى.ئادرېس_قىممىتى=تور_پۈتۈن_سان(인터넷주소읽기(ئادرېس_تېكست));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ئادرېس,sizeof(ئادرېس),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ئېقىم_ئۇلىغۇچ_ئوبيېكت,ئۇلاش_ئېقىم);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int ئۇزۇنلۇق_قىممىتى=mp_obj_get_int(한도); if(ئۇزۇنلۇق_قىممىتى<1||ئۇزۇنلۇق_قىممىتى>512)mp_raise_OSError(MP_EINVAL);
    unsigned char مەلۇمات[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)مەلۇمات,ئۇزۇنلۇق_قىممىتى,0,0,0));
    return mp_obj_new_bytes(مەلۇمات,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ئېقىم_ئوقۇغۇچ_ئوبيېكت,흐름읽기);
static mp_obj_t يازماق_ئېقىم(mp_obj_t 종단,mp_obj_t مەزمۇن_قىممىتى) {
    mp_buffer_info_t مەلۇمات; mp_get_buffer_raise(مەزمۇن_قىممىتى,&مەلۇمات,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)مەلۇمات.buf,مەلۇمات.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ئېقىم_يازغۇچ_ئوبيېكت,يازماق_ئېقىم);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t ئاتى) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)يول_دەلىل(ئاتى),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t قۇرۇش_مۇندەرىجە(mp_obj_t ئاتى) {
    결과검사(사용자호출(18,(uintptr_t)يول_دەلىل(ئاتى),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(مۇندەرىجە_ئىجادكار_ئوبيېكت,قۇرۇش_مۇندەرىجە);
static mp_obj_t چىقىرىۋەتمەك_مۇندەرىجە(mp_obj_t ئاتى) {
    결과검사(사용자호출(18,(uintptr_t)يول_دەلىل(ئاتى),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,چىقىرىۋەتمەك_مۇندەرىجە);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ئېقىم_ئۇلىغۇچ_ئوبيېكت) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ئېقىم_ئوقۇغۇچ_ئوبيېكت) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&ئېقىم_يازغۇچ_ئوبيېكت) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&مۇندەرىجە_ئىجادكار_ئوبيېكت) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ھۆججەت_ئوقۇغۇچ_ئوبيېكت) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ھۆججەت_يازغۇچ_ئوبيېكت) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&سائەت_ئوبيېكت) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
