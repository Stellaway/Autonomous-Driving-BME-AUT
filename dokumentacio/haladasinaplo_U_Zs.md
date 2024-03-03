### 2024.02.19-25
Elkészítettem a GitHub repo-t, hozzáadtam a kollégákat.
Elkezdtem kísérletezni pár könyvtárral, pygame-et nézegettem.
Dokumentációs mappát elkészítettem illetve összefoglaltam a tegnapi munkát.
Kinematikus Bicikli Modellet kezdtem tanulmányozni. 
Kezdetleges implementációja képes: mozogni.
A Pygame-mel közelebb kerültem, nehezen, de megküzdöttem vele, átlátom működését.
Elkezdem implementálni a kinematikus bicikli modellet.
KBM implementálása összejött. Egyelőre az A*-gal nincs összekötve. Jól szuperál.

### 2024.02.26-2024.03.03
Hozzáadtam a látható kerekeket a vizualizációkhoz, így már látható ahogyan kanyarodik a kétkerekű kis járművünk.
Az önvezetést imitálandó, implementálni kezdtem az egér követését. Ez majd a későbbiekben az útvonal követéséhez lesz használható, mivel kontroll inputok helyett a pályán akár egy mozgó pontot is tud követni.
Az első verzió implementálása könnyedén ment, annak minden hibájával együtt.
A legfontosabb bug az, hogyha balra néz az autó és az kurzor pozíciója, az irány radián -pi és +pi között mozog, erre pedig eternal heróttal válaszol.
Sikerült kijavítani, a problémát egy radiánértékeket 0 és 2pi közé (-pi és pi helyett) normalizáló fv okozta, ebből is tanultam.
Egy kezdetleges pályát rajzoltam paintben. A háttér kirajzolására a képkockánkénti screen.blit nagyon lomha és nemhatékony volt. Megoldásnak találtam, hogy a képre load után convert_alpha()-t hívok. Eképpen, továbbra is screen.blit-et használva jelentősen megnőtt a képkockaszám.