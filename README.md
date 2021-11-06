# Team 30er Zone
 
Unser Ziel war das Analysieren von Unfalldaten in Bezug auf die 30er Zonen in der Stadt St. Gallen. Insbesondere interessierte es uns, ob die Einführung von 30er Zonen die Anzahl Unfälle reduziert hat.

## Datensätze

Verwendet wurde der [Tempo 30 Zone](https://daten.stadt.sg.ch/explore/dataset/tempo-30-zonen/information/?location=16,47.42013,9.38173&basemap=jawg.streets) Datensatz der Stadt St. Gallen, sowie die gemeldeten [Verkehrsunfälle](https://data.geo.admin.ch/ch.astra.unfaelle-personenschaeden_alle/) des Bundes.

## Vorgehen

Als erstes mussten die Koordinaten der Unfallmeldungen vom [CH LV95](https://www.swisstopo.admin.ch/de/wissen-fakten/geodaesie-vermessung/bezugsrahmen/lokal/lv95.html) in Längen- und Breitengrade umgerechnet werden. So konnten sie einfach mit den gegebenen Polygonen der 30er Zonen verglichen werden. Die **shapely** Library bietet dafür gute Funktion.

```Python
from shapely.geometry import Point, Polygon
#...
point.within(polygon)
```

halt selbsterklärend.

