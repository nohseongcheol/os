// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Словаччина.JSvkOS.입력;

public final class 입력사건 {
    public enum 종류 {
        Ключ_неробочий,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final 종류 різновид_події;
    private final int 첫째값;
    private final int 둘째값;

    public 입력사건(종류 різновид_події, int 첫째값, int 둘째값) {
        this.різновид_події = різновид_події;
        this.첫째값 = 첫째값;
        this.둘째값 = 둘째값;
    }

    public 종류 різновид_події() {
        return різновид_події;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int 둘째값() {
        return 둘째값;
    }
}

