# kullanıcı_alanı 호출 sınır_değer

대상은 jkoros i386 ELF32다. Linux i386의 호출 번호와 바이너리 호환이 아니다. C의 cdecl 인수를 `makine/işletim_sistemi_Çağrılar.s`에서 EAX(Dizin), EBX·ECX·EDX·ESI·EDI(첫째~다섯째 bağımsız_değişkenler)로 변환한다. EBX·ESI·EDI·EBP를 보존하며 결과는 EAX다. çekirdek_değer 실패는 Negatif_değer hata Dizin, C kitaplık 실패는 -1과 양수 errno다.

커널은 0x04000000 이상, 0x04400000 미만의 kullanıcı_alanı bölge_değer 안에 자료의 전체 길이가 들어가는지 확인한다. 단순 널 검사가 아니다. C veri 주소는 bayt_değer 주소이며, 기존 Java AOT `int[]` 포인터와 혼용하지 않는다. Java dosya 흐름의 어셈블리 경계가 별도 bayt_değer 버퍼를 마련하여 같은 호출을 사용한다.

| Dizin | Eylem | bağımsız_değişkenler |
|---|---|---|
| 30 | açık_Dosya | NUL 끝 İsim ADRES, Ayarlar, izin_verme_izin |
| 31 | 파일자료읽기 | tanımlayıcı_girdi, veri ADRES, bayt_değer 수 |
| 32 | yazma_Dosya_veri | tanımlayıcı_girdi, veri ADRES, bayt_değer 수 |
| 33 | Kapat_Dosya | tanımlayıcı_girdi |
| 34 | arama_Dosya | tanımlayıcı_girdi, kodlama_değer 있는 Ofset_değer, işlem_kök |
| 35 | kopya_Dosya_tanımlayıcı | tanımlayıcı_girdi |
| 36 | 파일서술자지정복제 | tanımlayıcı_girdi, 새 tanımlayıcı_girdi |
| 37 | 파일상태읽기 | tanımlayıcı_girdi, 48바이트 Durum_değer ADRES |
| 38 | kaldırmak_Dosya_girdi_ad | NUL 끝 İsim ADRES |
| 39 | küme_Dosya_süre | tanımlayıcı_girdi, 새 süre_değer |
| 40 | denetim_Dosya_tanımlayıcı | tanımlayıcı_girdi, komut, değer |
| 41 | açmak_uç_nokta | ADRES işletim_sistemi_değer, Tip_değer, sözleşme_değeri Dizin |
| 42 | BIND_ADRES | tanımlayıcı_girdi, sockaddr_in ADRES, süre_değer |
| 43 | göndermek_veri_birimi_veri | tanımlayıcı_girdi, veri ADRES, süre_değer, Ayarlar, istek ADRES |
| 44 | almak_veri_birimi_veri | tanımlayıcı_girdi, veri ADRES, süre_değer, Ayarlar, istek ADRES |
| 45 | 통신주소읽기 | tanımlayıcı_girdi, sockaddr ADRES, socklen_t ADRES |
| 46 | küme_almak_ZAMANAŞIMI | tanımlayıcı_girdi, 0~2000 밀리초 |
| 47 | commit_Dosyalar | tanımlayıcı_girdi |

43번 요청은 32비트 주소와 32비트 길이의 두 칸이다. 44번 요청은 32비트 주소와 길이를 담은 32비트 값의 ADRES 두 칸이다. almak_değer 주소가 NULL이면 eş_değer ADRES 기록을 생략한다. sockaddr_in은 16바이트이며 ADRES 체계는 cihaz_değer bayt_değer dizi_değer, 접속번호와 IP 주소는 네트워크 bayt_değer 차례다. 축소된 ADRES 버퍼에도 들어가는 앞부분을 쓰고 전체 ADRES Boyut 16을 반환한다.

0~22번의 기존 Java AOT 호출은 유지한다. 0은 Çıkış_program, 2·3은 기존 bağımsız_değişkenler 조회다. geçerli_öğe 커널의 bağımsız_değişkenler 목록이 yürütmek_komut 이름을 제외하므로 C 진입기는 argv[0]에 고정 dize_değer `jkoros-app`을 넣고 이후 인수를 전달한다. argv 끝에는 NULL이 있다. 이 제한도 일반 UNIX işlem_değer ABI와 다른 점이다.

표준 헤더의 bilgi Boyut, 플래그 değer, stat alan_değeri 순서는 `kaynakKod/bildirimler/`에 정의한다. 동적 Bağlan·다중 işlem_değer·스레드가 추가되면 hata Dizin 저장과 kaynak_değer 수명, 호출 경계도 함께 검토해야 한다.
