// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** 從 Java 類別檔產生獨立 ARM64 核心的 C 原始碼，在主機 JDK 上執行。 */
public final class 提前所屬時間編譯器 {
    static final class 翻譯錯誤 extends RuntimeException {
        翻譯錯誤(String 說明) { super(說明); }
    }
    static final class 資料讀取器 {
        final byte[] 資料;
        int 位置;
        資料讀取器(byte[] 輸入資料) { 資料 = 輸入資料; }
        byte[] 讀取(int 長度) {
            if (長度 < 0 || 長度 > 資料.length - 位置) throw new 翻譯錯誤("已裁剪值 類別值 또는 命令 資料");
            byte[] 結果 = Arrays.copyOfRange(資料, 位置, 位置 + 長度); 位置 += 長度; return 結果;
        }
        int 讀取位元組() { if (位置 >= 資料.length) throw new 翻譯錯誤("已裁剪值 命令 資料"); return 資料[位置++] & 255; }
        int 讀取短整數() { return (讀取位元組() << 8) | 讀取位元組(); }
        int 讀取整數() { return (讀取短整數() << 16) | 讀取短整數(); }
        int 讀取有符號位元組() { return (byte) 讀取位元組(); }
        int 讀取有符號短整數() { return (short) 讀取短整數(); }
    }
    static final class 成員資料 {
        final int 存取條目;
        final String 名稱, 說明值;
        final Map<String, byte[]> 屬性值;
        成員資料(int 存取值, String 名稱值, String 描述符資料, Map<String, byte[]> 屬性資料) {
            存取條目 = 存取值; 名稱 = 名稱值; 說明值 = 描述符資料; 屬性值 = 屬性資料;
        }
    }
    static final class 方法引用 implements Comparable<方法引用> {
        final String 所有者值, 名稱, 說明值;
        方法引用(String 自有值, String 名稱值, String 描述符資料) { 所有者值 = 自有值; 名稱 = 名稱值; 說明值 = 描述符資料; }
        String[] 部件列() { return new String[]{所有者值, 名稱, 說明值}; }
        public int compareTo(方法引用 對端值) {
            int 比較值 = 所有者值.compareTo(對端值.所有者值);
            if (比較值 == 0) 比較值 = 名稱.compareTo(對端值.名稱);
            return 比較值 == 0 ? 說明值.compareTo(對端值.說明值) : 比較值;
        }
        public boolean equals(Object 對端值) { return 對端值 instanceof 方法引用 && compareTo((方法引用) 對端值) == 0; }
        public int hashCode() { return Objects.hash(所有者值, 名稱, 說明值); }
    }
    static final class 類別資料 {
        final int[] 常量種類;
        final Object[] 常量資料;
        final String 名稱;
        final List<成員資料> 字段值, 函數;
        類別資料(Path 路徑) throws IOException {
            資料讀取器 讀取器值 = new 資料讀取器(Files.readAllBytes(路徑));
            if (讀取器值.讀取整數() != 0xcafebabe) throw new 翻譯錯誤("Java 類別值 표식이 아님");
            讀取器值.讀取(4);
            int 項目個數 = 讀取器值.讀取短整數(); 常量種類 = new int[項目個數]; 常量資料 = new Object[項目個數];
            for (int 序數索引 = 1; 序數索引 < 項目個數; 序數索引++) {
                int 種類值 = 讀取器值.讀取位元組(); 常量種類[序數索引] = 種類值;
                switch (種類值) {
                    case 1:
                        int 長度 = 讀取器值.讀取短整數();
                        byte[] 字元緩衝區 = 讀取器值.讀取(長度), 長度帶前綴資料 = new byte[長度 + 2];
                        長度帶前綴資料[0] = (byte)(長度 >> 8); 長度帶前綴資料[1] = (byte)長度;
                        System.arraycopy(字元緩衝區, 0, 長度帶前綴資料, 2, 長度);
                        常量資料[序數索引] = new DataInputStream(new ByteArrayInputStream(長度帶前綴資料)).readUTF(); break;
                    case 3: 常量資料[序數索引] = 讀取器值.讀取整數(); break;
                    case 4: 讀取器值.讀取(4); break;
                    case 5: case 6: 讀取器值.讀取(8); 序數索引++; break;
                    case 7: case 8: case 16: 常量資料[序數索引] = 讀取器值.讀取短整數(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        常量資料[序數索引] = new int[]{讀取器值.讀取短整數(), 讀取器值.讀取短整數()}; break;
                    case 15: 常量資料[序數索引] = new int[]{讀取器值.讀取位元組(), 讀取器值.讀取短整數()}; break;
                    default: throw new 翻譯錯誤("지원하지 않는 常量值 種類值: " + 種類值);
                }
            }
            讀取器值.讀取短整數(); 名稱 = 類別名稱(讀取器值.讀取短整數());
            if (!類別名稱(讀取器值.讀取短整數()).equals("java/lang/Object") || 讀取器值.讀取短整數() != 0)
                throw new 翻譯錯誤(名稱 + ": 상속 및 인터페이스 是否不支持");
            字段值 = 讀取成員列(讀取器值); 函數 = 讀取成員列(讀取器值); 讀取屬性集(讀取器值);
            if (讀取器值.位置 != 讀取器值.資料.length) throw new 翻譯錯誤("類別值 뒤에 남은 資料");
        }
        String 字元(int 編號) {
            if (編號 < 1 || 編號 >= 常量種類.length || 常量種類[編號] != 1) throw new 翻譯錯誤("字元 常量值 編號 錯誤");
            return (String) 常量資料[編號];
        }
        String 類別名稱(int 編號) {
            if (編號 < 1 || 編號 >= 常量種類.length || 常量種類[編號] != 7) throw new 翻譯錯誤("類別值 引用 錯誤");
            return 字元((Integer)常量資料[編號]);
        }
        方法引用 引用(int 編號) {
            if (編號 < 1 || 編號 >= 常量種類.length || 常量種類[編號] < 9 || 常量種類[編號] > 11) throw new 翻譯錯誤("멤버 引用 錯誤");
            int[] 一對值 = (int[])常量資料[編號], 名稱一對 = (int[])常量資料[一對值[1]];
            return new 方法引用(類別名稱(一對值[0]), 字元(名稱一對[0]), 字元(名稱一對[1]));
        }
        Map<String, byte[]> 讀取屬性集(資料讀取器 讀取器值) {
            Map<String, byte[]> 結果 = new LinkedHashMap<>();
            int 項目個數 = 讀取器值.讀取短整數();
            for (int 序數索引 = 0; 序數索引 < 項目個數; 序數索引++) {
                String 屬性名稱 = 字元(讀取器值.讀取短整數()); byte[] 值 = 讀取器值.讀取(讀取器值.讀取整數());
                if (結果.put(屬性名稱, 值) != null) throw new 翻譯錯誤("겹친 屬性值: " + 屬性名稱);
            }
            return 結果;
        }
        List<成員資料> 讀取成員列(資料讀取器 讀取器值) {
            List<成員資料> 結果 = new ArrayList<>(); int 項目個數 = 讀取器值.讀取短整數();
            for (int 序數索引 = 0; 序數索引 < 項目個數; 序數索引++) {
                int 存取條目 = 讀取器值.讀取短整數(); String 方法條目名稱 = 字元(讀取器值.讀取短整數()), 說明值 = 字元(讀取器值.讀取短整數());
                結果.add(new 成員資料(存取條目, 方法條目名稱, 說明值, 讀取屬性集(讀取器值)));
            }
            return 結果;
        }
    }
    static final class 方法描述符 {
        final List<String> 實參 = new ArrayList<>();
        final String 發回結果;
        方法描述符(String 說明值) {
            if (!說明值.startsWith("(")) throw new 翻譯錯誤("函數 說明值 錯誤: " + 說明值);
            int 結尾 = 說明值.indexOf(')'); if (結尾 < 0) throw new 翻譯錯誤("函數 說明值 錯誤: " + 說明值);
            實參.addAll(解析類型列(說明值.substring(1, 結尾)));
            List<String> 已返回值列 = 解析類型列(說明值.substring(結尾 + 1));
            if (實參.contains("V") || 已返回值列.size() != 1) throw new 翻譯錯誤("函數 說明值 錯誤: " + 說明值);
            發回結果 = 已返回值列.get(0);
        }
    }
    static List<String> 解析類型列(String 說明值) {
        List<String> 結果 = new ArrayList<>();
        String[] 已允許格式 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 位置 = 0; 位置 < 說明值.length();) {
            String 選中狀態值 = null;
            for (String 格式值 : 已允許格式) if (說明值.startsWith(格式值, 位置)) { 選中狀態值 = 格式值; break; }
            if (選中狀態值 == null) throw new 翻譯錯誤("지원하지 않는 資料類型: " + 說明值);
            結果.add(選中狀態值); 位置 += 選中狀態值.length();
        }
        return 結果;
    }
    static String 符號(String 種類值, String... 部件列) {
        try {
            byte[] 哈希檔案 = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 部件列).getBytes(StandardCharsets.UTF_8));
            StringBuilder 文本 = new StringBuilder("j_" + 種類值 + "_");
            for (int 序數索引 = 0; 序數索引 < 12; 序數索引++) 文本.append(String.format(Locale.ROOT, "%02x", 哈希檔案[序數索引] & 255));
            return 文本.toString();
        } catch (Exception 錯誤) { throw new 翻譯錯誤(錯誤.toString()); }
    }
    final Map<String, 類別資料> 類別集列表 = new TreeMap<>();
    final Map<方法引用, 成員資料> 方法列列表 = new TreeMap<>(), 字段列列表 = new TreeMap<>();
    final Map<String, String> 字符串值列 = new LinkedHashMap<>(), 機器函數列表 = new LinkedHashMap<>();
    final String 執行狀態目標, 計算機類別;
    final int 堆機器字個數;
    final Path 資源路徑;
    提前所屬時間編譯器(List<Path> 路徑列表, String 目標值, int 詞法用機器字個數, Path 資源值) throws IOException {
        if ((!目標值.equals("kernel") && !目標值.equals("user")) || 詞法用機器字個數 < 1024 || 詞法用機器字個數 > 1048576) throw new 翻譯錯誤("執行命令 目標值 또는 記憶體 地址區域 大小 錯誤");
        執行狀態目標 = 目標值; 堆機器字個數 = 詞法用機器字個數; 資源路徑 = 資源值;
        // 產生各國原始碼時，此名稱也翻譯成對應語言。
        計算機類別 = 目標值.equals("kernel") ? "板" : "使用者";
        for (String 行 : Files.readAllLines(資源值.resolve("計算機功能.tsv"), StandardCharsets.UTF_8)) {
            String[] 部件列 = 行.split("\t", -1);
            if (部件列.length != 4) throw new 翻譯錯誤("計算機 函數 資料 錯誤");
            if (部件列[0].equals(目標值)) 機器函數列表.put(部件列[1] + 部件列[2], 部件列[3]);
        }
        for (Path 路徑 : 路徑列表) {
            類別資料 資料 = new 類別資料(路徑);
            if (類別集列表.put(資料.名稱, 資料) != null) throw new 翻譯錯誤("중복 類別值: " + 資料.名稱);
            for (成員資料 字段值 : 資料.字段值) {
                if ((字段值.存取條目 & 8) == 0 || 解析類型列(字段值.說明值).equals(Collections.singletonList("V"))) throw new 翻譯錯誤("靜態值 필드만 支持值");
                if (字段列列表.put(new 方法引用(資料.名稱, 字段值.名稱, 字段值.說明值), 字段值) != null) throw new 翻譯錯誤("중복 字段值");
            }
            for (成員資料 函數 : 資料.函數) {
                if (函數.名稱.equals("<init>")) continue;
                if ((函數.存取條目 & 8) == 0 || (函數.存取條目 & (0x20 | 0x400)) != 0) throw new 翻譯錯誤("靜態值 비동기화 함수만 支持值");
                new 方法描述符(函數.說明值);
                if (方法列列表.put(new 方法引用(資料.名稱, 函數.名稱, 函數.說明值), 函數) != null) throw new 翻譯錯誤("중복 函數");
            }
        }
    }
    String 字符串符號(String 文本) { return 字符串值列.computeIfAbsent(文本, 值 -> "j_text_" + 字符串值列.size()); }
    String 常量表達式(類別資料 資料, int 編號) {
        if (編號 < 1 || 編號 >= 資料.常量種類.length) throw new 翻譯錯誤("常量值 編號 裁剪 錯誤");
        if (資料.常量種類[編號] == 3) return "(word)(uint32_t)(" + 資料.常量資料[編號] + ")";
        if (資料.常量種類[編號] == 8) return "(word)" + 字符串符號(資料.字元((Integer)資料.常量資料[編號]));
        throw new 翻譯錯誤("정수와 字符串 상수만 支持值");
    }
    String 方法原型(方法引用 引用) {
        List<String> 參數列列表 = new ArrayList<>(); int 項目個數 = new 方法描述符(引用.說明值).實參.size();
        for (int 序數索引 = 0; 序數索引 < 項目個數; 序數索引++) 參數列列表.add("word a" + 序數索引);
        return "static word " + 符號("method", 引用.部件列()) + "(" + (項目個數 == 0 ? "void" : String.join(", ", 參數列列表)) + ")";
    }
    void 檢查局部(int 編號, int 局部變量個數) { if (編號 < 0 || 編號 >= 局部變量個數) throw new 翻譯錯誤("局部作用域 變量值 編號 裁剪 錯誤"); }
    void 發射分支(List<String> 輸出, Set<Integer> 分支列表, int 位置, int 移動量總量, String 條件) {
        int 目的地址值 = 位置 + 移動量總量; 分支列表.add(目的地址值);
        輸出.add((條件 == null ? "" : "if (" + 條件 + ") ") + "goto b" + 目的地址值 + ";");
    }
    String 方法主體(方法引用 函數, 成員資料 資料) {
        byte[] 主體資料 = 資料.屬性值.get("Code"); if (主體資料 == null) throw new 翻譯錯誤("函數 몸체가 缺失方法: " + 函數.名稱);
        資料讀取器 讀取器值 = new 資料讀取器(主體資料); int 棧深度 = 讀取器值.讀取短整數(), 局部變量個數 = 讀取器值.讀取短整數();
        資料讀取器 命令資料 = new 資料讀取器(讀取器值.讀取(讀取器值.讀取整數()));
        if (讀取器值.讀取短整數() != 0) throw new 翻譯錯誤("try/catch/finally 是否不支持");
        方法描述符 格式值 = new 方法描述符(函數.說明值); if (局部變量個數 < 格式值.實參.size()) throw new 翻譯錯誤("매개변수보다 적은 局部作用域 變量值");
        類別資料 類別值 = 類別集列表.get(函數.所有者值);
        List<String> 輸出 = new ArrayList<>(); 輸出.add(方法原型(函數) + " {");
        輸出.add("word s[" + Math.max(棧深度, 1) + "], l[" + Math.max(局部變量個數, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 序數索引 = 0; 序數索引 < 格式值.實參.size(); 序數索引++) 輸出.add("l[" + 序數索引 + "] = a" + 序數索引 + ";");
        Set<Integer> 邊界列列表 = new HashSet<>(), 分支列表 = new HashSet<>();
        String[] 比較列列表 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (命令資料.位置 < 命令資料.資料.length) {
            int 位置 = 命令資料.位置, 命令 = 命令資料.讀取位元組(); 邊界列列表.add(位置); 輸出.add("b" + 位置 + ":;");
            if (命令 == 0) continue;
            if (命令 == 1) 輸出.add("PUSH(0);");
            else if (命令 >= 2 && 命令 <= 8) 輸出.add("PUSH((uint32_t)(" + (命令 - 3) + "));");
            else if (命令 == 16 || 命令 == 17) 輸出.add("PUSH((uint32_t)(" + (命令 == 16 ? 命令資料.讀取有符號位元組() : 命令資料.讀取有符號短整數()) + "));");
            else if (命令 == 18 || 命令 == 19) 輸出.add("PUSH(" + 常量表達式(類別值, 命令 == 18 ? 命令資料.讀取位元組() : 命令資料.讀取短整數()) + ");");
            else if (命令 == 21 || 命令 == 25 || (命令 >= 26 && 命令 <= 29) || (命令 >= 42 && 命令 <= 45)) {
                int 編號 = 命令 == 21 || 命令 == 25 ? 命令資料.讀取位元組() : 命令 - (命令 <= 29 ? 26 : 42);
                檢查局部(編號, 局部變量個數); 輸出.add("PUSH(l[" + 編號 + "]);");
            } else if (命令 == 54 || 命令 == 58 || (命令 >= 59 && 命令 <= 62) || (命令 >= 75 && 命令 <= 78)) {
                int 編號 = 命令 == 54 || 命令 == 58 ? 命令資料.讀取位元組() : 命令 - (命令 <= 62 ? 59 : 75);
                檢查局部(編號, 局部變量個數); 輸出.add("l[" + 編號 + "] = POP();");
            } else if (命令 == 46) 輸出.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (命令 == 79) 輸出.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (命令 == 87 || 命令 == 88) 輸出.add(命令 == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (命令 >= 89 && 命令 <= 95) {
                int[] 項目個數列 = {1,2,3,2,3,4,2}; String[] 排序列表 = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 序數索引 = 0; 序數索引 < 項目個數列[命令 - 89]; 序數索引++) 輸出.add("abcd".charAt(序數索引) + " = POP();");
                for (char 值 : 排序列表[命令 - 89].toCharArray()) 輸出.add("PUSH(" + 值 + ");");
            } else if (命令 == 96 || 命令 == 100 || 命令 == 104 || 命令 == 126 || 命令 == 128 || 命令 == 130) {
                String 操作值 = 命令 == 96 ? "+" : 命令 == 100 ? "-" : 命令 == 104 ? "*" : 命令 == 126 ? "&" : 命令 == 128 ? "|" : "^";
                輸出.add("b = POP(); a = POP(); PUSH((uint32_t)a " + 操作值 + " (uint32_t)b);");
            } else if (命令 == 108 || 命令 == 112) 輸出.add("b = POP(); a = POP(); PUSH(divide(a,b," + (命令 == 112 ? 1 : 0) + "));");
            else if (命令 == 116) 輸出.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (命令 == 120 || 命令 == 122 || 命令 == 124) {
                輸出.add("b = POP(); a = POP();"); 輸出.add("PUSH(" + (命令 == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (命令 == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (命令 == 132) {
                int 編號 = 命令資料.讀取位元組(), 遞增總量 = 命令資料.讀取有符號位元組(); 檢查局部(編號, 局部變量個數);
                輸出.add("l[" + 編號 + "] = (uint32_t)l[" + 編號 + "] + (uint32_t)(" + 遞增總量 + ");");
            } else if (命令 >= 145 && 命令 <= 147) 輸出.add("a = POP(); PUSH((uint32_t)(" + (命令 == 145 ? "int8_t" : 命令 == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (命令 >= 153 && 命令 <= 158) {
                輸出.add("a = POP();"); 發射分支(輸出, 分支列表, 位置, 命令資料.讀取有符號短整數(), "(int32_t)a " + 比較列列表[命令 - 153] + " 0");
            } else if (命令 >= 159 && 命令 <= 166) {
                輸出.add("b = POP(); a = POP();"); 發射分支(輸出, 分支列表, 位置, 命令資料.讀取有符號短整數(), 命令 >= 165 ? "a " + 比較列列表[命令 - 159] + " b" : "(int32_t)a " + 比較列列表[命令 - 159] + " (int32_t)b");
            } else if (命令 == 167 || 命令 == 200) 發射分支(輸出, 分支列表, 位置, 命令 == 167 ? 命令資料.讀取有符號短整數() : 命令資料.讀取整數(), null);
            else if (命令 == 170 || 命令 == 171) {
                while (命令資料.位置 % 4 != 0) 命令資料.讀取位元組();
                int 默認值 = 命令資料.讀取整數(); 輸出.add("a = POP();");
                if (命令 == 170) {
                    int 底端值 = 命令資料.讀取整數(), 頂端值 = 命令資料.讀取整數(); long 項目個數 = (long)頂端值 - 底端值 + 1;
                    if (項目個數 < 1 || 項目個數 > (命令資料.資料.length - 命令資料.位置) / 4) throw new 翻譯錯誤("switch 裁剪 錯誤");
                    for (long 值 = 底端值; 值 <= 頂端值; 值++) 發射分支(輸出, 分支列表, 位置, 命令資料.讀取整數(), "(int32_t)a == (" + 值 + ")");
                } else {
                    int 項目個數 = 命令資料.讀取整數(), 前端資料 = 0;
                    if (項目個數 < 0 || 項目個數 > (命令資料.資料.length - 命令資料.位置) / 8) throw new 翻譯錯誤("switch 大小 錯誤");
                    for (int 序數索引 = 0; 序數索引 < 項目個數; 序數索引++) {
                        int 值 = 命令資料.讀取整數(); if (序數索引 > 0 && 值 <= 前端資料) throw new 翻譯錯誤("switch 排序值 錯誤"); 前端資料 = 值;
                        發射分支(輸出, 分支列表, 位置, 命令資料.讀取整數(), "(int32_t)a == (" + 值 + ")");
                    }
                }
                發射分支(輸出, 分支列表, 位置, 默認值, null);
            } else if (命令 == 172 || 命令 == 176 || 命令 == 177) 輸出.add("return " + (命令 == 177 ? "0" : "POP()") + ";");
            else if (命令 == 178 || 命令 == 179) {
                方法引用 引用 = 類別值.引用(命令資料.讀取短整數()); if (!字段列列表.containsKey(引用)) throw new 翻譯錯誤("알 數 없는 字段值");
                輸出.add(符號("init", 引用.所有者值) + "();"); String 字段值 = 符號("field", 引用.部件列());
                輸出.add(命令 == 178 ? "PUSH(" + 字段值 + ");" : 字段值 + " = POP();");
            } else if (命令 == 184) {
                方法引用 引用 = 類別值.引用(命令資料.讀取短整數()); if (!方法列列表.containsKey(引用)) throw new 翻譯錯誤("알 數 없는 函數");
                方法描述符 調用狀態類型 = new 方法描述符(引用.說明值); int 項目個數 = 調用狀態類型.實參.size();
                輸出.add(符號("init", 引用.所有者值) + "();"); 輸出.add("if(sp < " + 項目個數 + ") kernel_panic(\"call stack underflow\"); sp -= " + 項目個數 + ";");
                List<String> 調用狀態參數列 = new ArrayList<>(); for (int 序數索引 = 0; 序數索引 < 項目個數; 序數索引++) 調用狀態參數列.add("s[sp + " + 序數索引 + "]");
                輸出.add("a = " + 符號("method", 引用.部件列()) + "(" + String.join(",", 調用狀態參數列) + ");");
                if (!調用狀態類型.發回結果.equals("V")) 輸出.add("PUSH(a);");
            } else if (命令 == 182) {
                方法引用 引用 = 類別值.引用(命令資料.讀取短整數());
                if (引用.equals(new 方法引用("java/lang/String", "length", "()I"))) 輸出.add("a = POP(); PUSH(length(a));");
                else if (引用.equals(new 方法引用("java/lang/String", "charAt", "(I)C"))) 輸出.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new 翻譯錯誤("가상 函數 調用 是否不支持");
            } else if (命令 == 188) {
                if (命令資料.讀取位元組() != 10) throw new 翻譯錯誤("new int[]만 支持值"); 輸出.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (命令 == 190) 輸出.add("a = POP(); PUSH(length(a));");
            else if (命令 == 196) {
                int 擴展名值 = 命令資料.讀取位元組(), 編號 = 命令資料.讀取短整數(); 檢查局部(編號, 局部變量個數);
                if (擴展名值 == 21 || 擴展名值 == 25) 輸出.add("PUSH(l[" + 編號 + "]);");
                else if (擴展名值 == 54 || 擴展名值 == 58) 輸出.add("l[" + 編號 + "] = POP();");
                else if (擴展名值 == 132) 輸出.add("l[" + 編號 + "] = (uint32_t)l[" + 編號 + "] + (uint32_t)(" + 命令資料.讀取有符號短整數() + ");");
                else throw new 翻譯錯誤("是否不支持 wide 命令");
            } else if (命令 == 198 || 命令 == 199) {
                輸出.add("a = POP();"); 發射分支(輸出, 分支列表, 位置, 命令資料.讀取有符號短整數(), "a " + (命令 == 198 ? "==" : "!=") + " 0");
            } else throw new 翻譯錯誤(函數.所有者值 + "." + 函數.名稱 + ", 位元組值 " + 位置 + ": 是否不支持 命令 " + 命令);
        }
        if (!邊界列列表.containsAll(分支列表)) throw new 翻譯錯誤("命令 경계가 아닌 곳으로 分支");
        輸出.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 輸出);
    }
    String 導出方法(String 連接符號, String 目標值, boolean 擁有條目分) {
        int 位置索引 = 目標值.lastIndexOf('.'); if (位置索引 < 0 || !連接符號.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 翻譯錯誤("發射值 賦值值 錯誤");
        String 所有者值 = 目標值.substring(0, 位置索引).replace('.', '/'), 名稱 = 目標值.substring(位置索引 + 1); 方法引用 選中狀態值 = null;
        for (方法引用 引用 : 方法列列表.keySet()) if (引用.所有者值.equals(所有者值) && 引用.名稱.equals(名稱)) {
            if (選中狀態值 != null) throw new 翻譯錯誤("겹친 發射值 目標值"); 選中狀態值 = 引用;
        }
        if (選中狀態值 == null || (方法列列表.get(選中狀態值).存取條目 & 0x100) != 0) throw new 翻譯錯誤("내보낼 함수가 缺失方法 또는 native 函數");
        方法描述符 格式值 = new 方法描述符(選中狀態值.說明值);
        if ((擁有條目分 && !格式值.實參.isEmpty()) || !Arrays.asList("V", "I").contains(格式值.發回結果)) throw new 翻譯錯誤("條目分值 또는 C 邊界位置值 格式值 錯誤");
        List<String> 參數列列表 = new ArrayList<>(), 調用狀態參數列 = new ArrayList<>();
        for (int 序數索引 = 0; 序數索引 < 格式值.實參.size(); 序數索引++) {
            if (!格式值.實參.get(序數索引).equals("I")) throw new 翻譯錯誤("C 경계는 int 인수만 支持值");
            參數列列表.add("int32_t a" + 序數索引); 調用狀態參數列.add("(uint32_t)a" + 序數索引);
        }
        return (格式值.發回結果.equals("V") ? "void " : "int32_t ") + 連接符號 + "(" + (參數列列表.isEmpty() ? "void" : String.join(",", 參數列列表)) + ") { " + 符號("init", 選中狀態值.所有者值) + "(); " + (格式值.發回結果.equals("V") ? "" : "return (int32_t)") + 符號("method", 選中狀態值.部件列()) + "(" + String.join(",", 調用狀態參數列) + "); }";
    }
    String 生成(String 條目分, List<String> 導出條目列, boolean 通用表示法) throws IOException {
        List<String> 聲明列列表 = new ArrayList<>(), 主體列列表 = new ArrayList<>(), 字段聲明列 = new ArrayList<>();
        for (Map.Entry<方法引用, 成員資料> 條目值 : 方法列列表.entrySet()) {
            方法引用 引用 = 條目值.getKey(); 成員資料 資料 = 條目值.getValue(); 聲明列列表.add(方法原型(引用) + ";");
            if ((資料.存取條目 & 0x100) != 0) {
                String 連接 = 機器函數列表.get(引用.名稱 + 引用.說明值);
                if (!引用.所有者值.equals(計算機類別) || 連接 == null) throw new 翻譯錯誤("허용되지 않은 native 函數: " + 引用.名稱);
                int 項目個數 = new 方法描述符(引用.說明值).實參.size(); List<String> 參數列列表 = new ArrayList<>();
                for (int 序數索引 = 0; 序數索引 < 項目個數; 序數索引++) 參數列列表.add("a" + 序數索引);
                聲明列列表.add("extern word " + 連接 + "(" + (項目個數 == 0 ? "void" : String.join(",", Collections.nCopies(項目個數, "word"))) + ");");
                主體列列表.add(方法原型(引用) + " { return " + 連接 + "(" + String.join(",", 參數列列表) + "); }");
            } else 主體列列表.add(方法主體(引用, 資料));
        }
        for (Map.Entry<方法引用, 成員資料> 條目值 : 字段列列表.entrySet()) {
            方法引用 引用 = 條目值.getKey(); byte[] 常量值 = 條目值.getValue().屬性值.get("ConstantValue");
            String 值 = 常量值 == null ? "0" : 常量表達式(類別集列表.get(引用.所有者值), new 資料讀取器(常量值).讀取短整數());
            字段聲明列.add("static word " + 符號("field", 引用.部件列()) + " = " + 值 + ";");
        }
        for (String 名稱 : 類別集列表.keySet()) {
            String 初始化 = 符號("init", 名稱), 狀態值 = 符號("state", 名稱);
            聲明列列表.add("static void " + 初始化 + "(void);"); 字段聲明列.add("static unsigned " + 狀態值 + ";");
            方法引用 引用 = new 方法引用(名稱, "<clinit>", "()V");
            主體列列表.add("static void " + 初始化 + "(void) { if(" + 狀態值 + ") return; " + 狀態值 + " = 1; " + (方法列列表.containsKey(引用) ? 符號("method", 引用.部件列()) + "(); " : "") + 狀態值 + " = 2; }");
        }
        主體列列表.add(導出方法("java_entry", 條目分, true)); Set<String> 已導出名稱 = new HashSet<>();
        for (String 賦值值 : 導出條目列) {
            int 位置索引 = 賦值值.indexOf('='); if (位置索引 < 1) throw new 翻譯錯誤("發射值 賦值值 錯誤");
            String 名稱 = 賦值值.substring(0, 位置索引); 已導出名稱.add(名稱); 主體列列表.add(導出方法(名稱, 賦值值.substring(位置索引 + 1), false));
        }
        List<String> 字符串聲明列 = new ArrayList<>();
        for (Map.Entry<String, String> 條目值 : 字符串值列.entrySet()) {
            String 文本 = 條目值.getKey(); StringBuilder 陣列值 = new StringBuilder("static const word " + 條目值.getValue() + "[] = {" + 文本.length());
            for (int 序數索引 = 0; 序數索引 < 文本.length(); 序數索引++) 陣列值.append(", ").append((int)文本.charAt(序數索引));
            字符串聲明列.add(陣列值.append("};").toString());
        }
        String 支持值 = Files.readString(資源路徑.resolve("運行時支持.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(堆機器字個數));
        return 本地化已生成原始碼(支持值 + String.join("\n", 字符串聲明列) + "\n" + String.join("\n", 聲明列列表) + "\n" + String.join("\n", 字段聲明列) + "\n" + String.join("\n", 主體列列表) + "\n", 已導出名稱, 通用表示法);
    }
    String 本地化已生成原始碼(String 原始碼, Set<String> 已導出名稱, boolean 通用表示法) throws IOException {
        Map<String, String> 名稱表 = new HashMap<>();
        for (String 行 : Files.readAllLines(資源路徑.resolve("已生成名稱列.tsv"), StandardCharsets.UTF_8)) {
            String[] 一對值 = 行.split("\t"); 名稱表.put(一對值[0], 一對值[1]);
        }
        Pattern 塊片表達式 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 查找器值 = 塊片表達式.matcher(原始碼); StringBuffer 結果 = new StringBuffer();
        while (查找器值.find()) {
            String 名稱 = 查找器值.group(), 新建名稱 = 名稱;
            if (!名稱.startsWith("//") && !名稱.startsWith("/*") && !名稱.startsWith("\"") && !名稱.startsWith("'") && !已導出名稱.contains(名稱)) {
                新建名稱 = 名稱表.getOrDefault(名稱, 名稱);
                if (名稱.matches("a[0-9]+")) 新建名稱 = "實參" + 名稱.substring(1);
                if (名稱.matches("b[0-9]+")) 新建名稱 = "分支" + 名稱.substring(1);
                if (通用表示法) {
                    StringBuilder 表示法值 = new StringBuilder();
                    for (char 字元值 : 新建名稱.toCharArray()) 表示法值.append(字元值 < 128 ? Character.toString(字元值) : String.format(Locale.ROOT, "\\u%04x", (int)字元值));
                    新建名稱 = 表示法值.toString();
                }
            }
            查找器值.appendReplacement(結果, Matcher.quoteReplacement(新建名稱));
        }
        查找器值.appendTail(結果); return 結果.toString();
    }
    String x86方法本體(方法引用 函數, 成員資料 資料, Map<String,String> 計算機表, String 目標值) {
        String 標記值 = 符號("method", 函數.部件列());
        List<String> 行 = new ArrayList<>();
        if ((資料.存取條目 & 0x100) != 0) {
            String 連接 = 計算機表.get(函數.名稱 + 函數.說明值);
            if (!函數.所有者值.equals(目標值.equals("kernel") ? "設備" : "使用者") || 連接 == null) throw new 翻譯錯誤("허용되지 않은 native 函數");
            return ".text\n" + 標記值 + ":\njmp " + 連接;
        }
        byte[] 主體文本 = 資料.屬性值.get("Code"); if (主體文本 == null) throw new 翻譯錯誤("函數 몸체가 缺失方法");
        資料讀取器 讀取器值 = new 資料讀取器(主體文本); 讀取器值.讀取短整數(); int 局部個數 = 讀取器值.讀取短整數();
        資料讀取器 命令資料 = new 資料讀取器(讀取器值.讀取(讀取器值.讀取整數()));
        if (讀取器值.讀取短整數() != 0) throw new 翻譯錯誤("try/catch/finally 是否不支持");
        方法描述符 格式值 = new 方法描述符(函數.說明值); if (局部個數 < 格式值.實參.size()) throw new 翻譯錯誤("매개변수보다 적은 局部作用域 變量值");
        Collections.addAll(行,".text",".globl " + 標記值,".type " + 標記值 + ", @function",標記值 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 局部個數 * 4 + ", %esp");
        for (int 序數索引 = 0; 序數索引 < 格式值.實參.size(); 序數索引++) Collections.addAll(行,"movl " + (8 + 4 * (格式值.實參.size() - 序數索引 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (序數索引 + 1)) + "(%ebp)");
        類別資料 類別值 = 類別集列表.get(函數.所有者值); Set<Integer> 邊界列列表 = new HashSet<>(), 分支列表 = new HashSet<>();
        String[] 比較列列表 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (命令資料.位置 < 命令資料.資料.length) {
            int 位置 = 命令資料.位置, 命令 = 命令資料.讀取位元組(); String 位置索引 = 標記值 + "_b" + 位置;
            行.add(位置索引 + ":"); 邊界列列表.add(位置);
            if (命令 == 0) 行.add("nop");
            else if (命令 == 1) 行.add("pushl $0");
            else if (命令 >= 2 && 命令 <= 8) 行.add("pushl $" + (命令 - 3));
            else if (命令 == 16 || 命令 == 17) 行.add("pushl $" + (命令 == 16 ? 命令資料.讀取有符號位元組() : 命令資料.讀取有符號短整數()));
            else if (命令 == 18 || 命令 == 19) {
                int 編號 = 命令 == 18 ? 命令資料.讀取位元組() : 命令資料.讀取短整數();
                行.add("pushl $" + x86常數(類別值,編號));
            } else if (命令 == 21 || 命令 == 25 || (命令 >= 26 && 命令 <= 29) || (命令 >= 42 && 命令 <= 45) || 命令 == 54 || 命令 == 58 || (命令 >= 59 && 命令 <= 62) || (命令 >= 75 && 命令 <= 78)) {
                boolean 讀取結果 = 命令 < 54; int 編號 = 命令 == 21 || 命令 == 25 || 命令 == 54 || 命令 == 58 ? 命令資料.讀取位元組() : 命令 - (命令 <= 29 ? 26 : 命令 <= 45 ? 42 : 命令 <= 62 ? 59 : 75);
                檢查局部(編號,局部個數); 行.add((讀取結果 ? "pushl " : "popl ") + "-" + (4 * (編號 + 1)) + "(%ebp)");
            } else if (命令 == 46) Collections.addAll(行,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (命令 == 79) Collections.addAll(行,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (命令 == 87 || 命令 == 88) 行.add("addl $" + (命令 == 87 ? 4 : 8) + ", %esp");
            else if (命令 >= 89 && 命令 <= 95) {
                int[] 項目個數列 = {1,2,3,2,3,4,2}; int[][] 排序列表 = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 寄存器值列 = {"%eax","%ecx","%edx","%ebx"};
                for (int 序數索引 = 0; 序數索引 < 項目個數列[命令 - 89]; 序數索引++) 行.add("popl " + 寄存器值列[序數索引]);
                for (int 序數索引 : 排序列表[命令 - 89]) 行.add("pushl " + 寄存器值列[序數索引]);
            } else if (命令 == 96 || 命令 == 100 || 命令 == 104 || 命令 == 126 || 命令 == 128 || 命令 == 130) {
                String 操作值 = 命令 == 96 ? "addl" : 命令 == 100 ? "subl" : 命令 == 104 ? "imull" : 命令 == 126 ? "andl" : 命令 == 128 ? "orl" : "xorl";
                Collections.addAll(行,"popl %ecx","popl %eax",操作值 + " %ecx, %eax","pushl %eax");
            } else if (命令 == 108 || 命令 == 112) Collections.addAll(行,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 位置索引 + "_divide","cmpl $0x80000000, %eax","jne " + 位置索引 + "_divide","xorl %edx, %edx","jmp " + 位置索引 + "_done",位置索引 + "_divide:","cltd","idivl %ecx",位置索引 + "_done:","pushl " + (命令 == 108 ? "%eax" : "%edx"));
            else if (命令 == 116) 行.add("negl (%esp)");
            else if (命令 == 120 || 命令 == 122 || 命令 == 124) Collections.addAll(行,"popl %ecx","popl %eax",(命令 == 120 ? "sall" : 命令 == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (命令 == 132) {
                int 編號 = 命令資料.讀取位元組(), 遞增值 = 命令資料.讀取有符號位元組(); 檢查局部(編號,局部個數); 行.add("addl $" + 遞增值 + ", -" + (4 * (編號 + 1)) + "(%ebp)");
            } else if (命令 >= 145 && 命令 <= 147) Collections.addAll(行,"popl %eax",命令 == 145 ? "movsbl %al, %eax" : 命令 == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (命令 >= 153 && 命令 <= 166) {
                if (命令 <= 158) Collections.addAll(行,"popl %eax","testl %eax, %eax");
                else Collections.addAll(行,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int 目的地址值 = 位置 + 命令資料.讀取有符號短整數(); 分支列表.add(目的地址值); 行.add(比較列列表[命令 - (命令 <= 158 ? 153 : 159)] + " " + 標記值 + "_b" + 目的地址值);
            } else if (命令 == 167 || 命令 == 200) {
                int 目的地址值 = 位置 + (命令 == 167 ? 命令資料.讀取有符號短整數() : 命令資料.讀取整數()); 分支列表.add(目的地址值); 行.add("jmp " + 標記值 + "_b" + 目的地址值);
            } else if (命令 == 170 || 命令 == 171) {
                while (命令資料.位置 % 4 != 0) 命令資料.讀取位元組();
                int 默認值 = 位置 + 命令資料.讀取整數(); 分支列表.add(默認值); 行.add("popl %eax");
                int 項目個數, 底端值 = 0;
                if (命令 == 170) { 底端值 = 命令資料.讀取整數(); int 頂端值 = 命令資料.讀取整數(); long 長度 = (long)頂端值 - 底端值 + 1; if (長度 < 1 || 長度 > (命令資料.資料.length - 命令資料.位置) / 4) throw new 翻譯錯誤("switch 裁剪 錯誤"); 項目個數 = (int)長度; }
                else { 項目個數 = 命令資料.讀取整數(); if (項目個數 < 0 || 項目個數 > (命令資料.資料.length - 命令資料.位置) / 8) throw new 翻譯錯誤("switch 大小 錯誤"); }
                for (int 序數索引 = 0; 序數索引 < 項目個數; 序數索引++) {
                    int 值 = 命令 == 170 ? 底端值 + 序數索引 : 命令資料.讀取整數(), 目的地址值 = 位置 + 命令資料.讀取整數(); 分支列表.add(目的地址值);
                    Collections.addAll(行,"cmpl $" + 值 + ", %eax","je " + 標記值 + "_b" + 目的地址值);
                }
                行.add("jmp " + 標記值 + "_b" + 默認值);
            } else if (命令 == 172 || 命令 == 176 || 命令 == 177) {
                if (命令 != 177) 行.add("popl %eax"); Collections.addAll(行,"leave","ret");
            } else if (命令 == 178 || 命令 == 179) {
                方法引用 引用 = 類別值.引用(命令資料.讀取短整數()); if (!字段列列表.containsKey(引用)) throw new 翻譯錯誤("알 數 없는 字段值");
                Collections.addAll(行,"call " + 符號("init",引用.所有者值),(命令 == 178 ? "pushl " : "popl ") + 符號("field",引用.部件列()));
            } else if (命令 == 184) {
                方法引用 引用 = 類別值.引用(命令資料.讀取短整數()); if (!方法列列表.containsKey(引用)) throw new 翻譯錯誤("알 數 없는 函數");
                方法描述符 調用狀態類型 = new 方法描述符(引用.說明值); Collections.addAll(行,"call " + 符號("init",引用.所有者值),"call " + 符號("method",引用.部件列()));
                if (!調用狀態類型.實參.isEmpty()) 行.add("addl $" + 調用狀態類型.實參.size() * 4 + ", %esp");
                if (!調用狀態類型.發回結果.equals("V")) 行.add("pushl %eax");
            } else if (命令 == 182) {
                方法引用 引用 = 類別值.引用(命令資料.讀取短整數());
                if (引用.equals(new 方法引用("java/lang/String","length","()I"))) Collections.addAll(行,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (引用.equals(new 方法引用("java/lang/String","charAt","(I)C"))) Collections.addAll(行,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new 翻譯錯誤("가상 函數 調用 是否不支持");
            } else if (命令 == 188) {
                if (命令資料.讀取位元組() != 10) throw new 翻譯錯誤("new int[]만 支持值"); Collections.addAll(行,"popl %eax","call rt_new_array","pushl %eax");
            } else if (命令 == 190) Collections.addAll(行,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (命令 == 196) {
                int 擴展名值 = 命令資料.讀取位元組(), 編號 = 命令資料.讀取短整數(); 檢查局部(編號,局部個數);
                if (擴展名值 == 21 || 擴展名值 == 25 || 擴展名值 == 54 || 擴展名值 == 58) 行.add((擴展名值 <= 25 ? "pushl " : "popl ") + "-" + 4 * (編號 + 1) + "(%ebp)");
                else if (擴展名值 == 132) 行.add("addl $" + 命令資料.讀取有符號短整數() + ", -" + 4 * (編號 + 1) + "(%ebp)");
                else throw new 翻譯錯誤("wide 命令 是否不支持");
            } else if (命令 == 198 || 命令 == 199) {
                int 目的地址值 = 位置 + 命令資料.讀取有符號短整數(); 分支列表.add(目的地址值); Collections.addAll(行,"popl %eax","testl %eax, %eax",(命令 == 198 ? "je " : "jne ") + 標記值 + "_b" + 目的地址值);
            } else throw new 翻譯錯誤("是否不支持 命令: " + 命令);
        }
        if (!邊界列列表.containsAll(分支列表)) throw new 翻譯錯誤("命令 경계가 아닌 곳으로 分支");
        行.add(".size " + 標記值 + ", .-" + 標記值); return String.join("\n",行);
    }
    String x86常數(類別資料 資料, int 編號) {
        if (資料.常量種類[編號] == 3) return 資料.常量資料[編號].toString();
        if (資料.常量種類[編號] == 8) return 字符串符號(資料.字元((Integer)資料.常量資料[編號]));
        throw new 翻譯錯誤("정수와 字符串 상수만 支持值");
    }
    String x86組合語言(String 條目分, List<String> 已導出值, String 目標值) throws IOException {
        Map<String,String> 計算機表 = new HashMap<>();
        for (String 行 : Files.readAllLines(資源路徑.resolve("x86機器函數.tsv"))) { String[] 一對值 = 行.split("\t"); if (一對值[0].equals(目標值)) 計算機表.put(一對值[1] + 一對值[2],一對值[3]); }
        int 位置索引 = 條目分.lastIndexOf('.'); if (位置索引 < 0) throw new 翻譯錯誤("條目分 賦值值 錯誤");
        String 所有者值 = 條目分.substring(0,位置索引).replace('.','/'), 方法條目名稱 = 條目分.substring(位置索引 + 1); 方法引用 條目分值 = null;
        for (String 說明值 : Arrays.asList("()I","()V")) { 方法引用 引用 = new 方法引用(所有者值,方法條目名稱,說明值); if (方法列列表.containsKey(引用)) { if (條目分值 != null) throw new 翻譯錯誤("겹친 條目分"); 條目分值 = 引用; } }
        if (條目分值 == null || (方法列列表.get(條目分值).存取條目 & 0x100) != 0) throw new 翻譯錯誤("條目分值 函數 格式值 錯誤");
        List<String> 行 = new ArrayList<>(); 行.add(".code32");
        for (類別資料 資料 : 類別集列表.values()) {
            String 狀態值 = 符號("state",資料.名稱), 初始化 = 符號("init",資料.名稱);
            Collections.addAll(行,".bss",".balign 4",狀態值 + ": .long 0",".text",初始化 + ":","cmpl $0, " + 狀態值,"jne " + 初始化 + "_done","movl $1, " + 狀態值);
            方法引用 初始設定器引用 = new 方法引用(資料.名稱,"<clinit>","()V"); if (方法列列表.containsKey(初始設定器引用)) 行.add("call " + 符號("method",初始設定器引用.部件列()));
            Collections.addAll(行,"movl $2, " + 狀態值,初始化 + "_done:","ret");
            for (成員資料 字段值 : 資料.字段值) {
                byte[] 常量值 = 字段值.屬性值.get("ConstantValue"); String 值 = 常量值 == null ? "0" : x86常數(資料,new 資料讀取器(常量值).讀取短整數());
                Collections.addAll(行,".data",".balign 4",符號("field",資料.名稱,字段值.名稱,字段值.說明值) + ": .long " + 值);
            }
            for (成員資料 函數 : 資料.函數) if (!函數.名稱.equals("<init>")) 行.add(x86方法本體(new 方法引用(資料.名稱,函數.名稱,函數.說明值),函數,計算機表,目標值));
        }
        Collections.addAll(行,".text",".globl java_entry","java_entry:","call " + 符號("init",條目分值.所有者值),"call " + 符號("method",條目分值.部件列()));
        if (條目分值.說明值.equals("()V")) 行.add("xorl %eax, %eax"); 行.add("ret");
        for (String 賦值值 : 已導出值) {
            int 分隔符值 = 賦值值.indexOf('='); if (分隔符值 < 1) throw new 翻譯錯誤("發射值 賦值值 錯誤");
            String 外部值 = 賦值值.substring(0,分隔符值), 函數 = 賦值值.substring(分隔符值 + 1); int 除法結果 = 函數.lastIndexOf('.');
            if (除法結果 < 0 || !外部值.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new 翻譯錯誤("發射值 符號 錯誤");
            String 類別值 = 函數.substring(0,除法結果).replace('.','/'), 名稱 = 函數.substring(除法結果 + 1); 方法引用 選中狀態值 = null;
            for (方法引用 引用 : 方法列列表.keySet()) if (引用.所有者值.equals(類別值) && 引用.名稱.equals(名稱)) { if (選中狀態值 != null) throw new 翻譯錯誤("겹친 發射值 目標值"); 選中狀態值 = 引用; }
            if (選中狀態值 == null) throw new 翻譯錯誤("내보낼 함수가 缺失方法");
            Collections.addAll(行,".text",".globl " + 外部值,外部值 + ":","call " + 符號("init",選中狀態值.所有者值),"jmp " + 符號("method",選中狀態值.部件列()));
        }
        行.add(".section .rodata");
        for (Map.Entry<String,String> 條目值 : 字符串值列.entrySet()) {
            Collections.addAll(行,".balign 4",條目值.getValue() + ":",".long " + 條目值.getKey().length());
            List<String> 單位列列表 = new ArrayList<>(); for (char 單位值 : 條目值.getKey().toCharArray()) 單位列列表.add(Integer.toString(單位值)); if (!單位列列表.isEmpty()) 行.add(".long " + String.join(",",單位列列表));
        }
        行.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",行) + "\n";
    }
    static void 執行工具(List<String> 命令) throws Exception {
        if (new ProcessBuilder(命令).inheritIO().start().waitFor() != 0) throw new 翻譯錯誤("編譯原始碼 錯誤: " + 命令.get(0));
    }
    static String 資料字符串(String 文本) { return "\"" + 文本.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void x86編譯結果(List<Path> 輸入列表, String 目標值, String 條目分, List<String> 已導出值, Path 輸出, Path 資源值) throws Exception {
        Path 臨時值 = Files.createTempDirectory("jkoros-java-x86-"), 類別路徑 = 臨時值.resolve("classes"); Files.createDirectory(類別路徑);
        try {
            List<String> Java命令 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",類別路徑.toString(),"-sourcepath",類別路徑.toString(),"-d",類別路徑.toString()));
            List<Path> 字節碼 = new ArrayList<>(); int 原始碼個數 = 0;
            for (Path 輸入值 : 輸入列表) {
                if (輸出.toAbsolutePath().normalize().equals(輸入值.toAbsolutePath().normalize())) throw new 翻譯錯誤("輸出 파일과 입력이 相等文本");
                if (輸入值.toString().endsWith(".java")) { Java命令.add(輸入值.toString()); 原始碼個數++; }
                else if (輸入值.toString().endsWith(".class")) 字節碼.add(輸入值);
                else throw new 翻譯錯誤(".java 또는 .class만 支持值");
            }
            if (原始碼個數 > 0) 執行工具(Java命令);
            try (java.util.stream.Stream<Path> 路徑列表 = Files.walk(類別路徑)) { 路徑列表.filter(路徑 -> 路徑.toString().endsWith(".class")).sorted().forEach(字節碼::add); }
            提前所屬時間編譯器 轉換值 = new 提前所屬時間編譯器(字節碼,目標值.equals("user") ? "user" : "kernel",262144,資源值);
            String 組裝值 = 轉換值.x86組合語言(條目分,已導出值,目標值); Files.writeString(臨時值.resolve("program.s"),組裝值,StandardCharsets.UTF_8);
            Path 工具位置 = 資源值.getParent();
            執行工具(Arrays.asList("as","--32","-o",臨時值.resolve("program.o").toString(),臨時值.resolve("program.s").toString()));
            執行工具(Arrays.asList("as","--32","-o",臨時值.resolve("runtime.o").toString(),工具位置.resolve("運行時支持.s").toString()));
            List<String> 連接 = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (目標值.equals("kernel")) 連接.add("-r");
            else {
                執行工具(Arrays.asList("as","--32","-o",臨時值.resolve("start.o").toString(),工具位置.resolve(目標值.equals("user") ? "開始用戶程式.s" : "Linux啓動.s").toString()));
                Collections.addAll(連接,"-e","_start",臨時值.resolve("start.o").toString());
                if (目標值.equals("user")) Collections.addAll(連接,"-T",工具位置.resolve("用戶連接導航.ld").toString());
            }
            Collections.addAll(連接,"-o",臨時值.resolve("result").toString(),臨時值.resolve("program.o").toString(),臨時值.resolve("runtime.o").toString()); 執行工具(連接);
            輸出 = 輸出.toAbsolutePath(); Files.createDirectories(輸出.getParent()); Path 發佈值 = Files.createTempFile(輸出.getParent(),".elf-",".tmp");
            try { Files.copy(臨時值.resolve("result"),發佈值,StandardCopyOption.REPLACE_EXISTING); Files.move(發佈值,輸出,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(發佈值); }
            Files.setPosixFilePermissions(輸出,java.nio.file.attribute.PosixFilePermissions.fromString(目標值.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(輸出 + ".s"),組裝值,StandardCharsets.UTF_8);
            List<String> 符號資料 = new ArrayList<>(), 原始碼資料 = new ArrayList<>();
            for (方法引用 引用 : 轉換值.方法列列表.keySet()) 符號資料.add(資料字符串(符號("method",引用.部件列())) + ":" + 資料字符串(引用.所有者值 + "." + 引用.名稱 + 引用.說明值));
            for (Path 輸入值 : 輸入列表) {
                byte[] 哈希檔案 = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(輸入值)); StringBuilder 文本 = new StringBuilder(); for (byte 值 : 哈希檔案) 文本.append(String.format(Locale.ROOT,"%02x",值 & 255));
                原始碼資料.add(資料字符串(輸入值.toAbsolutePath().toString()) + ":" + 資料字符串(文本.toString()));
            }
            Files.writeString(Paths.get(輸出 + ".json"),"{\"target\":" + 資料字符串(目標值) + ",\"entry\":" + 資料字符串(條目分) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",符號資料) + "},\"sources\":{" + String.join(",",原始碼資料) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> 路徑列表 = Files.walk(臨時值)) { for (Path 路徑 : (Iterable<Path>)路徑列表.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(路徑); }
        }
    }
    public static void main(String[] 實參) {
        try {
            String 條目分 = null, 目標值 = "kernel", x86目標 = null; Path 輸出路徑 = null; int 詞法用機器字個數 = 262144; boolean 通用表示法 = false;
            List<String> 已導出值 = new ArrayList<>(); List<Path> 路徑列表 = new ArrayList<>();
            for (int 序數索引 = 0; 序數索引 < 實參.length; 序數索引++) {
                String 值 = 實參[序數索引];
                switch (值) {
                    case "--target": x86目標 = 實參[++序數索引]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry 類別值.函數 -o 輸出 [--target linux|kernel|user] [--profile kernel|user] [--export 符號=類別值.函數] 클래스파일 또는 Java원문"); return;
                    case "--entry": 條目分 = 實參[++序數索引]; break;
                    case "--profile": 目標值 = 實參[++序數索引]; break;
                    case "--heap-words": 詞法用機器字個數 = Integer.parseInt(實參[++序數索引]); break;
                    case "--export": 已導出值.add(實參[++序數索引]); break;
                    case "-o": 輸出路徑 = Paths.get(實參[++序數索引]); break;
                    case "--ucn": 通用表示法 = true; break;
                    default: if (值.startsWith("-")) throw new 翻譯錯誤("알 數 없는 옵션: " + 值); 路徑列表.add(Paths.get(值));
                }
            }
            if (條目分 == null || 輸出路徑 == null || 路徑列表.isEmpty()) throw new 翻譯錯誤("--entry, -o, 類別值 파일이 필요합니다");
            Path 資源值 = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (x86目標 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(x86目標)) throw new 翻譯錯誤("알 數 없는 執行命令 目標值");
                x86編譯結果(路徑列表,x86目標,條目分,已導出值,輸出路徑,資源值); return;
            }
            String 原始碼 = new 提前所屬時間編譯器(路徑列表, 目標值, 詞法用機器字個數, 資源值).生成(條目分, 已導出值, 通用表示法);
            輸出路徑 = 輸出路徑.toAbsolutePath(); Files.createDirectories(輸出路徑.getParent());
            Path 臨時值 = Files.createTempFile(輸出路徑.getParent(), ".aot-", ".tmp");
            try { Files.writeString(臨時值, 原始碼, StandardCharsets.UTF_8); Files.move(臨時值, 輸出路徑, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(臨時值); }
        } catch (Exception 錯誤) { System.err.println("編譯原始碼 錯誤: " + 錯誤.getMessage()); System.exit(1); }
    }
}
