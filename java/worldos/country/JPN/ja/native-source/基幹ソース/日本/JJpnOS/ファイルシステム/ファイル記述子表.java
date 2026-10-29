// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本.JJpnOS.ファイルシステム;

import java.util.HashMap;
import java.util.Map;

/** プロセスごとに独立した記述子と、共有可能な開いたファイルの記述情報を保持する。 */
public final class ファイル記述子表 {
    private static final int 最大記述子 = 32;

    private static final class 記述子入口 {
        private final ファイルシステム.開放済みファイル 開放済みファイル;
        private boolean 有効側実行処理閉鎖;

        記述子入口(ファイルシステム.開放済みファイル 開放済みファイル) {
            this.開放済みファイル = 開放済みファイル;
        }
    }

    private final ファイルシステム ファイルシステム;
    private final Map<Integer, 記述子入口> 記述子登録項目一覧 = new HashMap<Integer, 記述子入口>();

    public ファイル記述子表(ファイルシステム ファイルシステム) {
        this.ファイルシステム = ファイルシステム;
    }

    public int 開放(String 名前) {
        ファイルシステム.開放済みファイル 開放済みファイル = ファイルシステム.開放(名前);
        if (開放済みファイル == null) {
            return -2;
        }
        int 番号 = 空添字(3);
        if (番号 < 0) {
            return -24;
        }
        記述子登録項目一覧.put(Integer.valueOf(番号), new 記述子入口(開放済みファイル));
        return 番号;
    }

    public int 読取(int 番号, byte[] 宛先受取, int 容量) {
        記述子入口 入口値 = 記述子登録項目一覧.get(Integer.valueOf(番号));
        if (入口値 == null) {
            return -9;
        }
        if (容量 < 0 || 容量 > 宛先受取.length) {
            return -22;
        }
        int 剰余データ = 入口値.開放済みファイル.データ.length - 入口値.開放済みファイル.位置;
        int 容量読取 = Math.min(容量, Math.max(剰余データ, 0));
        System.arraycopy(入口値.開放済みファイル.データ, 入口値.開放済みファイル.位置, 宛先受取, 0, 容量読取);
        入口値.開放済みファイル.位置 += 容量読取;
        return 容量読取;
    }

    public int 移動位置(int 番号, int 距離値, int 計画根) {
        記述子入口 入口値 = 記述子登録項目一覧.get(Integer.valueOf(番号));
        if (入口値 == null) {
            return -9;
        }
        int 背景値;
        if (計画根 == 0) {
            背景値 = 0;
        } else if (計画根 == 1) {
            背景値 = 入口値.開放済みファイル.位置;
        } else if (計画根 == 2) {
            背景値 = 入口値.開放済みファイル.データ.length;
        } else {
            return -22;
        }
        int 新規位置 = 背景値 + 距離値;
        if (新規位置 < 0) {
            return -22;
        }
        入口値.開放済みファイル.位置 = 新規位置;
        return 新規位置;
    }

    public int 閉鎖(int 番号) {
        記述子入口 入口値 = 記述子登録項目一覧.remove(Integer.valueOf(番号));
        if (入口値 == null) {
            return -9;
        }
        入口値.開放済みファイル.参照個数--;
        return 0;
    }

    public int 複製済み記述子(int 番号, int 最小番号) {
        記述子入口 入口値 = 記述子登録項目一覧.get(Integer.valueOf(番号));
        if (入口値 == null) {
            return -9;
        }
        int 新規番号 = 空添字(最小番号);
        if (新規番号 < 0) {
            return -24;
        }
        入口値.開放済みファイル.参照個数++;
        記述子登録項目一覧.put(Integer.valueOf(新規番号), new 記述子入口(入口値.開放済みファイル));
        return 新規番号;
    }

    public int 複製位置(int 番号, int 新規番号) {
        if (番号 == 新規番号) {
            return 記述子登録項目一覧.containsKey(Integer.valueOf(番号)) ? 番号 : -9;
        }
        if (新規番号 < 0 || 新規番号 >= 最大記述子) {
            return -9;
        }
        記述子入口 原本 = 記述子登録項目一覧.get(Integer.valueOf(番号));
        if (原本 == null) {
            return -9;
        }
        if (記述子登録項目一覧.containsKey(Integer.valueOf(新規番号))) {
            閉鎖(新規番号);
        }
        原本.開放済みファイル.参照個数++;
        記述子登録項目一覧.put(Integer.valueOf(新規番号), new 記述子入口(原本.開放済みファイル));
        return 新規番号;
    }

    public int 閉鎖有効側実行処理設定(int 番号, boolean 値) {
        記述子入口 入口値 = 記述子登録項目一覧.get(Integer.valueOf(番号));
        if (入口値 == null) {
            return -9;
        }
        入口値.有効側実行処理閉鎖 = 値;
        return 0;
    }

    public int 有効側実行処理値閉鎖(int 番号) {
        記述子入口 入口値 = 記述子登録項目一覧.get(Integer.valueOf(番号));
        if (入口値 == null) {
            return -9;
        }
        return 入口値.有効側実行処理閉鎖 ? 1 : 0;
    }

    public ファイル情報 システム情報(int 番号) {
        if (番号 >= 0 && 番号 <= 2) {
            return new ファイル情報(0, 0020666);
        }
        記述子入口 入口値 = 記述子登録項目一覧.get(Integer.valueOf(番号));
        if (入口値 == null) {
            return null;
        }
        return new ファイル情報(入口値.開放済みファイル.データ.length, 0100444);
    }

    public void 有効側実行処理閉鎖() {
        Integer[] 番号一覧 = 記述子登録項目一覧.keySet().toArray(new Integer[0]);
        for (Integer 番号 : 番号一覧) {
            記述子入口 入口値 = 記述子登録項目一覧.get(番号);
            if (入口値 != null && 入口値.有効側実行処理閉鎖) {
                閉鎖(番号.intValue());
            }
        }
    }

    public boolean 判定開放(int 番号) {
        return 記述子登録項目一覧.containsKey(Integer.valueOf(番号));
    }

    public ファイル記述子表 複製処理値() {
        ファイル記述子表 結果 = new ファイル記述子表(ファイルシステム);
        for (Map.Entry<Integer, 記述子入口> 入口値 : 記述子登録項目一覧.entrySet()) {
            入口値.getValue().開放済みファイル.参照個数++;
            記述子入口 新規記述子 = new 記述子入口(入口値.getValue().開放済みファイル);
            新規記述子.有効側実行処理閉鎖 = 入口値.getValue().有効側実行処理閉鎖;
            結果.記述子登録項目一覧.put(入口値.getKey(), 新規記述子);
        }
        return 結果;
    }

    private int 空添字(int 最小番号) {
        for (int 番号 = Math.max(0, 最小番号); 番号 < 最大記述子; 番号++) {
            if (!記述子登録項目一覧.containsKey(Integer.valueOf(番号))) {
                return 番号;
            }
        }
        return -1;
    }
}
