// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int feil_VERDI() { throw new IllegalStateException("작업 중 unntak"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] ugyldig_KR = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("MATRISE_VERDI KONVERTER_VERDI 검사"); }
        Object[] SMS_Liste = new String[2];
        try { SMS_Liste[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("MATRISE_VERDI Type_VERDI 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Liste, 0, 2); } catch (ArrayStoreException e) { System.out.println("kopiere_VERDI Type_VERDI 검사"); }
        System.out.println((String)SMS_Liste[0]);
        try { "Tekst".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 klippe"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object blokkere_VERDI = new Object(); try { synchronized (blokkere_VERDI) { feil_VERDI(); } } catch (IllegalStateException e) { System.out.println("blokkere_VERDI unntak"); }
        synchronized (blokkere_VERDI) { System.out.println("blokkere_VERDI 회수"); }
        byte[] data = {0, (byte)128, (byte)255, 10};
        FileOutputStream Utgang = new FileOutputStream("byte_VERDI.bin"); Utgang.write(data); Utgang.flush(); Utgang.close();
        FileInputStream inndata_VERDI = new FileInputStream("byte_VERDI.bin"); byte[] 읽음 = new byte[8];
        System.out.println(inndata_VERDI.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(inndata_VERDI.read(읽음)); System.out.println(inndata_VERDI.read(읽음, 0, 0)); inndata_VERDI.close();
        try { inndata_VERDI.read(); } catch (IOException e) { System.out.println("닫힌 Fil"); }
    }
}
