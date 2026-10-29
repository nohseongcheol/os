// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Brunei.JBrnOS.sistem_fail;

public final class fail_info {
    private final int Saiz;
    private final int 형태;

    public fail_info(int Saiz, int 형태) {
        this.Saiz = Saiz;
        this.형태 = 형태;
    }

    public int Saiz() {
        return Saiz;
    }

    public int 형태() {
        return 형태;
    }
}

