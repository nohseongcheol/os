// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t ప్రమాణం) { if (ప్రమాణం < 0) mp_raise_OSError(-ప్రమాణం); return ప్రమాణం; }
static const char *పథం_కారకం(mp_obj_t మూల్యం) {
    size_t 개수; const char *పాత్ = mp_obj_str_get_data(మూల్యం, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!పాత్[순번]) mp_raise_OSError(MP_EINVAL);
    return పాత్;
}
static mp_obj_t 파일읽기(mp_obj_t పేరు) {
    intptr_t ఫైలు_నిర్వాహకం = 결과검사(사용자호출(3, (uintptr_t)పథం_కారకం(పేరు), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t పరిమాణం = 결과검사(사용자호출(9, ఫైలు_నిర్వాహకం, 0, 0, 0, 0, 0));
        vstr_t డేటా; vstr_init_len(&డేటా, పరిమాణం);
        intptr_t ప్రమాణం = 사용자호출(2, ఫైలు_నిర్వాహకం, (uintptr_t)డేటా.buf, పరిమాణం, 0, 0, 0);
        결과검사(ప్రమాణం); డేటా.len = ప్రమాణం;
        mp_obj_t మూల్యం = mp_obj_new_bytes_from_vstr(&డేటా);
        nlr_pop(); 사용자호출(4, ఫైలు_నిర్వాహకం, 0, 0, 0, 0, 0); return మూల్యం;
    }
    사용자호출(4, ఫైలు_నిర్వాహకం, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ఫైలు_రీడర్_అంశం, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t పరిమాణం=mp_obj_get_int(한도);
    if(పరిమాణం<0||పరిమాణం>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t డేటా; vstr_init_len(&డేటా,పరిమాణం);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)డేటా.buf,పరిమాణం,0,0,0);
    if(개수<0) { vstr_clear(&డేటా); 결과검사(개수); }
    డేటా.len=개수; return mp_obj_new_bytes_from_vstr(&డేటా);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t వ్రాయి_ఫైలు(mp_obj_t పేరు, mp_obj_t విషయం_మూల్యం) {
    const char *పాత్ = పథం_కారకం(పేరు);
    mp_buffer_info_t డేటా; mp_get_buffer_raise(విషయం_మూల్యం, &డేటా, MP_BUFFER_READ);
    if (డేటా.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ఫైలు_నిర్వాహకం = 결과검사(사용자호출(3, (uintptr_t)పాత్, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ఫైలు_నిర్వాహకం, (uintptr_t)డేటా.buf, డేటా.len, 0, 0, 0);
    사용자호출(4, ఫైలు_నిర్వాహకం, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(파일쓰기객체, వ్రాయి_ఫైలు);
static mp_obj_t తీసివెయ్యి_ఫైలు(mp_obj_t పేరు) { 결과검사(사용자호출(11, (uintptr_t)పథం_కారకం(పేరు), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, తీసివెయ్యి_ఫైలు);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *కారకం_శ్రేణి) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(కారకం_శ్రేణి[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t పరిమాణం[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, పరిమాణం);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t గడియారం_మూల్యం(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(గడియారం_అంశం, గడియారం_మూల్యం);
static mp_obj_t 전문열기(mp_obj_t పోర్ట్_సంఖ్య) {
    int డేటా_స్థాయి = mp_obj_get_int(పోర్ట్_సంఖ్య); if (డేటా_స్థాయి < 0 || డేటా_స్థాయి > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ఫైలు_నిర్వాహకం = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(డేటా_స్థాయి); 첫째값.sin_addr.s_addr = 0;
    intptr_t ప్రమాణం = 사용자호출(33, ఫైలు_నిర్వాహకం, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (ప్రమాణం < 0) { 사용자호출(4, ఫైలు_నిర్వాహకం, 0, 0, 0, 0, 0); 결과검사(ప్రమాణం); }
    return mp_obj_new_int(ఫైలు_నిర్వాహకం);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ఫైలు_నిర్వాహకం, mp_obj_t పోర్ట్_సంఖ్య, mp_obj_t విషయం_మూల్యం) {
    int డేటా_స్థాయి = mp_obj_get_int(పోర్ట్_సంఖ్య); if (డేటా_స్థాయి < 1 || డేటా_స్థాయి > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t డేటా; mp_get_buffer_raise(విషయం_మూల్యం, &డేటా, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(డేటా_స్థాయి); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ఫైలు_నిర్వాహకం), (uintptr_t)డేటా.buf, డేటా.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t మూల్యం) {
    size_t పొడవు_మూల్యం; const char *పాఠ్యము=mp_obj_str_get_data(మూల్యం,&పొడవు_మూల్యం);
    unsigned 현재위치=0; uint32_t ఇమెయిల్=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned మూల్యం=0,숫자수=0;
        while(현재위치<పొడవు_మూల్యం&&పాఠ్యము[현재위치]>='0'&&పాఠ్యము[현재위치]<='9') {
            మూల్యం=మూల్యం*10+పాఠ్యము[현재위치++]-'0'; if(++숫자수>3||మూల్యం>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        ఇమెయిల్=ఇమెయిల్<<8|మూల్యం;
        if(부분<3&&(현재위치>=పొడవు_మూల్యం||పాఠ్యము[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=పొడవు_మూల్యం)mp_raise_OSError(MP_EINVAL);
    return ఇమెయిల్;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *కారకం_శ్రేణి) {
    (void)항목수; uint32_t ఇమెయిల్=인터넷주소읽기(కారకం_శ్రేణి[1]);
    int పోర్ట్_సంఖ్య=mp_obj_get_int(కారకం_శ్రేణి[2]);if(పోర్ట్_సంఖ్య<1||పోర్ట్_సంఖ్య>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t డేటా;mp_get_buffer_raise(కారకం_శ్రేణి[3],&డేటా,MP_BUFFER_READ);
    struct pk_sockaddr_in లక్ష్యం={0};లక్ష్యం.sin_family=AF_INET;లక్ష్యం.sin_port=pk_htons(పోర్ట్_సంఖ్య);లక్ష్యం.sin_addr.s_addr=pk_htonl(ఇమెయిల్);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(కారకం_శ్రేణి[0]),(uintptr_t)డేటా.buf,డేటా.len,0,(uintptr_t)&లక్ష్యం,sizeof(లక్ష్యం))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ఫైలు_నిర్వాహకం) {
    unsigned char డేటా[512]; struct pk_sockaddr_in పియర్_మూల్యం; pk_socklen_t పొడవు_డేటా = sizeof(పియర్_మూల్యం);
    intptr_t పరిమాణం = 결과검사(사용자호출(35, mp_obj_get_int(ఫైలు_నిర్వాహకం), (uintptr_t)డేటా, 512, 0, (uintptr_t)&పియర్_మూల్యం, (uintptr_t)&పొడవు_డేటా));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(డేటా, పరిమాణం), MP_OBJ_NEW_SMALL_INT(pk_htons(పియర్_మూల్యం.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ఫైలు_నిర్వాహకం) { 결과검사(사용자호출(4, mp_obj_get_int(ఫైలు_నిర్వాహకం), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t తెరువు_ధార(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,మేఘం_కుటుంబం,ధార_నెట్_వర్క్,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,తెరువు_ధార);
static mp_obj_t అనుసంధానించు_ధార(mp_obj_t 종단,mp_obj_t ఇమెయిల్_పాఠం,mp_obj_t సూచీ) {
    int పోర్ట్_సంఖ్య=mp_obj_get_int(సూచీ); if(పోర్ట్_సంఖ్య<1||పోర్ట్_సంఖ్య>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ఇమెయిల్={0}; ఇమెయిల్.ఇమెయిల్_కుటుంబం=మేఘం_కుటుంబం;
    ఇమెయిల్.పోర్ట్_సంఖ్య=망차례짧은수(పోర్ట్_సంఖ్య); ఇమెయిల్.ఇంటర్నెట్_చిరునామా.ఇమెయిల్_మూల్యం=నెట్_వర్క్_పూర్ణాంకం(인터넷주소읽기(ఇమెయిల్_పాఠం));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ఇమెయిల్,sizeof(ఇమెయిల్),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ధార_అనుసంధకం_అంశం,అనుసంధానించు_ధార);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int పొడవు_మూల్యం=mp_obj_get_int(한도); if(పొడవు_మూల్యం<1||పొడవు_మూల్యం>512)mp_raise_OSError(MP_EINVAL);
    unsigned char డేటా[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)డేటా,పొడవు_మూల్యం,0,0,0));
    return mp_obj_new_bytes(డేటా,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ధార_రీడర్_అంశం,흐름읽기);
static mp_obj_t వ్రాయి_ధార(mp_obj_t 종단,mp_obj_t విషయం_మూల్యం) {
    mp_buffer_info_t డేటా; mp_get_buffer_raise(విషయం_మూల్యం,&డేటా,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)డేటా.buf,డేటా.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(흐름쓰기객체,వ్రాయి_ధార);
static mp_obj_t 잠시기다리기(mp_obj_t సమయం_మూల్యం) {
    결과검사(사용자호출(17,mp_obj_get_int(సమయం_మూల్యం),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(వేచియుండు_అంశం,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t పేరు) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)పథం_కారకం(పేరు),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t క్రియేట్_సంచయని(mp_obj_t పేరు) {
    결과검사(사용자호출(18,(uintptr_t)పథం_కారకం(పేరు),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(సంచయని_సృష్టికర్త_అంశం,క్రియేట్_సంచయని);
static mp_obj_t తీసివెయ్యి_సంచయని(mp_obj_t పేరు) {
    결과검사(사용자호출(18,(uintptr_t)పథం_కారకం(పేరు),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,తీసివెయ్యి_సంచయని);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ధార_అనుసంధకం_అంశం) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ధార_రీడర్_అంశం) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&흐름쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&వేచియుండు_అంశం) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&సంచయని_సృష్టికర్త_అంశం) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ఫైలు_రీడర్_అంశం) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&파일쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&గడియారం_అంశం) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
