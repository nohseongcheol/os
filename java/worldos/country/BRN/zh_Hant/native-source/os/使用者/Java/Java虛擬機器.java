// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 在 ring 3 執行的受限 JVM；執行時檢查檔案、堆疊、參照與分支邊界。 */
public final class Java虛擬機器 {
    static int[] 檔案 = new int[16384], 檔案名稱文本 = new int[64];
    static int[] 常量標籤 = new int[512], 常量首位值 = new int[512], 常量第二值 = new int[512], 字符串引用 = new int[512];
    static int[] 方法名稱文本 = new int[32], 方法類型 = new int[32], 方法存取 = new int[32];
    static int[] 方法開始 = new int[32], 方法結束 = new int[32], 方法棧 = new int[32], 方法局部變量列 = new int[32];
    static int[] 方法實際參數個數 = new int[32], 方法實際參數類型 = new int[512], 方法發回 = new int[32];
    static int[] 邊界位置值 = new int[16384];
    static int[] 局部值 = new int[4096], 局部類型 = new int[4096], 操作數棧值 = new int[4096], 操作數棧類型 = new int[4096];
    static int[] 幀方法 = new int[32], 幀位置 = new int[32], 幀棧 = new int[32];
    static int[] 堆值 = new int[8192];
    static int 大小, 讀取位置, 常量個數, 方法個數, 類別名稱, 幀索引 = -1, 堆結束位置 = 1, 發回類型;
    static boolean 錯誤;

    static void 失敗值(String 機器字文本) {
        if (!錯誤) { 使用者.寫入("JVM error: "); 使用者.寫入(機器字文本); 使用者.寫入字元值(10); }
        錯誤 = true;
    }
    static boolean 裁剪(int 運行, int 長度) { return 運行 >= 0 && 長度 >= 0 && 運行 <= 大小 - 長度; }
    static int 位元組值() {
        if (!裁剪(讀取位置, 1)) { 失敗值("truncated class file"); return 0; }
        return 檔案[讀取位置++];
    }
    static int 短整數值() { return 位元組值() << 8 | 位元組值(); }
    static int 整數() { return 短整數值() << 16 | 短整數值(); }
    static void 跳過位元組列(int 長度) { if (!裁剪(讀取位置, 長度)) 失敗值("invalid attribute size"); else 讀取位置 += 長度; }
    static boolean 檢查常量(int 數, int 種類值) {
        if (數 <= 0 || 數 >= 常量個數 || 常量標籤[數] != 種類值) { 失敗值("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 文本範圍(int 運行, int 長度, String 機器字文本) {
        if (!裁剪(運行, 長度) || 長度 != 機器字文本.length()) return false;
        for (int 數 = 0; 數 < 長度; 數++) if (檔案[運行 + 數] != 機器字文本.charAt(數)) return false;
        return true;
    }
    static boolean 機器字文本(int 常量值, String 機器字文本) { return 檢查常量(常量值, 1) && 文本範圍(常量首位值[常量值], 常量第二值[常量值], 機器字文本); }
    static boolean 匹配中機器字(int 首位操作數, int 第二操作數) {
        if (!檢查常量(首位操作數, 1) || !檢查常量(第二操作數, 1) || 常量第二值[首位操作數] != 常量第二值[第二操作數]) return false;
        for (int 數 = 0; 數 < 常量第二值[首位操作數]; 數++) if (檔案[常量首位值[首位操作數] + 數] != 檔案[常量首位值[第二操作數] + 數]) return false;
        return true;
    }
    static int 類別名稱文本(int 數) { return 檢查常量(數, 7) && 檢查常量(常量首位值[數], 1) ? 常量首位值[數] : 0; }
    static int 引用名稱(int 數) { return 檢查常量(數, 12) && 檢查常量(常量首位值[數], 1) ? 常量首位值[數] : 0; }
    static int 引用類型(int 數) { return 檢查常量(數, 12) && 檢查常量(常量第二值[數], 1) ? 常量第二值[數] : 0; }
    static int 描述符類型(int 結尾, boolean 空類型) {
        if (讀取位置 >= 結尾) { 失敗值("invalid descriptor"); return 0; }
        int 值 = 位元組值();
        if (值 == 'V' && 空類型) return 0;
        if (值 == 'I' || 值 == 'B' || 值 == 'C' || 值 == 'S' || 值 == 'Z') return 1;
        if (值 == '[') { 描述符類型(結尾, false); return 2; }
        if (值 == 'L') {
            int 運行 = 讀取位置;
            while (讀取位置 < 結尾 && 檔案[讀取位置] != ';') 讀取位置++;
            if (讀取位置 == 結尾 || 讀取位置 == 運行) 失敗值("invalid reference descriptor");
            else 讀取位置++;
            return 2;
        }
        失敗值("unsupported descriptor type"); return 0;
    }
    static void 讀取描述符(int 函數) {
        int 上一個項目 = 讀取位置, 數 = 方法類型[函數];
        if (!檢查常量(數, 1)) return;
        讀取位置 = 常量首位值[數]; int 結尾 = 讀取位置 + 常量第二值[數];
        if (位元組值() != '(') 失敗值("invalid method descriptor");
        int 項目個數 = 0;
        while (!錯誤 && 讀取位置 < 結尾 && 檔案[讀取位置] != ')') {
            if (項目個數 == 16) { 失敗值("too many method arguments"); break; }
            方法實際參數類型[函數 * 16 + 項目個數++] = 描述符類型(結尾, false);
        }
        if (讀取位置 >= 結尾 || 位元組值() != ')') 失敗值("invalid method descriptor");
        方法發回[函數] = 描述符類型(結尾, true); 方法實際參數個數[函數] = 項目個數;
        if (讀取位置 != 結尾) 失敗值("invalid method descriptor");
        讀取位置 = 上一個項目;
    }
    static void 跳過屬性() {
        int 項目個數 = 短整數值();
        for (int 數 = 0; 數 < 項目個數 && !錯誤; 數++) { 檢查常量(短整數值(), 1); 跳過位元組列(整數()); }
    }
    static int 命令長度(int 值) {
        if (值 == 16 || 值 == 18 || 值 == 21 || 值 == 25 || 值 == 54 || 值 == 58 || 值 == 188) return 2;
        if (值 == 17 || 值 == 19 || 值 == 132 || 值 >= 153 && 值 <= 167
            || 值 >= 178 && 值 <= 184 || 值 == 187 || 值 == 189 || 值 == 192 || 值 == 198 || 值 == 199) return 3;
        if (值 >= 0 && 值 <= 8 || 值 >= 26 && 值 <= 29 || 值 >= 42 && 值 <= 46 || 值 == 50
            || 值 >= 59 && 值 <= 62 || 值 >= 75 && 值 <= 79 || 值 == 83 || 值 == 87 || 值 == 89 || 值 == 95
            || 值 == 96 || 值 == 100 || 值 == 104 || 值 == 108 || 值 == 112 || 值 == 116
            || 值 == 120 || 值 == 122 || 值 == 124 || 值 == 126 || 值 == 128 || 值 == 130
            || 值 >= 145 && 值 <= 147 || 值 == 172 || 值 == 176 || 值 == 177 || 值 == 190) return 1;
        return 0;
    }
    static void 讀取類別() {
        if (整數() != 0xcafebabe) 失敗值("not a class file");
        int 次版本修訂 = 短整數值(), 版本值 = 短整數值();
        if (版本值 < 45 || 版本值 > 52 || 次版本修訂 != 0) 失敗值("supported class versions: 45..52, minor 0");
        常量個數 = 短整數值();
        if (常量個數 < 1 || 常量個數 > 512) { 失敗值("constant pool limit (511)"); return; }
        for (int 數 = 1; 數 < 常量個數 && !錯誤; 數++) {
            int 種類值 = 位元組值(); 常量標籤[數] = 種類值;
            if (種類值 == 1) { 常量第二值[數] = 短整數值(); 常量首位值[數] = 讀取位置; 跳過位元組列(常量第二值[數]); }
            else if (種類值 == 3) 常量首位值[數] = 整數();
            else if (種類值 == 7 || 種類值 == 8) 常量首位值[數] = 短整數值();
            else if (種類值 == 9 || 種類值 == 10 || 種類值 == 12) { 常量首位值[數] = 短整數值(); 常量第二值[數] = 短整數值(); }
            else 失敗值("unsupported constant type");
        }
        int 權限值 = 短整數值();
        if ((權限值 & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) 失敗值("unsupported class flags");
        類別名稱 = 類別名稱文本(短整數值());
        if (!機器字文本(類別名稱文本(短整數值()), "java/lang/Object")) 失敗值("inheritance unsupported");
        if (短整數值() != 0) 失敗值("interfaces unsupported");
        if (短整數值() != 0) 失敗值("fields unsupported");
        方法個數 = 短整數值();
        if (方法個數 < 1 || 方法個數 > 32) { 失敗值("method count limit (32)"); return; }
        for (int 數 = 0; 數 < 方法個數 && !錯誤; 數++) {
            方法存取[數] = 短整數值(); 方法名稱文本[數] = 短整數值(); 方法類型[數] = 短整數值();
            檢查常量(方法名稱文本[數], 1); 讀取描述符(數);
            if ((方法存取[數] & (0x100 | 0x400 | 0x20)) != 0) 失敗值("native, abstract and synchronized methods unsupported");
            if ((方法存取[數] & 8) == 0 && !機器字文本(方法名稱文本[數], "<init>")) 失敗值("instance methods unsupported");
            if (機器字文本(方法名稱文本[數], "<clinit>")) 失敗值("class initializers unsupported");
            for (int 前端值 = 0; 前端值 < 數; 前端值++) if (匹配中機器字(方法名稱文本[前端值], 方法名稱文本[數]) && 匹配中機器字(方法類型[前端值], 方法類型[數])) 失敗值("duplicate method");
            int 項目個數 = 短整數值();
            for (int 屬性值 = 0; 屬性值 < 項目個數 && !錯誤; 屬性值++) {
                int 名稱 = 短整數值(), 長度 = 整數(), 運行 = 讀取位置;
                if (!裁剪(運行, 長度)) { 失敗值("truncated method attribute"); break; }
                if (機器字文本(名稱, "Code")) {
                    if (方法開始[數] != 0) 失敗值("duplicate Code attribute");
                    方法棧[數] = 短整數值(); 方法局部變量列[數] = 短整數值(); int 程式碼長度 = 整數();
                    if (方法棧[數] > 128 || 方法局部變量列[數] > 128 || 方法局部變量列[數] < 方法實際參數個數[數]
                        || 程式碼長度 < 1 || 程式碼長度 > 8192) 失敗值("method memory limits exceeded");
                    方法開始[數] = 讀取位置; 跳過位元組列(程式碼長度); 方法結束[數] = 讀取位置;
                    if (短整數值() != 0) 失敗值("exception handlers unsupported");
                    跳過屬性();
                    if (讀取位置 != 運行 + 長度) 失敗值("Code attribute size mismatch");
                } else 跳過位元組列(長度);
            }
            if (方法開始[數] == 0) 失敗值("missing Code attribute");
            int 槽條目 = 方法開始[數];
            while (槽條目 < 方法結束[數] && !錯誤) {
                int 長度 = 命令長度(檔案[槽條目]);
                if (長度 == 0 || 長度 > 方法結束[數] - 槽條目) { 失敗值("unsupported or truncated bytecode"); break; }
                邊界位置值[槽條目] = 數 + 1; 槽條目 += 長度;
            }
            // 即使在不執行的路徑上，也拒絕無效的分支目標。
            槽條目 = 方法開始[數];
            while (槽條目 < 方法結束[數] && !錯誤) {
                int 值 = 檔案[槽條目];
                if (值 >= 153 && 值 <= 167 || 值 == 198 || 值 == 199) {
                    int 目的地址值 = 槽條目 + (short)(檔案[槽條目 + 1] << 8 | 檔案[槽條目 + 2]);
                    if (目的地址值 < 方法開始[數] || 目的地址值 >= 方法結束[數] || 邊界位置值[目的地址值] != 數 + 1) 失敗值("invalid branch target");
                }
                槽條目 += 命令長度(值);
            }
        }
        if (!錯誤) 跳過屬性();
        if (讀取位置 != 大小) 失敗值("extra class file data");
    }
    static int 分配存儲裝置(int 種類值, int 長度) {
        if (長度 < 0 || 長度 > 堆值.length - 堆結束位置 - 2) { 失敗值("object heap exhausted or negative array size"); return 0; }
        int 引用 = 堆結束位置; 堆結束位置 += 長度 + 2; 堆值[引用] = 種類值; 堆值[引用 + 1] = 長度;
        return 引用;
    }
    static boolean 物件值(int 引用, int 種類值) {
        if (引用 < 1 || 引用 >= 堆結束位置 - 1 || 堆值[引用] != 種類值) { 失敗值("null or invalid object reference"); return false; }
        return true;
    }
    static int 常量文本(int 編號) {
        if (!檢查常量(編號, 1)) return 0;
        if (字符串引用[編號] != 0) return 字符串引用[編號];
        int 引用 = 分配存儲裝置(1, 常量第二值[編號]); if (錯誤) return 0;
        int 結尾 = 常量首位值[編號] + 常量第二值[編號], 數 = 常量首位值[編號], 長度 = 0;
        while (數 < 結尾 && !錯誤) {
            int 值 = 檔案[數++];
            if (值 == 0) 失敗值("invalid modified UTF-8");
            else if (值 >= 192 && 值 <= 223 && 數 < 結尾) {
                int 下一項目 = 檔案[數++];
                if ((下一項目 & 192) != 128) 失敗值("invalid modified UTF-8");
                值 = (值 & 31) << 6 | 下一項目 & 63;
                if (值 != 0 && 值 < 128) 失敗值("overlong modified UTF-8");
            } else if (值 >= 224 && 值 <= 239 && 數 + 1 < 結尾) {
                int 首位操作數 = 檔案[數++], 第二操作數 = 檔案[數++];
                if ((首位操作數 & 192) != 128 || (第二操作數 & 192) != 128) 失敗值("invalid modified UTF-8");
                值 = (值 & 15) << 12 | (首位操作數 & 63) << 6 | 第二操作數 & 63;
                if (值 < 2048) 失敗值("overlong modified UTF-8");
            } else if (值 >= 128) 失敗值("invalid modified UTF-8");
            堆值[引用 + 2 + 長度++] = 值;
        }
        堆值[引用 + 1] = 長度; 字符串引用[編號] = 引用; return 引用;
    }
    static int 宿主字元(String 值) {
        int 引用 = 分配存儲裝置(1, 值.length()); if (錯誤) return 0;
        for (int 數 = 0; 數 < 值.length(); 數++) 堆值[引用 + 2 + 數] = 值.charAt(數);
        return 引用;
    }
    static void 寫入文本(int 引用) {
        if (引用 == 0) { 使用者.寫入("null"); return; }
        if (!物件值(引用, 1)) return;
        for (int 數 = 0; 數 < 堆值[引用 + 1]; 數++) 使用者.寫入字元值(堆值[引用 + 2 + 數]);
    }
    static int 數字字元(int 值) {
        int 引用 = 分配存儲裝置(1, 11); if (錯誤) return 0;
        int 長度 = 0;
        if (值 < 0) 堆值[引用 + 2 + 長度++] = '-'; else 值 = -值;
        int 位置索引 = 1000000000; boolean 運行 = false;
        while (位置索引 != 0) {
            int 數 = -(值 / 位置索引);
            if (數 != 0 || 運行 || 位置索引 == 1) { 堆值[引用 + 2 + 長度++] = '0' + 數; 運行 = true; }
            值 %= 位置索引; 位置索引 /= 10;
        }
        堆值[引用 + 1] = 長度; return 引用;
    }
    static int 解碼整數(int 引用) {
        if (!物件值(引用, 1)) return 0;
        int 長度 = 堆值[引用 + 1], 數 = 0, 值 = 0; boolean 負數值 = false;
        if (長度 > 0 && (堆值[引用 + 2] == '-' || 堆值[引用 + 2] == '+')) { 負數值 = 堆值[引用 + 2] == '-'; 數++; }
        if (數 == 長度) 失敗值("NumberFormatException");
        for (; 數 < 長度 && !錯誤; 數++) {
            int 數字值 = 堆值[引用 + 2 + 數] - '0';
            if (數字值 < 0 || 數字值 > 9 || 值 < -214748364 || 值 == -214748364 && 數字值 > (負數值 ? 8 : 7)) 失敗值("NumberFormatException");
            值 = 值 * 10 - 數字值;
        }
        return 負數值 ? 值 : -值;
    }
    static void 放入值(int 值, int 類型值) {
        if (錯誤) return;
        if (幀索引 < 0 || 幀棧[幀索引] >= 方法棧[幀方法[幀索引]]) { 失敗值("operand stack overflow"); return; }
        int 槽條目 = 幀索引 * 128 + 幀棧[幀索引]++; 操作數棧值[槽條目] = 值; 操作數棧類型[槽條目] = 類型值;
    }
    static int 減法值列(int 類型值) {
        if (錯誤) return 0;
        if (幀索引 < 0 || 幀棧[幀索引] < 1) { 失敗值("operand stack underflow"); return 0; }
        int 槽條目 = 幀索引 * 128 + --幀棧[幀索引]; 發回類型 = 操作數棧類型[槽條目];
        if (類型值 != 0 && 發回類型 != 類型值) 失敗值("operand type mismatch");
        return 操作數棧值[槽條目];
    }
    static void 讀取局部(int 編號, int 類型值) {
        if (編號 >= 方法局部變量列[幀方法[幀索引]] || 編號 < 0 || 局部類型[幀索引 * 128 + 編號] != 類型值) { 失敗值("invalid or uninitialized local"); return; }
        放入值(局部值[幀索引 * 128 + 編號], 類型值);
    }
    static void 寫入局部(int 編號, int 類型值) {
        if (編號 >= 方法局部變量列[幀方法[幀索引]] || 編號 < 0) { 失敗值("local index out of range"); return; }
        int 值 = 減法值列(類型值); 局部值[幀索引 * 128 + 編號] = 值; 局部類型[幀索引 * 128 + 編號] = 類型值;
    }
    static int 讀取操作碼位元組() {
        int 位置 = 幀位置[幀索引];
        if (位置 < 方法開始[幀方法[幀索引]] || 位置 >= 方法結束[幀方法[幀索引]]) { 失敗值("instruction pointer out of range"); return 0; }
        幀位置[幀索引]++; return 檔案[位置];
    }
    static int 讀取操作碼短整數() { return 讀取操作碼位元組() << 8 | 讀取操作碼位元組(); }
    static void 移動值(int 位置) {
        int 函數 = 幀方法[幀索引];
        if (位置 < 方法開始[函數] || 位置 >= 方法結束[函數] || 邊界位置值[位置] != 函數 + 1) 失敗值("invalid branch target");
        else 幀位置[幀索引] = 位置;
    }
    static void 調用(int 函數) {
        if (幀索引 == 31) { 失敗值("call stack limit (32)"); return; }
        int 下一項目 = 幀索引 + 1;
        for (int 數 = 0; 數 < 128; 數++) 局部類型[下一項目 * 128 + 數] = 0;
        for (int 數 = 方法實際參數個數[函數] - 1; 數 >= 0; 數--) {
            局部值[下一項目 * 128 + 數] = 減法值列(方法實際參數類型[函數 * 16 + 數]); 局部類型[下一項目 * 128 + 數] = 方法實際參數類型[函數 * 16 + 數];
        }
        幀索引 = 下一項目; 幀方法[幀索引] = 函數; 幀位置[幀索引] = 方法開始[函數]; 幀棧[幀索引] = 0;
    }
    static void 發回結果(int 類型值) {
        if (類型值 != 方法發回[幀方法[幀索引]]) { 失敗值("return type mismatch"); return; }
        int 值 = 類型值 == 0 ? 0 : 減法值列(類型值);
        幀索引--; if (幀索引 >= 0 && 類型值 != 0) 放入值(值, 類型值);
    }
    static int[] 流檔案名稱 = new int[64];
    static void 檔案流呼叫(int 所有者值, int 名稱, int 格式值, int 命令) {
        boolean 輸出 = 機器字文本(所有者值, "java/io/FileOutputStream");
        int 種類值 = 輸出 ? 6 : 5;
        if (命令 == 183 && 機器字文本(名稱, "<init>")) {
            boolean 繼續狀態值 = false;
            if (輸出 && 機器字文本(格式值, "(Ljava/lang/String;Z)V")) 繼續狀態值 = 減法值列(1) != 0;
            else if (!機器字文本(格式值, "(Ljava/lang/String;)V")) { 失敗值("unsupported file stream constructor"); return; }
            int 檔案條目名稱 = 減法值列(2), 流值 = 減法值列(2);
            if (!物件值(檔案條目名稱, 1) || !物件值(流值, 種類值) || 錯誤) return;
            if (堆值[流值 + 3] != 0) { 失敗值("file stream already initialized"); return; }
            int 長度 = 堆值[檔案條目名稱 + 1];
            if (長度 < 1 || 長度 > 63) { 失敗值("invalid file name length"); return; }
            for (int 槽條目 = 0; 槽條目 < 長度; 槽條目++) {
                int 值 = 堆值[檔案條目名稱 + 2 + 槽條目];
                if (值 < 1 || 值 > 127) { 失敗值("file stream paths currently require ASCII"); return; }
                流檔案名稱[槽條目] = 值;
            }
            流檔案名稱[長度] = 0;
            int 描述符條目 = 使用者.打開檔案描述符(流檔案名稱, 輸出 ? (繼續狀態值 ? 1089 : 577) : 0);
            if (描述符條目 < 0) { 失敗值("FileNotFoundException: file open failed"); return; }
            堆值[流值 + 2] = 描述符條目; 堆值[流值 + 3] = 1;
            return;
        }
        if (命令 != 182) { 失敗值("invalid file stream invocation"); return; }
        int 動作 = -1, 值 = 0;
        if (機器字文本(名稱, "close") && 機器字文本(格式值, "()V")) 動作 = 0;
        if (!輸出 && 機器字文本(名稱, "read") && 機器字文本(格式值, "()I")) 動作 = 1;
        if (輸出 && 機器字文本(名稱, "write") && 機器字文本(格式值, "(I)V")) { 動作 = 2; 值 = 減法值列(1); }
        if (動作 < 0) { 失敗值("unsupported file stream method"); return; }
        int 流值 = 減法值列(2);
        if (!物件值(流值, 種類值) || 錯誤) return;
        if (堆值[流值 + 3] == 0) { 失敗值("uninitialized file stream"); return; }
        int 描述符條目 = 堆值[流值 + 2];
        if (動作 == 0) {
            if (描述符條目 >= 0 && 使用者.關閉檔案描述符(描述符條目) < 0) 失敗值("IOException: close failed");
            堆值[流值 + 2] = -1; return;
        }
        if (描述符條目 < 0) { 失敗值("IOException: stream closed"); return; }
        if (動作 == 1) {
            int 結果 = 使用者.讀取一檔案位元組(描述符條目);
            if (結果 < -1) 失敗值("IOException: read failed"); else 放入值(結果, 1);
        } else if (使用者.寫入一檔案位元組(描述符條目, 值) != 1) 失敗值("IOException: write failed");
    }
    static void 呼叫方法(int 編號, int 命令) {
        if (!檢查常量(編號, 10)) return;
        int 所有者值 = 類別名稱文本(常量首位值[編號]), 名稱 = 引用名稱(常量第二值[編號]), 格式值 = 引用類型(常量第二值[編號]);
        if (錯誤) return;
        if (匹配中機器字(所有者值, 類別名稱)) {
            if (命令 != 184) { 失敗值("only static user methods are supported"); return; }
            for (int 數 = 0; 數 < 方法個數; 數++) if (匹配中機器字(名稱, 方法名稱文本[數]) && 匹配中機器字(格式值, 方法類型[數])) {
                if ((方法存取[數] & 8) == 0) 失敗值("method is not static"); else 調用(數);
                return;
            }
            失敗值("NoSuchMethodError"); return;
        }
        if (機器字文本(所有者值, "java/io/FileInputStream") || 機器字文本(所有者值, "java/io/FileOutputStream")) {
            檔案流呼叫(所有者值, 名稱, 格式值, 命令); return;
        }
        if (命令 == 184 && 機器字文本(所有者值, "java/lang/Integer") && 機器字文本(名稱, "parseInt") && 機器字文本(格式值, "(Ljava/lang/String;)I")) {
            放入值(解碼整數(減法值列(2)), 1); return;
        }
        if (命令 == 182 && 機器字文本(所有者值, "java/io/PrintStream") && (機器字文本(名稱, "println") || 機器字文本(名稱, "print"))) {
            int 類型值 = 0, 值 = 0;
            if (機器字文本(格式值, "(I)V")) { 類型值 = 1; 值 = 減法值列(1); }
            else if (機器字文本(格式值, "(Z)V")) { 類型值 = 2; 值 = 減法值列(1); }
            else if (機器字文本(格式值, "(C)V")) { 類型值 = 3; 值 = 減法值列(1); }
            else if (機器字文本(格式值, "(Ljava/lang/String;)V")) { 類型值 = 4; 值 = 減法值列(2); }
            else if (!機器字文本(格式值, "()V") || !機器字文本(名稱, "println")) 失敗值("unsupported print descriptor");
            if (減法值列(2) != -1) 失敗值("invalid PrintStream receiver");
            if (錯誤) return;
            if (類型值 == 1) Java工具.寫入編號(值);
            if (類型值 == 2) 使用者.寫入(值 == 0 ? "false" : "true");
            if (類型值 == 3) 使用者.寫入字元值(值 & 65535);
            if (類型值 == 4) 寫入文本(值);
            if (機器字文本(名稱, "println")) 使用者.寫入字元值(10);
            return;
        }
        if (命令 == 182 && 機器字文本(所有者值, "java/lang/String")) {
            if (機器字文本(名稱, "length") && 機器字文本(格式值, "()I")) {
                int 引用 = 減法值列(2); if (物件值(引用, 1)) 放入值(堆值[引用 + 1], 1); return;
            }
            if (機器字文本(名稱, "charAt") && 機器字文本(格式值, "(I)C")) {
                int 下標值 = 減法值列(1), 引用 = 減法值列(2);
                if (物件值(引用, 1)) {
                    if (下標值 < 0 || 下標值 >= 堆值[引用 + 1]) 失敗值("StringIndexOutOfBoundsException"); else 放入值(堆值[引用 + 2 + 下標值], 1);
                }
                return;
            }
        }
        if (機器字文本(所有者值, "java/lang/StringBuilder")) {
            if (命令 == 183 && 機器字文本(名稱, "<init>") && 機器字文本(格式值, "()V")) { 物件值(減法值列(2), 4); return; }
            if (命令 == 182 && 機器字文本(名稱, "toString") && 機器字文本(格式值, "()Ljava/lang/String;")) {
                int 引用 = 減法值列(2); if (物件值(引用, 4)) 放入值(堆值[引用 + 2] == 0 ? 宿主字元("") : 堆值[引用 + 2], 2); return;
            }
            if (命令 == 182 && 機器字文本(名稱, "append")) {
                int 文本 = 0;
                if (機器字文本(格式值, "(I)Ljava/lang/StringBuilder;")) 文本 = 數字字元(減法值列(1));
                else if (機器字文本(格式值, "(Z)Ljava/lang/StringBuilder;")) 文本 = 宿主字元(減法值列(1) == 0 ? "false" : "true");
                else if (機器字文本(格式值, "(C)Ljava/lang/StringBuilder;")) {
                    int 值 = 減法值列(1); 文本 = 分配存儲裝置(1, 1); if (!錯誤) 堆值[文本 + 2] = 值 & 65535;
                }
                else if (機器字文本(格式值, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { 文本 = 減法值列(2); if (文本 == 0) 文本 = 宿主字元("null"); }
                else { 失敗值("unsupported StringBuilder append"); return; }
                int 引用 = 減法值列(2); if (!物件值(引用, 4) || !物件值(文本, 1)) return;
                int 前端值 = 堆值[引用 + 2], 前端值長度 = 前端值 == 0 ? 0 : 堆值[前端值 + 1], 後端值長度 = 堆值[文本 + 1];
                int 新建文本 = 分配存儲裝置(1, 前端值長度 + 後端值長度); if (錯誤) return;
                for (int 數 = 0; 數 < 前端值長度; 數++) 堆值[新建文本 + 2 + 數] = 堆值[前端值 + 2 + 數];
                for (int 數 = 0; 數 < 後端值長度; 數++) 堆值[新建文本 + 2 + 前端值長度 + 數] = 堆值[文本 + 2 + 數];
                堆值[引用 + 2] = 新建文本; 放入值(引用, 2); return;
            }
        }
        失敗值("unsupported library method");
    }
    static int 陣列槽(int 引用, int 下標值, int 類型值) {
        if (!物件值(引用, 類型值)) return 0;
        if (下標值 < 0 || 下標值 >= 堆值[引用 + 1]) { 失敗值("ArrayIndexOutOfBoundsException"); return 0; }
        return 引用 + 2 + 下標值;
    }
    static void 執行命令() {
        int 餘數資料 = 500000;
        while (幀索引 >= 0 && !錯誤) {
            if (--餘數資料 == 0) { 失敗值("instruction limit (500000)"); break; }
            int 運行 = 幀位置[幀索引], 值 = 讀取操作碼位元組();
            if (錯誤) break;
            if (值 == 0) continue;
            if (值 == 1) { 放入值(0, 2); continue; }
            if (值 >= 2 && 值 <= 8) { 放入值(值 - 3, 1); continue; }
            if (值 == 16) { 放入值((byte)讀取操作碼位元組(), 1); continue; }
            if (值 == 17) { 放入值((short)讀取操作碼短整數(), 1); continue; }
            if (值 == 18 || 值 == 19) {
                int 數 = 值 == 18 ? 讀取操作碼位元組() : 讀取操作碼短整數();
                if (數 <= 0 || 數 >= 常量個數) 失敗值("invalid ldc constant");
                else if (常量標籤[數] == 3) 放入值(常量首位值[數], 1);
                else if (常量標籤[數] == 8) 放入值(常量文本(常量首位值[數]), 2);
                else 失敗值("unsupported ldc constant");
                continue;
            }
            if (值 == 21 || 值 == 25) { 讀取局部(讀取操作碼位元組(), 值 == 21 ? 1 : 2); continue; }
            if (值 >= 26 && 值 <= 29) { 讀取局部(值 - 26, 1); continue; }
            if (值 >= 42 && 值 <= 45) { 讀取局部(值 - 42, 2); continue; }
            if (值 == 54 || 值 == 58) { 寫入局部(讀取操作碼位元組(), 值 == 54 ? 1 : 2); continue; }
            if (值 >= 59 && 值 <= 62) { 寫入局部(值 - 59, 1); continue; }
            if (值 >= 75 && 值 <= 78) { 寫入局部(值 - 75, 2); continue; }
            if (值 == 46 || 值 == 50) {
                int 下標值 = 減法值列(1), 引用 = 減法值列(2), 槽條目 = 陣列槽(引用, 下標值, 值 == 46 ? 2 : 3);
                if (!錯誤) 放入值(堆值[槽條目], 值 == 46 ? 1 : 2); continue;
            }
            if (值 == 79 || 值 == 83) {
                int 項目元素 = 減法值列(值 == 79 ? 1 : 2), 下標值 = 減法值列(1), 引用 = 減法值列(2), 槽條目 = 陣列槽(引用, 下標值, 值 == 79 ? 2 : 3);
                if (值 == 83 && 項目元素 != 0) 物件值(項目元素, 1);
                if (!錯誤) 堆值[槽條目] = 項目元素; continue;
            }
            if (值 == 87) { 減法值列(0); continue; }
            if (值 == 89) { int 首位操作數 = 減法值列(0), 類型值 = 發回類型; 放入值(首位操作數, 類型值); 放入值(首位操作數, 類型值); continue; }
            if (值 == 95) { int 首位操作數 = 減法值列(0), 首位操作數類型 = 發回類型, 第二操作數 = 減法值列(0), 第二操作數類型 = 發回類型; 放入值(首位操作數, 首位操作數類型); 放入值(第二操作數, 第二操作數類型); continue; }
            if (值 == 96 || 值 == 100 || 值 == 104 || 值 == 108 || 值 == 112 || 值 == 120
                || 值 == 122 || 值 == 124 || 值 == 126 || 值 == 128 || 值 == 130) {
                int 第二操作數 = 減法值列(1), 首位操作數 = 減法值列(1), 結果 = 0;
                if ((值 == 108 || 值 == 112) && 第二操作數 == 0) { 失敗值("ArithmeticException: / by zero"); continue; }
                if (值 == 96) 結果 = 首位操作數 + 第二操作數;
                if (值 == 100) 結果 = 首位操作數 - 第二操作數;
                if (值 == 104) 結果 = 首位操作數 * 第二操作數;
                if (值 == 108) 結果 = 首位操作數 / 第二操作數;
                if (值 == 112) 結果 = 首位操作數 % 第二操作數;
                if (值 == 120) 結果 = 首位操作數 << 第二操作數;
                if (值 == 122) 結果 = 首位操作數 >> 第二操作數;
                if (值 == 124) 結果 = 首位操作數 >>> 第二操作數;
                if (值 == 126) 結果 = 首位操作數 & 第二操作數;
                if (值 == 128) 結果 = 首位操作數 | 第二操作數;
                if (值 == 130) 結果 = 首位操作數 ^ 第二操作數;
                放入值(結果, 1); continue;
            }
            if (值 == 116) { 放入值(-減法值列(1), 1); continue; }
            if (值 == 132) {
                int 局部作用域 = 讀取操作碼位元組(), 遞增步驟 = (byte)讀取操作碼位元組(); 讀取局部(局部作用域, 1); 放入值(減法值列(1) + 遞增步驟, 1); 寫入局部(局部作用域, 1); continue;
            }
            if (值 >= 145 && 值 <= 147) {
                int 數 = 減法值列(1); 放入值(值 == 145 ? (byte)數 : 值 == 146 ? (char)數 : (short)數, 1); continue;
            }
            if (值 >= 153 && 值 <= 167 || 值 == 198 || 值 == 199) {
                int 目的地址值 = 運行 + (short)讀取操作碼短整數(); boolean 應當繼續執行 = 值 == 167;
                if (值 >= 153 && 值 <= 158) {
                    int 數 = 減法值列(1); 應當繼續執行 = 值 == 153 ? 數 == 0 : 值 == 154 ? 數 != 0 : 值 == 155 ? 數 < 0 : 值 == 156 ? 數 >= 0 : 值 == 157 ? 數 > 0 : 數 <= 0;
                } else if (值 >= 159 && 值 <= 166) {
                    int 第二操作數 = 減法值列(值 >= 165 ? 2 : 1), 首位操作數 = 減法值列(值 >= 165 ? 2 : 1);
                    應當繼續執行 = 值 == 159 || 值 == 165 ? 首位操作數 == 第二操作數 : 值 == 160 || 值 == 166 ? 首位操作數 != 第二操作數 : 值 == 161 ? 首位操作數 < 第二操作數 : 值 == 162 ? 首位操作數 >= 第二操作數 : 值 == 163 ? 首位操作數 > 第二操作數 : 首位操作數 <= 第二操作數;
                } else if (值 == 198 || 值 == 199) { int 數 = 減法值列(2); 應當繼續執行 = 值 == 198 ? 數 == 0 : 數 != 0; }
                if (應當繼續執行) 移動值(目的地址值); continue;
            }
            if (值 == 172 || 值 == 176 || 值 == 177) { 發回結果(值 == 172 ? 1 : 值 == 176 ? 2 : 0); continue; }
            if (值 == 178) {
                int 數 = 讀取操作碼短整數(); if (!檢查常量(數, 9)) continue;
                if (!機器字文本(類別名稱文本(常量首位值[數]), "java/lang/System") || !機器字文本(引用名稱(常量第二值[數]), "out")
                    || !機器字文本(引用類型(常量第二值[數]), "Ljava/io/PrintStream;")) 失敗值("unsupported static field");
                else 放入值(-1, 2); continue;
            }
            if (值 == 182 || 值 == 183 || 值 == 184) { 呼叫方法(讀取操作碼短整數(), 值); continue; }
            if (值 == 187) {
                int 名稱 = 類別名稱文本(讀取操作碼短整數());
                if (機器字文本(名稱, "java/lang/StringBuilder")) 放入值(分配存儲裝置(4, 1), 2);
                else if (機器字文本(名稱, "java/io/FileInputStream") || 機器字文本(名稱, "java/io/FileOutputStream")) {
                    int 引用 = 分配存儲裝置(機器字文本(名稱, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!錯誤) { 堆值[引用 + 2] = -1; 放入值(引用, 2); }
                } else 失敗值("unsupported object construction");
                continue;
            }
            if (值 == 188 || 值 == 189) {
                if (值 == 188) { if (讀取操作碼位元組() != 10) 失敗值("only int[] newarray is supported"); }
                else if (!機器字文本(類別名稱文本(讀取操作碼短整數()), "java/lang/String")) 失敗值("only String[] anewarray is supported");
                int 長度 = 減法值列(1); 放入值(分配存儲裝置(值 == 188 ? 2 : 3, 長度), 2); continue;
            }
            if (值 == 190) {
                int 引用 = 減法值列(2);
                if (引用 < 1 || 引用 >= 堆結束位置 - 1 || (堆值[引用] != 2 && 堆值[引用] != 3)) 失敗值("null or invalid array");
                else 放入值(堆值[引用 + 1], 1); continue;
            }
            if (值 == 192) {
                int 名稱 = 類別名稱文本(讀取操作碼短整數()), 引用 = 減法值列(2);
                if (!機器字文本(名稱, "java/lang/String")) 失敗值("unsupported checkcast");
                else if (引用 != 0) 物件值(引用, 1);
                放入值(引用, 2); continue;
            }
            失敗值("unsupported bytecode");
        }
    }
    public static int 運行() {
        if (使用者.參數列個數() == 1 && Java工具.相等文本(使用者.實參(0), "-version")) {
            使用者.寫入("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (使用者.參數列個數() < 1) { 使用者.寫入("Usage: java CLASS [ARGS]\n"); return 2; }
        int 長度 = Java工具.名稱(檔案名稱文本, 使用者.實參(0));
        if (長度 < 1 || 長度 > 57) { 使用者.寫入("java: invalid class name\n"); return 2; }
        檔案名稱文本[長度] = '.'; 檔案名稱文本[長度 + 1] = 'c'; 檔案名稱文本[長度 + 2] = 'l'; 檔案名稱文本[長度 + 3] = 'a'; 檔案名稱文本[長度 + 4] = 's'; 檔案名稱文本[長度 + 5] = 's';
        大小 = 使用者.讀取檔案(檔案名稱文本, 檔案);
        if (大小 < 0) { 使用者.寫入("java: cannot read class: "); Java工具.寫入編號(大小); 使用者.寫入字元值(10); return 1; }
        讀取類別(); if (錯誤) return 1;
        int 字元名稱 = 常量文本(類別名稱);
        if (!錯誤 && 堆值[字元名稱 + 1] != 長度) 失敗值("class name does not match file");
        for (int 數 = 0; 數 < 長度 && !錯誤; 數++) if (堆值[字元名稱 + 2 + 數] != 檔案名稱文本[數]) 失敗值("class name does not match file");
        int 條目分值 = -1;
        for (int 數 = 0; 數 < 方法個數; 數++) if (機器字文本(方法名稱文本[數], "main") && 機器字文本(方法類型[數], "([Ljava/lang/String;)V") && (方法存取[數] & 9) == 9) 條目分值 = 數;
        if (條目分值 < 0) 失敗值("public static void main(String[] args) required");
        if (錯誤) return 1;
        int 實參 = 分配存儲裝置(3, 使用者.參數列個數() - 1);
        for (int 數 = 1; 數 < 使用者.參數列個數() && !錯誤; 數++) 堆值[實參 + 1 + 數] = 宿主字元(使用者.實參(數));
        幀索引 = 0; 幀方法[0] = 條目分值; 幀位置[0] = 方法開始[條目分值]; 局部值[0] = 實參; 局部類型[0] = 2;
        執行命令(); return 錯誤 ? 1 : 0;
    }
}
