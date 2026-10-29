// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 функция_мән. */
public final class виджет {
    private виджет() {}
    public static void 나중에실행(실행할일 тапсырма_ұсыныс) { оқиға_кезек.나중에실행(тапсырма_ұсыныс); }
    public static Белгі тег_мән(String Мәтін, int 가로, int Тік_лауазым, int 폭, int 높이) {
        return new Белгі(Мәтін, 가로, Тік_лауазым, 폭, 높이);
    }
    public static батырма батырма(String Мәтін, int 가로, int Тік_лауазым, int 폭, int 높이, 동작받이 받이) {
        return new батырма(Мәтін, 가로, Тік_лауазым, 폭, 높이, 받이);
    }
    public static мәтіндік_өріс мәтіндік_өріс(String Мәтін, int 가로, int Тік_лауазым, int 폭, int 높이) {
        return new мәтіндік_өріс(Мәтін, 가로, Тік_лауазым, 폭, 높이);
    }
}
