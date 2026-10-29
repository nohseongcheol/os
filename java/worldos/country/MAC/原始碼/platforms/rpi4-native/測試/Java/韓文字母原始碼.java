// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 韓文字母原始碼 {
    public static void main(String[] 實參) throws 中文.內建.輸入輸出異常 {
        中文.內建.輸出.寫入行("內建 컴파일러와 中文 庫");
        int 字元個數 = 中文.內建.字元.程式碼分個數("한글😀");
        中文.內建.輸出.寫入編號(字元個數);
        中文.內建.檔案.寫入("한글자료.txt", "內建 內核值 안에서 저장한 한글😀");
        中文.內建.輸出.寫入行(中文.內建.檔案.讀取("한글자료.txt"));
    }
}
