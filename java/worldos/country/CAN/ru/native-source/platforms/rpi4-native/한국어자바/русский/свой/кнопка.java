// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;
/** свой 화면에서 Действие 알림을 보내는 кнопка. */
public final class кнопка extends экран_элемент {
    public кнопка(String текст, int 가로, int Вертикаль_позиция, int 폭, int 높이, 동작받이 받이) {
        throw new Состояние_исключение("свой JVM의 русский кнопка генерировать 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
