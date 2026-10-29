// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int כשל_ערך() { throw new IllegalStateException("작업 중 חריגה"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] לא_חוקי_תוצאה = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("מערך_ערך המר_ערך 검사"); }
        Object[] טקסט_רשימה = new String[2];
        try { טקסט_רשימה[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("מערך_ערך כתב_ערך 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, טקסט_רשימה, 0, 2); } catch (ArrayStoreException e) { System.out.println("מופע_ערך כתב_ערך 검사"); }
        System.out.println((String)טקסט_רשימה[0]);
        try { "טקסט".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 לגזור"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object נעל_ערך = new Object(); try { synchronized (נעל_ערך) { כשל_ערך(); } } catch (IllegalStateException e) { System.out.println("נעל_ערך חריגה"); }
        synchronized (נעל_ערך) { System.out.println("נעל_ערך 회수"); }
        byte[] נתונים = {0, (byte)128, (byte)255, 10};
        FileOutputStream פלטטקסט = new FileOutputStream("בית_ערך.bin"); פלטטקסט.write(נתונים); פלטטקסט.flush(); פלטטקסט.close();
        FileInputStream קלט_ערך = new FileInputStream("בית_ערך.bin"); byte[] 읽음 = new byte[8];
        System.out.println(קלט_ערך.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(קלט_ערך.read(읽음)); System.out.println(קלט_ערך.read(읽음, 0, 0)); קלט_ערך.close();
        try { קלט_ערך.read(); } catch (IOException e) { System.out.println("닫힌 קובץ"); }
    }
}
