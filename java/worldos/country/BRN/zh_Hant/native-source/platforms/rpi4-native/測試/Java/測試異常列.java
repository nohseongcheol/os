// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 測試異常列 {
    static int 相割值列(int n) { return 8 / n; }
    static int 最終處理值() { try { return 相割值列(0); } finally { System.out.println("最終處理值"); } }
    public static void main(String[] a) {
        try { 最終處理值(); } catch (ArithmeticException e) { System.out.println("算術值 異常"); }
        try { throw new IllegalArgumentException("잘못된 實參 한글😀"); } catch (RuntimeException e) { System.out.println(e.getMessage()); }
        try { String s = null; s.length(); } catch (NullPointerException e) { System.out.println("빈 引用"); }
        try { int[] n = new int[1]; System.out.println(n[2]); } catch (IndexOutOfBoundsException e) { System.out.println("陣列值 裁剪"); }
        try { Integer.parseInt("2147483648"); } catch (NumberFormatException e) { System.out.println("整數 裁剪"); }
        try { Object x = "文本"; Integer n = (Integer)x; } catch (ClassCastException e) { System.out.println("類型值 轉換值"); }
        try { java.io.FileInputStream f = new java.io.FileInputStream("없는파일"); } catch (java.io.IOException e) { System.out.println("檔案 異常"); }
        System.out.println("異常 程序值條目 是否完成");
    }
}
