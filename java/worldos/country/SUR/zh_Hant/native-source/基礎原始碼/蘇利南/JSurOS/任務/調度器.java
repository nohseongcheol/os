// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 蘇利南.JSurOS.任務;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import 蘇利南.JSurOS.記憶體空間.頁管理器;
import 蘇利南.JSurOS.檔案系統.檔案描述符表;

/** 管理行程識別碼與循環排程的就緒佇列。 */
public final class 調度器 {
    private final 頁管理器 頁管理工作;
    private final Map<Integer, 程序值> 程序列表 = new HashMap<Integer, 程序值>();
    private final Queue<程序值> 就緒排隊 = new ArrayDeque<程序值>();
    private int 下一標識符 = 1;

    public 調度器(頁管理器 頁管理工作) {
        this.頁管理工作 = 頁管理工作;
    }

    public 程序值 首位程序(檔案描述符表 檔案描述符) {
        程序值 新建程序 = new 程序值(分配標識符(), 0, 頁管理工作.新建地址空間(), 檔案描述符);
        程序列表.put(Integer.valueOf(新建程序.標識符值()), 新建程序);
        就緒排隊.offer(新建程序);
        return 新建程序;
    }

    public 程序值 克隆值(程序值 父值) {
        程序值 子值 = new 程序值(
                分配標識符(),
                父值.標識符值(),
                頁管理工作.克隆複製啓用側寫入(父值.地址空間()),
                父值.檔案描述符().克隆值());
        子值.設定程式跳出(父值.程式跳出());
        程序列表.put(Integer.valueOf(子值.標識符值()), 子值);
        就緒排隊.offer(子值);
        return 子值;
    }

    public 程序值 下一程序() {
        int 檢查個數 = 就緒排隊.size();
        for (int 編號 = 0; 編號 < 檢查個數; 編號++) {
            程序值 下一項目 = 就緒排隊.poll();
            if (下一項目 != null && (下一項目.狀態值() == 程序狀態.準備 || 下一項目.狀態值() == 程序狀態.執行命令)) {
                下一項目.設定狀態(程序狀態.執行命令);
                就緒排隊.offer(下一項目);
                return 下一項目;
            }
        }
        return null;
    }

    public int 等待狀態用於子(程序值 父值, int 子標識符, boolean 非阻塞) {
        for (程序值 候選 : 程序列表.values()) {
            if (候選.父標識符() != 父值.標識符值()) {
                continue;
            }
            if (子標識符 > 0 && 候選.標識符值() != 子標識符) {
                continue;
            }
            if (候選.狀態值() == 程序狀態.退出程式) {
                int 結果 = (候選.退出程式碼() & 0xff) << 8;
                程序列表.remove(Integer.valueOf(候選.標識符值()));
                return 結果;
            }
            return 非阻塞 ? 0 : -11;
        }
        return -10;
    }

    public 程序值 查找程序(int 標識符值) {
        return 程序列表.get(Integer.valueOf(標識符值));
    }

    private int 分配標識符() {
        return 下一標識符++;
    }
}
