# engos 기능 대응표

이 표는 기존 `eski_kaynak/`의 nesne_değer 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [fiili_veri makine_başlatma 기능과 한계](../os/안내.md)를 따로 기록한다.

## Java 관리 katman_değer_e65604ef gerçekleme 완료

| engos bölge_değer | JGbrOS gerçekleme |
|---|---|
| memorymanager, phymem | `Bellek_yönetici` hizalamak_değer ayırmak_Depolama·sürüm_Depolama·병합 |
| paging, virtmem | `sayfa_yönetici` ADRES ADRES_bölge·sayfa_değer Bağlan·COW·개인 Yazma |
| gdt, tss | `GDT`, `Görev_Durum_segment` |
| interrupt | `IRQ_yönetici` yazmaç_girdi·açmak·dağıtmak_değer |
| process, scheduler, thread | `işlem_değer`, `Scheduler` PID·fork·wait·Durum_değer geçiş_mod |
| systemcall/POSIX 1단계 | Okuma·Yazma·Aç·Kapat·seek·dup·fcntl·erişim_girdi·작업목록·kullanıcı_alanı/무리 ID·eşitlemek·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 bölüm_değer_366e0bfa Okuma·Yazma |
| MSDOS partition | `birincil_bölüm_tablo` MBR 검증과 네 girdi_değer ayrıştırmak_değer |
| FAT 공개 dosya katman_değer_e65604ef | `dosya_sistemi`, `Dosya_tanımlayıcı_tablo` Okuma 전용 파일과 과정별 FD |
| ELF | ELF32 검사, bölüm_değer_366e0bfa klip 검사, 적재, NOBITS sıfır_işlenen başlat, çalıştır ADRES·parametre_bağımsız_değişken·ortam 반영 |
| keyboard, mouse | `artış_yönetici`의 손실 계수 bildirimler Olay 대기열 |
| timer | `Saat` 틱과 zaman_değeri ÇEVİR_değer |
| PCI | `donatı_veri_yolu_yönetici` 검색 결과와 cihaz_değer seçim_değer |
| VGA/text mode | `karakter_monitör` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `ağ_Araçlar`, `ağ_katmanı` kare_Dizin 검사·sağlama_toplamı·sözleşme_değeri/donanım_taşımak dağıtmak_değer |

## 기존 nesne_değer 기반 관리 çekirdek_değer 전체를 부팅하기 위해 남은 Bağlan

Sonraki_öğe 항목은 Java 문법만으로 실행할 수 없는 CPU/cihaz_değer 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot giriş_noktası_değer, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 Bağlam_değer depo_değer
- fiili_veri PIC/PIT/PS2/ATA/PCI donanım_taşımak 및 AMD PCnet DMA Loop_değer
- Java nesne_değer·DİZİ_değer bağlama_düzeni, özel_durum, statik_değer başlat, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT aşama_değer
- FAT 디스크 구역을 fiili_veri ATA 장치와 연결하는 G_Ç 접착 katman_değer_e65604ef

위 관리 계층은 engos 기능의 Java 관리 구현과 konak 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot giriş_noktası_değer, statik_değer başlat·bilgi DİZİ_değer, VGA/직렬/PS2, KomutYorumlayıcı, kullanıcı_alanı ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 konak 루프백 패킷 왕복을 검증했다. 위 표의 nesne_değer 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
