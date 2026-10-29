// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "통신규약.h"
static intptr_t 결과검사(intptr_t परिणाम) { if (परिणाम < 0) mp_raise_OSError(-परिणाम); return परिणाम; }
static const char *पथ_तर्क(mp_obj_t मान) {
    size_t 개수; const char *पथ = mp_obj_str_get_data(मान, &개수);
    if (!개수 || 개수 > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < 개수; 순번++) if (!पथ[순번]) mp_raise_OSError(MP_EINVAL);
    return पथ;
}
static mp_obj_t पढें_फ़ाइल(mp_obj_t नाम) {
    intptr_t फ़ाइल_हैंडल = 결과검사(사용자호출(3, (uintptr_t)पथ_तर्क(नाम), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t आकार = 결과검사(사용자호출(9, फ़ाइल_हैंडल, 0, 0, 0, 0, 0));
        vstr_t आँकड़े; vstr_init_len(&आँकड़े, आकार);
        intptr_t परिणाम = 사용자호출(2, फ़ाइल_हैंडल, (uintptr_t)आँकड़े.buf, आकार, 0, 0, 0);
        결과검사(परिणाम); आँकड़े.len = परिणाम;
        mp_obj_t मान = mp_obj_new_bytes_from_vstr(&आँकड़े);
        nlr_pop(); 사용자호출(4, फ़ाइल_हैंडल, 0, 0, 0, 0, 0); return मान;
    }
    사용자호출(4, फ़ाइल_हैंडल, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(फ़ाइल_पाठक_ऑब्जेक्ट, पढें_फ़ाइल);
static mp_obj_t 표준입력읽기(mp_obj_t 한도) {
    mp_int_t आकार=mp_obj_get_int(한도);
    if(आकार<0||आकार>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t आँकड़े; vstr_init_len(&आँकड़े,आकार);
    intptr_t 개수=사용자호출(2,0,(uintptr_t)आँकड़े.buf,आकार,0,0,0);
    if(개수<0) { vstr_clear(&आँकड़े); 결과검사(개수); }
    आँकड़े.len=개수; return mp_obj_new_bytes_from_vstr(&आँकड़े);
}
static MP_DEFINE_CONST_FUN_OBJ_1(표준입력읽기객체, 표준입력읽기);
static mp_obj_t लिखना_फ़ाइल(mp_obj_t नाम, mp_obj_t सामग्री_मान) {
    const char *पथ = पथ_तर्क(नाम);
    mp_buffer_info_t आँकड़े; mp_get_buffer_raise(सामग्री_मान, &आँकड़े, MP_BUFFER_READ);
    if (आँकड़े.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t फ़ाइल_हैंडल = 결과검사(사용자호출(3, (uintptr_t)पथ, 577, 0, 0, 0, 0));
    intptr_t 항목수 = 사용자호출(1, फ़ाइल_हैंडल, (uintptr_t)आँकड़े.buf, आँकड़े.len, 0, 0, 0);
    사용자호출(4, फ़ाइल_हैंडल, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(항목수));
}
static MP_DEFINE_CONST_FUN_OBJ_2(फ़ाइल_राइटर_ऑब्जेक्ट, लिखना_फ़ाइल);
static mp_obj_t निकालें_फ़ाइल(mp_obj_t नाम) { 결과검사(사용자호출(11, (uintptr_t)पथ_तर्क(नाम), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, निकालें_फ़ाइल);
static mp_obj_t पेंट_करना_रेक्_टेंगल(size_t 개수, const mp_obj_t *तर्क_सरणी) {
    (void)개수; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(तर्क_सरणी[순번]);
    결과검사(화면사각형(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(रेक्_टेंगल_ऑब्जेक्ट, 5, 5, पेंट_करना_रेक्_टेंगल);
static mp_obj_t 화면크기읽기(void) {
    mp_obj_t आकार[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(화면높이읽기()))};
    return mp_obj_new_tuple(2, आकार);
}
static MP_DEFINE_CONST_FUN_OBJ_0(화면크기객체, 화면크기읽기);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(화면기다림객체, 화면입력기다리기);
static mp_obj_t घड़ी_मान(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(घड़ी_ऑब्जेक्ट, घड़ी_मान);
static mp_obj_t यूज़र_डेटाग्राम_प्रॉटोकॉल_जारी(mp_obj_t पोर्ट_संख्या) {
    int डेटा_पद = mp_obj_get_int(पोर्ट_संख्या); if (डेटा_पद < 0 || डेटा_पद > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t फ़ाइल_हैंडल = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(डेटा_पद); 첫째값.sin_addr.s_addr = 0;
    intptr_t परिणाम = 사용자호출(33, फ़ाइल_हैंडल, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (परिणाम < 0) { 사용자호출(4, फ़ाइल_हैंडल, 0, 0, 0, 0, 0); 결과검사(परिणाम); }
    return mp_obj_new_int(फ़ाइल_हैंडल);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문열기객체, यूज़र_डेटाग्राम_प्रॉटोकॉल_जारी);
static mp_obj_t यूज़र_डेटाग्राम_प्रॉटोकॉल_भेजें(mp_obj_t फ़ाइल_हैंडल, mp_obj_t पोर्ट_संख्या, mp_obj_t सामग्री_मान) {
    int डेटा_पद = mp_obj_get_int(पोर्ट_संख्या); if (डेटा_पद < 1 || डेटा_पद > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t आँकड़े; mp_get_buffer_raise(सामग्री_मान, &आँकड़े, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(डेटा_पद); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(फ़ाइल_हैंडल), (uintptr_t)आँकड़े.buf, आँकड़े.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(전문전송객체, यूज़र_डेटाग्राम_प्रॉटोकॉल_भेजें);
static uint32_t पढें_इंटरनेट_पता(mp_obj_t मान) {
    size_t 길이; const char *पाठ=mp_obj_str_get_data(मान,&길이);
    unsigned अद्यतित_पद=0; uint32_t पता=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned मान=0,숫자수=0;
        while(अद्यतित_पद<길이&&पाठ[अद्यतित_पद]>='0'&&पाठ[अद्यतित_पद]<='9') {
            मान=मान*10+पाठ[अद्यतित_पद++]-'0'; if(++숫자수>3||मान>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!숫자수)mp_raise_OSError(MP_EINVAL);
        पता=पता<<8|मान;
        if(부분<3&&(अद्यतित_पद>=길이||पाठ[अद्यतित_पद++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(अद्यतित_पद!=길이)mp_raise_OSError(MP_EINVAL);
    return पता;
}
static mp_obj_t 전문주소전송(size_t 항목수, const mp_obj_t *तर्क_सरणी) {
    (void)항목수; uint32_t पता=पढें_इंटरनेट_पता(तर्क_सरणी[1]);
    int पोर्ट_संख्या=mp_obj_get_int(तर्क_सरणी[2]);if(पोर्ट_संख्या<1||पोर्ट_संख्या>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t आँकड़े;mp_get_buffer_raise(तर्क_सरणी[3],&आँकड़े,MP_BUFFER_READ);
    struct pk_sockaddr_in लक्ष्य={0};लक्ष्य.sin_family=AF_INET;लक्ष्य.sin_port=pk_htons(पोर्ट_संख्या);लक्ष्य.sin_addr.s_addr=pk_htonl(पता);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(तर्क_सरणी[0]),(uintptr_t)आँकड़े.buf,आँकड़े.len,0,(uintptr_t)&लक्ष्य,sizeof(लक्ष्य))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t फ़ाइल_हैंडल) {
    unsigned char आँकड़े[512]; struct pk_sockaddr_in पीअर_मान; pk_socklen_t 길이값 = sizeof(पीअर_मान);
    intptr_t आकार = 결과검사(사용자호출(35, mp_obj_get_int(फ़ाइल_हैंडल), (uintptr_t)आँकड़े, 512, 0, (uintptr_t)&पीअर_मान, (uintptr_t)&길이값));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(आँकड़े, आकार), MP_OBJ_NEW_SMALL_INT(pk_htons(पीअर_मान.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t यूज़र_डेटाग्राम_प्रॉटोकॉल_बंद(mp_obj_t फ़ाइल_हैंडल) { 결과검사(사용자호출(4, mp_obj_get_int(फ़ाइल_हैंडल), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(전문닫기객체, यूज़र_डेटाग्राम_प्रॉटोकॉल_बंद);
static mp_obj_t जारी_स्ट्रीम(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,क्लाउड_समूह,स्ट्रीम_नेटवर्क,स्ट्रीम_ट्रांसपोर्ट_प्रोटोकॉल,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,जारी_स्ट्रीम);
static mp_obj_t कनेक्ट_स्ट्रीम(mp_obj_t एंडपॉइंट,mp_obj_t पता_पाठ,mp_obj_t इंडेक्स) {
    int पोर्ट_संख्या=mp_obj_get_int(इंडेक्स); if(पोर्ट_संख्या<1||पोर्ट_संख्या>65535)mp_raise_OSError(MP_EINVAL);
    struct क्लाउड_सॉकेट_पता पता={0}; पता.पता_समूह=क्लाउड_समूह;
    पता.पोर्ट_संख्या=망차례짧은수(पोर्ट_संख्या); पता.इंटरनेट_पता.पता_मान=नेटवर्क_पूर्णांक(पढें_इंटरनेट_पता(पता_पाठ));
    결과검사(사용자호출(37,mp_obj_get_int(एंडपॉइंट),(uintptr_t)&पता,sizeof(पता),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(स्ट्रीम_कनेक्टर_ऑब्जेक्ट,कनेक्ट_स्ट्रीम);
static mp_obj_t पढें_स्ट्रीम(mp_obj_t एंडपॉइंट,mp_obj_t 한도) {
    int 길이=mp_obj_get_int(한도); if(길이<1||길이>512)mp_raise_OSError(MP_EINVAL);
    unsigned char आँकड़े[512];
    intptr_t 개수=결과검사(사용자호출(2,mp_obj_get_int(एंडपॉइंट),(uintptr_t)आँकड़े,길이,0,0,0));
    return mp_obj_new_bytes(आँकड़े,개수);
}
static MP_DEFINE_CONST_FUN_OBJ_2(स्ट्रीम_पाठक_ऑब्जेक्ट,पढें_स्ट्रीम);
static mp_obj_t लिखना_स्ट्रीम(mp_obj_t एंडपॉइंट,mp_obj_t सामग्री_मान) {
    mp_buffer_info_t आँकड़े; mp_get_buffer_raise(सामग्री_मान,&आँकड़े,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(एंडपॉइंट),(uintptr_t)आँकड़े.buf,आँकड़े.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(स्ट्रीम_राइटर_ऑब्जेक्ट,लिखना_स्ट्रीम);
static mp_obj_t 잠시기다리기(mp_obj_t समय_उपयोगिता) {
    결과검사(사용자호출(17,mp_obj_get_int(समय_उपयोगिता),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(प्रतीक्षा_करें_ऑब्जेक्ट,잠시기다리기);
static mp_obj_t 항목종류(mp_obj_t नाम) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)पथ_तर्क(नाम),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(항목종류객체,항목종류);
static mp_obj_t बनाएँ_डायरेक्टरी(mp_obj_t नाम) {
    결과검사(사용자호출(18,(uintptr_t)पथ_तर्क(नाम),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(डायरेक्टरी_निर्माता_ऑब्जेक्ट,बनाएँ_डायरेक्टरी);
static mp_obj_t निकालें_डायरेक्टरी(mp_obj_t नाम) {
    결과검사(사용자호출(18,(uintptr_t)पथ_तर्क(नाम),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,निकालें_डायरेक्टरी);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&स्ट्रीम_कनेक्टर_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&स्ट्रीम_पाठक_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&स्ट्रीम_राइटर_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&प्रतीक्षा_करें_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&항목종류객체) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&डायरेक्टरी_निर्माता_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&표준입력읽기객체) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&फ़ाइल_पाठक_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&फ़ाइल_राइटर_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&रेक्_टेंगल_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&화면크기객체) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&화면기다림객체) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&घड़ी_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&전문열기객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&전문전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&전문닫기객체) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
