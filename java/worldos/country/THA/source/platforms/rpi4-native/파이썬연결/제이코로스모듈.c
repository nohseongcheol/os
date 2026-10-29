// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t ผลลัพธ์) { if (ผลลัพธ์ < 0) mp_raise_OSError(-ผลลัพธ์); return ผลลัพธ์; }
static const char *พาธ_อาร์กิวเมนต์(mp_obj_t ค่า) {
    size_t 개수; const char *เส้นทาง = mp_obj_str_get_data(ค่า, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!เส้นทาง[순번]) mp_raise_OSError(MP_EINVAL);
    return เส้นทาง;
}
static mp_obj_t 파일읽기(mp_obj_t ชื่อ) {
    intptr_t แฟ้ม_จุดจับ = 결과검사(사용자호출(3, (uintptr_t)พาธ_อาร์กิวเมนต์(ชื่อ), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t ขนาด = 결과검사(사용자호출(9, แฟ้ม_จุดจับ, 0, 0, 0, 0, 0));
        vstr_t ข้อมูล; vstr_init_len(&ข้อมูล, ขนาด);
        intptr_t ผลลัพธ์ = 사용자호출(2, แฟ้ม_จุดจับ, (uintptr_t)ข้อมูล.buf, ขนาด, 0, 0, 0);
        결과검사(ผลลัพธ์); ข้อมูล.len = ผลลัพธ์;
        mp_obj_t ค่า = mp_obj_new_bytes_from_vstr(&ข้อมูล);
        nlr_pop(); 사용자호출(4, แฟ้ม_จุดจับ, 0, 0, 0, 0, 0); return ค่า;
    }
    사용자호출(4, แฟ้ม_จุดจับ, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(แฟ้ม_ผู้อ่าน_วัตถุ, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t ขนาด=mp_obj_get_int(한도);
    if(ขนาด<0||ขนาด>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t ข้อมูล; vstr_init_len(&ข้อมูล,ขนาด);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)ข้อมูล.buf,ขนาด,0,0,0);
    if(개수<0) { vstr_clear(&ข้อมูล); 결과검사(개수); }
    ข้อมูล.len=개수; return mp_obj_new_bytes_from_vstr(&ข้อมูล);
}
static MP_DEFINE_CONST_FUN_OBJ_1(อุปกรณ์นําเข้าข้อมูลมาตรฐาน_ผู้อ่าน_วัตถุ, 표준입력읽기);
static mp_obj_t 파일쓰기(mp_obj_t ชื่อ, mp_obj_t เนื้อหา_ค่า) {
    const char *เส้นทาง = พาธ_อาร์กิวเมนต์(ชื่อ);
    mp_buffer_info_t ข้อมูล; mp_get_buffer_raise(เนื้อหา_ค่า, &ข้อมูล, MP_BUFFER_READ);
    if (ข้อมูล.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t แฟ้ม_จุดจับ = 결과검사(사용자호출(3, (uintptr_t)เส้นทาง, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, แฟ้ม_จุดจับ, (uintptr_t)ข้อมูล.buf, ข้อมูล.len, 0, 0, 0);
    사용자호출(4, แฟ้ม_จุดจับ, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(파일쓰기객체, 파일쓰기);
static mp_obj_t นําออก_แฟ้ม(mp_obj_t ชื่อ) { 결과검사(사용자호출(11, (uintptr_t)พาธ_อาร์กิวเมนต์(ชื่อ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, นําออก_แฟ้ม);
static mp_obj_t ระบายสี_สี่เหลี่ยมผืนผ้า(size_t 개수, const mp_obj_t *อาร์กิวเมนต์_อาร์เรย์) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(อาร์กิวเมนต์_อาร์เรย์[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(สี่เหลี่ยมผืนผ้า_วัตถุ, 5, 5, ระบายสี_สี่เหลี่ยมผืนผ้า);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t ขนาด[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, ขนาด);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t นาฬิกา_ค่า(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(นาฬิกา_วัตถุ, นาฬิกา_ค่า);
static mp_obj_t 전문열기(mp_obj_t หมายเลขพอร์ต) {
    int ข้อมูล_ตําแหน่ง = mp_obj_get_int(หมายเลขพอร์ต); if (ข้อมูล_ตําแหน่ง < 0 || ข้อมูล_ตําแหน่ง > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t แฟ้ม_จุดจับ = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ข้อมูล_ตําแหน่ง); 첫째값.sin_addr.s_addr = 0;
    intptr_t ผลลัพธ์ = 사용자호출(33, แฟ้ม_จุดจับ, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (ผลลัพธ์ < 0) { 사용자호출(4, แฟ้ม_จุดจับ, 0, 0, 0, 0, 0); 결과검사(ผลลัพธ์); }
    return mp_obj_new_int(แฟ้ม_จุดจับ);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, 전문열기);
static mp_obj_t 전문전송(mp_obj_t แฟ้ม_จุดจับ, mp_obj_t หมายเลขพอร์ต, mp_obj_t เนื้อหา_ค่า) {
    int ข้อมูล_ตําแหน่ง = mp_obj_get_int(หมายเลขพอร์ต); if (ข้อมูล_ตําแหน่ง < 1 || ข้อมูล_ตําแหน่ง > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ข้อมูล; mp_get_buffer_raise(เนื้อหา_ค่า, &ข้อมูล, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(ข้อมูล_ตําแหน่ง); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(แฟ้ม_จุดจับ), (uintptr_t)ข้อมูล.buf, ข้อมูล.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, 전문전송);
static uint32_t 인터넷주소읽기(mp_obj_t ค่า) {
    size_t 길이; const char *ข้อความ=mp_obj_str_get_data(ค่า,&길이);
    unsigned ปัจจุบัน_ตําแหน่ง=0; uint32_t อีเมล=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned ค่า=0,숫자수=0;
        while(ปัจจุบัน_ตําแหน่ง<길이&&ข้อความ[ปัจจุบัน_ตําแหน่ง]>='0'&&ข้อความ[ปัจจุบัน_ตําแหน่ง]<='9') {
            ค่า=ค่า*10+ข้อความ[ปัจจุบัน_ตําแหน่ง++]-'0'; if(++숫자수>3||ค่า>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        อีเมล=อีเมล<<8|ค่า;
        if(부분<3&&(ปัจจุบัน_ตําแหน่ง>=길이||ข้อความ[ปัจจุบัน_ตําแหน่ง++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(ปัจจุบัน_ตําแหน่ง!=길이)mp_raise_OSError(MP_EINVAL);
    return อีเมล;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *อาร์กิวเมนต์_อาร์เรย์) {
    (void)항목수; uint32_t อีเมล=인터넷주소읽기(อาร์กิวเมนต์_อาร์เรย์[1]);
    int หมายเลขพอร์ต=mp_obj_get_int(อาร์กิวเมนต์_อาร์เรย์[2]);if(หมายเลขพอร์ต<1||หมายเลขพอร์ต>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t ข้อมูล;mp_get_buffer_raise(อาร์กิวเมนต์_อาร์เรย์[3],&ข้อมูล,MP_BUFFER_READ);
    struct pk_sockaddr_in เป้าหมาย={0};เป้าหมาย.sin_family=AF_INET;เป้าหมาย.sin_port=pk_htons(หมายเลขพอร์ต);เป้าหมาย.sin_addr.s_addr=pk_htonl(อีเมล);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(อาร์กิวเมนต์_อาร์เรย์[0]),(uintptr_t)ข้อมูล.buf,ข้อมูล.len,0,(uintptr_t)&เป้าหมาย,sizeof(เป้าหมาย))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t แฟ้ม_จุดจับ) {
    unsigned char ข้อมูล[512]; struct pk_sockaddr_in ชั้น_ค่า; pk_socklen_t 길이값 = sizeof(ชั้น_ค่า);
    intptr_t ขนาด = 결과검사(사용자호출(35, mp_obj_get_int(แฟ้ม_จุดจับ), (uintptr_t)ข้อมูล, 512, 0, (uintptr_t)&ชั้น_ค่า, (uintptr_t)&길이값));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(ข้อมูล, ขนาด), MP_OBJ_NEW_SMALL_INT(pk_htons(ชั้น_ค่า.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t 전문닫기(mp_obj_t แฟ้ม_จุดจับ) { 결과검사(사용자호출(4, mp_obj_get_int(แฟ้ม_จุดจับ), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, 전문닫기);
static mp_obj_t เปิด_สตรีม(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,คลาวด์_กลุ่ม,สตรีม_เครือข่าย,สตรีม_โพรโทคอลการส่งผ่าน,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,เปิด_สตรีม);
static mp_obj_t เชื่อมต่อ_สตรีม(mp_obj_t ปลายทาง,mp_obj_t อีเมล_ข้อความ,mp_obj_t ดัชนี) {
    int หมายเลขพอร์ต=mp_obj_get_int(ดัชนี); if(หมายเลขพอร์ต<1||หมายเลขพอร์ต>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 อีเมล={0}; อีเมล.อีเมล_กลุ่ม=คลาวด์_กลุ่ม;
    อีเมล.หมายเลขพอร์ต=망차례짧은수(หมายเลขพอร์ต); อีเมล.ที่อยู่อินเทอร์เน็ต.อีเมล_ค่า=เครือข่าย_จํานวนเต็ม(인터넷주소읽기(อีเมล_ข้อความ));
    결과검사(사용자호출(37,mp_obj_get_int(ปลายทาง),(uintptr_t)&อีเมล,sizeof(อีเมล),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(สตรีม_หัวต่อ_วัตถุ,เชื่อมต่อ_สตรีม);
static mp_obj_t 흐름읽기(mp_obj_t ปลายทาง,mp_obj_t 한도) {
    int 길이=mp_obj_get_int(한도); if(길이<1||길이>512)mp_raise_OSError(MP_EINVAL);
    unsigned char ข้อมูล[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(ปลายทาง),(uintptr_t)ข้อมูล,길이,0,0,0));
    return mp_obj_new_bytes(ข้อมูล,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(สตรีม_ผู้อ่าน_วัตถุ,흐름읽기);
static mp_obj_t 흐름쓰기(mp_obj_t ปลายทาง,mp_obj_t เนื้อหา_ค่า) {
    mp_buffer_info_t ข้อมูล; mp_get_buffer_raise(เนื้อหา_ค่า,&ข้อมูล,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(ปลายทาง),(uintptr_t)ข้อมูล.buf,ข้อมูล.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(흐름쓰기객체,흐름쓰기);
static mp_obj_t 잠시기다리기(mp_obj_t ค่าเวลา) {
    결과검사(사용자호출(17,mp_obj_get_int(ค่าเวลา),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(รอเดี๋ยว_วัตถุ,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t ชื่อ) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)พาธ_อาร์กิวเมนต์(ชื่อ),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t เปิด_ไดเรกทอรี(mp_obj_t ชื่อ) {
    결과검사(사용자호출(18,(uintptr_t)พาธ_อาร์กิวเมนต์(ชื่อ),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(ไดเรกทอรี_ผู้แต่ง_วัตถุ,เปิด_ไดเรกทอรี);
static mp_obj_t นําออก_ไดเรกทอรี(mp_obj_t ชื่อ) {
    결과검사(사용자호출(18,(uintptr_t)พาธ_อาร์กิวเมนต์(ชื่อ),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,นําออก_ไดเรกทอรี);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&สตรีม_หัวต่อ_วัตถุ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&สตรีม_ผู้อ่าน_วัตถุ) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&흐름쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&รอเดี๋ยว_วัตถุ) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&ไดเรกทอรี_ผู้แต่ง_วัตถุ) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&อุปกรณ์นําเข้าข้อมูลมาตรฐาน_ผู้อ่าน_วัตถุ) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&แฟ้ม_ผู้อ่าน_วัตถุ) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&파일쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&สี่เหลี่ยมผืนผ้า_วัตถุ) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&นาฬิกา_วัตถุ) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
