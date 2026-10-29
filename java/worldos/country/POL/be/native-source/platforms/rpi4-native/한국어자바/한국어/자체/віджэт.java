// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 функцыя_значэнне. */
public final class віджэт {
    private віджэт() {}
    public static void 나중에실행(실행할일 задача_дзеянне) { падзея_чарга.나중에실행(задача_дзеянне); }
    public static Адмеціна тэг_значэнне(String Тэкст, int 가로, int 세로, int 폭, int 높이) {
        return new Адмеціна(Тэкст, 가로, 세로, 폭, 높이);
    }
    public static кнопка кнопка(String Тэкст, int 가로, int 세로, int 폭, int 높이, 동작받이 받이) {
        return new кнопка(Тэкст, 가로, 세로, 폭, 높이, 받이);
    }
    public static Тэкст_поле Тэкст_поле(String Тэкст, int 가로, int 세로, int 폭, int 높이) {
        return new Тэкст_поле(Тэкст, 가로, 세로, 폭, 높이);
    }
}
