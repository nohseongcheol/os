// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·portë_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int numri_i_portës) throws I_O_përjashtim {
        try { 표준창구 = new java.net.ServerSocket(numri_i_portës);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public static 수신창구 Hap(int numri_i_portës) throws I_O_përjashtim {
        try { return new 수신창구(numri_i_portës);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public lidhje 받기() throws I_O_përjashtim {
        try { return new lidhje(표준창구.accept());
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public int numri_i_portës() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws I_O_përjashtim {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Mbyll() throws I_O_përjashtim {
        try { 표준창구.close();
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
}
