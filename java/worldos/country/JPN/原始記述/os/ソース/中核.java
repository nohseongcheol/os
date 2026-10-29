// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 実際の起動後に呼ばれる Java の入口。JVM やホスト OS に依存しない。 */
public final class 中核 {
    static int 合計値(int 終端) {
        int 総和値 = 0;
        for (int 番号 = 1; 番号 <= 終端; 番号++) 総和値 += 番号;
        return 総和値;
    }

    static boolean 試験() {
        int[] 値一覧 = new int[4];
        値一覧[2] = 合計値(10);
        int 負数値 = -7;
        int 最小値 = 0x80000000;
        int 除算結果 = -1;
        int 番号 = 記憶領域.記憶装置確保();
        boolean 通過値 = 値一覧[0] == 0 && 値一覧[2] == 55 && 値一覧.length == 4
            && 負数値 / 3 == -2 && 負数値 % 3 == -1 && 最小値 / 除算結果 == 最小値
            && 最小値 % 除算結果 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && 番号 >= 0 && 記憶領域.復帰結果(番号) && !記憶領域.復帰結果(番号);
        文字端末.書込(通過値 ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return 通過値;
    }

    public static void 起動処理() {
        文字端末.用意();
        文字端末.書込("JKOROS NATIVE JAVA\n");
        文字端末.書込("Java 기계어 中核値 起動処理\n");
        if (装置.起動標識() != 0x2badb002) {
            文字端末.書込("BAD MULTIBOOT MAGIC\n");
            装置.機械停止実行状態();
        }
        if (!試験()) 装置.機械停止実行状態();
        if (記憶領域.上限側記憶容量() < 15360) {
            文字端末.書込("At least 16 MiB RAM required\n");
            装置.機械停止実行状態();
        }
        装置.利用者プログラム用意();
        文字端末.書込("USER ELF: ring 3 / paging / int 0x80\n");
        通信装置駆動器.用意();
        通信網.清掃プロセス();
        主記憶ファイル体系.用意();
        ファイル永続化.用意();
        命令解釈器.起動処理();
    }
}
