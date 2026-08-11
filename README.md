# EDINBRO — Belfast 2026

Négyfős utazás Edinburgh-be és Belfastba az **Észak-Írország – Magyarország**
mérkőzésre (2026. szeptember 28., Windsor Park).

Egyetlen HTML fájl, függőségek nélkül. Offline is működik — internet csak a
beágyazott térképekhez és a Nemzeti Sport hírekhez kell.

## Mit tartalmaz

| Fül | Tartalom |
|---|---|
| Áttekintés | összefoglaló, a hat utazás kártyái, becsült költség |
| Meccsek | a két válogatott meccs, jegyvásárlási tudnivalók, hírek |
| Program | napokra bontott idővonal, szűrhető (fix / teendő / opcionális) |
| Szállás | a két Airbnb összehasonlítva, beágyazott térképpel |
| Utazás | Airlink 100, Airport Express 300, séta- és vonatútvonalak |
| Költségek | tételes bontás, létszám szerint, közös kassza elszámolással |
| Teendők | határidős lista, haladásjelzővel |

## Szerkesztés

Minden adat a fájl tetején lévő `ADAT` objektumban van — napok, események,
árak, szállások, teendők. A megjelenítés ebből generálódik, szóval elég ott
átírni valamit.

## Futtatás

Nyisd meg az `index.html`-t bármelyik böngészőben. Nincs build, nincs telepítés.
