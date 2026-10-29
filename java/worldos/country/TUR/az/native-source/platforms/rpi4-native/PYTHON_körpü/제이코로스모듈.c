// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t ölçü) { if (ölçü < 0) mp_raise_OSError(-ölçü); return ölçü; }
static const char *yol_arqument(mp_obj_t VALUE) {
    size_t element_COUNT; const char *Cığır = mp_obj_str_get_data(VALUE, &element_COUNT);
    if (!element_COUNT || element_COUNT > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < element_COUNT; 순번++) if (!Cığır[순번]) mp_raise_OSError(MP_EINVAL);
    return Cığır;
}
static mp_obj_t 파일읽기(mp_obj_t Ad) {
    intptr_t fayl_tutacaq = 결과검사(사용자호출(3, (uintptr_t)yol_arqument(Ad), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Böyüklük = 결과검사(사용자호출(9, fayl_tutacaq, 0, 0, 0, 0, 0));
        vstr_t verilənlər; vstr_init_len(&verilənlər, Böyüklük);
        intptr_t ölçü = 사용자호출(2, fayl_tutacaq, (uintptr_t)verilənlər.buf, Böyüklük, 0, 0, 0);
        결과검사(ölçü); verilənlər.len = ölçü;
        mp_obj_t VALUE = mp_obj_new_bytes_from_vstr(&verilənlər);
        nlr_pop(); 사용자호출(4, fayl_tutacaq, 0, 0, 0, 0, 0); return VALUE;
    }
    사용자호출(4, fayl_tutacaq, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(fayl_oxucu_obyekt, 파일읽기);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t Böyüklük=mp_obj_get_int(한도);
    if(Böyüklük<0||Böyüklük>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t verilənlər; vstr_init_len(&verilənlər,Böyüklük);
    intptr_t element_COUNT=사용자호출(2,0,(uintptr_t)verilənlər.buf,Böyüklük,0,0,0);
    if(element_COUNT<0) { vstr_clear(&verilənlər); 결과검사(element_COUNT); }
    verilənlər.len=element_COUNT; return mp_obj_new_bytes_from_vstr(&verilənlər);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t yazmaq_fayl(mp_obj_t Ad, mp_obj_t Məzmun_VALUE) {
    const char *Cığır = yol_arqument(Ad);
    mp_buffer_info_t verilənlər; mp_get_buffer_raise(Məzmun_VALUE, &verilənlər, MP_BUFFER_READ);
    if (verilənlər.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t fayl_tutacaq = 결과검사(사용자호출(3, (uintptr_t)Cığır, 577, 0, 0, 0, 0));
    intptr_t daxiletmə_COUNT = 사용자호출(1, fayl_tutacaq, (uintptr_t)verilənlər.buf, verilənlər.len, 0, 0, 0);
    사용자호출(4, fayl_tutacaq, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(daxiletmə_COUNT));
}
static MP_DEFINE_CONST_FUN_OBJ_2(fayl_Yazıçı_obyekt, yazmaq_fayl);
static mp_obj_t silmək_fayl(mp_obj_t Ad) { 결과검사(사용자호출(11, (uintptr_t)yol_arqument(Ad), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, silmək_fayl);
static mp_obj_t 사각형그리기(size_t element_COUNT, const mp_obj_t *arqument_ARRAY) {
    (void)element_COUNT; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(arqument_ARRAY[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(사각형객체, 5, 5, 사각형그리기);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t Böyüklük[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, Böyüklük);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t Saat_VALUE(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Saat_obyekt, Saat_VALUE);
static mp_obj_t UDP_açmaq(mp_obj_t 접속번호) {
    int verilənlər_yerinə_qoymaq = mp_obj_get_int(접속번호); if (verilənlər_yerinə_qoymaq < 0 || verilənlər_yerinə_qoymaq > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t fayl_tutacaq = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(verilənlər_yerinə_qoymaq); 첫째값.sin_addr.s_addr = 0;
    intptr_t ölçü = 사용자호출(33, fayl_tutacaq, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (ölçü < 0) { 사용자호출(4, fayl_tutacaq, 0, 0, 0, 0, 0); 결과검사(ölçü); }
    return mp_obj_new_int(fayl_tutacaq);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_açmaq_OBJ, UDP_açmaq);
static mp_obj_t UDP_göndərmək(mp_obj_t fayl_tutacaq, mp_obj_t 접속번호, mp_obj_t Məzmun_VALUE) {
    int verilənlər_yerinə_qoymaq = mp_obj_get_int(접속번호); if (verilənlər_yerinə_qoymaq < 1 || verilənlər_yerinə_qoymaq > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t verilənlər; mp_get_buffer_raise(Məzmun_VALUE, &verilənlər, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(verilənlər_yerinə_qoymaq); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(fayl_tutacaq), (uintptr_t)verilənlər.buf, verilənlər.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_göndərmək_OBJ, UDP_göndərmək);
static uint32_t 인터넷주소읽기(mp_obj_t VALUE) {
    size_t uzunluq_VALUE; const char *Mətn=mp_obj_str_get_data(VALUE,&uzunluq_VALUE);
    unsigned 현재위치=0; uint32_t ünvan=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALUE=0,rəqəm_COUNT=0;
        while(현재위치<uzunluq_VALUE&&Mətn[현재위치]>='0'&&Mətn[현재위치]<='9') {
            VALUE=VALUE*10+Mətn[현재위치++]-'0'; if(++rəqəm_COUNT>3||VALUE>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!rəqəm_COUNT)mp_raise_OSError(MP_EINVAL);
        ünvan=ünvan<<8|VALUE;
        if(부분<3&&(현재위치>=uzunluq_VALUE||Mətn[현재위치++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(현재위치!=uzunluq_VALUE)mp_raise_OSError(MP_EINVAL);
    return ünvan;
}
static mp_obj_t 전문주소전송(size_t daxiletmə_COUNT, const mp_obj_t *arqument_ARRAY) {
    (void)daxiletmə_COUNT; uint32_t ünvan=인터넷주소읽기(arqument_ARRAY[1]);
    int 접속번호=mp_obj_get_int(arqument_ARRAY[2]);if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t verilənlər;mp_get_buffer_raise(arqument_ARRAY[3],&verilənlər,MP_BUFFER_READ);
    struct pk_sockaddr_in hədəf={0};hədəf.sin_family=AF_INET;hədəf.sin_port=pk_htons(접속번호);hədəf.sin_addr.s_addr=pk_htonl(ünvan);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(arqument_ARRAY[0]),(uintptr_t)verilənlər.buf,verilənlər.len,0,(uintptr_t)&hədəf,sizeof(hədəf))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t fayl_tutacaq) {
    unsigned char verilənlər[512]; struct pk_sockaddr_in eynisəviyyəli_VALUE; pk_socklen_t uzunluq_verilənlər = sizeof(eynisəviyyəli_VALUE);
    intptr_t Böyüklük = 결과검사(사용자호출(35, mp_obj_get_int(fayl_tutacaq), (uintptr_t)verilənlər, 512, 0, (uintptr_t)&eynisəviyyəli_VALUE, (uintptr_t)&uzunluq_verilənlər));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(verilənlər, Böyüklük), MP_OBJ_NEW_SMALL_INT(pk_htons(eynisəviyyəli_VALUE.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_bağlamaq(mp_obj_t fayl_tutacaq) { 결과검사(사용자호출(4, mp_obj_get_int(fayl_tutacaq), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_bağlamaq_OBJ, UDP_bağlamaq);
static mp_obj_t açmaq_axın(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,bulud_Ailə,axın_Şəbəkə,흐름전송규약,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,açmaq_axın);
static mp_obj_t QOŞUN_axın(mp_obj_t 종단,mp_obj_t ünvan_SMS,mp_obj_t INDEX) {
    int 접속번호=mp_obj_get_int(INDEX); if(접속번호<1||접속번호>65535)mp_raise_OSError(MP_EINVAL);
    struct 인터넷통신주소 ünvan={0}; ünvan.ünvan_Ailə=bulud_Ailə;
    ünvan.접속번호=망차례짧은수(접속번호); ünvan.İnternet_ünvanı.ünvan_VALUE=Şəbəkə_tam_ədəd(인터넷주소읽기(ünvan_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(종단),(uintptr_t)&ünvan,sizeof(ünvan),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(axın_Birləşdirici_obyekt,QOŞUN_axın);
static mp_obj_t 흐름읽기(mp_obj_t 종단,mp_obj_t 한도) {
    int uzunluq_VALUE=mp_obj_get_int(한도); if(uzunluq_VALUE<1||uzunluq_VALUE>512)mp_raise_OSError(MP_EINVAL);
    unsigned char verilənlər[512];
    intptr_t element_COUNT=결과검사(사용자호출(2,mp_obj_get_int(종단),(uintptr_t)verilənlər,uzunluq_VALUE,0,0,0));
    return mp_obj_new_bytes(verilənlər,element_COUNT);
}
static MP_DEFINE_CONST_FUN_OBJ_2(axın_oxucu_obyekt,흐름읽기);
static mp_obj_t yazmaq_axın(mp_obj_t 종단,mp_obj_t Məzmun_VALUE) {
    mp_buffer_info_t verilənlər; mp_get_buffer_raise(Məzmun_VALUE,&verilənlər,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(종단),(uintptr_t)verilənlər.buf,verilənlər.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(axın_Yazıçı_obyekt,yazmaq_axın);
static mp_obj_t 잠시기다리기(mp_obj_t TIME_VALUE) {
    결과검사(사용자호출(17,mp_obj_get_int(TIME_VALUE),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(gözlə_obyekt,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t Ad) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)yol_arqument(Ad),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t yarat_kataloq(mp_obj_t Ad) {
    결과검사(사용자호출(18,(uintptr_t)yol_arqument(Ad),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더만들기객체,yarat_kataloq);
static mp_obj_t silmək_kataloq(mp_obj_t Ad) {
    결과검사(사용자호출(18,(uintptr_t)yol_arqument(Ad),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,silmək_kataloq);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&axın_Birləşdirici_obyekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&axın_oxucu_obyekt) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&axın_Yazıçı_obyekt) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&gözlə_obyekt) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&폴더만들기객체) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&fayl_oxucu_obyekt) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&fayl_Yazıçı_obyekt) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&사각형객체) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Saat_obyekt) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_açmaq_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_göndərmək_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_bağlamaq_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
