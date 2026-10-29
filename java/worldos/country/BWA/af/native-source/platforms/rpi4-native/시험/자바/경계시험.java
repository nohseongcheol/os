// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int faling_VALUE() { throw new IllegalStateException("작업 중 uitsondering"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] ongeldig_maatreël = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("ARRAY_VALUE CONVERT_VALUE 검사"); }
        Object[] SMS_Lys = new String[2];
        try { SMS_Lys[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("ARRAY_VALUE TYPE_VALUE 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Lys, 0, 2); } catch (ArrayStoreException e) { System.out.println("geval_VALUE TYPE_VALUE 검사"); }
        System.out.println((String)SMS_Lys[0]);
        try { "Teks".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 snit"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object 잠금 = new Object(); try { synchronized (잠금) { faling_VALUE(); } } catch (IllegalStateException e) { System.out.println("잠금 uitsondering"); }
        synchronized (잠금) { System.out.println("잠금 회수"); }
        byte[] data = {0, (byte)128, (byte)255, 10};
        FileOutputStream Afvoer = new FileOutputStream("greep_VALUE.bin"); Afvoer.write(data); Afvoer.flush(); Afvoer.close();
        FileInputStream 입력 = new FileInputStream("greep_VALUE.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 Lêer"); }
    }
}
