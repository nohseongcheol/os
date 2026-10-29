// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t ልኬት) { if (ልኬት < 0) mp_raise_OSError(-ልኬት); return ልኬት; }
static const char *ዱካ_ነጋሪ_እሴት(mp_obj_t እሴት) {
    size_t 개수; const char *መተላለፊያ = mp_obj_str_get_data(እሴት, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!መተላለፊያ[순번]) mp_raise_OSError(MP_EINVAL);
    return መተላለፊያ;
}
static mp_obj_t 파일읽기(mp_obj_t ስም) {
    intptr_t ፋይል_እጀታ = 결과검사(사용자호출(3, (uintptr_t)ዱካ_ነጋሪ_እሴት(ስም), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t መጠን = 결과검사(사용자호출(9, ፋይል_እጀታ, 0, 0, 0, 0, 0));
        vstr_t ውሂብ; vstr_init_len(&ውሂብ, መጠን);
        intptr_t ልኬት = 사용자호출(2, ፋይል_እጀታ, (uintptr_t)ውሂብ.buf, መጠን, 0, 0, 0);
        결과검사(ልኬት); ውሂብ.len = ልኬት;
        mp_obj_t እሴት = mp_obj_new_bytes_from_vstr(&ውሂብ);
        nlr_pop(); 사용자호출(4, ፋይል_እጀታ, 0, 0, 0, 0, 0); return እሴት;
    }
    사용자호출(4, ፋይል_እጀታ, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ፋይል_አንባቢ_ነገር, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t መጠን=mp_obj_get_int(한도);
    if(መጠን<0||መጠን>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t ውሂብ; vstr_init_len(&ውሂብ,መጠን);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)ውሂብ.buf,መጠን,0,0,0);
    if(개수<0) { vstr_clear(&ውሂብ); 결과검사(개수); }
    ውሂብ.len=개수; return mp_obj_new_bytes_from_vstr(&ውሂብ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t ጻፍ_ፋይል(mp_obj_t ስም, mp_obj_t ይዘት_እሴት) {
    const char *መተላለፊያ = ዱካ_ነጋሪ_እሴት(ስም);
    mp_buffer_info_t ውሂብ; mp_get_buffer_raise(ይዘት_እሴት, &ውሂብ, MP_BUFFER_READ);
    if (ውሂብ.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ፋይል_እጀታ = 결과검사(사용자호출(3, (uintptr_t)መተላለፊያ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ፋይል_እጀታ, (uintptr_t)ውሂብ.buf, ውሂብ.len, 0, 0, 0);
    사용자호출(4, ፋይል_እጀታ, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ፋይል_ፀሐፊ_ነገር, ጻፍ_ፋይል);
static mp_obj_t አስወግድ_ፋይል(mp_obj_t ስም) { 결과검사(사용자호출(11, (uintptr_t)ዱካ_ነጋሪ_እሴት(ስም), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, አስወግድ_ፋይል);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *ነጋሪ_እሴት_ድርድር) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(ነጋሪ_እሴት_ድርድር[순번]);
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
static mp_obj_t ሰዓት_እሴት(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(ሰዓት_ነገር, ሰዓት_እሴት);
static mp_obj_t 전문열기(mp_obj_t የወደብ_ቁጥር) {
    int ውሂብ_በቦታ_አስቀመጠ = mp_obj_get_int(የወደብ_ቁጥር); if (ውሂብ_በቦታ_አስቀመጠ < 0 || ውሂብ_በቦታ_አስቀመጠ > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ፋይል_እጀታ = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ውሂብ_በቦታ_አስቀመጠ); 첫째값.sin_addr.s_addr = 0;
    intptr_t ልኬት = 사용자호출(33, ፋይል_እጀታ, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (ልኬት < 0) { 사용자호출(4, ፋይል_እጀታ, 0, 0, 0, 0, 0); 결과검사(ልኬት); }
    return mp_obj_new_int(ፋይል_እጀታ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ፋይል_እጀታ, mp_obj_t የወደብ_ቁጥር, mp_obj_t ይዘት_እሴት) {
    int ውሂብ_በቦታ_አስቀመጠ = mp_obj_get_int(የወደብ_ቁጥር); if (ውሂብ_በቦታ_አስቀመጠ < 1 || ውሂብ_በቦታ_አስቀመጠ > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ውሂብ; mp_get_buffer_raise(ይዘት_እሴት, &ውሂብ, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ውሂብ_በቦታ_አስቀመጠ); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ፋይል_እጀታ), (uintptr_t)ውሂብ.buf, ውሂብ.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t እሴት) {
    size_t ርዝመት_እሴት; const char *ጽሁፍ=mp_obj_str_get_data(እሴት,&ርዝመት_እሴት);
    unsigned 현재위치=0; uint32_t አድራሻ=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned እሴት=0,숫자수=0;
        while(현재위치<ርዝመት_እሴት&&ጽሁፍ[현재위치]>='0'&&ጽሁፍ[현재위치]<='9') {
            እሴት=እሴት*10+ጽሁፍ[현재위치++]-'0'; if(++숫자수>3||እሴት>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        አድራሻ=አድራሻ<<8|እሴት;
        if(부분<3&&(현재위치>=ርዝመት_እሴት||ጽሁፍ[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=ርዝመት_እሴት)mp_raise_OSError(MP_EINVAL);
    return አድራሻ;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *ነጋሪ_እሴት_ድርድር) {
    (void)항목수; uint32_t አድራሻ=인터넷주소읽기(ነጋሪ_እሴት_ድርድር[1]);
    int የወደብ_ቁጥር=mp_obj_get_int(ነጋሪ_እሴት_ድርድር[2]);if(የወደብ_ቁጥር<1||የወደብ_ቁጥር>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ውሂብ;mp_get_buffer_raise(ነጋሪ_እሴት_ድርድር[3],&ውሂብ,MP_BUFFER_READ);
    struct pk_sockaddr_in ዓላማ={0};ዓላማ.sin_family=AF_INET;ዓላማ.sin_port=pk_htons(የወደብ_ቁጥር);ዓላማ.sin_addr.s_addr=pk_htonl(አድራሻ);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(ነጋሪ_እሴት_ድርድር[0]),(uintptr_t)ውሂብ.buf,ውሂብ.len,0,(uintptr_t)&ዓላማ,sizeof(ዓላማ))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ፋይል_እጀታ) {
    unsigned char ውሂብ[512]; struct pk_sockaddr_in አቻ_እሴት; pk_socklen_t ርዝመት_ውሂብ = sizeof(አቻ_እሴት);
    intptr_t መጠን = 결과검사(사용자호출(35, mp_obj_get_int(ፋይል_እጀታ), (uintptr_t)ውሂብ, 512, 0, (uintptr_t)&አቻ_እሴት, (uintptr_t)&ርዝመት_ውሂብ));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(ውሂብ, መጠን), MP_OBJ_NEW_SMALL_INT(pk_htons(አቻ_እሴት.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ፋይል_እጀታ) { 결과검사(사용자호출(4, mp_obj_get_int(ፋይል_እጀታ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t ክፈት_ልቀቅ(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,ክላውድ_ቤተሰብ,ልቀቅ_መረብ,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ክፈት_ልቀቅ);
static mp_obj_t አገናኝ_ልቀቅ(mp_obj_t 종단,mp_obj_t አድራሻ_ጽሁፍ,mp_obj_t መረጃ_ጠቆመ) {
    int የወደብ_ቁጥር=mp_obj_get_int(መረጃ_ጠቆመ); if(የወደብ_ቁጥር<1||የወደብ_ቁጥር>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 አድራሻ={0}; አድራሻ.አድራሻ_ቤተሰብ=ክላውድ_ቤተሰብ;
    አድራሻ.የወደብ_ቁጥር=망차례짧은수(የወደብ_ቁጥር); አድራሻ.የበይነመረብ_አድራሻ.አድራሻ_እሴት=መረብ_ኢንተጀር(인터넷주소읽기(አድራሻ_ጽሁፍ));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&አድራሻ,sizeof(አድራሻ),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ልቀቅ_አገናኝ_ነገር,አገናኝ_ልቀቅ);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int ርዝመት_እሴት=mp_obj_get_int(한도); if(ርዝመት_እሴት<1||ርዝመት_እሴት>512)mp_raise_OSError(MP_EINVAL);
    unsigned char ውሂብ[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)ውሂብ,ርዝመት_እሴት,0,0,0));
    return mp_obj_new_bytes(ውሂብ,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ልቀቅ_አንባቢ_ነገር,흐름읽기);
static mp_obj_t ጻፍ_ልቀቅ(mp_obj_t 종단,mp_obj_t ይዘት_እሴት) {
    mp_buffer_info_t ውሂብ; mp_get_buffer_raise(ይዘት_እሴት,&ውሂብ,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)ውሂብ.buf,ውሂብ.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ልቀቅ_ፀሐፊ_ነገር,ጻፍ_ልቀቅ);
static mp_obj_t 잠시기다리기(mp_obj_t ጊዜ_እሴት) {
    결과검사(사용자호출(17,mp_obj_get_int(ጊዜ_እሴት),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(መጠበቅ_ነገር,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t ስም) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)ዱካ_ነጋሪ_እሴት(ስም),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t ፍጠር_ማውጫ(mp_obj_t ስም) {
    결과검사(사용자호출(18,(uintptr_t)ዱካ_ነጋሪ_እሴት(ስም),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,ፍጠር_ማውጫ);
static mp_obj_t አስወግድ_ማውጫ(mp_obj_t ስም) {
    결과검사(사용자호출(18,(uintptr_t)ዱካ_ነጋሪ_እሴት(ስም),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,አስወግድ_ማውጫ);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ልቀቅ_አገናኝ_ነገር) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ልቀቅ_አንባቢ_ነገር) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&ልቀቅ_ፀሐፊ_ነገር) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&መጠበቅ_ነገር) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ፋይል_አንባቢ_ነገር) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ፋይል_ፀሐፊ_ነገር) },
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
