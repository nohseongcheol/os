// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int hutsegite_balio() { throw new IllegalStateException("작업 중 salbuespen"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] baliogabe_neurria = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("matrize_balio BIHURTU_balio 검사"); }
        Object[] SMS_Zerrenda = new String[2];
        try { SMS_Zerrenda[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("matrize_balio MOTA_balio 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Zerrenda, 0, 2); } catch (ArrayStoreException e) { System.out.println("kopiatu_balio MOTA_balio 검사"); }
        System.out.println((String)SMS_Zerrenda[0]);
        try { "Testua".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 klip"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object 잠금 = new Object(); try { synchronized (잠금) { hutsegite_balio(); } } catch (IllegalStateException e) { System.out.println("잠금 salbuespen"); }
        synchronized (잠금) { System.out.println("잠금 회수"); }
        byte[] datuak = {0, (byte)128, (byte)255, 10};
        FileOutputStream Irteera = new FileOutputStream("byte_balio.bin"); Irteera.write(datuak); Irteera.flush(); Irteera.close();
        FileInputStream 입력 = new FileInputStream("byte_balio.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 Fitxategia"); }
    }
}
