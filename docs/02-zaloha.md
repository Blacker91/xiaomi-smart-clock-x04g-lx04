# 2. Záloha

Tohle je jediný krok, který se nesmí přeskočit. BROM režim funguje nezávisle na obsahu paměti, takže dokud máš zálohu, jde budík vrátit z jakéhokoli stavu.

Každý příkaz spouštěj zvlášť: spusť → připoj budík v BROM režimu → počkej na 100 % → odpoj.

## Celá paměť (oblast USER)

```bash
python3 mtk.py rf zaloha_full.bin
```

Trvá to desítky minut. Výsledná velikost: **LX04 3,6 GB** (`0xE2000000`), **X04G 3,7 GB** (`0xEC000000`). Jiná velikost znamená neúplný soubor.

## boot1 — preloader

> [!IMPORTANT]
> `rf` čte **jen oblast USER**. Preloader leží v samostatné oblasti `EMMC_BOOT_1` a v dumpu výše **není**. Bez něj zálohu nikdy úplně neobnovíš.

```bash
python3 mtk.py r preloader boot1.bin --parttype boot1
```

Velikost 2,0 MB.

## Identita zařízení

Je obsažená i v celém dumpu, ale samostatné soubory se ti budou hodit při převodu a jsou rychle po ruce:

```bash
python3 mtk.py r proinfo proinfo.bin
python3 mtk.py r nvram nvram.bin
python3 mtk.py r protect1 protect1.bin
python3 mtk.py r protect2 protect2.bin
python3 mtk.py r persist persist.bin
```

| Soubor | Obsah | Velikost |
|---|---|---|
| `proinfo.bin` | sériové číslo | 3,0 MB |
| `nvram.bin` | MAC adresy, identifikátor `mi.did` | 5,0 MB |
| `protect1.bin`, `protect2.bin` | kalibrační data | 10 MB |
| `persist.bin` | kalibrační data | 48 MB |

## MAC adresy

Po převodu globálního kusu budeš potřebovat vrátit jeho vlastní MAC adresy ([04 – Změna MAC adresy](04-x04g-na-lx04.md#změna-mac-adresy)). Zjistíš je jen ze zálohy pořízené **před převodem** — proto ji před každou větší změnou dělej znovu. Ověř si rovnou, že je v ní najdeš:

```bash
python3 najdi_mac.py nvram.bin
```

## Kontrolní součty

```bash
md5sum *.bin > kontrolni_soucty.md5
```

Později ověříš, že se nic nepoškodilo: `md5sum -c kontrolni_soucty.md5`.

## Kam se zálohou

- Pojmenuj soubory podle budíku (`zaloha_LX04.bin`, `zaloha_X04G.bin`…), ať se ti při víc kusech nepletou.
- Drž ji **i mimo počítač** — NAS, externí disk.
- **Nikomu ji neposílej a nenahrávej veřejně.** Je v ní sériové číslo, MAC adresy a identifikátor, podle kterého tě pozná cloud Xiaomi.
