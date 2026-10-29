// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int বিফলতা_মান() { throw new IllegalStateException("작업 중 ব্যতিক্রম"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] অবৈধ_পরিমাপ = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("অ্যারে_মান 변환 검사"); }
        Object[] পাঠ_তালিকা = new String[2];
        try { পাঠ_তালিকা[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("অ্যারে_মান টাইপ_করুন_মান 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, পাঠ_তালিকা, 0, 2); } catch (ArrayStoreException e) { System.out.println("নজির_মান টাইপ_করুন_মান 검사"); }
        System.out.println((String)পাঠ_তালিকা[0]);
        try { "পাঠ".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 ক্লিপ"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object 잠금 = new Object(); try { synchronized (잠금) { বিফলতা_মান(); } } catch (IllegalStateException e) { System.out.println("잠금 ব্যতিক্রম"); }
        synchronized (잠금) { System.out.println("잠금 회수"); }
        byte[] ডাটা = {0, (byte)128, (byte)255, 10};
        FileOutputStream নির্গম = new FileOutputStream("বাইট_মান.bin"); নির্গম.write(ডাটা); নির্গম.flush(); নির্গম.close();
        FileInputStream 입력 = new FileInputStream("বাইট_মান.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 নথির_নাম"); }
    }
}
