// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package الجزائر.JDzaOS.إدخال_قيمة;

public final class إدخال_حدث {
    public enum 종류 {
        مفتاح_متوقف_عن_التشغيل,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final 종류 نوع_الحدث;
    private final int 첫째값;
    private final int 둘째값;

    public إدخال_حدث(종류 نوع_الحدث, int 첫째값, int 둘째값) {
        this.نوع_الحدث = نوع_الحدث;
        this.첫째값 = 첫째값;
        this.둘째값 = 둘째값;
    }

    public 종류 نوع_الحدث() {
        return نوع_الحدث;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int 둘째값() {
        return 둘째값;
    }
}

