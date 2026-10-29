// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int fejl_VÆRDI() { throw new IllegalStateException("작업 중 undtagelse"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] ugyldig_KR = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("MATRIX_VÆRDI KONVERTER_VÆRDI 검사"); }
        Object[] sms_Liste = new String[2];
        try { sms_Liste[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("MATRIX_VÆRDI Type_VÆRDI 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, sms_Liste, 0, 2); } catch (ArrayStoreException e) { System.out.println("kopiere_VÆRDI Type_VÆRDI 검사"); }
        System.out.println((String)sms_Liste[0]);
        try { "Tekst".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 klippe"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object lås_VÆRDI = new Object(); try { synchronized (lås_VÆRDI) { fejl_VÆRDI(); } } catch (IllegalStateException e) { System.out.println("lås_VÆRDI undtagelse"); }
        synchronized (lås_VÆRDI) { System.out.println("lås_VÆRDI 회수"); }
        byte[] data = {0, (byte)128, (byte)255, 10};
        FileOutputStream Udgang = new FileOutputStream("byte_VÆRDI.bin"); Udgang.write(data); Udgang.flush(); Udgang.close();
        FileInputStream input_VÆRDI = new FileInputStream("byte_VÆRDI.bin"); byte[] 읽음 = new byte[8];
        System.out.println(input_VÆRDI.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(input_VÆRDI.read(읽음)); System.out.println(input_VÆRDI.read(읽음, 0, 0)); input_VÆRDI.close();
        try { input_VÆRDI.read(); } catch (IOException e) { System.out.println("닫힌 Fil"); }
    }
}
