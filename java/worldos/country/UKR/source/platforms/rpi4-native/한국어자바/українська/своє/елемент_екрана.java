// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;
/** українська 화면 구성요소를 만드는 편의 функція_значення. */
public final class елемент_екрана {
    private елемент_екрана() {}
    public static void 나중에실행(실행할일 справа_Дія) { подія_черга.나중에실행(справа_Дія); }
    public static Мітка тег_значення(String текст, int 가로, int Вертикаль_посада, int 폭, int 높이) {
        return new Мітка(текст, 가로, Вертикаль_посада, 폭, 높이);
    }
    public static кнопка кнопка(String текст, int 가로, int Вертикаль_посада, int 폭, int 높이, 동작받이 받이) {
        return new кнопка(текст, 가로, Вертикаль_посада, 폭, 높이, 받이);
    }
    public static текстове_поле текстове_поле(String текст, int 가로, int Вертикаль_посада, int 폭, int 높이) {
        return new текстове_поле(текст, 가로, Вертикаль_посада, 폭, 높이);
    }
}
