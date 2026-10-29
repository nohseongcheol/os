// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t ಮಾಪನ) { if (ಮಾಪನ < 0) mp_raise_OSError(-ಮಾಪನ); return ಮಾಪನ; }
static const char *ಹಾದಿ_ವಾದ(mp_obj_t ಮೌಲ್ಯ) {
    size_t 개수; const char *ಮಾರ್ಗ = mp_obj_str_get_data(ಮೌಲ್ಯ, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!ಮಾರ್ಗ[순번]) mp_raise_OSError(MP_EINVAL);
    return ಮಾರ್ಗ;
}
static mp_obj_t 파일읽기(mp_obj_t ಹೆಸರು) {
    intptr_t ಫೈಲ್_ಹ್ಯಾಂಡಲ್ = 결과검사(사용자호출(3, (uintptr_t)ಹಾದಿ_ವಾದ(ಹೆಸರು), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t ಗಾತ್ರ = 결과검사(사용자호출(9, ಫೈಲ್_ಹ್ಯಾಂಡಲ್, 0, 0, 0, 0, 0));
        vstr_t ಡೇಟಾ; vstr_init_len(&ಡೇಟಾ, ಗಾತ್ರ);
        intptr_t ಮಾಪನ = 사용자호출(2, ಫೈಲ್_ಹ್ಯಾಂಡಲ್, (uintptr_t)ಡೇಟಾ.buf, ಗಾತ್ರ, 0, 0, 0);
        결과검사(ಮಾಪನ); ಡೇಟಾ.len = ಮಾಪನ;
        mp_obj_t ಮೌಲ್ಯ = mp_obj_new_bytes_from_vstr(&ಡೇಟಾ);
        nlr_pop(); 사용자호출(4, ಫೈಲ್_ಹ್ಯಾಂಡಲ್, 0, 0, 0, 0, 0); return ಮೌಲ್ಯ;
    }
    사용자호출(4, ಫೈಲ್_ಹ್ಯಾಂಡಲ್, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ಫೈಲ್_ಓದುಗ_ಆಬ್ಜೆಕ್ಟ್, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t ಗಾತ್ರ=mp_obj_get_int(한도);
    if(ಗಾತ್ರ<0||ಗಾತ್ರ>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t ಡೇಟಾ; vstr_init_len(&ಡೇಟಾ,ಗಾತ್ರ);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)ಡೇಟಾ.buf,ಗಾತ್ರ,0,0,0);
    if(개수<0) { vstr_clear(&ಡೇಟಾ); 결과검사(개수); }
    ಡೇಟಾ.len=개수; return mp_obj_new_bytes_from_vstr(&ಡೇಟಾ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t ಬರೆ_ಫೈಲ್(mp_obj_t ಹೆಸರು, mp_obj_t ವಿಷಯ_ಮೌಲ್ಯ) {
    const char *ಮಾರ್ಗ = ಹಾದಿ_ವಾದ(ಹೆಸರು);
    mp_buffer_info_t ಡೇಟಾ; mp_get_buffer_raise(ವಿಷಯ_ಮೌಲ್ಯ, &ಡೇಟಾ, MP_BUFFER_READ);
    if (ಡೇಟಾ.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ಫೈಲ್_ಹ್ಯಾಂಡಲ್ = 결과검사(사용자호출(3, (uintptr_t)ಮಾರ್ಗ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ಫೈಲ್_ಹ್ಯಾಂಡಲ್, (uintptr_t)ಡೇಟಾ.buf, ಡೇಟಾ.len, 0, 0, 0);
    사용자호출(4, ಫೈಲ್_ಹ್ಯಾಂಡಲ್, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ಫೈಲ್_ವ್ರೈಟರ್_ಆಬ್ಜೆಕ್ಟ್, ಬರೆ_ಫೈಲ್);
static mp_obj_t ತೆಗೆ_ಫೈಲ್(mp_obj_t ಹೆಸರು) { 결과검사(사용자호출(11, (uintptr_t)ಹಾದಿ_ವಾದ(ಹೆಸರು), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ತೆಗೆ_ಫೈಲ್);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *ವಾದ_ಅರೇ) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(ವಾದ_ಅರೇ[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t ಗಾತ್ರ[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, ಗಾತ್ರ);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t ಗಡಿಯಾರ_ಮೌಲ್ಯ(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(ಗಡಿಯಾರ_ಆಬ್ಜೆಕ್ಟ್, ಗಡಿಯಾರ_ಮೌಲ್ಯ);
static mp_obj_t 전문열기(mp_obj_t ಪೋರ್ಟ್_ಸಂಖ್ಯೆ) {
    int ಡೇಟಾ_ಹುದ್ದೆ = mp_obj_get_int(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ); if (ಡೇಟಾ_ಹುದ್ದೆ < 0 || ಡೇಟಾ_ಹುದ್ದೆ > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ಫೈಲ್_ಹ್ಯಾಂಡಲ್ = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ಡೇಟಾ_ಹುದ್ದೆ); 첫째값.sin_addr.s_addr = 0;
    intptr_t ಮಾಪನ = 사용자호출(33, ಫೈಲ್_ಹ್ಯಾಂಡಲ್, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (ಮಾಪನ < 0) { 사용자호출(4, ಫೈಲ್_ಹ್ಯಾಂಡಲ್, 0, 0, 0, 0, 0); 결과검사(ಮಾಪನ); }
    return mp_obj_new_int(ಫೈಲ್_ಹ್ಯಾಂಡಲ್);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ಫೈಲ್_ಹ್ಯಾಂಡಲ್, mp_obj_t ಪೋರ್ಟ್_ಸಂಖ್ಯೆ, mp_obj_t ವಿಷಯ_ಮೌಲ್ಯ) {
    int ಡೇಟಾ_ಹುದ್ದೆ = mp_obj_get_int(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ); if (ಡೇಟಾ_ಹುದ್ದೆ < 1 || ಡೇಟಾ_ಹುದ್ದೆ > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ಡೇಟಾ; mp_get_buffer_raise(ವಿಷಯ_ಮೌಲ್ಯ, &ಡೇಟಾ, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ಡೇಟಾ_ಹುದ್ದೆ); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ಫೈಲ್_ಹ್ಯಾಂಡಲ್), (uintptr_t)ಡೇಟಾ.buf, ಡೇಟಾ.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t ಮೌಲ್ಯ) {
    size_t ಉದ್ದ_ಮೌಲ್ಯ; const char *ಪಠ್ಯ=mp_obj_str_get_data(ಮೌಲ್ಯ,&ಉದ್ದ_ಮೌಲ್ಯ);
    unsigned 현재위치=0; uint32_t ಇಮೇಲ್=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned ಮೌಲ್ಯ=0,숫자수=0;
        while(현재위치<ಉದ್ದ_ಮೌಲ್ಯ&&ಪಠ್ಯ[현재위치]>='0'&&ಪಠ್ಯ[현재위치]<='9') {
            ಮೌಲ್ಯ=ಮೌಲ್ಯ*10+ಪಠ್ಯ[현재위치++]-'0'; if(++숫자수>3||ಮೌಲ್ಯ>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        ಇಮೇಲ್=ಇಮೇಲ್<<8|ಮೌಲ್ಯ;
        if(부분<3&&(현재위치>=ಉದ್ದ_ಮೌಲ್ಯ||ಪಠ್ಯ[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=ಉದ್ದ_ಮೌಲ್ಯ)mp_raise_OSError(MP_EINVAL);
    return ಇಮೇಲ್;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *ವಾದ_ಅರೇ) {
    (void)항목수; uint32_t ಇಮೇಲ್=인터넷주소읽기(ವಾದ_ಅರೇ[1]);
    int ಪೋರ್ಟ್_ಸಂಖ್ಯೆ=mp_obj_get_int(ವಾದ_ಅರೇ[2]);if(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ<1||ಪೋರ್ಟ್_ಸಂಖ್ಯೆ>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ಡೇಟಾ;mp_get_buffer_raise(ವಾದ_ಅರೇ[3],&ಡೇಟಾ,MP_BUFFER_READ);
    struct pk_sockaddr_in ಲಕ್ಷ್ಯ={0};ಲಕ್ಷ್ಯ.sin_family=AF_INET;ಲಕ್ಷ್ಯ.sin_port=pk_htons(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ);ಲಕ್ಷ್ಯ.sin_addr.s_addr=pk_htonl(ಇಮೇಲ್);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(ವಾದ_ಅರೇ[0]),(uintptr_t)ಡೇಟಾ.buf,ಡೇಟಾ.len,0,(uintptr_t)&ಲಕ್ಷ್ಯ,sizeof(ಲಕ್ಷ್ಯ))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ಫೈಲ್_ಹ್ಯಾಂಡಲ್) {
    unsigned char ಡೇಟಾ[512]; struct pk_sockaddr_in ಪೀರ್_ಮೌಲ್ಯ; pk_socklen_t ಉದ್ದ_ಡೇಟಾ = sizeof(ಪೀರ್_ಮೌಲ್ಯ);
    intptr_t ಗಾತ್ರ = 결과검사(사용자호출(35, mp_obj_get_int(ಫೈಲ್_ಹ್ಯಾಂಡಲ್), (uintptr_t)ಡೇಟಾ, 512, 0, (uintptr_t)&ಪೀರ್_ಮೌಲ್ಯ, (uintptr_t)&ಉದ್ದ_ಡೇಟಾ));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(ಡೇಟಾ, ಗಾತ್ರ), MP_OBJ_NEW_SMALL_INT(pk_htons(ಪೀರ್_ಮೌಲ್ಯ.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ಫೈಲ್_ಹ್ಯಾಂಡಲ್) { 결과검사(사용자호출(4, mp_obj_get_int(ಫೈಲ್_ಹ್ಯಾಂಡಲ್), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t ರಚಿಸು_ಸ್ಟ್ರೀಮ್(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,ಕ್ಲೌಡ್_ಕುಟುಂಬ,ಸ್ಟ್ರೀಮ್_ನೆಟ್_ವರ್ಕ್,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ರಚಿಸು_ಸ್ಟ್ರೀಮ್);
static mp_obj_t ಕನೆಕ್ಟ್_ಸ್ಟ್ರೀಮ್(mp_obj_t 종단,mp_obj_t ಇಮೇಲ್_ಪಠ್ಯ,mp_obj_t ಪದಸೂಚಿ) {
    int ಪೋರ್ಟ್_ಸಂಖ್ಯೆ=mp_obj_get_int(ಪದಸೂಚಿ); if(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ<1||ಪೋರ್ಟ್_ಸಂಖ್ಯೆ>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ಇಮೇಲ್={0}; ಇಮೇಲ್.ಇಮೇಲ್_ಕುಟುಂಬ=ಕ್ಲೌಡ್_ಕುಟುಂಬ;
    ಇಮೇಲ್.ಪೋರ್ಟ್_ಸಂಖ್ಯೆ=망차례짧은수(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ); ಇಮೇಲ್.ಇಂಟರ್ನೆಟ್_ವಿಳಾಸ.ಇಮೇಲ್_ಮೌಲ್ಯ=ನೆಟ್_ವರ್ಕ್_ಪೂರ್ಣಸಂಖ್ಯೆ(인터넷주소읽기(ಇಮೇಲ್_ಪಠ್ಯ));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ಇಮೇಲ್,sizeof(ಇಮೇಲ್),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ಸ್ಟ್ರೀಮ್_ಜೋಡಿಸುವವ_ಆಬ್ಜೆಕ್ಟ್,ಕನೆಕ್ಟ್_ಸ್ಟ್ರೀಮ್);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int ಉದ್ದ_ಮೌಲ್ಯ=mp_obj_get_int(한도); if(ಉದ್ದ_ಮೌಲ್ಯ<1||ಉದ್ದ_ಮೌಲ್ಯ>512)mp_raise_OSError(MP_EINVAL);
    unsigned char ಡೇಟಾ[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)ಡೇಟಾ,ಉದ್ದ_ಮೌಲ್ಯ,0,0,0));
    return mp_obj_new_bytes(ಡೇಟಾ,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ಸ್ಟ್ರೀಮ್_ಓದುಗ_ಆಬ್ಜೆಕ್ಟ್,흐름읽기);
static mp_obj_t ಬರೆ_ಸ್ಟ್ರೀಮ್(mp_obj_t 종단,mp_obj_t ವಿಷಯ_ಮೌಲ್ಯ) {
    mp_buffer_info_t ಡೇಟಾ; mp_get_buffer_raise(ವಿಷಯ_ಮೌಲ್ಯ,&ಡೇಟಾ,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)ಡೇಟಾ.buf,ಡೇಟಾ.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ಸ್ಟ್ರೀಮ್_ವ್ರೈಟರ್_ಆಬ್ಜೆಕ್ಟ್,ಬರೆ_ಸ್ಟ್ರೀಮ್);
static mp_obj_t 잠시기다리기(mp_obj_t ಸಮಯ_ಮೌಲ್ಯ) {
    결과검사(사용자호출(17,mp_obj_get_int(ಸಮಯ_ಮೌಲ್ಯ),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(ನಿರೀಕ್ಷಣೆ_ಆಬ್ಜೆಕ್ಟ್,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t ಹೆಸರು) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)ಹಾದಿ_ವಾದ(ಹೆಸರು),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t ರಚಿಸು_ಡೈರೆಕ್ಟರಿ(mp_obj_t ಹೆಸರು) {
    결과검사(사용자호출(18,(uintptr_t)ಹಾದಿ_ವಾದ(ಹೆಸರು),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(ಡೈರೆಕ್ಟರಿ_ರಚನೆಕಾರರು_ಆಬ್ಜೆಕ್ಟ್,ರಚಿಸು_ಡೈರೆಕ್ಟರಿ);
static mp_obj_t ತೆಗೆ_ಡೈರೆಕ್ಟರಿ(mp_obj_t ಹೆಸರು) {
    결과검사(사용자호출(18,(uintptr_t)ಹಾದಿ_ವಾದ(ಹೆಸರು),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ತೆಗೆ_ಡೈರೆಕ್ಟರಿ);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ಸ್ಟ್ರೀಮ್_ಜೋಡಿಸುವವ_ಆಬ್ಜೆಕ್ಟ್) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ಸ್ಟ್ರೀಮ್_ಓದುಗ_ಆಬ್ಜೆಕ್ಟ್) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&ಸ್ಟ್ರೀಮ್_ವ್ರೈಟರ್_ಆಬ್ಜೆಕ್ಟ್) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&ನಿರೀಕ್ಷಣೆ_ಆಬ್ಜೆಕ್ಟ್) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&ಡೈರೆಕ್ಟರಿ_ರಚನೆಕಾರರು_ಆಬ್ಜೆಕ್ಟ್) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ಫೈಲ್_ಓದುಗ_ಆಬ್ಜೆಕ್ಟ್) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ಫೈಲ್_ವ್ರೈಟರ್_ಆಬ್ಜೆಕ್ಟ್) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&ಗಡಿಯಾರ_ಆಬ್ಜೆಕ್ಟ್) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
