// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;
/** eigin JVM과 커널의 Gluggi 관리 기능에 직접 연결되는 Gluggi. */
public final class Gluggi extends 화면구성요소 {
    public Gluggi(String gluggi_Titill, int 폭, int 높이) {
        throw new staða_undantekning("eigin JVM의 Íslenska Gluggi skapa 기능이 필요합니다.");
    }
    public native void bæta_við_eining(화면구성요소 eining_VALUE);
    public native void sýna_gluggi();
    public native void Loka();
    public native boolean 보이는가();
}
