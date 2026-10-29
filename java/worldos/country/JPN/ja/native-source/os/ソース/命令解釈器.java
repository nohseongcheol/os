// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ディスクへ書き込まない小さな直列通信・PS2 命令解釈器。 */
public final class 命令解釈器 {
    static int[] 入力値 = new int[128];
    static int 長さ = 0;
    static boolean 復帰到達先前回行 = false;
    static boolean 行桁あふれ = false;

    static boolean 命令(String 名前) {
        if (長さ < 名前.length()) return false;
        for (int 番号 = 0; 番号 < 名前.length(); 番号++)
            if (入力値[番号] != 名前.charAt(番号)) return false;
        return 長さ == 名前.length() || 入力値[名前.length()] == ' ';
    }

    static void ヘルプ表示() {
        文字端末.書込("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        文字端末.書込("apps | run NAME [ARGS] | net\n");
        文字端末.書込("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        文字端末.書込("sync (연결된 JKSTORE1 格納値 장치에 ファイル 보존)\n");
    }

    static void プロセス値入口() {
        if (長さ == 0) return;
        if (命令("help")) ヘルプ表示();
        else if (命令("sync")) {
            int 結果 = ファイル永続化.同期化();
            文字端末.書込("Sync: "); 文字端末.番号書込(結果); 文字端末.文字(10);
        }
        else if (命令("ls")) 主記憶ファイル体系.入口一覧();
        else if (命令("edit")) 主記憶ファイル体系.命令(入力値, 4, 長さ, 0);
        else if (命令("cat")) 主記憶ファイル体系.命令(入力値, 3, 長さ, 1);
        else if (命令("rm")) 主記憶ファイル体系.命令(入力値, 2, 長さ, 2);
        else if (命令("java") || 命令("javac")) {
            int 結果 = 実行管理.命令実行(入力値, 0, 長さ);
            文字端末.書込("Exit: "); 文字端末.番号書込(結果); 文字端末.文字(10);
        }
        else if (命令("apps")) 実行管理.入口一覧();
        else if (命令("net")) 通信網.状況値();
        else if (命令("run")) {
            int 結果 = 実行管理.命令実行(入力値, 3, 長さ);
            文字端末.書込("Exit: "); 文字端末.番号書込(結果); 文字端末.書込("\n");
        } else if (命令("info")) {
            文字端末.書込("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (命令("mem")) {
            文字端末.書込("上限側側面 記憶 番地領域(KiB): "); 文字端末.番号書込(記憶領域.上限側記憶容量());
            文字端末.書込("\n배열 동적 記憶 番地領域(バイト値): "); 文字端末.番号書込(装置.配列使用量());
            文字端末.書込(" / 262144\n작업 番地領域 区画値: "); 文字端末.番号書込(記憶領域.使用済み入口個数());
            文字端末.書込(" / 8 (각 4096바이트)\n");
        } else if (命令("alloc")) {
            int 番号 = 記憶領域.記憶装置確保();
            文字端末.書込("区画値 番号: "); 文字端末.番号書込(番号); 文字端末.書込("\n");
        } else if (命令("free")) {
            if (長さ == 6 && 入力値[4] == ' ' && 入力値[5] >= '0' && 入力値[5] <= '7') {
                文字端末.書込(記憶領域.復帰結果(入力値[5] - '0') ? "반환됨\n" : "할당되지 않은 区画値\n");
            } else 文字端末.書込("사용법: free 0..7\n");
        } else if (命令("echo")) {
            for (int 番号 = 5; 番号 < 長さ; 番号++) 文字端末.文字(入力値[番号]);
            文字端末.文字(10);
        } else if (命令("clear")) 文字端末.入口消去処理();
        else if (命令("test")) 中核.試験();
        else if (命令("halt")) {
            文字端末.書込("HALTED\n");
            装置.機械停止実行状態();
        } else 文字端末.書込("알 数 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 論理積書込受理(int 値) {
        if (値 == 10 && 復帰到達先前回行) { 復帰到達先前回行 = false; return; }
        復帰到達先前回行 = 値 == 13;
        if (値 == 10 || 値 == 13) {
            文字端末.文字(10);
            if (主記憶ファイル体系.判定編集中) 主記憶ファイル体系.編集済み行(入力値, 長さ, 行桁あふれ);
            else プロセス値入口();
            長さ = 0;
            行桁あふれ = false;
            文字端末.書込(主記憶ファイル体系.判定編集中 ? "...> " : "jkoros> ");
        } else if (値 == 8 || 値 == 127) {
            if (長さ > 0) {
                長さ--;
                文字端末.直列バイト(8); 文字端末.直列バイト(32); 文字端末.直列バイト(8);
                文字端末.画面文字(8);
            }
        } else if (値 >= 32 && 値 < 127 && 長さ < 入力値.length) {
            入力値[長さ++] = 値;
            文字端末.文字(値);
        } else if (値 >= 32 && 値 < 127) 行桁あふれ = true;
    }

    static void 起動処理() {
        ヘルプ表示();
        文字端末.書込("READY\njkoros> ");
        while (true) {
            int 値 = 文字端末.直列読取();
            if (値 < 0) 値 = キーボード.読取();
            if (値 >= 0) 論理積書込受理(値);
            else { 通信網.検証(); 装置.短時間だけ実行権譲渡(); }
        }
    }
}
