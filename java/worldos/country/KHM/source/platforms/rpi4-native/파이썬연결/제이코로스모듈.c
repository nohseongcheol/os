// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t ការវាស់វែង) { if (ការវាស់វែង < 0) mp_raise_OSError(-ការវាស់វែង); return ការវាស់វែង; }
static const char *ផ្លូវ_អាគុយម៉ង់(mp_obj_t តំលៃ) {
    size_t 개수; const char *ផ្លូវ = mp_obj_str_get_data(តំលៃ, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!ផ្លូវ[순번]) mp_raise_OSError(MP_EINVAL);
    return ផ្លូវ;
}
static mp_obj_t 파일읽기(mp_obj_t ឈ្មោះ) {
    intptr_t ឯកសារ_ការកាន់កាប់ = 결과검사(사용자호출(3, (uintptr_t)ផ្លូវ_អាគុយម៉ង់(ឈ្មោះ), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t ដាក់ទំហំ = 결과검사(사용자호출(9, ឯកសារ_ការកាន់កាប់, 0, 0, 0, 0, 0));
        vstr_t ទិន្នន័យ; vstr_init_len(&ទិន្នន័យ, ដាក់ទំហំ);
        intptr_t ការវាស់វែង = 사용자호출(2, ឯកសារ_ការកាន់កាប់, (uintptr_t)ទិន្នន័យ.buf, ដាក់ទំហំ, 0, 0, 0);
        결과검사(ការវាស់វែង); ទិន្នន័យ.len = ការវាស់វែង;
        mp_obj_t តំលៃ = mp_obj_new_bytes_from_vstr(&ទិន្នន័យ);
        nlr_pop(); 사용자호출(4, ឯកសារ_ការកាន់កាប់, 0, 0, 0, 0, 0); return តំលៃ;
    }
    사용자호출(4, ឯកសារ_ការកាន់កាប់, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ឯកសារ_អ្នកអាន_វត្ថុ, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t ដាក់ទំហំ=mp_obj_get_int(한도);
    if(ដាក់ទំហំ<0||ដាក់ទំហំ>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t ទិន្នន័យ; vstr_init_len(&ទិន្នន័យ,ដាក់ទំហំ);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)ទិន្នន័យ.buf,ដាក់ទំហំ,0,0,0);
    if(개수<0) { vstr_clear(&ទិន្នន័យ); 결과검사(개수); }
    ទិន្នន័យ.len=개수; return mp_obj_new_bytes_from_vstr(&ទិន្នន័យ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t សរសេរ_ឯកសារ(mp_obj_t ឈ្មោះ, mp_obj_t មាតិកា_តំលៃ) {
    const char *ផ្លូវ = ផ្លូវ_អាគុយម៉ង់(ឈ្មោះ);
    mp_buffer_info_t ទិន្នន័យ; mp_get_buffer_raise(មាតិកា_តំលៃ, &ទិន្នន័យ, MP_BUFFER_READ);
    if (ទិន្នន័យ.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ឯកសារ_ការកាន់កាប់ = 결과검사(사용자호출(3, (uintptr_t)ផ្លូវ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ឯកសារ_ការកាន់កាប់, (uintptr_t)ទិន្នន័យ.buf, ទិន្នន័យ.len, 0, 0, 0);
    사용자호출(4, ឯកសារ_ការកាន់កាប់, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ឯកសារ_អ្នកនិពន្ធ_វត្ថុ, សរសេរ_ឯកសារ);
static mp_obj_t យកចេញ_ឯកសារ(mp_obj_t ឈ្មោះ) { 결과검사(사용자호출(11, (uintptr_t)ផ្លូវ_អាគុយម៉ង់(ឈ្មោះ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, យកចេញ_ឯកសារ);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *អាគុយម៉ង់_អារេ) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(អាគុយម៉ង់_អារេ[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t ដាក់ទំហំ[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, ដាក់ទំហំ);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t នាឡិកា_តំលៃ(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(នាឡិកា_វត្ថុ, នាឡិកា_តំលៃ);
static mp_obj_t 전문열기(mp_obj_t លេខរន្ធ) {
    int ទិន្នន័យ_កំណត់ទីតាំង = mp_obj_get_int(លេខរន្ធ); if (ទិន្នន័យ_កំណត់ទីតាំង < 0 || ទិន្នន័យ_កំណត់ទីតាំង > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ឯកសារ_ការកាន់កាប់ = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ទិន្នន័យ_កំណត់ទីតាំង); 첫째값.sin_addr.s_addr = 0;
    intptr_t ការវាស់វែង = 사용자호출(33, ឯកសារ_ការកាន់កាប់, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (ការវាស់វែង < 0) { 사용자호출(4, ឯកសារ_ការកាន់កាប់, 0, 0, 0, 0, 0); 결과검사(ការវាស់វែង); }
    return mp_obj_new_int(ឯកសារ_ការកាន់កាប់);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ឯកសារ_ការកាន់កាប់, mp_obj_t លេខរន្ធ, mp_obj_t មាតិកា_តំលៃ) {
    int ទិន្នន័យ_កំណត់ទីតាំង = mp_obj_get_int(លេខរន្ធ); if (ទិន្នន័យ_កំណត់ទីតាំង < 1 || ទិន្នន័យ_កំណត់ទីតាំង > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ទិន្នន័យ; mp_get_buffer_raise(មាតិកា_តំលៃ, &ទិន្នន័យ, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ទិន្នន័យ_កំណត់ទីតាំង); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ឯកសារ_ការកាន់កាប់), (uintptr_t)ទិន្នន័យ.buf, ទិន្នន័យ.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t តំលៃ) {
    size_t ប្រវែង_តំលៃ; const char *អត្ថបទ=mp_obj_str_get_data(តំលៃ,&ប្រវែង_តំលៃ);
    unsigned 현재위치=0; uint32_t អ៊ីម៉ែល=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned តំលៃ=0,숫자수=0;
        while(현재위치<ប្រវែង_តំលៃ&&អត្ថបទ[현재위치]>='0'&&អត្ថបទ[현재위치]<='9') {
            តំលៃ=តំលៃ*10+អត្ថបទ[현재위치++]-'0'; if(++숫자수>3||តំលៃ>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        អ៊ីម៉ែល=អ៊ីម៉ែល<<8|តំលៃ;
        if(부분<3&&(현재위치>=ប្រវែង_តំលៃ||អត្ថបទ[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=ប្រវែង_តំលៃ)mp_raise_OSError(MP_EINVAL);
    return អ៊ីម៉ែល;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *អាគុយម៉ង់_អារេ) {
    (void)항목수; uint32_t អ៊ីម៉ែល=인터넷주소읽기(អាគុយម៉ង់_អារេ[1]);
    int លេខរន្ធ=mp_obj_get_int(អាគុយម៉ង់_អារេ[2]);if(លេខរន្ធ<1||លេខរន្ធ>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ទិន្នន័យ;mp_get_buffer_raise(អាគុយម៉ង់_អារេ[3],&ទិន្នន័យ,MP_BUFFER_READ);
    struct pk_sockaddr_in គោលដៅ={0};គោលដៅ.sin_family=AF_INET;គោលដៅ.sin_port=pk_htons(លេខរន្ធ);គោលដៅ.sin_addr.s_addr=pk_htonl(អ៊ីម៉ែល);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(អាគុយម៉ង់_អារេ[0]),(uintptr_t)ទិន្នន័យ.buf,ទិន្នន័យ.len,0,(uintptr_t)&គោលដៅ,sizeof(គោលដៅ))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ឯកសារ_ការកាន់កាប់) {
    unsigned char ទិន្នន័យ[512]; struct pk_sockaddr_in សិទ្ធស្មើ_តំលៃ; pk_socklen_t ប្រវែង_ទិន្នន័យ = sizeof(សិទ្ធស្មើ_តំលៃ);
    intptr_t ដាក់ទំហំ = 결과검사(사용자호출(35, mp_obj_get_int(ឯកសារ_ការកាន់កាប់), (uintptr_t)ទិន្នន័យ, 512, 0, (uintptr_t)&សិទ្ធស្មើ_តំលៃ, (uintptr_t)&ប្រវែង_ទិន្នន័យ));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(ទិន្នន័យ, ដាក់ទំហំ), MP_OBJ_NEW_SMALL_INT(pk_htons(សិទ្ធស្មើ_តំលៃ.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ឯកសារ_ការកាន់កាប់) { 결과검사(사용자호출(4, mp_obj_get_int(ឯកសារ_ការកាន់កាប់), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t បើក_ស្ទ្រីម(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,អ៊ីនធឺណិត_គ្រួសារ,ស្ទ្រីម_ណិតវឺក,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,បើក_ស្ទ្រីម);
static mp_obj_t ភ្ជាប់_ស្ទ្រីម(mp_obj_t 종단,mp_obj_t អ៊ីម៉ែល_អត្ថបទ,mp_obj_t សន្ទស្សន៏) {
    int លេខរន្ធ=mp_obj_get_int(សន្ទស្សន៏); if(លេខរន្ធ<1||លេខរន្ធ>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 អ៊ីម៉ែល={0}; អ៊ីម៉ែល.អ៊ីម៉ែល_គ្រួសារ=អ៊ីនធឺណិត_គ្រួសារ;
    អ៊ីម៉ែល.លេខរន្ធ=망차례짧은수(លេខរន្ធ); អ៊ីម៉ែល.អាសយដ្ឋានអ៊ីនធឺណិត.អ៊ីម៉ែល_តំលៃ=ណិតវឺក_ចំនួនគត់(인터넷주소읽기(អ៊ីម៉ែល_អត្ថបទ));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&អ៊ីម៉ែល,sizeof(អ៊ីម៉ែល),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ស្ទ្រីម_អង្គភ្ជាប់_វត្ថុ,ភ្ជាប់_ស្ទ្រីម);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int ប្រវែង_តំលៃ=mp_obj_get_int(한도); if(ប្រវែង_តំលៃ<1||ប្រវែង_តំលៃ>512)mp_raise_OSError(MP_EINVAL);
    unsigned char ទិន្នន័យ[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)ទិន្នន័យ,ប្រវែង_តំលៃ,0,0,0));
    return mp_obj_new_bytes(ទិន្នន័យ,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ស្ទ្រីម_អ្នកអាន_វត្ថុ,흐름읽기);
static mp_obj_t សរសេរ_ស្ទ្រីម(mp_obj_t 종단,mp_obj_t មាតិកា_តំលៃ) {
    mp_buffer_info_t ទិន្នន័យ; mp_get_buffer_raise(មាតិកា_តំលៃ,&ទិន្នន័យ,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)ទិន្នន័យ.buf,ទិន្នន័យ.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ស្ទ្រីម_អ្នកនិពន្ធ_វត្ថុ,សរសេរ_ស្ទ្រីម);
static mp_obj_t 잠시기다리기(mp_obj_t ពេល_វេលា_តំលៃ) {
    결과검사(사용자호출(17,mp_obj_get_int(ពេល_វេលា_តំលៃ),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(រង់ចាំ_វត្ថុ,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t ឈ្មោះ) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)ផ្លូវ_អាគុយម៉ង់(ឈ្មោះ),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t បង្កើត_បញ្ជី(mp_obj_t ឈ្មោះ) {
    결과검사(사용자호출(18,(uintptr_t)ផ្លូវ_អាគុយម៉ង់(ឈ្មោះ),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(បញ្ជី_អ្នកបង្កើត_វត្ថុ,បង្កើត_បញ្ជី);
static mp_obj_t យកចេញ_បញ្ជី(mp_obj_t ឈ្មោះ) {
    결과검사(사용자호출(18,(uintptr_t)ផ្លូវ_អាគុយម៉ង់(ឈ្មោះ),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,យកចេញ_បញ្ជី);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ស្ទ្រីម_អង្គភ្ជាប់_វត្ថុ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ស្ទ្រីម_អ្នកអាន_វត្ថុ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&ស្ទ្រីម_អ្នកនិពន្ធ_វត្ថុ) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&រង់ចាំ_វត្ថុ) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&បញ្ជី_អ្នកបង្កើត_វត្ថុ) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ឯកសារ_អ្នកអាន_វត្ថុ) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ឯកសារ_អ្នកនិពន្ធ_វត្ថុ) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&នាឡិកា_វត្ថុ) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
