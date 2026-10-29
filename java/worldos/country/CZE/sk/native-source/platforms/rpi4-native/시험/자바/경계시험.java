// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int zlyhanie_VALUE() { throw new IllegalStateException("작업 중 výnimka"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] neplatné_KR = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("pole_VALUE CONVERT_VALUE 검사"); }
        Object[] SMS_Zoznam = new String[2];
        try { SMS_Zoznam[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("pole_VALUE Typ_VALUE 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Zoznam, 0, 2); } catch (ArrayStoreException e) { System.out.println("inštancia_VALUE Typ_VALUE 검사"); }
        System.out.println((String)SMS_Zoznam[0]);
        try { "Spracovanie_textu".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 klip"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object zámok_VALUE = new Object(); try { synchronized (zámok_VALUE) { zlyhanie_VALUE(); } } catch (IllegalStateException e) { System.out.println("zámok_VALUE výnimka"); }
        synchronized (zámok_VALUE) { System.out.println("zámok_VALUE 회수"); }
        byte[] údaje = {0, (byte)128, (byte)255, 10};
        FileOutputStream Výstup = new FileOutputStream("Byte_VALUE.bin"); Výstup.write(údaje); Výstup.flush(); Výstup.close();
        FileInputStream vstup_VALUE = new FileInputStream("Byte_VALUE.bin"); byte[] 읽음 = new byte[8];
        System.out.println(vstup_VALUE.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(vstup_VALUE.read(읽음)); System.out.println(vstup_VALUE.read(읽음, 0, 0)); vstup_VALUE.close();
        try { vstup_VALUE.read(); } catch (IOException e) { System.out.println("닫힌 Súbor"); }
    }
}
