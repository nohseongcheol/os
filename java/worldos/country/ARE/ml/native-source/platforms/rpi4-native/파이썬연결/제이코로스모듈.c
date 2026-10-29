// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t അളവ്) { if (അളവ് < 0) mp_raise_OSError(-അളവ്); return അളവ്; }
static const char *പാത_ആര്_ഗ്യുമെന്_റ്(mp_obj_t മൂല്യം) {
    size_t 개수; const char *വഴി = mp_obj_str_get_data(മൂല്യം, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!വഴി[순번]) mp_raise_OSError(MP_EINVAL);
    return വഴി;
}
static mp_obj_t 파일읽기(mp_obj_t പേരു്) {
    intptr_t ഫയല്_കൈകാര്യംചെയ്യല് = 결과검사(사용자호출(3, (uintptr_t)പാത_ആര്_ഗ്യുമെന്_റ്(പേരു്), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t വലിപ്പം = 결과검사(사용자호출(9, ഫയല്_കൈകാര്യംചെയ്യല്, 0, 0, 0, 0, 0));
        vstr_t ഡാറ്റാ; vstr_init_len(&ഡാറ്റാ, വലിപ്പം);
        intptr_t അളവ് = 사용자호출(2, ഫയല്_കൈകാര്യംചെയ്യല്, (uintptr_t)ഡാറ്റാ.buf, വലിപ്പം, 0, 0, 0);
        결과검사(അളവ്); ഡാറ്റാ.len = അളവ്;
        mp_obj_t മൂല്യം = mp_obj_new_bytes_from_vstr(&ഡാറ്റാ);
        nlr_pop(); 사용자호출(4, ഫയല്_കൈകാര്യംചെയ്യല്, 0, 0, 0, 0, 0); return മൂല്യം;
    }
    사용자호출(4, ഫയല്_കൈകാര്യംചെയ്യല്, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ഫയല്_റീഡര്_ഓബ്ജക്റ്റ്, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t വലിപ്പം=mp_obj_get_int(한도);
    if(വലിപ്പം<0||വലിപ്പം>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t ഡാറ്റാ; vstr_init_len(&ഡാറ്റാ,വലിപ്പം);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)ഡാറ്റാ.buf,വലിപ്പം,0,0,0);
    if(개수<0) { vstr_clear(&ഡാറ്റാ); 결과검사(개수); }
    ഡാറ്റാ.len=개수; return mp_obj_new_bytes_from_vstr(&ഡാറ്റാ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t റൈറ്റ്_ചെയ്യുക_ഫയല്(mp_obj_t പേരു്, mp_obj_t ഉള്ളടക്കം_മൂല്യം) {
    const char *വഴി = പാത_ആര്_ഗ്യുമെന്_റ്(പേരു്);
    mp_buffer_info_t ഡാറ്റാ; mp_get_buffer_raise(ഉള്ളടക്കം_മൂല്യം, &ഡാറ്റാ, MP_BUFFER_READ);
    if (ഡാറ്റാ.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ഫയല്_കൈകാര്യംചെയ്യല് = 결과검사(사용자호출(3, (uintptr_t)വഴി, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ഫയല്_കൈകാര്യംചെയ്യല്, (uintptr_t)ഡാറ്റാ.buf, ഡാറ്റാ.len, 0, 0, 0);
    사용자호출(4, ഫയല്_കൈകാര്യംചെയ്യല്, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ഫയല്_റൈറ്റര്_ഓബ്ജക്റ്റ്, റൈറ്റ്_ചെയ്യുക_ഫയല്);
static mp_obj_t നീക്കംചെയ്യുക_ഫയല്(mp_obj_t പേരു്) { 결과검사(사용자호출(11, (uintptr_t)പാത_ആര്_ഗ്യുമെന്_റ്(പേരു്), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, നീക്കംചെയ്യുക_ഫയല്);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *ആര്_ഗ്യുമെന്_റ്_അരേ) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(ആര്_ഗ്യുമെന്_റ്_അരേ[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t വലിപ്പം[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, വലിപ്പം);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t ഘടികാരം_മൂല്യം(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(ഘടികാരം_ഓബ്ജക്റ്റ്, ഘടികാരം_മൂല്യം);
static mp_obj_t 전문열기(mp_obj_t പോര്_ട്ട്_നമ്പര്) {
    int ഡാറ്റാ_പദവി = mp_obj_get_int(പോര്_ട്ട്_നമ്പര്); if (ഡാറ്റാ_പദവി < 0 || ഡാറ്റാ_പദവി > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ഫയല്_കൈകാര്യംചെയ്യല് = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ഡാറ്റാ_പദവി); 첫째값.sin_addr.s_addr = 0;
    intptr_t അളവ് = 사용자호출(33, ഫയല്_കൈകാര്യംചെയ്യല്, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (അളവ് < 0) { 사용자호출(4, ഫയല്_കൈകാര്യംചെയ്യല്, 0, 0, 0, 0, 0); 결과검사(അളവ്); }
    return mp_obj_new_int(ഫയല്_കൈകാര്യംചെയ്യല്);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ഫയല്_കൈകാര്യംചെയ്യല്, mp_obj_t പോര്_ട്ട്_നമ്പര്, mp_obj_t ഉള്ളടക്കം_മൂല്യം) {
    int ഡാറ്റാ_പദവി = mp_obj_get_int(പോര്_ട്ട്_നമ്പര്); if (ഡാറ്റാ_പദവി < 1 || ഡാറ്റാ_പദവി > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ഡാറ്റാ; mp_get_buffer_raise(ഉള്ളടക്കം_മൂല്യം, &ഡാറ്റാ, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ഡാറ്റാ_പദവി); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ഫയല്_കൈകാര്യംചെയ്യല്), (uintptr_t)ഡാറ്റാ.buf, ഡാറ്റാ.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t മൂല്യം) {
    size_t ദൈര്_ഘ്യം_മൂല്യം; const char *പദാവലി=mp_obj_str_get_data(മൂല്യം,&ദൈര്_ഘ്യം_മൂല്യം);
    unsigned 현재위치=0; uint32_t ഇമെയിൽ=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned മൂല്യം=0,숫자수=0;
        while(현재위치<ദൈര്_ഘ്യം_മൂല്യം&&പദാവലി[현재위치]>='0'&&പദാവലി[현재위치]<='9') {
            മൂല്യം=മൂല്യം*10+പദാവലി[현재위치++]-'0'; if(++숫자수>3||മൂല്യം>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        ഇമെയിൽ=ഇമെയിൽ<<8|മൂല്യം;
        if(부분<3&&(현재위치>=ദൈര്_ഘ്യം_മൂല്യം||പദാവലി[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=ദൈര്_ഘ്യം_മൂല്യം)mp_raise_OSError(MP_EINVAL);
    return ഇമെയിൽ;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *ആര്_ഗ്യുമെന്_റ്_അരേ) {
    (void)항목수; uint32_t ഇമെയിൽ=인터넷주소읽기(ആര്_ഗ്യുമെന്_റ്_അരേ[1]);
    int പോര്_ട്ട്_നമ്പര്=mp_obj_get_int(ആര്_ഗ്യുമെന്_റ്_അരേ[2]);if(പോര്_ട്ട്_നമ്പര്<1||പോര്_ട്ട്_നമ്പര്>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ഡാറ്റാ;mp_get_buffer_raise(ആര്_ഗ്യുമെന്_റ്_അരേ[3],&ഡാറ്റാ,MP_BUFFER_READ);
    struct pk_sockaddr_in ലക്_ഷ്യം={0};ലക്_ഷ്യം.sin_family=AF_INET;ലക്_ഷ്യം.sin_port=pk_htons(പോര്_ട്ട്_നമ്പര്);ലക്_ഷ്യം.sin_addr.s_addr=pk_htonl(ഇമെയിൽ);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(ആര്_ഗ്യുമെന്_റ്_അരേ[0]),(uintptr_t)ഡാറ്റാ.buf,ഡാറ്റാ.len,0,(uintptr_t)&ലക്_ഷ്യം,sizeof(ലക്_ഷ്യം))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ഫയല്_കൈകാര്യംചെയ്യല്) {
    unsigned char ഡാറ്റാ[512]; struct pk_sockaddr_in പീര്_മൂല്യം; pk_socklen_t ദൈര്_ഘ്യം_ഡാറ്റാ = sizeof(പീര്_മൂല്യം);
    intptr_t വലിപ്പം = 결과검사(사용자호출(35, mp_obj_get_int(ഫയല്_കൈകാര്യംചെയ്യല്), (uintptr_t)ഡാറ്റാ, 512, 0, (uintptr_t)&പീര്_മൂല്യം, (uintptr_t)&ദൈര്_ഘ്യം_ഡാറ്റാ));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(ഡാറ്റാ, വലിപ്പം), MP_OBJ_NEW_SMALL_INT(pk_htons(പീര്_മൂല്യം.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ഫയല്_കൈകാര്യംചെയ്യല്) { 결과검사(사용자호출(4, mp_obj_get_int(ഫയല്_കൈകാര്യംചെയ്യല്), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t തുറക്കുക_സ്ട്രീം(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,ക്ലൌഡ്_കുടുംബം,സ്ട്രീം_നെറ്റ്_വർക്ക്,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,തുറക്കുക_സ്ട്രീം);
static mp_obj_t കണക്റ്റ്_സ്ട്രീം(mp_obj_t അവസാനബിന്ദു,mp_obj_t ഇമെയിൽ_ലിഖിതം,mp_obj_t സൂചിക) {
    int പോര്_ട്ട്_നമ്പര്=mp_obj_get_int(സൂചിക); if(പോര്_ട്ട്_നമ്പര്<1||പോര്_ട്ട്_നമ്പര്>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ഇമെയിൽ={0}; ഇമെയിൽ.ഇമെയിൽ_കുടുംബം=ക്ലൌഡ്_കുടുംബം;
    ഇമെയിൽ.പോര്_ട്ട്_നമ്പര്=망차례짧은수(പോര്_ട്ട്_നമ്പര്); ഇമെയിൽ.ഇന്_റര്_നെറ്റ്_വിലാസം.ഇമെയിൽ_മൂല്യം=നെറ്റ്_വർക്ക്_പൂര്_ണ്ണസംഖ്യ(인터넷주소읽기(ഇമെയിൽ_ലിഖിതം));
    결과검사(사용자호출(37,mp_obj_get_int(അവസാനബിന്ദു),(uintptr_t)&ഇമെയിൽ,sizeof(ഇമെയിൽ),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(സ്ട്രീം_കണക്ടര്_ഓബ്ജക്റ്റ്,കണക്റ്റ്_സ്ട്രീം);
static mp_obj_t 흐름읽기(mp_obj_t അവസാനബിന്ദു,mp_obj_t 한도) {
    int ദൈര്_ഘ്യം_മൂല്യം=mp_obj_get_int(한도); if(ദൈര്_ഘ്യം_മൂല്യം<1||ദൈര്_ഘ്യം_മൂല്യം>512)mp_raise_OSError(MP_EINVAL);
    unsigned char ഡാറ്റാ[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(അവസാനബിന്ദു),(uintptr_t)ഡാറ്റാ,ദൈര്_ഘ്യം_മൂല്യം,0,0,0));
    return mp_obj_new_bytes(ഡാറ്റാ,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(സ്ട്രീം_റീഡര്_ഓബ്ജക്റ്റ്,흐름읽기);
static mp_obj_t റൈറ്റ്_ചെയ്യുക_സ്ട്രീം(mp_obj_t അവസാനബിന്ദു,mp_obj_t ഉള്ളടക്കം_മൂല്യം) {
    mp_buffer_info_t ഡാറ്റാ; mp_get_buffer_raise(ഉള്ളടക്കം_മൂല്യം,&ഡാറ്റാ,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(അവസാനബിന്ദു),(uintptr_t)ഡാറ്റാ.buf,ഡാറ്റാ.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(സ്ട്രീം_റൈറ്റര്_ഓബ്ജക്റ്റ്,റൈറ്റ്_ചെയ്യുക_സ്ട്രീം);
static mp_obj_t 잠시기다리기(mp_obj_t സമയ_മൂല്യം) {
    결과검사(사용자호출(17,mp_obj_get_int(സമയ_മൂല്യം),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(കാക്കുക_ഓബ്ജക്റ്റ്,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t പേരു്) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)പാത_ആര്_ഗ്യുമെന്_റ്(പേരു്),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t സൃഷ്_ടിക്കുക_ഡയറക്ടറി(mp_obj_t പേരു്) {
    결과검사(사용자호출(18,(uintptr_t)പാത_ആര്_ഗ്യുമെന്_റ്(പേരു്),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(ഡയറക്ടറി_സ്രഷ്_ടാവ്_ഓബ്ജക്റ്റ്,സൃഷ്_ടിക്കുക_ഡയറക്ടറി);
static mp_obj_t നീക്കംചെയ്യുക_ഡയറക്ടറി(mp_obj_t പേരു്) {
    결과검사(사용자호출(18,(uintptr_t)പാത_ആര്_ഗ്യുമെന്_റ്(പേരു്),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,നീക്കംചെയ്യുക_ഡയറക്ടറി);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&സ്ട്രീം_കണക്ടര്_ഓബ്ജക്റ്റ്) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&സ്ട്രീം_റീഡര്_ഓബ്ജക്റ്റ്) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&സ്ട്രീം_റൈറ്റര്_ഓബ്ജക്റ്റ്) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&കാക്കുക_ഓബ്ജക്റ്റ്) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&ഡയറക്ടറി_സ്രഷ്_ടാവ്_ഓബ്ജക്റ്റ്) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ഫയല്_റീഡര്_ഓബ്ജക്റ്റ്) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ഫയല്_റൈറ്റര്_ഓബ്ജക്റ്റ്) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&ഘടികാരം_ഓബ്ജക്റ്റ്) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
