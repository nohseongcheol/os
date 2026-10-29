// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;

/** 전문(電文)·cainéal_iontráil(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int uimhir_phoirt) throws I_O_eisceacht {
        try { 표준종단 = 통신.Oscail(uimhir_phoirt);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public static 전문통로 Oscail(int uimhir_phoirt) throws I_O_eisceacht {
        try { return new 전문통로(uimhir_phoirt);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public void seol(String ADDRESS, int uimhir_phoirt, String sonraí) throws I_O_eisceacht {
        try { 통신.seol(표준종단, ADDRESS, uimhir_phoirt, sonraí);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public String 받기() throws I_O_eisceacht {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_eisceacht {
        try { 통신.TIMEOUT(표준종단, 밀리초);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public int uimhir_phoirt() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Dún() { 통신.Dún(표준종단); }
}
