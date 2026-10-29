// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class अपवाद_चाचणी {
    static int भागाकारकरा_मूल्ये(int n) { return 8 / n; }
    static int अंतिमकरा_मूल्य() { try { return भागाकारकरा_मूल्ये(0); } finally { System.out.println("अंतिमकरा_मूल्य"); } }
    public static void main(String[] a) {
        try { अंतिमकरा_मूल्य(); } catch (ArithmeticException e) { System.out.println("अंकगणिती_मूल्य अपवाद"); }
        try { throw new IllegalArgumentException("잘못된 बाबी 한글😀"); } catch (RuntimeException e) { System.out.println(e.getMessage()); }
        try { String s = null; s.length(); } catch (NullPointerException e) { System.out.println("빈 संदर्भ"); }
        try { int[] n = new int[1]; System.out.println(n[2]); } catch (IndexOutOfBoundsException e) { System.out.println("ऍरे_मूल्य क्लिप"); }
        try { Integer.parseInt("2147483648"); } catch (NumberFormatException e) { System.out.println("पूर्णांक क्लिप"); }
        try { Object x = "पाठ्य"; Integer n = (Integer)x; } catch (ClassCastException e) { System.out.println("टाइप_करा_मूल्य रूपांतरकरा_मूल्य"); }
        try { java.io.FileInputStream f = new java.io.FileInputStream("없는파일"); } catch (java.io.IOException e) { System.out.println("फाइल अपवाद"); }
        System.out.println("अपवाद प्रक्रिया_मूल्य_प्रविष्टी आहे_पूर्ण");
    }
}
