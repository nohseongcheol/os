// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;
/** Asli JVM이 jalankan()에 제공하는 명령행 argumen. Kelas_VALUE 이름은 제외한다. */
public final class 실행인수 {
    private 실행인수() {}
    public static native int item_COUNT();
    public static native String teks(int 순번) throws 범위예외;
}
