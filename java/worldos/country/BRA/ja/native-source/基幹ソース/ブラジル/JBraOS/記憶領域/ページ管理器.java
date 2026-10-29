// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ブラジル.JBraOS.記憶領域;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiBページの対応付けと書込み時コピーを提供する。 */
public final class ページ管理器 {
    public static final int ページ容量 = 4096;

    private static final class ページ値 {
        private byte[] データ = new byte[ページ容量];
        private int 参照個数 = 1;
        private boolean 可能判定書込 = true;
        private boolean 有効側書込複写;
    }

    public static final class 番地空間 {
        private final Map<Integer, ページ値> ページ表 = new HashMap<Integer, ページ値>();
    }

    public 番地空間 新規番地空間() {
        return new 番地空間();
    }

    public void 対応表ページ(番地空間 番地領域, int 仮想番地, boolean 可能判定書込) {
        int 番号 = ページ番号(仮想番地);
        ページ値 新規ページ = new ページ値();
        新規ページ.可能判定書込 = 可能判定書込;
        番地領域.ページ表.put(Integer.valueOf(番号), 新規ページ);
    }

    public 番地空間 複製処理複写有効側書込(番地空間 原本) {
        番地空間 複製済み値 = new 番地空間();
        for (Map.Entry<Integer, ページ値> 入口値 : 原本.ページ表.entrySet()) {
            ページ値 共有ページ = 入口値.getValue();
            共有ページ.参照個数++;
            if (共有ページ.可能判定書込) {
                共有ページ.可能判定書込 = false;
                共有ページ.有効側書込複写 = true;
            }
            複製済み値.ページ表.put(入口値.getKey(), 共有ページ);
        }
        return 複製済み値;
    }

    public byte バイト値読取(番地空間 番地領域, int 仮想番地) {
        ページ値 対象値 = ページ探索(番地領域, 仮想番地);
        return 対象値.データ[Math.floorMod(仮想番地, ページ容量)];
    }

    public void バイト値書込(番地空間 番地領域, int 仮想番地, byte 値) {
        int 番号 = ページ番号(仮想番地);
        ページ値 対象値 = ページ探索(番地領域, 仮想番地);
        if (!対象値.可能判定書込) {
            if (!対象値.有効側書込複写) {
                throw new IllegalStateException("読取 전용 쪽입니다.");
            }
            対象値 = 非公開ページ作成(番地領域, 番号, 対象値);
        }
        対象値.データ[Math.floorMod(仮想番地, ページ容量)] = 値;
    }

    public void 非公開範囲書込(番地空間 番地領域, int 番地開始処理, int 容量) {
        if (容量 < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int 終端位置番地 = Math.addExact(番地開始処理, 容量);
        for (int 番地 = 番地開始処理; 番地 < 終端位置番地; 番地 = (ページ番号(番地) + 1) * ページ容量) {
            int 番号 = ページ番号(番地);
            ページ値 対象値 = ページ探索(番地領域, 番地);
            if (対象値.有効側書込複写) {
                非公開ページ作成(番地領域, 番号, 対象値);
            } else {
                対象値.可能判定書込 = true;
            }
        }
    }

    public void 範囲書込(番地空間 番地領域, int 番地開始処理, byte[] データ) {
        for (int 番号 = 0; 番号 < データ.length; 番号++) {
            バイト値書込(番地領域, 番地開始処理 + 番号, データ[番号]);
        }
    }

    private ページ値 非公開ページ作成(番地空間 番地領域, int 番号, ページ値 共有ページ) {
        ページ値 非公開ページ = new ページ値();
        非公開ページ.データ = Arrays.copyOf(共有ページ.データ, 共有ページ.データ.length);
        非公開ページ.可能判定書込 = true;
        非公開ページ.有効側書込複写 = false;
        共有ページ.参照個数--;
        番地領域.ページ表.put(Integer.valueOf(番号), 非公開ページ);
        return 非公開ページ;
    }

    private ページ値 ページ探索(番地空間 番地領域, int 番地) {
        ページ値 対象値 = 番地領域.ページ表.get(Integer.valueOf(ページ番号(番地)));
        if (対象値 == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return 対象値;
    }

    private int ページ番号(int 番地) {
        if (番地 < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return 番地 / ページ容量;
    }
}

