// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자체;

/** 출력(出力)과 Stream_agaciro: 순서를 보존해 내보내는 바이트의 umurongo_icyinjizwa. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void kwandika(int agaciro) throws 입출력예외 {
        try { 표준흐름.write(agaciro);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public void kwandika(byte[] amakurushingiro) throws 입출력예외 {
        try { 표준흐름.write(amakurushingiro);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public void kwandika(byte[] amakurushingiro, int ihuriro, int uburebure_agaciro) throws 입출력예외 {
        try { 표준흐름.write(amakurushingiro, ihuriro, uburebure_agaciro);
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
    public void Gufunga() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException IKOSA) { throw 예외변환.I_O(IKOSA); }
        catch (RuntimeException IKOSA) { throw 예외변환.gukora_ibwiriza(IKOSA); }
    }
}
