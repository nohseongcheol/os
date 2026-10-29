// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;
/** עצמי JVM이 הפעלה()에 제공하는 명령행 ארגומנטים. כיתה_ערך 이름은 제외한다. */
public final class 실행인수 {
    private 실행인수() {}
    public static native int 개수();
    public static native String טקסט(int 순번) throws 범위예외;
}
