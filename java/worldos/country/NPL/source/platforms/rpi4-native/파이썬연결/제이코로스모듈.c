// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t मापन) { if (मापन < 0) mp_raise_OSError(-मापन); return मापन; }
static const char *बाटो_तर्क(mp_obj_t मान) {
    size_t 개수; const char *मार्ग = mp_obj_str_get_data(मान, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!मार्ग[순번]) mp_raise_OSError(MP_EINVAL);
    return मार्ग;
}
static mp_obj_t 파일읽기(mp_obj_t नाम) {
    intptr_t फाइल_ह्यान्डल = 결과검사(사용자호출(3, (uintptr_t)बाटो_तर्क(नाम), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t आकार = 결과검사(사용자호출(9, फाइल_ह्यान्डल, 0, 0, 0, 0, 0));
        vstr_t लगत; vstr_init_len(&लगत, आकार);
        intptr_t मापन = 사용자호출(2, फाइल_ह्यान्डल, (uintptr_t)लगत.buf, आकार, 0, 0, 0);
        결과검사(मापन); लगत.len = मापन;
        mp_obj_t मान = mp_obj_new_bytes_from_vstr(&लगत);
        nlr_pop(); 사용자호출(4, फाइल_ह्यान्डल, 0, 0, 0, 0, 0); return मान;
    }
    사용자호출(4, फाइल_ह्यान्डल, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(फाइल_पाठक_वस्तु, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t आकार=mp_obj_get_int(한도);
    if(आकार<0||आकार>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t लगत; vstr_init_len(&लगत,आकार);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)लगत.buf,आकार,0,0,0);
    if(개수<0) { vstr_clear(&लगत); 결과검사(개수); }
    लगत.len=개수; return mp_obj_new_bytes_from_vstr(&लगत);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t लेख्नुहोस्_फाइल(mp_obj_t नाम, mp_obj_t सामग्री_मान) {
    const char *मार्ग = बाटो_तर्क(नाम);
    mp_buffer_info_t लगत; mp_get_buffer_raise(सामग्री_मान, &लगत, MP_BUFFER_READ);
    if (लगत.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t फाइल_ह्यान्डल = 결과검사(사용자호출(3, (uintptr_t)मार्ग, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, फाइल_ह्यान्डल, (uintptr_t)लगत.buf, लगत.len, 0, 0, 0);
    사용자호출(4, फाइल_ह्यान्डल, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(फाइल_लेखक_वस्तु, लेख्नुहोस्_फाइल);
static mp_obj_t हटाउनुहोस्_फाइल(mp_obj_t नाम) { 결과검사(사용자호출(11, (uintptr_t)बाटो_तर्क(नाम), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, हटाउनुहोस्_फाइल);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *तर्क_विन्यास) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(तर्क_विन्यास[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t आकार[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, आकार);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t घडी_मान(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(घडी_वस्तु, घडी_मान);
static mp_obj_t युडिपी_सिर्जना(mp_obj_t 접속번호) {
    int लगत_राख्नुहोस् = mp_obj_get_int(접속번호); if (लगत_राख्नुहोस् < 0 || लगत_राख्नुहोस् > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t फाइल_ह्यान्डल = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(लगत_राख्नुहोस्); 첫째값.sin_addr.s_addr = 0;
    intptr_t मापन = 사용자호출(33, फाइल_ह्यान्डल, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (मापन < 0) { 사용자호출(4, फाइल_ह्यान्डल, 0, 0, 0, 0, 0); 결과검사(मापन); }
    return mp_obj_new_int(फाइल_ह्यान्डल);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, युडिपी_सिर्जना);
static mp_obj_t युडिपी_पठाउनुहोस्(mp_obj_t फाइल_ह्यान्डल, mp_obj_t 접속번호, mp_obj_t सामग्री_मान) {
    int लगत_राख्नुहोस् = mp_obj_get_int(접속번호); if (लगत_राख्नुहोस् < 1 || लगत_राख्नुहोस् > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t लगत; mp_get_buffer_raise(सामग्री_मान, &लगत, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(लगत_राख्नुहोस्); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(फाइल_ह्यान्डल), (uintptr_t)लगत.buf, लगत.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, युडिपी_पठाउनुहोस्);
static uint32_t 인터넷주소읽기(mp_obj_t मान) {
    size_t लम्बाइ_मान; const char *पाठ=mp_obj_str_get_data(मान,&लम्बाइ_मान);
    unsigned 현재위치=0; uint32_t ठेगाना=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned मान=0,숫자수=0;
        while(현재위치<लम्बाइ_मान&&पाठ[현재위치]>='0'&&पाठ[현재위치]<='9') {
            मान=मान*10+पाठ[현재위치++]-'0'; if(++숫자수>3||मान>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        ठेगाना=ठेगाना<<8|मान;
        if(부분<3&&(현재위치>=लम्बाइ_मान||पाठ[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=लम्बाइ_मान)mp_raise_OSError(MP_EINVAL);
    return ठेगाना;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *तर्क_विन्यास) {
    (void)항목수; uint32_t ठेगाना=인터넷주소읽기(तर्क_विन्यास[1]);
    int 접속번호=mp_obj_get_int(तर्क_विन्यास[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t लगत;mp_get_buffer_raise(तर्क_विन्यास[3],&लगत,MP_BUFFER_READ);
    struct pk_sockaddr_in लक्ष्य={0};लक्ष्य.sin_family=AF_INET;लक्ष्य.sin_port=pk_htons(접속번호);लक्ष्य.sin_addr.s_addr=pk_htonl(ठेगाना);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(तर्क_विन्यास[0]),(uintptr_t)लगत.buf,लगत.len,0,(uintptr_t)&लक्ष्य,sizeof(लक्ष्य))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t फाइल_ह्यान्डल) {
    unsigned char लगत[512]; struct pk_sockaddr_in समान_मान; pk_socklen_t लम्बाइ_लगत = sizeof(समान_मान);
    intptr_t आकार = 결과검사(사용자호출(35, mp_obj_get_int(फाइल_ह्यान्डल), (uintptr_t)लगत, 512, 0, (uintptr_t)&समान_मान, (uintptr_t)&लम्बाइ_लगत));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(लगत, आकार), MP_OBJ_NEW_SMALL_INT(pk_htons(समान_मान.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t युडिपी_बन्द_गर्नुहोस्(mp_obj_t फाइल_ह्यान्डल) { 결과검사(사용자호출(4, mp_obj_get_int(फाइल_ह्यान्डल), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, युडिपी_बन्द_गर्नुहोस्);
static mp_obj_t सिर्जना_प्रवाह(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,क्लाउड_परिवार,प्रवाह_सञ्जाल,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,सिर्जना_प्रवाह);
static mp_obj_t कनेक्ट_प्रवाह(mp_obj_t 종단,mp_obj_t ठेगाना_पाठ,mp_obj_t अनुक्रमणिका) {
    int 접속번호=mp_obj_get_int(अनुक्रमणिका); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ठेगाना={0}; ठेगाना.ठेगाना_परिवार=क्लाउड_परिवार;
    ठेगाना.접속번호=망차례짧은수(접속번호); ठेगाना.इन्टरनेट_ठेगाना.ठेगाना_मान=सञ्जाल_पूर्ण_सङ्ख्या(인터넷주소읽기(ठेगाना_पाठ));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ठेगाना,sizeof(ठेगाना),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(प्रवाह_योजक_वस्तु,कनेक्ट_प्रवाह);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int लम्बाइ_मान=mp_obj_get_int(한도); if(लम्बाइ_मान<1||लम्बाइ_मान>512)mp_raise_OSError(MP_EINVAL);
    unsigned char लगत[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)लगत,लम्बाइ_मान,0,0,0));
    return mp_obj_new_bytes(लगत,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(प्रवाह_पाठक_वस्तु,흐름읽기);
static mp_obj_t लेख्नुहोस्_प्रवाह(mp_obj_t 종단,mp_obj_t सामग्री_मान) {
    mp_buffer_info_t लगत; mp_get_buffer_raise(सामग्री_मान,&लगत,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)लगत.buf,लगत.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(प्रवाह_लेखक_वस्तु,लेख्नुहोस्_प्रवाह);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t नाम) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)बाटो_तर्क(नाम),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t सिर्जना_डाइरेक्टरी(mp_obj_t नाम) {
    결과검사(사용자호출(18,(uintptr_t)बाटो_तर्क(नाम),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(डाइरेक्टरी_सिर्जनाकर्ता_वस्तु,सिर्जना_डाइरेक्टरी);
static mp_obj_t हटाउनुहोस्_डाइरेक्टरी(mp_obj_t नाम) {
    결과검사(사용자호출(18,(uintptr_t)बाटो_तर्क(नाम),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,हटाउनुहोस्_डाइरेक्टरी);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&प्रवाह_योजक_वस्तु) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&प्रवाह_पाठक_वस्तु) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&प्रवाह_लेखक_वस्तु) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&डाइरेक्टरी_सिर्जनाकर्ता_वस्तु) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&फाइल_पाठक_वस्तु) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&फाइल_लेखक_वस्तु) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&घडी_वस्तु) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
