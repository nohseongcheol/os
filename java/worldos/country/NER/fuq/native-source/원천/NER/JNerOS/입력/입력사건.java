// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package NER.JNerOS.입력;

public final class 입력사건 {
    public enum 종류 {
        키누름,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final 종류 사건종류;
    private final int 첫째값;
    private final int 둘째값;

    public 입력사건(종류 사건종류, int 첫째값, int 둘째값) {
        this.사건종류 = 사건종류;
        this.첫째값 = 첫째값;
        this.둘째값 = 둘째값;
    }

    public 종류 사건종류() {
        return 사건종류;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int 둘째값() {
        return 둘째값;
    }
}

