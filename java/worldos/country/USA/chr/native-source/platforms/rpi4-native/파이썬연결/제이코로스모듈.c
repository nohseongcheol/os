// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) mp_raise_OSError(-결과); return 결과; }
static const char *ᎠᏍᏓᏩᏛᏍᏗ_ᏗᏓᎦᏘᎸᏍᏗ(mp_obj_t ᏧᎬᏩᎶᏗᏯ) {
    size_t 개수; const char *ᎠᏍᏓᏩᏛᏍᏗ = mp_obj_str_get_data(ᏧᎬᏩᎶᏗᏯ, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!ᎠᏍᏓᏩᏛᏍᏗ[순번]) mp_raise_OSError(MP_EINVAL);
    return ᎠᏍᏓᏩᏛᏍᏗ;
}
static mp_obj_t 파일읽기(mp_obj_t ᏚᏙᎥᎢ) {
    intptr_t ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ = 결과검사(사용자호출(3, (uintptr_t)ᎠᏍᏓᏩᏛᏍᏗ_ᏗᏓᎦᏘᎸᏍᏗ(ᏚᏙᎥᎢ), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t ᎢᎩᏓ = 결과검사(사용자호출(9, ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ, 0, 0, 0, 0, 0));
        vstr_t ᎦᏟᏌᏅᎯ; vstr_init_len(&ᎦᏟᏌᏅᎯ, ᎢᎩᏓ);
        intptr_t 결과 = 사용자호출(2, ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ, (uintptr_t)ᎦᏟᏌᏅᎯ.buf, ᎢᎩᏓ, 0, 0, 0);
        결과검사(결과); ᎦᏟᏌᏅᎯ.len = 결과;
        mp_obj_t ᏧᎬᏩᎶᏗᏯ = mp_obj_new_bytes_from_vstr(&ᎦᏟᏌᏅᎯ);
        nlr_pop(); 사용자호출(4, ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ, 0, 0, 0, 0, 0); return ᏧᎬᏩᎶᏗᏯ;
    }
    사용자호출(4, ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ᎠᏍᏆᏂᎪᏙᏗ_ᏗᎪᎵᏰᏍᎩ_ᎪᎱᏍᏗ, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t ᎢᎩᏓ=mp_obj_get_int(한도);
    if(ᎢᎩᏓ<0||ᎢᎩᏓ>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t ᎦᏟᏌᏅᎯ; vstr_init_len(&ᎦᏟᏌᏅᎯ,ᎢᎩᏓ);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)ᎦᏟᏌᏅᎯ.buf,ᎢᎩᏓ,0,0,0);
    if(개수<0) { vstr_clear(&ᎦᏟᏌᏅᎯ); 결과검사(개수); }
    ᎦᏟᏌᏅᎯ.len=개수; return mp_obj_new_bytes_from_vstr(&ᎦᏟᏌᏅᎯ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t ᎪᏪᎶᏗ_ᎠᏍᏆᏂᎪᏙᏗ(mp_obj_t ᏚᏙᎥᎢ, mp_obj_t ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ) {
    const char *ᎠᏍᏓᏩᏛᏍᏗ = ᎠᏍᏓᏩᏛᏍᏗ_ᏗᏓᎦᏘᎸᏍᏗ(ᏚᏙᎥᎢ);
    mp_buffer_info_t ᎦᏟᏌᏅᎯ; mp_get_buffer_raise(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ, &ᎦᏟᏌᏅᎯ, MP_BUFFER_READ);
    if (ᎦᏟᏌᏅᎯ.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ = 결과검사(사용자호출(3, (uintptr_t)ᎠᏍᏓᏩᏛᏍᏗ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ, (uintptr_t)ᎦᏟᏌᏅᎯ.buf, ᎦᏟᏌᏅᎯ.len, 0, 0, 0);
    사용자호출(4, ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(파일쓰기객체, ᎪᏪᎶᏗ_ᎠᏍᏆᏂᎪᏙᏗ);
static mp_obj_t ᎯᎲᎾ_ᎠᏍᏆᏂᎪᏙᏗ(mp_obj_t ᏚᏙᎥᎢ) { 결과검사(사용자호출(11, (uintptr_t)ᎠᏍᏓᏩᏛᏍᏗ_ᏗᏓᎦᏘᎸᏍᏗ(ᏚᏙᎥᎢ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ᎯᎲᎾ_ᎠᏍᏆᏂᎪᏙᏗ);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *ᏗᏓᎦᏘᎸᏍᏗ_array) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(ᏗᏓᎦᏘᎸᏍᏗ_array[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t ᎢᎩᏓ[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, ᎢᎩᏓ);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t ᏩᏥ_ᏧᎬᏩᎶᏗᏯ(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(ᏩᏥ_ᎪᎱᏍᏗ, ᏩᏥ_ᏧᎬᏩᎶᏗᏯ);
static mp_obj_t 전문열기(mp_obj_t 접속번호) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 0 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = 0;
    intptr_t 결과 = 사용자호출(33, ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (결과 < 0) { 사용자호출(4, ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ, 0, 0, 0, 0, 0); 결과검사(결과); }
    return mp_obj_new_int(ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ, mp_obj_t 접속번호, mp_obj_t ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ) {
    int 자료위치 = mp_obj_get_int(접속번호); if (자료위치 < 1 || 자료위치 > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ᎦᏟᏌᏅᎯ; mp_get_buffer_raise(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ, &ᎦᏟᏌᏅᎯ, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(자료위치); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ), (uintptr_t)ᎦᏟᏌᏅᎯ.buf, ᎦᏟᏌᏅᎯ.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t ᏧᎬᏩᎶᏗᏯ) {
    size_t ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ; const char *ᎠᎪᎵᏰᏗ=mp_obj_str_get_data(ᏧᎬᏩᎶᏗᏯ,&ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);
    unsigned 현재위치=0; uint32_t ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned ᏧᎬᏩᎶᏗᏯ=0,숫자수=0;
        while(현재위치<ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ&&ᎠᎪᎵᏰᏗ[현재위치]>='0'&&ᎠᎪᎵᏰᏗ[현재위치]<='9') {
            ᏧᎬᏩᎶᏗᏯ=ᏧᎬᏩᎶᏗᏯ*10+ᎠᎪᎵᏰᏗ[현재위치++]-'0'; if(++숫자수>3||ᏧᎬᏩᎶᏗᏯ>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=ᎪᏪᎵ_ᏫᏗᎦᏅᏗ<<8|ᏧᎬᏩᎶᏗᏯ;
        if(부분<3&&(현재위치>=ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ||ᎠᎪᎵᏰᏗ[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ)mp_raise_OSError(MP_EINVAL);
    return ᎪᏪᎵ_ᏫᏗᎦᏅᏗ;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *ᏗᏓᎦᏘᎸᏍᏗ_array) {
    (void)항목수; uint32_t ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=인터넷주소읽기(ᏗᏓᎦᏘᎸᏍᏗ_array[1]);
    int 접속번호=mp_obj_get_int(ᏗᏓᎦᏘᎸᏍᏗ_array[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ᎦᏟᏌᏅᎯ;mp_get_buffer_raise(ᏗᏓᎦᏘᎸᏍᏗ_array[3],&ᎦᏟᏌᏅᎯ,MP_BUFFER_READ);
    struct pk_sockaddr_in ᎠᏉᏅᏗᎢ={0};ᎠᏉᏅᏗᎢ.sin_family=AF_INET;ᎠᏉᏅᏗᎢ.sin_port=pk_htons(접속번호);ᎠᏉᏅᏗᎢ.sin_addr.s_addr=pk_htonl(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(ᏗᏓᎦᏘᎸᏍᏗ_array[0]),(uintptr_t)ᎦᏟᏌᏅᎯ.buf,ᎦᏟᏌᏅᎯ.len,0,(uintptr_t)&ᎠᏉᏅᏗᎢ,sizeof(ᎠᏉᏅᏗᎢ))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ) {
    unsigned char ᎦᏟᏌᏅᎯ[512]; struct pk_sockaddr_in ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ; pk_socklen_t ᏱᎦᏅᎯᏓ_ᎦᏟᏌᏅᎯ = sizeof(ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ);
    intptr_t ᎢᎩᏓ = 결과검사(사용자호출(35, mp_obj_get_int(ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ), (uintptr_t)ᎦᏟᏌᏅᎯ, 512, 0, (uintptr_t)&ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ, (uintptr_t)&ᏱᎦᏅᎯᏓ_ᎦᏟᏌᏅᎯ));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(ᎦᏟᏌᏅᎯ, ᎢᎩᏓ), MP_OBJ_NEW_SMALL_INT(pk_htons(ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ) { 결과검사(사용자호출(4, mp_obj_get_int(ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t ᎯᏍᏚᎢ_ᎤᏪᎬ(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,인터넷주소갈래,ᎤᏪᎬ_ᏧᎾᏚᏓᎵ,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ᎯᏍᏚᎢ_ᎤᏪᎬ);
static mp_obj_t ᎫᏓᎳ_ᎤᏪᎬ(mp_obj_t 종단,mp_obj_t ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᎠᎪᎵᏰᏗ,mp_obj_t ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) {
    int 접속번호=mp_obj_get_int(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ᎪᏪᎵ_ᏫᏗᎦᏅᏗ={0}; ᎪᏪᎵ_ᏫᏗᎦᏅᏗ.주소갈래=인터넷주소갈래;
    ᎪᏪᎵ_ᏫᏗᎦᏅᏗ.접속번호=망차례짧은수(접속번호); ᎪᏪᎵ_ᏫᏗᎦᏅᏗ.ᎠᏏᎳᏕᏫᏒᎢ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᏧᎬᏩᎶᏗᏯ=ᏧᎾᏚᏓᎵ_integer(인터넷주소읽기(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᎠᎪᎵᏰᏗ));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,sizeof(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ᎤᏪᎬ_ᎫᏓᎸᏙᏗ_ᎪᎱᏍᏗ,ᎫᏓᎳ_ᎤᏪᎬ);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ=mp_obj_get_int(한도); if(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ<1||ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ>512)mp_raise_OSError(MP_EINVAL);
    unsigned char ᎦᏟᏌᏅᎯ[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)ᎦᏟᏌᏅᎯ,ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ,0,0,0));
    return mp_obj_new_bytes(ᎦᏟᏌᏅᎯ,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ᎤᏪᎬ_ᏗᎪᎵᏰᏍᎩ_ᎪᎱᏍᏗ,흐름읽기);
static mp_obj_t ᎪᏪᎶᏗ_ᎤᏪᎬ(mp_obj_t 종단,mp_obj_t ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ) {
    mp_buffer_info_t ᎦᏟᏌᏅᎯ; mp_get_buffer_raise(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ,&ᎦᏟᏌᏅᎯ,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)ᎦᏟᏌᏅᎯ.buf,ᎦᏟᏌᏅᎯ.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(흐름쓰기객체,ᎪᏪᎶᏗ_ᎤᏪᎬ);
static mp_obj_t 잠시기다리기(mp_obj_t 시간) {
    결과검사(사용자호출(17,mp_obj_get_int(시간),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(기다림객체,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t ᏚᏙᎥᎢ) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)ᎠᏍᏓᏩᏛᏍᏗ_ᏗᏓᎦᏘᎸᏍᏗ(ᏚᏙᎥᎢ),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t 폴더만들기(mp_obj_t ᏚᏙᎥᎢ) {
    결과검사(사용자호출(18,(uintptr_t)ᎠᏍᏓᏩᏛᏍᏗ_ᏗᏓᎦᏘᎸᏍᏗ(ᏚᏙᎥᎢ),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,폴더만들기);
static mp_obj_t ᎯᎲᎾ_ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ(mp_obj_t ᏚᏙᎥᎢ) {
    결과검사(사용자호출(18,(uintptr_t)ᎠᏍᏓᏩᏛᏍᏗ_ᏗᏓᎦᏘᎸᏍᏗ(ᏚᏙᎥᎢ),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ᎯᎲᎾ_ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ᎤᏪᎬ_ᎫᏓᎸᏙᏗ_ᎪᎱᏍᏗ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ᎤᏪᎬ_ᏗᎪᎵᏰᏍᎩ_ᎪᎱᏍᏗ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&흐름쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ᎠᏍᏆᏂᎪᏙᏗ_ᏗᎪᎵᏰᏍᎩ_ᎪᎱᏍᏗ) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&파일쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&ᏩᏥ_ᎪᎱᏍᏗ) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
