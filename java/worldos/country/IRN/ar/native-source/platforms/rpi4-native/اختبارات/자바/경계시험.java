// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int فشل_قيمة() { throw new IllegalStateException("작업 중 استثناء"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] غير_صالح_مقياس = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("صفيف_قيمة تحويل_قيمة 검사"); }
        Object[] نص_قائمة = new String[2];
        try { نص_قائمة[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("صفيف_قيمة نوع_قيمة 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, نص_قائمة, 0, 2); } catch (ArrayStoreException e) { System.out.println("مثيل_قيمة نوع_قيمة 검사"); }
        System.out.println((String)نص_قائمة[0]);
        try { "نص".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 يقص"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object قفل_قيمة = new Object(); try { synchronized (قفل_قيمة) { فشل_قيمة(); } } catch (IllegalStateException e) { System.out.println("قفل_قيمة استثناء"); }
        synchronized (قفل_قيمة) { System.out.println("قفل_قيمة 회수"); }
        byte[] بيانات = {0, (byte)128, (byte)255, 10};
        FileOutputStream مخرجات = new FileOutputStream("بايت_قيمة.bin"); مخرجات.write(بيانات); مخرجات.flush(); مخرجات.close();
        FileInputStream إدخال_قيمة = new FileInputStream("بايت_قيمة.bin"); byte[] يقرأ_مقياس = new byte[8];
        System.out.println(إدخال_قيمة.read(يقرأ_مقياس, 2, 4)); System.out.println(يقرأ_مقياس[3] + ":" + يقرأ_مقياس[4]);
        System.out.println(إدخال_قيمة.read(يقرأ_مقياس)); System.out.println(إدخال_قيمة.read(يقرأ_مقياس, 0, 0)); إدخال_قيمة.close();
        try { إدخال_قيمة.read(); } catch (IOException e) { System.out.println("닫힌 ملف"); }
    }
}
