// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 ფუნქცია_მნიშვნელობა. */
public final class ვიჯეტი {
    private ვიჯეტი() {}
    public static void 나중에실행(실행할일 დავალება_მოქმედება) { მოვლენა_რიგი.나중에실행(დავალება_მოქმედება); }
    public static სათაური თეგი_მნიშვნელობა(String ტექსტი, int 가로, int ვერტიკალური_პოზიცია, int 폭, int 높이) {
        return new სათაური(ტექსტი, 가로, ვერტიკალური_პოზიცია, 폭, 높이);
    }
    public static ღილაკი ღილაკი(String ტექსტი, int 가로, int ვერტიკალური_პოზიცია, int 폭, int 높이, 동작받이 받이) {
        return new ღილაკი(ტექსტი, 가로, ვერტიკალური_პოზიცია, 폭, 높이, 받이);
    }
    public static ტექსტური_ველი ტექსტური_ველი(String ტექსტი, int 가로, int ვერტიკალური_პოზიცია, int 폭, int 높이) {
        return new ტექსტური_ველი(ტექსტი, 가로, ვერტიკალური_პოზიცია, 폭, 높이);
    }
}
