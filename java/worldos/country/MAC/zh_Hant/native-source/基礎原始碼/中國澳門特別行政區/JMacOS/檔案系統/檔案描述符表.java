// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中國澳門特別行政區.JMacOS.檔案系統;

import java.util.HashMap;
import java.util.Map;

/** 保留各行程獨立的描述子與可共用的開啟檔案描述。 */
public final class 檔案描述符表 {
    private static final int 最大描述符 = 32;

    private static final class 描述符條目 {
        private final 檔案系統.已打開檔案 已打開檔案;
        private boolean 關閉啓用側執行操作;

        描述符條目(檔案系統.已打開檔案 已打開檔案) {
            this.已打開檔案 = 已打開檔案;
        }
    }

    private final 檔案系統 檔案系統;
    private final Map<Integer, 描述符條目> 描述符條目列 = new HashMap<Integer, 描述符條目>();

    public 檔案描述符表(檔案系統 檔案系統) {
        this.檔案系統 = 檔案系統;
    }

    public int 打開(String 名稱) {
        檔案系統.已打開檔案 已打開檔案 = 檔案系統.打開(名稱);
        if (已打開檔案 == null) {
            return -2;
        }
        int 編號 = 空索引(3);
        if (編號 < 0) {
            return -24;
        }
        描述符條目列.put(Integer.valueOf(編號), new 描述符條目(已打開檔案));
        return 編號;
    }

    public int 讀取(int 編號, byte[] 接收目的地址, int 大小) {
        描述符條目 條目值 = 描述符條目列.get(Integer.valueOf(編號));
        if (條目值 == null) {
            return -9;
        }
        if (大小 < 0 || 大小 > 接收目的地址.length) {
            return -22;
        }
        int 餘數資料 = 條目值.已打開檔案.資料.length - 條目值.已打開檔案.位置;
        int 讀取大小 = Math.min(大小, Math.max(餘數資料, 0));
        System.arraycopy(條目值.已打開檔案.資料, 條目值.已打開檔案.位置, 接收目的地址, 0, 讀取大小);
        條目值.已打開檔案.位置 += 讀取大小;
        return 讀取大小;
    }

    public int 移動位置(int 編號, int 距離值, int 項目根) {
        描述符條目 條目值 = 描述符條目列.get(Integer.valueOf(編號));
        if (條目值 == null) {
            return -9;
        }
        int 背景值;
        if (項目根 == 0) {
            背景值 = 0;
        } else if (項目根 == 1) {
            背景值 = 條目值.已打開檔案.位置;
        } else if (項目根 == 2) {
            背景值 = 條目值.已打開檔案.資料.length;
        } else {
            return -22;
        }
        int 新建位置 = 背景值 + 距離值;
        if (新建位置 < 0) {
            return -22;
        }
        條目值.已打開檔案.位置 = 新建位置;
        return 新建位置;
    }

    public int 關閉(int 編號) {
        描述符條目 條目值 = 描述符條目列.remove(Integer.valueOf(編號));
        if (條目值 == null) {
            return -9;
        }
        條目值.已打開檔案.引用個數--;
        return 0;
    }

    public int 已克隆描述符(int 編號, int 最小編號) {
        描述符條目 條目值 = 描述符條目列.get(Integer.valueOf(編號));
        if (條目值 == null) {
            return -9;
        }
        int 新建編號 = 空索引(最小編號);
        if (新建編號 < 0) {
            return -24;
        }
        條目值.已打開檔案.引用個數++;
        描述符條目列.put(Integer.valueOf(新建編號), new 描述符條目(條目值.已打開檔案));
        return 新建編號;
    }

    public int 複製副本位置(int 編號, int 新建編號) {
        if (編號 == 新建編號) {
            return 描述符條目列.containsKey(Integer.valueOf(編號)) ? 編號 : -9;
        }
        if (新建編號 < 0 || 新建編號 >= 最大描述符) {
            return -9;
        }
        描述符條目 原始 = 描述符條目列.get(Integer.valueOf(編號));
        if (原始 == null) {
            return -9;
        }
        if (描述符條目列.containsKey(Integer.valueOf(新建編號))) {
            關閉(新建編號);
        }
        原始.已打開檔案.引用個數++;
        描述符條目列.put(Integer.valueOf(新建編號), new 描述符條目(原始.已打開檔案));
        return 新建編號;
    }

    public int 設定關閉啓用側執行操作(int 編號, boolean 值) {
        描述符條目 條目值 = 描述符條目列.get(Integer.valueOf(編號));
        if (條目值 == null) {
            return -9;
        }
        條目值.關閉啓用側執行操作 = 值;
        return 0;
    }

    public int 關閉啓用側執行操作值(int 編號) {
        描述符條目 條目值 = 描述符條目列.get(Integer.valueOf(編號));
        if (條目值 == null) {
            return -9;
        }
        return 條目值.關閉啓用側執行操作 ? 1 : 0;
    }

    public 檔案信息 系統信息(int 編號) {
        if (編號 >= 0 && 編號 <= 2) {
            return new 檔案信息(0, 0020666);
        }
        描述符條目 條目值 = 描述符條目列.get(Integer.valueOf(編號));
        if (條目值 == null) {
            return null;
        }
        return new 檔案信息(條目值.已打開檔案.資料.length, 0100444);
    }

    public void 關閉啓用側執行操作() {
        Integer[] 編號列表 = 描述符條目列.keySet().toArray(new Integer[0]);
        for (Integer 編號 : 編號列表) {
            描述符條目 條目值 = 描述符條目列.get(編號);
            if (條目值 != null && 條目值.關閉啓用側執行操作) {
                關閉(編號.intValue());
            }
        }
    }

    public boolean 是否打開(int 編號) {
        return 描述符條目列.containsKey(Integer.valueOf(編號));
    }

    public 檔案描述符表 克隆值() {
        檔案描述符表 結果 = new 檔案描述符表(檔案系統);
        for (Map.Entry<Integer, 描述符條目> 條目值 : 描述符條目列.entrySet()) {
            條目值.getValue().已打開檔案.引用個數++;
            描述符條目 新建描述符 = new 描述符條目(條目值.getValue().已打開檔案);
            新建描述符.關閉啓用側執行操作 = 條目值.getValue().關閉啓用側執行操作;
            結果.描述符條目列.put(條目值.getKey(), 新建描述符);
        }
        return 結果;
    }

    private int 空索引(int 最小編號) {
        for (int 編號 = Math.max(0, 最小編號); 編號 < 最大描述符; 編號++) {
            if (!描述符條目列.containsKey(Integer.valueOf(編號))) {
                return 編號;
            }
        }
        return -1;
    }
}
