// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ተጠቃሚ 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ፋይል {
    private ፋይል() {}
    public static byte[] 바이트읽기(String ሽም) throws 입출력예외 {
        try {
        FileInputStream ወሓዚ_ዋጋ = new FileInputStream(ሽም);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, ዋጋ;
            while ((ዋጋ = ወሓዚ_ዋጋ.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("ፋይል መጠን 제한"); 임시[수++] = (byte)ዋጋ; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { ወሓዚ_ዋጋ.close(); }
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public static void ጸሓፍ_ባይት_ዋጋ(String ሽም, byte[] ትሕዝቶ_ዋጋ) throws 입출력예외 {
        try {
        FileOutputStream ወሓዚ_ዋጋ = new FileOutputStream(ሽም);
        try { for (int ደጋግም_መሐበሪ = 0; ደጋግም_መሐበሪ < ትሕዝቶ_ዋጋ.length; ደጋግም_መሐበሪ++) ወሓዚ_ዋጋ.write(ትሕዝቶ_ዋጋ[ደጋግም_መሐበሪ] & 255); } finally { ወሓዚ_ዋጋ.close(); }
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public static String 읽기(String ሽም) throws 입출력예외 {
        try { return 문자.ምስጢር_ፍታሕ_ሓበሬታ(바이트읽기(ሽም));
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public static void ጸሓፍ(String ሽም, String ትሕዝቶ_ዋጋ) throws 입출력예외 {
        try { ጸሓፍ_ባይት_ዋጋ(ሽም, 문자.부호화(ትሕዝቶ_ዋጋ));
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
}
