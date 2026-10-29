// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM이 Bitir()에 제공하는 명령행 인수. klas_baha 이름은 제외한다. */
public final class 실행인수 {
    private 실행인수() {}
    public static native int 개수();
    public static native String Metin(int 순번) throws 범위예외;
}
