// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;
/** Български 화면 구성요소를 만드는 편의 функция_стойност. */
public final class изпълним_модул {
    private изпълним_модул() {}
    public static void 나중에실행(실행할일 задача_проект) { събитие_опашка.나중에실행(задача_проект); }
    public static Етикет етикет_стойност(String Текст, int 가로, int вертикал_позиция, int 폭, int 높이) {
        return new Етикет(Текст, 가로, вертикал_позиция, 폭, 높이);
    }
    public static бутон бутон(String Текст, int 가로, int вертикал_позиция, int 폭, int 높이, 동작받이 받이) {
        return new бутон(Текст, 가로, вертикал_позиция, 폭, 높이, 받이);
    }
    public static текстово_поле текстово_поле(String Текст, int 가로, int вертикал_позиция, int 폭, int 높이) {
        return new текстово_поле(Текст, 가로, вертикал_позиция, 폭, 높이);
    }
}
