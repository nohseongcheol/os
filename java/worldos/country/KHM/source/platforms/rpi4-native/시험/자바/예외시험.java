// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 예외시험 {
    static int 나누기(int n) { return 8 / n; }
    static int 마무리() { try { return 나누기(0); } finally { System.out.println("마무리"); } }
    public static void main(String[] a) {
        try { 마무리(); } catch (ArithmeticException e) { System.out.println("산술 ការលើកលែង"); }
        try { throw new IllegalArgumentException("잘못된 អាគុយម៉ង់ 한글😀"); } catch (RuntimeException e) { System.out.println(e.getMessage()); }
        try { String s = null; s.length(); } catch (NullPointerException e) { System.out.println("빈 យោង"); }
        try { int[] n = new int[1]; System.out.println(n[2]); } catch (IndexOutOfBoundsException e) { System.out.println("អារេ_តំលៃ មេឌៀខ្លីៗ"); }
        try { Integer.parseInt("2147483648"); } catch (NumberFormatException e) { System.out.println("ចំនួនគត់ មេឌៀខ្លីៗ"); }
        try { Object x = "អត្ថបទ"; Integer n = (Integer)x; } catch (ClassCastException e) { System.out.println("វាយបញ្ចូល_តំលៃ 변환"); }
        try { java.io.FileInputStream f = new java.io.FileInputStream("없는파일"); } catch (java.io.IOException e) { System.out.println("ឯកសារ ការលើកលែង"); }
        System.out.println("ការលើកលែង ដំណើរការ_តំលៃ_ការបញ្ចូល 완료");
    }
}
