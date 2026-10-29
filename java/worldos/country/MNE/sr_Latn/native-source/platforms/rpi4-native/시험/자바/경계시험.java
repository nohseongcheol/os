// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int otkazivanje_VALUE() { throw new IllegalStateException("작업 중 izuzetak"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] nevažeći_KR = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("niz_VALUE CONVERT_VALUE 검사"); }
        Object[] SMS_Lista = new String[2];
        try { SMS_Lista[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("niz_VALUE tip_VALUE 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Lista, 0, 2); } catch (ArrayStoreException e) { System.out.println("instanca_VALUE tip_VALUE 검사"); }
        System.out.println((String)SMS_Lista[0]);
        try { "글".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 klip"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object zaključati_VALUE = new Object(); try { synchronized (zaključati_VALUE) { otkazivanje_VALUE(); } } catch (IllegalStateException e) { System.out.println("zaključati_VALUE izuzetak"); }
        synchronized (zaključati_VALUE) { System.out.println("zaključati_VALUE 회수"); }
        byte[] podaci = {0, (byte)128, (byte)255, 10};
        FileOutputStream 출력 = new FileOutputStream("bajt_VALUE.bin"); 출력.write(podaci); 출력.flush(); 출력.close();
        FileInputStream 입력 = new FileInputStream("bajt_VALUE.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 Datoteka"); }
    }
}
