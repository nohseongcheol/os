// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *경로인수(mp_obj_t 값) {
    size_t 개수; const char *경로 = mp_obj_str_get_data(값, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!경로[순번]) mp_raise_OSError(MP_EINVAL);
    return 경로;
}
static mp_obj_t 파일읽기(mp_obj_t 이름) {
    intptr_t 파일기술자 = 결과검사(사용자호출(3, (uintptr_t)경로인수(이름), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t 크기 = 결과검사(사용자호출(9, 파일기술자, 0, 0, 0, 0, 0));
        vstr_t 자료; vstr_init_len(&자료, 크기);
        intptr_t 결과 = 사용자호출(2, 파일기술자, (uintptr_t)자료.buf, 크기, 0, 0, 0);
        결과검사(결과); 자료.len = 결과;
        mp_obj_t 값 = mp_obj_new_bytes_from_vstr(&자료);
        nlr_pop(); 사용자호출(4, 파일기술자, 0, 0, 0, 0, 0); return 값;
    }
    사용자호출(4, 파일기술자, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(파일읽기객체, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t 크기=mp_obj_get_int(한도);
    if(크기<0||크기>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t 자료; vstr_init_len(&자료,크기);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)자료.buf,크기,0,0,0);
    if(개수<0) { vstr_clear(&자료); 결과검사(개수); }
    자료.len=개수; return mp_obj_new_bytes_from_vstr(&자료);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t 파일쓰기(mp_obj_t 이름, mp_obj_t 내용) {
    const char *경로 = 경로인수(이름);
    mp_buffer_info_t 자료; mp_get_buffer_raise(내용, &자료, MP_BUFFER_READ);
    if (자료.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t 파일기술자 = 결과검사(사용자호출(3, (uintptr_t)경로, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, 파일기술자, (uintptr_t)자료.buf, 자료.len, 0, 0, 0);
    사용자호출(4, 파일기술자, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(파일쓰기객체, 파일쓰기);
static mp_obj_t 파일지우기(mp_obj_t 이름) { 결과검사(사용자호출(11, (uintptr_t)경로인수(이름), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, 파일지우기);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *인수배열) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(인수배열[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t 크기[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, 크기);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t 시계값(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(시계객체, 시계값);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t 파일기술자 = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, 파일기술자, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, 파일기술자, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(파일기술자);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t 파일기술자, mp_obj_t 접속번호, mp_obj_t 내용) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t 자료; mp_get_buffer_raise(내용, &자료, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(파일기술자), (uintptr_t)자료.buf, 자료.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t 값) {
    size_t 길이; const char *Tekst=mp_obj_str_get_data(값,&길이);
    unsigned 현재위치=0; uint32_t 주소=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned 값=0,숫자수=0;
        while(현재위치<길이&&Tekst[현재위치]>='0'&&Tekst[현재위치]<='9') {
            값=값*10+Tekst[현재위치++]-'0'; if(++숫자수>3||값>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        주소=주소<<8|값;
        if(부분<3&&(현재위치>=길이||Tekst[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=길이)mp_raise_OSError(MP_EINVAL);
    return 주소;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *인수배열) {
    (void)항목수; uint32_t 주소=인터넷주소읽기(인수배열[1]);
    int 접속번호=mp_obj_get_int(인수배열[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t 자료;mp_get_buffer_raise(인수배열[3],&자료,MP_BUFFER_READ);
    struct pk_sockaddr_in 대상={0};대상.sin_family=AF_INET;대상.sin_port=pk_htons(접속번호);대상.sin_addr.s_addr=pk_htonl(주소);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(인수배열[0]),(uintptr_t)자료.buf,자료.len,0,(uintptr_t)&대상,sizeof(대상))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t 파일기술자) {
    unsigned char 자료[512]; struct pk_sockaddr_in 상대; pk_socklen_t 길이값 = sizeof(상대);
    intptr_t 크기 = 결과검사(사용자호출(35, mp_obj_get_int(파일기술자), (uintptr_t)자료, 512, 0, (uintptr_t)&상대, (uintptr_t)&길이값));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(자료, 크기), MP_OBJ_NEW_SMALL_INT(pk_htons(상대.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t 파일기술자) { 결과검사(사용자호출(4, mp_obj_get_int(파일기술자), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t 흐름열기(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,인터넷주소갈래,흐름통신,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,흐름열기);
static mp_obj_t 흐름연결(mp_obj_t 종단,mp_obj_t 주소글,mp_obj_t 번호) {
    int 접속번호=mp_obj_get_int(번호); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 주소={0}; 주소.주소갈래=인터넷주소갈래;
    주소.접속번호=망차례짧은수(접속번호); 주소.인터넷주소.주소값=망차례정수(인터넷주소읽기(주소글));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&주소,sizeof(주소),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(흐름연결객체,흐름연결);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int 길이=mp_obj_get_int(한도); if(길이<1||길이>512)mp_raise_OSError(MP_EINVAL);
    unsigned char 자료[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)자료,길이,0,0,0));
    return mp_obj_new_bytes(자료,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(흐름읽기객체,흐름읽기);
static mp_obj_t 흐름쓰기(mp_obj_t 종단,mp_obj_t 내용) {
    mp_buffer_info_t 자료; mp_get_buffer_raise(내용,&자료,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)자료.buf,자료.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(흐름쓰기객체,흐름쓰기);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t 이름) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)경로인수(이름),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t 폴더만들기(mp_obj_t 이름) {
    결과검사(사용자호출(18,(uintptr_t)경로인수(이름),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,폴더만들기);
static mp_obj_t 폴더지우기(mp_obj_t 이름) {
    결과검사(사용자호출(18,(uintptr_t)경로인수(이름),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,폴더지우기);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&흐름연결객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&흐름읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&흐름쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&파일읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&파일쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&시계객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
