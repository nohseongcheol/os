// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 顏色 {
    public static void main(String[] 實參) throws Exception {
        int 總和值 = 0;
        int 數 = 1;
        while (數 <= 10) {
            總和值 = 總和值 + 數;
            數 = 數 + 1;
        }
        中文.內建.輸出.寫入編號(總和值);
        中文.內建.檔案.寫入("aot.txt", "한글 AOT 檔案 😀");
        中文.內建.輸出.寫入行(中文.內建.檔案.讀取("aot.txt"));
    }
}
