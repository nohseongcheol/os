// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int ناکامی_قدر() { throw new IllegalStateException("작업 중 استثنا"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] بے_جواز_پیمائش = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("لڑی_قدر 변환 검사"); }
        Object[] متن_فہرست = new String[2];
        try { متن_فہرست[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("لڑی_قدر ٹائپ_کریں_قدر 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, متن_فہرست, 0, 2); } catch (ArrayStoreException e) { System.out.println("نقل_قدر ٹائپ_کریں_قدر 검사"); }
        System.out.println((String)متن_فہرست[0]);
        try { "متن".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 تراشہ"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object 잠금 = new Object(); try { synchronized (잠금) { ناکامی_قدر(); } } catch (IllegalStateException e) { System.out.println("잠금 استثنا"); }
        synchronized (잠금) { System.out.println("잠금 회수"); }
        byte[] کوائف = {0, (byte)128, (byte)255, 10};
        FileOutputStream اخراج_کا_مقام = new FileOutputStream("بائٹ_قدر.bin"); اخراج_کا_مقام.write(کوائف); اخراج_کا_مقام.flush(); اخراج_کا_مقام.close();
        FileInputStream 입력 = new FileInputStream("بائٹ_قدر.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 فائل_کا_نام"); }
    }
}
