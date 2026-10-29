// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ಬಳಕೆದಾರ 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ಕಡತ {
    private ಕಡತ() {}
    public static byte[] 바이트읽기(String ಹೆಸರು) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try {
        FileInputStream ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ = new FileInputStream(ಹೆಸರು);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, ಮೌಲ್ಯ;
            while ((ಮೌಲ್ಯ = ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.read()) != -1) { if (수 == 임시.length) throw new ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ("ಕಡತ ಗಾತ್ರ 제한"); 임시[수++] = (byte)ಮೌಲ್ಯ; }
            byte[] ಮಾಪನ = new byte[수]; System.arraycopy(임시, 0, ಮಾಪನ, 0, 수); return ಮಾಪನ;
        } finally { ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.close(); }
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public static void ಬರೆ_ಬೈಟ್_ಮೌಲ್ಯ(String ಹೆಸರು, byte[] ವಿಷಯ_ಮೌಲ್ಯ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try {
        FileOutputStream ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ = new FileOutputStream(ಹೆಸರು);
        try { for (int ಲೂಪ್_ಪದಸೂಚಿ = 0; ಲೂಪ್_ಪದಸೂಚಿ < ವಿಷಯ_ಮೌಲ್ಯ.length; ಲೂಪ್_ಪದಸೂಚಿ++) ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.write(ವಿಷಯ_ಮೌಲ್ಯ[ಲೂಪ್_ಪದಸೂಚಿ] & 255); } finally { ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.close(); }
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public static String ಓದು(String ಹೆಸರು) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { return 문자.ಡೀಕ್ರಿಪ್ಟ್_ಮಾಡಿ_ಡೇಟಾ(바이트읽기(ಹೆಸರು));
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public static void ಬರೆ(String ಹೆಸರು, String ವಿಷಯ_ಮೌಲ್ಯ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { ಬರೆ_ಬೈಟ್_ಮೌಲ್ಯ(ಹೆಸರು, 문자.부호화(ವಿಷಯ_ಮೌಲ್ಯ));
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
}
