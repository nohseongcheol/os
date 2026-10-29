// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class kommunikáció {
    private kommunikáció() {}
    /** HTTP HIBA 상태도 호출자가 판단할 szám 있도록 válasz 전체를 반환한다. */
    public static HttpResponse<String> ÁTHELYEZ_ÉRTÉK(URI CÍM, Duration időkorlát)
            throws IOException, InterruptedException {
        HttpClient Kapcsolódás = HttpClient.newBuilder().connectTimeout(időkorlát).build();
        return Kapcsolódás.send(HttpRequest.newBuilder(CÍM).timeout(időkorlát).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket Connect_Endpoint(String CÍM, int hardver_port, int 제한밀리초) throws IOException {
        Socket Kapcsolódás = new Socket();
        try {
            Kapcsolódás.connect(new InetSocketAddress(CÍM, hardver_port), 제한밀리초);
            Kapcsolódás.setSoTimeout(제한밀리초);
            return Kapcsolódás;
        } catch (IOException HIBA) { Kapcsolódás.close(); throw HIBA; }
    }
}
