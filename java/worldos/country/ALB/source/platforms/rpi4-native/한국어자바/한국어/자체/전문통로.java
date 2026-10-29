// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·kanal_futje(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int numri_i_portës) throws I_O_përjashtim {
        try { 표준종단 = 통신.Hap(numri_i_portës);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public static 전문통로 Hap(int numri_i_portës) throws I_O_përjashtim {
        try { return new 전문통로(numri_i_portës);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public void dërgoj(String email, int numri_i_portës, String të_dhëna) throws I_O_përjashtim {
        try { 통신.dërgoj(표준종단, email, numri_i_portës, të_dhëna);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public String 받기() throws I_O_përjashtim {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_përjashtim {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public int numri_i_portës() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Mbyll() { 통신.Mbyll(표준종단); }
}
