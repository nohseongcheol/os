// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;
/** свой JVM과 커널의 Окно 관리 기능에 직접 연결되는 Окно. */
public final class Окно extends экран_элемент {
    public Окно(String окно_право, int 폭, int 높이) {
        throw new Состояние_исключение("свой JVM의 русский Окно генерировать 기능이 필요합니다.");
    }
    public native void добавить_элемент(экран_элемент элемент_ЗНАЧЕН);
    public native void выпуск_окно();
    public native void Закрыть();
    public native boolean 보이는가();
}
