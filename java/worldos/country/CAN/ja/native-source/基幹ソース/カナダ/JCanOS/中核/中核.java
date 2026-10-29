// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package カナダ.JCanOS.中核;

import カナダ.JCanOS.記憶領域.記憶管理器;
import カナダ.JCanOS.記憶領域.ページ管理器;
import カナダ.JCanOS.入力値.入力管理器;
import カナダ.JCanOS.作業.プロセス値;
import カナダ.JCanOS.作業.割当器;
import カナダ.JCanOS.システム呼出.システム呼出;
import カナダ.JCanOS.ファイルシステム.ファイル記述子表;
import カナダ.JCanOS.ファイルシステム.ファイルシステム;

/** Java 管理カーネルの組立てと起動を担う。 */
public final class 中核 {
    private final 機器値 装置;
    private final 記憶管理器 記憶領域 = new 記憶管理器(32 * 1024 * 1024);
    private final ページ管理器 ページ管理業務 = new ページ管理器();
    private final ファイルシステム ファイルシステム = new ファイルシステム();
    private final 割当器 割当器 = new 割当器(ページ管理業務);
    private final 入力管理器 入力管理業務 = new 入力管理器(256);
    private final プロセス値 先頭位置プロセス;
    private final システム呼出 システム呼出;

    public 中核(機器値 装置) {
        this.装置 = 装置;
        先頭位置プロセス = 割当器.先頭位置プロセス(new ファイル記述子表(ファイルシステム));
        システム呼出 = new システム呼出(ファイルシステム, ページ管理業務, 割当器, 装置, 入力管理業務);
    }

    public void 起動処理() {
        装置.直列出力("=== JCanOS 관리 中核値 ===\n");
    }

    public void 段階実行() {
        装置.機械停止CPU();
    }

    public 記憶管理器 記憶領域() {
        return 記憶領域;
    }

    public ページ管理器 ページ管理業務() {
        return ページ管理業務;
    }

    public ファイルシステム ファイルシステム() {
        return ファイルシステム;
    }

    public 割当器 割当器() {
        return 割当器;
    }

    public 入力管理器 入力管理業務() {
        return 入力管理業務;
    }

    public プロセス値 先頭位置プロセス() {
        return 先頭位置プロセス;
    }

    public システム呼出 システム呼出() {
        return システム呼出;
    }
}
