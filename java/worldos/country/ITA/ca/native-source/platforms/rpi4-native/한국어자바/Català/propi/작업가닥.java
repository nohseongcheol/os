// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;
/** propi JVM 스케줄러가 관리하는 Executa_ordre flux_VALOR. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 tasca_acció) {
        throw new Estat_excepció("propi JVM의 Català 작업 fil_VALOR generar 기능이 필요합니다.");
    }
    public native void Inici_tasca() throws fil_Estat_excepció;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void RENDTO_tasca();
}
