// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;
/** Македонски 화면 구성요소를 만드는 편의 ФУНКЦИЈА_VALUE. */
public final class графичка_контрола {
    private графичка_контрола() {}
    public static void 나중에실행(실행할일 задача_Дејство) { настан_ред_на_чекање.나중에실행(задача_Дејство); }
    public static Ознака ознака_VALUE(String Текст, int 가로, int вертикала_позиционирање, int 폭, int 높이) {
        return new Ознака(Текст, 가로, вертикала_позиционирање, 폭, 높이);
    }
    public static копче копче(String Текст, int 가로, int вертикала_позиционирање, int 폭, int 높이, 동작받이 받이) {
        return new копче(Текст, 가로, вертикала_позиционирање, 폭, 높이, 받이);
    }
    public static СМС_поле СМС_поле(String Текст, int 가로, int вертикала_позиционирање, int 폭, int 높이) {
        return new СМС_поле(Текст, 가로, вертикала_позиционирање, 폭, 높이);
    }
}
