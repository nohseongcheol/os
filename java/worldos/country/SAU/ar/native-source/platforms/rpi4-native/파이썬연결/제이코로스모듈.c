// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t نتيجة) { if (نتيجة < 0) mp_raise_OSError(-نتيجة); return نتيجة; }
static const char *مسار_وسيطة(mp_obj_t قيمة) {
    size_t 개수; const char *مسار = mp_obj_str_get_data(قيمة, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!مسار[순번]) mp_raise_OSError(MP_EINVAL);
    return مسار;
}
static mp_obj_t يقرأ_ملف(mp_obj_t اسم) {
    intptr_t ملف_مؤشر = 결과검사(사용자호출(3, (uintptr_t)مسار_وسيطة(اسم), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t حجم = 결과검사(사용자호출(9, ملف_مؤشر, 0, 0, 0, 0, 0));
        vstr_t بيانات; vstr_init_len(&بيانات, حجم);
        intptr_t نتيجة = 사용자호출(2, ملف_مؤشر, (uintptr_t)بيانات.buf, حجم, 0, 0, 0);
        결과검사(نتيجة); بيانات.len = نتيجة;
        mp_obj_t قيمة = mp_obj_new_bytes_from_vstr(&بيانات);
        nlr_pop(); 사용자호출(4, ملف_مؤشر, 0, 0, 0, 0, 0); return قيمة;
    }
    사용자호출(4, ملف_مؤشر, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ملف_قارئ_عنصر, يقرأ_ملف);
static mp_obj_t يقرأ_إدخال_قياسي(mp_obj_t 한도) {
    mp_int_t حجم=mp_obj_get_int(한도);
    if(حجم<0||حجم>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t بيانات; vstr_init_len(&بيانات,حجم);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)بيانات.buf,حجم,0,0,0);
    if(개수<0) { vstr_clear(&بيانات); 결과검사(개수); }
    بيانات.len=개수; return mp_obj_new_bytes_from_vstr(&بيانات);
}
static MP_DEFINE_CONST_FUN_OBJ_1(إدخال_قياسي_قارئ_عنصر, يقرأ_إدخال_قياسي);
static mp_obj_t كتابة_ملف(mp_obj_t اسم, mp_obj_t محتوى_قيمة) {
    const char *مسار = مسار_وسيطة(اسم);
    mp_buffer_info_t بيانات; mp_get_buffer_raise(محتوى_قيمة, &بيانات, MP_BUFFER_READ);
    if (بيانات.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t ملف_مؤشر = 결과검사(사용자호출(3, (uintptr_t)مسار, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, ملف_مؤشر, (uintptr_t)بيانات.buf, بيانات.len, 0, 0, 0);
    사용자호출(4, ملف_مؤشر, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(파일쓰기객체, كتابة_ملف);
static mp_obj_t يزيل_ملف(mp_obj_t اسم) { 결과검사(사용자호출(11, (uintptr_t)مسار_وسيطة(اسم), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, يزيل_ملف);
static mp_obj_t الرسام_مستطيل(size_t 개수, const mp_obj_t *وسيطة_صفيف) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(وسيطة_صفيف[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(مستطيل_عنصر, 5, 5, الرسام_مستطيل);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t حجم[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, حجم);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t ساعة_قيمة(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(ساعة_عنصر, ساعة_قيمة);
static mp_obj_t بروتوكول_مخطط_بيانات_المستخدم_فتح(mp_obj_t رقم_المنفذ) {
    int بيانات_منصب = mp_obj_get_int(رقم_المنفذ); if (بيانات_منصب < 0 || بيانات_منصب > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t ملف_مؤشر = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(بيانات_منصب); 첫째값.sin_addr.s_addr = 0;
    intptr_t نتيجة = 사용자호출(33, ملف_مؤشر, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (نتيجة < 0) { 사용자호출(4, ملف_مؤشر, 0, 0, 0, 0, 0); 결과검사(نتيجة); }
    return mp_obj_new_int(ملف_مؤشر);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, بروتوكول_مخطط_بيانات_المستخدم_فتح);
static mp_obj_t بروتوكول_مخطط_بيانات_المستخدم_يرسل(mp_obj_t ملف_مؤشر, mp_obj_t رقم_المنفذ, mp_obj_t محتوى_قيمة) {
    int بيانات_منصب = mp_obj_get_int(رقم_المنفذ); if (بيانات_منصب < 1 || بيانات_منصب > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t بيانات; mp_get_buffer_raise(محتوى_قيمة, &بيانات, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(بيانات_منصب); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(ملف_مؤشر), (uintptr_t)بيانات.buf, بيانات.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, بروتوكول_مخطط_بيانات_المستخدم_يرسل);
static uint32_t يقرأ_عنوان_الإنترنت(mp_obj_t قيمة) {
    size_t 길이; const char *نص=mp_obj_str_get_data(قيمة,&길이);
    unsigned حديث_منصب=0; uint32_t عنوان=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned قيمة=0,숫자수=0;
        while(حديث_منصب<길이&&نص[حديث_منصب]>='0'&&نص[حديث_منصب]<='9') {
            قيمة=قيمة*10+نص[حديث_منصب++]-'0'; if(++숫자수>3||قيمة>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        عنوان=عنوان<<8|قيمة;
        if(부분<3&&(حديث_منصب>=길이||نص[حديث_منصب++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(حديث_منصب!=길이)mp_raise_OSError(MP_EINVAL);
    return عنوان;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *وسيطة_صفيف) {
    (void)항목수; uint32_t عنوان=يقرأ_عنوان_الإنترنت(وسيطة_صفيف[1]);
    int رقم_المنفذ=mp_obj_get_int(وسيطة_صفيف[2]);if(رقم_المنفذ<1||رقم_المنفذ>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t بيانات;mp_get_buffer_raise(وسيطة_صفيف[3],&بيانات,MP_BUFFER_READ);
    struct pk_sockaddr_in الهدف={0};الهدف.sin_family=AF_INET;الهدف.sin_port=pk_htons(رقم_المنفذ);الهدف.sin_addr.s_addr=pk_htonl(عنوان);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(وسيطة_صفيف[0]),(uintptr_t)بيانات.buf,بيانات.len,0,(uintptr_t)&الهدف,sizeof(الهدف))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t ملف_مؤشر) {
    unsigned char بيانات[512]; struct pk_sockaddr_in نظير_قيمة; pk_socklen_t 길이값 = sizeof(نظير_قيمة);
    intptr_t حجم = 결과검사(사용자호출(35, mp_obj_get_int(ملف_مؤشر), (uintptr_t)بيانات, 512, 0, (uintptr_t)&نظير_قيمة, (uintptr_t)&길이값));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(بيانات, حجم), MP_OBJ_NEW_SMALL_INT(pk_htons(نظير_قيمة.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t بروتوكول_مخطط_بيانات_المستخدم_يغلق(mp_obj_t ملف_مؤشر) { 결과검사(사용자호출(4, mp_obj_get_int(ملف_مؤشر), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, بروتوكول_مخطط_بيانات_المستخدم_يغلق);
static mp_obj_t فتح_بث(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,سحابة_عائلة,بث_شبكة,بث_بروتوكول_النقل,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,فتح_بث);
static mp_obj_t يتصل_بث(mp_obj_t المشارك,mp_obj_t عنوان_نص,mp_obj_t فهرس) {
    int رقم_المنفذ=mp_obj_get_int(فهرس); if(رقم_المنفذ<1||رقم_المنفذ>65535)mp_raise_OSError(MP_EINVAL);
    struct سحابة_مأخذ_التوصيل_عنوان عنوان={0}; عنوان.عنوان_عائلة=سحابة_عائلة;
    عنوان.رقم_المنفذ=망차례짧은수(رقم_المنفذ); عنوان.عنوان_الإنترنت.عنوان_قيمة=شبكة_عدد_صحيح(يقرأ_عنوان_الإنترنت(عنوان_نص));
    결과검사(사용자호출(37,mp_obj_get_int(المشارك),(uintptr_t)&عنوان,sizeof(عنوان),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(بث_موصل_عنصر,يتصل_بث);
static mp_obj_t يقرأ_بث(mp_obj_t المشارك,mp_obj_t 한도) {
    int 길이=mp_obj_get_int(한도); if(길이<1||길이>512)mp_raise_OSError(MP_EINVAL);
    unsigned char بيانات[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(المشارك),(uintptr_t)بيانات,길이,0,0,0));
    return mp_obj_new_bytes(بيانات,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(بث_قارئ_عنصر,يقرأ_بث);
static mp_obj_t كتابة_بث(mp_obj_t المشارك,mp_obj_t محتوى_قيمة) {
    mp_buffer_info_t بيانات; mp_get_buffer_raise(محتوى_قيمة,&بيانات,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(المشارك),(uintptr_t)بيانات.buf,بيانات.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(흐름쓰기객체,كتابة_بث);
static mp_obj_t 잠시기다리기(mp_obj_t قيمة_الوقت) {
    결과검사(사용자호출(17,mp_obj_get_int(قيمة_الوقت),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(انتظر_عنصر,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t اسم) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)مسار_وسيطة(اسم),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t فتح_دليل(mp_obj_t اسم) {
    결과검사(사용자호출(18,(uintptr_t)مسار_وسيطة(اسم),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(دليل_مؤلف_عنصر,فتح_دليل);
static mp_obj_t يزيل_دليل(mp_obj_t اسم) {
    결과검사(사용자호출(18,(uintptr_t)مسار_وسيطة(اسم),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,يزيل_دليل);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&بث_موصل_عنصر) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&بث_قارئ_عنصر) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&흐름쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&انتظر_عنصر) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&دليل_مؤلف_عنصر) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&إدخال_قياسي_قارئ_عنصر) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ملف_قارئ_عنصر) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&파일쓰기객체) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&مستطيل_عنصر) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&ساعة_عنصر) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
