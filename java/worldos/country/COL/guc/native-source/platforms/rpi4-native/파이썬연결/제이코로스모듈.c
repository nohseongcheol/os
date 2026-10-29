// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *wopu_a_ttaaleemüin_ajutuu_23a4b1a4(mp_obj_t ajutuu) {
    size_t 개수; const char *wopu_a_ttaaleemüin = mp_obj_str_get_data(ajutuu, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!wopu_a_ttaaleemüin[순번]) mp_raise_OSError(MP_EINVAL);
    return wopu_a_ttaaleemüin;
}
static mp_obj_t 파일읽기(mp_obj_t 이름) {
    intptr_t anaajaalaa_aapaaya = 결과검사(사용자호출(3, (uintptr_t)wopu_a_ttaaleemüin_ajutuu_23a4b1a4(이름), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t 크기 = 결과검사(사용자호출(9, anaajaalaa_aapaaya, 0, 0, 0, 0, 0));
        vstr_t atijaaya; vstr_init_len(&atijaaya, 크기);
        intptr_t 결과 = 사용자호출(2, anaajaalaa_aapaaya, (uintptr_t)atijaaya.buf, 크기, 0, 0, 0);
        결과검사(결과); atijaaya.len = 결과;
        mp_obj_t ajutuu = mp_obj_new_bytes_from_vstr(&atijaaya);
        nlr_pop(); 사용자호출(4, anaajaalaa_aapaaya, 0, 0, 0, 0, 0); return ajutuu;
    }
    사용자호출(4, anaajaalaa_aapaaya, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(파일읽기객체, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t 크기=mp_obj_get_int(한도);
    if(크기<0||크기>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t atijaaya; vstr_init_len(&atijaaya,크기);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)atijaaya.buf,크기,0,0,0);
    if(개수<0) { vstr_clear(&atijaaya); 결과검사(개수); }
    atijaaya.len=개수; return mp_obj_new_bytes_from_vstr(&atijaaya);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t ashajaa_anaajaalaa(mp_obj_t 이름, mp_obj_t alu_ujatüü_ajutuu) {
    const char *wopu_a_ttaaleemüin = wopu_a_ttaaleemüin_ajutuu_23a4b1a4(이름);
    mp_buffer_info_t atijaaya; mp_get_buffer_raise(alu_ujatüü_ajutuu, &atijaaya, MP_BUFFER_READ);
    if (atijaaya.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t anaajaalaa_aapaaya = 결과검사(사용자호출(3, (uintptr_t)wopu_a_ttaaleemüin, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, anaajaalaa_aapaaya, (uintptr_t)atijaaya.buf, atijaaya.len, 0, 0, 0);
    사용자호출(4, anaajaalaa_aapaaya, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(파일쓰기객체, ashajaa_anaajaalaa);
static mp_obj_t 파일지우기(mp_obj_t 이름) { 결과검사(사용자호출(11, (uintptr_t)wopu_a_ttaaleemüin_ajutuu_23a4b1a4(이름), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, 파일지우기);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *ajutuu_matüriisü) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(ajutuu_matüriisü[순번]);
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
static mp_obj_t ka_iyaawatia_ajutuu(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(시계객체, ka_iyaawatia_ajutuu);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t anaajaalaa_aapaaya = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, anaajaalaa_aapaaya, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, anaajaalaa_aapaaya, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(anaajaalaa_aapaaya);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t anaajaalaa_aapaaya, mp_obj_t 접속번호, mp_obj_t alu_ujatüü_ajutuu) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t atijaaya; mp_get_buffer_raise(alu_ujatüü_ajutuu, &atijaaya, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(anaajaalaa_aapaaya), (uintptr_t)atijaaya.buf, atijaaya.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t ajutuu) {
    size_t akaliaa_ajutuu; const char *글=mp_obj_str_get_data(ajutuu,&akaliaa_ajutuu);
    unsigned 현재위치=0; uint32_t ejepüsee=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned ajutuu=0,숫자수=0;
        while(현재위치<akaliaa_ajutuu&&글[현재위치]>='0'&&글[현재위치]<='9') {
            ajutuu=ajutuu*10+글[현재위치++]-'0'; if(++숫자수>3||ajutuu>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        ejepüsee=ejepüsee<<8|ajutuu;
        if(부분<3&&(현재위치>=akaliaa_ajutuu||글[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=akaliaa_ajutuu)mp_raise_OSError(MP_EINVAL);
    return ejepüsee;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *ajutuu_matüriisü) {
    (void)항목수; uint32_t ejepüsee=인터넷주소읽기(ajutuu_matüriisü[1]);
    int 접속번호=mp_obj_get_int(ajutuu_matüriisü[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t atijaaya;mp_get_buffer_raise(ajutuu_matüriisü[3],&atijaaya,MP_BUFFER_READ);
    struct pk_sockaddr_in 대상={0};대상.sin_family=AF_INET;대상.sin_port=pk_htons(접속번호);대상.sin_addr.s_addr=pk_htonl(ejepüsee);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(ajutuu_matüriisü[0]),(uintptr_t)atijaaya.buf,atijaaya.len,0,(uintptr_t)&대상,sizeof(대상))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t anaajaalaa_aapaaya) {
    unsigned char atijaaya[512]; struct pk_sockaddr_in wanaawasü_ajutuu; pk_socklen_t akaliaa_atijaaya = sizeof(wanaawasü_ajutuu);
    intptr_t 크기 = 결과검사(사용자호출(35, mp_obj_get_int(anaajaalaa_aapaaya), (uintptr_t)atijaaya, 512, 0, (uintptr_t)&wanaawasü_ajutuu, (uintptr_t)&akaliaa_atijaaya));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(atijaaya, 크기), MP_OBJ_NEW_SMALL_INT(pk_htons(wanaawasü_ajutuu.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t anaajaalaa_aapaaya) { 결과검사(사용자호출(4, mp_obj_get_int(anaajaalaa_aapaaya), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t 흐름열기(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,인터넷주소갈래,palantüsü_kusu,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,흐름열기);
static mp_obj_t a_ataa_palantüsü(mp_obj_t 종단,mp_obj_t 주소글,mp_obj_t ee_iyatialujuna) {
    int 접속번호=mp_obj_get_int(ee_iyatialujuna); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ejepüsee={0}; ejepüsee.주소갈래=인터넷주소갈래;
    ejepüsee.접속번호=망차례짧은수(접속번호); ejepüsee.ejepüsee_Internet.ejepüsee_ajutuu=kusu_waneepiasü(인터넷주소읽기(주소글));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ejepüsee,sizeof(ejepüsee),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(흐름연결객체,a_ataa_palantüsü);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int akaliaa_ajutuu=mp_obj_get_int(한도); if(akaliaa_ajutuu<1||akaliaa_ajutuu>512)mp_raise_OSError(MP_EINVAL);
    unsigned char atijaaya[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)atijaaya,akaliaa_ajutuu,0,0,0));
    return mp_obj_new_bytes(atijaaya,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(흐름읽기객체,흐름읽기);
static mp_obj_t ashajaa_palantüsü(mp_obj_t 종단,mp_obj_t alu_ujatüü_ajutuu) {
    mp_buffer_info_t atijaaya; mp_get_buffer_raise(alu_ujatüü_ajutuu,&atijaaya,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)atijaaya.buf,atijaaya.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(흐름쓰기객체,ashajaa_palantüsü);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t 이름) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)wopu_a_ttaaleemüin_ajutuu_23a4b1a4(이름),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t 폴더만들기(mp_obj_t 이름) {
    결과검사(사용자호출(18,(uintptr_t)wopu_a_ttaaleemüin_ajutuu_23a4b1a4(이름),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,폴더만들기);
static mp_obj_t 폴더지우기(mp_obj_t 이름) {
    결과검사(사용자호출(18,(uintptr_t)wopu_a_ttaaleemüin_ajutuu_23a4b1a4(이름),2,0,0,0,0)); return mp_const_none;
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
