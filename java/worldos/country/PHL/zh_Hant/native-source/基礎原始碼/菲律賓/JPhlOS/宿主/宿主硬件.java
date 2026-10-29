// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 菲律賓.JPhlOS.宿主;

import java.util.HashMap;
import java.util.Map;
import 菲律賓.JPhlOS.內核.硬件值;

/** 在一般 JVM 上對受管理核心進行確定性測試的硬體替身。 */
public final class 宿主硬件 implements 硬件值 {
    private final Map<Integer, Integer> 硬件埠值 = new HashMap<Integer, Integer>();
    private final StringBuilder 串行日誌 = new StringBuilder();

    @Override
    public void 串行輸出(String 內容值) {
        串行日誌.append(內容值);
        System.out.print(內容值);
    }

    @Override
    public int 讀取埠位元組(int 硬件埠編號) {
        Integer 值 = 硬件埠值.get(Integer.valueOf(硬件埠編號));
        return 值 == null ? 0 : 值.intValue();
    }

    @Override
    public void 寫入埠位元組(int 硬件埠編號, int 值) {
        硬件埠值.put(Integer.valueOf(硬件埠編號), Integer.valueOf(值 & 0xff));
    }

    @Override
    public void 停機CPU() {
        // 主機測試中立即返回，不等待下一個事件。
    }

    public String 串行日誌() {
        return 串行日誌.toString();
    }
}

