// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 中文.內建.連接通道;
import 中文.內建.運行參數;
import 中文.內建.數據報信道;
import 中文.內建.字元;
import 中文.內建.輸出;
import 中文.內建.檢查項;
import 中文.內建.輸入流;
import 中文.內建.輸入輸出異常;

public class 網路例 {
    public static void 運行() throws 輸入輸出異常 {
        // 主機: python3 工具集/示例回顯.py --tcp-port 9000 --udp-port 9001
        連接通道 連接 = 連接通道.打開("10.0.2.2", 字元.解析整數(運行參數.文本(0)));
        try {
            連接.超時(700);
            byte[] 消息 = 字元.編碼("JAVA TCP zh_Hant\n");
            連接.輸出().寫入(消息);
            輸入流 輸入值 = 連接.輸入值();
            for (int 數 = 0; 數 < 字元.位元組個數(消息); 數++) {
                檢查項.確認真值(輸入值.讀取() == (消息[數] & 255), "TCP 回覆 불일치");
            }
        } finally { 連接.關閉(); }
        數據報信道 端點 = 數據報信道.打開(0);
        try {
            端點.超時(700);
            端點.發送("10.0.2.2", 字元.解析整數(運行參數.文本(1)), "JAVA UDP zh_Hant");
            檢查項.確認真值(字元.相等文本(端點.接收(), "JAVA UDP zh_Hant"), "UDP 回覆 불일치");
        } finally { 端點.關閉(); }
        輸出.寫入行("JAVA 네트워크 驗證: TCP UDP zh_Hant");
    }
}
