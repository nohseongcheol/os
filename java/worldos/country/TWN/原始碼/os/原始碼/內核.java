// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 實際啟動後呼叫的 Java 進入點，不依賴 JVM 或主機作業系統。 */
public final class 內核 {
    static int 總計值(int 結尾) {
        int 總和值 = 0;
        for (int 編號 = 1; 編號 <= 結尾; 編號++) 總和值 += 編號;
        return 總和值;
    }

    static boolean 測試() {
        int[] 值列 = new int[4];
        值列[2] = 總計值(10);
        int 負數值 = -7;
        int 最小值 = 0x80000000;
        int 除法結果 = -1;
        int 編號 = 記憶體空間.分配存儲裝置();
        boolean 通過值 = 值列[0] == 0 && 值列[2] == 55 && 值列.length == 4
            && 負數值 / 3 == -2 && 負數值 % 3 == -1 && 最小值 / 除法結果 == 最小值
            && 最小值 % 除法結果 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && 編號 >= 0 && 記憶體空間.發回結果(編號) && !記憶體空間.發回結果(編號);
        字元終端.寫入(通過值 ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return 通過值;
    }

    public static void 運行() {
        字元終端.準備();
        字元終端.寫入("JKOROS NATIVE JAVA\n");
        字元終端.寫入("Java 기계어 內核值 運行\n");
        if (設備.啓動標記() != 0x2badb002) {
            字元終端.寫入("BAD MULTIBOOT MAGIC\n");
            設備.停機執行狀態();
        }
        if (!測試()) 設備.停機執行狀態();
        if (記憶體空間.上位側記憶體大小() < 15360) {
            字元終端.寫入("At least 16 MiB RAM required\n");
            設備.停機執行狀態();
        }
        設備.準備用戶程式();
        字元終端.寫入("USER ELF: ring 3 / paging / int 0x80\n");
        網絡設備驅動.準備();
        通信網絡.清潔程序();
        主記憶體檔案系統.準備();
        檔案持久化.準備();
        命令解釋器.運行();
    }
}
