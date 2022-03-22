# Mikolaj Wirkijowski 166837, uprzejmie proszę o nie używanie klucza API w celach innych niż ocena projektu.

from HeightDataHandler import HeightDataFromPath

samples = 128
delft_rotterdam = HeightDataFromPath("Delft", "Rotterdam",
                                     "Ścieżka płaska, Delft -> Rotterdam", samples, "delft_rotterdam")

uluru_aus = HeightDataFromPath("-25.331848185899144, 131.04585751017956", "-25.35930754883879, 131.0182200277016",
                               "Przekrój przez skałę Uluru, Australia", samples, "uluruAus")

sudety = HeightDataFromPath("Sudety Zachodnie", "Sudety Północne", "Droga przez Sudety", samples, "sudetyzachpol")

grand_canyon = HeightDataFromPath("36.12826545341861, -113.49146452042679", "35.86716966056297, -113.03965176339605",
                                  "Droga przez Grand Canyon, USA", samples, "gcanyonusa")

row_marianski = HeightDataFromPath("Guam", "Dinaey", "Droga  Guam -> Dinaey  w pobliżu rowu Mariańskiego", samples,
                                   "row_marianski")

delft_rotterdam.draw_elevation()
uluru_aus.draw_elevation()
sudety.draw_elevation()
grand_canyon.draw_elevation()
row_marianski.draw_elevation()
