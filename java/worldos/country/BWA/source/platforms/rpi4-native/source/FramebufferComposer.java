// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Manages clipping, strip composition and pointer background. The board handles actual framebuffer access. */
public final class FramebufferComposer {
    static int widthValue, heightValue, isComposing, leftBoundaryValue, upperBoundary, rightBoundaryValue, lowerBoundaryValue;
    static int pointerX, pointerY, pointerShape;
    static int counterLow, counterHigh;
    static int[] composedPixels = new int[32 * 1920];
    static int[] pointerBackground = new int[21 * 21];
    static int[] clippedBounds = new int[4];
    public static void prepare(int widthSpan, int lengthValue) {
        widthValue = widthSpan; heightValue = lengthValue; isComposing = 0; pointerShape = 0;
        counterLow = 0; counterHigh = 0;
    }
    public static int getWidth() { return widthValue; }
    public static int getHeight() { return heightValue; }
    public static int getCounterLow() { return counterLow; }
    public static int getCounterHigh() { return counterHigh; }
    public static int clipValue(int ordinalIndex) { return clippedBounds[ordinalIndex]; }
    static int addPositiveLength(int startValue, int lengthValue) {
        if (startValue > 2147483647 - lengthValue) return 2147483647;
        return startValue + lengthValue;
    }
    public static int clip(int horizontalPosition, int verticalPosition, int widthSpan, int lengthValue) {
        if (widthValue == 0 || widthSpan <= 0 || lengthValue <= 0) return 0;
        int right = addPositiveLength(horizontalPosition, widthSpan), lowerSide = addPositiveLength(verticalPosition, lengthValue);
        int leftSide = isComposing != 0 ? leftBoundaryValue : 0, upperSide = isComposing != 0 ? upperBoundary : 0;
        int maximumHorizontalPosition = isComposing != 0 ? rightBoundaryValue : widthValue, maximumVerticalPosition = isComposing != 0 ? lowerBoundaryValue : heightValue;
        if (horizontalPosition < leftSide) horizontalPosition = leftSide;
        if (verticalPosition < upperSide) verticalPosition = upperSide;
        if (right > maximumHorizontalPosition) right = maximumHorizontalPosition;
        if (lowerSide > maximumVerticalPosition) lowerSide = maximumVerticalPosition;
        if (right <= horizontalPosition || lowerSide <= verticalPosition) return 0;
        clippedBounds[0] = horizontalPosition; clippedBounds[1] = verticalPosition;
        clippedBounds[2] = right - horizontalPosition; clippedBounds[3] = lowerSide - verticalPosition;
        return 1;
    }
    public static int run(int horizontalPosition, int verticalPosition, int widthSpan, int lengthValue) {
        if (isComposing != 0 || lengthValue > 32 || clip(horizontalPosition, verticalPosition, widthSpan, lengthValue) == 0) return 0;
        leftBoundaryValue = clippedBounds[0]; upperBoundary = clippedBounds[1];
        rightBoundaryValue = leftBoundaryValue + clippedBounds[2]; lowerBoundaryValue = upperBoundary + clippedBounds[3];
        isComposing = 1; return 1;
    }
    static boolean pointerBit(int horizontalPosition, int verticalPosition, int shapeValue) {
        if (shapeValue == 1) return horizontalPosition >= 0 && horizontalPosition <= verticalPosition / 2 && verticalPosition < 16;
        if (shapeValue == 3) horizontalPosition = 20 - horizontalPosition;
        int differenceValue = horizontalPosition - verticalPosition; if (differenceValue < 0) differenceValue = -differenceValue;
        return (differenceValue <= 1 && horizontalPosition >= 3 && horizontalPosition <= 17) ||
            (horizontalPosition >= 2 && horizontalPosition <= 8 && verticalPosition >= 2 && verticalPosition <= 8 && (horizontalPosition <= 3 || verticalPosition <= 3)) ||
            (horizontalPosition >= 12 && horizontalPosition <= 18 && verticalPosition >= 12 && verticalPosition <= 18 && (horizontalPosition >= 17 || verticalPosition >= 17));
    }
    static int pointerPixel(int horizontalPosition, int verticalPosition) {
        if (pointerBit(horizontalPosition, verticalPosition, pointerShape)) return 2;
        for (int line = -1; line <= 1; line++) for (int slotEntry = -1; slotEntry <= 1; slotEntry++)
            if (pointerBit(horizontalPosition + slotEntry, verticalPosition + line, pointerShape)) return 1;
        return 0;
    }
    static void displayPixel(int horizontalPosition, int verticalPosition, int colourValue) {
        int slotEntry = horizontalPosition - pointerX, line = verticalPosition - pointerY;
        if (pointerShape != 0 && slotEntry >= 0 && line >= 0 && slotEntry < 21 && line < 21) {
            pointerBackground[line * 21 + slotEntry] = colourValue;
            int pointValue = pointerPixel(slotEntry, line); if (pointValue != 0) colourValue = pointValue == 2 ? 0xffffff : 0x101010;
        }
        if (Board.readDisplayPixel(horizontalPosition, verticalPosition) != colourValue) {
            Board.writeDisplayPixel(horizontalPosition, verticalPosition, colourValue);
            counterLow++; if (counterLow == 0) counterHigh++;
        }
    }
    public static void finish() {
        if (isComposing == 0) return;
        for (int line = upperBoundary; line < lowerBoundaryValue; line++) for (int slotEntry = leftBoundaryValue; slotEntry < rightBoundaryValue; slotEntry++)
            displayPixel(slotEntry, line, composedPixels[(line - upperBoundary) * 1920 + slotEntry]);
        isComposing = 0;
    }
    public static int pixel(int horizontalPosition, int verticalPosition, int colourValue) {
        if (horizontalPosition < 0 || verticalPosition < 0 || horizontalPosition >= widthValue || verticalPosition >= heightValue) return 0;
        if (isComposing != 0) {
            if (horizontalPosition >= leftBoundaryValue && horizontalPosition < rightBoundaryValue && verticalPosition >= upperBoundary && verticalPosition < lowerBoundaryValue)
                composedPixels[(verticalPosition - upperBoundary) * 1920 + horizontalPosition] = colourValue;
        } else displayPixel(horizontalPosition, verticalPosition, colourValue);
        return 0;
    }
    public static void rectangleFill(int horizontalPosition, int verticalPosition, int widthSpan, int lengthValue, int colourValue) {
        if (clip(horizontalPosition, verticalPosition, widthSpan, lengthValue) == 0) return;
        horizontalPosition = clippedBounds[0]; verticalPosition = clippedBounds[1]; widthSpan = clippedBounds[2]; lengthValue = clippedBounds[3];
        for (int line = verticalPosition; line < verticalPosition + lengthValue; line++) for (int slotEntry = horizontalPosition; slotEntry < horizontalPosition + widthSpan; slotEntry++) {
            if (isComposing != 0) composedPixels[(line - upperBoundary) * 1920 + slotEntry] = colourValue;
            else displayPixel(slotEntry, line, colourValue);
        }
    }
    public static void pointer(int horizontalPosition, int verticalPosition, int shapeValue) {
        if (widthValue == 0) return;
        int newHorizontalPosition = horizontalPosition - (shapeValue >= 2 ? 10 : 0), newVerticalPosition = verticalPosition - (shapeValue >= 2 ? 10 : 0);
        if (pointerShape == shapeValue && pointerX == newHorizontalPosition && pointerY == newVerticalPosition) return;
        if (pointerShape != 0) for (int line = 0; line < 21; line++) for (int slotEntry = 0; slotEntry < 21; slotEntry++) {
            int firstOperand = pointerX + slotEntry, threeValue = pointerY + line;
            if (firstOperand >= 0 && threeValue >= 0 && firstOperand < widthValue && threeValue < heightValue) Board.writeDisplayPixel(firstOperand, threeValue, pointerBackground[line * 21 + slotEntry]);
        }
        pointerShape = shapeValue; pointerX = newHorizontalPosition; pointerY = newVerticalPosition;
        if (shapeValue != 0) for (int line = 0; line < 21; line++) for (int slotEntry = 0; slotEntry < 21; slotEntry++) {
            int firstOperand = pointerX + slotEntry, threeValue = pointerY + line;
            if (firstOperand >= 0 && threeValue >= 0 && firstOperand < widthValue && threeValue < heightValue) {
                pointerBackground[line * 21 + slotEntry] = Board.readDisplayPixel(firstOperand, threeValue);
                int pointValue = pointerPixel(slotEntry, line); if (pointValue != 0) Board.writeDisplayPixel(firstOperand, threeValue, pointValue == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
