// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 菲律賓.JPhlOS.任務;

import 菲律賓.JPhlOS.記憶體空間.頁管理器;
import 菲律賓.JPhlOS.檔案系統.檔案描述符表;

public final class 程序值 {
    private final int 標識符值;
    private final int 父標識符;
    private final 頁管理器.地址空間 地址空間;
    private final 檔案描述符表 檔案描述符;
    private 程序狀態 狀態值 = 程序狀態.準備;
    private int 退出程式碼;
    private int 程式跳出 = 0x06000000;
    private int 執行狀態開始地址;
    private String[] 執行狀態實際參數 = new String[0];
    private String[] 環境值 = new String[0];

    程序值(int 標識符值, int 父標識符, 頁管理器.地址空間 地址空間, 檔案描述符表 檔案描述符) {
        this.標識符值 = 標識符值;
        this.父標識符 = 父標識符;
        this.地址空間 = 地址空間;
        this.檔案描述符 = 檔案描述符;
    }

    public int 標識符值() {
        return 標識符值;
    }

    public int 父標識符() {
        return 父標識符;
    }

    public 頁管理器.地址空間 地址空間() {
        return 地址空間;
    }

    public 檔案描述符表 檔案描述符() {
        return 檔案描述符;
    }

    public 程序狀態 狀態值() {
        return 狀態值;
    }

    public void 設定狀態(程序狀態 新建狀態) {
        狀態值 = 新建狀態;
    }

    public int 退出程式碼() {
        return 退出程式碼;
    }

    public void 退出程式(int 值) {
        退出程式碼 = 值 & 0xff;
        狀態值 = 程序狀態.退出程式;
    }

    public int 程式跳出() {
        return 程式跳出;
    }

    public void 設定程式跳出(int 新建結束) {
        if (新建結束 < 0x06000000 || 新建結束 > 0x07000000) {
            throw new IllegalArgumentException("程式 結尾 범위를 벗어났습니다.");
        }
        程式跳出 = 新建結束;
    }

    public void 設定執行狀態上下文(int 開始地址, String[] 形式參數實際參數, String[] 環境) {
        執行狀態開始地址 = 開始地址;
        執行狀態實際參數 = 形式參數實際參數.clone();
        環境值 = 環境.clone();
    }

    public int 執行狀態開始地址() { return 執行狀態開始地址; }
    public String[] 執行狀態實際參數() { return 執行狀態實際參數.clone(); }
    public String[] 環境值() { return 環境值.clone(); }
}
