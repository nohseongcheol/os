// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;

/** 입력(入力)과 voog_VALUE: 순서대로 들어오는 바이트를 읽는 Kanal_kirje. */
public final class sisendvoog {
    private final java.io.InputStream 표준흐름;
    sisendvoog(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Lugemine() throws I_O_erand {
        try { return 표준흐름.read();
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public int Lugemine(byte[] andmed) throws I_O_erand {
        try { return 표준흐름.read(andmed);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public int Lugemine(byte[] andmed, int Käivita_2, int 길이) throws I_O_erand {
        try { return 표준흐름.read(andmed, Käivita_2, 길이);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public void Suletud() throws I_O_erand {
        try { 표준흐름.close();
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
}
