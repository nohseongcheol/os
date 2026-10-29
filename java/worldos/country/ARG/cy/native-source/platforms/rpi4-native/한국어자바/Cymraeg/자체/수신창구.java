// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;

/** 수신(受信)·porth_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int rhif_porth) throws I_O_eithriad {
        try { 표준창구 = new java.net.ServerSocket(rhif_porth);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public static 수신창구 Agor(int rhif_porth) throws I_O_eithriad {
        try { return new 수신창구(rhif_porth);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public cyswllt 받기() throws I_O_eithriad {
        try { return new cyswllt(표준창구.accept());
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public int rhif_porth() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws I_O_eithriad {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Cau() throws I_O_eithriad {
        try { 표준창구.close();
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
}
