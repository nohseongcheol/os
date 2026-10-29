// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bhutan.JBtnOS.FileSystem;

public final class fileInformation {
    private final int size;
    private final int shapeKind;

    public fileInformation(int size, int shapeKind) {
        this.size = size;
        this.shapeKind = shapeKind;
    }

    public int size() {
        return size;
    }

    public int shapeKind() {
        return shapeKind;
    }
}

