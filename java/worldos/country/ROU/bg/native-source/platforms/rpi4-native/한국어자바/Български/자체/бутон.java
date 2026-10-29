// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;
/** 자체 화면에서 Операция 알림을 보내는 бутон. */
public final class бутон extends 화면구성요소 {
    public бутон(String Текст, int 가로, int вертикал_позиция, int 폭, int 높이, 동작받이 받이) {
        throw new Състояние_изключение("자체 JVM의 Български бутон генерирам 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
