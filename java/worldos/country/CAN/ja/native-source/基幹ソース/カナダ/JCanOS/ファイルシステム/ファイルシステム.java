// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package カナダ.JCanOS.ファイルシステム;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 読取り層に対応する、読取り専用ファイル格納域の管理モデル。 */
public final class ファイルシステム {
    static final class 開放済みファイル {
        final byte[] データ;
        int 位置;
        int 参照個数 = 1;

        開放済みファイル(byte[] データ) {
            this.データ = データ;
        }
    }

    private final Map<String, byte[]> ファイル登録項目一覧 = new LinkedHashMap<String, byte[]>();

    public void ファイル追記(String 名前, byte[] データ) {
        ファイル登録項目一覧.put(正規名前(名前), Arrays.copyOf(データ, データ.length));
    }

    開放済みファイル 開放(String 名前) {
        byte[] データ = ファイル登録項目一覧.get(正規名前(名前));
        if (データ == null) {
            return null;
        }
        return new 開放済みファイル(データ);
    }

    public boolean 存在判定値(String 名前) {
        return ファイル登録項目一覧.containsKey(正規名前(名前));
    }

    public ファイル情報 システム情報(String 名前) {
        byte[] データ = ファイル登録項目一覧.get(正規名前(名前));
        if (データ == null) {
            return null;
        }
        return new ファイル情報(データ.length, 0100444);
    }

    private String 正規名前(String 名前) {
        if (名前 == null) {
            throw new NullPointerException("ファイル 이름이 없습니다.");
        }
        String 結果 = 名前.startsWith("/") ? 名前.substring(1) : 名前;
        return 結果.toUpperCase(Locale.ROOT);
    }
}
