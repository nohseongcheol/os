// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t அளவிடக்கூடியது) { if (அளவிடக்கூடியது < 0) mp_raise_OSError(-அளவிடக்கூடியது); return அளவிடக்கூடியது; }
static const char *பாதை_மதிப்புரு(mp_obj_t மதிப்பு) {
    size_t 개수; const char *பாதை_2 = mp_obj_str_get_data(மதிப்பு, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!பாதை_2[순번]) mp_raise_OSError(MP_EINVAL);
    return பாதை_2;
}
static mp_obj_t 파일읽기(mp_obj_t பெயர்) {
    intptr_t கோப்பு_நடத்தி = 결과검사(사용자호출(3, (uintptr_t)பாதை_மதிப்புரு(பெயர்), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t அளவு = 결과검사(사용자호출(9, கோப்பு_நடத்தி, 0, 0, 0, 0, 0));
        vstr_t தரவு; vstr_init_len(&தரவு, அளவு);
        intptr_t அளவிடக்கூடியது = 사용자호출(2, கோப்பு_நடத்தி, (uintptr_t)தரவு.buf, அளவு, 0, 0, 0);
        결과검사(அளவிடக்கூடியது); தரவு.len = அளவிடக்கூடியது;
        mp_obj_t மதிப்பு = mp_obj_new_bytes_from_vstr(&தரவு);
        nlr_pop(); 사용자호출(4, கோப்பு_நடத்தி, 0, 0, 0, 0, 0); return மதிப்பு;
    }
    사용자호출(4, கோப்பு_நடத்தி, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(கோப்பு_படிப்பவர்_பொருள், 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t அளவு=mp_obj_get_int(한도);
    if(அளவு<0||அளவு>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t தரவு; vstr_init_len(&தரவு,அளவு);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)தரவு.buf,அளவு,0,0,0);
    if(개수<0) { vstr_clear(&தரவு); 결과검사(개수); }
    தரவு.len=개수; return mp_obj_new_bytes_from_vstr(&தரவு);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t எழுது_கோப்பு(mp_obj_t பெயர், mp_obj_t உள்ளடக்கம்_மதிப்பு) {
    const char *பாதை_2 = பாதை_மதிப்புரு(பெயர்);
    mp_buffer_info_t தரவு; mp_get_buffer_raise(உள்ளடக்கம்_மதிப்பு, &தரவு, MP_BUFFER_READ);
    if (தரவு.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t கோப்பு_நடத்தி = 결과검사(사용자호출(3, (uintptr_t)பாதை_2, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, கோப்பு_நடத்தி, (uintptr_t)தரவு.buf, தரவு.len, 0, 0, 0);
    사용자호출(4, கோப்பு_நடத்தி, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(கோப்பு_ரைட்டர்_பொருள், எழுது_கோப்பு);
static mp_obj_t அகற்று_கோப்பு(mp_obj_t பெயர்) { 결과검사(사용자호출(11, (uintptr_t)பாதை_மதிப்புரு(பெயர்), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, அகற்று_கோப்பு);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *மதிப்புரு_கோவை) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(மதிப்புரு_கோவை[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t அளவு[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, அளவு);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t கடிகாரம்_மதிப்பு(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(கடிகாரம்_பொருள், கடிகாரம்_மதிப்பு);
static mp_obj_t 전문열기(mp_obj_t முனைய_எண்) {
    int தரவு_நிலை = mp_obj_get_int(முனைய_எண்); if (தரவு_நிலை < 0 || தரவு_நிலை > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t கோப்பு_நடத்தி = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(தரவு_நிலை); 첫째값.sin_addr.s_addr = 0;
    intptr_t அளவிடக்கூடியது = 사용자호출(33, கோப்பு_நடத்தி, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (அளவிடக்கூடியது < 0) { 사용자호출(4, கோப்பு_நடத்தி, 0, 0, 0, 0, 0); 결과검사(அளவிடக்கூடியது); }
    return mp_obj_new_int(கோப்பு_நடத்தி);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t கோப்பு_நடத்தி, mp_obj_t முனைய_எண், mp_obj_t உள்ளடக்கம்_மதிப்பு) {
    int தரவு_நிலை = mp_obj_get_int(முனைய_எண்); if (தரவு_நிலை < 1 || தரவு_நிலை > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t தரவு; mp_get_buffer_raise(உள்ளடக்கம்_மதிப்பு, &தரவு, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(தரவு_நிலை); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(கோப்பு_நடத்தி), (uintptr_t)தரவு.buf, தரவு.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t மதிப்பு) {
    size_t நீளம்_மதிப்பு; const char *உரை=mp_obj_str_get_data(மதிப்பு,&நீளம்_மதிப்பு);
    unsigned 현재위치=0; uint32_t முகவரி=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned மதிப்பு=0,숫자수=0;
        while(현재위치<நீளம்_மதிப்பு&&உரை[현재위치]>='0'&&உரை[현재위치]<='9') {
            மதிப்பு=மதிப்பு*10+உரை[현재위치++]-'0'; if(++숫자수>3||மதிப்பு>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        முகவரி=முகவரி<<8|மதிப்பு;
        if(부분<3&&(현재위치>=நீளம்_மதிப்பு||உரை[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=நீளம்_மதிப்பு)mp_raise_OSError(MP_EINVAL);
    return முகவரி;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *மதிப்புரு_கோவை) {
    (void)항목수; uint32_t முகவரி=인터넷주소읽기(மதிப்புரு_கோவை[1]);
    int முனைய_எண்=mp_obj_get_int(மதிப்புரு_கோவை[2]);if(முனைய_எண்<1||முனைய_எண்>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t தரவு;mp_get_buffer_raise(மதிப்புரு_கோவை[3],&தரவு,MP_BUFFER_READ);
    struct pk_sockaddr_in இலக்கு={0};இலக்கு.sin_family=AF_INET;இலக்கு.sin_port=pk_htons(முனைய_எண்);இலக்கு.sin_addr.s_addr=pk_htonl(முகவரி);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(மதிப்புரு_கோவை[0]),(uintptr_t)தரவு.buf,தரவு.len,0,(uintptr_t)&இலக்கு,sizeof(இலக்கு))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t கோப்பு_நடத்தி) {
    unsigned char தரவு[512]; struct pk_sockaddr_in பியர்_மதிப்பு; pk_socklen_t நீளம்_தரவு = sizeof(பியர்_மதிப்பு);
    intptr_t அளவு = 결과검사(사용자호출(35, mp_obj_get_int(கோப்பு_நடத்தி), (uintptr_t)தரவு, 512, 0, (uintptr_t)&பியர்_மதிப்பு, (uintptr_t)&நீளம்_தரவு));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(தரவு, அளவு), MP_OBJ_NEW_SMALL_INT(pk_htons(பியர்_மதிப்பு.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t கோப்பு_நடத்தி) { 결과검사(사용자호출(4, mp_obj_get_int(கோப்பு_நடத்தி), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t திற_தொடரோடி(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,இணையம்_குடும்பம்,தொடரோடி_பிணையம்,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,திற_தொடரோடி);
static mp_obj_t இணை_தொடரோடி(mp_obj_t முடிவுப்_புள்ளி,mp_obj_t முகவரி_உரை,mp_obj_t அடைவு) {
    int முனைய_எண்=mp_obj_get_int(அடைவு); if(முனைய_எண்<1||முனைய_எண்>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 முகவரி={0}; முகவரி.முகவரி_குடும்பம்=இணையம்_குடும்பம்;
    முகவரி.முனைய_எண்=망차례짧은수(முனைய_எண்); முகவரி.இணைய_முகவரி.முகவரி_மதிப்பு=பிணையம்_முழு_எண்(인터넷주소읽기(முகவரி_உரை));
    결과검사(사용자호출(37,mp_obj_get_int(முடிவுப்_புள்ளி),(uintptr_t)&முகவரி,sizeof(முகவரி),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(தொடரோடி_இணைப்பான்_பொருள்,இணை_தொடரோடி);
static mp_obj_t 흐름읽기(mp_obj_t முடிவுப்_புள்ளி,mp_obj_t 한도) {
    int நீளம்_மதிப்பு=mp_obj_get_int(한도); if(நீளம்_மதிப்பு<1||நீளம்_மதிப்பு>512)mp_raise_OSError(MP_EINVAL);
    unsigned char தரவு[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(முடிவுப்_புள்ளி),(uintptr_t)தரவு,நீளம்_மதிப்பு,0,0,0));
    return mp_obj_new_bytes(தரவு,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(தொடரோடி_படிப்பவர்_பொருள்,흐름읽기);
static mp_obj_t எழுது_தொடரோடி(mp_obj_t முடிவுப்_புள்ளி,mp_obj_t உள்ளடக்கம்_மதிப்பு) {
    mp_buffer_info_t தரவு; mp_get_buffer_raise(உள்ளடக்கம்_மதிப்பு,&தரவு,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(முடிவுப்_புள்ளி),(uintptr_t)தரவு.buf,தரவு.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(தொடரோடி_ரைட்டர்_பொருள்,எழுது_தொடரோடி);
static mp_obj_t 잠시기다리기(mp_obj_t நேர_மதிப்பு) {
    결과검사(사용자호출(17,mp_obj_get_int(நேர_மதிப்பு),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(காத்திரு_பொருள்,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t பெயர்) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)பாதை_மதிப்புரு(பெயர்),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t உருவாக்கு_கோப்பகம்(mp_obj_t பெயர்) {
    결과검사(사용자호출(18,(uintptr_t)பாதை_மதிப்புரு(பெயர்),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(கோப்பகம்_கிரியேட்டர்_பொருள்,உருவாக்கு_கோப்பகம்);
static mp_obj_t அகற்று_கோப்பகம்(mp_obj_t பெயர்) {
    결과검사(사용자호출(18,(uintptr_t)பாதை_மதிப்புரு(பெயர்),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,அகற்று_கோப்பகம்);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&தொடரோடி_இணைப்பான்_பொருள்) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&தொடரோடி_படிப்பவர்_பொருள்) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&தொடரோடி_ரைட்டர்_பொருள்) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&காத்திரு_பொருள்) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&கோப்பகம்_கிரியேட்டர்_பொருள்) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&கோப்பு_படிப்பவர்_பொருள்) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&கோப்பு_ரைட்டர்_பொருள்) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&கடிகாரம்_பொருள்) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
