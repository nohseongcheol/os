// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *መገዲ_ሓባሪ_ቁጽሪ(mp_obj_t ዋጋ) {
    size_t 개수; const char *መገዲ = mp_obj_str_get_data(ዋጋ, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!መገዲ[순번]) mp_raise_OSError(MP_EINVAL);
    return መገዲ;
}
static mp_obj_t 파일읽기(mp_obj_t ሽም) {
    intptr_t ፋይል_መትሓዚ = 결과검사(사용자호출(3, (uintptr_t)መገዲ_ሓባሪ_ቁጽሪ(ሽም), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t መጠን = 결과검사(사용자호출(9, ፋይል_መትሓዚ, 0, 0, 0, 0, 0));
        vstr_t ሓበሬታ; vstr_init_len(&ሓበሬታ, መጠን);
        intptr_t 결과 = 사용자호출(2, ፋይል_መትሓዚ, (uintptr_t)ሓበሬታ.buf, መጠን, 0, 0, 0);
        결과검사(결과); ሓበሬታ.len = 결과;
        mp_obj_t ዋጋ = mp_obj_new_bytes_from_vstr(&ሓበሬታ);
        nlr_pop(); 사용자호출(4, ፋይል_መትሓዚ, 0, 0, 0, 0, 0); return ዋጋ;
    }
    사용자호출(4, ፋይል_መትሓዚ, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ፋይል_ኣንባቢ_ነገር, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t መጠን=mp_obj_get_int(한도);
    if(መጠን<0||መጠን>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t ሓበሬታ; vstr_init_len(&ሓበሬታ,መጠን);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)ሓበሬታ.buf,መጠን,0,0,0);
    if(개수<0) { vstr_clear(&ሓበሬታ); 결과검사(개수); }
    ሓበሬታ.len=개수; return mp_obj_new_bytes_from_vstr(&ሓበሬታ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t ጸሓፍ_ፋይል(mp_obj_t ሽም, mp_obj_t ትሕዝቶ_ዋጋ) {
    const char *መገዲ = መገዲ_ሓባሪ_ቁጽሪ(ሽም);
    mp_buffer_info_t ሓበሬታ; mp_get_buffer_raise(ትሕዝቶ_ዋጋ, &ሓበሬታ, MP_BUFFER_READ);
    if (ሓበሬታ.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ፋይል_መትሓዚ = 결과검사(사용자호출(3, (uintptr_t)መገዲ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ፋይል_መትሓዚ, (uintptr_t)ሓበሬታ.buf, ሓበሬታ.len, 0, 0, 0);
    사용자호출(4, ፋይል_መትሓዚ, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ፋይል_ጸሓፊ_ነገር, ጸሓፍ_ፋይል);
static mp_obj_t ኣልግስ_ፋይል(mp_obj_t ሽም) { 결과검사(사용자호출(11, (uintptr_t)መገዲ_ሓባሪ_ቁጽሪ(ሽም), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ኣልግስ_ፋይል);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *ሓባሪ_ቁጽሪ_ተርታ) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(ሓባሪ_ቁጽሪ_ተርታ[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t መጠን[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, መጠን);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t ሰዓት_ዋጋ(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(ሰዓት_ነገር, ሰዓት_ዋጋ);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ፋይል_መትሓዚ = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, ፋይል_መትሓዚ, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, ፋይል_መትሓዚ, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(ፋይል_መትሓዚ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ፋይል_መትሓዚ, mp_obj_t 접속번호, mp_obj_t ትሕዝቶ_ዋጋ) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ሓበሬታ; mp_get_buffer_raise(ትሕዝቶ_ዋጋ, &ሓበሬታ, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ፋይል_መትሓዚ), (uintptr_t)ሓበሬታ.buf, ሓበሬታ.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t ዋጋ) {
    size_t ንውሓት_ዋጋ; const char *ጽሑፍ=mp_obj_str_get_data(ዋጋ,&ንውሓት_ዋጋ);
    unsigned 현재위치=0; uint32_t ኣድራሻ=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned ዋጋ=0,숫자수=0;
        while(현재위치<ንውሓት_ዋጋ&&ጽሑፍ[현재위치]>='0'&&ጽሑፍ[현재위치]<='9') {
            ዋጋ=ዋጋ*10+ጽሑፍ[현재위치++]-'0'; if(++숫자수>3||ዋጋ>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        ኣድራሻ=ኣድራሻ<<8|ዋጋ;
        if(부분<3&&(현재위치>=ንውሓት_ዋጋ||ጽሑፍ[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=ንውሓት_ዋጋ)mp_raise_OSError(MP_EINVAL);
    return ኣድራሻ;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *ሓባሪ_ቁጽሪ_ተርታ) {
    (void)항목수; uint32_t ኣድራሻ=인터넷주소읽기(ሓባሪ_ቁጽሪ_ተርታ[1]);
    int 접속번호=mp_obj_get_int(ሓባሪ_ቁጽሪ_ተርታ[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ሓበሬታ;mp_get_buffer_raise(ሓባሪ_ቁጽሪ_ተርታ[3],&ሓበሬታ,MP_BUFFER_READ);
    struct pk_sockaddr_in ዕላማ={0};ዕላማ.sin_family=AF_INET;ዕላማ.sin_port=pk_htons(접속번호);ዕላማ.sin_addr.s_addr=pk_htonl(ኣድራሻ);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(ሓባሪ_ቁጽሪ_ተርታ[0]),(uintptr_t)ሓበሬታ.buf,ሓበሬታ.len,0,(uintptr_t)&ዕላማ,sizeof(ዕላማ))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ፋይል_መትሓዚ) {
    unsigned char ሓበሬታ[512]; struct pk_sockaddr_in መዘና_ዋጋ; pk_socklen_t ንውሓት_ሓበሬታ = sizeof(መዘና_ዋጋ);
    intptr_t መጠን = 결과검사(사용자호출(35, mp_obj_get_int(ፋይል_መትሓዚ), (uintptr_t)ሓበሬታ, 512, 0, (uintptr_t)&መዘና_ዋጋ, (uintptr_t)&ንውሓት_ሓበሬታ));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(ሓበሬታ, መጠን), MP_OBJ_NEW_SMALL_INT(pk_htons(መዘና_ዋጋ.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ፋይል_መትሓዚ) { 결과검사(사용자호출(4, mp_obj_get_int(ፋይል_መትሓዚ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t ክፈት_ወሓዚ(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,መርበብ_ስድራቤት,ወሓዚ_ማሕበራዊ_ኔትወርክ,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ክፈት_ወሓዚ);
static mp_obj_t ኣላግብ_ወሓዚ(mp_obj_t 종단,mp_obj_t ኣድራሻ_ጽሑፍ,mp_obj_t መሐበሪ) {
    int 접속번호=mp_obj_get_int(መሐበሪ); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ኣድራሻ={0}; ኣድራሻ.ኣድራሻ_ስድራቤት=መርበብ_ስድራቤት;
    ኣድራሻ.접속번호=망차례짧은수(접속번호); ኣድራሻ.ናይ_መርበብ_ኣድራሻ.ኣድራሻ_ዋጋ=ማሕበራዊ_ኔትወርክ_ኢንቲጀር(인터넷주소읽기(ኣድራሻ_ጽሑፍ));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ኣድራሻ,sizeof(ኣድራሻ),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ወሓዚ_መላገቢ_ነገር,ኣላግብ_ወሓዚ);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int ንውሓት_ዋጋ=mp_obj_get_int(한도); if(ንውሓት_ዋጋ<1||ንውሓት_ዋጋ>512)mp_raise_OSError(MP_EINVAL);
    unsigned char ሓበሬታ[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)ሓበሬታ,ንውሓት_ዋጋ,0,0,0));
    return mp_obj_new_bytes(ሓበሬታ,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ወሓዚ_ኣንባቢ_ነገር,흐름읽기);
static mp_obj_t ጸሓፍ_ወሓዚ(mp_obj_t 종단,mp_obj_t ትሕዝቶ_ዋጋ) {
    mp_buffer_info_t ሓበሬታ; mp_get_buffer_raise(ትሕዝቶ_ዋጋ,&ሓበሬታ,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)ሓበሬታ.buf,ሓበሬታ.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ወሓዚ_ጸሓፊ_ነገር,ጸሓፍ_ወሓዚ);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t ሽም) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)መገዲ_ሓባሪ_ቁጽሪ(ሽም),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t ፍጠር_ሓባሪ_ማህደር(mp_obj_t ሽም) {
    결과검사(사용자호출(18,(uintptr_t)መገዲ_ሓባሪ_ቁጽሪ(ሽም),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,ፍጠር_ሓባሪ_ማህደር);
static mp_obj_t ኣልግስ_ሓባሪ_ማህደር(mp_obj_t ሽም) {
    결과검사(사용자호출(18,(uintptr_t)መገዲ_ሓባሪ_ቁጽሪ(ሽም),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ኣልግስ_ሓባሪ_ማህደር);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ወሓዚ_መላገቢ_ነገር) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ወሓዚ_ኣንባቢ_ነገር) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&ወሓዚ_ጸሓፊ_ነገር) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ፋይል_ኣንባቢ_ነገር) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ፋይል_ጸሓፊ_ነገር) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&ሰዓት_ነገር) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
