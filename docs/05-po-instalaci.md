# 5. Po instalaci

## ADB

Na tomhle firmwaru je ADB zapnuté rovnou. Připoj budík k počítači běžně (bez BROM režimu):

```bash
adb devices
```

Kdyby se budík neobjevil, zapni vývojářský režim: **设置 (Nastavení) → 系统 (Systém) → 关于音箱 (O reproduktoru)** a opakovaně klepej na **版本号 (číslo verze)**.

## Instalace aplikací

```bash
adb install -r aplikace.apk
```

Budík nemá Google služby ani aktuální WebView a běží na Androidu 8.1. Hodně běžných aplikací na něm padá nebo se vůbec nenainstaluje — nejčastěji kvůli `ConstraintLayout` (hláška `You must supply a layout_width attribute`) nebo chybějícím knihovnám pro armeabi-v7a (`INSTALL_FAILED_NO_MATCHING_ABIS`).

Proto vzniklo [Free Radio](https://github.com/Blacker91/Radio-budik) — internetové rádio psané přímo pro tenhle budík.

## Odebrání zbytečných aplikací

Tyhle aplikace jde bez problémů odebrat, budík dál funguje normálně. Seznam je v souboru [`odstranit.txt`](../odstranit.txt):

| Balíček | Co to je |
|---|---|
| `com.xiaomi.smarthome` | Mi Home / Mijia |
| `com.qiyi.video.speaker` | iQiyi (video) |
| `tv.danmaku.bili` | Bilibili (video) |
| `com.xiaomi.mico.gallery` | galerie |
| `com.xiaomi.micovoip` | volání |
| `com.xiaomi.mesh.gateway` | brána pro chytrou domácnost |
| `com.xiaomi.mico.feedback` | odesílání logů a hlášení chyb |
| `com.xiaomi.mico.romupdate` | aktualizace systému od Xiaomi |
| `com.mediatek.duraspeed` | DuraSpeed — ukončuje aplikace na pozadí |
| `com.mediatek.bluetooth.dtt`, `com.mediatek.mtklogger.proxy`, `com.mediatek.dataprotection` | servisní nástroje MediaTek |
| `com.android.wallpapercropper`, `…wallpaperbackup`, `…managedprovisioning`, `…backupconfirm`, `…sharedstoragebackup`, `…companiondevicemanager`, `…providers.downloads.ui` | systémové doplňky, které budík nepotřebuje |

Odebrání celého seznamu najednou:

```bash
while read p; do echo -n "$p: "; adb shell -n pm uninstall -k --user 0 $p; done < odstranit.txt
```

(`-n` u `adb shell` je nutné — bez něj by adb spolkl zbytek seznamu a odebral jen první aplikaci.)

Aplikace se odebere jen pro uživatele, v systému zůstane. Zpátky ji vrátíš:

```bash
adb shell cmd package install-existing <balíček>
```

> [!CAUTION]
> **Nesahej na `com.xiaomi.micolauncher`** — je to launcher, displej by zůstal prázdný.

Kdo chce opatrněji, může aplikace místo odebrání jen vypnout a kdykoli zapnout:

```bash
adb shell pm disable-user --user 0 com.qiyi.video.speaker   # vypnout
adb shell pm enable com.qiyi.video.speaker                  # zapnout
adb shell pm list packages -d                               # seznam vypnutých
```
