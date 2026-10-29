// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Grenada.JGrdOS.Screen;

import java.util.Arrays;

/** Model of an 80x25 character display, such as VGA text mode. */
public final class characterDisplay {
    public static final int widthValue = 80;
    public static final int heightValue = 25;
    private final char[] characterValues = new char[widthValue * heightValue];
    private int horizontalPosition;
    private int verticalPosition;

    public characterDisplay() {
        eraseEntry();
    }

    public void Output(String contentValue) {
        for (int index = 0; index < contentValue.length(); index++) {
            char Characters = contentValue.charAt(index);
            if (Characters == '\n') {
                horizontalPosition = 0;
                verticalPosition++;
            } else {
                printCharacter(horizontalPosition++, verticalPosition, Characters);
            }
            if (horizontalPosition >= widthValue) {
                horizontalPosition = 0;
                verticalPosition++;
            }
            if (verticalPosition >= heightValue) {
                scrollUp();
            }
        }
    }

    public char Characters(int horizontalPosition, int verticalPosition) {
        verifyPosition(horizontalPosition, verticalPosition);
        return characterValues[verticalPosition * widthValue + horizontalPosition];
    }

    public void eraseEntry() {
        Arrays.fill(characterValues, ' ');
        horizontalPosition = 0;
        verticalPosition = 0;
    }

    private void printCharacter(int horizontalPosition, int verticalPosition, char Characters) {
        verifyPosition(horizontalPosition, verticalPosition);
        characterValues[verticalPosition * widthValue + horizontalPosition] = Characters;
    }

    private void scrollUp() {
        System.arraycopy(characterValues, widthValue, characterValues, 0, widthValue * (heightValue - 1));
        Arrays.fill(characterValues, widthValue * (heightValue - 1), characterValues.length, ' ');
        verticalPosition = heightValue - 1;
    }

    private void verifyPosition(int horizontalPosition, int verticalPosition) {
        if (horizontalPosition < 0 || horizontalPosition >= widthValue || verticalPosition < 0 || verticalPosition >= heightValue) {
            throw new IllegalArgumentException("Screen 위치가 올바르지 않습니다.");
        }
    }
}

