// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int ความล้มเหลว_ค่า() { throw new IllegalStateException("작업 중 ข้อยกเว้น"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] ไม่ถูกต้อง_เมตริก = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("อาร์เรย์_ค่า แปลง_ค่า_4633b7f3 검사"); }
        Object[] ข้อความ_รายการ = new String[2];
        try { ข้อความ_รายการ[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("อาร์เรย์_ค่า ชนิด_ค่า 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, ข้อความ_รายการ, 0, 2); } catch (ArrayStoreException e) { System.out.println("คัดลอก_ค่า ชนิด_ค่า 검사"); }
        System.out.println((String)ข้อความ_รายการ[0]);
        try { "ข้อความ".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 คลิป"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object ล็อก_ค่า = new Object(); try { synchronized (ล็อก_ค่า) { ความล้มเหลว_ค่า(); } } catch (IllegalStateException e) { System.out.println("ล็อก_ค่า ข้อยกเว้น"); }
        synchronized (ล็อก_ค่า) { System.out.println("ล็อก_ค่า 회수"); }
        byte[] ข้อมูล = {0, (byte)128, (byte)255, 10};
        FileOutputStream ข้อความออก = new FileOutputStream("ไบต์_ค่า.bin"); ข้อความออก.write(ข้อมูล); ข้อความออก.flush(); ข้อความออก.close();
        FileInputStream 입력 = new FileInputStream("ไบต์_ค่า.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 แฟ้ม"); }
    }
}
