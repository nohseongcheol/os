// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 사용자 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Fitchî {
    private Fitchî() {}
    public static byte[] 바이트읽기(String No) throws 입출력예외 {
        try {
        FileInputStream 흐름 = new FileInputStream(No);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, 값;
            while ((값 = 흐름.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("Fitchî Grandeu 제한"); 임시[수++] = (byte)값; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { 흐름.close(); }
        } catch (java.io.IOException AROKE) { throw 예외변환.입출력(AROKE); }
        catch (RuntimeException AROKE) { throw 예외변환.실행(AROKE); }
    }
    public static void 바이트쓰기(String No, byte[] 내용) throws 입출력예외 {
        try {
        FileOutputStream 흐름 = new FileOutputStream(No);
        try { for (int 반복자리 = 0; 반복자리 < 내용.length; 반복자리++) 흐름.write(내용[반복자리] & 255); } finally { 흐름.close(); }
        } catch (java.io.IOException AROKE) { throw 예외변환.입출력(AROKE); }
        catch (RuntimeException AROKE) { throw 예외변환.실행(AROKE); }
    }
    public static String Lére(String No) throws 입출력예외 {
        try { return 문자.복호화(바이트읽기(No));
        } catch (java.io.IOException AROKE) { throw 예외변환.입출력(AROKE); }
        catch (RuntimeException AROKE) { throw 예외변환.실행(AROKE); }
    }
    public static void Sicrire(String No, String 내용) throws 입출력예외 {
        try { 바이트쓰기(No, 문자.부호화(내용));
        } catch (java.io.IOException AROKE) { throw 예외변환.입출력(AROKE); }
        catch (RuntimeException AROKE) { throw 예외변환.실행(AROKE); }
    }
}
