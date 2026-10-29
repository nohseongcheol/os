// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中國香港特別行政區.JHkgOS.內核;

import 中國香港特別行政區.JHkgOS.記憶體空間.記憶體管理器;
import 中國香港特別行政區.JHkgOS.記憶體空間.頁管理器;
import 中國香港特別行政區.JHkgOS.輸入值.輸入管理器;
import 中國香港特別行政區.JHkgOS.任務.程序值;
import 中國香港特別行政區.JHkgOS.任務.調度器;
import 中國香港特別行政區.JHkgOS.系統呼叫.系統呼叫;
import 中國香港特別行政區.JHkgOS.檔案系統.檔案描述符表;
import 中國香港特別行政區.JHkgOS.檔案系統.檔案系統;

/** 負責 Java 管理核心的組裝與啟動。 */
public final class 內核 {
    private final 硬件值 設備;
    private final 記憶體管理器 記憶體空間 = new 記憶體管理器(32 * 1024 * 1024);
    private final 頁管理器 頁管理工作 = new 頁管理器();
    private final 檔案系統 檔案系統 = new 檔案系統();
    private final 調度器 調度器 = new 調度器(頁管理工作);
    private final 輸入管理器 輸入管理工作 = new 輸入管理器(256);
    private final 程序值 首位程序;
    private final 系統呼叫 系統呼叫;

    public 內核(硬件值 設備) {
        this.設備 = 設備;
        首位程序 = 調度器.首位程序(new 檔案描述符表(檔案系統));
        系統呼叫 = new 系統呼叫(檔案系統, 頁管理工作, 調度器, 設備, 輸入管理工作);
    }

    public void 運行() {
        設備.串行輸出("=== JHkgOS 관리 內核值 ===\n");
    }

    public void 執行步驟() {
        設備.停機CPU();
    }

    public 記憶體管理器 記憶體空間() {
        return 記憶體空間;
    }

    public 頁管理器 頁管理工作() {
        return 頁管理工作;
    }

    public 檔案系統 檔案系統() {
        return 檔案系統;
    }

    public 調度器 調度器() {
        return 調度器;
    }

    public 輸入管理器 輸入管理工作() {
        return 輸入管理工作;
    }

    public 程序值 首位程序() {
        return 首位程序;
    }

    public 系統呼叫 系統呼叫() {
        return 系統呼叫;
    }
}
