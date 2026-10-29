// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;

/** 表示等待執行緒的操作被中斷，而非工作本身結束。 */
public class 等待狀態已中斷異常 extends java.lang.InterruptedException {
    public 等待狀態已中斷異常() { super(); }
    public 等待狀態已中斷異常(String 說明) { super(說明); }
    public String 說明() { return getMessage(); }
}
