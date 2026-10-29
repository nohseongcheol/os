// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 巴拿馬.JPanOS.系統呼叫;

public final class 系統詳情列 {
    private final String 系統名稱;
    private final String 節點名稱;
    private final String 版本版次值;
    private final String 版本值;
    private final String 計算機;

    public 系統詳情列(String 系統名稱, String 節點名稱, String 版本版次值, String 版本值, String 計算機) {
        this.系統名稱 = 系統名稱;
        this.節點名稱 = 節點名稱;
        this.版本版次值 = 版本版次值;
        this.版本值 = 版本值;
        this.計算機 = 計算機;
    }

    public String 系統名稱() { return 系統名稱; }
    public String 節點名稱() { return 節點名稱; }
    public String 版本版次值() { return 版本版次值; }
    public String 版本值() { return 版本值; }
    public String 計算機() { return 計算機; }
}
