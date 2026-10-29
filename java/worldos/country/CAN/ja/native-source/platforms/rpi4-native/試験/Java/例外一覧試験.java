// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 例外一覧試験 {
    static int 除算処理値一覧(int n) { return 8 / n; }
    static int 最終化値() { try { return 除算処理値一覧(0); } finally { System.out.println("最終化値"); } }
    public static void main(String[] a) {
        try { 最終化値(); } catch (ArithmeticException e) { System.out.println("算術値 例外"); }
        try { throw new IllegalArgumentException("잘못된 引数 한글😀"); } catch (RuntimeException e) { System.out.println(e.getMessage()); }
        try { String s = null; s.length(); } catch (NullPointerException e) { System.out.println("빈 参照"); }
        try { int[] n = new int[1]; System.out.println(n[2]); } catch (IndexOutOfBoundsException e) { System.out.println("配列値 切抜き"); }
        try { Integer.parseInt("2147483648"); } catch (NumberFormatException e) { System.out.println("整数値 切抜き"); }
        try { Object x = "文"; Integer n = (Integer)x; } catch (ClassCastException e) { System.out.println("型値 値変換"); }
        try { java.io.FileInputStream f = new java.io.FileInputStream("없는파일"); } catch (java.io.IOException e) { System.out.println("ファイル 例外"); }
        System.out.println("例外 プロセス値入口 判定完了");
    }
}
