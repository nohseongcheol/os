// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;
/** savs JVM이 Palaist()에 제공하는 명령행 Parametri. klase_VALUE 이름은 제외한다. */
public final class 실행인수 {
    private 실행인수() {}
    public static native int krājums_COUNT();
    public static native String Teksts(int 순번) throws 범위예외;
}
