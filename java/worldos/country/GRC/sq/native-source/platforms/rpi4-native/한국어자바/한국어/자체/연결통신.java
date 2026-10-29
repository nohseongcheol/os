// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static lidhje Hap(String email, int numri_i_portës) throws I_O_përjashtim {
        try { return lidhje.Hap(email, numri_i_portës);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public static 수신창구 수신열기(int numri_i_portës) throws I_O_përjashtim {
        try { return 수신창구.Hap(numri_i_portës);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public static Socket Lidhu(String email, int portë_VALUE) throws I_O_përjashtim {
        try { return new Socket(email, portë_VALUE);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public static ServerSocket 듣기(int portë_VALUE) throws I_O_përjashtim {
        try { return new ServerSocket(portë_VALUE);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public static Socket 받기(ServerSocket server_VALUE) throws I_O_përjashtim {
        try { return server_VALUE.accept();
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
}
