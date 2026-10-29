// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;

/** 입력(入力)과 sruth_VALUE: 순서대로 들어오는 바이트를 읽는 cainéal_iontráil. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Léigh() throws I_O_eisceacht {
        try { return 표준흐름.read();
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public int Léigh(byte[] sonraí) throws I_O_eisceacht {
        try { return 표준흐름.read(sonraí);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public int Léigh(byte[] sonraí, int Rith_2, int fad_VALUE) throws I_O_eisceacht {
        try { return 표준흐름.read(sonraí, Rith_2, fad_VALUE);
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
    public void Dún() throws I_O_eisceacht {
        try { 표준흐름.close();
        } catch (java.io.IOException ERREÁID) { throw CONVERT_eisceacht.I_O(ERREÁID); }
        catch (RuntimeException ERREÁID) { throw CONVERT_eisceacht.Rith_ordú(ERREÁID); }
    }
}
