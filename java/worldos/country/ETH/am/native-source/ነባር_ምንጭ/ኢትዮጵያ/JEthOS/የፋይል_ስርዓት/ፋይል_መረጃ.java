// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.የፋይል_ስርዓት;

public final class ፋይል_መረጃ {
    private final int መጠን;
    private final int 형태;

    public ፋይል_መረጃ(int መጠን, int 형태) {
        this.መጠን = መጠን;
        this.형태 = 형태;
    }

    public int መጠን() {
        return መጠን;
    }

    public int 형태() {
        return 형태;
    }
}

