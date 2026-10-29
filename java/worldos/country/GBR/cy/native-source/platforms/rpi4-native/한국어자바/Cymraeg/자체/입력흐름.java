// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;

/** 입력(入力)과 ffrwd_VALUE: 순서대로 들어오는 바이트를 읽는 sianel_cofnod. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Darllen() throws I_O_eithriad {
        try { return 표준흐름.read();
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public int Darllen(byte[] data) throws I_O_eithriad {
        try { return 표준흐름.read(data);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public int Darllen(byte[] data, int Gweithredu_2, int hyd_VALUE) throws I_O_eithriad {
        try { return 표준흐름.read(data, Gweithredu_2, hyd_VALUE);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public void Cau() throws I_O_eithriad {
        try { 표준흐름.close();
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
}
