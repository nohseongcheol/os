// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static ಸಂಪರ್ಕ ತೆರೆ(String ಇಮೇಲ್, int ಪೋರ್ಟ್_ಸಂಖ್ಯೆ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { return ಸಂಪರ್ಕ.ತೆರೆ(ಇಮೇಲ್, ಪೋರ್ಟ್_ಸಂಖ್ಯೆ);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public static 수신창구 수신열기(int ಪೋರ್ಟ್_ಸಂಖ್ಯೆ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { return 수신창구.ತೆರೆ(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public static Socket ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು(String ಇಮೇಲ್, int ಪೋರ್ಟ್_ಮೌಲ್ಯ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { return new Socket(ಇಮೇಲ್, ಪೋರ್ಟ್_ಮೌಲ್ಯ);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public static ServerSocket 듣기(int ಪೋರ್ಟ್_ಮೌಲ್ಯ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { return new ServerSocket(ಪೋರ್ಟ್_ಮೌಲ್ಯ);
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
    public static Socket 받기(ServerSocket ಸರ್ವರ್_ಮೌಲ್ಯ) throws ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ {
        try { return ಸರ್ವರ್_ಮೌಲ್ಯ.accept();
        } catch (java.io.IOException ದೋಷ) { throw 예외변환.ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(ದೋಷ); }
        catch (RuntimeException ದೋಷ) { throw 예외변환.ಪೂರೈಸು_ಆದೇಶ(ದೋಷ); }
    }
}
