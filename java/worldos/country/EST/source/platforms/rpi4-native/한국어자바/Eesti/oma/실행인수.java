// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;
/** oma JVM이 Käivita_2()에 제공하는 명령행 Argumendid. tund_VALUE 이름은 제외한다. */
public final class 실행인수 {
    private 실행인수() {}
    public static native int kaup_COUNT();
    public static native String Tekst(int 순번) throws 범위예외;
}
