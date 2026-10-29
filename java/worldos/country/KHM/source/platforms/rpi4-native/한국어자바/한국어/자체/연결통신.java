// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static ការភ្ជាប់ បើក(String អ៊ីម៉ែល, int លេខរន្ធ) throws ចូល_ចេញ_ការលើកលែង {
        try { return ការភ្ជាប់.បើក(អ៊ីម៉ែល, លេខរន្ធ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public static 수신창구 수신열기(int លេខរន្ធ) throws ចូល_ចេញ_ការលើកលែង {
        try { return 수신창구.បើក(លេខរន្ធ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public static Socket ភ្ជាប់(String អ៊ីម៉ែល, int ច្រក_តំលៃ) throws ចូល_ចេញ_ការលើកលែង {
        try { return new Socket(អ៊ីម៉ែល, ច្រក_តំលៃ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public static ServerSocket 듣기(int ច្រក_តំលៃ) throws ចូល_ចេញ_ការលើកលែង {
        try { return new ServerSocket(ច្រក_តំលៃ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public static Socket 받기(ServerSocket ម៉ាស៊ីនមេ_តំលៃ) throws ចូល_ចេញ_ការលើកលែង {
        try { return ម៉ាស៊ីនមេ_តំលៃ.accept();
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
}
