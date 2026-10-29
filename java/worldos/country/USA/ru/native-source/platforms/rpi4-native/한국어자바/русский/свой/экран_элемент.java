// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;
/** свой JVM экран 객체의 공통 계약. 표준 Swing 객체를 보관하지 않는다. */
public abstract class экран_элемент {
    public native String чтение_SMS();
    public native void запись_SMS(String текст);
    public native void 자리정하기(int 가로, int Вертикаль_позиция, int 폭, int 높이);
}
