// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 檔案例 {
    public static void 運行() throws 中文.內建.輸入輸出異常 {
        中文.內建.檔案.寫入("java.txt", "JAVA 檔案: zh_Hant 😀\n");
        中文.內建.輸出.寫入(中文.內建.檔案.讀取("java.txt"));
    }
}
