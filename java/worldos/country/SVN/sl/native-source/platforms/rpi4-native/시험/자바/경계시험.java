// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int napaka_VALUE() { throw new IllegalStateException("작업 중 izjema"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] neveljaven_KR = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("ARRAY_VALUE CONVERT_VALUE 검사"); }
        Object[] SMS_Seznam = new String[2];
        try { SMS_Seznam[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("ARRAY_VALUE Tip_VALUE 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Seznam, 0, 2); } catch (ArrayStoreException e) { System.out.println("kopirati_VALUE Tip_VALUE 검사"); }
        System.out.println((String)SMS_Seznam[0]);
        try { "Besedilo".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 izrezek"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object zaklepanje_VALUE = new Object(); try { synchronized (zaklepanje_VALUE) { napaka_VALUE(); } } catch (IllegalStateException e) { System.out.println("zaklepanje_VALUE izjema"); }
        synchronized (zaklepanje_VALUE) { System.out.println("zaklepanje_VALUE 회수"); }
        byte[] podatki = {0, (byte)128, (byte)255, 10};
        FileOutputStream Izpis = new FileOutputStream("bajt_VALUE.bin"); Izpis.write(podatki); Izpis.flush(); Izpis.close();
        FileInputStream 입력 = new FileInputStream("bajt_VALUE.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 Datoteka"); }
    }
}
