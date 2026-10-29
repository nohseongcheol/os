// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 함수. */
public final class 화면요소 {
    private 화면요소() {}
    public static void 나중에실행(실행할일 할일) { 화면일정.나중에실행(할일); }
    public static 글표지 표지(String Teks, int 가로, int 세로, int 폭, int 높이) {
        return new 글표지(Teks, 가로, 세로, 폭, 높이);
    }
    public static 단추 단추(String Teks, int 가로, int 세로, int 폭, int 높이, 동작받이 받이) {
        return new 단추(Teks, 가로, 세로, 폭, 높이, 받이);
    }
    public static 입력칸 입력칸(String Teks, int 가로, int 세로, int 폭, int 높이) {
        return new 입력칸(Teks, 가로, 세로, 폭, 높이);
    }
}
