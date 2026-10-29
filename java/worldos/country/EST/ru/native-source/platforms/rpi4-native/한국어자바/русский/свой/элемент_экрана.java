// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;
/** русский экран 구성요소를 만드는 편의 ФУНКЦИЯ_ЗНАЧЕН. */
public final class элемент_экрана {
    private элемент_экрана() {}
    public static void 나중에실행(실행할일 дело_задача) { Событие_Очередь.나중에실행(дело_задача); }
    public static Метка тег_ЗНАЧЕН(String текст, int 가로, int Вертикаль_позиция, int 폭, int 높이) {
        return new Метка(текст, 가로, Вертикаль_позиция, 폭, 높이);
    }
    public static кнопка кнопка(String текст, int 가로, int Вертикаль_позиция, int 폭, int 높이, 동작받이 받이) {
        return new кнопка(текст, 가로, Вертикаль_позиция, 폭, 높이, 받이);
    }
    public static текстовое_поле текстовое_поле(String текст, int 가로, int Вертикаль_позиция, int 폭, int 높이) {
        return new текстовое_поле(текст, 가로, Вертикаль_позиция, 폭, 높이);
    }
}
