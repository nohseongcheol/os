// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java クラスファイルから独立 ARM64 カーネル用の C ソースを生成する。ホスト JDK で実行する。 */
public final class 事前用時間コンパイラ {
    static final class 翻訳エラー extends RuntimeException {
        翻訳エラー(String 説明) { super(説明); }
    }
    static final class データ読取器 {
        final byte[] データ;
        int 位置;
        データ読取器(byte[] 入力データ) { データ = 入力データ; }
        byte[] 読取(int 長さ) {
            if (長さ < 0 || 長さ > データ.length - 位置) throw new 翻訳エラー("切抜き済み値 クラス値 또는 命令 データ");
            byte[] 結果 = Arrays.copyOfRange(データ, 位置, 位置 + 長さ); 位置 += 長さ; return 結果;
        }
        int バイト読取() { if (位置 >= データ.length) throw new 翻訳エラー("切抜き済み値 命令 データ"); return データ[位置++] & 255; }
        int 短整数読取() { return (バイト読取() << 8) | バイト読取(); }
        int 整数読取() { return (短整数読取() << 16) | 短整数読取(); }
        int 符号付きバイト読取() { return (byte) バイト読取(); }
        int 符号付き短整数読取() { return (short) 短整数読取(); }
    }
    static final class 成員データ {
        final int アクセス入口;
        final String 名前, 説明値;
        final Map<String, byte[]> 属性値;
        成員データ(int アクセス値, String 名前値, String 記述子データ, Map<String, byte[]> 属性データ) {
            アクセス入口 = アクセス値; 名前 = 名前値; 説明値 = 記述子データ; 属性値 = 属性データ;
        }
    }
    static final class メソッド参照 implements Comparable<メソッド参照> {
        final String 所有者値, 名前, 説明値;
        メソッド参照(String 所有対象値, String 名前値, String 記述子データ) { 所有者値 = 所有対象値; 名前 = 名前値; 説明値 = 記述子データ; }
        String[] 構成要素一覧() { return new String[]{所有者値, 名前, 説明値}; }
        public int compareTo(メソッド参照 通信相手値) {
            int 比較状態値 = 所有者値.compareTo(通信相手値.所有者値);
            if (比較状態値 == 0) 比較状態値 = 名前.compareTo(通信相手値.名前);
            return 比較状態値 == 0 ? 説明値.compareTo(通信相手値.説明値) : 比較状態値;
        }
        public boolean equals(Object 通信相手値) { return 通信相手値 instanceof メソッド参照 && compareTo((メソッド参照) 通信相手値) == 0; }
        public int hashCode() { return Objects.hash(所有者値, 名前, 説明値); }
    }
    static final class クラスデータ {
        final int[] 定数種別;
        final Object[] 定数データ;
        final String 名前;
        final List<成員データ> フィールド値, 関数;
        クラスデータ(Path 経路) throws IOException {
            データ読取器 読取器値 = new データ読取器(Files.readAllBytes(経路));
            if (読取器値.整数読取() != 0xcafebabe) throw new 翻訳エラー("Java クラス値 표식이 아님");
            読取器値.読取(4);
            int 項目個数 = 読取器値.短整数読取(); 定数種別 = new int[項目個数]; 定数データ = new Object[項目個数];
            for (int 序数添字 = 1; 序数添字 < 項目個数; 序数添字++) {
                int 種別値 = 読取器値.バイト読取(); 定数種別[序数添字] = 種別値;
                switch (種別値) {
                    case 1:
                        int 長さ = 読取器値.短整数読取();
                        byte[] 文字緩衝域 = 読取器値.読取(長さ), 長さ接頭辞付きデータ = new byte[長さ + 2];
                        長さ接頭辞付きデータ[0] = (byte)(長さ >> 8); 長さ接頭辞付きデータ[1] = (byte)長さ;
                        System.arraycopy(文字緩衝域, 0, 長さ接頭辞付きデータ, 2, 長さ);
                        定数データ[序数添字] = new DataInputStream(new ByteArrayInputStream(長さ接頭辞付きデータ)).readUTF(); break;
                    case 3: 定数データ[序数添字] = 読取器値.整数読取(); break;
                    case 4: 読取器値.読取(4); break;
                    case 5: case 6: 読取器値.読取(8); 序数添字++; break;
                    case 7: case 8: case 16: 定数データ[序数添字] = 読取器値.短整数読取(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        定数データ[序数添字] = new int[]{読取器値.短整数読取(), 読取器値.短整数読取()}; break;
                    case 15: 定数データ[序数添字] = new int[]{読取器値.バイト読取(), 読取器値.短整数読取()}; break;
                    default: throw new 翻訳エラー("지원하지 않는 定数値 種別値: " + 種別値);
                }
            }
            読取器値.短整数読取(); 名前 = クラス名前(読取器値.短整数読取());
            if (!クラス名前(読取器値.短整数読取()).equals("java/lang/Object") || 読取器値.短整数読取() != 0)
                throw new 翻訳エラー(名前 + ": 상속 및 인터페이스 判定未対応");
            フィールド値 = 成員一覧読取(読取器値); 関数 = 成員一覧読取(読取器値); 属性一覧読取(読取器値);
            if (読取器値.位置 != 読取器値.データ.length) throw new 翻訳エラー("クラス値 뒤에 남은 データ");
        }
        String 文字(int 番号) {
            if (番号 < 1 || 番号 >= 定数種別.length || 定数種別[番号] != 1) throw new 翻訳エラー("文字 定数値 番号 エラー");
            return (String) 定数データ[番号];
        }
        String クラス名前(int 番号) {
            if (番号 < 1 || 番号 >= 定数種別.length || 定数種別[番号] != 7) throw new 翻訳エラー("クラス値 参照 エラー");
            return 文字((Integer)定数データ[番号]);
        }
        メソッド参照 参照(int 番号) {
            if (番号 < 1 || 番号 >= 定数種別.length || 定数種別[番号] < 9 || 定数種別[番号] > 11) throw new 翻訳エラー("멤버 参照 エラー");
            int[] 対値 = (int[])定数データ[番号], 名前対 = (int[])定数データ[対値[1]];
            return new メソッド参照(クラス名前(対値[0]), 文字(名前対[0]), 文字(名前対[1]));
        }
        Map<String, byte[]> 属性一覧読取(データ読取器 読取器値) {
            Map<String, byte[]> 結果 = new LinkedHashMap<>();
            int 項目個数 = 読取器値.短整数読取();
            for (int 序数添字 = 0; 序数添字 < 項目個数; 序数添字++) {
                String 属性名前 = 文字(読取器値.短整数読取()); byte[] 値 = 読取器値.読取(読取器値.整数読取());
                if (結果.put(属性名前, 値) != null) throw new 翻訳エラー("겹친 属性値: " + 属性名前);
            }
            return 結果;
        }
        List<成員データ> 成員一覧読取(データ読取器 読取器値) {
            List<成員データ> 結果 = new ArrayList<>(); int 項目個数 = 読取器値.短整数読取();
            for (int 序数添字 = 0; 序数添字 < 項目個数; 序数添字++) {
                int アクセス入口 = 読取器値.短整数読取(); String メソッド入口名前 = 文字(読取器値.短整数読取()), 説明値 = 文字(読取器値.短整数読取());
                結果.add(new 成員データ(アクセス入口, メソッド入口名前, 説明値, 属性一覧読取(読取器値)));
            }
            return 結果;
        }
    }
    static final class メソッド記述子 {
        final List<String> 引数 = new ArrayList<>();
        final String 復帰結果;
        メソッド記述子(String 説明値) {
            if (!説明値.startsWith("(")) throw new 翻訳エラー("関数 説明値 エラー: " + 説明値);
            int 終端 = 説明値.indexOf(')'); if (終端 < 0) throw new 翻訳エラー("関数 説明値 エラー: " + 説明値);
            引数.addAll(型一覧解析(説明値.substring(1, 終端)));
            List<String> 返却済み値一覧 = 型一覧解析(説明値.substring(終端 + 1));
            if (引数.contains("V") || 返却済み値一覧.size() != 1) throw new 翻訳エラー("関数 説明値 エラー: " + 説明値);
            復帰結果 = 返却済み値一覧.get(0);
        }
    }
    static List<String> 型一覧解析(String 説明値) {
        List<String> 結果 = new ArrayList<>();
        String[] 許可済み書式 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 位置 = 0; 位置 < 説明値.length();) {
            String 選択状態値 = null;
            for (String 書式値 : 許可済み書式) if (説明値.startsWith(書式値, 位置)) { 選択状態値 = 書式値; break; }
            if (選択状態値 == null) throw new 翻訳エラー("지원하지 않는 データ型: " + 説明値);
            結果.add(選択状態値); 位置 += 選択状態値.length();
        }
        return 結果;
    }
    static String 記号(String 種別値, String... 構成要素一覧) {
        try {
            byte[] ハッシュファイル = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 構成要素一覧).getBytes(StandardCharsets.UTF_8));
            StringBuilder 文 = new StringBuilder("j_" + 種別値 + "_");
            for (int 序数添字 = 0; 序数添字 < 12; 序数添字++) 文.append(String.format(Locale.ROOT, "%02x", ハッシュファイル[序数添字] & 255));
            return 文.toString();
        } catch (Exception エラー) { throw new 翻訳エラー(エラー.toString()); }
    }
    final Map<String, クラスデータ> クラス群一覧 = new TreeMap<>();
    final Map<メソッド参照, 成員データ> メソッド一覧一覧 = new TreeMap<>(), フィールド一覧一覧 = new TreeMap<>();
    final Map<String, String> 文字列値一覧 = new LinkedHashMap<>(), 機械関数一覧 = new LinkedHashMap<>();
    final String 実行状態対象, 機械クラス;
    final int ヒープ語個数;
    final Path 資源経路;
    事前用時間コンパイラ(List<Path> 経路一覧, String 対象値, int 字句用語個数, Path 資源値) throws IOException {
        if ((!対象値.equals("kernel") && !対象値.equals("user")) || 字句用語個数 < 1024 || 字句用語個数 > 1048576) throw new 翻訳エラー("命令実行 対象値 또는 記憶 番地領域 容量 エラー");
        実行状態対象 = 対象値; ヒープ語個数 = 字句用語個数; 資源経路 = 資源値;
        // この名前も国別ソースの生成時に対象言語へ翻訳する。
        機械クラス = 対象値.equals("kernel") ? "基板" : "利用者";
        for (String 行 : Files.readAllLines(資源値.resolve("機械関数群.tsv"), StandardCharsets.UTF_8)) {
            String[] 構成要素一覧 = 行.split("\t", -1);
            if (構成要素一覧.length != 4) throw new 翻訳エラー("機械 関数 データ エラー");
            if (構成要素一覧[0].equals(対象値)) 機械関数一覧.put(構成要素一覧[1] + 構成要素一覧[2], 構成要素一覧[3]);
        }
        for (Path 経路 : 経路一覧) {
            クラスデータ データ = new クラスデータ(経路);
            if (クラス群一覧.put(データ.名前, データ) != null) throw new 翻訳エラー("중복 クラス値: " + データ.名前);
            for (成員データ フィールド値 : データ.フィールド値) {
                if ((フィールド値.アクセス入口 & 8) == 0 || 型一覧解析(フィールド値.説明値).equals(Collections.singletonList("V"))) throw new 翻訳エラー("静的値 필드만 支援値");
                if (フィールド一覧一覧.put(new メソッド参照(データ.名前, フィールド値.名前, フィールド値.説明値), フィールド値) != null) throw new 翻訳エラー("중복 フィールド値");
            }
            for (成員データ 関数 : データ.関数) {
                if (関数.名前.equals("<init>")) continue;
                if ((関数.アクセス入口 & 8) == 0 || (関数.アクセス入口 & (0x20 | 0x400)) != 0) throw new 翻訳エラー("静的値 비동기화 함수만 支援値");
                new メソッド記述子(関数.説明値);
                if (メソッド一覧一覧.put(new メソッド参照(データ.名前, 関数.名前, 関数.説明値), 関数) != null) throw new 翻訳エラー("중복 関数");
            }
        }
    }
    String 文字列記号(String 文) { return 文字列値一覧.computeIfAbsent(文, 値 -> "j_text_" + 文字列値一覧.size()); }
    String 定数式(クラスデータ データ, int 番号) {
        if (番号 < 1 || 番号 >= データ.定数種別.length) throw new 翻訳エラー("定数値 番号 切抜き エラー");
        if (データ.定数種別[番号] == 3) return "(word)(uint32_t)(" + データ.定数データ[番号] + ")";
        if (データ.定数種別[番号] == 8) return "(word)" + 文字列記号(データ.文字((Integer)データ.定数データ[番号]));
        throw new 翻訳エラー("정수와 文字列 상수만 支援値");
    }
    String メソッド原型(メソッド参照 参照) {
        List<String> 引数列一覧 = new ArrayList<>(); int 項目個数 = new メソッド記述子(参照.説明値).引数.size();
        for (int 序数添字 = 0; 序数添字 < 項目個数; 序数添字++) 引数列一覧.add("word a" + 序数添字);
        return "static word " + 記号("method", 参照.構成要素一覧()) + "(" + (項目個数 == 0 ? "void" : String.join(", ", 引数列一覧)) + ")";
    }
    void 局所検査(int 番号, int 局所変数個数) { if (番号 < 0 || 番号 >= 局所変数個数) throw new 翻訳エラー("局所有効範囲 変数値 番号 切抜き エラー"); }
    void 分岐出力(List<String> 出力, Set<Integer> 分岐一覧, int 位置, int 移動量総量, String 条件) {
        int 宛先値 = 位置 + 移動量総量; 分岐一覧.add(宛先値);
        出力.add((条件 == null ? "" : "if (" + 条件 + ") ") + "goto b" + 宛先値 + ";");
    }
    String メソッド本体(メソッド参照 関数, 成員データ データ) {
        byte[] 本体データ = データ.属性値.get("Code"); if (本体データ == null) throw new 翻訳エラー("関数 몸체가 未存在メソッド: " + 関数.名前);
        データ読取器 読取器値 = new データ読取器(本体データ); int スタック深さ = 読取器値.短整数読取(), 局所変数個数 = 読取器値.短整数読取();
        データ読取器 命令データ = new データ読取器(読取器値.読取(読取器値.整数読取()));
        if (読取器値.短整数読取() != 0) throw new 翻訳エラー("try/catch/finally 判定未対応");
        メソッド記述子 書式値 = new メソッド記述子(関数.説明値); if (局所変数個数 < 書式値.引数.size()) throw new 翻訳エラー("매개변수보다 적은 局所有効範囲 変数値");
        クラスデータ クラス値 = クラス群一覧.get(関数.所有者値);
        List<String> 出力 = new ArrayList<>(); 出力.add(メソッド原型(関数) + " {");
        出力.add("word s[" + Math.max(スタック深さ, 1) + "], l[" + Math.max(局所変数個数, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 序数添字 = 0; 序数添字 < 書式値.引数.size(); 序数添字++) 出力.add("l[" + 序数添字 + "] = a" + 序数添字 + ";");
        Set<Integer> 境界一覧一覧 = new HashSet<>(), 分岐一覧 = new HashSet<>();
        String[] 比較一覧一覧 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (命令データ.位置 < 命令データ.データ.length) {
            int 位置 = 命令データ.位置, 命令 = 命令データ.バイト読取(); 境界一覧一覧.add(位置); 出力.add("b" + 位置 + ":;");
            if (命令 == 0) continue;
            if (命令 == 1) 出力.add("PUSH(0);");
            else if (命令 >= 2 && 命令 <= 8) 出力.add("PUSH((uint32_t)(" + (命令 - 3) + "));");
            else if (命令 == 16 || 命令 == 17) 出力.add("PUSH((uint32_t)(" + (命令 == 16 ? 命令データ.符号付きバイト読取() : 命令データ.符号付き短整数読取()) + "));");
            else if (命令 == 18 || 命令 == 19) 出力.add("PUSH(" + 定数式(クラス値, 命令 == 18 ? 命令データ.バイト読取() : 命令データ.短整数読取()) + ");");
            else if (命令 == 21 || 命令 == 25 || (命令 >= 26 && 命令 <= 29) || (命令 >= 42 && 命令 <= 45)) {
                int 番号 = 命令 == 21 || 命令 == 25 ? 命令データ.バイト読取() : 命令 - (命令 <= 29 ? 26 : 42);
                局所検査(番号, 局所変数個数); 出力.add("PUSH(l[" + 番号 + "]);");
            } else if (命令 == 54 || 命令 == 58 || (命令 >= 59 && 命令 <= 62) || (命令 >= 75 && 命令 <= 78)) {
                int 番号 = 命令 == 54 || 命令 == 58 ? 命令データ.バイト読取() : 命令 - (命令 <= 62 ? 59 : 75);
                局所検査(番号, 局所変数個数); 出力.add("l[" + 番号 + "] = POP();");
            } else if (命令 == 46) 出力.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (命令 == 79) 出力.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (命令 == 87 || 命令 == 88) 出力.add(命令 == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (命令 >= 89 && 命令 <= 95) {
                int[] 項目個数一覧 = {1,2,3,2,3,4,2}; String[] 順序一覧 = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 序数添字 = 0; 序数添字 < 項目個数一覧[命令 - 89]; 序数添字++) 出力.add("abcd".charAt(序数添字) + " = POP();");
                for (char 値 : 順序一覧[命令 - 89].toCharArray()) 出力.add("PUSH(" + 値 + ");");
            } else if (命令 == 96 || 命令 == 100 || 命令 == 104 || 命令 == 126 || 命令 == 128 || 命令 == 130) {
                String 操作値 = 命令 == 96 ? "+" : 命令 == 100 ? "-" : 命令 == 104 ? "*" : 命令 == 126 ? "&" : 命令 == 128 ? "|" : "^";
                出力.add("b = POP(); a = POP(); PUSH((uint32_t)a " + 操作値 + " (uint32_t)b);");
            } else if (命令 == 108 || 命令 == 112) 出力.add("b = POP(); a = POP(); PUSH(divide(a,b," + (命令 == 112 ? 1 : 0) + "));");
            else if (命令 == 116) 出力.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (命令 == 120 || 命令 == 122 || 命令 == 124) {
                出力.add("b = POP(); a = POP();"); 出力.add("PUSH(" + (命令 == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (命令 == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (命令 == 132) {
                int 番号 = 命令データ.バイト読取(), 増分総量 = 命令データ.符号付きバイト読取(); 局所検査(番号, 局所変数個数);
                出力.add("l[" + 番号 + "] = (uint32_t)l[" + 番号 + "] + (uint32_t)(" + 増分総量 + ");");
            } else if (命令 >= 145 && 命令 <= 147) 出力.add("a = POP(); PUSH((uint32_t)(" + (命令 == 145 ? "int8_t" : 命令 == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (命令 >= 153 && 命令 <= 158) {
                出力.add("a = POP();"); 分岐出力(出力, 分岐一覧, 位置, 命令データ.符号付き短整数読取(), "(int32_t)a " + 比較一覧一覧[命令 - 153] + " 0");
            } else if (命令 >= 159 && 命令 <= 166) {
                出力.add("b = POP(); a = POP();"); 分岐出力(出力, 分岐一覧, 位置, 命令データ.符号付き短整数読取(), 命令 >= 165 ? "a " + 比較一覧一覧[命令 - 159] + " b" : "(int32_t)a " + 比較一覧一覧[命令 - 159] + " (int32_t)b");
            } else if (命令 == 167 || 命令 == 200) 分岐出力(出力, 分岐一覧, 位置, 命令 == 167 ? 命令データ.符号付き短整数読取() : 命令データ.整数読取(), null);
            else if (命令 == 170 || 命令 == 171) {
                while (命令データ.位置 % 4 != 0) 命令データ.バイト読取();
                int 既定値 = 命令データ.整数読取(); 出力.add("a = POP();");
                if (命令 == 170) {
                    int 下端値 = 命令データ.整数読取(), 上端値 = 命令データ.整数読取(); long 項目個数 = (long)上端値 - 下端値 + 1;
                    if (項目個数 < 1 || 項目個数 > (命令データ.データ.length - 命令データ.位置) / 4) throw new 翻訳エラー("switch 切抜き エラー");
                    for (long 値 = 下端値; 値 <= 上端値; 値++) 分岐出力(出力, 分岐一覧, 位置, 命令データ.整数読取(), "(int32_t)a == (" + 値 + ")");
                } else {
                    int 項目個数 = 命令データ.整数読取(), 前面データ = 0;
                    if (項目個数 < 0 || 項目個数 > (命令データ.データ.length - 命令データ.位置) / 8) throw new 翻訳エラー("switch 容量 エラー");
                    for (int 序数添字 = 0; 序数添字 < 項目個数; 序数添字++) {
                        int 値 = 命令データ.整数読取(); if (序数添字 > 0 && 値 <= 前面データ) throw new 翻訳エラー("switch 順序値 エラー"); 前面データ = 値;
                        分岐出力(出力, 分岐一覧, 位置, 命令データ.整数読取(), "(int32_t)a == (" + 値 + ")");
                    }
                }
                分岐出力(出力, 分岐一覧, 位置, 既定値, null);
            } else if (命令 == 172 || 命令 == 176 || 命令 == 177) 出力.add("return " + (命令 == 177 ? "0" : "POP()") + ";");
            else if (命令 == 178 || 命令 == 179) {
                メソッド参照 参照 = クラス値.参照(命令データ.短整数読取()); if (!フィールド一覧一覧.containsKey(参照)) throw new 翻訳エラー("알 数 없는 フィールド値");
                出力.add(記号("init", 参照.所有者値) + "();"); String フィールド値 = 記号("field", 参照.構成要素一覧());
                出力.add(命令 == 178 ? "PUSH(" + フィールド値 + ");" : フィールド値 + " = POP();");
            } else if (命令 == 184) {
                メソッド参照 参照 = クラス値.参照(命令データ.短整数読取()); if (!メソッド一覧一覧.containsKey(参照)) throw new 翻訳エラー("알 数 없는 関数");
                メソッド記述子 呼出状態型 = new メソッド記述子(参照.説明値); int 項目個数 = 呼出状態型.引数.size();
                出力.add(記号("init", 参照.所有者値) + "();"); 出力.add("if(sp < " + 項目個数 + ") kernel_panic(\"call stack underflow\"); sp -= " + 項目個数 + ";");
                List<String> 呼出状態引数列 = new ArrayList<>(); for (int 序数添字 = 0; 序数添字 < 項目個数; 序数添字++) 呼出状態引数列.add("s[sp + " + 序数添字 + "]");
                出力.add("a = " + 記号("method", 参照.構成要素一覧()) + "(" + String.join(",", 呼出状態引数列) + ");");
                if (!呼出状態型.復帰結果.equals("V")) 出力.add("PUSH(a);");
            } else if (命令 == 182) {
                メソッド参照 参照 = クラス値.参照(命令データ.短整数読取());
                if (参照.equals(new メソッド参照("java/lang/String", "length", "()I"))) 出力.add("a = POP(); PUSH(length(a));");
                else if (参照.equals(new メソッド参照("java/lang/String", "charAt", "(I)C"))) 出力.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new 翻訳エラー("가상 関数 呼出 判定未対応");
            } else if (命令 == 188) {
                if (命令データ.バイト読取() != 10) throw new 翻訳エラー("new int[]만 支援値"); 出力.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (命令 == 190) 出力.add("a = POP(); PUSH(length(a));");
            else if (命令 == 196) {
                int 拡張子値 = 命令データ.バイト読取(), 番号 = 命令データ.短整数読取(); 局所検査(番号, 局所変数個数);
                if (拡張子値 == 21 || 拡張子値 == 25) 出力.add("PUSH(l[" + 番号 + "]);");
                else if (拡張子値 == 54 || 拡張子値 == 58) 出力.add("l[" + 番号 + "] = POP();");
                else if (拡張子値 == 132) 出力.add("l[" + 番号 + "] = (uint32_t)l[" + 番号 + "] + (uint32_t)(" + 命令データ.符号付き短整数読取() + ");");
                else throw new 翻訳エラー("判定未対応 wide 命令");
            } else if (命令 == 198 || 命令 == 199) {
                出力.add("a = POP();"); 分岐出力(出力, 分岐一覧, 位置, 命令データ.符号付き短整数読取(), "a " + (命令 == 198 ? "==" : "!=") + " 0");
            } else throw new 翻訳エラー(関数.所有者値 + "." + 関数.名前 + ", バイト値 " + 位置 + ": 判定未対応 命令 " + 命令);
        }
        if (!境界一覧一覧.containsAll(分岐一覧)) throw new 翻訳エラー("命令 경계가 아닌 곳으로 分岐");
        出力.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 出力);
    }
    String 公開メソッド(String 連結記号, String 対象値, boolean 保有入口点) {
        int 位置添字 = 対象値.lastIndexOf('.'); if (位置添字 < 0 || !連結記号.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 翻訳エラー("値出力 代入値 エラー");
        String 所有者値 = 対象値.substring(0, 位置添字).replace('.', '/'), 名前 = 対象値.substring(位置添字 + 1); メソッド参照 選択状態値 = null;
        for (メソッド参照 参照 : メソッド一覧一覧.keySet()) if (参照.所有者値.equals(所有者値) && 参照.名前.equals(名前)) {
            if (選択状態値 != null) throw new 翻訳エラー("겹친 値出力 対象値"); 選択状態値 = 参照;
        }
        if (選択状態値 == null || (メソッド一覧一覧.get(選択状態値).アクセス入口 & 0x100) != 0) throw new 翻訳エラー("내보낼 함수가 未存在メソッド 또는 native 関数");
        メソッド記述子 書式値 = new メソッド記述子(選択状態値.説明値);
        if ((保有入口点 && !書式値.引数.isEmpty()) || !Arrays.asList("V", "I").contains(書式値.復帰結果)) throw new 翻訳エラー("入口点値 또는 C 境界位置値 書式値 エラー");
        List<String> 引数列一覧 = new ArrayList<>(), 呼出状態引数列 = new ArrayList<>();
        for (int 序数添字 = 0; 序数添字 < 書式値.引数.size(); 序数添字++) {
            if (!書式値.引数.get(序数添字).equals("I")) throw new 翻訳エラー("C 경계는 int 인수만 支援値");
            引数列一覧.add("int32_t a" + 序数添字); 呼出状態引数列.add("(uint32_t)a" + 序数添字);
        }
        return (書式値.復帰結果.equals("V") ? "void " : "int32_t ") + 連結記号 + "(" + (引数列一覧.isEmpty() ? "void" : String.join(",", 引数列一覧)) + ") { " + 記号("init", 選択状態値.所有者値) + "(); " + (書式値.復帰結果.equals("V") ? "" : "return (int32_t)") + 記号("method", 選択状態値.構成要素一覧()) + "(" + String.join(",", 呼出状態引数列) + "); }";
    }
    String 生成(String 入口点, List<String> 公開登録項目一覧, boolean 汎用表記) throws IOException {
        List<String> 宣言一覧一覧 = new ArrayList<>(), 本体一覧一覧 = new ArrayList<>(), フィールド宣言一覧 = new ArrayList<>();
        for (Map.Entry<メソッド参照, 成員データ> 入口値 : メソッド一覧一覧.entrySet()) {
            メソッド参照 参照 = 入口値.getKey(); 成員データ データ = 入口値.getValue(); 宣言一覧一覧.add(メソッド原型(参照) + ";");
            if ((データ.アクセス入口 & 0x100) != 0) {
                String 接続 = 機械関数一覧.get(参照.名前 + 参照.説明値);
                if (!参照.所有者値.equals(機械クラス) || 接続 == null) throw new 翻訳エラー("허용되지 않은 native 関数: " + 参照.名前);
                int 項目個数 = new メソッド記述子(参照.説明値).引数.size(); List<String> 引数列一覧 = new ArrayList<>();
                for (int 序数添字 = 0; 序数添字 < 項目個数; 序数添字++) 引数列一覧.add("a" + 序数添字);
                宣言一覧一覧.add("extern word " + 接続 + "(" + (項目個数 == 0 ? "void" : String.join(",", Collections.nCopies(項目個数, "word"))) + ");");
                本体一覧一覧.add(メソッド原型(参照) + " { return " + 接続 + "(" + String.join(",", 引数列一覧) + "); }");
            } else 本体一覧一覧.add(メソッド本体(参照, データ));
        }
        for (Map.Entry<メソッド参照, 成員データ> 入口値 : フィールド一覧一覧.entrySet()) {
            メソッド参照 参照 = 入口値.getKey(); byte[] 定数値 = 入口値.getValue().属性値.get("ConstantValue");
            String 値 = 定数値 == null ? "0" : 定数式(クラス群一覧.get(参照.所有者値), new データ読取器(定数値).短整数読取());
            フィールド宣言一覧.add("static word " + 記号("field", 参照.構成要素一覧()) + " = " + 値 + ";");
        }
        for (String 名前 : クラス群一覧.keySet()) {
            String 初期化 = 記号("init", 名前), 状況値 = 記号("state", 名前);
            宣言一覧一覧.add("static void " + 初期化 + "(void);"); フィールド宣言一覧.add("static unsigned " + 状況値 + ";");
            メソッド参照 参照 = new メソッド参照(名前, "<clinit>", "()V");
            本体一覧一覧.add("static void " + 初期化 + "(void) { if(" + 状況値 + ") return; " + 状況値 + " = 1; " + (メソッド一覧一覧.containsKey(参照) ? 記号("method", 参照.構成要素一覧()) + "(); " : "") + 状況値 + " = 2; }");
        }
        本体一覧一覧.add(公開メソッド("java_entry", 入口点, true)); Set<String> 公開済み名前 = new HashSet<>();
        for (String 代入値 : 公開登録項目一覧) {
            int 位置添字 = 代入値.indexOf('='); if (位置添字 < 1) throw new 翻訳エラー("値出力 代入値 エラー");
            String 名前 = 代入値.substring(0, 位置添字); 公開済み名前.add(名前); 本体一覧一覧.add(公開メソッド(名前, 代入値.substring(位置添字 + 1), false));
        }
        List<String> 文字列宣言一覧 = new ArrayList<>();
        for (Map.Entry<String, String> 入口値 : 文字列値一覧.entrySet()) {
            String 文 = 入口値.getKey(); StringBuilder 配列値 = new StringBuilder("static const word " + 入口値.getValue() + "[] = {" + 文.length());
            for (int 序数添字 = 0; 序数添字 < 文.length(); 序数添字++) 配列値.append(", ").append((int)文.charAt(序数添字));
            文字列宣言一覧.add(配列値.append("};").toString());
        }
        String 支援値 = Files.readString(資源経路.resolve("実行環境支援.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(ヒープ語個数));
        return 生成済みソース現地語化(支援値 + String.join("\n", 文字列宣言一覧) + "\n" + String.join("\n", 宣言一覧一覧) + "\n" + String.join("\n", フィールド宣言一覧) + "\n" + String.join("\n", 本体一覧一覧) + "\n", 公開済み名前, 汎用表記);
    }
    String 生成済みソース現地語化(String ソース, Set<String> 公開済み名前, boolean 汎用表記) throws IOException {
        Map<String, String> 名前表 = new HashMap<>();
        for (String 行 : Files.readAllLines(資源経路.resolve("生成済み名前一覧.tsv"), StandardCharsets.UTF_8)) {
            String[] 対値 = 行.split("\t"); 名前表.put(対値[0], 対値[1]);
        }
        Pattern 断片要素式 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 探索器値 = 断片要素式.matcher(ソース); StringBuffer 結果 = new StringBuffer();
        while (探索器値.find()) {
            String 名前 = 探索器値.group(), 新規名前 = 名前;
            if (!名前.startsWith("//") && !名前.startsWith("/*") && !名前.startsWith("\"") && !名前.startsWith("'") && !公開済み名前.contains(名前)) {
                新規名前 = 名前表.getOrDefault(名前, 名前);
                if (名前.matches("a[0-9]+")) 新規名前 = "引数" + 名前.substring(1);
                if (名前.matches("b[0-9]+")) 新規名前 = "分岐" + 名前.substring(1);
                if (汎用表記) {
                    StringBuilder 表記値 = new StringBuilder();
                    for (char 文字値 : 新規名前.toCharArray()) 表記値.append(文字値 < 128 ? Character.toString(文字値) : String.format(Locale.ROOT, "\\u%04x", (int)文字値));
                    新規名前 = 表記値.toString();
                }
            }
            探索器値.appendReplacement(結果, Matcher.quoteReplacement(新規名前));
        }
        探索器値.appendTail(結果); return 結果.toString();
    }
    String x86メソッド本体(メソッド参照 関数, 成員データ データ, Map<String,String> 機械表, String 対象値) {
        String 標識値 = 記号("method", 関数.構成要素一覧());
        List<String> 行 = new ArrayList<>();
        if ((データ.アクセス入口 & 0x100) != 0) {
            String 接続 = 機械表.get(関数.名前 + 関数.説明値);
            if (!関数.所有者値.equals(対象値.equals("kernel") ? "装置" : "利用者") || 接続 == null) throw new 翻訳エラー("허용되지 않은 native 関数");
            return ".text\n" + 標識値 + ":\njmp " + 接続;
        }
        byte[] 本体本文 = データ.属性値.get("Code"); if (本体本文 == null) throw new 翻訳エラー("関数 몸체가 未存在メソッド");
        データ読取器 読取器値 = new データ読取器(本体本文); 読取器値.短整数読取(); int 局所個数 = 読取器値.短整数読取();
        データ読取器 命令データ = new データ読取器(読取器値.読取(読取器値.整数読取()));
        if (読取器値.短整数読取() != 0) throw new 翻訳エラー("try/catch/finally 判定未対応");
        メソッド記述子 書式値 = new メソッド記述子(関数.説明値); if (局所個数 < 書式値.引数.size()) throw new 翻訳エラー("매개변수보다 적은 局所有効範囲 変数値");
        Collections.addAll(行,".text",".globl " + 標識値,".type " + 標識値 + ", @function",標識値 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 局所個数 * 4 + ", %esp");
        for (int 序数添字 = 0; 序数添字 < 書式値.引数.size(); 序数添字++) Collections.addAll(行,"movl " + (8 + 4 * (書式値.引数.size() - 序数添字 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (序数添字 + 1)) + "(%ebp)");
        クラスデータ クラス値 = クラス群一覧.get(関数.所有者値); Set<Integer> 境界一覧一覧 = new HashSet<>(), 分岐一覧 = new HashSet<>();
        String[] 比較一覧一覧 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (命令データ.位置 < 命令データ.データ.length) {
            int 位置 = 命令データ.位置, 命令 = 命令データ.バイト読取(); String 位置添字 = 標識値 + "_b" + 位置;
            行.add(位置添字 + ":"); 境界一覧一覧.add(位置);
            if (命令 == 0) 行.add("nop");
            else if (命令 == 1) 行.add("pushl $0");
            else if (命令 >= 2 && 命令 <= 8) 行.add("pushl $" + (命令 - 3));
            else if (命令 == 16 || 命令 == 17) 行.add("pushl $" + (命令 == 16 ? 命令データ.符号付きバイト読取() : 命令データ.符号付き短整数読取()));
            else if (命令 == 18 || 命令 == 19) {
                int 番号 = 命令 == 18 ? 命令データ.バイト読取() : 命令データ.短整数読取();
                行.add("pushl $" + x86定数(クラス値,番号));
            } else if (命令 == 21 || 命令 == 25 || (命令 >= 26 && 命令 <= 29) || (命令 >= 42 && 命令 <= 45) || 命令 == 54 || 命令 == 58 || (命令 >= 59 && 命令 <= 62) || (命令 >= 75 && 命令 <= 78)) {
                boolean 結果読取 = 命令 < 54; int 番号 = 命令 == 21 || 命令 == 25 || 命令 == 54 || 命令 == 58 ? 命令データ.バイト読取() : 命令 - (命令 <= 29 ? 26 : 命令 <= 45 ? 42 : 命令 <= 62 ? 59 : 75);
                局所検査(番号,局所個数); 行.add((結果読取 ? "pushl " : "popl ") + "-" + (4 * (番号 + 1)) + "(%ebp)");
            } else if (命令 == 46) Collections.addAll(行,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (命令 == 79) Collections.addAll(行,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (命令 == 87 || 命令 == 88) 行.add("addl $" + (命令 == 87 ? 4 : 8) + ", %esp");
            else if (命令 >= 89 && 命令 <= 95) {
                int[] 項目個数一覧 = {1,2,3,2,3,4,2}; int[][] 順序一覧 = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 値一覧レジスタ = {"%eax","%ecx","%edx","%ebx"};
                for (int 序数添字 = 0; 序数添字 < 項目個数一覧[命令 - 89]; 序数添字++) 行.add("popl " + 値一覧レジスタ[序数添字]);
                for (int 序数添字 : 順序一覧[命令 - 89]) 行.add("pushl " + 値一覧レジスタ[序数添字]);
            } else if (命令 == 96 || 命令 == 100 || 命令 == 104 || 命令 == 126 || 命令 == 128 || 命令 == 130) {
                String 操作値 = 命令 == 96 ? "addl" : 命令 == 100 ? "subl" : 命令 == 104 ? "imull" : 命令 == 126 ? "andl" : 命令 == 128 ? "orl" : "xorl";
                Collections.addAll(行,"popl %ecx","popl %eax",操作値 + " %ecx, %eax","pushl %eax");
            } else if (命令 == 108 || 命令 == 112) Collections.addAll(行,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 位置添字 + "_divide","cmpl $0x80000000, %eax","jne " + 位置添字 + "_divide","xorl %edx, %edx","jmp " + 位置添字 + "_done",位置添字 + "_divide:","cltd","idivl %ecx",位置添字 + "_done:","pushl " + (命令 == 108 ? "%eax" : "%edx"));
            else if (命令 == 116) 行.add("negl (%esp)");
            else if (命令 == 120 || 命令 == 122 || 命令 == 124) Collections.addAll(行,"popl %ecx","popl %eax",(命令 == 120 ? "sall" : 命令 == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (命令 == 132) {
                int 番号 = 命令データ.バイト読取(), 増分値 = 命令データ.符号付きバイト読取(); 局所検査(番号,局所個数); 行.add("addl $" + 増分値 + ", -" + (4 * (番号 + 1)) + "(%ebp)");
            } else if (命令 >= 145 && 命令 <= 147) Collections.addAll(行,"popl %eax",命令 == 145 ? "movsbl %al, %eax" : 命令 == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (命令 >= 153 && 命令 <= 166) {
                if (命令 <= 158) Collections.addAll(行,"popl %eax","testl %eax, %eax");
                else Collections.addAll(行,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int 宛先値 = 位置 + 命令データ.符号付き短整数読取(); 分岐一覧.add(宛先値); 行.add(比較一覧一覧[命令 - (命令 <= 158 ? 153 : 159)] + " " + 標識値 + "_b" + 宛先値);
            } else if (命令 == 167 || 命令 == 200) {
                int 宛先値 = 位置 + (命令 == 167 ? 命令データ.符号付き短整数読取() : 命令データ.整数読取()); 分岐一覧.add(宛先値); 行.add("jmp " + 標識値 + "_b" + 宛先値);
            } else if (命令 == 170 || 命令 == 171) {
                while (命令データ.位置 % 4 != 0) 命令データ.バイト読取();
                int 既定値 = 位置 + 命令データ.整数読取(); 分岐一覧.add(既定値); 行.add("popl %eax");
                int 項目個数, 下端値 = 0;
                if (命令 == 170) { 下端値 = 命令データ.整数読取(); int 上端値 = 命令データ.整数読取(); long 長さ = (long)上端値 - 下端値 + 1; if (長さ < 1 || 長さ > (命令データ.データ.length - 命令データ.位置) / 4) throw new 翻訳エラー("switch 切抜き エラー"); 項目個数 = (int)長さ; }
                else { 項目個数 = 命令データ.整数読取(); if (項目個数 < 0 || 項目個数 > (命令データ.データ.length - 命令データ.位置) / 8) throw new 翻訳エラー("switch 容量 エラー"); }
                for (int 序数添字 = 0; 序数添字 < 項目個数; 序数添字++) {
                    int 値 = 命令 == 170 ? 下端値 + 序数添字 : 命令データ.整数読取(), 宛先値 = 位置 + 命令データ.整数読取(); 分岐一覧.add(宛先値);
                    Collections.addAll(行,"cmpl $" + 値 + ", %eax","je " + 標識値 + "_b" + 宛先値);
                }
                行.add("jmp " + 標識値 + "_b" + 既定値);
            } else if (命令 == 172 || 命令 == 176 || 命令 == 177) {
                if (命令 != 177) 行.add("popl %eax"); Collections.addAll(行,"leave","ret");
            } else if (命令 == 178 || 命令 == 179) {
                メソッド参照 参照 = クラス値.参照(命令データ.短整数読取()); if (!フィールド一覧一覧.containsKey(参照)) throw new 翻訳エラー("알 数 없는 フィールド値");
                Collections.addAll(行,"call " + 記号("init",参照.所有者値),(命令 == 178 ? "pushl " : "popl ") + 記号("field",参照.構成要素一覧()));
            } else if (命令 == 184) {
                メソッド参照 参照 = クラス値.参照(命令データ.短整数読取()); if (!メソッド一覧一覧.containsKey(参照)) throw new 翻訳エラー("알 数 없는 関数");
                メソッド記述子 呼出状態型 = new メソッド記述子(参照.説明値); Collections.addAll(行,"call " + 記号("init",参照.所有者値),"call " + 記号("method",参照.構成要素一覧()));
                if (!呼出状態型.引数.isEmpty()) 行.add("addl $" + 呼出状態型.引数.size() * 4 + ", %esp");
                if (!呼出状態型.復帰結果.equals("V")) 行.add("pushl %eax");
            } else if (命令 == 182) {
                メソッド参照 参照 = クラス値.参照(命令データ.短整数読取());
                if (参照.equals(new メソッド参照("java/lang/String","length","()I"))) Collections.addAll(行,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (参照.equals(new メソッド参照("java/lang/String","charAt","(I)C"))) Collections.addAll(行,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new 翻訳エラー("가상 関数 呼出 判定未対応");
            } else if (命令 == 188) {
                if (命令データ.バイト読取() != 10) throw new 翻訳エラー("new int[]만 支援値"); Collections.addAll(行,"popl %eax","call rt_new_array","pushl %eax");
            } else if (命令 == 190) Collections.addAll(行,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (命令 == 196) {
                int 拡張子値 = 命令データ.バイト読取(), 番号 = 命令データ.短整数読取(); 局所検査(番号,局所個数);
                if (拡張子値 == 21 || 拡張子値 == 25 || 拡張子値 == 54 || 拡張子値 == 58) 行.add((拡張子値 <= 25 ? "pushl " : "popl ") + "-" + 4 * (番号 + 1) + "(%ebp)");
                else if (拡張子値 == 132) 行.add("addl $" + 命令データ.符号付き短整数読取() + ", -" + 4 * (番号 + 1) + "(%ebp)");
                else throw new 翻訳エラー("wide 命令 判定未対応");
            } else if (命令 == 198 || 命令 == 199) {
                int 宛先値 = 位置 + 命令データ.符号付き短整数読取(); 分岐一覧.add(宛先値); Collections.addAll(行,"popl %eax","testl %eax, %eax",(命令 == 198 ? "je " : "jne ") + 標識値 + "_b" + 宛先値);
            } else throw new 翻訳エラー("判定未対応 命令: " + 命令);
        }
        if (!境界一覧一覧.containsAll(分岐一覧)) throw new 翻訳エラー("命令 경계가 아닌 곳으로 分岐");
        行.add(".size " + 標識値 + ", .-" + 標識値); return String.join("\n",行);
    }
    String x86定数(クラスデータ データ, int 番号) {
        if (データ.定数種別[番号] == 3) return データ.定数データ[番号].toString();
        if (データ.定数種別[番号] == 8) return 文字列記号(データ.文字((Integer)データ.定数データ[番号]));
        throw new 翻訳エラー("정수와 文字列 상수만 支援値");
    }
    String x86アセンブリ(String 入口点, List<String> 公開済み値, String 対象値) throws IOException {
        Map<String,String> 機械表 = new HashMap<>();
        for (String 行 : Files.readAllLines(資源経路.resolve("x86機械関数.tsv"))) { String[] 対値 = 行.split("\t"); if (対値[0].equals(対象値)) 機械表.put(対値[1] + 対値[2],対値[3]); }
        int 位置添字 = 入口点.lastIndexOf('.'); if (位置添字 < 0) throw new 翻訳エラー("入口点 代入値 エラー");
        String 所有者値 = 入口点.substring(0,位置添字).replace('.','/'), メソッド入口名前 = 入口点.substring(位置添字 + 1); メソッド参照 入口点値 = null;
        for (String 説明値 : Arrays.asList("()I","()V")) { メソッド参照 参照 = new メソッド参照(所有者値,メソッド入口名前,説明値); if (メソッド一覧一覧.containsKey(参照)) { if (入口点値 != null) throw new 翻訳エラー("겹친 入口点"); 入口点値 = 参照; } }
        if (入口点値 == null || (メソッド一覧一覧.get(入口点値).アクセス入口 & 0x100) != 0) throw new 翻訳エラー("入口点値 関数 書式値 エラー");
        List<String> 行 = new ArrayList<>(); 行.add(".code32");
        for (クラスデータ データ : クラス群一覧.values()) {
            String 状況値 = 記号("state",データ.名前), 初期化 = 記号("init",データ.名前);
            Collections.addAll(行,".bss",".balign 4",状況値 + ": .long 0",".text",初期化 + ":","cmpl $0, " + 状況値,"jne " + 初期化 + "_done","movl $1, " + 状況値);
            メソッド参照 初期設定器参照 = new メソッド参照(データ.名前,"<clinit>","()V"); if (メソッド一覧一覧.containsKey(初期設定器参照)) 行.add("call " + 記号("method",初期設定器参照.構成要素一覧()));
            Collections.addAll(行,"movl $2, " + 状況値,初期化 + "_done:","ret");
            for (成員データ フィールド値 : データ.フィールド値) {
                byte[] 定数値 = フィールド値.属性値.get("ConstantValue"); String 値 = 定数値 == null ? "0" : x86定数(データ,new データ読取器(定数値).短整数読取());
                Collections.addAll(行,".data",".balign 4",記号("field",データ.名前,フィールド値.名前,フィールド値.説明値) + ": .long " + 値);
            }
            for (成員データ 関数 : データ.関数) if (!関数.名前.equals("<init>")) 行.add(x86メソッド本体(new メソッド参照(データ.名前,関数.名前,関数.説明値),関数,機械表,対象値));
        }
        Collections.addAll(行,".text",".globl java_entry","java_entry:","call " + 記号("init",入口点値.所有者値),"call " + 記号("method",入口点値.構成要素一覧()));
        if (入口点値.説明値.equals("()V")) 行.add("xorl %eax, %eax"); 行.add("ret");
        for (String 代入値 : 公開済み値) {
            int 区切り記号値 = 代入値.indexOf('='); if (区切り記号値 < 1) throw new 翻訳エラー("値出力 代入値 エラー");
            String 外部値 = 代入値.substring(0,区切り記号値), 関数 = 代入値.substring(区切り記号値 + 1); int 除算結果 = 関数.lastIndexOf('.');
            if (除算結果 < 0 || !外部値.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 翻訳エラー("値出力 記号 エラー");
            String クラス値 = 関数.substring(0,除算結果).replace('.','/'), 名前 = 関数.substring(除算結果 + 1); メソッド参照 選択状態値 = null;
            for (メソッド参照 参照 : メソッド一覧一覧.keySet()) if (参照.所有者値.equals(クラス値) && 参照.名前.equals(名前)) { if (選択状態値 != null) throw new 翻訳エラー("겹친 値出力 対象値"); 選択状態値 = 参照; }
            if (選択状態値 == null) throw new 翻訳エラー("내보낼 함수가 未存在メソッド");
            Collections.addAll(行,".text",".globl " + 外部値,外部値 + ":","call " + 記号("init",選択状態値.所有者値),"jmp " + 記号("method",選択状態値.構成要素一覧()));
        }
        行.add(".section .rodata");
        for (Map.Entry<String,String> 入口値 : 文字列値一覧.entrySet()) {
            Collections.addAll(行,".balign 4",入口値.getValue() + ":",".long " + 入口値.getKey().length());
            List<String> 単位一覧一覧 = new ArrayList<>(); for (char 単位値 : 入口値.getKey().toCharArray()) 単位一覧一覧.add(Integer.toString(単位値)); if (!単位一覧一覧.isEmpty()) 行.add(".long " + String.join(",",単位一覧一覧));
        }
        行.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",行) + "\n";
    }
    static void 道具要素実行(List<String> 命令) throws Exception {
        if (new ProcessBuilder(命令).inheritIO().start().waitFor() != 0) throw new 翻訳エラー("ソースコンパイル エラー: " + 命令.get(0));
    }
    static String データ文字列(String 文) { return "\"" + 文.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void x86翻訳結果(List<Path> 入力一覧, String 対象値, String 入口点, List<String> 公開済み値, Path 出力, Path 資源値) throws Exception {
        Path 一時値 = Files.createTempDirectory("jkoros-java-x86-"), クラス経路 = 一時値.resolve("classes"); Files.createDirectory(クラス経路);
        try {
            List<String> Java命令 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",クラス経路.toString(),"-sourcepath",クラス経路.toString(),"-d",クラス経路.toString()));
            List<Path> バイトコード = new ArrayList<>(); int ソース個数 = 0;
            for (Path 入力値 : 入力一覧) {
                if (出力.toAbsolutePath().normalize().equals(入力値.toAbsolutePath().normalize())) throw new 翻訳エラー("出力 파일과 입력이 等価本文");
                if (入力値.toString().endsWith(".java")) { Java命令.add(入力値.toString()); ソース個数++; }
                else if (入力値.toString().endsWith(".class")) バイトコード.add(入力値);
                else throw new 翻訳エラー(".java 또는 .class만 支援値");
            }
            if (ソース個数 > 0) 道具要素実行(Java命令);
            try (java.util.stream.Stream<Path> 経路一覧 = Files.walk(クラス経路)) { 経路一覧.filter(経路 -> 経路.toString().endsWith(".class")).sorted().forEach(バイトコード::add); }
            事前用時間コンパイラ 値変換 = new 事前用時間コンパイラ(バイトコード,対象値.equals("user") ? "user" : "kernel",262144,資源値);
            String 値組立て = 値変換.x86アセンブリ(入口点,公開済み値,対象値); Files.writeString(一時値.resolve("program.s"),値組立て,StandardCharsets.UTF_8);
            Path 道具要素位置 = 資源値.getParent();
            道具要素実行(Arrays.asList("as","--32","-o",一時値.resolve("program.o").toString(),一時値.resolve("program.s").toString()));
            道具要素実行(Arrays.asList("as","--32","-o",一時値.resolve("runtime.o").toString(),道具要素位置.resolve("実行環境支援.s").toString()));
            List<String> 接続 = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (対象値.equals("kernel")) 接続.add("-r");
            else {
                道具要素実行(Arrays.asList("as","--32","-o",一時値.resolve("start.o").toString(),道具要素位置.resolve(対象値.equals("user") ? "利用者プログラム開始処理.s" : "Linux始動.s").toString()));
                Collections.addAll(接続,"-e","_start",一時値.resolve("start.o").toString());
                if (対象値.equals("user")) Collections.addAll(接続,"-T",道具要素位置.resolve("利用者連結配置.ld").toString());
            }
            Collections.addAll(接続,"-o",一時値.resolve("result").toString(),一時値.resolve("program.o").toString(),一時値.resolve("runtime.o").toString()); 道具要素実行(接続);
            出力 = 出力.toAbsolutePath(); Files.createDirectories(出力.getParent()); Path 公表値 = Files.createTempFile(出力.getParent(),".elf-",".tmp");
            try { Files.copy(一時値.resolve("result"),公表値,StandardCopyOption.REPLACE_EXISTING); Files.move(公表値,出力,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(公表値); }
            Files.setPosixFilePermissions(出力,java.nio.file.attribute.PosixFilePermissions.fromString(対象値.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(出力 + ".s"),値組立て,StandardCharsets.UTF_8);
            List<String> 記号データ = new ArrayList<>(), ソースデータ = new ArrayList<>();
            for (メソッド参照 参照 : 値変換.メソッド一覧一覧.keySet()) 記号データ.add(データ文字列(記号("method",参照.構成要素一覧())) + ":" + データ文字列(参照.所有者値 + "." + 参照.名前 + 参照.説明値));
            for (Path 入力値 : 入力一覧) {
                byte[] ハッシュファイル = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(入力値)); StringBuilder 文 = new StringBuilder(); for (byte 値 : ハッシュファイル) 文.append(String.format(Locale.ROOT,"%02x",値 & 255));
                ソースデータ.add(データ文字列(入力値.toAbsolutePath().toString()) + ":" + データ文字列(文.toString()));
            }
            Files.writeString(Paths.get(出力 + ".json"),"{\"target\":" + データ文字列(対象値) + ",\"entry\":" + データ文字列(入口点) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",記号データ) + "},\"sources\":{" + String.join(",",ソースデータ) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> 経路一覧 = Files.walk(一時値)) { for (Path 経路 : (Iterable<Path>)経路一覧.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(経路); }
        }
    }
    public static void main(String[] 引数) {
        try {
            String 入口点 = null, 対象値 = "kernel", x86翻訳対象 = null; Path 出力経路 = null; int 字句用語個数 = 262144; boolean 汎用表記 = false;
            List<String> 公開済み値 = new ArrayList<>(); List<Path> 経路一覧 = new ArrayList<>();
            for (int 序数添字 = 0; 序数添字 < 引数.length; 序数添字++) {
                String 値 = 引数[序数添字];
                switch (値) {
                    case "--target": x86翻訳対象 = 引数[++序数添字]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry クラス値.関数 -o 出力 [--target linux|kernel|user] [--profile kernel|user] [--export 記号=クラス値.関数] 클래스파일 또는 Java원문"); return;
                    case "--entry": 入口点 = 引数[++序数添字]; break;
                    case "--profile": 対象値 = 引数[++序数添字]; break;
                    case "--heap-words": 字句用語個数 = Integer.parseInt(引数[++序数添字]); break;
                    case "--export": 公開済み値.add(引数[++序数添字]); break;
                    case "-o": 出力経路 = Paths.get(引数[++序数添字]); break;
                    case "--ucn": 汎用表記 = true; break;
                    default: if (値.startsWith("-")) throw new 翻訳エラー("알 数 없는 옵션: " + 値); 経路一覧.add(Paths.get(値));
                }
            }
            if (入口点 == null || 出力経路 == null || 経路一覧.isEmpty()) throw new 翻訳エラー("--entry, -o, クラス値 파일이 필요합니다");
            Path 資源値 = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (x86翻訳対象 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(x86翻訳対象)) throw new 翻訳エラー("알 数 없는 命令実行 対象値");
                x86翻訳結果(経路一覧,x86翻訳対象,入口点,公開済み値,出力経路,資源値); return;
            }
            String ソース = new 事前用時間コンパイラ(経路一覧, 対象値, 字句用語個数, 資源値).生成(入口点, 公開済み値, 汎用表記);
            出力経路 = 出力経路.toAbsolutePath(); Files.createDirectories(出力経路.getParent());
            Path 一時値 = Files.createTempFile(出力経路.getParent(), ".aot-", ".tmp");
            try { Files.writeString(一時値, ソース, StandardCharsets.UTF_8); Files.move(一時値, 出力経路, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(一時値); }
        } catch (Exception エラー) { System.err.println("ソースコンパイル エラー: " + エラー.getMessage()); System.exit(1); }
    }
}
