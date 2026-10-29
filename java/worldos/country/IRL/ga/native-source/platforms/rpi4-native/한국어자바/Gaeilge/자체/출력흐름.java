// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;

/** Aschur(出力)과 sruth_VALUE: 순서를 보존해 내보내는 바이트의 cainéal_iontráil. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Scríobh(int VALUE) throws I_O_eisceacht {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public void Scríobh(byte[] sonraí) throws I_O_eisceacht {
        try { 표준흐름.write(sonraí);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public void Scríobh(byte[] sonraí, int Rith_2, int fad_VALUE) throws I_O_eisceacht {
        try { 표준흐름.write(sonraí, Rith_2, fad_VALUE);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public void 내보내기() throws I_O_eisceacht {
        try { 표준흐름.flush();
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public void Dún() throws I_O_eisceacht {
        try { 표준흐름.close();
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
}
