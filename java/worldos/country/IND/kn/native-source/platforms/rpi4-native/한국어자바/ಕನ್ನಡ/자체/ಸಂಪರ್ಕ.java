// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;

/** ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು(連結)·ಚಾನಲ್_ನಮೂದು(通路): 상대와 이어진 TCP ಬೈಟ್_ಮೌಲ್ಯ 흐름의 종단. */
public final class ಸಂಪರ್ಕ {
    private final java.net.Socket 표준연결;
    ಸಂಪರ್ಕ(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static ಸಂಪರ್ಕ ತೆರೆ(String ಇಮೇಲ್, int ಪೋರ್ಟ್_ಸಂಖ್ಯೆ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try {
            return new ಸಂಪರ್ಕ(new java.net.Socket(ಇಮೇಲ್, ಪೋರ್ಟ್_ಸಂಖ್ಯೆ));
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public 입력흐름 입력() throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public 출력흐름 ಔಟ್_ಪುಟ್() throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public void 대기시간(int 밀리초) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public int ಪೋರ್ಟ್_ಸಂಖ್ಯೆ() { return 표준연결.getPort(); }
    public int ಸ್ಥಳೀಯ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void ಮುಚ್ಚು() throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { 표준연결.close();
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
}
