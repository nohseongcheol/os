// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int செயலிழப்பு_மதிப்பு() { throw new IllegalStateException("작업 중 விதிவிலக்கு"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] செல்லுபடியாகாத_அளவிடக்கூடியது = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("கோவை_மதிப்பு_ed437109 변환 검사"); }
        Object[] உரை_பட்டியல் = new String[2];
        try { உரை_பட்டியல்[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("கோவை_மதிப்பு_ed437109 வகை_மதிப்பு 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, உரை_பட்டியல், 0, 2); } catch (ArrayStoreException e) { System.out.println("நகலெடு_மதிப்பு வகை_மதிப்பு 검사"); }
        System.out.println((String)உரை_பட்டியல்[0]);
        try { "உரை".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 கிளிப்"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object பூட்டு_மதிப்பு = new Object(); try { synchronized (பூட்டு_மதிப்பு) { செயலிழப்பு_மதிப்பு(); } } catch (IllegalStateException e) { System.out.println("பூட்டு_மதிப்பு விதிவிலக்கு"); }
        synchronized (பூட்டு_மதிப்பு) { System.out.println("பூட்டு_மதிப்பு 회수"); }
        byte[] தரவு = {0, (byte)128, (byte)255, 10};
        FileOutputStream வெளியீட்டு_இடம் = new FileOutputStream("பைட்_மதிப்பு.bin"); வெளியீட்டு_இடம்.write(தரவு); வெளியீட்டு_இடம்.flush(); வெளியீட்டு_இடம்.close();
        FileInputStream 입력 = new FileInputStream("பைட்_மதிப்பு.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 கோப்பின்_பெயர்"); }
    }
}
