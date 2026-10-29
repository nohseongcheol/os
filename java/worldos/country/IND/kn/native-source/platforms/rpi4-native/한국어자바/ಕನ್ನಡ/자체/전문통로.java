// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;

/** 전문(電文)·ಚಾನಲ್_ನಮೂದು(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int ಪೋರ್ಟ್_ಸಂಖ್ಯೆ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { 표준종단 = 통신.ತೆರೆ(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public static 전문통로 ತೆರೆ(int ಪೋರ್ಟ್_ಸಂಖ್ಯೆ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { return new 전문통로(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public void ಕಳುಹಿಸಿ(String ಇಮೇಲ್, int ಪೋರ್ಟ್_ಸಂಖ್ಯೆ, String ಡೇಟಾ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { 통신.ಕಳುಹಿಸಿ(표준종단, ಇಮೇಲ್, ಪೋರ್ಟ್_ಸಂಖ್ಯೆ, ಡೇಟಾ);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public String 받기() throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public void 대기시간(int 밀리초) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public int ಪೋರ್ಟ್_ಸಂಖ್ಯೆ() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void ಮುಚ್ಚು() { 통신.ಮುಚ್ಚು(표준종단); }
}
