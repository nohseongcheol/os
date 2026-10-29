// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中國澳門特別行政區.JMacOS.存儲裝置設備;

import java.util.Arrays;

/** 與 ATA 28 位元命令層一致的 512 位元組邏輯磁區裝置。 */
public final class 高級技術附件 {
    public static final int 區段大小 = 512;
    private final byte[] 資料;
    private final boolean 讀取僅用值;

    public 高級技術附件(int 區段個數, boolean 讀取僅用值) {
        if (區段個數 <= 0) {
            throw new IllegalArgumentException("區段值 수가 올바르지 않습니다.");
        }
        資料 = new byte[Math.multiplyExact(區段個數, 區段大小)];
        this.讀取僅用值 = 讀取僅用值;
    }

    public int 區段個數() {
        return 資料.length / 區段大小;
    }

    public void 讀取(int 區段索引, byte[] 接收目的地址) {
        檢查範圍(區段索引, 接收目的地址);
        System.arraycopy(資料, 區段索引 * 區段大小, 接收目的地址, 0, 區段大小);
    }

    public void 寫入(int 區段索引, byte[] 資料目標側寫入) {
        if (讀取僅用值) {
            throw new IllegalStateException("讀取 전용 장치입니다.");
        }
        檢查範圍(區段索引, 資料目標側寫入);
        System.arraycopy(資料目標側寫入, 0, 資料, 區段索引 * 區段大小, 區段大小);
    }

    public void 擦除條目() {
        if (讀取僅用值) {
            throw new IllegalStateException("讀取 전용 장치입니다.");
        }
        Arrays.fill(資料, (byte) 0);
    }

    private void 檢查範圍(int 區段索引, byte[] 臨時空間) {
        if (區段索引 < 0 || 區段索引 >= 區段個數() || 臨時空間.length < 區段大小) {
            throw new IllegalArgumentException("ATA 區段值 범위가 올바르지 않습니다.");
        }
    }
}

