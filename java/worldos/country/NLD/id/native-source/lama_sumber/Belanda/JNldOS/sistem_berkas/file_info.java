// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belanda.JNldOS.sistem_berkas;

public final class file_info {
    private final int Ukuran;
    private final int 형태;

    public file_info(int Ukuran, int 형태) {
        this.Ukuran = Ukuran;
        this.형태 = 형태;
    }

    public int Ukuran() {
        return Ukuran;
    }

    public int 형태() {
        return 형태;
    }
}

