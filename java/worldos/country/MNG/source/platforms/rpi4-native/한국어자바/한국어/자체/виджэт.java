// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 ФУНКЦ_утга. */
public final class виджэт {
    private виджэт() {}
    public static void 나중에실행(실행할일 даалгавар_үйлдэл) { үйлдэл_дараалал.나중에실행(даалгавар_үйлдэл); }
    public static Тэмдэг шошго_утга(String Бичвэр, int 가로, int 세로, int 폭, int 높이) {
        return new Тэмдэг(Бичвэр, 가로, 세로, 폭, 높이);
    }
    public static товч товч(String Бичвэр, int 가로, int 세로, int 폭, int 높이, 동작받이 받이) {
        return new товч(Бичвэр, 가로, 세로, 폭, 높이, 받이);
    }
    public static бичвэрийн_талбар бичвэрийн_талбар(String Бичвэр, int 가로, int 세로, int 폭, int 높이) {
        return new бичвэрийн_талбар(Бичвэр, 가로, 세로, 폭, 높이);
    }
}
