// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Србија.JSrbOS.фајл_систем;

public final class фајл_информација {
    private final int Величина;
    private final int 형태;

    public фајл_информација(int Величина, int 형태) {
        this.Величина = Величина;
        this.형태 = 형태;
    }

    public int Величина() {
        return Величина;
    }

    public int 형태() {
        return 형태;
    }
}

