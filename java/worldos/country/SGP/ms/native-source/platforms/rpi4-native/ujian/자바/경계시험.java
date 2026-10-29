// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int kegagalan_VALUE() { throw new IllegalStateException("작업 중 pengecualian"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] tak_sah_ukuran = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("ARRAY_VALUE tukar_VALUE 검사"); }
        Object[] SMS_Senarai = new String[2];
        try { SMS_Senarai[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("ARRAY_VALUE TYPE_VALUE 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Senarai, 0, 2); } catch (ArrayStoreException e) { System.out.println("tika_VALUE TYPE_VALUE 검사"); }
        System.out.println((String)SMS_Senarai[0]);
        try { "Teks".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 klip"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object kunci_VALUE = new Object(); try { synchronized (kunci_VALUE) { kegagalan_VALUE(); } } catch (IllegalStateException e) { System.out.println("kunci_VALUE pengecualian"); }
        synchronized (kunci_VALUE) { System.out.println("kunci_VALUE 회수"); }
        byte[] data = {0, (byte)128, (byte)255, 10};
        FileOutputStream 출력 = new FileOutputStream("bait_VALUE.bin"); 출력.write(data); 출력.flush(); 출력.close();
        FileInputStream 입력 = new FileInputStream("bait_VALUE.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 Fail"); }
    }
}
