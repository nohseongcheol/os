// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package カナダ.JCanOS.ホスト;

import java.util.HashMap;
import java.util.Map;
import カナダ.JCanOS.中核.機器値;

/** 通常の JVM で管理カーネルを決定的に試験するための代用ハードウェア。 */
public final class ホスト機器 implements 機器値 {
    private final Map<Integer, Integer> 機器ポート値 = new HashMap<Integer, Integer>();
    private final StringBuilder 直列履歴記録 = new StringBuilder();

    @Override
    public void 直列出力(String 内容物値) {
        直列履歴記録.append(内容物値);
        System.out.print(内容物値);
    }

    @Override
    public int ポートバイト読取(int 機器ポート番号) {
        Integer 値 = 機器ポート値.get(Integer.valueOf(機器ポート番号));
        return 値 == null ? 0 : 値.intValue();
    }

    @Override
    public void ポートバイト書込(int 機器ポート番号, int 値) {
        機器ポート値.put(Integer.valueOf(機器ポート番号), Integer.valueOf(値 & 0xff));
    }

    @Override
    public void 機械停止CPU() {
        // ホスト試験では次の事象を待たず、ただちに戻る。
    }

    public String 直列履歴記録() {
        return 直列履歴記録.toString();
    }
}

