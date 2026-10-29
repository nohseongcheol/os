// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ਉਪਭੋਗਤਾ 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ਫਾਇਲ {
    private ਫਾਇਲ() {}
    public static byte[] 바이트읽기(String ਨਾਂ) throws 입출력예외 {
        try {
        FileInputStream ਸਟ੍ਰੀਮ_ਕੀਮਤ = new FileInputStream(ਨਾਂ);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, ਕੀਮਤ;
            while ((ਕੀਮਤ = ਸਟ੍ਰੀਮ_ਕੀਮਤ.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("ਫਾਇਲ ਆਕਾਰ 제한"); 임시[수++] = (byte)ਕੀਮਤ; }
            byte[] ਮਾਪ = new byte[수]; System.arraycopy(임시, 0, ਮਾਪ, 0, 수); return ਮਾਪ;
        } finally { ਸਟ੍ਰੀਮ_ਕੀਮਤ.close(); }
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public static void ਲਿੱਖੋ_ਬਾਈਟ_ਕੀਮਤ(String ਨਾਂ, byte[] ਤਤਕਰਾ_ਕੀਮਤ) throws 입출력예외 {
        try {
        FileOutputStream ਸਟ੍ਰੀਮ_ਕੀਮਤ = new FileOutputStream(ਨਾਂ);
        try { for (int ਲੂਪ_ਅਨੁਕ੍ਰਮਣਿਕਾ = 0; ਲੂਪ_ਅਨੁਕ੍ਰਮਣਿਕਾ < ਤਤਕਰਾ_ਕੀਮਤ.length; ਲੂਪ_ਅਨੁਕ੍ਰਮਣਿਕਾ++) ਸਟ੍ਰੀਮ_ਕੀਮਤ.write(ਤਤਕਰਾ_ਕੀਮਤ[ਲੂਪ_ਅਨੁਕ੍ਰਮਣਿਕਾ] & 255); } finally { ਸਟ੍ਰੀਮ_ਕੀਮਤ.close(); }
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public static String ਪੜ੍ਹਨ(String ਨਾਂ) throws 입출력예외 {
        try { return 문자.ਬਦਲਾਵ_ਕਰੋ_ਸਮੱਗਰੀ(바이트읽기(ਨਾਂ));
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public static void ਲਿਖਣ(String ਨਾਂ, String ਤਤਕਰਾ_ਕੀਮਤ) throws 입출력예외 {
        try { ਲਿੱਖੋ_ਬਾਈਟ_ਕੀਮਤ(ਨਾਂ, 문자.부호화(ਤਤਕਰਾ_ਕੀਮਤ));
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
}
