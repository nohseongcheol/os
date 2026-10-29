#ifndef JKOROS_NATIVE_GRAPHICS_H
#define JKOROS_NATIVE_GRAPHICS_H
/* 게스트 cc의 सुरू_करा 라이브러리가 वास्तविक_डेटा 프레임버퍼/단조 घड्याळ SVC에 연결한다. */
int pk_rectangle(unsigned x,unsigned y,unsigned width,unsigned height,unsigned color);
unsigned pk_ticks_ms(void);
int pk_graphics_wait(void);
int आयत_आरेखित_करा(unsigned आडवे_स्थान,unsigned अनुलंब_स्थान,unsigned रुंदी_मूल्य,unsigned उंची_मूल्य,unsigned पिक्सेल_रंग);
unsigned मिलिसेकंद(void);
int प्रतीक्षा_करा_साठी_रेखांकन(void);
int पडदा_रुंदी(void);
int पडदा_उंची(void);
#endif
