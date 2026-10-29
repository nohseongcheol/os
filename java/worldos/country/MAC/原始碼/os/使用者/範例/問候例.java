// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 問候例 {
    public static int 運行() {
        使用者.寫入("Hello from a separate Java ELF!\n");
        使用者.寫入(使用者.執行狀態權限() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int 編號 = 0; 編號 < 使用者.參數列個數(); 編號++) {
            使用者.寫入("arg: "); 使用者.寫入(使用者.實參(編號)); 使用者.寫入("\n");
        }
        return 使用者.執行狀態權限() == 3 ? 0 : 1;
    }
}
