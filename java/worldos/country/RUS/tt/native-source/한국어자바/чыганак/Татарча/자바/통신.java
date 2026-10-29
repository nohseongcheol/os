// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Хата 상태도 호출자가 판단할 수 있도록 җавап_бирү 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI адрес, Duration вакыт_чиге)
            throws IOException, InterruptedException {
        HttpClient ялгау = HttpClient.newBuilder().connectTimeout(вакыт_чиге).build();
        return ялгау.send(HttpRequest.newBuilder(адрес).timeout(вакыт_чиге).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String адрес, int 포트, int 제한밀리초) throws IOException {
        Socket ялгау = new Socket();
        try {
            ялгау.connect(new InetSocketAddress(адрес, 포트), 제한밀리초);
            ялгау.setSoTimeout(제한밀리초);
            return ялгау;
        } catch (IOException Хата) { ялгау.close(); throw Хата; }
    }
}
