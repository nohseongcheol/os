// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;

/** 전문(電文)·sianel_cofnod(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int rhif_porth) throws I_O_eithriad {
        try { 표준종단 = 통신.Agor(rhif_porth);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public static 전문통로 Agor(int rhif_porth) throws I_O_eithriad {
        try { return new 전문통로(rhif_porth);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public void anfon(String ADDRESS, int rhif_porth, String data) throws I_O_eithriad {
        try { 통신.anfon(표준종단, ADDRESS, rhif_porth, data);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public String 받기() throws I_O_eithriad {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_eithriad {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public int rhif_porth() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Cau() { 통신.Cau(표준종단); }
}
