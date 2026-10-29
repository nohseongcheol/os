// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 命令列，支援引號、Backspace、Ctrl-U、Ctrl-C 與 RAM 編輯器。 */
public final class 命令解釋器 {
    static int[] 行 = new int[4096], 詞元值 = new int[4096], 起始分 = new int[32], 長度 = new int[32];
    static int[] 已編輯內容 = new int[16384], 編輯名稱 = new int[63];
    static int 詞元個數, 編輯名稱長度, 結果;
    static boolean 上一個行;
    static void 原始位元組(int 值) { 板.寫入串行(值); }
    static int 讀取輸入行() { return 行編輯器.讀取(); }
    static boolean 相割值列(int 大小) {
        int 位置 = 0, 結尾 = 0; 詞元個數 = 0;
        while (位置 < 大小) {
            while (位置 < 大小 && (行[位置] == 32 || 行[位置] == 9)) 位置++;
            if (位置 == 大小) break;
            if (詞元個數 == 16) { 終端輸入輸出.寫入("命令 解析值: 인수가 너무 많습니다\n"); return false; }
            起始分[詞元個數] = 結尾; int 引號值 = 0;
            while (位置 < 大小) {
                int 值 = 行[位置++];
                if (引號值 == 0 && (值 == 32 || 值 == 9)) break;
                if (值 == 引號值) { 引號值 = 0; continue; }
                if (引號值 == 0 && (值 == 39 || 值 == 34)) { 引號值 = 值; continue; }
                詞元值[結尾++] = 值;
            }
            if (引號值 != 0) { 終端輸入輸出.寫入("命令 解析值: 따옴표가 닫히지 않았습니다\n"); return false; }
            長度[詞元個數] = 結尾 - 起始分[詞元個數]; 詞元個數++;
        }
        return true;
    }
    static boolean 相等文本(int 編號, String 機器字文本) {
        if (編號 >= 詞元個數) return false;
        int 位置索引=0;
        for (int 序數索引=0; 序數索引<機器字文本.length(); 序數索引++) {
            int 字元程式碼=機器字文本.charAt(序數索引);
            if (字元程式碼>=0xd800 && 字元程式碼<=0xdbff && 序數索引+1<機器字文本.length()) 字元程式碼=0x10000+((字元程式碼-0xd800)<<10)+機器字文本.charAt(++序數索引)-0xdc00;
            int 位元組個數=字元程式碼<128?1:字元程式碼<2048?2:字元程式碼<65536?3:4;
            for (int 序列值=位元組個數-1; 序列值>=0; 序列值--) {
                int 值=位元組個數==1?字元程式碼:序列值==位元組個數-1?(位元組個數==2?0xc0:位元組個數==3?0xe0:0xf0)|(字元程式碼>>(6*序列值)):0x80|((字元程式碼>>(6*序列值))&63);
                if (位置索引>=長度[編號] || 詞元值[起始分[編號]+位置索引++]!=值) return false;
            }
        }
        return 位置索引==長度[編號];
    }
    static int 路徑(int 編號) {
        if (編號 >= 詞元個數) return -22;
        int 結果 = 記憶體檔案集.路徑開始(長度[編號]); if (結果 < 0) return 結果;
        for (int 循環索引 = 0; 循環索引 < 長度[編號]; 循環索引++) {
            結果 = 記憶體檔案集.路徑位元組(循環索引, 詞元值[起始分[編號] + 循環索引]); if (結果 < 0) return 結果;
        }
        return 0;
    }
    static void 錯誤(int 編號) { 結果 = 1; 終端輸入輸出.寫入("錯誤 "); 終端輸入輸出.數(編號); 終端輸入輸出.字元(10); }
    static void 視圖值() {
        if (詞元個數 != 2) { 終端輸入輸出.寫入("사용법: cat 檔案\n"); return; }
        int 結果 = 路徑(1); if (結果 < 0) { 錯誤(結果); return; }
        int 檔案 = 記憶體檔案集.打開(0); if (檔案 < 0) { 錯誤(檔案); return; }
        while (true) { int 值 = 記憶體檔案集.讀取(檔案); if (值 == 256) break; if (值 < 0) { 錯誤(值); break; } 原始位元組(值); }
        記憶體檔案集.關閉(檔案); 終端輸入輸出.字元(10);
    }
    static void 編輯值() {
        if (詞元個數 != 2) { 終端輸入輸出.寫入("사용법: edit 檔案\n"); return; }
        int 結果 = 路徑(1); if (結果 < 0) { 錯誤(結果); return; }
        編輯名稱長度 = 長度[1];
        for (int 循環索引 = 0; 循環索引 < 編輯名稱長度; 循環索引++) 編輯名稱[循環索引] = 詞元值[起始分[1] + 循環索引];
        終端輸入輸出.寫入("EDIT: 檔案 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(最大值 16384바이트)\n");
        int 大小 = 0;
        while (true) {
            終端輸入輸出.寫入("edit> "); int 輸入值 = 讀取輸入行();
            if (輸入值 < 0) { 終端輸入輸出.寫入("EDIT CANCELLED\n"); return; }
            if (輸入值 == 1 && 行[0] == '.') break;
            if (輸入值 + 1 > 已編輯內容.length - 大小) { 終端輸入輸出.寫入("EDIT CANCELLED: file too large\n"); return; }
            for (int 循環索引 = 0; 循環索引 < 輸入值; 循環索引++) 已編輯內容[大小++] = 行[循環索引];
            已編輯內容[大小++] = 10;
        }
        記憶體檔案集.路徑開始(編輯名稱長度);
        for (int 循環索引 = 0; 循環索引 < 編輯名稱長度; 循環索引++) 記憶體檔案集.路徑位元組(循環索引, 編輯名稱[循環索引]);
        int 檔案 = 記憶體檔案集.打開(577); if (檔案 < 0) { 錯誤(檔案); return; }
        for (int 循環索引 = 0; 循環索引 < 大小; 循環索引++) 記憶體檔案集.寫入(檔案, 已編輯內容[循環索引]);
        記憶體檔案集.關閉(檔案); 終端輸入輸出.寫入("SAVED "); 終端輸入輸出.數(大小); 終端輸入輸出.寫入("位元組值(주기억 檔案)\n");
    }
    static int 十六進制數值(int 值) {
        if (值 >= '0' && 值 <= '9') return 值 - '0';
        if (值 >= 'a' && 值 <= 'f') return 值 - 'a' + 10;
        if (值 >= 'A' && 值 <= 'F') return 值 - 'A' + 10;
        return -1;
    }
    static void 二進制輸入輸出(boolean 放入值) {
        if (詞元個數 != 2) { 終端輸入輸出.寫入("사용법: load 檔案 | hex 檔案\n"); return; }
        int 結果 = 路徑(1); if (結果 < 0) { 錯誤(結果); return; }
        if (!放入值) {
            int 檔案 = 記憶體檔案集.打開(0); if (檔案 < 0) { 錯誤(檔案); return; }
            終端輸入輸出.寫入("HEX BEGIN "); 終端輸入輸出.數(記憶體檔案集.大小(檔案)); 終端輸入輸出.字元(10);
            int 條目個數 = 0;
            while (true) {
                int 值 = 記憶體檔案集.讀取(檔案); if (值 < 0 || 值 == 256) break;
                終端輸入輸出.字元("0123456789abcdef".charAt(值 >> 4)); 終端輸入輸出.字元("0123456789abcdef".charAt(值 & 15));
                if (++條目個數 % 32 == 0) 終端輸入輸出.字元(10);
            }
            if (條目個數 % 32 != 0) 終端輸入輸出.字元(10);
            記憶體檔案集.關閉(檔案); 終端輸入輸出.寫入("HEX END\n"); return;
        }
        編輯名稱長度 = 長度[1];
        for (int 循環索引 = 0; 循環索引 < 編輯名稱長度; 循環索引++) 編輯名稱[循環索引] = 詞元值[起始分[1] + 循環索引];
        終端輸入輸出.寫入("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int 大小 = 0;
        while (true) {
            終端輸入輸出.寫入("hex> "); int 輸入值 = 讀取輸入行();
            if (輸入值 < 0) { 終端輸入輸出.寫入("LOAD CANCELLED\n"); return; }
            if (輸入值 == 1 && 行[0] == '.') break;
            int 前端值 = -1;
            for (int 循環索引 = 0; 循環索引 < 輸入值; 循環索引++) {
                if (行[循環索引] == 32 || 行[循環索引] == 9) continue;
                int 值 = 十六進制數值(行[循環索引]);
                if (值 < 0 || 大小 >= 已編輯內容.length) { 終端輸入輸出.寫入("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (前端值 < 0) 前端值 = 值; else { 已編輯內容[大小++] = 前端值 * 16 + 值; 前端值 = -1; }
            }
            if (前端值 >= 0) { 終端輸入輸出.寫入("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        記憶體檔案集.路徑開始(編輯名稱長度);
        for (int 循環索引 = 0; 循環索引 < 編輯名稱長度; 循環索引++) 記憶體檔案集.路徑位元組(循環索引, 編輯名稱[循環索引]);
        int 檔案 = 記憶體檔案集.打開(577); if (檔案 < 0) { 錯誤(檔案); return; }
        for (int 循環索引 = 0; 循環索引 < 大小; 循環索引++) 記憶體檔案集.寫入(檔案, 已編輯內容[循環索引]);
        記憶體檔案集.關閉(檔案); 終端輸入輸出.寫入("LOADED "); 終端輸入輸出.數(大小); 終端輸入輸出.寫入("位元組值(주기억 檔案)\n");
    }
    static int 工具集(int 編號) {
        return 工具條目(編號, 1);
    }
    static int 工具條目(int 編號, int 運行) {
        if (詞元個數 - 運行 > 8) return -22;
        板.準備參數列(詞元個數 - 運行);
        for (int 首位資料 = 運行; 首位資料 < 詞元個數; 首位資料++) {
            if (長度[首位資料] > 255) return -36;
            for (int 循環索引 = 0; 循環索引 < 長度[首位資料]; 循環索引++) 板.實際參數位元組(首位資料 - 運行, 循環索引, 詞元值[起始分[首位資料] + 循環索引]);
        }
        return 編號 == -2 ? 板.執行Linux檔案() : 編號 < 0 ? 板.執行用戶檔案() : 板.運行用戶程式(編號);
    }
    static int Python捆綁() {
        if (詞元個數 > 8) return -22;
        板.準備參數列(詞元個數);
        String 路徑 = "/lib/軟件包.py";
        // 將 Java 字串寫入 shell 的 UTF-8 引數緩衝區。
        int 位置索引 = 0;
        for (int 序數索引 = 0; 序數索引 < 路徑.length(); 序數索引++) {
            int 字元值 = 路徑.charAt(序數索引);
            if (字元值 < 128) 板.實際參數位元組(0, 位置索引++, 字元值);
            else { 板.實際參數位元組(0, 位置索引++, 0xe0 | (字元值 >> 12)); 板.實際參數位元組(0, 位置索引++, 0x80 | ((字元值 >> 6) & 63)); 板.實際參數位元組(0, 位置索引++, 0x80 | (字元值 & 63)); }
        }
        for (int 序數索引 = 1; 序數索引 < 詞元個數; 序數索引++) {
            if (長度[序數索引] > 255) return -36;
            for (int 字元值 = 0; 字元值 < 長度[序數索引]; 字元值++) 板.實際參數位元組(序數索引, 字元值, 詞元值[起始分[序數索引] + 字元值]);
        }
        return 板.運行用戶程式(12);
    }
    static int 執行狀態格式() {
        int 已處理值 = 路徑(0); if (已處理值 < 0) return 已處理值;
        int 檔案 = 記憶體檔案集.打開(0); if (檔案 < 0) return 檔案;
        int 首位資料 = 記憶體檔案集.讀取(檔案), 位元組資料 = 記憶體檔案集.讀取(檔案), 字元程式碼 = 記憶體檔案集.讀取(檔案), 尾隨值 = 記憶體檔案集.讀取(檔案);
        記憶體檔案集.關閉(檔案);
        if (首位資料 == 127 && 位元組資料 == 'E' && 字元程式碼 == 'L' && 尾隨值 == 'F') return 1;
        if (首位資料 == 'P' && 位元組資料 == 'K' && 字元程式碼 == 3 && 尾隨值 == 4) return 2;
        return 0;
    }
    static int 運行範例(int 編號, String 實參) {
        板.準備參數列(1);
        for (int 循環索引 = 0; 循環索引 < 實參.length(); 循環索引++) 板.實際參數位元組(0, 循環索引, 實參.charAt(循環索引));
        return 板.運行用戶程式(編號);
    }
    static void 文本位元組(int 檔案, int 值) { 記憶體檔案集.寫入(檔案, 值); }
    static void 靜態檔案(String 名稱, String 內容值) {
        // 套件內檔名使用 ASCII，檔案內容以 UTF-8 儲存。
        記憶體檔案集.路徑開始(名稱.length());
        for (int 循環索引 = 0; 循環索引 < 名稱.length(); 循環索引++) 記憶體檔案集.路徑位元組(循環索引, 名稱.charAt(循環索引));
        int 檔案 = 記憶體檔案集.打開(193); if (檔案 < 0) return;
        for (int 循環索引 = 0; 循環索引 < 內容值.length(); 循環索引++) {
            int 字元程式碼 = 內容值.charAt(循環索引);
            if (字元程式碼 >= 0xd800 && 字元程式碼 <= 0xdbff && 循環索引 + 1 < 內容值.length()) 字元程式碼 = 0x10000 + ((字元程式碼 - 0xd800) << 10) + 內容值.charAt(++循環索引) - 0xdc00;
            if (字元程式碼 < 128) 文本位元組(檔案, 字元程式碼);
            else {
                int 數 = 字元程式碼 < 2048 ? 2 : 字元程式碼 < 65536 ? 3 : 4;
                文本位元組(檔案, (數 == 2 ? 0xc0 : 數 == 3 ? 0xe0 : 0xf0) | (字元程式碼 >> (6 * (數 - 1))));
                for (int 條目個數 = 數 - 1; 條目個數 > 0; 條目個數--) 文本位元組(檔案, 0x80 | ((字元程式碼 >> (6 * (條目個數 - 1))) & 63));
            }
        }
        記憶體檔案集.關閉(檔案);
    }
    static void 韓文字母幫助() {
        終端輸入輸出.寫入("按 F9 或 Shift+Space 可切換到中文拼音輸入。\n");
        終端輸入輸出.寫入("  [ZH_HANT] candidates; [EN] ASCII\n");
        終端輸入輸出.寫入("  ni → 你\n");
        終端輸入輸出.寫入("  F9: EN ↔ zh_Hant | Ctrl+Shift+V: UTF-8\n");
        終端輸入輸出.寫入("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        終端輸入輸出.寫入("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
        終端輸入輸出.寫入("  Space: next candidate; F9: commit / EN\n");
        終端輸入輸出.寫入("  Syllable candidates: Space cycles, F9 commits. No predictive phrase model.\n");
    }
    static int 範例路徑(String 名稱) {
        int 位元組個數 = 0;
        for (int 循環索引 = 0; 循環索引 < 名稱.length(); 循環索引++) { int 字元程式碼 = 名稱.charAt(循環索引); if (字元程式碼 >= 0xd800 && 字元程式碼 <= 0xdfff) return -22; 位元組個數 += 字元程式碼 < 128 ? 1 : 字元程式碼 < 2048 ? 2 : 3; }
        int 已處理值 = 記憶體檔案集.路徑開始(位元組個數); if (已處理值 < 0) return 已處理值;
        int 位置索引 = 0;
        for (int 循環索引 = 0; 循環索引 < 名稱.length(); 循環索引++) {
            int 字元程式碼 = 名稱.charAt(循環索引);
            if (字元程式碼 < 128) 記憶體檔案集.路徑位元組(位置索引++, 字元程式碼);
            else if (字元程式碼 < 2048) { 記憶體檔案集.路徑位元組(位置索引++, 0xc0 | (字元程式碼 >> 6)); 記憶體檔案集.路徑位元組(位置索引++, 0x80 | (字元程式碼 & 63)); }
            else { 記憶體檔案集.路徑位元組(位置索引++, 0xe0 | (字元程式碼 >> 12)); 記憶體檔案集.路徑位元組(位置索引++, 0x80 | ((字元程式碼 >> 6) & 63)); 記憶體檔案集.路徑位元組(位置索引++, 0x80 | (字元程式碼 & 63)); }
        }
        return 0;
    }
    static int 範例目錄(String 名稱) {
        int 已處理值 = 範例路徑(名稱); if (已處理值 < 0) return 已處理值;
        已處理值 = 記憶體檔案集.創建目錄(); return 已處理值 == -17 ? 0 : 已處理值;
    }
    static int 範例檔案(String 名稱, String 資料) {
        int 已處理值 = 範例路徑(名稱); if (已處理值 < 0) return 已處理值;
        int 檔案 = 記憶體檔案集.打開(193); if (檔案 == -17) return 0; if (檔案 < 0) return 檔案;
        for (int 循環索引 = 0; 循環索引 < 資料.length(); 循環索引 += 2) {
            已處理值 = 記憶體檔案集.寫入(檔案, 十六進制數值(資料.charAt(循環索引)) * 16 + 十六進制數值(資料.charAt(循環索引 + 1)));
            if (已處理值 < 0) { 記憶體檔案集.關閉(檔案); return 已處理值; }
        }
        return 記憶體檔案集.關閉(檔案);
    }
    static void 顯示幫助() {
        系統工具.顯示幫助();
        終端輸入輸出.寫入("sshd / 安全命令殼 start|stop|status: SSH :22 (user, 장치별 密碼值)\n");
        終端輸入輸出.寫入("vncd / 遠程顯示操作 start|stop|status: VNC :5900 (장치별 密碼值)\n");
        終端輸入輸出.寫入("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        終端輸入輸出.寫入("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        終端輸入輸出.寫入("wc grep head tail tee env export unset history sh source true false exit\n");
        終端輸入輸出.寫入("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        終端輸入輸出.寫入("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        終端輸入輸出.寫入("角值 + 左側 버튼 拖動值: 終端 大小 更改值; terminal size: 欄值/列值\n");
        終端輸入輸出.寫入("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        終端輸入輸出.寫入("vi FILE: i to insert; Esc then :wq to save and quit\n");
        終端輸入輸出.寫入("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        終端輸入輸出.寫入("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        終端輸入輸出.寫入("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        終端輸入輸出.寫入("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        終端輸入輸出.寫入("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        終端輸入輸出.寫入("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        終端輸入輸出.寫入("python FILE.py | python -c 'CODE' (MicroPython)\n");
        終端輸入輸出.寫入("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        終端輸入輸出.寫入("pip: MicroPython 原始碼樹 安裝值; 宿主 --network --pip 所需條件值; /lib는 RAM\n");
        終端輸入輸出.寫入("gui | run cpp | net test | tasks | selftest | samples\n");
        終端輸入輸出.寫入("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        終端輸入輸出.寫入("/example/java /example/c /example/python: examples ready at boot\n");
        終端輸入輸出.寫入("example java|c|python: restore missing examples (keeps existing files)\n");
        韓文字母幫助();
    }
    static void 終端(boolean 曾經已切換) {
        if (曾經已切換 && 板.終端(2) != 0) { 板.終端(0); 終端輸入輸出.寫入("TERMINAL CLOSED\n"); }
        else if (板.終端(1) < 0) 錯誤(-19);
        else 終端輸入輸出.寫入("TERMINAL READY — zh_Hant terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void 命令() {
        if (詞元個數 == 0) return;
        if (系統工具.執行命令()) return;
        if (相等文本(0,"sshd") || 相等文本(0,"安全命令殼") || 相等文本(0,"vncd") || 相等文本(0,"遠程顯示操作")) {
            int 種類值=相等文本(0,"vncd")||相等文本(0,"遠程顯示操作")?1:0;
            int 動作=相等文本(1,"start")||相等文本(1,"運行")?1:相等文本(1,"stop")||相等文本(1,"停止")?0:2;
            int 狀態值=板.遠程控制(種類值,動作);
            if(狀態值<0)錯誤(狀態值);else 終端輸入輸出.寫入(板.遠程控制(種類值,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (相等文本(0, "help") || 相等文本(0, "h")) { if (相等文本(1, "ko") || 相等文本(1, "input")) 韓文字母幫助(); else 顯示幫助(); }
        else if (相等文本(0, "info") || 相等文本(0, "i")) 內核.系統信息();
        else if (相等文本(0, "pwd")) { 記憶體檔案集.當前寫入(); 終端輸入輸出.字元(10); }
        else if (相等文本(0, "cd")) {
            int 已處理值;
            if (詞元個數 == 1) { 記憶體檔案集.路徑開始(1); 已處理值 = 記憶體檔案集.路徑位元組(0, '/'); } else 已處理值 = 詞元個數 == 2 ? 路徑(1) : -22;
            if (已處理值 >= 0) 已處理值 = 記憶體檔案集.更改目錄(); if (已處理值 < 0) 錯誤(已處理值);
        }
        else if (相等文本(0, "ls") || 相等文本(0, "f")) {
            int 實際參數索引 = 相等文本(1, "-l") ? 2 : 1, 已處理值;
            if (詞元個數 == 實際參數索引) { 記憶體檔案集.路徑開始(1); 已處理值 = 記憶體檔案集.路徑位元組(0, '.'); } else 已處理值 = 詞元個數 == 實際參數索引 + 1 ? 路徑(實際參數索引) : -22;
            if (已處理值 >= 0) 已處理值 = 記憶體檔案集.路徑條目列(); if (已處理值 < 0) 錯誤(已處理值);
        }
        else if (相等文本(0, "mkdir") || 相等文本(0, "rmdir") || 相等文本(0, "touch")) 命令殼工具.檔案作業(相等文本(0, "mkdir") ? "mkdir" : 相等文本(0, "rmdir") ? "rmdir" : "touch");
        else if (相等文本(0, "cp") || 相等文本(0, "mv")) 命令殼工具.複製值(相等文本(0, "mv"));
        else if (相等文本(0, "cat")) 命令殼工具.視圖值();
        else if (相等文本(0, "wc")) 命令殼工具.計數中值();
        else if (相等文本(0, "grep")) 命令殼工具.查找條目();
        else if (相等文本(0, "head") || 相等文本(0, "tail")) 命令殼工具.頭值(相等文本(0, "tail"));
        else if (相等文本(0, "tee")) 命令殼工具.寫入共同();
        else if (相等文本(0, "env")) 命令殼語法.顯示環境();
        else if (相等文本(0, "export") || 相等文本(0, "unset")) {
            if (詞元個數 == 1) 命令殼語法.顯示環境();
            for (int 循環索引 = 1; 循環索引 < 詞元個數; 循環索引++) { int 已處理值 = 命令殼語法.環境設置(循環索引, 相等文本(0, "unset")); if (已處理值 != 0) { 結果 = 已處理值; 終端輸入輸出.寫入("命令 解析值: 變量值 이름이 잘못되었거나 예약된 이름이거나 環境 공간이 가득 찼습니다\n"); } }
        }
        else if (相等文本(0, "sh") || 相等文本(0, "source")) 命令殼語法.執行檔案();
        else if (相等文本(0, "true")) 結果 = 0;
        else if (相等文本(0, "false")) 結果 = 1;
        else if (相等文本(0, "history")) 行編輯器.顯示日誌();
        else if (相等文本(0, "exit")) {
            if (命令殼語法.深度值 > 0) { 結果 = 詞元個數 == 1 ? 命令殼語法.狀態值 : 命令殼工具.數字值(1); if (結果 < 0 || 結果 > 255) 結果 = 2; 命令殼語法.腳本結束 = true; }
            else if (板.終端(2) != 0) 終端(true);
            else 終端輸入輸出.寫入("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (相等文本(0, "edit")) 編輯值();
        else if (相等文本(0, "load") || 相等文本(0, "hex")) 二進制輸入輸出(相等文本(0, "load"));
        else if (相等文本(0, "rm")) {
            if (詞元個數 < 2) { 結果 = 2; 終端輸入輸出.寫入("사용법: rm 檔案...\n"); }
            for (int 循環索引 = 1; 循環索引 < 詞元個數; 循環索引++) { int 已處理值 = 路徑(循環索引); if (已處理值 == 0) 已處理值 = 記憶體檔案集.擦除條目(); if (已處理值 < 0) 錯誤(已處理值); }
        }
        else if (相等文本(0, "echo")) {
            int 開始位置 = 相等文本(1, "-n") ? 2 : 1;
            for (int 首位資料 = 開始位置; 首位資料 < 詞元個數; 首位資料++) { if (首位資料 > 開始位置) 終端輸入輸出.字元(32); for (int 循環索引 = 0; 循環索引 < 長度[首位資料]; 循環索引++) 板.寫入串行(詞元值[起始分[首位資料] + 循環索引]); }
            if (開始位置 == 1) 終端輸入輸出.字元(10);
        }
        else if (相等文本(0, "clear")) 終端輸入輸出.寫入("\u001b[2J\u001b[H");
        else if (相等文本(0, "javac") || 相等文本(0, "java") || 相等文本(0, "python") || 相等文本(0, "pip")) {
            int 已處理值 = 相等文本(0, "pip") ? Python捆綁() : 工具集(相等文本(0, "javac") ? 10 : 相等文本(0, "java") ? 11 : 12); 結果 = 已處理值 == -1005 ? -1005 : 已處理值 < 0 ? 126 : 已處理值;
            if (已處理值 != -1005 && !命令殼語法.是否連接中) { 終端輸入輸出.寫入("exit "); 終端輸入輸出.數(已處理值); 終端輸入輸出.字元(10); }
        }
        else if (相等文本(0, "vi")) { int 已處理值 = 工具集(13); 結果 = 已處理值 == -1005 ? -1005 : 已處理值 < 0 ? 126 : 已處理值; }
        else if (相等文本(0, "cc") || 相等文本(0, "tcc")) { int 已處理值 = 工具集(15); 結果 = 已處理值 < 0 ? 126 : 已處理值; if (!命令殼語法.是否連接中) { 終端輸入輸出.寫入("exit "); 終端輸入輸出.數(已處理值); 終端輸入輸出.字元(10); } }
        else if (相等文本(0, "jaot")) { int 已處理值 = 工具集(16); 結果 = 已處理值 < 0 ? 126 : 已處理值; if (!命令殼語法.是否連接中) { 終端輸入輸出.寫入("exit "); 終端輸入輸出.數(已處理值); 終端輸入輸出.字元(10); } }
        else if (相等文本(0, "terminal")) {
            if (相等文本(1, "size")) { int 大小 = 板.終端(13); 終端輸入輸出.寫入("TERMINAL SIZE "); 終端輸入輸出.數(大小 & 65535); 終端輸入輸出.字元('x'); 終端輸入輸出.數(大小 >>> 16); 終端輸入輸出.字元(10); }
            else 終端(false);
        }
        else if (相等文本(0, "gui") || 相等文本(0, "v")) { 板.終端(9); 桌面.執行命令(); }
        else if (相等文本(0, "c")) 內核.測試C();
        else if (相等文本(0, "tasks") || 相等文本(0, "t")) 內核.測試任務列();
        else if (相等文本(0, "g")) 內核.屏幕();
        else if (相等文本(0, "selftest") || 相等文本(0, "u")) 內核.測試用戶程式列();
        else if (相等文本(0, "e") || (相等文本(0, "run") && 相等文本(1, "cpp"))) {
            int 已處理值 = 板.運行用戶程式(0); if (已處理值 == 0) 終端輸入輸出.寫入("ELF DEMO PASS\n"); else 錯誤(已處理值);
        }
        else if (相等文本(0, "run")) { int 已處理值 = 相等文本(1, "--linux") ? 工具條目(-2, 2) : 工具集(-1); 結果 = 已處理值 == -1005 ? -1005 : 已處理值 < 0 ? 126 : 已處理值; if (已處理值 != -1005 && !命令殼語法.是否連接中) { 終端輸入輸出.寫入("exit "); 終端輸入輸出.數(已處理值); 終端輸入輸出.字元(10); } }
        else if (相等文本(0, "n") || (相等文本(0, "net") && 相等文本(1, "test"))) 內核.測試聯網();
        else if (相等文本(0, "ftpd")) {
            if (相等文本(1, "start")) { int 已處理值 = 板.檔案傳送服務(1); if (已處理值 < 0) 錯誤(已處理值); else { 終端輸入輸出.寫入("FTP listening "); 系統工具.寫入地址(板.網路運行狀態(0,0)); 終端輸入輸出.寫入(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (相等文本(1, "stop")) { 板.檔案傳送服務(0); 終端輸入輸出.寫入("FTP stopped\n"); }
            else 終端輸入輸出.寫入(板.檔案傳送服務(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (相等文本(0, "samples")) { 軟件包.準備(); 終端輸入輸出.寫入("SAMPLES READY (existing files kept)\n"); }
        else if (相等文本(0, "example")) {
            int 語言 = 相等文本(1, "java") ? 0 : 相等文本(1, "c") ? 1 : 相等文本(1, "python") ? 2 : -1;
            if (詞元個數 != 2 || 語言 < 0) 終端輸入輸出.寫入("example java|c|python: 輸出, 檔案, 네트워크, 그래픽, Java Swing 窗口 範例\n");
            else { int 已處理值 = 範例捆綁.安裝值(語言); if (已處理值 < 0) { 錯誤(已處理值); if (已處理值 == -28) 終端輸入輸出.寫入("RAM full: remove unused files, then retry example\n"); } else 終端輸入輸出.寫入("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int 格式值 = 執行狀態格式();
            if (格式值 == 1 || 格式值 == 2) {
                int 已處理值 = 工具條目(格式值 == 1 ? -1 : 14, 0); 結果 = 已處理值 == -1005 ? -1005 : 已處理值 < 0 ? 126 : 已處理值;
                if (已處理值 != -1005 && !命令殼語法.是否連接中) { 終端輸入輸出.寫入("exit "); 終端輸入輸出.數(已處理值); 終端輸入輸出.字元(10); }
            } else if (格式值 == 0) { 結果 = 126; 終端輸入輸出.寫入("실행할 數 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 結果 = 127; 終端輸入輸出.寫入("Unknown command. help: commands\n"); }
        }
    }
    public static void 執行命令() {
        軟件包.準備();
        for (int 語言 = 0; 語言 < 3; 語言++) { int 已處理值 = 範例捆綁.安裝值(語言); if (已處理值 < 0) 錯誤(已處理值); }
        顯示幫助();
        while (true) {
            窗口會話.程序值條目(); if (窗口會話.恢復執行執行狀態()) continue;
            if (!窗口會話.讀取繼續狀態) 終端輸入輸出.寫入("jkoros-native> "); 行編輯器.命令行 = true; 板.遠程等待狀態(1); int 大小 = 讀取輸入行(); 板.遠程等待狀態(0); 行編輯器.命令行 = false;
            if (大小 == -3) continue;
            if (大小 == -2) 終端輸入輸出.寫入("命令 解析值: 명령줄이 너무 깁니다\n");
            if (大小 >= 0) { 命令殼語法.腳本結束 = false; 命令殼語法.執行命令(行, 0, 大小, 0); } else 命令殼語法.狀態值 = 130;
            板.結束遠程命令(命令殼語法.狀態值);
            行編輯器.大小 = 行編輯器.光標值 = 行編輯器.開始窗口 = 0;
        }
    }
}
