#ifndef JKOROS_NATIVE_GRAPHICS_H
#define JKOROS_NATIVE_GRAPHICS_H
/* 게스트 cc의 လုပ်ဆောင် 라이브러리가 တကယ့်ဒေတာ 프레임버퍼/단조 နာရီ SVC에 연결한다. */
int pk_rectangle(unsigned x,unsigned y,unsigned width,unsigned height,unsigned color);
unsigned pk_ticks_ms(void);
int pk_graphics_wait(void);
int စတုဂံဆွဲ(unsigned အလျားတည်နေရာ,unsigned ဒေါင်လိုက်တည်နေရာ,unsigned အနံတန်ဖိုး,unsigned အမြင့်တန်ဖိုး,unsigned ပုံမှတ်အရောင်);
unsigned မီလီစက္ကန့်(void);
int 그림기다리기(void);
int မျက်နှာပြင်အနံ(void);
int မျက်နှာပြင်အမြင့်(void);
#endif
