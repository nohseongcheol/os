// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 функција_вриједност. */
public final class виџет {
    private виџет() {}
    public static void 나중에실행(실행할일 задатак_радња) { догађај_редослијед.나중에실행(задатак_радња); }
    public static ознака ознака_вриједност(String текст, int 가로, int 세로, int 폭, int 높이) {
        return new ознака(текст, 가로, 세로, 폭, 높이);
    }
    public static дугме дугме(String текст, int 가로, int 세로, int 폭, int 높이, 동작받이 받이) {
        return new дугме(текст, 가로, 세로, 폭, 높이, 받이);
    }
    public static текст_поље текст_поље(String текст, int 가로, int 세로, int 폭, int 높이) {
        return new текст_поље(текст, 가로, 세로, 폭, 높이);
    }
}
