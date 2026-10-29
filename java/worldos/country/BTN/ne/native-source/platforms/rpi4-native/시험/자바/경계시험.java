// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int विफल_मान() { throw new IllegalStateException("작업 중 예외"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] अवैधानिक_मापन = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("विन्यास_मान 변환 검사"); }
        Object[] पाठ_सूची = new String[2];
        try { पाठ_सूची[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("विन्यास_मान प्रकार_मान 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, पाठ_सूची, 0, 2); } catch (ArrayStoreException e) { System.out.println("उद्धरण_मान_37b3d3b1 प्रकार_मान 검사"); }
        System.out.println((String)पाठ_सूची[0]);
        try { "पाठ".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 क्लिप"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object 잠금 = new Object(); try { synchronized (잠금) { विफल_मान(); } } catch (IllegalStateException e) { System.out.println("잠금 예외"); }
        synchronized (잠금) { System.out.println("잠금 회수"); }
        byte[] लगत = {0, (byte)128, (byte)255, 10};
        FileOutputStream 출력 = new FileOutputStream("बाइट_मान.bin"); 출력.write(लगत); 출력.flush(); 출력.close();
        FileInputStream 입력 = new FileInputStream("बाइट_मान.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 फाइल"); }
    }
}
