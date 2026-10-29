// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;
/** 자체 JVM 스케줄러가 관리하는 Изврши_наредба Stream_VALUE. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 задача_Дејство) {
        throw new статус_исклучок("자체 JVM의 Македонски 작업 нишка_VALUE генерира 기능이 필요합니다.");
    }
    public native void Start_задача() throws нишка_статус_исклучок;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void YIELD_задача();
}
