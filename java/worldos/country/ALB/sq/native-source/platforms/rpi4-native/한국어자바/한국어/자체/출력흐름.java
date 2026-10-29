// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 Stream_VALUE: 순서를 보존해 내보내는 바이트의 kanal_futje. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Shkrimi(int VALUE) throws I_O_përjashtim {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public void Shkrimi(byte[] të_dhëna) throws I_O_përjashtim {
        try { 표준흐름.write(të_dhëna);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public void Shkrimi(byte[] të_dhëna, int Ekzekuto, int gjatësi_VALUE) throws I_O_përjashtim {
        try { 표준흐름.write(të_dhëna, Ekzekuto, gjatësi_VALUE);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public void 내보내기() throws I_O_përjashtim {
        try { 표준흐름.flush();
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public void Mbyll() throws I_O_përjashtim {
        try { 표준흐름.close();
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
}
