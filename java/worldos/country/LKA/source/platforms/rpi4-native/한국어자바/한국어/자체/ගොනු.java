// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 පරිශීලක 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ගොනු {
    private ගොනු() {}
    public static byte[] 바이트읽기(String නම) throws 입출력예외 {
        try {
        FileInputStream දහර_අගය = new FileInputStream(නම);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, අගය;
            while ((අගය = දහර_අගය.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("ගොනු ප්_රමාණය 제한"); 임시[수++] = (byte)අගය; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { දහර_අගය.close(); }
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public static void ලියන්න_බයිටය_අගය(String නම, byte[] අන්තර්ගතය_අගය) throws 입출력예외 {
        try {
        FileOutputStream දහර_අගය = new FileOutputStream(නම);
        try { for (int ලූපය_සූචිය = 0; ලූපය_සූචිය < අන්තර්ගතය_අගය.length; ලූපය_සූචිය++) දහර_අගය.write(අන්තර්ගතය_අගය[ලූපය_සූචිය] & 255); } finally { දහර_අගය.close(); }
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public static String කියවීම(String නම) throws 입출력예외 {
        try { return 문자.විගුප්ත_කේතනය_කරන්න_දත්ත(바이트읽기(නම));
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public static void ලිවීම(String නම, String අන්තර්ගතය_අගය) throws 입출력예외 {
        try { ලියන්න_බයිටය_අගය(නම, 문자.부호화(අන්තර්ගතය_අගය));
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
}
