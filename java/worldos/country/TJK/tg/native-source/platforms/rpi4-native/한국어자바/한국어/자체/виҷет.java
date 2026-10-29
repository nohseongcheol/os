// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 функсия_қимат. */
public final class виҷет {
    private виҷет() {}
    public static void 나중에실행(실행할일 вазифа_амал) { рӯйдод_навбат.나중에실행(вазифа_амал); }
    public static барчасп барчасп_қимат(String Матн, int 가로, int 세로, int 폭, int 높이) {
        return new барчасп(Матн, 가로, 세로, 폭, 높이);
    }
    public static тугма тугма(String Матн, int 가로, int 세로, int 폭, int 높이, 동작받이 받이) {
        return new тугма(Матн, 가로, 세로, 폭, 높이, 받이);
    }
    public static Матн_майдон Матн_майдон(String Матн, int 가로, int 세로, int 폭, int 높이) {
        return new Матн_майдон(Матн, 가로, 세로, 폭, 높이);
    }
}
