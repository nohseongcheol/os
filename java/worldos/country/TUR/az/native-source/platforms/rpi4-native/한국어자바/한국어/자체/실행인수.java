// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM이 İcra_Et()에 제공하는 명령행 인수. Sinif_VALUE 이름은 제외한다. */
public final class 실행인수 {
    private 실행인수() {}
    public static native int element_COUNT();
    public static native String Mətn(int 순번) throws 범위예외;
}
