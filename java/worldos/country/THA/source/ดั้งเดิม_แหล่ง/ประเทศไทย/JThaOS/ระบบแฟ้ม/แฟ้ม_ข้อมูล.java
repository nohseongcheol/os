// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.ระบบแฟ้ม;

public final class แฟ้ม_ข้อมูล {
    private final int ขนาด;
    private final int 형태;

    public แฟ้ม_ข้อมูล(int ขนาด, int 형태) {
        this.ขนาด = ขนาด;
        this.형태 = 형태;
    }

    public int ขนาด() {
        return ขนาด;
    }

    public int 형태() {
        return 형태;
    }
}

