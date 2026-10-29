// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 მომხმარებელი 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ფაილი {
    private ფაილი() {}
    public static byte[] 바이트읽기(String სახელი) throws 입출력예외 {
        try {
        FileInputStream ნაკადი_მნიშვნელობა = new FileInputStream(სახელი);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, მნიშვნელობა;
            while ((მნიშვნელობა = ნაკადი_მნიშვნელობა.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("ფაილი ზომა 제한"); 임시[수++] = (byte)მნიშვნელობა; }
            byte[] გაზომვა = new byte[수]; System.arraycopy(임시, 0, გაზომვა, 0, 수); return გაზომვა;
        } finally { ნაკადი_მნიშვნელობა.close(); }
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public static void ჩაწერა_ბაიტი_მნიშვნელობა(String სახელი, byte[] შიგთავსი_მნიშვნელობა) throws 입출력예외 {
        try {
        FileOutputStream ნაკადი_მნიშვნელობა = new FileOutputStream(სახელი);
        try { for (int ციკლი_ინდექსი = 0; ციკლი_ინდექსი < შიგთავსი_მნიშვნელობა.length; ციკლი_ინდექსი++) ნაკადი_მნიშვნელობა.write(შიგთავსი_მნიშვნელობა[ციკლი_ინდექსი] & 255); } finally { ნაკადი_მნიშვნელობა.close(); }
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public static String კითხვა(String სახელი) throws 입출력예외 {
        try { return 문자.გაშიფვრა_მონაცემები(바이트읽기(სახელი));
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public static void ჩაწერა(String სახელი, String შიგთავსი_მნიშვნელობა) throws 입출력예외 {
        try { ჩაწერა_ბაიტი_მნიშვნელობა(სახელი, 문자.부호화(შიგთავსი_მნიშვნელობა));
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
}
