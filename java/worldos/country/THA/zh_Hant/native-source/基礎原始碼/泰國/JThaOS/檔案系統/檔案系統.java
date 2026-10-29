// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 泰國.JThaOS.檔案系統;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** 對應 engos FAT 讀取層的唯讀檔案儲存管理模型。 */
public final class 檔案系統 {
    static final class 已打開檔案 {
        final byte[] 資料;
        int 位置;
        int 引用個數 = 1;

        已打開檔案(byte[] 資料) {
            this.資料 = 資料;
        }
    }

    private final Map<String, byte[]> 檔案條目列 = new LinkedHashMap<String, byte[]>();

    public void 追加檔案(String 名稱, byte[] 資料) {
        檔案條目列.put(規範形式名稱(名稱), Arrays.copyOf(資料, 資料.length));
    }

    已打開檔案 打開(String 名稱) {
        byte[] 資料 = 檔案條目列.get(規範形式名稱(名稱));
        if (資料 == null) {
            return null;
        }
        return new 已打開檔案(資料);
    }

    public boolean 存在判斷值(String 名稱) {
        return 檔案條目列.containsKey(規範形式名稱(名稱));
    }

    public 檔案信息 系統信息(String 名稱) {
        byte[] 資料 = 檔案條目列.get(規範形式名稱(名稱));
        if (資料 == null) {
            return null;
        }
        return new 檔案信息(資料.length, 0100444);
    }

    private String 規範形式名稱(String 名稱) {
        if (名稱 == null) {
            throw new NullPointerException("檔案 이름이 없습니다.");
        }
        String 結果 = 名稱.startsWith("/") ? 名稱.substring(1) : 名稱;
        return 結果.toUpperCase(Locale.ROOT);
    }
}
