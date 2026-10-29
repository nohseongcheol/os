// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;

/** Nasc(連結)·cainéal_iontráil(通路): 상대와 이어진 TCP beart_VALUE 흐름의 종단. */
public final class nasc {
    private final java.net.Socket 표준연결;
    nasc(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static nasc Oscail(String ADDRESS, int uimhir_phoirt) throws I_O_eisceacht {
        try {
            return new nasc(new java.net.Socket(ADDRESS, uimhir_phoirt));
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public 입력흐름 입력() throws I_O_eisceacht {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public 출력흐름 Aschur() throws I_O_eisceacht {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public void TIMEOUT(int 밀리초) throws I_O_eisceacht {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public int uimhir_phoirt() { return 표준연결.getPort(); }
    public int logánta_uimhir_phoirt() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Dún() throws I_O_eisceacht {
        try { 표준연결.close();
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
}
