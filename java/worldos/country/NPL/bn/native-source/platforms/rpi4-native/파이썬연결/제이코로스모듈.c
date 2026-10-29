// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t পরিমাপ) { if (পরিমাপ < 0) mp_raise_OSError(-পরিমাপ); return পরিমাপ; }
static const char *পথ_যুক্তি(mp_obj_t মান) {
    size_t 개수; const char *পথ_2 = mp_obj_str_get_data(মান, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!পথ_2[순번]) mp_raise_OSError(MP_EINVAL);
    return পথ_2;
}
static mp_obj_t 파일읽기(mp_obj_t নাম) {
    intptr_t ফাইল_হাতল = 결과검사(사용자호출(3, (uintptr_t)পথ_যুক্তি(নাম), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t আকার = 결과검사(사용자호출(9, ফাইল_হাতল, 0, 0, 0, 0, 0));
        vstr_t ডাটা; vstr_init_len(&ডাটা, আকার);
        intptr_t পরিমাপ = 사용자호출(2, ফাইল_হাতল, (uintptr_t)ডাটা.buf, আকার, 0, 0, 0);
        결과검사(পরিমাপ); ডাটা.len = পরিমাপ;
        mp_obj_t মান = mp_obj_new_bytes_from_vstr(&ডাটা);
        nlr_pop(); 사용자호출(4, ফাইল_হাতল, 0, 0, 0, 0, 0); return মান;
    }
    사용자호출(4, ফাইল_হাতল, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ফাইল_পাঠক_বস্তু, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t আকার=mp_obj_get_int(한도);
    if(আকার<0||আকার>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t ডাটা; vstr_init_len(&ডাটা,আকার);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)ডাটা.buf,আকার,0,0,0);
    if(개수<0) { vstr_clear(&ডাটা); 결과검사(개수); }
    ডাটা.len=개수; return mp_obj_new_bytes_from_vstr(&ডাটা);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t লেখা_ফাইল(mp_obj_t নাম, mp_obj_t সামগ্রি_মান) {
    const char *পথ_2 = পথ_যুক্তি(নাম);
    mp_buffer_info_t ডাটা; mp_get_buffer_raise(সামগ্রি_মান, &ডাটা, MP_BUFFER_READ);
    if (ডাটা.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ফাইল_হাতল = 결과검사(사용자호출(3, (uintptr_t)পথ_2, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ফাইল_হাতল, (uintptr_t)ডাটা.buf, ডাটা.len, 0, 0, 0);
    사용자호출(4, ফাইল_হাতল, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ফাইল_লেখক_বস্তু, লেখা_ফাইল);
static mp_obj_t সরানো_ফাইল(mp_obj_t নাম) { 결과검사(사용자호출(11, (uintptr_t)পথ_যুক্তি(নাম), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, সরানো_ফাইল);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *যুক্তি_অ্যারে) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(যুক্তি_অ্যারে[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t আকার[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, আকার);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t ঘড়ি_মান(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(ঘড়ি_বস্তু, ঘড়ি_মান);
static mp_obj_t 전문열기(mp_obj_t পোর্ট_নম্বর) {
    int ডাটা_পদ = mp_obj_get_int(পোর্ট_নম্বর); if (ডাটা_পদ < 0 || ডাটা_পদ > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ফাইল_হাতল = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ডাটা_পদ); 첫째값.sin_addr.s_addr = 0;
    intptr_t পরিমাপ = 사용자호출(33, ফাইল_হাতল, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (পরিমাপ < 0) { 사용자호출(4, ফাইল_হাতল, 0, 0, 0, 0, 0); 결과검사(পরিমাপ); }
    return mp_obj_new_int(ফাইল_হাতল);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ফাইল_হাতল, mp_obj_t পোর্ট_নম্বর, mp_obj_t সামগ্রি_মান) {
    int ডাটা_পদ = mp_obj_get_int(পোর্ট_নম্বর); if (ডাটা_পদ < 1 || ডাটা_পদ > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ডাটা; mp_get_buffer_raise(সামগ্রি_মান, &ডাটা, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ডাটা_পদ); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ফাইল_হাতল), (uintptr_t)ডাটা.buf, ডাটা.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t মান) {
    size_t দৈর্ঘ্য_মান; const char *পাঠ=mp_obj_str_get_data(মান,&দৈর্ঘ্য_মান);
    unsigned 현재위치=0; uint32_t ইমেইল=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned মান=0,숫자수=0;
        while(현재위치<দৈর্ঘ্য_মান&&পাঠ[현재위치]>='0'&&পাঠ[현재위치]<='9') {
            মান=মান*10+পাঠ[현재위치++]-'0'; if(++숫자수>3||মান>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        ইমেইল=ইমেইল<<8|মান;
        if(부분<3&&(현재위치>=দৈর্ঘ্য_মান||পাঠ[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=দৈর্ঘ্য_মান)mp_raise_OSError(MP_EINVAL);
    return ইমেইল;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *যুক্তি_অ্যারে) {
    (void)항목수; uint32_t ইমেইল=인터넷주소읽기(যুক্তি_অ্যারে[1]);
    int পোর্ট_নম্বর=mp_obj_get_int(যুক্তি_অ্যারে[2]);if(পোর্ট_নম্বর<1||পোর্ট_নম্বর>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ডাটা;mp_get_buffer_raise(যুক্তি_অ্যারে[3],&ডাটা,MP_BUFFER_READ);
    struct pk_sockaddr_in লক্ষ্য={0};লক্ষ্য.sin_family=AF_INET;লক্ষ্য.sin_port=pk_htons(পোর্ট_নম্বর);লক্ষ্য.sin_addr.s_addr=pk_htonl(ইমেইল);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(যুক্তি_অ্যারে[0]),(uintptr_t)ডাটা.buf,ডাটা.len,0,(uintptr_t)&লক্ষ্য,sizeof(লক্ষ্য))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ফাইল_হাতল) {
    unsigned char ডাটা[512]; struct pk_sockaddr_in পিয়ার_মান; pk_socklen_t দৈর্ঘ্য_ডাটা = sizeof(পিয়ার_মান);
    intptr_t আকার = 결과검사(사용자호출(35, mp_obj_get_int(ফাইল_হাতল), (uintptr_t)ডাটা, 512, 0, (uintptr_t)&পিয়ার_মান, (uintptr_t)&দৈর্ঘ্য_ডাটা));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(ডাটা, আকার), MP_OBJ_NEW_SMALL_INT(pk_htons(পিয়ার_মান.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ফাইল_হাতল) { 결과검사(사용자호출(4, mp_obj_get_int(ফাইল_হাতল), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t খোলা_প্রবাহ(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,ক্লাউড_পরিবার,প্রবাহ_নেটওয়ার্ক,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,খোলা_প্রবাহ);
static mp_obj_t সংযোগ_প্রবাহ(mp_obj_t 종단,mp_obj_t ইমেইল_পাঠ,mp_obj_t সূচি) {
    int পোর্ট_নম্বর=mp_obj_get_int(সূচি); if(পোর্ট_নম্বর<1||পোর্ট_নম্বর>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ইমেইল={0}; ইমেইল.ইমেইল_পরিবার=ক্লাউড_পরিবার;
    ইমেইল.পোর্ট_নম্বর=망차례짧은수(পোর্ট_নম্বর); ইমেইল.ইন্টারনেট_ঠিকানা.ইমেইল_মান=নেটওয়ার্ক_পূর্ণসংখ্যা(인터넷주소읽기(ইমেইল_পাঠ));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ইমেইল,sizeof(ইমেইল),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(প্রবাহ_সংযোজক_বস্তু,সংযোগ_প্রবাহ);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int দৈর্ঘ্য_মান=mp_obj_get_int(한도); if(দৈর্ঘ্য_মান<1||দৈর্ঘ্য_মান>512)mp_raise_OSError(MP_EINVAL);
    unsigned char ডাটা[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)ডাটা,দৈর্ঘ্য_মান,0,0,0));
    return mp_obj_new_bytes(ডাটা,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(প্রবাহ_পাঠক_বস্তু,흐름읽기);
static mp_obj_t লেখা_প্রবাহ(mp_obj_t 종단,mp_obj_t সামগ্রি_মান) {
    mp_buffer_info_t ডাটা; mp_get_buffer_raise(সামগ্রি_মান,&ডাটা,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)ডাটা.buf,ডাটা.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(প্রবাহ_লেখক_বস্তু,লেখা_প্রবাহ);
static mp_obj_t 잠시기다리기(mp_obj_t সময়_মান) {
    결과검사(사용자호출(17,mp_obj_get_int(সময়_মান),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(অপেক্ষা_বস্তু,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t নাম) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)পথ_যুক্তি(নাম),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t ক্রিয়েট_ডিরেক্টরি(mp_obj_t নাম) {
    결과검사(사용자호출(18,(uintptr_t)পথ_যুক্তি(নাম),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,ক্রিয়েট_ডিরেক্টরি);
static mp_obj_t সরানো_ডিরেক্টরি(mp_obj_t নাম) {
    결과검사(사용자호출(18,(uintptr_t)পথ_যুক্তি(নাম),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,সরানো_ডিরেক্টরি);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&প্রবাহ_সংযোজক_বস্তু) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&প্রবাহ_পাঠক_বস্তু) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&প্রবাহ_লেখক_বস্তু) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&অপেক্ষা_বস্তু) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ফাইল_পাঠক_বস্তু) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ফাইল_লেখক_বস্তু) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&ঘড়ি_বস্তু) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
