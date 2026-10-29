// 동일 मराठी 헤더를 사용하는 별도 EL0 लायब्ररी. गाभा_मूल्य 직접 호출판과 혼합 निषिद्ध_मूल्य.
#include "संचिका_द्विमानजोडणी.h"
#include "आवाहन.h"
#include "संचारजाळे_द्विमानजोडणी.h"
static int त्रुटी_कोड;
int *pk_errno_location(void) { return &त्रुटी_कोड; }
static intptr_t पडताळलेले(intptr_t मोजमाप) { if (मोजमाप < 0) { त्रुटी_कोड = -मोजमाप; return -1; } return मोजमाप; }
int pk_open(const char *path, int flags, ...) { return पडताळलेले(प्रयोक्ता_आवाहन(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
आदानप्रदान_मोजमाप_टाइप_करा pk_read(int fd, void *p, size_t n) { return पडताळलेले(प्रयोक्ता_आवाहन(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
आदानप्रदान_मोजमाप_टाइप_करा pk_write(int fd, const void *p, size_t n) { return पडताळलेले(प्रयोक्ता_आवाहन(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return पडताळलेले(प्रयोक्ता_आवाहन(4, fd, 0, 0, 0, 0, 0)); }
संचिका_ऑफसेट_टाइप_करा pk_lseek(int fd, संचिका_ऑफसेट_टाइप_करा offset, int origin) { return पडताळलेले(प्रयोक्ता_आवाहन(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return पडताळलेले(प्रयोक्ता_आवाहन(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, संचिका_ऑफसेट_टाइप_करा size) { return पडताळलेले(प्रयोक्ता_आवाहन(10, fd, size, 0, 0, 0, 0)); }
int pk_fsync(int fd) { return पडताळलेले(प्रयोक्ता_आवाहन(12, fd, 0, 0, 0, 0, 0)); }
int pk_size(int fd) { return पडताळलेले(प्रयोक्ता_आवाहन(9, fd, 0, 0, 0, 0, 0)); }
int pk_socket(int domain, int type, int protocol) { return पडताळलेले(प्रयोक्ता_आवाहन(32, domain, type, protocol, 0, 0, 0)); }
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length) {
    return पडताळलेले(प्रयोक्ता_आवाहन(33, fd, (uintptr_t)address, length, 0, 0, 0));
}
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length) {
    return पडताळलेले(प्रयोक्ता_आवाहन(34, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, length));
}
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length) {
    return पडताळलेले(प्रयोक्ता_आवाहन(35, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, (uintptr_t)length));
}
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length) {
    return पडताळलेले(प्रयोक्ता_आवाहन(36, fd, (uintptr_t)address, (uintptr_t)length, 0, 0, 0));
}
int pk_connect(int fd,const struct pk_sockaddr *address,pk_socklen_t length){return पडताळलेले(प्रयोक्ता_आवाहन(37,fd,(uintptr_t)address,length,0,0,0));}
int pk_listen(int fd,int backlog){return पडताळलेले(प्रयोक्ता_आवाहन(38,fd,backlog,0,0,0,0));}
int pk_accept(int fd,struct pk_sockaddr *address,pk_socklen_t *length){return पडताळलेले(प्रयोक्ता_आवाहन(39,fd,(uintptr_t)address,(uintptr_t)length,0,0,0));}

/* मराठी 공개 함수의 वास्तविक_डेटा EL0 अंमलबजावणी. 구조체는 SVC에서 इन्स्टन्स_मूल्य·검증한다. */
int संचारटोक_तयार_करा(int पत्ता_कुटुंब,int संचार_मोड,int स्थानांतर_प्रोटोकॉल) {
    return पडताळलेले(प्रयोक्ता_आवाहन(32,पत्ता_कुटुंब,संचार_मोड,स्थानांतर_प्रोटोकॉल,0,0,0));
}
int बाइंड_करा_पत्ता(int संचारटोक,const struct संचारद्वार_पत्ता *पत्ता,संचारद्वार_पत्ता_लांबी_टाइप_करा लांबी_मूल्य) {
    return पडताळलेले(प्रयोक्ता_आवाहन(33,संचारटोक,(uintptr_t)पत्ता,लांबी_मूल्य,0,0,0));
}
intptr_t स्वतंत्रसंदेश_डेटा_पाठवा(int संचारटोक,const void *डेटा,size_t आयटम_संख्या,int निवड_मूल्य,const struct संचारद्वार_पत्ता *पत्ता,संचारद्वार_पत्ता_लांबी_टाइप_करा लांबी_मूल्य) {
    return पडताळलेले(प्रयोक्ता_आवाहन(34,संचारटोक,(uintptr_t)डेटा,आयटम_संख्या,निवड_मूल्य,(uintptr_t)पत्ता,लांबी_मूल्य));
}
intptr_t स्वतंत्रसंदेश_डेटा_स्वीकारा(int संचारटोक,void *डेटा,size_t आयटम_संख्या,int निवड_मूल्य,struct संचारद्वार_पत्ता *पत्ता,संचारद्वार_पत्ता_लांबी_टाइप_करा *लांबी_मूल्य) {
    return पडताळलेले(प्रयोक्ता_आवाहन(35,संचारटोक,(uintptr_t)डेटा,आयटम_संख्या,निवड_मूल्य,(uintptr_t)पत्ता,(uintptr_t)लांबी_मूल्य));
}
int संचारद्वार_पत्ता_वाचा(int संचारटोक,struct संचारद्वार_पत्ता *पत्ता,संचारद्वार_पत्ता_लांबी_टाइप_करा *लांबी_मूल्य) {
    return पडताळलेले(प्रयोक्ता_आवाहन(36,संचारटोक,(uintptr_t)पत्ता,(uintptr_t)लांबी_मूल्य,0,0,0));
}
int कनेक्ट_संचारजाळे(int संचारटोक,const struct संचारद्वार_पत्ता *पत्ता,संचारद्वार_पत्ता_लांबी_टाइप_करा लांबी_मूल्य) {
    return पडताळलेले(प्रयोक्ता_आवाहन(37,संचारटोक,(uintptr_t)पत्ता,लांबी_मूल्य,0,0,0));
}
int प्रतीक्षा_करा_साठी_नेटवर्क_कनेक्शन(int संचारटोक,int प्रतीक्षारत_संख्या) {
    return पडताळलेले(प्रयोक्ता_आवाहन(38,संचारटोक,प्रतीक्षारत_संख्या,0,0,0,0));
}
int स्वीकारा_नेटवर्क_कनेक्शन(int संचारटोक,struct संचारद्वार_पत्ता *पत्ता,संचारद्वार_पत्ता_लांबी_टाइप_करा *लांबी_मूल्य) {
    return पडताळलेले(प्रयोक्ता_आवाहन(39,संचारटोक,(uintptr_t)पत्ता,(uintptr_t)लांबी_मूल्य,0,0,0));
}

/* फाइल 함수도 독립된 मराठी फलन_मूल्य 심볼로 제공한다. */
int संचिका_उघडा(const char *मार्ग,int पद्धत_मोड,...) { return पडताळलेले(प्रयोक्ता_आवाहन(3,(uintptr_t)मार्ग,पद्धत_मोड,0,0,0,0)); }
आदानप्रदान_मोजमाप_टाइप_करा संचिका_डेटा_वाचा(int फाइल,void *डेटा,size_t आयटम_संख्या) { return पडताळलेले(प्रयोक्ता_आवाहन(2,फाइल,(uintptr_t)डेटा,आयटम_संख्या,0,0,0)); }
आदानप्रदान_मोजमाप_टाइप_करा संचिका_डेटा_लिहा(int फाइल,const void *डेटा,size_t आयटम_संख्या) { return पडताळलेले(प्रयोक्ता_आवाहन(1,फाइल,(uintptr_t)डेटा,आयटम_संख्या,0,0,0)); }
int संचिका_मिटवा(int फाइल) { return पडताळलेले(प्रयोक्ता_आवाहन(4,फाइल,0,0,0,0,0)); }
संचिका_ऑफसेट_टाइप_करा शोधा_संचिका(int फाइल,संचिका_ऑफसेट_टाइप_करा अंतर_मूल्य,int प्रोजेक्ट_मूळ) { return पडताळलेले(प्रयोक्ता_आवाहन(5,फाइल,अंतर_मूल्य,प्रोजेक्ट_मूळ,0,0,0)); }
int संचिका_प्रविष्टी_नाव_काढणे(const char *मार्ग) { return पडताळलेले(प्रयोक्ता_आवाहन(11,(uintptr_t)मार्ग,0,0,0,0,0)); }
int संचिका_लांबी_संच(int फाइल,संचिका_ऑफसेट_टाइप_करा आकार) { return पडताळलेले(प्रयोक्ता_आवाहन(10,फाइल,आकार,0,0,0,0)); }
int स्थिरकरा_फाईल_संग्रहण(int फाइल) { return पडताळलेले(प्रयोक्ता_आवाहन(12,फाइल,0,0,0,0,0)); }
int संचिका_आकारा(int फाइल) { return पडताळलेले(प्रयोक्ता_आवाहन(9,फाइल,0,0,0,0,0)); }
