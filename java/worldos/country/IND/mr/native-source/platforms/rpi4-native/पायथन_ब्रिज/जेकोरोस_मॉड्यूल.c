// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "आवाहन.h"
#include "संचारजाळे_द्विमानजोडणी.h"
static intptr_t पडताळलेले(intptr_t मोजमाप) { if (मोजमाप < 0) mp_raise_OSError(-मोजमाप); return मोजमाप; }
static const char *पथ_वितर्क(mp_obj_t मूल्य) {
    size_t आयटम_संख्या; const char *मार्ग = mp_obj_str_get_data(मूल्य, &आयटम_संख्या);
    if (!आयटम_संख्या || आयटम_संख्या > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t क्रमांक_अनुक्रमणिका = 0; क्रमांक_अनुक्रमणिका < आयटम_संख्या; क्रमांक_अनुक्रमणिका++) if (!मार्ग[क्रमांक_अनुक्रमणिका]) mp_raise_OSError(MP_EINVAL);
    return मार्ग;
}
static mp_obj_t संचिका_वाचा(mp_obj_t नाव) {
    intptr_t संचिका_हाताळा = पडताळलेले(प्रयोक्ता_आवाहन(3, (uintptr_t)पथ_वितर्क(नाव), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t अभाव_स्थानिक_परतकरा;
    if (nlr_push(&अभाव_स्थानिक_परतकरा) == 0) {
        size_t आकार = पडताळलेले(प्रयोक्ता_आवाहन(9, संचिका_हाताळा, 0, 0, 0, 0, 0));
        vstr_t डेटा; vstr_init_len(&डेटा, आकार);
        intptr_t मोजमाप = प्रयोक्ता_आवाहन(2, संचिका_हाताळा, (uintptr_t)डेटा.buf, आकार, 0, 0, 0);
        पडताळलेले(मोजमाप); डेटा.len = मोजमाप;
        mp_obj_t मूल्य = mp_obj_new_bytes_from_vstr(&डेटा);
        nlr_pop(); प्रयोक्ता_आवाहन(4, संचिका_हाताळा, 0, 0, 0, 0, 0); return मूल्य;
    }
    प्रयोक्ता_आवाहन(4, संचिका_हाताळा, 0, 0, 0, 0, 0); nlr_jump(अभाव_स्थानिक_परतकरा.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(संचिका_रीडर_ऑब्जेक्ट, संचिका_वाचा);
static mp_obj_t प्रमाणित_आदान_वाचा(mp_obj_t धारणक्षमता_मर्यादा) {
    mp_int_t आकार=mp_obj_get_int(धारणक्षमता_मर्यादा);
    if(आकार<0||आकार>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t डेटा; vstr_init_len(&डेटा,आकार);
    intptr_t आयटम_संख्या=प्रयोक्ता_आवाहन(2,0,(uintptr_t)डेटा.buf,आकार,0,0,0);
    if(आयटम_संख्या<0) { vstr_clear(&डेटा); पडताळलेले(आयटम_संख्या); }
    डेटा.len=आयटम_संख्या; return mp_obj_new_bytes_from_vstr(&डेटा);
}
static MP_DEFINE_CONST_FUN_OBJ_1(प्रमाणित_आदान_रीडर_ऑब्जेक्ट, प्रमाणित_आदान_वाचा);
static mp_obj_t संचिका_लिहा(mp_obj_t नाव, mp_obj_t सामुग्री_मूल्य) {
    const char *मार्ग = पथ_वितर्क(नाव);
    mp_buffer_info_t डेटा; mp_get_buffer_raise(सामुग्री_मूल्य, &डेटा, MP_BUFFER_READ);
    if (डेटा.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t संचिका_हाताळा = पडताळलेले(प्रयोक्ता_आवाहन(3, (uintptr_t)मार्ग, 577, 0, 0, 0, 0));
    intptr_t प्रविष्टी_संख्या = प्रयोक्ता_आवाहन(1, संचिका_हाताळा, (uintptr_t)डेटा.buf, डेटा.len, 0, 0, 0);
    प्रयोक्ता_आवाहन(4, संचिका_हाताळा, 0, 0, 0, 0, 0); return mp_obj_new_int(पडताळलेले(प्रविष्टी_संख्या));
}
static MP_DEFINE_CONST_FUN_OBJ_2(संचिका_राइटर_ऑब्जेक्ट, संचिका_लिहा);
static mp_obj_t संचिका_काढणे(mp_obj_t नाव) { पडताळलेले(प्रयोक्ता_आवाहन(11, (uintptr_t)पथ_वितर्क(नाव), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(संचिका_काढणारा_ऑब्जेक्ट, संचिका_काढणे);
static mp_obj_t पेंट_आयत(size_t आयटम_संख्या, const mp_obj_t *वितर्क_ऍरे) {
    (void)आयटम_संख्या; unsigned पहिले_मूल्य[5]; for (unsigned क्रमांक_अनुक्रमणिका = 0; क्रमांक_अनुक्रमणिका < 5; क्रमांक_अनुक्रमणिका++) पहिले_मूल्य[क्रमांक_अनुक्रमणिका] = mp_obj_get_int(वितर्क_ऍरे[क्रमांक_अनुक्रमणिका]);
    पडताळलेले(पडदा_आयत(पहिले_मूल्य[0], पहिले_मूल्य[1], पहिले_मूल्य[2], पहिले_मूल्य[3], पहिले_मूल्य[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(आयत_ऑब्जेक्ट, 5, 5, पेंट_आयत);
static mp_obj_t पडदा_आकारा_वाचा(void) {
    mp_obj_t आकार[2] = {mp_obj_new_int(पडताळलेले(पडदा_रुंदी_वाचा())), mp_obj_new_int(पडताळलेले(पडदा_उंची_वाचा()))};
    return mp_obj_new_tuple(2, आकार);
}
static MP_DEFINE_CONST_FUN_OBJ_0(पडदा_आकारा_ऑब्जेक्ट, पडदा_आकारा_वाचा);
static mp_obj_t प्रतीक्षा_करा_साठी_पडदा_आदान(void) { return mp_obj_new_int(पडताळलेले(प्रतीक्षा_करा_साठी_पडदा_कळ())); }
static MP_DEFINE_CONST_FUN_OBJ_0(पडदा_प्रतीक्षा_करा_ऑब्जेक्ट, प्रतीक्षा_करा_साठी_पडदा_आदान);
static mp_obj_t घड्याळ_मूल्य(void) { return mp_obj_new_int_from_uint(प्रयोक्ता_आवाहन(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(घड्याळ_ऑब्जेक्ट, घड्याळ_मूल्य);
static mp_obj_t स्वतंत्रसंदेशसंचार_उघडा(mp_obj_t पोर्ट_नंबर) {
    int डेटा_स्थान = mp_obj_get_int(पोर्ट_नंबर); if (डेटा_स्थान < 0 || डेटा_स्थान > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t संचिका_हाताळा = पडताळलेले(प्रयोक्ता_आवाहन(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in पहिले_मूल्य = {0}; पहिले_मूल्य.sin_family = AF_INET; पहिले_मूल्य.sin_port = pk_htons(डेटा_स्थान); पहिले_मूल्य.sin_addr.s_addr = 0;
    intptr_t मोजमाप = प्रयोक्ता_आवाहन(33, संचिका_हाताळा, (uintptr_t)&पहिले_मूल्य, sizeof(पहिले_मूल्य), 0, 0, 0);
    if (मोजमाप < 0) { प्रयोक्ता_आवाहन(4, संचिका_हाताळा, 0, 0, 0, 0, 0); पडताळलेले(मोजमाप); }
    return mp_obj_new_int(संचिका_हाताळा);
}
static MP_DEFINE_CONST_FUN_OBJ_1(स्वतंत्रसंदेशसंचार_उघडा_वस्तुसंचिका, स्वतंत्रसंदेशसंचार_उघडा);
static mp_obj_t स्वतंत्रसंदेशसंचार_पाठवा(mp_obj_t संचिका_हाताळा, mp_obj_t पोर्ट_नंबर, mp_obj_t सामुग्री_मूल्य) {
    int डेटा_स्थान = mp_obj_get_int(पोर्ट_नंबर); if (डेटा_स्थान < 1 || डेटा_स्थान > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t डेटा; mp_get_buffer_raise(सामुग्री_मूल्य, &डेटा, MP_BUFFER_READ);
    struct pk_sockaddr_in पहिले_मूल्य = {0}; पहिले_मूल्य.sin_family = AF_INET; पहिले_मूल्य.sin_port = pk_htons(डेटा_स्थान); पहिले_मूल्य.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(पडताळलेले(प्रयोक्ता_आवाहन(34, mp_obj_get_int(संचिका_हाताळा), (uintptr_t)डेटा.buf, डेटा.len, 0, (uintptr_t)&पहिले_मूल्य, sizeof(पहिले_मूल्य))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(स्वतंत्रसंदेशसंचार_पाठवा_वस्तुसंचिका, स्वतंत्रसंदेशसंचार_पाठवा);
static uint32_t इंटरनेट_पत्ता_वाचा(mp_obj_t मूल्य) {
    size_t लांबी_मूल्य; const char *पाठ्य=mp_obj_str_get_data(मूल्य,&लांबी_मूल्य);
    unsigned सध्याचे_स्थान=0; uint32_t पत्ता=0;
    for(unsigned उपभाग_मूल्य=0;उपभाग_मूल्य<4;उपभाग_मूल्य++) {
        unsigned मूल्य=0,अंक_संख्या=0;
        while(सध्याचे_स्थान<लांबी_मूल्य&&पाठ्य[सध्याचे_स्थान]>='0'&&पाठ्य[सध्याचे_स्थान]<='9') {
            मूल्य=मूल्य*10+पाठ्य[सध्याचे_स्थान++]-'0'; if(++अंक_संख्या>3||मूल्य>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!अंक_संख्या)mp_raise_OSError(MP_EINVAL);
        पत्ता=पत्ता<<8|मूल्य;
        if(उपभाग_मूल्य<3&&(सध्याचे_स्थान>=लांबी_मूल्य||पाठ्य[सध्याचे_स्थान++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(सध्याचे_स्थान!=लांबी_मूल्य)mp_raise_OSError(MP_EINVAL);
    return पत्ता;
}
static mp_obj_t स्वतंत्रसंदेशसंचार_गंतव्यालापाठवा(size_t प्रविष्टी_संख्या, const mp_obj_t *वितर्क_ऍरे) {
    (void)प्रविष्टी_संख्या; uint32_t पत्ता=इंटरनेट_पत्ता_वाचा(वितर्क_ऍरे[1]);
    int पोर्ट_नंबर=mp_obj_get_int(वितर्क_ऍरे[2]);if(पोर्ट_नंबर<1||पोर्ट_नंबर>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t डेटा;mp_get_buffer_raise(वितर्क_ऍरे[3],&डेटा,MP_BUFFER_READ);
    struct pk_sockaddr_in लक्ष्य={0};लक्ष्य.sin_family=AF_INET;लक्ष्य.sin_port=pk_htons(पोर्ट_नंबर);लक्ष्य.sin_addr.s_addr=pk_htonl(पत्ता);
    return mp_obj_new_int(पडताळलेले(प्रयोक्ता_आवाहन(34,mp_obj_get_int(वितर्क_ऍरे[0]),(uintptr_t)डेटा.buf,डेटा.len,0,(uintptr_t)&लक्ष्य,sizeof(लक्ष्य))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(स्वतंत्रसंदेशसंचार_गंतव्यालापाठवा_वस्तुसंचिका,4,4,स्वतंत्रसंदेशसंचार_गंतव्यालापाठवा);
static mp_obj_t स्वतंत्रसंदेशसंचार_स्वीकार(mp_obj_t संचिका_हाताळा) {
    unsigned char डेटा[512]; struct pk_sockaddr_in समकक्ष_मूल्य; pk_socklen_t लांबी_डेटा = sizeof(समकक्ष_मूल्य);
    intptr_t आकार = पडताळलेले(प्रयोक्ता_आवाहन(35, mp_obj_get_int(संचिका_हाताळा), (uintptr_t)डेटा, 512, 0, (uintptr_t)&समकक्ष_मूल्य, (uintptr_t)&लांबी_डेटा));
    mp_obj_t मूल्ये[2] = {mp_obj_new_bytes(डेटा, आकार), MP_OBJ_NEW_SMALL_INT(pk_htons(समकक्ष_मूल्य.sin_port))};
    return mp_obj_new_tuple(2, मूल्ये);
}
static MP_DEFINE_CONST_FUN_OBJ_1(स्वतंत्रसंदेशसंचार_स्वीकार_वस्तुसंचिका, स्वतंत्रसंदेशसंचार_स्वीकार);
static mp_obj_t स्वतंत्रसंदेशसंचार_मिटवा(mp_obj_t संचिका_हाताळा) { पडताळलेले(प्रयोक्ता_आवाहन(4, mp_obj_get_int(संचिका_हाताळा), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(स्वतंत्रसंदेशसंचार_मिटवा_वस्तुसंचिका, स्वतंत्रसंदेशसंचार_मिटवा);
static mp_obj_t प्रवाह_उघडा(void) {
    return mp_obj_new_int(पडताळलेले(प्रयोक्ता_आवाहन(32,क्लाउड_कुटुंब,प्रवाह_संचारजाळे,प्रवाह_वाहतूक_प्रोटोकॉल,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(प्रवाह_उघडणारा_ऑब्जेक्ट,प्रवाह_उघडा);
static mp_obj_t कनेक्ट_प्रवाह(mp_obj_t संचारटोक,mp_obj_t पत्ता_मजकूर,mp_obj_t अनुक्रमणिका) {
    int पोर्ट_नंबर=mp_obj_get_int(अनुक्रमणिका); if(पोर्ट_नंबर<1||पोर्ट_नंबर>65535)mp_raise_OSError(MP_EINVAL);
    struct क्लाउड_संचारद्वार_पत्ता पत्ता={0}; पत्ता.पत्ता_कुटुंब=क्लाउड_कुटुंब;
    पत्ता.पोर्ट_नंबर=संचारजाळे_लघु(पोर्ट_नंबर); पत्ता.इंटरनेट_पत्ता.पत्ता_मूल्य=संचारजाळे_पूर्णांक(इंटरनेट_पत्ता_वाचा(पत्ता_मजकूर));
    पडताळलेले(प्रयोक्ता_आवाहन(37,mp_obj_get_int(संचारटोक),(uintptr_t)&पत्ता,sizeof(पत्ता),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(प्रवाह_कनेक्टर_ऑब्जेक्ट,कनेक्ट_प्रवाह);
static mp_obj_t प्रवाह_वाचा(mp_obj_t संचारटोक,mp_obj_t धारणक्षमता_मर्यादा) {
    int लांबी_मूल्य=mp_obj_get_int(धारणक्षमता_मर्यादा); if(लांबी_मूल्य<1||लांबी_मूल्य>512)mp_raise_OSError(MP_EINVAL);
    unsigned char डेटा[512];
    intptr_t आयटम_संख्या=पडताळलेले(प्रयोक्ता_आवाहन(2,mp_obj_get_int(संचारटोक),(uintptr_t)डेटा,लांबी_मूल्य,0,0,0));
    return mp_obj_new_bytes(डेटा,आयटम_संख्या);
}
static MP_DEFINE_CONST_FUN_OBJ_2(प्रवाह_रीडर_ऑब्जेक्ट,प्रवाह_वाचा);
static mp_obj_t प्रवाह_लिहा(mp_obj_t संचारटोक,mp_obj_t सामुग्री_मूल्य) {
    mp_buffer_info_t डेटा; mp_get_buffer_raise(सामुग्री_मूल्य,&डेटा,MP_BUFFER_READ);
    return mp_obj_new_int(पडताळलेले(प्रयोक्ता_आवाहन(1,mp_obj_get_int(संचारटोक),(uintptr_t)डेटा.buf,डेटा.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(प्रवाह_राइटर_ऑब्जेक्ट,प्रवाह_लिहा);
static mp_obj_t प्रतीक्षा_करा_तात्पुरते(mp_obj_t वेळ_मूल्य) {
    पडताळलेले(प्रयोक्ता_आवाहन(17,mp_obj_get_int(वेळ_मूल्य),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(प्रतीक्षा_करा_ऑब्जेक्ट,प्रतीक्षा_करा_तात्पुरते);
static mp_obj_t प्रविष्टी_प्रकार(mp_obj_t नाव) {
    return mp_obj_new_int(पडताळलेले(प्रयोक्ता_आवाहन(18,(uintptr_t)पथ_वितर्क(नाव),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(प्रविष्टी_प्रकार_ऑब्जेक्ट,प्रविष्टी_प्रकार);
static mp_obj_t निर्देशिका_तयार_करा(mp_obj_t नाव) {
    पडताळलेले(प्रयोक्ता_आवाहन(18,(uintptr_t)पथ_वितर्क(नाव),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(निर्देशिका_निर्माता_ऑब्जेक्ट,निर्देशिका_तयार_करा);
static mp_obj_t निर्देशिका_काढणे(mp_obj_t नाव) {
    पडताळलेले(प्रयोक्ता_आवाहन(18,(uintptr_t)पथ_वितर्क(नाव),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(निर्देशिका_काढणारा_ऑब्जेक्ट,निर्देशिका_काढणे);
static const mp_rom_map_elem_t मॉड्यूल_नावे[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&प्रवाह_उघडणारा_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&प्रवाह_कनेक्टर_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&प्रवाह_रीडर_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&प्रवाह_राइटर_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&प्रतीक्षा_करा_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&प्रविष्टी_प्रकार_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&निर्देशिका_निर्माता_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&निर्देशिका_काढणारा_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&प्रमाणित_आदान_रीडर_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&संचिका_रीडर_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&संचिका_राइटर_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&संचिका_काढणारा_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&आयत_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&पडदा_आकारा_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&पडदा_प्रतीक्षा_करा_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&घड्याळ_ऑब्जेक्ट) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&स्वतंत्रसंदेशसंचार_उघडा_वस्तुसंचिका) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&स्वतंत्रसंदेशसंचार_पाठवा_वस्तुसंचिका) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&स्वतंत्रसंदेशसंचार_गंतव्यालापाठवा_वस्तुसंचिका) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&स्वतंत्रसंदेशसंचार_स्वीकार_वस्तुसंचिका) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&स्वतंत्रसंदेशसंचार_मिटवा_वस्तुसंचिका) },
};
static MP_DEFINE_CONST_DICT(मॉड्यूल_सार्वत्रिकचले, मॉड्यूल_नावे);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&मॉड्यूल_सार्वत्रिकचले };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
