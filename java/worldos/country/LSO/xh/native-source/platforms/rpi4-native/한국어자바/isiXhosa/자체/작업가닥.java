// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자체;
/** 자체 JVM 스케줄러가 관리하는 ukwenza_umyalelo Stream_ixabiso. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 umsebenzi_Isenzo) {
        throw new 상태예외("자체 JVM의 isiXhosa 작업 ithredi_ixabiso 생성 기능이 필요합니다.");
    }
    public native void qala_umsebenzi() throws 가닥상태예외;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void misa_okwexeshana_umsebenzi();
}
