# Xiaomi Mi Smart Clock — čínský systém LX04 a převod globální verze

Návod, jak na budíku **Xiaomi Mi Smart Clock** dostat čínský systém LX04 s upravenou ROM **SP6** — a hlavně jak na něj převést **globální verzi X04G**. Výsledkem je budík, do kterého jde přes ADB instalovat vlastní aplikace.

Postup je ověřený na skutečném hardwaru. Popsané je jen to, co opravdu proběhlo a fungovalo.

> [!CAUTION]
> Zasahuješ do paměti zařízení na nejnižší úrovni. Než cokoli zapíšeš, **udělej kompletní zálohu** ([02 – Záloha](docs/02-zaloha.md)) a ulož ji mimo počítač. Se zálohou se dá budík vrátit vždycky — bez ní ne. Celé na vlastní riziko.

## Dva budíky, stejný hardware

| | Čínský **LX04** (小爱触屏音箱) | Globální **X04G** (Mi Smart Clock) |
|---|---|---|
| Systém | Android 8.1, asistent Xiao AI | Android 10 Go, Google Assistant |
| Čip | MT8167 | MT8167 |
| eMMC | `M62704`, USER `0xE2000000` | `004GA0`, USER `0xEC000000` |
| Rozložení oddílů | klasické A/B | dynamické oddíly (`super`) + AVB |
| Instalace vlastních aplikací | po úpravě ROM ano | prakticky ne |

Oba mají stejný procesor a desku, liší se paměťovým čipem a systémem. Díky tomu jde na globální kus nahrát čínský systém.

## Postup

1. [Příprava](docs/01-priprava.md) — mtkclient na Linuxu, tlačítkové sekvence
2. [Záloha](docs/02-zaloha.md) — kompletní dump, boot1 a identita zařízení
3. [Čínský LX04 → SP6](docs/03-lx04-na-sp6.md) — aktualizace čínského budíku
4. [Globální X04G → LX04](docs/04-x04g-na-lx04.md) — převod globální verze, včetně rychlého převodu dalších kusů
5. [Po instalaci](docs/05-po-instalaci.md) — ADB, vypnutí čínských aplikací, vlastní aplikace
6. [Návrat ze zálohy](docs/06-navrat.md) — zpět na původní systém, včetně globálního
7. [Řešení problémů](docs/07-problemy.md) — chyby, slepé uličky a proč nefungují

Nástroje pro převedený budík:
- [`najdi_mac.py`](najdi_mac.py) — najde v záloze původní MAC adresy Wi-Fi a Bluetooth
- [`zmen_mac.py`](zmen_mac.py) — zapíše je do NVRAM souborů a přepočítá kontrolní součet

## Co tady nenajdeš

- **Převod čínského budíku na globální systém.** Tohle vyzkoušené nemáme — víc v [06 – Návrat ze zálohy](docs/06-navrat.md#čínský-budík-na-globální-systém).
- **Firmware SP6.** Autor upravené ROM zakazuje její další šíření v jakékoli podobě. Návod říká, kde ji najdeš, ale soubory tu nejsou.
- **SP Flash Tool, DA a auth soubory.** Patří do projektu [AyraHikari/xiaomi-x04g-lx04](https://github.com/AyraHikari/xiaomi-x04g-lx04), odkazujeme tam.
- **Zálohy a dumpy.** Obsahují sériové číslo, MAC adresy a identifikátor zařízení. Svoje nikdy nikomu neposílej a cizí nepoužívej — vznikla by dvě zařízení se stejnou identitou.

## Poděkování

- [bkerler/mtkclient](https://github.com/bkerler/mtkclient) — nástroj, přes který se dá do MediaTek zařízení dostat i se zamčeným bootloaderem
- [AyraHikari/xiaomi-x04g-lx04](https://github.com/AyraHikari/xiaomi-x04g-lx04) — původní výzkum převodu mezi X04G a LX04, DA pro SP Flash Tool
- autor upravené ROM 官改 SP6 pro LX04

## Související

[Free Radio](https://github.com/Blacker91/Radio-budik) — internetové rádio napsané pro tenhle budík. Běžné rádiové aplikace na něm padají.

## Licence

Text návodu: [CC BY 4.0](LICENSE) — můžeš ho šířit a upravovat, jen uveď zdroj. Firmware, nástroje a jejich licence patří jejich autorům.
