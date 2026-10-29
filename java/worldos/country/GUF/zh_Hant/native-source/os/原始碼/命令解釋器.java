// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 不寫入磁碟的小型串列埠/PS2 命令解譯器。 */
public final class 命令解釋器 {
    static int[] 輸入值 = new int[128];
    static int 長度 = 0;
    static boolean 發回目標側上一個行 = false;
    static boolean 行溢出 = false;

    static boolean 命令(String 名稱) {
        if (長度 < 名稱.length()) return false;
        for (int 編號 = 0; 編號 < 名稱.length(); 編號++)
            if (輸入值[編號] != 名稱.charAt(編號)) return false;
        return 長度 == 名稱.length() || 輸入值[名稱.length()] == ' ';
    }

    static void 顯示幫助() {
        字元終端.寫入("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        字元終端.寫入("apps | run NAME [ARGS] | net\n");
        字元終端.寫入("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        字元終端.寫入("sync (연결된 JKSTORE1 存儲值 장치에 檔案 보존)\n");
    }

    static void 程序值條目() {
        if (長度 == 0) return;
        if (命令("help")) 顯示幫助();
        else if (命令("sync")) {
            int 結果 = 檔案持久化.同步化();
            字元終端.寫入("Sync: "); 字元終端.寫入編號(結果); 字元終端.字元(10);
        }
        else if (命令("ls")) 主記憶體檔案系統.條目列表();
        else if (命令("edit")) 主記憶體檔案系統.命令(輸入值, 4, 長度, 0);
        else if (命令("cat")) 主記憶體檔案系統.命令(輸入值, 3, 長度, 1);
        else if (命令("rm")) 主記憶體檔案系統.命令(輸入值, 2, 長度, 2);
        else if (命令("java") || 命令("javac")) {
            int 結果 = 執行管理.執行命令(輸入值, 0, 長度);
            字元終端.寫入("Exit: "); 字元終端.寫入編號(結果); 字元終端.字元(10);
        }
        else if (命令("apps")) 執行管理.條目列表();
        else if (命令("net")) 通信網絡.狀態值();
        else if (命令("run")) {
            int 結果 = 執行管理.執行命令(輸入值, 3, 長度);
            字元終端.寫入("Exit: "); 字元終端.寫入編號(結果); 字元終端.寫入("\n");
        } else if (命令("info")) {
            字元終端.寫入("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (命令("mem")) {
            字元終端.寫入("上位側側 記憶體 地址區域(KiB): "); 字元終端.寫入編號(記憶體空間.上位側記憶體大小());
            字元終端.寫入("\n배열 동적 記憶體 地址區域(位元組值): "); 字元終端.寫入編號(設備.陣列用量());
            字元終端.寫入(" / 262144\n작업 地址區域 區段值: "); 字元終端.寫入編號(記憶體空間.已使用條目個數());
            字元終端.寫入(" / 8 (각 4096바이트)\n");
        } else if (命令("alloc")) {
            int 編號 = 記憶體空間.分配存儲裝置();
            字元終端.寫入("區段值 編號: "); 字元終端.寫入編號(編號); 字元終端.寫入("\n");
        } else if (命令("free")) {
            if (長度 == 6 && 輸入值[4] == ' ' && 輸入值[5] >= '0' && 輸入值[5] <= '7') {
                字元終端.寫入(記憶體空間.發回結果(輸入值[5] - '0') ? "반환됨\n" : "할당되지 않은 區段值\n");
            } else 字元終端.寫入("사용법: free 0..7\n");
        } else if (命令("echo")) {
            for (int 編號 = 5; 編號 < 長度; 編號++) 字元終端.字元(輸入值[編號]);
            字元終端.字元(10);
        } else if (命令("clear")) 字元終端.擦除條目();
        else if (命令("test")) 內核.測試();
        else if (命令("halt")) {
            字元終端.寫入("HALTED\n");
            設備.停機執行狀態();
        } else 字元終端.寫入("알 數 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 接受與寫入(int 值) {
        if (值 == 10 && 發回目標側上一個行) { 發回目標側上一個行 = false; return; }
        發回目標側上一個行 = 值 == 13;
        if (值 == 10 || 值 == 13) {
            字元終端.字元(10);
            if (主記憶體檔案系統.是否編輯中) 主記憶體檔案系統.已編輯行(輸入值, 長度, 行溢出);
            else 程序值條目();
            長度 = 0;
            行溢出 = false;
            字元終端.寫入(主記憶體檔案系統.是否編輯中 ? "...> " : "jkoros> ");
        } else if (值 == 8 || 值 == 127) {
            if (長度 > 0) {
                長度--;
                字元終端.串行位元組(8); 字元終端.串行位元組(32); 字元終端.串行位元組(8);
                字元終端.屏幕字元(8);
            }
        } else if (值 >= 32 && 值 < 127 && 長度 < 輸入值.length) {
            輸入值[長度++] = 值;
            字元終端.字元(值);
        } else if (值 >= 32 && 值 < 127) 行溢出 = true;
    }

    static void 運行() {
        顯示幫助();
        字元終端.寫入("READY\njkoros> ");
        while (true) {
            int 值 = 字元終端.讀取串行();
            if (值 < 0) 值 = 鍵盤.讀取();
            if (值 >= 0) 接受與寫入(值);
            else { 通信網絡.驗證(); 設備.掛起短暫地(); }
        }
    }
}
