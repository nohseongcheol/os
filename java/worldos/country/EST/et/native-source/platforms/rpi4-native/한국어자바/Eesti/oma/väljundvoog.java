// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;

/** Väljund(出力)과 voog_VALUE: 순서를 보존해 내보내는 바이트의 Kanal_kirje. */
public final class väljundvoog {
    private final java.io.OutputStream 표준흐름;
    väljundvoog(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Kirjutamine(int VALUE) throws I_O_erand {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public void Kirjutamine(byte[] andmed) throws I_O_erand {
        try { 표준흐름.write(andmed);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public void Kirjutamine(byte[] andmed, int Käivita_2, int 길이) throws I_O_erand {
        try { 표준흐름.write(andmed, Käivita_2, 길이);
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public void 내보내기() throws I_O_erand {
        try { 표준흐름.flush();
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
    public void Suletud() throws I_O_erand {
        try { 표준흐름.close();
        } catch (java.io.IOException VIGA) { throw CONVERT_erand.I_O(VIGA); }
        catch (RuntimeException VIGA) { throw CONVERT_erand.Täida_käsk(VIGA); }
    }
}
