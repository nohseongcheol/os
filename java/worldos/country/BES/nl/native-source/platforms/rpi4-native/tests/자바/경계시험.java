// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int fout_WAARDE() { throw new IllegalStateException("작업 중 uitzondering"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] nietig_HR = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("MATRIX_WAARDE CONVERTEREN_WAARDE 검사"); }
        Object[] sms_Lijst = new String[2];
        try { sms_Lijst[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("MATRIX_WAARDE TYPE_WAARDE 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, sms_Lijst, 0, 2); } catch (ArrayStoreException e) { System.out.println("kopiëren_WAARDE TYPE_WAARDE 검사"); }
        System.out.println((String)sms_Lijst[0]);
        try { "tekst".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 clip"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object vergrendelen_WAARDE = new Object(); try { synchronized (vergrendelen_WAARDE) { fout_WAARDE(); } } catch (IllegalStateException e) { System.out.println("vergrendelen_WAARDE uitzondering"); }
        synchronized (vergrendelen_WAARDE) { System.out.println("vergrendelen_WAARDE 회수"); }
        byte[] gegevens = {0, (byte)128, (byte)255, 10};
        FileOutputStream tekstuitvoer = new FileOutputStream("byte_WAARDE.bin"); tekstuitvoer.write(gegevens); tekstuitvoer.flush(); tekstuitvoer.close();
        FileInputStream invoer_WAARDE = new FileInputStream("byte_WAARDE.bin"); byte[] 읽음 = new byte[8];
        System.out.println(invoer_WAARDE.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(invoer_WAARDE.read(읽음)); System.out.println(invoer_WAARDE.read(읽음, 0, 0)); invoer_WAARDE.close();
        try { invoer_WAARDE.read(); } catch (IOException e) { System.out.println("닫힌 bestand"); }
    }
}
