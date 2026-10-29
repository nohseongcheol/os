// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int hiba_ÉRTÉK() { throw new IllegalStateException("작업 중 kivétel"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] alaptalan_KR = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("TÖMB_ÉRTÉK konvertál_ÉRTÉK 검사"); }
        Object[] SMS_Lista = new String[2];
        try { SMS_Lista[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("TÖMB_ÉRTÉK beír_ÉRTÉK 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Lista, 0, 2); } catch (ArrayStoreException e) { System.out.println("másol_ÉRTÉK beír_ÉRTÉK 검사"); }
        System.out.println((String)SMS_Lista[0]);
        try { "Szöveg".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 klip"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object lezár_ÉRTÉK = new Object(); try { synchronized (lezár_ÉRTÉK) { hiba_ÉRTÉK(); } } catch (IllegalStateException e) { System.out.println("lezár_ÉRTÉK kivétel"); }
        synchronized (lezár_ÉRTÉK) { System.out.println("lezár_ÉRTÉK 회수"); }
        byte[] adat = {0, (byte)128, (byte)255, 10};
        FileOutputStream Kimenet = new FileOutputStream("bájt_ÉRTÉK.bin"); Kimenet.write(adat); Kimenet.flush(); Kimenet.close();
        FileInputStream bevitel_ÉRTÉK = new FileInputStream("bájt_ÉRTÉK.bin"); byte[] 읽음 = new byte[8];
        System.out.println(bevitel_ÉRTÉK.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(bevitel_ÉRTÉK.read(읽음)); System.out.println(bevitel_ÉRTÉK.read(읽음, 0, 0)); bevitel_ÉRTÉK.close();
        try { bevitel_ÉRTÉK.read(); } catch (IOException e) { System.out.println("닫힌 Fájl"); }
    }
}
