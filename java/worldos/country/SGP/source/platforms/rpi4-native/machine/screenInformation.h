#ifndef nativeScreenInformationHeader
#define nativeScreenInformationHeader
#include <stdint.h>
/* 초기화가 끝난 actualData RGB32 Screen size. 준비되지 않았으면 0이다. */
uintptr_t boardScreenWidth(void);
uintptr_t boardScreenHeight(void);
/* 0: hiddenValue, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void boardPointer(int horizontalPosition, int verticalPosition, unsigned shapeValue);
/* 한 번에 32줄을 완성한 backValue, 달라진 화소만 actualData 화면에 옮긴다. */
void boardPrepareDrawing(volatile uint32_t *data, unsigned widthSpan, unsigned lengthValue, unsigned lineSpacingValue);
int boardDrawingBounds(int *horizontalPosition, int *verticalPosition, int *widthSpan, int *lengthValue);
int boardStartDrawing(int horizontalPosition, int verticalPosition, int widthSpan, int lengthValue);
void boardFinishDrawing(void);
void boardRectangleFill(int horizontalPosition, int verticalPosition, int widthSpan, int lengthValue, uint32_t colourValue);
/* actualData showValue 메모리에 기록한 pixel number. pointer 갱신은 제외한다. */
uint64_t boardDrawingCount(void);
uint32_t boardReadScreen(unsigned horizontalPosition, unsigned verticalPosition);
#endif
