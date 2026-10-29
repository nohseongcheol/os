// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static haɗi Buɗe(String imel, int lambar_kafa) throws I_O_banbanchi {
        try { return haɗi.Buɗe(imel, lambar_kafa);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public static 수신창구 수신열기(int lambar_kafa) throws I_O_banbanchi {
        try { return 수신창구.Buɗe(lambar_kafa);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public static Socket Haɗi(String imel, int fot_Daraja) throws I_O_banbanchi {
        try { return new Socket(imel, fot_Daraja);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public static ServerSocket 듣기(int fot_Daraja) throws I_O_banbanchi {
        try { return new ServerSocket(fot_Daraja);
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
    public static Socket 받기(ServerSocket Saba_Daraja) throws I_O_banbanchi {
        try { return Saba_Daraja.accept();
        } catch (java.io.IOException Kuskure) { throw 예외변환.I_O(Kuskure); }
        catch (RuntimeException Kuskure) { throw 예외변환.gudanar_Umarni(Kuskure); }
    }
}
