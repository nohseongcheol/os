// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;

/** Allbwn(出力)과 ffrwd_VALUE: 순서를 보존해 내보내는 바이트의 sianel_cofnod. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Ysgrifennu(int VALUE) throws I_O_eithriad {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public void Ysgrifennu(byte[] data) throws I_O_eithriad {
        try { 표준흐름.write(data);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public void Ysgrifennu(byte[] data, int Gweithredu_2, int hyd_VALUE) throws I_O_eithriad {
        try { 표준흐름.write(data, Gweithredu_2, hyd_VALUE);
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public void 내보내기() throws I_O_eithriad {
        try { 표준흐름.flush();
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
    public void Cau() throws I_O_eithriad {
        try { 표준흐름.close();
        } catch (java.io.IOException Gwall) { throw CONVERT_eithriad.I_O(Gwall); }
        catch (RuntimeException Gwall) { throw CONVERT_eithriad.Gweithredu_gorchymyn(Gwall); }
    }
}
