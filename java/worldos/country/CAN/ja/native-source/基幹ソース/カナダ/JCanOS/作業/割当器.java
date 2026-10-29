// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package カナダ.JCanOS.作業;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import カナダ.JCanOS.記憶領域.ページ管理器;
import カナダ.JCanOS.ファイルシステム.ファイル記述子表;

/** プロセス識別子とラウンドロビンの実行待ち行列を管理する。 */
public final class 割当器 {
    private final ページ管理器 ページ管理業務;
    private final Map<Integer, プロセス値> プロセス一覧 = new HashMap<Integer, プロセス値>();
    private final Queue<プロセス値> 準備済み待ち行列 = new ArrayDeque<プロセス値>();
    private int 次回識別子 = 1;

    public 割当器(ページ管理器 ページ管理業務) {
        this.ページ管理業務 = ページ管理業務;
    }

    public プロセス値 先頭位置プロセス(ファイル記述子表 ファイル記述子) {
        プロセス値 新規プロセス = new プロセス値(識別子確保(), 0, ページ管理業務.新規番地空間(), ファイル記述子);
        プロセス一覧.put(Integer.valueOf(新規プロセス.識別子値()), 新規プロセス);
        準備済み待ち行列.offer(新規プロセス);
        return 新規プロセス;
    }

    public プロセス値 複製処理値(プロセス値 親値) {
        プロセス値 子値 = new プロセス値(
                識別子確保(),
                親値.識別子値(),
                ページ管理業務.複製処理複写有効側書込(親値.番地空間()),
                親値.ファイル記述子().複製処理値());
        子値.プログラム中断設定(親値.プログラム中断());
        プロセス一覧.put(Integer.valueOf(子値.識別子値()), 子値);
        準備済み待ち行列.offer(子値);
        return 子値;
    }

    public プロセス値 次回プロセス() {
        int 個数検査 = 準備済み待ち行列.size();
        for (int 番号 = 0; 番号 < 個数検査; 番号++) {
            プロセス値 次回項目 = 準備済み待ち行列.poll();
            if (次回項目 != null && (次回項目.状況値() == プロセス状況.用意 || 次回項目.状況値() == プロセス状況.命令実行)) {
                次回項目.状況設定(プロセス状況.命令実行);
                準備済み待ち行列.offer(次回項目);
                return 次回項目;
            }
        }
        return null;
    }

    public int 対象子待合(プロセス値 親値, int 子識別子, boolean 非該当閉塞) {
        for (プロセス値 候補 : プロセス一覧.values()) {
            if (候補.親識別子() != 親値.識別子値()) {
                continue;
            }
            if (子識別子 > 0 && 候補.識別子値() != 子識別子) {
                continue;
            }
            if (候補.状況値() == プロセス状況.終了点プログラム) {
                int 結果 = (候補.終了点コード() & 0xff) << 8;
                プロセス一覧.remove(Integer.valueOf(候補.識別子値()));
                return 結果;
            }
            return 非該当閉塞 ? 0 : -11;
        }
        return -10;
    }

    public プロセス値 プロセス探索(int 識別子値) {
        return プロセス一覧.get(Integer.valueOf(識別子値));
    }

    private int 識別子確保() {
        return 次回識別子++;
    }
}
