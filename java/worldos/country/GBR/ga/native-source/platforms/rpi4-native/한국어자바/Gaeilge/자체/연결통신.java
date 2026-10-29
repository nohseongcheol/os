// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static nasc Oscail(String ADDRESS, int uimhir_phoirt) throws I_O_eisceacht {
        try { return nasc.Oscail(ADDRESS, uimhir_phoirt);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public static 수신창구 수신열기(int uimhir_phoirt) throws I_O_eisceacht {
        try { return 수신창구.Oscail(uimhir_phoirt);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public static Socket Nasc(String ADDRESS, int port_VALUE) throws I_O_eisceacht {
        try { return new Socket(ADDRESS, port_VALUE);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public static ServerSocket 듣기(int port_VALUE) throws I_O_eisceacht {
        try { return new ServerSocket(port_VALUE);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public static Socket 받기(ServerSocket freastalaí_VALUE) throws I_O_eisceacht {
        try { return freastalaí_VALUE.accept();
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
}
