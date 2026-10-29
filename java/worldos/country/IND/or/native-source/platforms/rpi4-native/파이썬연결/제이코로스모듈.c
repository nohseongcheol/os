// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t ମାପ) { if (ମାପ < 0) mp_raise_OSError(-ମାପ); return ମାପ; }
static const char *ପଥ_ଯୁକ୍ତି(mp_obj_t ମୂଲ୍ୟ) {
    size_t 개수; const char *ପଥ = mp_obj_str_get_data(ମୂଲ୍ୟ, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!ପଥ[순번]) mp_raise_OSError(MP_EINVAL);
    return ପଥ;
}
static mp_obj_t 파일읽기(mp_obj_t ନାମ) {
    intptr_t ଫାଇଲ୍_ହାଣ୍ଡେଲ୍ = 결과검사(사용자호출(3, (uintptr_t)ପଥ_ଯୁକ୍ତି(ନାମ), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t ଆକାର = 결과검사(사용자호출(9, ଫାଇଲ୍_ହାଣ୍ଡେଲ୍, 0, 0, 0, 0, 0));
        vstr_t ଡାଟା; vstr_init_len(&ଡାଟା, ଆକାର);
        intptr_t ମାପ = 사용자호출(2, ଫାଇଲ୍_ହାଣ୍ଡେଲ୍, (uintptr_t)ଡାଟା.buf, ଆକାର, 0, 0, 0);
        결과검사(ମାପ); ଡାଟା.len = ମାପ;
        mp_obj_t ମୂଲ୍ୟ = mp_obj_new_bytes_from_vstr(&ଡାଟା);
        nlr_pop(); 사용자호출(4, ଫାଇଲ୍_ହାଣ୍ଡେଲ୍, 0, 0, 0, 0, 0); return ମୂଲ୍ୟ;
    }
    사용자호출(4, ଫାଇଲ୍_ହାଣ୍ଡେଲ୍, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ଫାଇଲ୍_ପାଠକ_ଅବଜେକ୍ଟ, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t ଆକାର=mp_obj_get_int(한도);
    if(ଆକାର<0||ଆକାର>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t ଡାଟା; vstr_init_len(&ଡାଟା,ଆକାର);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)ଡାଟା.buf,ଆକାର,0,0,0);
    if(개수<0) { vstr_clear(&ଡାଟା); 결과검사(개수); }
    ଡାଟା.len=개수; return mp_obj_new_bytes_from_vstr(&ଡାଟା);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t ଲିଖନ_ଫାଇଲ୍(mp_obj_t ନାମ, mp_obj_t ବିଷୟ_ମୂଲ୍ୟ) {
    const char *ପଥ = ପଥ_ଯୁକ୍ତି(ନାମ);
    mp_buffer_info_t ଡାଟା; mp_get_buffer_raise(ବିଷୟ_ମୂଲ୍ୟ, &ଡାଟା, MP_BUFFER_READ);
    if (ଡାଟା.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ଫାଇଲ୍_ହାଣ୍ଡେଲ୍ = 결과검사(사용자호출(3, (uintptr_t)ପଥ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ଫାଇଲ୍_ହାଣ୍ଡେଲ୍, (uintptr_t)ଡାଟା.buf, ଡାଟା.len, 0, 0, 0);
    사용자호출(4, ଫାଇଲ୍_ହାଣ୍ଡେଲ୍, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ଫାଇଲ୍_ରାଇଟର୍_ଅବଜେକ୍ଟ, ଲିଖନ_ଫାଇଲ୍);
static mp_obj_t ଅପସାରଣ_କରିବା_ଫାଇଲ୍(mp_obj_t ନାମ) { 결과검사(사용자호출(11, (uintptr_t)ପଥ_ଯୁକ୍ତି(ନାମ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, ଅପସାରଣ_କରିବା_ଫାଇଲ୍);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *ଯୁକ୍ତି_ଆରେ) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(ଯୁକ୍ତି_ଆରେ[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t ଆକାର[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, ଆକାର);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t ଘଣ୍ଟା_ମୂଲ୍ୟ(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(ଘଣ୍ଟା_ଅବଜେକ୍ଟ, ଘଣ୍ଟା_ମୂଲ୍ୟ);
static mp_obj_t 전문열기(mp_obj_t ପୋର୍ଟ୍_ନମ୍ଵର୍) {
    int ଡାଟା_ସ୍ଥିତି = mp_obj_get_int(ପୋର୍ଟ୍_ନମ୍ଵର୍); if (ଡାଟା_ସ୍ଥିତି < 0 || ଡାଟା_ସ୍ଥିତି > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ଫାଇଲ୍_ହାଣ୍ଡେଲ୍ = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ଡାଟା_ସ୍ଥିତି); 첫째값.sin_addr.s_addr = 0;
    intptr_t ମାପ = 사용자호출(33, ଫାଇଲ୍_ହାଣ୍ଡେଲ୍, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (ମାପ < 0) { 사용자호출(4, ଫାଇଲ୍_ହାଣ୍ଡେଲ୍, 0, 0, 0, 0, 0); 결과검사(ମାପ); }
    return mp_obj_new_int(ଫାଇଲ୍_ହାଣ୍ଡେଲ୍);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t ଫାଇଲ୍_ହାଣ୍ଡେଲ୍, mp_obj_t ପୋର୍ଟ୍_ନମ୍ଵର୍, mp_obj_t ବିଷୟ_ମୂଲ୍ୟ) {
    int ଡାଟା_ସ୍ଥିତି = mp_obj_get_int(ପୋର୍ଟ୍_ନମ୍ଵର୍); if (ଡାଟା_ସ୍ଥିତି < 1 || ଡାଟା_ସ୍ଥିତି > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ଡାଟା; mp_get_buffer_raise(ବିଷୟ_ମୂଲ୍ୟ, &ଡାଟା, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ଡାଟା_ସ୍ଥିତି); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ଫାଇଲ୍_ହାଣ୍ଡେଲ୍), (uintptr_t)ଡାଟା.buf, ଡାଟା.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t ମୂଲ୍ୟ) {
    size_t ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ; const char *ପାଠ୍ଯ=mp_obj_str_get_data(ମୂଲ୍ୟ,&ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ);
    unsigned 현재위치=0; uint32_t ଠିକଣା=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned ମୂଲ୍ୟ=0,숫자수=0;
        while(현재위치<ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ&&ପାଠ୍ଯ[현재위치]>='0'&&ପାଠ୍ଯ[현재위치]<='9') {
            ମୂଲ୍ୟ=ମୂଲ୍ୟ*10+ପାଠ୍ଯ[현재위치++]-'0'; if(++숫자수>3||ମୂଲ୍ୟ>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        ଠିକଣା=ଠିକଣା<<8|ମୂଲ୍ୟ;
        if(부분<3&&(현재위치>=ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ||ପାଠ୍ଯ[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ)mp_raise_OSError(MP_EINVAL);
    return ଠିକଣା;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *ଯୁକ୍ତି_ଆରେ) {
    (void)항목수; uint32_t ଠିକଣା=인터넷주소읽기(ଯୁକ୍ତି_ଆରେ[1]);
    int ପୋର୍ଟ୍_ନମ୍ଵର୍=mp_obj_get_int(ଯୁକ୍ତି_ଆରେ[2]);if(ପୋର୍ଟ୍_ନମ୍ଵର୍<1||ପୋର୍ଟ୍_ନମ୍ଵର୍>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ଡାଟା;mp_get_buffer_raise(ଯୁକ୍ତି_ଆରେ[3],&ଡାଟା,MP_BUFFER_READ);
    struct pk_sockaddr_in ଲକ୍ଷ୍ୟସ୍ଥଳ={0};ଲକ୍ଷ୍ୟସ୍ଥଳ.sin_family=AF_INET;ଲକ୍ଷ୍ୟସ୍ଥଳ.sin_port=pk_htons(ପୋର୍ଟ୍_ନମ୍ଵର୍);ଲକ୍ଷ୍ୟସ୍ଥଳ.sin_addr.s_addr=pk_htonl(ଠିକଣା);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(ଯୁକ୍ତି_ଆରେ[0]),(uintptr_t)ଡାଟା.buf,ଡାଟା.len,0,(uintptr_t)&ଲକ୍ଷ୍ୟସ୍ଥଳ,sizeof(ଲକ୍ଷ୍ୟସ୍ଥଳ))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ଫାଇଲ୍_ହାଣ୍ଡେଲ୍) {
    unsigned char ଡାଟା[512]; struct pk_sockaddr_in ସମକକ୍ଷ_ମୂଲ୍ୟ; pk_socklen_t ଦୈର୍ଘ୍ୟ_ଡାଟା = sizeof(ସମକକ୍ଷ_ମୂଲ୍ୟ);
    intptr_t ଆକାର = 결과검사(사용자호출(35, mp_obj_get_int(ଫାଇଲ୍_ହାଣ୍ଡେଲ୍), (uintptr_t)ଡାଟା, 512, 0, (uintptr_t)&ସମକକ୍ଷ_ମୂଲ୍ୟ, (uintptr_t)&ଦୈର୍ଘ୍ୟ_ଡାଟା));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(ଡାଟା, ଆକାର), MP_OBJ_NEW_SMALL_INT(pk_htons(ସମକକ୍ଷ_ମୂଲ୍ୟ.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t ଫାଇଲ୍_ହାଣ୍ଡେଲ୍) { 결과검사(사용자호출(4, mp_obj_get_int(ଫାଇଲ୍_ହାଣ୍ଡେଲ୍), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t ଖୋଲିବା_ଷ୍ଟ୍ରିମ୍(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,କ୍ଲାଉଡ୍_ପରିବାର,ଷ୍ଟ୍ରିମ୍_ନେଟ୍_ୱାର୍କ୍,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ଖୋଲିବା_ଷ୍ଟ୍ରିମ୍);
static mp_obj_t ସଂଯୋଗ_ଷ୍ଟ୍ରିମ୍(mp_obj_t 종단,mp_obj_t ଠିକଣା_ପାଠ,mp_obj_t ଅନୁକ୍ରମଣିକା) {
    int ପୋର୍ଟ୍_ନମ୍ଵର୍=mp_obj_get_int(ଅନୁକ୍ରମଣିକା); if(ପୋର୍ଟ୍_ନମ୍ଵର୍<1||ପୋର୍ଟ୍_ନମ୍ଵର୍>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ଠିକଣା={0}; ଠିକଣା.ଠିକଣା_ପରିବାର=କ୍ଲାଉଡ୍_ପରିବାର;
    ଠିକଣା.ପୋର୍ଟ୍_ନମ୍ଵର୍=망차례짧은수(ପୋର୍ଟ୍_ନମ୍ଵର୍); ଠିକଣା.ଇଣ୍ଟର୍ନେଟ୍_ଠିକଣା.ଠିକଣା_ମୂଲ୍ୟ=ନେଟ୍_ୱାର୍କ୍_ଇଣ୍ଟିଜର(인터넷주소읽기(ଠିକଣା_ପାଠ));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ଠିକଣା,sizeof(ଠିକଣା),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ଷ୍ଟ୍ରିମ୍_ସଂଲଗ୍ନକ_ଅବଜେକ୍ଟ,ସଂଯୋଗ_ଷ୍ଟ୍ରିମ୍);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ=mp_obj_get_int(한도); if(ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ<1||ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ>512)mp_raise_OSError(MP_EINVAL);
    unsigned char ଡାଟା[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)ଡାଟା,ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ,0,0,0));
    return mp_obj_new_bytes(ଡାଟା,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ଷ୍ଟ୍ରିମ୍_ପାଠକ_ଅବଜେକ୍ଟ,흐름읽기);
static mp_obj_t ଲିଖନ_ଷ୍ଟ୍ରିମ୍(mp_obj_t 종단,mp_obj_t ବିଷୟ_ମୂଲ୍ୟ) {
    mp_buffer_info_t ଡାଟା; mp_get_buffer_raise(ବିଷୟ_ମୂଲ୍ୟ,&ଡାଟା,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)ଡାଟା.buf,ଡାଟା.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(ଷ୍ଟ୍ରିମ୍_ରାଇଟର୍_ଅବଜେକ୍ଟ,ଲିଖନ_ଷ୍ଟ୍ରିମ୍);
static mp_obj_t 잠시기다리기(mp_obj_t ସମୟ_ମୂଲ୍ୟ) {
    결과검사(사용자호출(17,mp_obj_get_int(ସମୟ_ମୂଲ୍ୟ),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(ଅପେକ୍ଷା_ଅବଜେକ୍ଟ,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t ନାମ) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)ପଥ_ଯୁକ୍ତି(ନାମ),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t ସୃଷ୍ଟି_ଡିରେକ୍ଟୋରୀ(mp_obj_t ନାମ) {
    결과검사(사용자호출(18,(uintptr_t)ପଥ_ଯୁକ୍ତି(ନାମ),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(ଡିରେକ୍ଟୋରୀ_କ୍ରିଏଟର୍_ଅବଜେକ୍ଟ,ସୃଷ୍ଟି_ଡିରେକ୍ଟୋରୀ);
static mp_obj_t ଅପସାରଣ_କରିବା_ଡିରେକ୍ଟୋରୀ(mp_obj_t ନାମ) {
    결과검사(사용자호출(18,(uintptr_t)ପଥ_ଯୁକ୍ତି(ନାମ),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,ଅପସାରଣ_କରିବା_ଡିରେକ୍ଟୋରୀ);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ଷ୍ଟ୍ରିମ୍_ସଂଲଗ୍ନକ_ଅବଜେକ୍ଟ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ଷ୍ଟ୍ରିମ୍_ପାଠକ_ଅବଜେକ୍ଟ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&ଷ୍ଟ୍ରିମ୍_ରାଇଟର୍_ଅବଜେକ୍ଟ) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&ଅପେକ୍ଷା_ଅବଜେକ୍ଟ) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&ଡିରେକ୍ଟୋରୀ_କ୍ରିଏଟର୍_ଅବଜେକ୍ଟ) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ଫାଇଲ୍_ପାଠକ_ଅବଜେକ୍ଟ) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&ଫାଇଲ୍_ରାଇଟର୍_ଅବଜେକ୍ଟ) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&ଘଣ୍ଟା_ଅବଜେକ୍ଟ) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
