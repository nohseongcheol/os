// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 функция_маани. */
public final class уижет {
    private уижет() {}
    public static void 나중에실행(실행할일 маселе_иш_аракет) { окуя_кезек.나중에실행(маселе_иш_аракет); }
    public static метка тэг_маани(String Текст, int 가로, int 세로, int 폭, int 높이) {
        return new метка(Текст, 가로, 세로, 폭, 높이);
    }
    public static баскыч баскыч(String Текст, int 가로, int 세로, int 폭, int 높이, 동작받이 받이) {
        return new баскыч(Текст, 가로, 세로, 폭, 높이, 받이);
    }
    public static текст_талаасы текст_талаасы(String Текст, int 가로, int 세로, int 폭, int 높이) {
        return new текст_талаасы(Текст, 가로, 세로, 폭, 높이);
    }
}
