// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 Stream_VALUE: 순서대로 들어오는 바이트를 읽는 kanal_futje. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Leximi() throws I_O_përjashtim {
        try { return 표준흐름.read();
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public int Leximi(byte[] të_dhëna) throws I_O_përjashtim {
        try { return 표준흐름.read(të_dhëna);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public int Leximi(byte[] të_dhëna, int Ekzekuto, int gjatësi_VALUE) throws I_O_përjashtim {
        try { return 표준흐름.read(të_dhëna, Ekzekuto, gjatësi_VALUE);
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
    public void Mbyll() throws I_O_përjashtim {
        try { 표준흐름.close();
        } catch (java.io.IOException GABIM) { throw CONVERT_përjashtim.I_O(GABIM); }
        catch (RuntimeException GABIM) { throw CONVERT_përjashtim.zbatoj_komandë(GABIM); }
    }
}
