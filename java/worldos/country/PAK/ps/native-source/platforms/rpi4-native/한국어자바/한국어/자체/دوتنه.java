// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 کارن 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class دوتنه {
    private دوتنه() {}
    public static byte[] 바이트읽기(String نوم) throws 입출력예외 {
        try {
        FileInputStream بهنګ_ارزښت = new FileInputStream(نوم);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, ارزښت;
            while ((ارزښت = بهنګ_ارزښت.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("دوتنه کچ 제한"); 임시[수++] = (byte)ارزښت; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { بهنګ_ارزښت.close(); }
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public static void ليکل_بايټ_ارزښت(String نوم, byte[] منځپانګه_ارزښت) throws 입출력예외 {
        try {
        FileOutputStream بهنګ_ارزښت = new FileOutputStream(نوم);
        try { for (int کړۍ_لړیال = 0; کړۍ_لړیال < منځپانګه_ارزښت.length; کړۍ_لړیال++) بهنګ_ارزښت.write(منځپانګه_ارزښت[کړۍ_لړیال] & 255); } finally { بهنګ_ارزښت.close(); }
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public static String لوستل(String نوم) throws 입출력예외 {
        try { return 문자.کوډ_پرانېستل_اومتوک(바이트읽기(نوم));
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public static void لوستل_2(String نوم, String منځپانګه_ارزښت) throws 입출력예외 {
        try { ليکل_بايټ_ارزښت(نوم, 문자.부호화(منځپانګه_ارزښت));
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
}
