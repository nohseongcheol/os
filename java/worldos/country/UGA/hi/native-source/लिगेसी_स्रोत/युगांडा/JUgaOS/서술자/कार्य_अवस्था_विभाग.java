// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package युगांडा.JUgaOS.서술자;

/** x86 작업 स्विच_मोड 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class कार्य_अवस्था_विभाग {
    private int स्टैक_शून्य_ब्_लॉक;
    private int स्टैक_शून्य_पता;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int पता) {
        स्टैक_शून्य_ब्_लॉक = 조각;
        स्टैक_शून्य_पता = पता;
    }

    public int स्टैक_शून्य_ब्_लॉक() { return स्टैक_शून्य_ब्_लॉक; }
    public int स्टैक_शून्य_पता() { return स्टैक_शून्य_पता; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

