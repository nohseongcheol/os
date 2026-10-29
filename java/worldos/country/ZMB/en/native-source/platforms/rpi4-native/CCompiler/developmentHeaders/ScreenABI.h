#ifndef JKOROS_NATIVE_GRAPHICS_H
#define JKOROS_NATIVE_GRAPHICS_H
/* 게스트 cc의 run 라이브러리가 actualData 프레임버퍼/단조 Clock SVC에 연결한다. */
int pk_rectangle(unsigned x,unsigned y,unsigned width,unsigned height,unsigned color);
unsigned pk_ticks_ms(void);
int pk_graphics_wait(void);
int drawRectangle(unsigned horizontalPosition,unsigned verticalPosition,unsigned widthValue,unsigned heightValue,unsigned pixelColour);
unsigned milliseconds(void);
int waitForDrawing(void);
int screenWidth(void);
int screenHeight(void);
#endif
