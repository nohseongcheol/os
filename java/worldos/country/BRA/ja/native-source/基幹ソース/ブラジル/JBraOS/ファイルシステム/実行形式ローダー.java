// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ブラジル.JBraOS.ファイルシステム;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** リトルエンディアン ELF32 実行ファイルのヘッダーと読込み区画を検証する。 */
public final class 実行形式ローダー {
    public static final class 区画値 {
        private final int 種別値;
        private final int フラグ値;
        private final int 番地;
        private final int ファイル位置;
        private final int 容量;

        区画値(int 種別値, int フラグ値, int 番地, int ファイル位置, int 容量) {
            this.種別値 = 種別値;
            this.フラグ値 = フラグ値;
            this.番地 = 番地;
            this.ファイル位置 = ファイル位置;
            this.容量 = 容量;
        }

        public int 種別値() {
            return 種別値;
        }

        public int フラグ値() {
            return フラグ値;
        }

        public int 番地() {
            return 番地;
        }

        public int ファイル位置() {
            return ファイル位置;
        }

        public int 容量() {
            return 容量;
        }
    }

    public static final class イメージ {
        private final int 番地開始処理;
        private final List<区画値> 区画一覧一覧;

        イメージ(int 番地開始処理, List<区画値> 区画一覧一覧) {
            this.番地開始処理 = 番地開始処理;
            this.区画一覧一覧 = Collections.unmodifiableList(区画一覧一覧);
        }

        public int 番地開始処理() {
            return 番地開始処理;
        }

        public List<区画値> 区画一覧一覧() {
            return 区画一覧一覧;
        }
    }

    public イメージ 検査項目(byte[] データ) {
        if (データ == null || データ.length < 52
                || データ[0] != 0x7f || データ[1] != 'E' || データ[2] != 'L' || データ[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (データ[4] != 1 || データ[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int 番地開始処理 = 整数値解析(データ, 24);
        int 区画表位置 = 整数値解析(データ, 32);
        int 区画入口容量 = 短整数整数値読取(データ, 46);
        int 区画個数 = 短整数整数値読取(データ, 48);
        if (区画入口容量 < 40 || 区画表位置 < 0
                || (long) 区画表位置 + (long) 区画入口容量 * 区画個数 > データ.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<区画値> 区画一覧一覧 = new ArrayList<区画値>();
        for (int 番号 = 0; 番号 < 区画個数; 番号++) {
            int 位置 = 区画表位置 + 番号 * 区画入口容量;
            int 種別値 = 整数値解析(データ, 位置 + 4);
            int フラグ値 = 整数値解析(データ, 位置 + 8);
            int 番地 = 整数値解析(データ, 位置 + 12);
            int ファイル位置 = 整数値解析(データ, 位置 + 16);
            int 容量 = 整数値解析(データ, 位置 + 20);
            if (容量 < 0 || (種別値 != 8 && ((long) ファイル位置 + 容量 > データ.length || ファイル位置 < 0))) {
                throw new IllegalArgumentException("ELF 区画値 データ 범위가 올바르지 않습니다.");
            }
            区画一覧一覧.add(new 区画値(種別値, フラグ値, 番地, ファイル位置, 容量));
        }
        return new イメージ(番地開始処理, 区画一覧一覧);
    }

    private int 整数値解析(byte[] データ, int 位置) {
        if (位置 < 0 || 位置 > データ.length - 4) {
            throw new IllegalArgumentException("ELF 整数値 범위를 벗어났습니다.");
        }
        return (データ[位置] & 0xff)
                | ((データ[位置 + 1] & 0xff) << 8)
                | ((データ[位置 + 2] & 0xff) << 16)
                | ((データ[位置 + 3] & 0xff) << 24);
    }

    private int 短整数整数値読取(byte[] データ, int 位置) {
        if (位置 < 0 || 位置 > データ.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 整数値 범위를 벗어났습니다.");
        }
        return (データ[位置] & 0xff) | ((データ[位置 + 1] & 0xff) << 8);
    }
}
