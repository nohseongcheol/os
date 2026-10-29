// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int selhání_HODNOTA() { throw new IllegalStateException("작업 중 výjimka"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] neplatný_KV = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("pole_HODNOTA CONVERT_HODNOTA 검사"); }
        Object[] SMS_Seznam = new String[2];
        try { SMS_Seznam[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("pole_HODNOTA TYP_HODNOTA 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, SMS_Seznam, 0, 2); } catch (ArrayStoreException e) { System.out.println("instance_HODNOTA TYP_HODNOTA 검사"); }
        System.out.println((String)SMS_Seznam[0]);
        try { "text".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 oříznout"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object zámek_HODNOTA = new Object(); try { synchronized (zámek_HODNOTA) { selhání_HODNOTA(); } } catch (IllegalStateException e) { System.out.println("zámek_HODNOTA výjimka"); }
        synchronized (zámek_HODNOTA) { System.out.println("zámek_HODNOTA 회수"); }
        byte[] data = {0, (byte)128, (byte)255, 10};
        FileOutputStream výstupní_pozice = new FileOutputStream("bajt_HODNOTA.bin"); výstupní_pozice.write(data); výstupní_pozice.flush(); výstupní_pozice.close();
        FileInputStream vstup_HODNOTA = new FileInputStream("bajt_HODNOTA.bin"); byte[] 읽음 = new byte[8];
        System.out.println(vstup_HODNOTA.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(vstup_HODNOTA.read(읽음)); System.out.println(vstup_HODNOTA.read(읽음, 0, 0)); vstup_HODNOTA.close();
        try { vstup_HODNOTA.read(); } catch (IOException e) { System.out.println("닫힌 název_souboru"); }
    }
}
