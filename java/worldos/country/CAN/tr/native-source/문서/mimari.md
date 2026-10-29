# JCanOS mimari

아래는 nesne_değer 기반 관리 çekirdek_değer 전체의 hedef_nesne 구조다. geçerli_öğe fiili_veri makine_başlatma 가능한 제한형 구현은 `compiler/`와 `os/`에 있으며 [네이티브 işletim_sistemi 안내](../os/안내.md)에 gerçekleme 범위를 명시한다. 아래의 GC·Bağlam_değer geçiş_mod·dosya_sistemi 등이 새 ISO에 모두 포함돼 있지는 않다.

```text
GRUB 또는 UEFI
  ↓
x86 최소 부트·트랩 katman_değer_e65604ef
  ↓
Java AOT 실행기와 nesne_değer·DİZİ_değer·GC 런타임
  ↓
donanım_değer sınır_değer
  ↓
Java 관리 çekirdek_değer
  ├─ Bellek_bölge/쪽관리/COW
  ├─ işlem_değer/배정/wait
  ├─ dosya_sistemi/ELF/POSIX
  └─ artış_değer/depolama_aygıtı/ağ_Yığın
```

OpenJDK 자체는 이미 운영체제가 제공하는 dosya, 스레드, 가상 기억공간을 전제로 한다. 따라서 çekirdek_değer 부팅에는 OpenJDK를 그대로 넣지 않고 제한된 Java 바이트코드 AOT와 작은 런타임을 사용한다.

네이티브 계층에는 `in/out`, `hlt`, CR0/CR2/CR3/CR4, `iret`, Bağlam_değer 저장처럼 Java로 표현할 수 없는 CPU 동작만 남긴다. 정책과 자료구조는 Java에 둔다.
