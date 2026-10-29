// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** ഫലം(出力)과 സ്ട്രീം_മൂല്യം: 순서를 보존해 내보내는 바이트의 ചാനല്_എന്_ട്രി. */
public final class ഔട്ട്പുട്ട്_തുടര്_ച്ച {
    private final java.io.OutputStream 표준흐름;
    ഔട്ട്പുട്ട്_തുടര്_ച്ച(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void എഴുത്തു്(int മൂല്യം) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { 표준흐름.write(മൂല്യം);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public void എഴുത്തു്(byte[] ഡാറ്റാ) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { 표준흐름.write(ഡാറ്റാ);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public void എഴുത്തു്(byte[] ഡാറ്റാ, int നടപ്പിലാക്കുക, int ദൈര്_ഘ്യം_മൂല്യം) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { 표준흐름.write(ഡാറ്റാ, നടപ്പിലാക്കുക, ദൈര്_ഘ്യം_മൂല്യം);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public void 내보내기() throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { 표준흐름.flush();
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public void അടയ്ക്കു() throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { 표준흐름.close();
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
}
