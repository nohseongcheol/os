// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 測試邊界列 {
    static int 失敗值() { throw new IllegalStateException("任務 중 異常"); }
    public static void main(String[] a) throws Exception {
        Object 明文陣列 = new Object[2]; System.out.println(明文陣列 instanceof String[]);
        try { String[] 無效結果 = (String[])明文陣列; } catch (ClassCastException e) { System.out.println("陣列值 轉換值 檢查項"); }
        Object[] 文本列表 = new String[2];
        try { 文本列表[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("陣列值 類型值 檢查項"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, 文本列表, 0, 2); } catch (ArrayStoreException e) { System.out.println("複製值 類型值 檢查項"); }
        System.out.println((String)文本列表[0]);
        try { "文本".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("字元 裁剪"); }
        Integer 一值 = Integer.valueOf(127), 二值 = Integer.valueOf(127); System.out.println(一值 == 二值);
        Object 鎖值 = new Object(); try { synchronized (鎖值) { 失敗值(); } } catch (IllegalStateException e) { System.out.println("鎖值 異常"); }
        synchronized (鎖值) { System.out.println("鎖值 회수"); }
        byte[] 資料 = {0, (byte)128, (byte)255, 10};
        FileOutputStream 輸出 = new FileOutputStream("位元組值.bin"); 輸出.write(資料); 輸出.flush(); 輸出.close();
        FileInputStream 輸入值 = new FileInputStream("位元組值.bin"); byte[] 讀取結果 = new byte[8];
        System.out.println(輸入值.read(讀取結果, 2, 4)); System.out.println(讀取結果[3] + ":" + 讀取結果[4]);
        System.out.println(輸入值.read(讀取結果)); System.out.println(輸入值.read(讀取結果, 0, 0)); 輸入值.close();
        try { 輸入值.read(); } catch (IOException e) { System.out.println("닫힌 檔案"); }
    }
}
