// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 функција_вриједност. */
public final class виџет {
    private виџет() {}
    public static void 나중에실행(실행할일 задатак_радња) { догађај_редослед.나중에실행(задатак_радња); }
    public static Натпис ознака_вриједност(String Текст, int 가로, int вертикала_позиција, int 폭, int 높이) {
        return new Натпис(Текст, 가로, вертикала_позиција, 폭, 높이);
    }
    public static дугме дугме(String Текст, int 가로, int вертикала_позиција, int 폭, int 높이, 동작받이 받이) {
        return new дугме(Текст, 가로, вертикала_позиција, 폭, 높이, 받이);
    }
    public static текстуално_поље текстуално_поље(String Текст, int 가로, int вертикала_позиција, int 폭, int 높이) {
        return new текстуално_поље(Текст, 가로, вертикала_позиција, 폭, 높이);
    }
}
