// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;
/** 자체 JVM 스케줄러가 관리하는 изпълнявам_команда поток_стойност. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 задача_проект) {
        throw new Състояние_изключение("자체 JVM의 Български 작업 нишка_стойност генерирам 기능이 필요합니다.");
    }
    public native void Старт_задача() throws нишка_Състояние_изключение;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void преустановявам_временно_задача();
}
