// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
/** saját JVM 스케줄러가 관리하는 végrehajt_parancs Stream_ÉRTÉK. 표준 Thread를 감싸지 않는다. */
public final class dolgozó {
    public dolgozó(실행할일 teendő_Action) {
        throw new Állapot_kivétel("saját JVM의 magyar 작업 szál_ÉRTÉK generálás 기능이 필요합니다.");
    }
    public native void START_teendő() throws szál_Állapot_kivétel;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void HOZAM_teendő();
}
