// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *පෙත_විස්තාරකය(mp_obj_t අගය) {
    size_t 개수; const char *මාර්_ගය = mp_obj_str_get_data(අගය, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!මාර්_ගය[순번]) mp_raise_OSError(MP_EINVAL);
    return මාර්_ගය;
}
static mp_obj_t 파일읽기(mp_obj_t නම) {
    intptr_t ගොනුව_හසුරුව = 결과검사(사용자호출(3, (uintptr_t)පෙත_විස්තාරකය(නම), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t ප්_රමාණය = 결과검사(사용자호출(9, ගොනුව_හසුරුව, 0, 0, 0, 0, 0));
        vstr_t දත්ත; vstr_init_len(&දත්ත, ප්_රමාණය);
        intptr_t 결과 = 사용자호출(2, ගොනුව_හසුරුව, (uintptr_t)දත්ත.buf, ප්_රමාණය, 0, 0, 0);
        결과검사(결과); දත්ත.len = 결과;
        mp_obj_t අගය = mp_obj_new_bytes_from_vstr(&දත්ත);
        nlr_pop(); 사용자호출(4, ගොනුව_හසුරුව, 0, 0, 0, 0, 0); return අගය;
    }
    사용자호출(4, ගොනුව_හසුරුව, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ගොනුව_පාඨක_වස්තුව, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t ප්_රමාණය=mp_obj_get_int(한도);
    if(ප්_රමාණය<0||ප්_රමාණය>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t දත්ත; vstr_init_len(&දත්ත,ප්_රමාණය);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)දත්ත.buf,ප්_රමාණය,0,0,0);
    if(개수<0) { vstr_clear(&දත්ත); 결과검사(개수); }
    දත්ත.len=개수; return mp_obj_new_bytes_from_vstr(&දත්ත);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t ලියන්න_ගොනුව(mp_obj_t නම, mp_obj_t අන්තර්ගතය_අගය) {
    const char *මාර්_ගය = පෙත_විස්තාරකය(නම);
    mp_buffer_info_t දත්ත; mp_get_buffer_raise(අන්තර්ගතය_අගය, &දත්ත, MP_BUFFER_READ);
    if (දත්ත.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ගොනුව_හසුරුව = 결과검사(사용자호출(3, (uintptr_t)මාර්_ගය, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ගොනුව_හසුරුව, (uintptr_t)දත්ත.buf, දත්ත.len, 0, 0, 0);
    사용자호출(4, ගොනුව_හසුරුව, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ගොනුව_Windows_Live_ලේඛක_වස්තුව, ලියන්න_ගොනුව);
static mp_obj_t ඉවත්_කරන්න_ගොනුව(mp_obj_t නම) { 결과검사(사용자호출(11, (uintptr_t)පෙත_විස්තාරකය(නම), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ඉවත්_කරන්න_ගොනුව);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *විස්තාරකය_ආරා_ව) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(විස්තාරකය_ආරා_ව[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t ප්_රමාණය[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, ප්_රමාණය);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t ඝටිකා_ව_අගය(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(ඝටිකා_ව_වස්තුව, ඝටිකා_ව_අගය);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ගොනුව_හසුරුව = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, ගොනුව_හසුරුව, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, ගොනුව_හසුරුව, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(ගොනුව_හසුරුව);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ගොනුව_හසුරුව, mp_obj_t 접속번호, mp_obj_t අන්තර්ගතය_අගය) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t දත්ත; mp_get_buffer_raise(අන්තර්ගතය_අගය, &දත්ත, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ගොනුව_හසුරුව), (uintptr_t)දත්ත.buf, දත්ත.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t අගය) {
    size_t දිග_අගය; const char *පෙළ=mp_obj_str_get_data(අගය,&දිග_අගය);
    unsigned 현재위치=0; uint32_t යොමුව=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned අගය=0,숫자수=0;
        while(현재위치<දිග_අගය&&පෙළ[현재위치]>='0'&&පෙළ[현재위치]<='9') {
            අගය=අගය*10+පෙළ[현재위치++]-'0'; if(++숫자수>3||අගය>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        යොමුව=යොමුව<<8|අගය;
        if(부분<3&&(현재위치>=දිග_අගය||පෙළ[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=දිග_අගය)mp_raise_OSError(MP_EINVAL);
    return යොමුව;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *විස්තාරකය_ආරා_ව) {
    (void)항목수; uint32_t යොමුව=인터넷주소읽기(විස්තාරකය_ආරා_ව[1]);
    int 접속번호=mp_obj_get_int(විස්තාරකය_ආරා_ව[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t දත්ත;mp_get_buffer_raise(විස්තාරකය_ආරා_ව[3],&දත්ත,MP_BUFFER_READ);
    struct pk_sockaddr_in ඉලක්කය={0};ඉලක්කය.sin_family=AF_INET;ඉලක්කය.sin_port=pk_htons(접속번호);ඉලක්කය.sin_addr.s_addr=pk_htonl(යොමුව);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(විස්තාරකය_ආරා_ව[0]),(uintptr_t)දත්ත.buf,දත්ත.len,0,(uintptr_t)&ඉලක්කය,sizeof(ඉලක්කය))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ගොනුව_හසුරුව) {
    unsigned char දත්ත[512]; struct pk_sockaddr_in සමානයා_අගය; pk_socklen_t දිග_දත්ත = sizeof(සමානයා_අගය);
    intptr_t ප්_රමාණය = 결과검사(사용자호출(35, mp_obj_get_int(ගොනුව_හසුරුව), (uintptr_t)දත්ත, 512, 0, (uintptr_t)&සමානයා_අගය, (uintptr_t)&දිග_දත්ත));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(දත්ත, ප්_රමාණය), MP_OBJ_NEW_SMALL_INT(pk_htons(සමානයා_අගය.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ගොනුව_හසුරුව) { 결과검사(사용자호출(4, mp_obj_get_int(ගොනුව_හසුරුව), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t සාදන්න_දහර(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,වළාකුළු_පවුල,දහර_ජාලය,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,සාදන්න_දහර);
static mp_obj_t සබඳින්න_දහර(mp_obj_t 종단,mp_obj_t යොමුව_පෙළ,mp_obj_t සූචිය) {
    int 접속번호=mp_obj_get_int(සූචිය); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 යොමුව={0}; යොමුව.යොමුව_පවුල=වළාකුළු_පවුල;
    යොමුව.접속번호=망차례짧은수(접속번호); යොමුව.අන්තර්ජාල_ලිපිනය.යොමුව_අගය=ජාලය_පූර්ණාංකය(인터넷주소읽기(යොමුව_පෙළ));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&යොමුව,sizeof(යොමුව),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(දහර_සම්බන්ධකය_වස්තුව,සබඳින්න_දහර);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int දිග_අගය=mp_obj_get_int(한도); if(දිග_අගය<1||දිග_අගය>512)mp_raise_OSError(MP_EINVAL);
    unsigned char දත්ත[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)දත්ත,දිග_අගය,0,0,0));
    return mp_obj_new_bytes(දත්ත,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(දහර_පාඨක_වස්තුව,흐름읽기);
static mp_obj_t ලියන්න_දහර(mp_obj_t 종단,mp_obj_t අන්තර්ගතය_අගය) {
    mp_buffer_info_t දත්ත; mp_get_buffer_raise(අන්තර්ගතය_අගය,&දත්ත,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)දත්ත.buf,දත්ත.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(දහර_Windows_Live_ලේඛක_වස්තුව,ලියන්න_දහර);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t නම) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)පෙත_විස්තාරකය(නම),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t සාදන්න_නාමාවලිය(mp_obj_t නම) {
    결과검사(사용자호출(18,(uintptr_t)පෙත_විස්තාරකය(නම),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,සාදන්න_නාමාවලිය);
static mp_obj_t ඉවත්_කරන්න_නාමාවලිය(mp_obj_t නම) {
    결과검사(사용자호출(18,(uintptr_t)පෙත_විස්තාරකය(නම),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ඉවත්_කරන්න_නාමාවලිය);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&දහර_සම්බන්ධකය_වස්තුව) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&දහර_පාඨක_වස්තුව) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&දහර_Windows_Live_ලේඛක_වස්තුව) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ගොනුව_පාඨක_වස්තුව) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ගොනුව_Windows_Live_ලේඛක_වස්තුව) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&ඝටිකා_ව_වස්තුව) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
