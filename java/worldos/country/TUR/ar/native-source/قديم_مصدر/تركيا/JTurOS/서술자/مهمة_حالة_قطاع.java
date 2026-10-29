// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package تركيا.JTurOS.서술자;

/** x86 작업 تبديل_الوضع 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class مهمة_حالة_قطاع {
    private int رمز_صفر_حظر;
    private int رمز_صفر_عنوان;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int عنوان) {
        رمز_صفر_حظر = 조각;
        رمز_صفر_عنوان = عنوان;
    }

    public int رمز_صفر_حظر() { return رمز_صفر_حظر; }
    public int رمز_صفر_عنوان() { return رمز_صفر_عنوان; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

