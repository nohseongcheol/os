// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *گوزەر_ئارگیومێنت(mp_obj_t نرخ) {
    size_t 개수; const char *گوزەر = mp_obj_str_get_data(نرخ, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!گوزەر[순번]) mp_raise_OSError(MP_EINVAL);
    return گوزەر;
}
static mp_obj_t 파일읽기(mp_obj_t ناو) {
    intptr_t فایل_دەسک = 결과검사(사용자호출(3, (uintptr_t)گوزەر_ئارگیومێنت(ناو), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t گۆڕینی_ئەندازە = 결과검사(사용자호출(9, فایل_دەسک, 0, 0, 0, 0, 0));
        vstr_t دەیتا; vstr_init_len(&دەیتا, گۆڕینی_ئەندازە);
        intptr_t 결과 = 사용자호출(2, فایل_دەسک, (uintptr_t)دەیتا.buf, گۆڕینی_ئەندازە, 0, 0, 0);
        결과검사(결과); دەیتا.len = 결과;
        mp_obj_t نرخ = mp_obj_new_bytes_from_vstr(&دەیتا);
        nlr_pop(); 사용자호출(4, فایل_دەسک, 0, 0, 0, 0, 0); return نرخ;
    }
    사용자호출(4, فایل_دەسک, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(فایل_خوێنەر_شت, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t گۆڕینی_ئەندازە=mp_obj_get_int(한도);
    if(گۆڕینی_ئەندازە<0||گۆڕینی_ئەندازە>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t دەیتا; vstr_init_len(&دەیتا,گۆڕینی_ئەندازە);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)دەیتا.buf,گۆڕینی_ئەندازە,0,0,0);
    if(개수<0) { vstr_clear(&دەیتا); 결과검사(개수); }
    دەیتا.len=개수; return mp_obj_new_bytes_from_vstr(&دەیتا);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t ڕایت_کردن_فایل(mp_obj_t ناو, mp_obj_t ناوەرۆک_نرخ) {
    const char *گوزەر = گوزەر_ئارگیومێنت(ناو);
    mp_buffer_info_t دەیتا; mp_get_buffer_raise(ناوەرۆک_نرخ, &دەیتا, MP_BUFFER_READ);
    if (دەیتا.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t فایل_دەسک = 결과검사(사용자호출(3, (uintptr_t)گوزەر, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, فایل_دەسک, (uintptr_t)دەیتا.buf, دەیتا.len, 0, 0, 0);
    사용자호출(4, فایل_دەسک, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(فایل_نووسەر_شت, ڕایت_کردن_فایل);
static mp_obj_t لابردن_فایل(mp_obj_t ناو) { 결과검사(사용자호출(11, (uintptr_t)گوزەر_ئارگیومێنت(ناو), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, لابردن_فایل);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *ئارگیومێنت_ڕیزی_داتا) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(ئارگیومێنت_ڕیزی_داتا[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t گۆڕینی_ئەندازە[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, گۆڕینی_ئەندازە);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t کاتژمێر_نرخ(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(کاتژمێر_شت, کاتژمێر_نرخ);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t فایل_دەسک = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, فایل_دەسک, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, فایل_دەسک, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(فایل_دەسک);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t فایل_دەسک, mp_obj_t 접속번호, mp_obj_t ناوەرۆک_نرخ) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t دەیتا; mp_get_buffer_raise(ناوەرۆک_نرخ, &دەیتا, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(فایل_دەسک), (uintptr_t)دەیتا.buf, دەیتا.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t نرخ) {
    size_t درێژی_نرخ; const char *دەق=mp_obj_str_get_data(نرخ,&درێژی_نرخ);
    unsigned 현재위치=0; uint32_t ناونیشان=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned نرخ=0,숫자수=0;
        while(현재위치<درێژی_نرخ&&دەق[현재위치]>='0'&&دەق[현재위치]<='9') {
            نرخ=نرخ*10+دەق[현재위치++]-'0'; if(++숫자수>3||نرخ>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        ناونیشان=ناونیشان<<8|نرخ;
        if(부분<3&&(현재위치>=درێژی_نرخ||دەق[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=درێژی_نرخ)mp_raise_OSError(MP_EINVAL);
    return ناونیشان;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *ئارگیومێنت_ڕیزی_داتا) {
    (void)항목수; uint32_t ناونیشان=인터넷주소읽기(ئارگیومێنت_ڕیزی_داتا[1]);
    int 접속번호=mp_obj_get_int(ئارگیومێنت_ڕیزی_داتا[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t دەیتا;mp_get_buffer_raise(ئارگیومێنت_ڕیزی_داتا[3],&دەیتا,MP_BUFFER_READ);
    struct pk_sockaddr_in مەبەست={0};مەبەست.sin_family=AF_INET;مەبەست.sin_port=pk_htons(접속번호);مەبەست.sin_addr.s_addr=pk_htonl(ناونیشان);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(ئارگیومێنت_ڕیزی_داتا[0]),(uintptr_t)دەیتا.buf,دەیتا.len,0,(uintptr_t)&مەبەست,sizeof(مەبەست))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t فایل_دەسک) {
    unsigned char دەیتا[512]; struct pk_sockaddr_in هاوتا_نرخ; pk_socklen_t درێژی_دەیتا = sizeof(هاوتا_نرخ);
    intptr_t گۆڕینی_ئەندازە = 결과검사(사용자호출(35, mp_obj_get_int(فایل_دەسک), (uintptr_t)دەیتا, 512, 0, (uintptr_t)&هاوتا_نرخ, (uintptr_t)&درێژی_دەیتا));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(دەیتا, گۆڕینی_ئەندازە), MP_OBJ_NEW_SMALL_INT(pk_htons(هاوتا_نرخ.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t فایل_دەسک) { 결과검사(사용자호출(4, mp_obj_get_int(فایل_دەسک), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t کردنەوە_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,هەور_خێزان,Stream_تۆڕ,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,کردنەوە_Stream);
static mp_obj_t لكاندن_Stream(mp_obj_t 종단,mp_obj_t ناونیشان_دەق,mp_obj_t پێرست) {
    int 접속번호=mp_obj_get_int(پێرست); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ناونیشان={0}; ناونیشان.ناونیشان_خێزان=هەور_خێزان;
    ناونیشان.접속번호=망차례짧은수(접속번호); ناونیشان.ناونیشانی_ئینتەرنێتی.ناونیشان_نرخ=تۆڕ_ژمارەی_سروشتی(인터넷주소읽기(ناونیشان_دەق));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ناونیشان,sizeof(ناونیشان),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_لکێنەر_شت,لكاندن_Stream);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int درێژی_نرخ=mp_obj_get_int(한도); if(درێژی_نرخ<1||درێژی_نرخ>512)mp_raise_OSError(MP_EINVAL);
    unsigned char دەیتا[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)دەیتا,درێژی_نرخ,0,0,0));
    return mp_obj_new_bytes(دەیتا,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_خوێنەر_شت,흐름읽기);
static mp_obj_t ڕایت_کردن_Stream(mp_obj_t 종단,mp_obj_t ناوەرۆک_نرخ) {
    mp_buffer_info_t دەیتا; mp_get_buffer_raise(ناوەرۆک_نرخ,&دەیتا,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)دەیتا.buf,دەیتا.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_نووسەر_شت,ڕایت_کردن_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t کات_نرخ) {
    결과검사(사용자호출(17,mp_obj_get_int(کات_نرخ),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(چاوەڕوان_کردن_شت,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t ناو) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)گوزەر_ئارگیومێنت(ناو),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t دروستکردن_ڕێبەرنامە(mp_obj_t ناو) {
    결과검사(사용자호출(18,(uintptr_t)گوزەر_ئارگیومێنت(ناو),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,دروستکردن_ڕێبەرنامە);
static mp_obj_t لابردن_ڕێبەرنامە(mp_obj_t ناو) {
    결과검사(사용자호출(18,(uintptr_t)گوزەر_ئارگیومێنت(ناو),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,لابردن_ڕێبەرنامە);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_لکێنەر_شت) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_خوێنەر_شت) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_نووسەر_شت) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&چاوەڕوان_کردن_شت) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&فایل_خوێنەر_شت) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&فایل_نووسەر_شت) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&کاتژمێر_شت) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
