// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 菲律賓.JPhlOS.系統呼叫;

import 菲律賓.JPhlOS.記憶體空間.頁管理器;
import 菲律賓.JPhlOS.任務.程序值;
import 菲律賓.JPhlOS.任務.調度器;
import 菲律賓.JPhlOS.檔案系統.可執行文件加載器;
import 菲律賓.JPhlOS.檔案系統.檔案系統;
import 菲律賓.JPhlOS.檔案系統.檔案信息;
import 菲律賓.JPhlOS.內核.硬件值;
import 菲律賓.JPhlOS.輸入值.輸入管理器;
import 菲律賓.JPhlOS.輸入值.輸入事件;

/** engos 第一階段 POSIX 呼叫的 Java 管理層。 */
public final class 系統呼叫 {
    public static final int 讀取僅用標誌 = 0;
    public static final int 搜索開始 = 0;
    public static final int 搜索當前 = 1;
    public static final int 查找條目結束 = 2;

    private final 檔案系統 檔案系統;
    private final 頁管理器 頁管理工作;
    private final 調度器 調度器;
    private final 可執行文件加載器 加載器 = new 可執行文件加載器();
    private final 硬件值 設備;
    private final 輸入管理器 輸入管理工作;

    public 系統呼叫(檔案系統 檔案系統, 頁管理器 頁管理工作, 調度器 調度器, 硬件值 設備, 輸入管理器 輸入管理工作) {
        this.檔案系統 = 檔案系統;
        this.頁管理工作 = 頁管理工作;
        this.調度器 = 調度器;
        this.設備 = 設備;
        this.輸入管理工作 = 輸入管理工作;
    }

    public int 程序標識符(程序值 當前程序) {
        return 當前程序.標識符值();
    }

    public int 父程序標識符(程序值 當前程序) {
        return 當前程序.父標識符();
    }

    public int 打開(程序值 當前程序, String 名稱, int 標誌值) {
        if (標誌值 != 讀取僅用標誌) {
            return -30;
        }
        return 當前程序.檔案描述符().打開(名稱);
    }

    public int 讀取(程序值 當前程序, int 描述符條目, byte[] 接收目的地址, int 大小) {
        if (描述符條目 == 0) {
            if (大小 <= 0 || 接收目的地址.length == 0) {
                return 0;
            }
            輸入事件 事件 = 輸入管理工作.下一事件();
            if (事件 == null || 事件.事件種類() != 輸入事件.種類值.鍵向下) {
                return -11;
            }
            接收目的地址[0] = (byte) 事件.首位值();
            return 1;
        }
        return 當前程序.檔案描述符().讀取(描述符條目, 接收目的地址, 大小);
    }

    public int 寫入(程序值 當前程序, int 描述符條目, byte[] 資料, int 大小) {
        if (描述符條目 != 1 && 描述符條目 != 2) {
            return 當前程序.檔案描述符().是否打開(描述符條目) ? -30 : -9;
        }
        if (大小 < 0 || 大小 > 資料.length) {
            return -22;
        }
        設備.串行輸出(new String(資料, 0, 大小, java.nio.charset.StandardCharsets.UTF_8));
        return 大小;
    }

    public int 關閉(程序值 當前程序, int 描述符條目) {
        return 當前程序.檔案描述符().關閉(描述符條目);
    }

    public int 移動位置(程序值 當前程序, int 描述符條目, int 距離值, int 項目根) {
        return 當前程序.檔案描述符().移動位置(描述符條目, 距離值, 項目根);
    }

    public int 複製副本描述符(程序值 當前程序, int 描述符條目) {
        return 當前程序.檔案描述符().已克隆描述符(描述符條目, 0);
    }

    public int 複製副本描述符位置(程序值 當前程序, int 描述符條目, int 新建描述符) {
        return 當前程序.檔案描述符().複製副本位置(描述符條目, 新建描述符);
    }

    public int 是否可訪問(String 名稱, int 方法模式) {
        檔案信息 系統信息 = 檔案系統.系統信息(名稱);
        if (系統信息 == null) {
            return -2;
        }
        if ((方法模式 & 1) != 0 && (系統信息.形狀種類() & 0111) == 0) {
            return -13;
        }
        if ((方法模式 & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int 切換任務列表(String 名稱) {
        return "/".equals(名稱) ? 0 : -20;
    }

    public String 當前任務列表(int 接收大小) {
        return 接收大小 >= 2 ? "/" : null;
    }

    public int 用戶標識符() { return 0; }
    public int 實效用戶標識符() { return 0; }
    public int 組標識符() { return 0; }
    public int 實效組標識符() { return 0; }

    public int 同步化檔案(程序值 當前程序, int 描述符條目) {
        return 當前程序.檔案描述符().系統信息(描述符條目) == null ? -9 : 0;
    }

    public void 同步化全部() {
        // 目前檔案系統唯讀，沒有需要寫出的資料。
    }

    public boolean 是否終端(程序值 當前程序, int 描述符條目) {
        檔案信息 系統信息 = 當前程序.檔案描述符().系統信息(描述符條目);
        return 系統信息 != null && (系統信息.形狀種類() & 0170000) == 0020000;
    }

    public int 檔案控制(程序值 當前程序, int 描述符條目, int 命令, int 形式參數實際參數) {
        if (命令 == 0) {
            return 當前程序.檔案描述符().已克隆描述符(描述符條目, 形式參數實際參數);
        }
        if (命令 == 1) {
            return 當前程序.檔案描述符().關閉啓用側執行操作值(描述符條目);
        }
        if (命令 == 2) {
            return 當前程序.檔案描述符().設定關閉啓用側執行操作(描述符條目, (形式參數實際參數 & 1) != 0);
        }
        if (命令 == 3) {
            return 當前程序.檔案描述符().系統信息(描述符條目) == null ? -9 : 讀取僅用標誌;
        }
        if (命令 == 4) {
            return 形式參數實際參數 == 讀取僅用標誌 ? 0 : -30;
        }
        return -22;
    }

    public int 創建條目(String 名稱, int 權限值) {
        return -30;
    }

    public 檔案信息 描述符信息(程序值 當前程序, int 描述符條目) {
        return 當前程序.檔案描述符().系統信息(描述符條目);
    }

    public 系統詳情列 系統詳情列() {
        return new 系統詳情列("JPhlOS", "JPhlOS", "0.1", "Java managed kernel", "i386");
    }

    public 檔案信息 檔案信息(String 名稱) {
        return 檔案系統.系統信息(名稱);
    }

    public 程序值 克隆程序(程序值 父值) {
        return 調度器.克隆值(父值);
    }

    public int 等待狀態用於子(程序值 父值, int 子標識符, boolean 非阻塞) {
        return 調度器.等待狀態用於子(父值, 子標識符, 非阻塞);
    }

    public int 程式跳出(程序值 當前程序, int 新建結束) {
        int 上一個結束 = 當前程序.程式跳出();
        if (新建結束 == 0) {
            return 上一個結束;
        }
        if (新建結束 < 0x06000000 || 新建結束 > 0x07000000) {
            return -12;
        }
        int 首位頁 = 上一個結束 / 頁管理器.頁大小;
        int 最後頁 = (新建結束 + 頁管理器.頁大小 - 1) / 頁管理器.頁大小;
        if (新建結束 > 上一個結束) {
            for (int 編號 = 首位頁; 編號 < 最後頁; 編號++) {
                int 地址 = 編號 * 頁管理器.頁大小;
                try {
                    頁管理工作.讀取位元組值(當前程序.地址空間(), 地址);
                } catch (IllegalStateException 錯誤) {
                    頁管理工作.映射表頁(當前程序.地址空間(), 地址, true);
                }
            }
        }
        當前程序.設定程式跳出(新建結束);
        return 新建結束;
    }

    public int 增加程式跳出(程序值 當前程序, int 遞增總量) {
        int 上一個結束 = 當前程序.程式跳出();
        int 結果 = 程式跳出(當前程序, 上一個結束 + 遞增總量);
        return 結果 < 0 ? 結果 : 上一個結束;
    }

    public int 執行命令(程序值 當前程序, byte[] 可執行文件檔案) {
        return 執行命令(當前程序, 可執行文件檔案, new String[0], new String[0]);
    }

    public int 執行命令(程序值 當前程序, byte[] 可執行文件檔案, String[] 形式參數實際參數, String[] 環境) {
        可執行文件加載器.映像 映像值;
        try {
            映像值 = 加載器.檢查項(可執行文件檔案);
        } catch (IllegalArgumentException 錯誤) {
            return -8;
        }
        if (形式參數實際參數 == null || 環境 == null || 形式參數實際參數.length > 16 || 環境.length > 16) {
            return -7;
        }
        for (可執行文件加載器.區段值 區段值 : 映像值.區段列列表()) {
            if ((區段值.標誌值() & 2) == 0 || 區段值.大小() == 0) {
                continue;
            }
            int 首位頁 = 區段值.地址() / 頁管理器.頁大小;
            int 最後頁 = (區段值.地址() + 區段值.大小() + 頁管理器.頁大小 - 1) / 頁管理器.頁大小;
            for (int 編號 = 首位頁; 編號 < 最後頁; 編號++) {
                int 地址 = 編號 * 頁管理器.頁大小;
                try {
                    頁管理工作.讀取位元組值(當前程序.地址空間(), 地址);
                    頁管理工作.私有範圍寫入(當前程序.地址空間(), 地址, 頁管理器.頁大小);
                } catch (IllegalStateException 錯誤) {
                    頁管理工作.映射表頁(當前程序.地址空間(), 地址, true);
                }
            }
            for (int 編號 = 0; 編號 < 區段值.大小(); 編號++) {
                byte 值 = 區段值.種類值() == 8 ? 0 : 可執行文件檔案[區段值.檔案位置() + 編號];
                頁管理工作.寫入位元組值(當前程序.地址空間(), 區段值.地址() + 編號, 值);
            }
        }
        當前程序.設定執行狀態上下文(映像值.開始地址(), 形式參數實際參數, 環境);
        當前程序.檔案描述符().關閉啓用側執行操作();
        return 0;
    }

    public void 結束程序(程序值 當前程序, int 狀態值) {
        當前程序.退出程式(狀態值);
    }
}
