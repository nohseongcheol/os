// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t ਮਾਪ) { if (ਮਾਪ < 0) mp_raise_OSError(-ਮਾਪ); return ਮਾਪ; }
static const char *ਰਸਤਾ_ਦਲੀਲ(mp_obj_t ਕੀਮਤ) {
    size_t 개수; const char *ਮਾਰਗ = mp_obj_str_get_data(ਕੀਮਤ, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!ਮਾਰਗ[순번]) mp_raise_OSError(MP_EINVAL);
    return ਮਾਰਗ;
}
static mp_obj_t 파일읽기(mp_obj_t ਨਾਂ) {
    intptr_t ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ = 결과검사(사용자호출(3, (uintptr_t)ਰਸਤਾ_ਦਲੀਲ(ਨਾਂ), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t ਆਕਾਰ = 결과검사(사용자호출(9, ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ, 0, 0, 0, 0, 0));
        vstr_t ਸਮੱਗਰੀ; vstr_init_len(&ਸਮੱਗਰੀ, ਆਕਾਰ);
        intptr_t ਮਾਪ = 사용자호출(2, ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ, (uintptr_t)ਸਮੱਗਰੀ.buf, ਆਕਾਰ, 0, 0, 0);
        결과검사(ਮਾਪ); ਸਮੱਗਰੀ.len = ਮਾਪ;
        mp_obj_t ਕੀਮਤ = mp_obj_new_bytes_from_vstr(&ਸਮੱਗਰੀ);
        nlr_pop(); 사용자호출(4, ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ, 0, 0, 0, 0, 0); return ਕੀਮਤ;
    }
    사용자호출(4, ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ਲਿਖਤ_ਪੱਤਰ_ਪਾਠਕ_ਔਬਜੈਕਟ, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t ਆਕਾਰ=mp_obj_get_int(한도);
    if(ਆਕਾਰ<0||ਆਕਾਰ>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t ਸਮੱਗਰੀ; vstr_init_len(&ਸਮੱਗਰੀ,ਆਕਾਰ);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)ਸਮੱਗਰੀ.buf,ਆਕਾਰ,0,0,0);
    if(개수<0) { vstr_clear(&ਸਮੱਗਰੀ); 결과검사(개수); }
    ਸਮੱਗਰੀ.len=개수; return mp_obj_new_bytes_from_vstr(&ਸਮੱਗਰੀ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ(mp_obj_t ਨਾਂ, mp_obj_t ਤਤਕਰਾ_ਕੀਮਤ) {
    const char *ਮਾਰਗ = ਰਸਤਾ_ਦਲੀਲ(ਨਾਂ);
    mp_buffer_info_t ਸਮੱਗਰੀ; mp_get_buffer_raise(ਤਤਕਰਾ_ਕੀਮਤ, &ਸਮੱਗਰੀ, MP_BUFFER_READ);
    if (ਸਮੱਗਰੀ.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ = 결과검사(사용자호출(3, (uintptr_t)ਮਾਰਗ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ, (uintptr_t)ਸਮੱਗਰੀ.buf, ਸਮੱਗਰੀ.len, 0, 0, 0);
    사용자호출(4, ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ਲਿਖਤ_ਪੱਤਰ_ਲੇਖਕ_ਔਬਜੈਕਟ, ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ);
static mp_obj_t ਹਟਾਉਣਾ_ਲਿਖਤ_ਪੱਤਰ(mp_obj_t ਨਾਂ) { 결과검사(사용자호출(11, (uintptr_t)ਰਸਤਾ_ਦਲੀਲ(ਨਾਂ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ਹਟਾਉਣਾ_ਲਿਖਤ_ਪੱਤਰ);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t ਆਕਾਰ[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, ਆਕਾਰ);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t ਘੜੀ_ਕੀਮਤ(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(ਘੜੀ_ਔਬਜੈਕਟ, ਘੜੀ_ਕੀਮਤ);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ = mp_obj_get_int(접속번호); if (ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ < 0 || ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ); 첫째값.sin_addr.s_addr = 0;
    intptr_t ਮਾਪ = 사용자호출(33, ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (ਮਾਪ < 0) { 사용자호출(4, ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ, 0, 0, 0, 0, 0); 결과검사(ਮਾਪ); }
    return mp_obj_new_int(ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ, mp_obj_t 접속번호, mp_obj_t ਤਤਕਰਾ_ਕੀਮਤ) {
    int ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ = mp_obj_get_int(접속번호); if (ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ < 1 || ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ਸਮੱਗਰੀ; mp_get_buffer_raise(ਤਤਕਰਾ_ਕੀਮਤ, &ਸਮੱਗਰੀ, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ), (uintptr_t)ਸਮੱਗਰੀ.buf, ਸਮੱਗਰੀ.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t ਕੀਮਤ) {
    size_t ਲੰਬਾਈ_ਕੀਮਤ; const char *ਟੈਕਸਟ=mp_obj_str_get_data(ਕੀਮਤ,&ਲੰਬਾਈ_ਕੀਮਤ);
    unsigned 현재위치=0; uint32_t ਪਤਾ=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned ਕੀਮਤ=0,숫자수=0;
        while(현재위치<ਲੰਬਾਈ_ਕੀਮਤ&&ਟੈਕਸਟ[현재위치]>='0'&&ਟੈਕਸਟ[현재위치]<='9') {
            ਕੀਮਤ=ਕੀਮਤ*10+ਟੈਕਸਟ[현재위치++]-'0'; if(++숫자수>3||ਕੀਮਤ>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        ਪਤਾ=ਪਤਾ<<8|ਕੀਮਤ;
        if(부분<3&&(현재위치>=ਲੰਬਾਈ_ਕੀਮਤ||ਟੈਕਸਟ[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=ਲੰਬਾਈ_ਕੀਮਤ)mp_raise_OSError(MP_EINVAL);
    return ਪਤਾ;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ) {
    (void)항목수; uint32_t ਪਤਾ=인터넷주소읽기(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ[1]);
    int 접속번호=mp_obj_get_int(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ਸਮੱਗਰੀ;mp_get_buffer_raise(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ[3],&ਸਮੱਗਰੀ,MP_BUFFER_READ);
    struct pk_sockaddr_in ਟੀਚਾ={0};ਟੀਚਾ.sin_family=AF_INET;ਟੀਚਾ.sin_port=pk_htons(접속번호);ਟੀਚਾ.sin_addr.s_addr=pk_htonl(ਪਤਾ);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ[0]),(uintptr_t)ਸਮੱਗਰੀ.buf,ਸਮੱਗਰੀ.len,0,(uintptr_t)&ਟੀਚਾ,sizeof(ਟੀਚਾ))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ) {
    unsigned char ਸਮੱਗਰੀ[512]; struct pk_sockaddr_in ਪਿਅਰ_ਕੀਮਤ; pk_socklen_t ਲੰਬਾਈ_ਸਮੱਗਰੀ = sizeof(ਪਿਅਰ_ਕੀਮਤ);
    intptr_t ਆਕਾਰ = 결과검사(사용자호출(35, mp_obj_get_int(ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ), (uintptr_t)ਸਮੱਗਰੀ, 512, 0, (uintptr_t)&ਪਿਅਰ_ਕੀਮਤ, (uintptr_t)&ਲੰਬਾਈ_ਸਮੱਗਰੀ));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(ਸਮੱਗਰੀ, ਆਕਾਰ), MP_OBJ_NEW_SMALL_INT(pk_htons(ਪਿਅਰ_ਕੀਮਤ.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ) { 결과검사(사용자호출(4, mp_obj_get_int(ਲਿਖਤ_ਪੱਤਰ_ਸੰਭਾਲਣਾ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t ਖੋਲੋ_ਸਟ੍ਰੀਮ(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,ਬੱਦਲ_ਪਰਿਵਾਰ,ਸਟ੍ਰੀਮ_ਨੈਟਵਰਕ,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ਖੋਲੋ_ਸਟ੍ਰੀਮ);
static mp_obj_t ਕਨੈਕਟ_ਕਰੋ_ਸਟ੍ਰੀਮ(mp_obj_t 종단,mp_obj_t ਪਤਾ_ਪਾਠ,mp_obj_t ਅਨੁਕ੍ਰਮਣਿਕਾ) {
    int 접속번호=mp_obj_get_int(ਅਨੁਕ੍ਰਮਣਿਕਾ); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ਪਤਾ={0}; ਪਤਾ.ਪਤਾ_ਪਰਿਵਾਰ=ਬੱਦਲ_ਪਰਿਵਾਰ;
    ਪਤਾ.접속번호=망차례짧은수(접속번호); ਪਤਾ.ਇੰਟਰਨੈਟ_ਪਤਾ.ਪਤਾ_ਕੀਮਤ=ਨੈਟਵਰਕ_ਪੂਰਣ_ਅੰਕ(인터넷주소읽기(ਪਤਾ_ਪਾਠ));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ਪਤਾ,sizeof(ਪਤਾ),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ਸਟ੍ਰੀਮ_ਕਨੈਕਟਰ_ਔਬਜੈਕਟ,ਕਨੈਕਟ_ਕਰੋ_ਸਟ੍ਰੀਮ);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int ਲੰਬਾਈ_ਕੀਮਤ=mp_obj_get_int(한도); if(ਲੰਬਾਈ_ਕੀਮਤ<1||ਲੰਬਾਈ_ਕੀਮਤ>512)mp_raise_OSError(MP_EINVAL);
    unsigned char ਸਮੱਗਰੀ[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)ਸਮੱਗਰੀ,ਲੰਬਾਈ_ਕੀਮਤ,0,0,0));
    return mp_obj_new_bytes(ਸਮੱਗਰੀ,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ਸਟ੍ਰੀਮ_ਪਾਠਕ_ਔਬਜੈਕਟ,흐름읽기);
static mp_obj_t ਲਿੱਖੋ_ਸਟ੍ਰੀਮ(mp_obj_t 종단,mp_obj_t ਤਤਕਰਾ_ਕੀਮਤ) {
    mp_buffer_info_t ਸਮੱਗਰੀ; mp_get_buffer_raise(ਤਤਕਰਾ_ਕੀਮਤ,&ਸਮੱਗਰੀ,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)ਸਮੱਗਰੀ.buf,ਸਮੱਗਰੀ.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ਸਟ੍ਰੀਮ_ਲੇਖਕ_ਔਬਜੈਕਟ,ਲਿੱਖੋ_ਸਟ੍ਰੀਮ);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t ਨਾਂ) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)ਰਸਤਾ_ਦਲੀਲ(ਨਾਂ),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t ਬਣਾਓ_ਨਿਰਦੇਸ਼ਕ(mp_obj_t ਨਾਂ) {
    결과검사(사용자호출(18,(uintptr_t)ਰਸਤਾ_ਦਲੀਲ(ਨਾਂ),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(ਨਿਰਦੇਸ਼ਕ_ਸਿਰਜਣਹਾਰ_ਔਬਜੈਕਟ,ਬਣਾਓ_ਨਿਰਦੇਸ਼ਕ);
static mp_obj_t ਹਟਾਉਣਾ_ਨਿਰਦੇਸ਼ਕ(mp_obj_t ਨਾਂ) {
    결과검사(사용자호출(18,(uintptr_t)ਰਸਤਾ_ਦਲੀਲ(ਨਾਂ),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ਹਟਾਉਣਾ_ਨਿਰਦੇਸ਼ਕ);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ਸਟ੍ਰੀਮ_ਕਨੈਕਟਰ_ਔਬਜੈਕਟ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ਸਟ੍ਰੀਮ_ਪਾਠਕ_ਔਬਜੈਕਟ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&ਸਟ੍ਰੀਮ_ਲੇਖਕ_ਔਬਜੈਕਟ) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&ਨਿਰਦੇਸ਼ਕ_ਸਿਰਜਣਹਾਰ_ਔਬਜੈਕਟ) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ਲਿਖਤ_ਪੱਤਰ_ਪਾਠਕ_ਔਬਜੈਕਟ) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ਲਿਖਤ_ਪੱਤਰ_ਲੇਖਕ_ਔਬਜੈਕਟ) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&ਘੜੀ_ਔਬਜੈਕਟ) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
