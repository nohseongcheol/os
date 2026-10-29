// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Польща.JPolOS.системний_виклик;

public final class Система_Відомості {
    private final String Система_ім_я;
    private final String вузол_ім_я;
    private final String випуск_значення;
    private final String версія_значення;
    private final String комп_ютер;

    public Система_Відомості(String Система_ім_я, String вузол_ім_я, String випуск_значення, String версія_значення, String комп_ютер) {
        this.Система_ім_я = Система_ім_я;
        this.вузол_ім_я = вузол_ім_я;
        this.випуск_значення = випуск_значення;
        this.версія_значення = версія_значення;
        this.комп_ютер = комп_ютер;
    }

    public String Система_ім_я() { return Система_ім_я; }
    public String вузол_ім_я() { return вузол_ім_я; }
    public String випуск_значення() { return випуск_значення; }
    public String версія_значення() { return версія_значення; }
    public String комп_ютер() { return комп_ютер; }
}
