// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class 경계시험 {
    static int ವೈಫಲ್ಯ_ಮೌಲ್ಯ() { throw new IllegalStateException("작업 중 ವಿನಾಯಿತಿ"); }
    public static void main(String[] a) throws Exception {
        Object 그냥배열 = new Object[2]; System.out.println(그냥배열 instanceof String[]);
        try { String[] ಅಮಾನ್ಯ_ಮಾಪನ = (String[])그냥배열; } catch (ClassCastException e) { System.out.println("ಅರೇ_ಮೌಲ್ಯ 변환 검사"); }
        Object[] ಪಠ್ಯ_ಪಟ್ಟಿ = new String[2];
        try { ಪಠ್ಯ_ಪಟ್ಟಿ[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("ಅರೇ_ಮೌಲ್ಯ ಪ್ರಕಾರ_ಮೌಲ್ಯ 검사"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, ಪಠ್ಯ_ಪಟ್ಟಿ, 0, 2); } catch (ArrayStoreException e) { System.out.println("ನಕಲಿಸು_ಮೌಲ್ಯ ಪ್ರಕಾರ_ಮೌಲ್ಯ 검사"); }
        System.out.println((String)ಪಠ್ಯ_ಪಟ್ಟಿ[0]);
        try { "ಪಠ್ಯ".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("문자 ಕ್ಲಿಪ್"); }
        Integer 하나 = Integer.valueOf(127), 둘 = Integer.valueOf(127); System.out.println(하나 == 둘);
        Object 잠금 = new Object(); try { synchronized (잠금) { ವೈಫಲ್ಯ_ಮೌಲ್ಯ(); } } catch (IllegalStateException e) { System.out.println("잠금 ವಿನಾಯಿತಿ"); }
        synchronized (잠금) { System.out.println("잠금 회수"); }
        byte[] ಡೇಟಾ = {0, (byte)128, (byte)255, 10};
        FileOutputStream ಔಟ್_ಪುಟ್ = new FileOutputStream("ಬೈಟ್_ಮೌಲ್ಯ.bin"); ಔಟ್_ಪುಟ್.write(ಡೇಟಾ); ಔಟ್_ಪುಟ್.flush(); ಔಟ್_ಪುಟ್.close();
        FileInputStream 입력 = new FileInputStream("ಬೈಟ್_ಮೌಲ್ಯ.bin"); byte[] 읽음 = new byte[8];
        System.out.println(입력.read(읽음, 2, 4)); System.out.println(읽음[3] + ":" + 읽음[4]);
        System.out.println(입력.read(읽음)); System.out.println(입력.read(읽음, 0, 0)); 입력.close();
        try { 입력.read(); } catch (IOException e) { System.out.println("닫힌 ಕಡತ"); }
    }
}
