// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class thửCácNgoạiLệ {
    static int cácGiáTrịChia(int n) { return 8 / n; }
    static int giáTrịHoànThiện() { try { return cácGiáTrịChia(0); } finally { System.out.println("giáTrịHoànThiện"); } }
    public static void main(String[] a) {
        try { giáTrịHoànThiện(); } catch (ArithmeticException e) { System.out.println("giáTrịSốHọc ngoạiLệ"); }
        try { throw new IllegalArgumentException("잘못된 cácĐốiSố 한글😀"); } catch (RuntimeException e) { System.out.println(e.getMessage()); }
        try { String s = null; s.length(); } catch (NullPointerException e) { System.out.println("빈 thamChiếu"); }
        try { int[] n = new int[1]; System.out.println(n[2]); } catch (IndexOutOfBoundsException e) { System.out.println("giáTrịMảng cắtXén"); }
        try { Integer.parseInt("2147483648"); } catch (NumberFormatException e) { System.out.println("SốNguyên cắtXén"); }
        try { Object x = "vănBản"; Integer n = (Integer)x; } catch (ClassCastException e) { System.out.println("giáTrịKiểu chuyểnĐổiGiáTrị"); }
        try { java.io.FileInputStream f = new java.io.FileInputStream("없는파일"); } catch (java.io.IOException e) { System.out.println("Tệp ngoạiLệ"); }
        System.out.println("ngoạiLệ mụcGiáTrịTiếnTrình làĐầyĐủ");
    }
}
