// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3 で動く制限付き JVM。実行中にファイル、スタック、参照、分岐の境界を検査する。 */
public final class Java仮想機械 {
    static int[] ファイル = new int[16384], ファイル名前本文 = new int[64];
    static int[] 定数印札 = new int[512], 定数先頭位置値 = new int[512], 定数第二値 = new int[512], 文字列参照 = new int[512];
    static int[] メソッド名前本文 = new int[32], メソッド型 = new int[32], メソッドアクセス = new int[32];
    static int[] メソッド開始処理 = new int[32], メソッド終端位置 = new int[32], メソッドスタック = new int[32], メソッド局所変数一覧 = new int[32];
    static int[] メソッド引数個数 = new int[32], メソッド引数型 = new int[512], メソッド復帰 = new int[32];
    static int[] 境界位置値 = new int[16384];
    static int[] 局所値 = new int[4096], 局所型 = new int[4096], 被演算子スタック値 = new int[4096], 被演算子スタック型 = new int[4096];
    static int[] 枠組メソッド = new int[32], 枠組位置 = new int[32], 枠組スタック = new int[32];
    static int[] ヒープ値 = new int[8192];
    static int 容量, 位置読取, 定数個数, メソッド個数, クラス名前, 枠組添字 = -1, ヒープ終端位置位置 = 1, 復帰型;
    static boolean エラー;

    static void 失敗値(String 語本文) {
        if (!エラー) { 利用者.書込("JVM error: "); 利用者.書込(語本文); 利用者.文字値書込(10); }
        エラー = true;
    }
    static boolean 切抜き(int 起動処理, int 長さ) { return 起動処理 >= 0 && 長さ >= 0 && 起動処理 <= 容量 - 長さ; }
    static int バイト値() {
        if (!切抜き(位置読取, 1)) { 失敗値("truncated class file"); return 0; }
        return ファイル[位置読取++];
    }
    static int 短整数値() { return バイト値() << 8 | バイト値(); }
    static int 整数値() { return 短整数値() << 16 | 短整数値(); }
    static void バイト列読飛ばし(int 長さ) { if (!切抜き(位置読取, 長さ)) 失敗値("invalid attribute size"); else 位置読取 += 長さ; }
    static boolean 定数検査(int 数, int 種別値) {
        if (数 <= 0 || 数 >= 定数個数 || 定数印札[数] != 種別値) { 失敗値("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 本文範囲(int 起動処理, int 長さ, String 語本文) {
        if (!切抜き(起動処理, 長さ) || 長さ != 語本文.length()) return false;
        for (int 数 = 0; 数 < 長さ; 数++) if (ファイル[起動処理 + 数] != 語本文.charAt(数)) return false;
        return true;
    }
    static boolean 語本文(int 定数値, String 語本文) { return 定数検査(定数値, 1) && 本文範囲(定数先頭位置値[定数値], 定数第二値[定数値], 語本文); }
    static boolean 照合中語(int 先頭位置被演算子, int 第二被演算子) {
        if (!定数検査(先頭位置被演算子, 1) || !定数検査(第二被演算子, 1) || 定数第二値[先頭位置被演算子] != 定数第二値[第二被演算子]) return false;
        for (int 数 = 0; 数 < 定数第二値[先頭位置被演算子]; 数++) if (ファイル[定数先頭位置値[先頭位置被演算子] + 数] != ファイル[定数先頭位置値[第二被演算子] + 数]) return false;
        return true;
    }
    static int クラス名前本文(int 数) { return 定数検査(数, 7) && 定数検査(定数先頭位置値[数], 1) ? 定数先頭位置値[数] : 0; }
    static int 参照名前(int 数) { return 定数検査(数, 12) && 定数検査(定数先頭位置値[数], 1) ? 定数先頭位置値[数] : 0; }
    static int 参照型(int 数) { return 定数検査(数, 12) && 定数検査(定数第二値[数], 1) ? 定数第二値[数] : 0; }
    static int 記述子型(int 終端, boolean 空型) {
        if (位置読取 >= 終端) { 失敗値("invalid descriptor"); return 0; }
        int 値 = バイト値();
        if (値 == 'V' && 空型) return 0;
        if (値 == 'I' || 値 == 'B' || 値 == 'C' || 値 == 'S' || 値 == 'Z') return 1;
        if (値 == '[') { 記述子型(終端, false); return 2; }
        if (値 == 'L') {
            int 起動処理 = 位置読取;
            while (位置読取 < 終端 && ファイル[位置読取] != ';') 位置読取++;
            if (位置読取 == 終端 || 位置読取 == 起動処理) 失敗値("invalid reference descriptor");
            else 位置読取++;
            return 2;
        }
        失敗値("unsupported descriptor type"); return 0;
    }
    static void 記述子読取(int 関数) {
        int 前回項目 = 位置読取, 数 = メソッド型[関数];
        if (!定数検査(数, 1)) return;
        位置読取 = 定数先頭位置値[数]; int 終端 = 位置読取 + 定数第二値[数];
        if (バイト値() != '(') 失敗値("invalid method descriptor");
        int 項目個数 = 0;
        while (!エラー && 位置読取 < 終端 && ファイル[位置読取] != ')') {
            if (項目個数 == 16) { 失敗値("too many method arguments"); break; }
            メソッド引数型[関数 * 16 + 項目個数++] = 記述子型(終端, false);
        }
        if (位置読取 >= 終端 || バイト値() != ')') 失敗値("invalid method descriptor");
        メソッド復帰[関数] = 記述子型(終端, true); メソッド引数個数[関数] = 項目個数;
        if (位置読取 != 終端) 失敗値("invalid method descriptor");
        位置読取 = 前回項目;
    }
    static void 属性読飛ばし() {
        int 項目個数 = 短整数値();
        for (int 数 = 0; 数 < 項目個数 && !エラー; 数++) { 定数検査(短整数値(), 1); バイト列読飛ばし(整数値()); }
    }
    static int 命令長さ(int 値) {
        if (値 == 16 || 値 == 18 || 値 == 21 || 値 == 25 || 値 == 54 || 値 == 58 || 値 == 188) return 2;
        if (値 == 17 || 値 == 19 || 値 == 132 || 値 >= 153 && 値 <= 167
            || 値 >= 178 && 値 <= 184 || 値 == 187 || 値 == 189 || 値 == 192 || 値 == 198 || 値 == 199) return 3;
        if (値 >= 0 && 値 <= 8 || 値 >= 26 && 値 <= 29 || 値 >= 42 && 値 <= 46 || 値 == 50
            || 値 >= 59 && 値 <= 62 || 値 >= 75 && 値 <= 79 || 値 == 83 || 値 == 87 || 値 == 89 || 値 == 95
            || 値 == 96 || 値 == 100 || 値 == 104 || 値 == 108 || 値 == 112 || 値 == 116
            || 値 == 120 || 値 == 122 || 値 == 124 || 値 == 126 || 値 == 128 || 値 == 130
            || 値 >= 145 && 値 <= 147 || 値 == 172 || 値 == 176 || 値 == 177 || 値 == 190) return 1;
        return 0;
    }
    static void クラス読取() {
        if (整数値() != 0xcafebabe) 失敗値("not a class file");
        int 副版改訂 = 短整数値(), 版値 = 短整数値();
        if (版値 < 45 || 版値 > 52 || 副版改訂 != 0) 失敗値("supported class versions: 45..52, minor 0");
        定数個数 = 短整数値();
        if (定数個数 < 1 || 定数個数 > 512) { 失敗値("constant pool limit (511)"); return; }
        for (int 数 = 1; 数 < 定数個数 && !エラー; 数++) {
            int 種別値 = バイト値(); 定数印札[数] = 種別値;
            if (種別値 == 1) { 定数第二値[数] = 短整数値(); 定数先頭位置値[数] = 位置読取; バイト列読飛ばし(定数第二値[数]); }
            else if (種別値 == 3) 定数先頭位置値[数] = 整数値();
            else if (種別値 == 7 || 種別値 == 8) 定数先頭位置値[数] = 短整数値();
            else if (種別値 == 9 || 種別値 == 10 || 種別値 == 12) { 定数先頭位置値[数] = 短整数値(); 定数第二値[数] = 短整数値(); }
            else 失敗値("unsupported constant type");
        }
        int 許可値 = 短整数値();
        if ((許可値 & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) 失敗値("unsupported class flags");
        クラス名前 = クラス名前本文(短整数値());
        if (!語本文(クラス名前本文(短整数値()), "java/lang/Object")) 失敗値("inheritance unsupported");
        if (短整数値() != 0) 失敗値("interfaces unsupported");
        if (短整数値() != 0) 失敗値("fields unsupported");
        メソッド個数 = 短整数値();
        if (メソッド個数 < 1 || メソッド個数 > 32) { 失敗値("method count limit (32)"); return; }
        for (int 数 = 0; 数 < メソッド個数 && !エラー; 数++) {
            メソッドアクセス[数] = 短整数値(); メソッド名前本文[数] = 短整数値(); メソッド型[数] = 短整数値();
            定数検査(メソッド名前本文[数], 1); 記述子読取(数);
            if ((メソッドアクセス[数] & (0x100 | 0x400 | 0x20)) != 0) 失敗値("native, abstract and synchronized methods unsupported");
            if ((メソッドアクセス[数] & 8) == 0 && !語本文(メソッド名前本文[数], "<init>")) 失敗値("instance methods unsupported");
            if (語本文(メソッド名前本文[数], "<clinit>")) 失敗値("class initializers unsupported");
            for (int 前面値 = 0; 前面値 < 数; 前面値++) if (照合中語(メソッド名前本文[前面値], メソッド名前本文[数]) && 照合中語(メソッド型[前面値], メソッド型[数])) 失敗値("duplicate method");
            int 項目個数 = 短整数値();
            for (int 属性値 = 0; 属性値 < 項目個数 && !エラー; 属性値++) {
                int 名前 = 短整数値(), 長さ = 整数値(), 起動処理 = 位置読取;
                if (!切抜き(起動処理, 長さ)) { 失敗値("truncated method attribute"); break; }
                if (語本文(名前, "Code")) {
                    if (メソッド開始処理[数] != 0) 失敗値("duplicate Code attribute");
                    メソッドスタック[数] = 短整数値(); メソッド局所変数一覧[数] = 短整数値(); int コード長さ = 整数値();
                    if (メソッドスタック[数] > 128 || メソッド局所変数一覧[数] > 128 || メソッド局所変数一覧[数] < メソッド引数個数[数]
                        || コード長さ < 1 || コード長さ > 8192) 失敗値("method memory limits exceeded");
                    メソッド開始処理[数] = 位置読取; バイト列読飛ばし(コード長さ); メソッド終端位置[数] = 位置読取;
                    if (短整数値() != 0) 失敗値("exception handlers unsupported");
                    属性読飛ばし();
                    if (位置読取 != 起動処理 + 長さ) 失敗値("Code attribute size mismatch");
                } else バイト列読飛ばし(長さ);
            }
            if (メソッド開始処理[数] == 0) 失敗値("missing Code attribute");
            int 槽入口 = メソッド開始処理[数];
            while (槽入口 < メソッド終端位置[数] && !エラー) {
                int 長さ = 命令長さ(ファイル[槽入口]);
                if (長さ == 0 || 長さ > メソッド終端位置[数] - 槽入口) { 失敗値("unsupported or truncated bytecode"); break; }
                境界位置値[槽入口] = 数 + 1; 槽入口 += 長さ;
            }
            // 実行されない経路でも、不正な分岐先は許さない。
            槽入口 = メソッド開始処理[数];
            while (槽入口 < メソッド終端位置[数] && !エラー) {
                int 値 = ファイル[槽入口];
                if (値 >= 153 && 値 <= 167 || 値 == 198 || 値 == 199) {
                    int 宛先値 = 槽入口 + (short)(ファイル[槽入口 + 1] << 8 | ファイル[槽入口 + 2]);
                    if (宛先値 < メソッド開始処理[数] || 宛先値 >= メソッド終端位置[数] || 境界位置値[宛先値] != 数 + 1) 失敗値("invalid branch target");
                }
                槽入口 += 命令長さ(値);
            }
        }
        if (!エラー) 属性読飛ばし();
        if (位置読取 != 容量) 失敗値("extra class file data");
    }
    static int 記憶装置確保(int 種別値, int 長さ) {
        if (長さ < 0 || 長さ > ヒープ値.length - ヒープ終端位置位置 - 2) { 失敗値("object heap exhausted or negative array size"); return 0; }
        int 参照 = ヒープ終端位置位置; ヒープ終端位置位置 += 長さ + 2; ヒープ値[参照] = 種別値; ヒープ値[参照 + 1] = 長さ;
        return 参照;
    }
    static boolean オブジェクト値(int 参照, int 種別値) {
        if (参照 < 1 || 参照 >= ヒープ終端位置位置 - 1 || ヒープ値[参照] != 種別値) { 失敗値("null or invalid object reference"); return false; }
        return true;
    }
    static int 定数本文(int 番号) {
        if (!定数検査(番号, 1)) return 0;
        if (文字列参照[番号] != 0) return 文字列参照[番号];
        int 参照 = 記憶装置確保(1, 定数第二値[番号]); if (エラー) return 0;
        int 終端 = 定数先頭位置値[番号] + 定数第二値[番号], 数 = 定数先頭位置値[番号], 長さ = 0;
        while (数 < 終端 && !エラー) {
            int 値 = ファイル[数++];
            if (値 == 0) 失敗値("invalid modified UTF-8");
            else if (値 >= 192 && 値 <= 223 && 数 < 終端) {
                int 次回項目 = ファイル[数++];
                if ((次回項目 & 192) != 128) 失敗値("invalid modified UTF-8");
                値 = (値 & 31) << 6 | 次回項目 & 63;
                if (値 != 0 && 値 < 128) 失敗値("overlong modified UTF-8");
            } else if (値 >= 224 && 値 <= 239 && 数 + 1 < 終端) {
                int 先頭位置被演算子 = ファイル[数++], 第二被演算子 = ファイル[数++];
                if ((先頭位置被演算子 & 192) != 128 || (第二被演算子 & 192) != 128) 失敗値("invalid modified UTF-8");
                値 = (値 & 15) << 12 | (先頭位置被演算子 & 63) << 6 | 第二被演算子 & 63;
                if (値 < 2048) 失敗値("overlong modified UTF-8");
            } else if (値 >= 128) 失敗値("invalid modified UTF-8");
            ヒープ値[参照 + 2 + 長さ++] = 値;
        }
        ヒープ値[参照 + 1] = 長さ; 文字列参照[番号] = 参照; return 参照;
    }
    static int ホスト文字(String 値) {
        int 参照 = 記憶装置確保(1, 値.length()); if (エラー) return 0;
        for (int 数 = 0; 数 < 値.length(); 数++) ヒープ値[参照 + 2 + 数] = 値.charAt(数);
        return 参照;
    }
    static void 本文書込(int 参照) {
        if (参照 == 0) { 利用者.書込("null"); return; }
        if (!オブジェクト値(参照, 1)) return;
        for (int 数 = 0; 数 < ヒープ値[参照 + 1]; 数++) 利用者.文字値書込(ヒープ値[参照 + 2 + 数]);
    }
    static int 桁文字(int 値) {
        int 参照 = 記憶装置確保(1, 11); if (エラー) return 0;
        int 長さ = 0;
        if (値 < 0) ヒープ値[参照 + 2 + 長さ++] = '-'; else 値 = -値;
        int 位置添字 = 1000000000; boolean 起動処理 = false;
        while (位置添字 != 0) {
            int 数 = -(値 / 位置添字);
            if (数 != 0 || 起動処理 || 位置添字 == 1) { ヒープ値[参照 + 2 + 長さ++] = '0' + 数; 起動処理 = true; }
            値 %= 位置添字; 位置添字 /= 10;
        }
        ヒープ値[参照 + 1] = 長さ; return 参照;
    }
    static int 整数値復号(int 参照) {
        if (!オブジェクト値(参照, 1)) return 0;
        int 長さ = ヒープ値[参照 + 1], 数 = 0, 値 = 0; boolean 負数値 = false;
        if (長さ > 0 && (ヒープ値[参照 + 2] == '-' || ヒープ値[参照 + 2] == '+')) { 負数値 = ヒープ値[参照 + 2] == '-'; 数++; }
        if (数 == 長さ) 失敗値("NumberFormatException");
        for (; 数 < 長さ && !エラー; 数++) {
            int 桁値 = ヒープ値[参照 + 2 + 数] - '0';
            if (桁値 < 0 || 桁値 > 9 || 値 < -214748364 || 値 == -214748364 && 桁値 > (負数値 ? 8 : 7)) 失敗値("NumberFormatException");
            値 = 値 * 10 - 桁値;
        }
        return 負数値 ? 値 : -値;
    }
    static void 値格納(int 値, int 型値) {
        if (エラー) return;
        if (枠組添字 < 0 || 枠組スタック[枠組添字] >= メソッドスタック[枠組メソッド[枠組添字]]) { 失敗値("operand stack overflow"); return; }
        int 槽入口 = 枠組添字 * 128 + 枠組スタック[枠組添字]++; 被演算子スタック値[槽入口] = 値; 被演算子スタック型[槽入口] = 型値;
    }
    static int 値一覧減算(int 型値) {
        if (エラー) return 0;
        if (枠組添字 < 0 || 枠組スタック[枠組添字] < 1) { 失敗値("operand stack underflow"); return 0; }
        int 槽入口 = 枠組添字 * 128 + --枠組スタック[枠組添字]; 復帰型 = 被演算子スタック型[槽入口];
        if (型値 != 0 && 復帰型 != 型値) 失敗値("operand type mismatch");
        return 被演算子スタック値[槽入口];
    }
    static void 局所読取(int 番号, int 型値) {
        if (番号 >= メソッド局所変数一覧[枠組メソッド[枠組添字]] || 番号 < 0 || 局所型[枠組添字 * 128 + 番号] != 型値) { 失敗値("invalid or uninitialized local"); return; }
        値格納(局所値[枠組添字 * 128 + 番号], 型値);
    }
    static void 局所書込(int 番号, int 型値) {
        if (番号 >= メソッド局所変数一覧[枠組メソッド[枠組添字]] || 番号 < 0) { 失敗値("local index out of range"); return; }
        int 値 = 値一覧減算(型値); 局所値[枠組添字 * 128 + 番号] = 値; 局所型[枠組添字 * 128 + 番号] = 型値;
    }
    static int 命令符号バイト読取() {
        int 位置 = 枠組位置[枠組添字];
        if (位置 < メソッド開始処理[枠組メソッド[枠組添字]] || 位置 >= メソッド終端位置[枠組メソッド[枠組添字]]) { 失敗値("instruction pointer out of range"); return 0; }
        枠組位置[枠組添字]++; return ファイル[位置];
    }
    static int 命令符号短整数読取() { return 命令符号バイト読取() << 8 | 命令符号バイト読取(); }
    static void 移動値(int 位置) {
        int 関数 = 枠組メソッド[枠組添字];
        if (位置 < メソッド開始処理[関数] || 位置 >= メソッド終端位置[関数] || 境界位置値[位置] != 関数 + 1) 失敗値("invalid branch target");
        else 枠組位置[枠組添字] = 位置;
    }
    static void 呼出(int 関数) {
        if (枠組添字 == 31) { 失敗値("call stack limit (32)"); return; }
        int 次回項目 = 枠組添字 + 1;
        for (int 数 = 0; 数 < 128; 数++) 局所型[次回項目 * 128 + 数] = 0;
        for (int 数 = メソッド引数個数[関数] - 1; 数 >= 0; 数--) {
            局所値[次回項目 * 128 + 数] = 値一覧減算(メソッド引数型[関数 * 16 + 数]); 局所型[次回項目 * 128 + 数] = メソッド引数型[関数 * 16 + 数];
        }
        枠組添字 = 次回項目; 枠組メソッド[枠組添字] = 関数; 枠組位置[枠組添字] = メソッド開始処理[関数]; 枠組スタック[枠組添字] = 0;
    }
    static void 復帰結果(int 型値) {
        if (型値 != メソッド復帰[枠組メソッド[枠組添字]]) { 失敗値("return type mismatch"); return; }
        int 値 = 型値 == 0 ? 0 : 値一覧減算(型値);
        枠組添字--; if (枠組添字 >= 0 && 型値 != 0) 値格納(値, 型値);
    }
    static int[] ストリームファイル名前 = new int[64];
    static void ファイルストリーム呼出し(int 所有者値, int 名前, int 書式値, int 命令) {
        boolean 出力 = 語本文(所有者値, "java/io/FileOutputStream");
        int 種別値 = 出力 ? 6 : 5;
        if (命令 == 183 && 語本文(名前, "<init>")) {
            boolean 継続状態値 = false;
            if (出力 && 語本文(書式値, "(Ljava/lang/String;Z)V")) 継続状態値 = 値一覧減算(1) != 0;
            else if (!語本文(書式値, "(Ljava/lang/String;)V")) { 失敗値("unsupported file stream constructor"); return; }
            int ファイル入口名前 = 値一覧減算(2), ストリーム値 = 値一覧減算(2);
            if (!オブジェクト値(ファイル入口名前, 1) || !オブジェクト値(ストリーム値, 種別値) || エラー) return;
            if (ヒープ値[ストリーム値 + 3] != 0) { 失敗値("file stream already initialized"); return; }
            int 長さ = ヒープ値[ファイル入口名前 + 1];
            if (長さ < 1 || 長さ > 63) { 失敗値("invalid file name length"); return; }
            for (int 槽入口 = 0; 槽入口 < 長さ; 槽入口++) {
                int 値 = ヒープ値[ファイル入口名前 + 2 + 槽入口];
                if (値 < 1 || 値 > 127) { 失敗値("file stream paths currently require ASCII"); return; }
                ストリームファイル名前[槽入口] = 値;
            }
            ストリームファイル名前[長さ] = 0;
            int 記述子入口 = 利用者.ファイル記述子開放(ストリームファイル名前, 出力 ? (継続状態値 ? 1089 : 577) : 0);
            if (記述子入口 < 0) { 失敗値("FileNotFoundException: file open failed"); return; }
            ヒープ値[ストリーム値 + 2] = 記述子入口; ヒープ値[ストリーム値 + 3] = 1;
            return;
        }
        if (命令 != 182) { 失敗値("invalid file stream invocation"); return; }
        int 動作 = -1, 値 = 0;
        if (語本文(名前, "close") && 語本文(書式値, "()V")) 動作 = 0;
        if (!出力 && 語本文(名前, "read") && 語本文(書式値, "()I")) 動作 = 1;
        if (出力 && 語本文(名前, "write") && 語本文(書式値, "(I)V")) { 動作 = 2; 値 = 値一覧減算(1); }
        if (動作 < 0) { 失敗値("unsupported file stream method"); return; }
        int ストリーム値 = 値一覧減算(2);
        if (!オブジェクト値(ストリーム値, 種別値) || エラー) return;
        if (ヒープ値[ストリーム値 + 3] == 0) { 失敗値("uninitialized file stream"); return; }
        int 記述子入口 = ヒープ値[ストリーム値 + 2];
        if (動作 == 0) {
            if (記述子入口 >= 0 && 利用者.ファイル記述子閉鎖(記述子入口) < 0) 失敗値("IOException: close failed");
            ヒープ値[ストリーム値 + 2] = -1; return;
        }
        if (記述子入口 < 0) { 失敗値("IOException: stream closed"); return; }
        if (動作 == 1) {
            int 結果 = 利用者.一ファイルバイト読取(記述子入口);
            if (結果 < -1) 失敗値("IOException: read failed"); else 値格納(結果, 1);
        } else if (利用者.一ファイルバイト書込(記述子入口, 値) != 1) 失敗値("IOException: write failed");
    }
    static void メソッド呼出し(int 番号, int 命令) {
        if (!定数検査(番号, 10)) return;
        int 所有者値 = クラス名前本文(定数先頭位置値[番号]), 名前 = 参照名前(定数第二値[番号]), 書式値 = 参照型(定数第二値[番号]);
        if (エラー) return;
        if (照合中語(所有者値, クラス名前)) {
            if (命令 != 184) { 失敗値("only static user methods are supported"); return; }
            for (int 数 = 0; 数 < メソッド個数; 数++) if (照合中語(名前, メソッド名前本文[数]) && 照合中語(書式値, メソッド型[数])) {
                if ((メソッドアクセス[数] & 8) == 0) 失敗値("method is not static"); else 呼出(数);
                return;
            }
            失敗値("NoSuchMethodError"); return;
        }
        if (語本文(所有者値, "java/io/FileInputStream") || 語本文(所有者値, "java/io/FileOutputStream")) {
            ファイルストリーム呼出し(所有者値, 名前, 書式値, 命令); return;
        }
        if (命令 == 184 && 語本文(所有者値, "java/lang/Integer") && 語本文(名前, "parseInt") && 語本文(書式値, "(Ljava/lang/String;)I")) {
            値格納(整数値復号(値一覧減算(2)), 1); return;
        }
        if (命令 == 182 && 語本文(所有者値, "java/io/PrintStream") && (語本文(名前, "println") || 語本文(名前, "print"))) {
            int 型値 = 0, 値 = 0;
            if (語本文(書式値, "(I)V")) { 型値 = 1; 値 = 値一覧減算(1); }
            else if (語本文(書式値, "(Z)V")) { 型値 = 2; 値 = 値一覧減算(1); }
            else if (語本文(書式値, "(C)V")) { 型値 = 3; 値 = 値一覧減算(1); }
            else if (語本文(書式値, "(Ljava/lang/String;)V")) { 型値 = 4; 値 = 値一覧減算(2); }
            else if (!語本文(書式値, "()V") || !語本文(名前, "println")) 失敗値("unsupported print descriptor");
            if (値一覧減算(2) != -1) 失敗値("invalid PrintStream receiver");
            if (エラー) return;
            if (型値 == 1) Java道具.番号書込(値);
            if (型値 == 2) 利用者.書込(値 == 0 ? "false" : "true");
            if (型値 == 3) 利用者.文字値書込(値 & 65535);
            if (型値 == 4) 本文書込(値);
            if (語本文(名前, "println")) 利用者.文字値書込(10);
            return;
        }
        if (命令 == 182 && 語本文(所有者値, "java/lang/String")) {
            if (語本文(名前, "length") && 語本文(書式値, "()I")) {
                int 参照 = 値一覧減算(2); if (オブジェクト値(参照, 1)) 値格納(ヒープ値[参照 + 1], 1); return;
            }
            if (語本文(名前, "charAt") && 語本文(書式値, "(I)C")) {
                int 添え字値 = 値一覧減算(1), 参照 = 値一覧減算(2);
                if (オブジェクト値(参照, 1)) {
                    if (添え字値 < 0 || 添え字値 >= ヒープ値[参照 + 1]) 失敗値("StringIndexOutOfBoundsException"); else 値格納(ヒープ値[参照 + 2 + 添え字値], 1);
                }
                return;
            }
        }
        if (語本文(所有者値, "java/lang/StringBuilder")) {
            if (命令 == 183 && 語本文(名前, "<init>") && 語本文(書式値, "()V")) { オブジェクト値(値一覧減算(2), 4); return; }
            if (命令 == 182 && 語本文(名前, "toString") && 語本文(書式値, "()Ljava/lang/String;")) {
                int 参照 = 値一覧減算(2); if (オブジェクト値(参照, 4)) 値格納(ヒープ値[参照 + 2] == 0 ? ホスト文字("") : ヒープ値[参照 + 2], 2); return;
            }
            if (命令 == 182 && 語本文(名前, "append")) {
                int 文 = 0;
                if (語本文(書式値, "(I)Ljava/lang/StringBuilder;")) 文 = 桁文字(値一覧減算(1));
                else if (語本文(書式値, "(Z)Ljava/lang/StringBuilder;")) 文 = ホスト文字(値一覧減算(1) == 0 ? "false" : "true");
                else if (語本文(書式値, "(C)Ljava/lang/StringBuilder;")) {
                    int 値 = 値一覧減算(1); 文 = 記憶装置確保(1, 1); if (!エラー) ヒープ値[文 + 2] = 値 & 65535;
                }
                else if (語本文(書式値, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { 文 = 値一覧減算(2); if (文 == 0) 文 = ホスト文字("null"); }
                else { 失敗値("unsupported StringBuilder append"); return; }
                int 参照 = 値一覧減算(2); if (!オブジェクト値(参照, 4) || !オブジェクト値(文, 1)) return;
                int 前面値 = ヒープ値[参照 + 2], 前面値長さ = 前面値 == 0 ? 0 : ヒープ値[前面値 + 1], 後端値長さ = ヒープ値[文 + 1];
                int 新規本文 = 記憶装置確保(1, 前面値長さ + 後端値長さ); if (エラー) return;
                for (int 数 = 0; 数 < 前面値長さ; 数++) ヒープ値[新規本文 + 2 + 数] = ヒープ値[前面値 + 2 + 数];
                for (int 数 = 0; 数 < 後端値長さ; 数++) ヒープ値[新規本文 + 2 + 前面値長さ + 数] = ヒープ値[文 + 2 + 数];
                ヒープ値[参照 + 2] = 新規本文; 値格納(参照, 2); return;
            }
        }
        失敗値("unsupported library method");
    }
    static int 配列槽(int 参照, int 添え字値, int 型値) {
        if (!オブジェクト値(参照, 型値)) return 0;
        if (添え字値 < 0 || 添え字値 >= ヒープ値[参照 + 1]) { 失敗値("ArrayIndexOutOfBoundsException"); return 0; }
        return 参照 + 2 + 添え字値;
    }
    static void 命令実行() {
        int 剰余データ = 500000;
        while (枠組添字 >= 0 && !エラー) {
            if (--剰余データ == 0) { 失敗値("instruction limit (500000)"); break; }
            int 起動処理 = 枠組位置[枠組添字], 値 = 命令符号バイト読取();
            if (エラー) break;
            if (値 == 0) continue;
            if (値 == 1) { 値格納(0, 2); continue; }
            if (値 >= 2 && 値 <= 8) { 値格納(値 - 3, 1); continue; }
            if (値 == 16) { 値格納((byte)命令符号バイト読取(), 1); continue; }
            if (値 == 17) { 値格納((short)命令符号短整数読取(), 1); continue; }
            if (値 == 18 || 値 == 19) {
                int 数 = 値 == 18 ? 命令符号バイト読取() : 命令符号短整数読取();
                if (数 <= 0 || 数 >= 定数個数) 失敗値("invalid ldc constant");
                else if (定数印札[数] == 3) 値格納(定数先頭位置値[数], 1);
                else if (定数印札[数] == 8) 値格納(定数本文(定数先頭位置値[数]), 2);
                else 失敗値("unsupported ldc constant");
                continue;
            }
            if (値 == 21 || 値 == 25) { 局所読取(命令符号バイト読取(), 値 == 21 ? 1 : 2); continue; }
            if (値 >= 26 && 値 <= 29) { 局所読取(値 - 26, 1); continue; }
            if (値 >= 42 && 値 <= 45) { 局所読取(値 - 42, 2); continue; }
            if (値 == 54 || 値 == 58) { 局所書込(命令符号バイト読取(), 値 == 54 ? 1 : 2); continue; }
            if (値 >= 59 && 値 <= 62) { 局所書込(値 - 59, 1); continue; }
            if (値 >= 75 && 値 <= 78) { 局所書込(値 - 75, 2); continue; }
            if (値 == 46 || 値 == 50) {
                int 添え字値 = 値一覧減算(1), 参照 = 値一覧減算(2), 槽入口 = 配列槽(参照, 添え字値, 値 == 46 ? 2 : 3);
                if (!エラー) 値格納(ヒープ値[槽入口], 値 == 46 ? 1 : 2); continue;
            }
            if (値 == 79 || 値 == 83) {
                int 項目要素 = 値一覧減算(値 == 79 ? 1 : 2), 添え字値 = 値一覧減算(1), 参照 = 値一覧減算(2), 槽入口 = 配列槽(参照, 添え字値, 値 == 79 ? 2 : 3);
                if (値 == 83 && 項目要素 != 0) オブジェクト値(項目要素, 1);
                if (!エラー) ヒープ値[槽入口] = 項目要素; continue;
            }
            if (値 == 87) { 値一覧減算(0); continue; }
            if (値 == 89) { int 先頭位置被演算子 = 値一覧減算(0), 型値 = 復帰型; 値格納(先頭位置被演算子, 型値); 値格納(先頭位置被演算子, 型値); continue; }
            if (値 == 95) { int 先頭位置被演算子 = 値一覧減算(0), 先頭位置被演算子型 = 復帰型, 第二被演算子 = 値一覧減算(0), 第二被演算子型 = 復帰型; 値格納(先頭位置被演算子, 先頭位置被演算子型); 値格納(第二被演算子, 第二被演算子型); continue; }
            if (値 == 96 || 値 == 100 || 値 == 104 || 値 == 108 || 値 == 112 || 値 == 120
                || 値 == 122 || 値 == 124 || 値 == 126 || 値 == 128 || 値 == 130) {
                int 第二被演算子 = 値一覧減算(1), 先頭位置被演算子 = 値一覧減算(1), 結果 = 0;
                if ((値 == 108 || 値 == 112) && 第二被演算子 == 0) { 失敗値("ArithmeticException: / by zero"); continue; }
                if (値 == 96) 結果 = 先頭位置被演算子 + 第二被演算子;
                if (値 == 100) 結果 = 先頭位置被演算子 - 第二被演算子;
                if (値 == 104) 結果 = 先頭位置被演算子 * 第二被演算子;
                if (値 == 108) 結果 = 先頭位置被演算子 / 第二被演算子;
                if (値 == 112) 結果 = 先頭位置被演算子 % 第二被演算子;
                if (値 == 120) 結果 = 先頭位置被演算子 << 第二被演算子;
                if (値 == 122) 結果 = 先頭位置被演算子 >> 第二被演算子;
                if (値 == 124) 結果 = 先頭位置被演算子 >>> 第二被演算子;
                if (値 == 126) 結果 = 先頭位置被演算子 & 第二被演算子;
                if (値 == 128) 結果 = 先頭位置被演算子 | 第二被演算子;
                if (値 == 130) 結果 = 先頭位置被演算子 ^ 第二被演算子;
                値格納(結果, 1); continue;
            }
            if (値 == 116) { 値格納(-値一覧減算(1), 1); continue; }
            if (値 == 132) {
                int 局所有効範囲 = 命令符号バイト読取(), 増分段階 = (byte)命令符号バイト読取(); 局所読取(局所有効範囲, 1); 値格納(値一覧減算(1) + 増分段階, 1); 局所書込(局所有効範囲, 1); continue;
            }
            if (値 >= 145 && 値 <= 147) {
                int 数 = 値一覧減算(1); 値格納(値 == 145 ? (byte)数 : 値 == 146 ? (char)数 : (short)数, 1); continue;
            }
            if (値 >= 153 && 値 <= 167 || 値 == 198 || 値 == 199) {
                int 宛先値 = 起動処理 + (short)命令符号短整数読取(); boolean 要否続行 = 値 == 167;
                if (値 >= 153 && 値 <= 158) {
                    int 数 = 値一覧減算(1); 要否続行 = 値 == 153 ? 数 == 0 : 値 == 154 ? 数 != 0 : 値 == 155 ? 数 < 0 : 値 == 156 ? 数 >= 0 : 値 == 157 ? 数 > 0 : 数 <= 0;
                } else if (値 >= 159 && 値 <= 166) {
                    int 第二被演算子 = 値一覧減算(値 >= 165 ? 2 : 1), 先頭位置被演算子 = 値一覧減算(値 >= 165 ? 2 : 1);
                    要否続行 = 値 == 159 || 値 == 165 ? 先頭位置被演算子 == 第二被演算子 : 値 == 160 || 値 == 166 ? 先頭位置被演算子 != 第二被演算子 : 値 == 161 ? 先頭位置被演算子 < 第二被演算子 : 値 == 162 ? 先頭位置被演算子 >= 第二被演算子 : 値 == 163 ? 先頭位置被演算子 > 第二被演算子 : 先頭位置被演算子 <= 第二被演算子;
                } else if (値 == 198 || 値 == 199) { int 数 = 値一覧減算(2); 要否続行 = 値 == 198 ? 数 == 0 : 数 != 0; }
                if (要否続行) 移動値(宛先値); continue;
            }
            if (値 == 172 || 値 == 176 || 値 == 177) { 復帰結果(値 == 172 ? 1 : 値 == 176 ? 2 : 0); continue; }
            if (値 == 178) {
                int 数 = 命令符号短整数読取(); if (!定数検査(数, 9)) continue;
                if (!語本文(クラス名前本文(定数先頭位置値[数]), "java/lang/System") || !語本文(参照名前(定数第二値[数]), "out")
                    || !語本文(参照型(定数第二値[数]), "Ljava/io/PrintStream;")) 失敗値("unsupported static field");
                else 値格納(-1, 2); continue;
            }
            if (値 == 182 || 値 == 183 || 値 == 184) { メソッド呼出し(命令符号短整数読取(), 値); continue; }
            if (値 == 187) {
                int 名前 = クラス名前本文(命令符号短整数読取());
                if (語本文(名前, "java/lang/StringBuilder")) 値格納(記憶装置確保(4, 1), 2);
                else if (語本文(名前, "java/io/FileInputStream") || 語本文(名前, "java/io/FileOutputStream")) {
                    int 参照 = 記憶装置確保(語本文(名前, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!エラー) { ヒープ値[参照 + 2] = -1; 値格納(参照, 2); }
                } else 失敗値("unsupported object construction");
                continue;
            }
            if (値 == 188 || 値 == 189) {
                if (値 == 188) { if (命令符号バイト読取() != 10) 失敗値("only int[] newarray is supported"); }
                else if (!語本文(クラス名前本文(命令符号短整数読取()), "java/lang/String")) 失敗値("only String[] anewarray is supported");
                int 長さ = 値一覧減算(1); 値格納(記憶装置確保(値 == 188 ? 2 : 3, 長さ), 2); continue;
            }
            if (値 == 190) {
                int 参照 = 値一覧減算(2);
                if (参照 < 1 || 参照 >= ヒープ終端位置位置 - 1 || (ヒープ値[参照] != 2 && ヒープ値[参照] != 3)) 失敗値("null or invalid array");
                else 値格納(ヒープ値[参照 + 1], 1); continue;
            }
            if (値 == 192) {
                int 名前 = クラス名前本文(命令符号短整数読取()), 参照 = 値一覧減算(2);
                if (!語本文(名前, "java/lang/String")) 失敗値("unsupported checkcast");
                else if (参照 != 0) オブジェクト値(参照, 1);
                値格納(参照, 2); continue;
            }
            失敗値("unsupported bytecode");
        }
    }
    public static int 起動処理() {
        if (利用者.引数列個数() == 1 && Java道具.等価本文(利用者.引数(0), "-version")) {
            利用者.書込("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (利用者.引数列個数() < 1) { 利用者.書込("Usage: java CLASS [ARGS]\n"); return 2; }
        int 長さ = Java道具.名前(ファイル名前本文, 利用者.引数(0));
        if (長さ < 1 || 長さ > 57) { 利用者.書込("java: invalid class name\n"); return 2; }
        ファイル名前本文[長さ] = '.'; ファイル名前本文[長さ + 1] = 'c'; ファイル名前本文[長さ + 2] = 'l'; ファイル名前本文[長さ + 3] = 'a'; ファイル名前本文[長さ + 4] = 's'; ファイル名前本文[長さ + 5] = 's';
        容量 = 利用者.ファイル読取(ファイル名前本文, ファイル);
        if (容量 < 0) { 利用者.書込("java: cannot read class: "); Java道具.番号書込(容量); 利用者.文字値書込(10); return 1; }
        クラス読取(); if (エラー) return 1;
        int 文字名前 = 定数本文(クラス名前);
        if (!エラー && ヒープ値[文字名前 + 1] != 長さ) 失敗値("class name does not match file");
        for (int 数 = 0; 数 < 長さ && !エラー; 数++) if (ヒープ値[文字名前 + 2 + 数] != ファイル名前本文[数]) 失敗値("class name does not match file");
        int 入口点値 = -1;
        for (int 数 = 0; 数 < メソッド個数; 数++) if (語本文(メソッド名前本文[数], "main") && 語本文(メソッド型[数], "([Ljava/lang/String;)V") && (メソッドアクセス[数] & 9) == 9) 入口点値 = 数;
        if (入口点値 < 0) 失敗値("public static void main(String[] args) required");
        if (エラー) return 1;
        int 引数 = 記憶装置確保(3, 利用者.引数列個数() - 1);
        for (int 数 = 1; 数 < 利用者.引数列個数() && !エラー; 数++) ヒープ値[引数 + 1 + 数] = ホスト文字(利用者.引数(数));
        枠組添字 = 0; 枠組メソッド[0] = 入口点値; 枠組位置[0] = メソッド開始処理[入口点値]; 局所値[0] = 引数; 局所型[0] = 2;
        命令実行(); return エラー ? 1 : 0;
    }
}
