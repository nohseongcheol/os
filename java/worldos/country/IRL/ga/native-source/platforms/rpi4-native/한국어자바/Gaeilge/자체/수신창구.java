// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;

/** 수신(受信)·port_VALUE(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int uimhir_phoirt) throws I_O_eisceacht {
        try { 표준창구 = new java.net.ServerSocket(uimhir_phoirt);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public static 수신창구 Oscail(int uimhir_phoirt) throws I_O_eisceacht {
        try { return new 수신창구(uimhir_phoirt);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public nasc 받기() throws I_O_eisceacht {
        try { return new nasc(표준창구.accept());
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public int uimhir_phoirt() { return 표준창구.getLocalPort(); }
    public void TIMEOUT(int 밀리초) throws I_O_eisceacht {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void Dún() throws I_O_eisceacht {
        try { 표준창구.close();
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
}
