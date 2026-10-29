// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *راههه_دليل(mp_obj_t قدر) {
    size_t 개수; const char *راههه = mp_obj_str_get_data(قدر, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!راههه[순번]) mp_raise_OSError(MP_EINVAL);
    return راههه;
}
static mp_obj_t 파일읽기(mp_obj_t نالو) {
    intptr_t فائل_منهن_ڏيڻ = 결과검사(사용자호출(3, (uintptr_t)راههه_دليل(نالو), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t سائيز = 결과검사(사용자호출(9, فائل_منهن_ڏيڻ, 0, 0, 0, 0, 0));
        vstr_t ڪوائف; vstr_init_len(&ڪوائف, سائيز);
        intptr_t 결과 = 사용자호출(2, فائل_منهن_ڏيڻ, (uintptr_t)ڪوائف.buf, سائيز, 0, 0, 0);
        결과검사(결과); ڪوائف.len = 결과;
        mp_obj_t قدر = mp_obj_new_bytes_from_vstr(&ڪوائف);
        nlr_pop(); 사용자호출(4, فائل_منهن_ڏيڻ, 0, 0, 0, 0, 0); return قدر;
    }
    사용자호출(4, فائل_منهن_ڏيڻ, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(فائل_ريڊر_عنصر, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t سائيز=mp_obj_get_int(한도);
    if(سائيز<0||سائيز>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t ڪوائف; vstr_init_len(&ڪوائف,سائيز);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)ڪوائف.buf,سائيز,0,0,0);
    if(개수<0) { vstr_clear(&ڪوائف); 결과검사(개수); }
    ڪوائف.len=개수; return mp_obj_new_bytes_from_vstr(&ڪوائف);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t لکو_فائل(mp_obj_t نالو, mp_obj_t مواد_قدر) {
    const char *راههه = راههه_دليل(نالو);
    mp_buffer_info_t ڪوائف; mp_get_buffer_raise(مواد_قدر, &ڪوائف, MP_BUFFER_READ);
    if (ڪوائف.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t فائل_منهن_ڏيڻ = 결과검사(사용자호출(3, (uintptr_t)راههه, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, فائل_منهن_ڏيڻ, (uintptr_t)ڪوائف.buf, ڪوائف.len, 0, 0, 0);
    사용자호출(4, فائل_منهن_ڏيڻ, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(فائل_رائيٽر_عنصر, لکو_فائل);
static mp_obj_t هٽايو_فائل(mp_obj_t نالو) { 결과검사(사용자호출(11, (uintptr_t)راههه_دليل(نالو), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, هٽايو_فائل);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *دليل_ترتيب) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(دليل_ترتيب[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t سائيز[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, سائيز);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t گهڙي_قدر(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(گهڙي_عنصر, گهڙي_قدر);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t فائل_منهن_ڏيڻ = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, فائل_منهن_ڏيڻ, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, فائل_منهن_ڏيڻ, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(فائل_منهن_ڏيڻ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t فائل_منهن_ڏيڻ, mp_obj_t 접속번호, mp_obj_t مواد_قدر) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ڪوائف; mp_get_buffer_raise(مواد_قدر, &ڪوائف, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(فائل_منهن_ڏيڻ), (uintptr_t)ڪوائف.buf, ڪوائف.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t قدر) {
    size_t لمبائي_قدر; const char *متن=mp_obj_str_get_data(قدر,&لمبائي_قدر);
    unsigned 현재위치=0; uint32_t پتو=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned قدر=0,숫자수=0;
        while(현재위치<لمبائي_قدر&&متن[현재위치]>='0'&&متن[현재위치]<='9') {
            قدر=قدر*10+متن[현재위치++]-'0'; if(++숫자수>3||قدر>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        پتو=پتو<<8|قدر;
        if(부분<3&&(현재위치>=لمبائي_قدر||متن[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=لمبائي_قدر)mp_raise_OSError(MP_EINVAL);
    return پتو;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *دليل_ترتيب) {
    (void)항목수; uint32_t پتو=인터넷주소읽기(دليل_ترتيب[1]);
    int 접속번호=mp_obj_get_int(دليل_ترتيب[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ڪوائف;mp_get_buffer_raise(دليل_ترتيب[3],&ڪوائف,MP_BUFFER_READ);
    struct pk_sockaddr_in هدف={0};هدف.sin_family=AF_INET;هدف.sin_port=pk_htons(접속번호);هدف.sin_addr.s_addr=pk_htonl(پتو);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(دليل_ترتيب[0]),(uintptr_t)ڪوائف.buf,ڪوائف.len,0,(uintptr_t)&هدف,sizeof(هدف))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t فائل_منهن_ڏيڻ) {
    unsigned char ڪوائف[512]; struct pk_sockaddr_in همعصر_قدر; pk_socklen_t لمبائي_ڪوائف = sizeof(همعصر_قدر);
    intptr_t سائيز = 결과검사(사용자호출(35, mp_obj_get_int(فائل_منهن_ڏيڻ), (uintptr_t)ڪوائف, 512, 0, (uintptr_t)&همعصر_قدر, (uintptr_t)&لمبائي_ڪوائف));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(ڪوائف, سائيز), MP_OBJ_NEW_SMALL_INT(pk_htons(همعصر_قدر.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t فائل_منهن_ڏيڻ) { 결과검사(사용자호출(4, mp_obj_get_int(فائل_منهن_ڏيڻ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t ٺاھيو_اسٽريم(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,ڪلائوڊ_خاندان,اسٽريم_نيٽ_ورڪ,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ٺاھيو_اسٽريم);
static mp_obj_t ڪنيڪٽ_اسٽريم(mp_obj_t 종단,mp_obj_t پتو_متن,mp_obj_t ابتدائي) {
    int 접속번호=mp_obj_get_int(ابتدائي); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 پتو={0}; پتو.پتو_خاندان=ڪلائوڊ_خاندان;
    پتو.접속번호=망차례짧은수(접속번호); پتو.انٽرنيٽ_پتو.پتو_قدر=نيٽ_ورڪ_عدد_صحيح(인터넷주소읽기(پتو_متن));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&پتو,sizeof(پتو),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(اسٽريم_ڪنڪٽر_عنصر,ڪنيڪٽ_اسٽريم);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int لمبائي_قدر=mp_obj_get_int(한도); if(لمبائي_قدر<1||لمبائي_قدر>512)mp_raise_OSError(MP_EINVAL);
    unsigned char ڪوائف[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)ڪوائف,لمبائي_قدر,0,0,0));
    return mp_obj_new_bytes(ڪوائف,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(اسٽريم_ريڊر_عنصر,흐름읽기);
static mp_obj_t لکو_اسٽريم(mp_obj_t 종단,mp_obj_t مواد_قدر) {
    mp_buffer_info_t ڪوائف; mp_get_buffer_raise(مواد_قدر,&ڪوائف,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)ڪوائف.buf,ڪوائف.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(اسٽريم_رائيٽر_عنصر,لکو_اسٽريم);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t نالو) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)راههه_دليل(نالو),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t ٺاھيو_ڊائريڪٽري(mp_obj_t نالو) {
    결과검사(사용자호출(18,(uintptr_t)راههه_دليل(نالو),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,ٺاھيو_ڊائريڪٽري);
static mp_obj_t هٽايو_ڊائريڪٽري(mp_obj_t نالو) {
    결과검사(사용자호출(18,(uintptr_t)راههه_دليل(نالو),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,هٽايو_ڊائريڪٽري);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&اسٽريم_ڪنڪٽر_عنصر) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&اسٽريم_ريڊر_عنصر) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&اسٽريم_رائيٽر_عنصر) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&فائل_ريڊر_عنصر) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&فائل_رائيٽر_عنصر) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&گهڙي_عنصر) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
