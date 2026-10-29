// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.서술자;

/** x86 작업 මාරු_වන්න_ප්_රකාරය 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class කාර්යය_තත්වය_ඛණ්ඩය {
    private int 영번쌓임조각;
    private int 영번쌓임주소;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int යොමුව) {
        영번쌓임조각 = 조각;
        영번쌓임주소 = යොමුව;
    }

    public int 영번쌓임조각() { return 영번쌓임조각; }
    public int 영번쌓임주소() { return 영번쌓임주소; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

