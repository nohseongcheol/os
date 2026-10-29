// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package カナダ.JCanOS.通信網;

import java.util.HashMap;
import java.util.Map;

/** Ethernet、ARP、IPv4、ICMP、UDP、TCP の受信振分けを一か所で管理する。 */
public final class 通信網階層 {
    @FunctionalInterface
    public interface データ処理器 {
        void プロセス値入口(byte[] データ, int 起動処理, int 長さ);
    }

    private final Map<Integer, データ処理器> Ethernet処理器 = new HashMap<Integer, データ処理器>();
    private final Map<Integer, データ処理器> インターネット通信規約処理器 = new HashMap<Integer, データ処理器>();
    private final Map<Integer, データ処理器> 利用者データ単位処理器 = new HashMap<Integer, データ処理器>();
    private final Map<Integer, データ処理器> 伝送状態制御処理器 = new HashMap<Integer, データ処理器>();

    public void Ethernetレジスタ(int 種別値, データ処理器 処理器) {
        Ethernet処理器.put(Integer.valueOf(種別値 & 0xffff), 処理器);
    }

    public void インターネット通信規約レジスタ(int 契約値, データ処理器 処理器) {
        インターネット通信規約処理器.put(Integer.valueOf(契約値 & 0xff), 処理器);
    }

    public void 利用者データ単位レジスタ(int 機器ポート, データ処理器 処理器) {
        利用者データ単位処理器.put(Integer.valueOf(機器ポート & 0xffff), 処理器);
    }

    public void 伝送状態制御レジスタ(int 機器ポート, データ処理器 処理器) {
        伝送状態制御処理器.put(Integer.valueOf(機器ポート & 0xffff), 処理器);
    }

    public boolean Ethernet受取(byte[] 枠組添字) {
        if (!通信網道具.判定Ethernet枠組(枠組添字)) {
            return false;
        }
        int 種別値 = 通信網道具.Ethernet上限側通信規約(枠組添字);
        データ処理器 直接処理器 = Ethernet処理器.get(Integer.valueOf(種別値));
        if (直接処理器 != null) {
            直接処理器.プロセス値入口(枠組添字, 14, 枠組添字.length - 14);
            return true;
        }
        return 種別値 == 0x0800 && インターネットパケット受取(枠組添字, 14);
    }

    private boolean インターネットパケット受取(byte[] データ, int 起動処理) {
        if (!通信網道具.判定IP版4通信規約(データ, 起動処理)) {
            return false;
        }
        int ヘッダー長さ = (データ[起動処理] & 0x0f) * 4;
        int 合計長さ = 通信網道具.大エンディアン短整数(データ, 起動処理 + 2);
        if (合計長さ < ヘッダー長さ || 起動処理 + 合計長さ > データ.length) {
            return false;
        }
        int 契約値 = データ[起動処理 + 9] & 0xff;
        int 内容物開始処理 = 起動処理 + ヘッダー長さ;
        int 内容物長さ = 合計長さ - ヘッダー長さ;
        データ処理器 直接処理器 = インターネット通信規約処理器.get(Integer.valueOf(契約値));
        if (直接処理器 != null) {
            直接処理器.プロセス値入口(データ, 内容物開始処理, 内容物長さ);
            return true;
        }
        if (内容物長さ < 4) {
            return false;
        }
        int 宛先ポート番号 = 通信網道具.大エンディアン短整数(データ, 内容物開始処理 + 2);
        Map<Integer, データ処理器> ポート表 = 契約値 == 17 ? 利用者データ単位処理器 : 契約値 == 6 ? 伝送状態制御処理器 : null;
        if (ポート表 == null) {
            return false;
        }
        データ処理器 ポート処理器 = ポート表.get(Integer.valueOf(宛先ポート番号));
        if (ポート処理器 == null) {
            return false;
        }
        ポート処理器.プロセス値入口(データ, 内容物開始処理, 内容物長さ);
        return true;
    }
}

