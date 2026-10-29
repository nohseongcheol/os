// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;
/** своє JVM과 커널의 Вікно 관리 기능에 직접 연결되는 Вікно. */
public final class Вікно extends 화면구성요소 {
    public Вікно(String вікно_Назва, int 폭, int 높이) {
        throw new Стан_виняток("своє JVM의 українська Вікно генерувати 기능이 필요합니다.");
    }
    public native void Додати_елемент(화면구성요소 елемент_значення);
    public native void показувати_вікно();
    public native void Закрити();
    public native boolean 보이는가();
}
