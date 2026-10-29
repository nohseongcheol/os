// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int αποτυχία_τιμή() { throw new IllegalStateException("작업 중 εξαίρεση"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] άκυρος_μέτρηση = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("πίνακας_τιμή μετατρέπω_τιμή 검사"); }
        Object[] μήνυμα_Λίστα = new String[2];
        try { μήνυμα_Λίστα[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("πίνακας_τιμή Τύπος_τιμή 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, μήνυμα_Λίστα, 0, 2); } catch (ArrayStoreException e) { System.out.println("παρουσία_τιμή Τύπος_τιμή 검사"); }
        System.out.println((String)μήνυμα_Λίστα[0]);
        try { "Κείμενο".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 απόσπασμα"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object κλείδωμα_τιμή = new Object(); try { synchronized (κλείδωμα_τιμή) { αποτυχία_τιμή(); } } catch (IllegalStateException e) { System.out.println("κλείδωμα_τιμή εξαίρεση"); }
        synchronized (κλείδωμα_τιμή) { System.out.println("κλείδωμα_τιμή 회수"); }
        byte[] δεδομένα = {0, (byte)128, (byte)255, 10};
        FileOutputStream Έξοδος = new FileOutputStream("바이트.bin"); Έξοδος.write(δεδομένα); Έξοδος.flush(); Έξοδος.close();
        FileInputStream είσοδος_τιμή = new FileInputStream("바이트.bin"); byte[] 읽음 = new byte[8];
        System.out.println(είσοδος_τιμή.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(είσοδος_τιμή.read(읽음)); System.out.println(είσοδος_τιμή.read(읽음, 0, 0)); είσοδος_τιμή.close();
        try { είσοδος_τιμή.read(); } catch (IOException e) { System.out.println("닫힌 Αρχείο"); }
    }
}
