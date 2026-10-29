// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本.JJpnOS.記憶装置装置;

import java.util.Arrays;

/** ATA 28ビット命令層と同じ512バイト論理セクター装置。 */
public final class 高度技術添付 {
    public static final int 区画容量 = 512;
    private final byte[] データ;
    private final boolean 専用値読取;

    public 高度技術添付(int 区画個数, boolean 専用値読取) {
        if (区画個数 <= 0) {
            throw new IllegalArgumentException("区画値 수가 올바르지 않습니다.");
        }
        データ = new byte[Math.multiplyExact(区画個数, 区画容量)];
        this.専用値読取 = 専用値読取;
    }

    public int 区画個数() {
        return データ.length / 区画容量;
    }

    public void 読取(int 区画添字, byte[] 宛先受取) {
        範囲検査(区画添字, 宛先受取);
        System.arraycopy(データ, 区画添字 * 区画容量, 宛先受取, 0, 区画容量);
    }

    public void 書込(int 区画添字, byte[] データ到達先書込) {
        if (専用値読取) {
            throw new IllegalStateException("読取 전용 장치입니다.");
        }
        範囲検査(区画添字, データ到達先書込);
        System.arraycopy(データ到達先書込, 0, データ, 区画添字 * 区画容量, 区画容量);
    }

    public void 入口消去処理() {
        if (専用値読取) {
            throw new IllegalStateException("読取 전용 장치입니다.");
        }
        Arrays.fill(データ, (byte) 0);
    }

    private void 範囲検査(int 区画添字, byte[] 一時空間) {
        if (区画添字 < 0 || 区画添字 >= 区画個数() || 一時空間.length < 区画容量) {
            throw new IllegalArgumentException("ATA 区画値 범위가 올바르지 않습니다.");
        }
    }
}

