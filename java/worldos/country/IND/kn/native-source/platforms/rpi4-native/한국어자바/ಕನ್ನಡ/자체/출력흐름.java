// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;

/** ಔಟ್_ಪುಟ್(出力)과 ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ: 순서를 보존해 내보내는 바이트의 ಚಾನಲ್_ನಮೂದು. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void ಬರೆ(int ಮೌಲ್ಯ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { 표준흐름.write(ಮೌಲ್ಯ);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public void ಬರೆ(byte[] ಡೇಟಾ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { 표준흐름.write(ಡೇಟಾ);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public void ಬರೆ(byte[] ಡೇಟಾ, int ಚಲಾಯಿಸು_2, int ಉದ್ದ_ಮೌಲ್ಯ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { 표준흐름.write(ಡೇಟಾ, ಚಲಾಯಿಸು_2, ಉದ್ದ_ಮೌಲ್ಯ);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public void 내보내기() throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { 표준흐름.flush();
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public void ಮುಚ್ಚು() throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { 표준흐름.close();
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
}
