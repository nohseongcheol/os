// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Польша.JPolOS.системный_вызов;

public final class система_Сведения {
    private final String система_имя;
    private final String узел_имя;
    private final String выпуск_ЗНАЧЕН_237a4c94;
    private final String версия_ЗНАЧЕН_65c6ecdc;
    private final String компьютер_5eb260fa;

    public система_Сведения(String система_имя, String узел_имя, String выпуск_ЗНАЧЕН_237a4c94, String версия_ЗНАЧЕН_65c6ecdc, String компьютер_5eb260fa) {
        this.система_имя = система_имя;
        this.узел_имя = узел_имя;
        this.выпуск_ЗНАЧЕН_237a4c94 = выпуск_ЗНАЧЕН_237a4c94;
        this.версия_ЗНАЧЕН_65c6ecdc = версия_ЗНАЧЕН_65c6ecdc;
        this.компьютер_5eb260fa = компьютер_5eb260fa;
    }

    public String система_имя() { return система_имя; }
    public String узел_имя() { return узел_имя; }
    public String выпуск_ЗНАЧЕН_237a4c94() { return выпуск_ЗНАЧЕН_237a4c94; }
    public String версия_ЗНАЧЕН_65c6ecdc() { return версия_ЗНАЧЕН_65c6ecdc; }
    public String компьютер_5eb260fa() { return компьютер_5eb260fa; }
}
