// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 汶萊.JBrnOS.內核;

/** Java 管理核心與 CPU 專用程式之間的唯一邊界。 */
public interface 硬件值 {
    void 串行輸出(String 內容值);

    int 讀取埠位元組(int 硬件埠編號);

    void 寫入埠位元組(int 硬件埠編號, int 值);

    void 停機CPU();
}

