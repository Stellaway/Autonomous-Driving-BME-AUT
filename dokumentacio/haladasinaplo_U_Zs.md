### 2024.02.19-25
- Elkészítettem a GitHub repo-t, hozzáadtam a kollégákat.
- Elkezdtem kísérletezni pár könyvtárral, pygame-et nézegettem.
- Dokumentációs mappát elkészítettem illetve összefoglaltam a tegnapi munkát.
- Kinematikus Bicikli Modellet kezdtem tanulmányozni. 
- Kezdetleges implementációja képes: mozogni.
- A Pygame-mel közelebb kerültem, nehezen, de megküzdöttem vele, átlátom működését.
- Elkezdem implementálni a kinematikus bicikli modellet.
- KBM implementálása összejött. Egyelőre az A*-gal nincs összekötve. Jól szuperál.

### 2024.02.26-2024.03.03
- Hozzáadtam a kerekeket a vizualizációhoz, így már látható ahogyan kanyarodik a kétkerekű kis járművünk.
- Az önvezetést imitálandó, implementálni kezdtem az egér követését. Ez majd a későbbiekben az útvonal követéséhez lesz használható, mivel kontroll inputok helyett a pályán akár egy mozgó pontot is tud követni.
- Az első verzió implementálása könnyedén ment, annak minden hibájával együtt.
- A legfontosabb bug az, hogyha balra néz az autó és az kurzor pozíciója, az irány radián -pi és +pi között mozog, akkor erre eternal heróttal válaszol.
- Sikerült kijavítani, a problémát egy radiánértékeket 0 és 2pi közé (-pi és pi helyett) normalizáló fv okozta, ebből is tanultam.
- Egy kezdetleges pályát rajzoltam paintben. A háttér kirajzolására a képkockánkénti screen.blit nagyon lomha és nemhatékony volt. Megoldásnak találtam, hogy a képre load után convert_alpha()-t hívok. Eképpen, továbbra is screen.blit-et használva jelentősen megnőtt a képkockaszám.

### 2024.03.04-2024.03.10
A bemutatón egy korábban észre nem vett hiba jött elő az egérrel való kormányzással kapcsolatban. A hibát kijavítottam, egy véletlen pí hozzáadás okozta.

### 2024.03.11-2024.03.24
Elkezdtem a két irányból jövő projekt (részemről a bicikli modell, Robi részéről az útkereső algoritmus) összeollózását.

### 2024.03.24-2024.04.07
A projekt összeállítását folytattam.
Közben a bicikli modell demót igyekszem továbbá pixelfüggetlenné tenni. Ehhez az első lépés a rect image elvetése, és saját generálása.

### 2024.04.15-2024.04.21
Lehetővé teszem, hogy az autónk a kijelölt útvonalon haladó demó járművet kövesse. Mivel a demó autó mindig újrakezdi, ez nem egy optimális megoldás.

### 2024.04.22-2024.04.28
Az autó mostmár magát az utat követi. Azonban csak a kezdő pozició -> cél pozíció irányba tud menni.

### 2024.04.29-2024.05.05
Az autó a kijelölt útvonalat követi, és a saját irányának megfelelő irányt követi.
Irodalomkutatás path planningről.

### 2024.05.06-2024.05.12
Hasznos forrásanyagokat találtam:
-https://www.gamedeveloper.com/programming/toward-more-realistic-pathfinding
-https://github.com/Habrador/Self-driving-vehicle