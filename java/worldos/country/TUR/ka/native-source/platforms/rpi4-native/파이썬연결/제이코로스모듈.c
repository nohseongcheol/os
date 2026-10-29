// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t გაზომვა) { if (გაზომვა < 0) mp_raise_OSError(-გაზომვა); return გაზომვა; }
static const char *მდებარეობა_არგუმენტი(mp_obj_t მნიშვნელობა) {
    size_t 개수; const char *გეზი = mp_obj_str_get_data(მნიშვნელობა, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!გეზი[순번]) mp_raise_OSError(MP_EINVAL);
    return გეზი;
}
static mp_obj_t 파일읽기(mp_obj_t სახელი) {
    intptr_t ფაილი_სახელური = 결과검사(사용자호출(3, (uintptr_t)მდებარეობა_არგუმენტი(სახელი), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t ზომა = 결과검사(사용자호출(9, ფაილი_სახელური, 0, 0, 0, 0, 0));
        vstr_t მონაცემები; vstr_init_len(&მონაცემები, ზომა);
        intptr_t გაზომვა = 사용자호출(2, ფაილი_სახელური, (uintptr_t)მონაცემები.buf, ზომა, 0, 0, 0);
        결과검사(გაზომვა); მონაცემები.len = გაზომვა;
        mp_obj_t მნიშვნელობა = mp_obj_new_bytes_from_vstr(&მონაცემები);
        nlr_pop(); 사용자호출(4, ფაილი_სახელური, 0, 0, 0, 0, 0); return მნიშვნელობა;
    }
    사용자호출(4, ფაილი_სახელური, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ფაილი_წამკითხველი_ობიექტი, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t ზომა=mp_obj_get_int(한도);
    if(ზომა<0||ზომა>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t მონაცემები; vstr_init_len(&მონაცემები,ზომა);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)მონაცემები.buf,ზომა,0,0,0);
    if(개수<0) { vstr_clear(&მონაცემები); 결과검사(개수); }
    მონაცემები.len=개수; return mp_obj_new_bytes_from_vstr(&მონაცემები);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t ჩაწერა_ფაილი(mp_obj_t სახელი, mp_obj_t შიგთავსი_მნიშვნელობა) {
    const char *გეზი = მდებარეობა_არგუმენტი(სახელი);
    mp_buffer_info_t მონაცემები; mp_get_buffer_raise(შიგთავსი_მნიშვნელობა, &მონაცემები, MP_BUFFER_READ);
    if (მონაცემები.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ფაილი_სახელური = 결과검사(사용자호출(3, (uintptr_t)გეზი, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ფაილი_სახელური, (uintptr_t)მონაცემები.buf, მონაცემები.len, 0, 0, 0);
    사용자호출(4, ფაილი_სახელური, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ფაილი_ტექსტური_რედაქტორი_ობიექტი, ჩაწერა_ფაილი);
static mp_obj_t ამოშლა_ფაილი(mp_obj_t სახელი) { 결과검사(사용자호출(11, (uintptr_t)მდებარეობა_არგუმენტი(სახელი), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ამოშლა_ფაილი);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *არგუმენტი_მასივი) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(არგუმენტი_მასივი[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t ზომა[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, ზომა);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t საათი_მნიშვნელობა(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(საათი_ობიექტი, საათი_მნიშვნელობა);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int მონაცემები_პოზიცია = mp_obj_get_int(접속번호); if (მონაცემები_პოზიცია < 0 || მონაცემები_პოზიცია > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ფაილი_სახელური = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(მონაცემები_პოზიცია); 첫째값.sin_addr.s_addr = 0;
    intptr_t გაზომვა = 사용자호출(33, ფაილი_სახელური, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (გაზომვა < 0) { 사용자호출(4, ფაილი_სახელური, 0, 0, 0, 0, 0); 결과검사(გაზომვა); }
    return mp_obj_new_int(ფაილი_სახელური);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ფაილი_სახელური, mp_obj_t 접속번호, mp_obj_t შიგთავსი_მნიშვნელობა) {
    int მონაცემები_პოზიცია = mp_obj_get_int(접속번호); if (მონაცემები_პოზიცია < 1 || მონაცემები_პოზიცია > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t მონაცემები; mp_get_buffer_raise(შიგთავსი_მნიშვნელობა, &მონაცემები, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(მონაცემები_პოზიცია); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ფაილი_სახელური), (uintptr_t)მონაცემები.buf, მონაცემები.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t მნიშვნელობა) {
    size_t სიგრძე_მნიშვნელობა; const char *ტექსტი=mp_obj_str_get_data(მნიშვნელობა,&სიგრძე_მნიშვნელობა);
    unsigned 현재위치=0; uint32_t მისამართი=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned მნიშვნელობა=0,숫자수=0;
        while(현재위치<სიგრძე_მნიშვნელობა&&ტექსტი[현재위치]>='0'&&ტექსტი[현재위치]<='9') {
            მნიშვნელობა=მნიშვნელობა*10+ტექსტი[현재위치++]-'0'; if(++숫자수>3||მნიშვნელობა>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        მისამართი=მისამართი<<8|მნიშვნელობა;
        if(부분<3&&(현재위치>=სიგრძე_მნიშვნელობა||ტექსტი[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=სიგრძე_მნიშვნელობა)mp_raise_OSError(MP_EINVAL);
    return მისამართი;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *არგუმენტი_მასივი) {
    (void)항목수; uint32_t მისამართი=인터넷주소읽기(არგუმენტი_მასივი[1]);
    int 접속번호=mp_obj_get_int(არგუმენტი_მასივი[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t მონაცემები;mp_get_buffer_raise(არგუმენტი_მასივი[3],&მონაცემები,MP_BUFFER_READ);
    struct pk_sockaddr_in მიზანი={0};მიზანი.sin_family=AF_INET;მიზანი.sin_port=pk_htons(접속번호);მიზანი.sin_addr.s_addr=pk_htonl(მისამართი);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(არგუმენტი_მასივი[0]),(uintptr_t)მონაცემები.buf,მონაცემები.len,0,(uintptr_t)&მიზანი,sizeof(მიზანი))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ფაილი_სახელური) {
    unsigned char მონაცემები[512]; struct pk_sockaddr_in კვანძი_მნიშვნელობა_6a3b6fa7; pk_socklen_t სიგრძე_მონაცემები = sizeof(კვანძი_მნიშვნელობა_6a3b6fa7);
    intptr_t ზომა = 결과검사(사용자호출(35, mp_obj_get_int(ფაილი_სახელური), (uintptr_t)მონაცემები, 512, 0, (uintptr_t)&კვანძი_მნიშვნელობა_6a3b6fa7, (uintptr_t)&სიგრძე_მონაცემები));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(მონაცემები, ზომა), MP_OBJ_NEW_SMALL_INT(pk_htons(კვანძი_მნიშვნელობა_6a3b6fa7.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ფაილი_სახელური) { 결과검사(사용자호출(4, mp_obj_get_int(ფაილი_სახელური), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t გახსნა_ნაკადი(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,ინტერნეტი_ოჯახი,ნაკადი_ქსელი,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,გახსნა_ნაკადი);
static mp_obj_t დაკავშირება_ნაკადი(mp_obj_t 종단,mp_obj_t მისამართი_ტექსტი,mp_obj_t ინდექსი) {
    int 접속번호=mp_obj_get_int(ინდექსი); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 მისამართი={0}; მისამართი.მისამართი_ოჯახი=ინტერნეტი_ოჯახი;
    მისამართი.접속번호=망차례짧은수(접속번호); მისამართი.ინტერნეტის_მისამართი.მისამართი_მნიშვნელობა=ქსელი_მთელი_რიცხვი(인터넷주소읽기(მისამართი_ტექსტი));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&მისამართი,sizeof(მისამართი),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ნაკადი_მაერთებელი_ობიექტი,დაკავშირება_ნაკადი);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int სიგრძე_მნიშვნელობა=mp_obj_get_int(한도); if(სიგრძე_მნიშვნელობა<1||სიგრძე_მნიშვნელობა>512)mp_raise_OSError(MP_EINVAL);
    unsigned char მონაცემები[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)მონაცემები,სიგრძე_მნიშვნელობა,0,0,0));
    return mp_obj_new_bytes(მონაცემები,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ნაკადი_წამკითხველი_ობიექტი,흐름읽기);
static mp_obj_t ჩაწერა_ნაკადი(mp_obj_t 종단,mp_obj_t შიგთავსი_მნიშვნელობა) {
    mp_buffer_info_t მონაცემები; mp_get_buffer_raise(შიგთავსი_მნიშვნელობა,&მონაცემები,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)მონაცემები.buf,მონაცემები.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ნაკადი_ტექსტური_რედაქტორი_ობიექტი,ჩაწერა_ნაკადი);
static mp_obj_t 잠시기다리기(mp_obj_t დრო_მნიშვნელობა) {
    결과검사(사용자호출(17,mp_obj_get_int(დრო_მნიშვნელობა),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(მოლოდინი_ობიექტი,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t სახელი) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)მდებარეობა_არგუმენტი(სახელი),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t შექმნა_საქაღალდე(mp_obj_t სახელი) {
    결과검사(사용자호출(18,(uintptr_t)მდებარეობა_არგუმენტი(სახელი),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,შექმნა_საქაღალდე);
static mp_obj_t ამოშლა_საქაღალდე(mp_obj_t სახელი) {
    결과검사(사용자호출(18,(uintptr_t)მდებარეობა_არგუმენტი(სახელი),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ამოშლა_საქაღალდე);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ნაკადი_მაერთებელი_ობიექტი) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ნაკადი_წამკითხველი_ობიექტი) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&ნაკადი_ტექსტური_რედაქტორი_ობიექტი) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&მოლოდინი_ობიექტი) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ფაილი_წამკითხველი_ობიექტი) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ფაილი_ტექსტური_რედაქტორი_ობიექტი) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&საათი_ობიექტი) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
