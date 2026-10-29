// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t मेजप) { if (मेजप < 0) mp_raise_OSError(-मेजप); return मेजप; }
static const char *पाथ_युक्तीवाद(mp_obj_t मोल) {
    size_t आयटम_COUNT; const char *पाथ = mp_obj_str_get_data(मोल, &आयटम_COUNT);
    if (!आयटम_COUNT || आयटम_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < आयटम_COUNT; 순번++) if (!पाथ[순번]) mp_raise_OSError(MP_EINVAL);
    return पाथ;
}
static mp_obj_t 파일읽기(mp_obj_t नांव) {
    intptr_t फायल_हँडल = 결과검사(사용자호출(3, (uintptr_t)पाथ_युक्तीवाद(नांव), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t आवाठ = 결과검사(사용자호출(9, फायल_हँडल, 0, 0, 0, 0, 0));
        vstr_t डेटा; vstr_init_len(&डेटा, आवाठ);
        intptr_t मेजप = 사용자호출(2, फायल_हँडल, (uintptr_t)डेटा.buf, आवाठ, 0, 0, 0);
        결과검사(मेजप); डेटा.len = मेजप;
        mp_obj_t मोल = mp_obj_new_bytes_from_vstr(&डेटा);
        nlr_pop(); 사용자호출(4, फायल_हँडल, 0, 0, 0, 0, 0); return मोल;
    }
    사용자호출(4, फायल_हँडल, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(फायल_वाचक_ऑब्जॅक्ट, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t आवाठ=mp_obj_get_int(한도);
    if(आवाठ<0||आवाठ>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t डेटा; vstr_init_len(&डेटा,आवाठ);
    intptr_t आयटम_COUNT=사용자호출(2,0,(uintptr_t)डेटा.buf,आवाठ,0,0,0);
    if(आयटम_COUNT<0) { vstr_clear(&डेटा); 결과검사(आयटम_COUNT); }
    डेटा.len=आयटम_COUNT; return mp_obj_new_bytes_from_vstr(&डेटा);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t बरोवचें_फायल(mp_obj_t नांव, mp_obj_t अनुक्रमणिका_मोल) {
    const char *पाथ = पाथ_युक्तीवाद(नांव);
    mp_buffer_info_t डेटा; mp_get_buffer_raise(अनुक्रमणिका_मोल, &डेटा, MP_BUFFER_READ);
    if (डेटा.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t फायल_हँडल = 결과검사(사용자호출(3, (uintptr_t)पाथ, 577, 0, 0, 0, 0));
    intptr_t प्रवेश_COUNT = 사용자호출(1, फायल_हँडल, (uintptr_t)डेटा.buf, डेटा.len, 0, 0, 0);
    사용자호출(4, फायल_हँडल, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(प्रवेश_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(फायल_बरोवपी_ऑब्जॅक्ट, बरोवचें_फायल);
static mp_obj_t काडचें_फायल(mp_obj_t नांव) { 결과검사(사용자호출(11, (uintptr_t)पाथ_युक्तीवाद(नांव), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, काडचें_फायल);
static mp_obj_t 사각형그리기(size_t आयटम_COUNT, const mp_obj_t *युक्तीवाद_क्रम) {
    (void)आयटम_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(युक्तीवाद_क्रम[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t आवाठ[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, आवाठ);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t घडयाळ_मोल(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(घडयाळ_ऑब्जॅक्ट, घडयाळ_मोल);
static mp_obj_t UDP_उगडचें(mp_obj_t 접속번호) {
    int डेटा_स्थिती = mp_obj_get_int(접속번호); if (डेटा_स्थिती < 0 || डेटा_स्थिती > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t फायल_हँडल = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(डेटा_स्थिती); 첫째값.sin_addr.s_addr = 0;
    intptr_t मेजप = 사용자호출(33, फायल_हँडल, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (मेजप < 0) { 사용자호출(4, फायल_हँडल, 0, 0, 0, 0, 0); 결과검사(मेजप); }
    return mp_obj_new_int(फायल_हँडल);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, UDP_उगडचें);
static mp_obj_t UDP_धाडचें(mp_obj_t फायल_हँडल, mp_obj_t 접속번호, mp_obj_t अनुक्रमणिका_मोल) {
    int डेटा_स्थिती = mp_obj_get_int(접속번호); if (डेटा_स्थिती < 1 || डेटा_स्थिती > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t डेटा; mp_get_buffer_raise(अनुक्रमणिका_मोल, &डेटा, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(डेटा_स्थिती); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(फायल_हँडल), (uintptr_t)डेटा.buf, डेटा.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, UDP_धाडचें);
static uint32_t 인터넷주소읽기(mp_obj_t मोल) {
    size_t लांबाय_मोल; const char *SMS=mp_obj_str_get_data(मोल,&लांबाय_मोल);
    unsigned 현재위치=0; uint32_t नामो=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned मोल=0,अंक_COUNT=0;
        while(현재위치<लांबाय_मोल&&SMS[현재위치]>='0'&&SMS[현재위치]<='9') {
            मोल=मोल*10+SMS[현재위치++]-'0'; if(++अंक_COUNT>3||मोल>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!अंक_COUNT)mp_raise_OSError(MP_EINVAL);
        नामो=नामो<<8|मोल;
        if(부분<3&&(현재위치>=लांबाय_मोल||SMS[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=लांबाय_मोल)mp_raise_OSError(MP_EINVAL);
    return नामो;
}
static mp_obj_t 전문주소전송(size_t प्रवेश_COUNT, const mp_obj_t *युक्तीवाद_क्रम) {
    (void)प्रवेश_COUNT; uint32_t नामो=인터넷주소읽기(युक्तीवाद_क्रम[1]);
    int 접속번호=mp_obj_get_int(युक्तीवाद_क्रम[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t डेटा;mp_get_buffer_raise(युक्तीवाद_क्रम[3],&डेटा,MP_BUFFER_READ);
    struct pk_sockaddr_in लक्ष्य={0};लक्ष्य.sin_family=AF_INET;लक्ष्य.sin_port=pk_htons(접속번호);लक्ष्य.sin_addr.s_addr=pk_htonl(नामो);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(युक्तीवाद_क्रम[0]),(uintptr_t)डेटा.buf,डेटा.len,0,(uintptr_t)&लक्ष्य,sizeof(लक्ष्य))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t फायल_हँडल) {
    unsigned char डेटा[512]; struct pk_sockaddr_in पीयर_मोल; pk_socklen_t लांबाय_डेटा = sizeof(पीयर_मोल);
    intptr_t आवाठ = 결과검사(사용자호출(35, mp_obj_get_int(फायल_हँडल), (uintptr_t)डेटा, 512, 0, (uintptr_t)&पीयर_मोल, (uintptr_t)&लांबाय_डेटा));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(डेटा, आवाठ), MP_OBJ_NEW_SMALL_INT(pk_htons(पीयर_मोल.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_शेवट(mp_obj_t फायल_हँडल) { 결과검사(사용자호출(4, mp_obj_get_int(फायल_हँडल), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, UDP_शेवट);
static mp_obj_t उगडचें_Stream(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,कूप_कुटुंब,Stream_नॅटवर्क,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,उगडचें_Stream);
static mp_obj_t कनॅक्ट_Stream(mp_obj_t 종단,mp_obj_t नामो_SMS,mp_obj_t INDEX) {
    int 접속번호=mp_obj_get_int(INDEX); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 नामो={0}; नामो.नामो_कुटुंब=कूप_कुटुंब;
    नामो.접속번호=망차례짧은수(접속번호); नामो.माजाळ्याचो_नामो.नामो_मोल=नॅटवर्क_पुर्णांक(인터넷주소읽기(नामो_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&नामो,sizeof(नामो),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(Stream_कनॅक्टर_ऑब्जॅक्ट,कनॅक्ट_Stream);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int लांबाय_मोल=mp_obj_get_int(한도); if(लांबाय_मोल<1||लांबाय_मोल>512)mp_raise_OSError(MP_EINVAL);
    unsigned char डेटा[512];
    intptr_t आयटम_COUNT=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)डेटा,लांबाय_मोल,0,0,0));
    return mp_obj_new_bytes(डेटा,आयटम_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_वाचक_ऑब्जॅक्ट,흐름읽기);
static mp_obj_t बरोवचें_Stream(mp_obj_t 종단,mp_obj_t अनुक्रमणिका_मोल) {
    mp_buffer_info_t डेटा; mp_get_buffer_raise(अनुक्रमणिका_मोल,&डेटा,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)डेटा.buf,डेटा.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Stream_बरोवपी_ऑब्जॅक्ट,बरोवचें_Stream);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_मोल) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_मोल),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t नांव) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)पाथ_युक्तीवाद(नांव),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t निर्माण_करचें_नामावळ(mp_obj_t नांव) {
    결과검사(사용자호출(18,(uintptr_t)पाथ_युक्तीवाद(नांव),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(नामावळ_निर्मातो_ऑब्जॅक्ट,निर्माण_करचें_नामावळ);
static mp_obj_t काडचें_नामावळ(mp_obj_t नांव) {
    결과검사(사용자호출(18,(uintptr_t)पाथ_युक्तीवाद(नांव),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,काडचें_नामावळ);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&Stream_कनॅक्टर_ऑब्जॅक्ट) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&Stream_वाचक_ऑब्जॅक्ट) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&Stream_बरोवपी_ऑब्जॅक्ट) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&नामावळ_निर्मातो_ऑब्जॅक्ट) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&फायल_वाचक_ऑब्जॅक्ट) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&फायल_बरोवपी_ऑब्जॅक्ट) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&घडयाळ_ऑब्जॅक्ट) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
