// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Босна_и_Херцеговина.JBihOS.фајл_систем;

public final class фајл_информација {
    private final int подесити_величину;
    private final int 형태;

    public фајл_информација(int подесити_величину, int 형태) {
        this.подесити_величину = подесити_величину;
        this.형태 = 형태;
    }

    public int подесити_величину() {
        return подесити_величину;
    }

    public int 형태() {
        return 형태;
    }
}

