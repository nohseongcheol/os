// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t ມາດຕະການ) { if (ມາດຕະການ < 0) mp_raise_OSError(-ມາດຕະການ); return ມາດຕະການ; }
static const char *ທາງໂຄຈອນ_ຂໍ້ພິສູດ(mp_obj_t ຄ່າ) {
    size_t 개수; const char *ທາງໂຄຈອນ = mp_obj_str_get_data(ຄ່າ, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!ທາງໂຄຈອນ[순번]) mp_raise_OSError(MP_EINVAL);
    return ທາງໂຄຈອນ;
}
static mp_obj_t 파일읽기(mp_obj_t ຊື່) {
    intptr_t ຟາຍ_ຈັດ_ການ = 결과검사(사용자호출(3, (uintptr_t)ທາງໂຄຈອນ_ຂໍ້ພິສູດ(ຊື່), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t ຂະ_ຫນາດ = 결과검사(사용자호출(9, ຟາຍ_ຈັດ_ການ, 0, 0, 0, 0, 0));
        vstr_t ຂໍ້ມູນ; vstr_init_len(&ຂໍ້ມູນ, ຂະ_ຫນາດ);
        intptr_t ມາດຕະການ = 사용자호출(2, ຟາຍ_ຈັດ_ການ, (uintptr_t)ຂໍ້ມູນ.buf, ຂະ_ຫນາດ, 0, 0, 0);
        결과검사(ມາດຕະການ); ຂໍ້ມູນ.len = ມາດຕະການ;
        mp_obj_t ຄ່າ = mp_obj_new_bytes_from_vstr(&ຂໍ້ມູນ);
        nlr_pop(); 사용자호출(4, ຟາຍ_ຈັດ_ການ, 0, 0, 0, 0, 0); return ຄ່າ;
    }
    사용자호출(4, ຟາຍ_ຈັດ_ການ, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ຟາຍ_ຜູ້ອ່ານ_ວັດ_ຖຸ, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t ຂະ_ຫນາດ=mp_obj_get_int(한도);
    if(ຂະ_ຫນາດ<0||ຂະ_ຫນາດ>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t ຂໍ້ມູນ; vstr_init_len(&ຂໍ້ມູນ,ຂະ_ຫນາດ);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)ຂໍ້ມູນ.buf,ຂະ_ຫນາດ,0,0,0);
    if(개수<0) { vstr_clear(&ຂໍ້ມູນ); 결과검사(개수); }
    ຂໍ້ມູນ.len=개수; return mp_obj_new_bytes_from_vstr(&ຂໍ້ມູນ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t ຂຽນ_ຟາຍ(mp_obj_t ຊື່, mp_obj_t ເນື້ອໃນ_ຄ່າ_cb0f2404) {
    const char *ທາງໂຄຈອນ = ທາງໂຄຈອນ_ຂໍ້ພິສູດ(ຊື່);
    mp_buffer_info_t ຂໍ້ມູນ; mp_get_buffer_raise(ເນື້ອໃນ_ຄ່າ_cb0f2404, &ຂໍ້ມູນ, MP_BUFFER_READ);
    if (ຂໍ້ມູນ.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ຟາຍ_ຈັດ_ການ = 결과검사(사용자호출(3, (uintptr_t)ທາງໂຄຈອນ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ຟາຍ_ຈັດ_ການ, (uintptr_t)ຂໍ້ມູນ.buf, ຂໍ້ມູນ.len, 0, 0, 0);
    사용자호출(4, ຟາຍ_ຈັດ_ການ, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(파일쓰기객체, ຂຽນ_ຟາຍ);
static mp_obj_t 파일지우기(mp_obj_t ຊື່) { 결과검사(사용자호출(11, (uintptr_t)ທາງໂຄຈອນ_ຂໍ້ພິສູດ(ຊື່), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, 파일지우기);
static mp_obj_t 사각형그리기(size_t 개수, const mp_obj_t *ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t ຂະ_ຫນາດ[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, ຂະ_ຫນາດ);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t ໂມງ_ຄ່າ(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(ໂມງ_ວັດ_ຖຸ, ໂມງ_ຄ່າ);
static mp_obj_t ຢູດີພີ_ສ້າງ(mp_obj_t ຫມາຍເລກພອດ) {
    int ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ = mp_obj_get_int(ຫມາຍເລກພອດ); if (ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ < 0 || ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ຟາຍ_ຈັດ_ການ = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ); 첫째값.sin_addr.s_addr = 0;
    intptr_t ມາດຕະການ = 사용자호출(33, ຟາຍ_ຈັດ_ການ, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (ມາດຕະການ < 0) { 사용자호출(4, ຟາຍ_ຈັດ_ການ, 0, 0, 0, 0, 0); 결과검사(ມາດຕະການ); }
    return mp_obj_new_int(ຟາຍ_ຈັດ_ການ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, ຢູດີພີ_ສ້າງ);
static mp_obj_t ຢູດີພີ_ສົ່ງ(mp_obj_t ຟາຍ_ຈັດ_ການ, mp_obj_t ຫມາຍເລກພອດ, mp_obj_t ເນື້ອໃນ_ຄ່າ_cb0f2404) {
    int ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ = mp_obj_get_int(ຫມາຍເລກພອດ); if (ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ < 1 || ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ຂໍ້ມູນ; mp_get_buffer_raise(ເນື້ອໃນ_ຄ່າ_cb0f2404, &ຂໍ້ມູນ, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ຟາຍ_ຈັດ_ການ), (uintptr_t)ຂໍ້ມູນ.buf, ຂໍ້ມູນ.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, ຢູດີພີ_ສົ່ງ);
static uint32_t 인터넷주소읽기(mp_obj_t ຄ່າ) {
    size_t ຄວາມຍາວ_ຄ່າ; const char *ຂໍ້ຄວາມ=mp_obj_str_get_data(ຄ່າ,&ຄວາມຍາວ_ຄ່າ);
    unsigned 현재위치=0; uint32_t ອີເມວ=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned ຄ່າ=0,숫자수=0;
        while(현재위치<ຄວາມຍາວ_ຄ່າ&&ຂໍ້ຄວາມ[현재위치]>='0'&&ຂໍ້ຄວາມ[현재위치]<='9') {
            ຄ່າ=ຄ່າ*10+ຂໍ້ຄວາມ[현재위치++]-'0'; if(++숫자수>3||ຄ່າ>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        ອີເມວ=ອີເມວ<<8|ຄ່າ;
        if(부분<3&&(현재위치>=ຄວາມຍາວ_ຄ່າ||ຂໍ້ຄວາມ[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=ຄວາມຍາວ_ຄ່າ)mp_raise_OSError(MP_EINVAL);
    return ອີເມວ;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ) {
    (void)항목수; uint32_t ອີເມວ=인터넷주소읽기(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ[1]);
    int ຫມາຍເລກພອດ=mp_obj_get_int(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ[2]);if(ຫມາຍເລກພອດ<1||ຫມາຍເລກພອດ>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ຂໍ້ມູນ;mp_get_buffer_raise(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ[3],&ຂໍ້ມູນ,MP_BUFFER_READ);
    struct pk_sockaddr_in ເປົ້າ_ຫມາຍ={0};ເປົ້າ_ຫມາຍ.sin_family=AF_INET;ເປົ້າ_ຫມາຍ.sin_port=pk_htons(ຫມາຍເລກພອດ);ເປົ້າ_ຫມາຍ.sin_addr.s_addr=pk_htonl(ອີເມວ);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ[0]),(uintptr_t)ຂໍ້ມູນ.buf,ຂໍ້ມູນ.len,0,(uintptr_t)&ເປົ້າ_ຫມາຍ,sizeof(ເປົ້າ_ຫມາຍ))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ຟາຍ_ຈັດ_ການ) {
    unsigned char ຂໍ້ມູນ[512]; struct pk_sockaddr_in ລຸ້ນດຽວກັນ_ຄ່າ; pk_socklen_t ຄວາມຍາວ_ຂໍ້ມູນ = sizeof(ລຸ້ນດຽວກັນ_ຄ່າ);
    intptr_t ຂະ_ຫນາດ = 결과검사(사용자호출(35, mp_obj_get_int(ຟາຍ_ຈັດ_ການ), (uintptr_t)ຂໍ້ມູນ, 512, 0, (uintptr_t)&ລຸ້ນດຽວກັນ_ຄ່າ, (uintptr_t)&ຄວາມຍາວ_ຂໍ້ມູນ));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(ຂໍ້ມູນ, ຂະ_ຫນາດ), MP_OBJ_NEW_SMALL_INT(pk_htons(ລຸ້ນດຽວກັນ_ຄ່າ.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t ຢູດີພີ_ປິດ(mp_obj_t ຟາຍ_ຈັດ_ການ) { 결과검사(사용자호출(4, mp_obj_get_int(ຟາຍ_ຈັດ_ການ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, ຢູດີພີ_ປິດ);
static mp_obj_t ສ້າງ_ສະຕຣີມ(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,ຄລາວ_ຄອບຄົວ,ສະຕຣີມ_ເຄືອຂ່າຍ,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,ສ້າງ_ສະຕຣີມ);
static mp_obj_t ເຊື່ອມຕໍ່_ສະຕຣີມ(mp_obj_t 종단,mp_obj_t ອີເມວ_ຂໍ້ຄວາມ,mp_obj_t ດັດຊະນີ) {
    int ຫມາຍເລກພອດ=mp_obj_get_int(ດັດຊະນີ); if(ຫມາຍເລກພອດ<1||ຫມາຍເລກພອດ>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ອີເມວ={0}; ອີເມວ.ອີເມວ_ຄອບຄົວ=ຄລາວ_ຄອບຄົວ;
    ອີເມວ.ຫມາຍເລກພອດ=망차례짧은수(ຫມາຍເລກພອດ); ອີເມວ.ທີ່ຢູ່ອິນເຕີເນັດ.ອີເມວ_ຄ່າ=ເຄືອຂ່າຍ_ຕົວເລກຈໍານວນເຕັມ(인터넷주소읽기(ອີເມວ_ຂໍ້ຄວາມ));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ອີເມວ,sizeof(ອີເມວ),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ສະຕຣີມ_ຕົວ_ເຊື່ອມ_ຕໍ່_ວັດ_ຖຸ,ເຊື່ອມຕໍ່_ສະຕຣີມ);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int ຄວາມຍາວ_ຄ່າ=mp_obj_get_int(한도); if(ຄວາມຍາວ_ຄ່າ<1||ຄວາມຍາວ_ຄ່າ>512)mp_raise_OSError(MP_EINVAL);
    unsigned char ຂໍ້ມູນ[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)ຂໍ້ມູນ,ຄວາມຍາວ_ຄ່າ,0,0,0));
    return mp_obj_new_bytes(ຂໍ້ມູນ,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(ສະຕຣີມ_ຜູ້ອ່ານ_ວັດ_ຖຸ,흐름읽기);
static mp_obj_t ຂຽນ_ສະຕຣີມ(mp_obj_t 종단,mp_obj_t ເນື້ອໃນ_ຄ່າ_cb0f2404) {
    mp_buffer_info_t ຂໍ້ມູນ; mp_get_buffer_raise(ເນື້ອໃນ_ຄ່າ_cb0f2404,&ຂໍ້ມູນ,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)ຂໍ້ມູນ.buf,ຂໍ້ມູນ.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(흐름쓰기객체,ຂຽນ_ສະຕຣີມ);
static mp_obj_t 잠시기다리기(mp_obj_t ເວລາ_ຄ່າ) {
    결과검사(사용자호출(17,mp_obj_get_int(ເວລາ_ຄ່າ),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(ລໍຖ້າ_ວັດ_ຖຸ,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t ຊື່) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)ທາງໂຄຈອນ_ຂໍ້ພິສູດ(ຊື່),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t ສ້າງ_ກຸ່ມຂໍ້ມູນ(mp_obj_t ຊື່) {
    결과검사(사용자호출(18,(uintptr_t)ທາງໂຄຈອນ_ຂໍ້ພິສູດ(ຊື່),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(ກຸ່ມຂໍ້ມູນ_ຜູ້ສ້າງ_ວັດ_ຖຸ,ສ້າງ_ກຸ່ມຂໍ້ມູນ);
static mp_obj_t 폴더지우기(mp_obj_t ຊື່) {
    결과검사(사용자호출(18,(uintptr_t)ທາງໂຄຈອນ_ຂໍ້ພິສູດ(ຊື່),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,폴더지우기);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&ສະຕຣີມ_ຕົວ_ເຊື່ອມ_ຕໍ່_ວັດ_ຖຸ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&ສະຕຣີມ_ຜູ້ອ່ານ_ວັດ_ຖຸ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&흐름쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&ລໍຖ້າ_ວັດ_ຖຸ) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&ກຸ່ມຂໍ້ມູນ_ຜູ້ສ້າງ_ວັດ_ຖຸ) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ຟາຍ_ຜູ້ອ່ານ_ວັດ_ຖຸ) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&파일쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&ໂມງ_ວັດ_ຖຸ) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
