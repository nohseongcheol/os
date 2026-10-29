// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static aloqa Ochish(String manzil, int 접속번호) throws I_O_istisno {
        try { return aloqa.Ochish(manzil, 접속번호);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public static 수신창구 수신열기(int 접속번호) throws I_O_istisno {
        try { return 수신창구.Ochish(접속번호);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public static Socket Ulanish(String manzil, int port_VALUE) throws I_O_istisno {
        try { return new Socket(manzil, port_VALUE);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public static ServerSocket 듣기(int port_VALUE) throws I_O_istisno {
        try { return new ServerSocket(port_VALUE);
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
    public static Socket 받기(ServerSocket server_VALUE) throws I_O_istisno {
        try { return server_VALUE.accept();
        } catch (java.io.IOException Xato) { throw CONVERT_istisno.I_O(Xato); }
        catch (RuntimeException Xato) { throw CONVERT_istisno.bajarmoq_buyruq(Xato); }
    }
}
