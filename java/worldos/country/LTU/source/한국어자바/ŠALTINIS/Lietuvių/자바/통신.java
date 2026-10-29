// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP KLAIDA 상태도 호출자가 판단할 numeris 있도록 atsakyti 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI ADDRESS, Duration laiko_apribojimas)
            throws IOException, InterruptedException {
        HttpClient Prisijungti = HttpClient.newBuilder().connectTimeout(laiko_apribojimas).build();
        return Prisijungti.send(HttpRequest.newBuilder(ADDRESS).timeout(laiko_apribojimas).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket ryšys_dalyvis(String ADDRESS, int aparatūra_jungtis, int 제한밀리초) throws IOException {
        Socket Prisijungti = new Socket();
        try {
            Prisijungti.connect(new InetSocketAddress(ADDRESS, aparatūra_jungtis), 제한밀리초);
            Prisijungti.setSoTimeout(제한밀리초);
            return Prisijungti;
        } catch (IOException KLAIDA) { Prisijungti.close(); throw KLAIDA; }
    }
}
