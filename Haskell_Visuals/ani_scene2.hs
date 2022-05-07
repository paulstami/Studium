
import Graphics.Gloss

main :: IO ()
main
    = animate
        (InWindow
               "A simple scenery"           -- Fenstertitel
                (1200, 600)                 -- Fenstergröße
                (10, 10))                   -- Festerposition
        blue                            -- Hintergrundfarbe
        picture                         -- darzustellendes Bild

picture :: Float -> Picture
picture time
        = scale 4 4$
          translate (-150) (-75)$
          Pictures[ sky time                                                                                    --Himmel
                  , translate (150) (0) $ sun time                                                              --Sonne
                  , translate (150) (0) $ moon time                                                             --Mond
                  , translate (250) (6) $ scale 0.22 0.22 $ tree 4 time (dim $ dim brown)                       --Baum
                  , translate (50*sin(time)+10*cos(time*3)) (40*cos(time)+10*sin(time*3)) $ frog                --Frosch
                  , translate 0 (-12) $ scale 1.5 1.5 $grass 15 time                                            --Gras
                  ]                              

-- Farben für die Gräser
yellowgreen :: Color
yellowgreen = makeColorI 76 112 13 255

darkgreen :: Color
darkgreen = makeColorI 13 112 40 255

darkergreen :: Color
darkergreen = makeColorI 0 77 9 255

-- mit dem Untergehen der Sonne, werden Gelb- und Blauwerte aus dem Mix genommen, sodass die Farbe dunkler wird
skycolor :: Float -> Color
skycolor time = makeColorI 15 (round(40*cos(time/2)+60)) (round(80*cos(time/2)+189)) 255

--der Himmel ist ein blaues Rechteck, dessen blauton durch skycolor bestimmt wird
sky :: Float -> Picture
sky time = translate (150) (75)$color (skycolor time) $ rectangleSolid 300 150

-- erzeugt ein Grasbündel aus 5 unterschiedlich rotierten Grasstücken, die sich mit Hilfe von time im Wind bewegen
grassbundle :: Color -> Float -> Picture
grassbundle gcolor time
          = let grassbit 
                       = rotate (4*sin (time)) $ color gcolor $ Polygon[(2,0), (1,15), (1,15), (-2,0)]
            in Pictures[rotate (-45) $ grassbit
                        , rotate (-23) $ grassbit
                        , grassbit
                        , rotate (28) $ grassbit
                        , rotate (45) $ grassbit]

-- eine Grasreihe besteht aus vielen Grasbündeln, die rekursiv erstellt werden
grassrow ::Int -> Float -> Color -> Float -> Picture
grassrow 0 offset gcolor time = grassbundle gcolor time
grassrow n offset gcolor time
        = Pictures [translate (fromIntegral n*offset) (0) $ grassbundle gcolor time
                   , grassrow (n-1) offset gcolor time]
                  
-- erstellt das Gras, indem es vier verschiedene Grasreihen versetzt übereinander legt
grass :: Int -> Float -> Picture
grass size time
     = Pictures [translate (-4.5) 6 $ grassrow size 15.0 yellowgreen (-time)
                  , translate 3 6 $ grassrow size 15.0 darkgreen time
                  , translate 6 3 $ grassrow size 15.0 darkergreen time
                  , translate 7.5 0 $ grassrow size 15.0 yellowgreen (-time)
                  , grassrow size 15.0 darkgreen time ]
                     
-- die Sonne besteht aus einem orangen Hauptkreis und 4 versetzen gelben Kreis dahinter, die als Schein dienen
sun :: Float -> Picture
sun time = Pictures[color yellow $ translate (2*sin(time*10)+200*sin(time/2)) (2*(cos(time*10))+100*cos(time/2)) $ circleSolid 31
                   ,color yellow $ translate (-2*sin(time*10)+200*sin(time/2)) (-2*(cos(time*10))+100*cos(time/2)) $ circleSolid 31
                   ,color yellow $ translate (2*sin(time*10+2)+200*sin(time/2)) (2*(cos(time*10+2))+100*cos(time/2)) $ circleSolid 31
                   ,color yellow $ translate (-2*sin(time*10+2)+200*sin(time/2)) (-2*(cos(time*10+2))+100*cos(time/2)) $ circleSolid 31
                   ,color (light orange) $ translate (200*sin(time/2)) (100*cos(time/2)) $ circleSolid 30 ]

-- ein hellgrauer Mondkreis, der stets der Sonne gegenüberliegt
moon :: Float -> Picture
moon time = translate ((-200)*sin(time/2)) ((-100)*cos(time/2)) $ color (greyN 0.9) $ circleSolid 20 

-- eine kleinteilige Zusammenstellung eines Frosches aus einem Polygon, Linien und Kreisen
frog :: Picture
frog = scale 5 5 $Pictures[translate (-1.5) (1.5)$color darkergreen $ circleSolid 0.5
                , translate (1.5) (1.5)$color darkergreen $ circleSolid 0.5
                , translate (-1.5) (1.5)$color red $ circleSolid 0.3
                , translate (1.5) (1.5)$color red $ circleSolid 0.3
                , translate (-1.5) (1.5) $ circleSolid 0.2
                , translate (1.5) (1.5) $ circleSolid 0.2
                , color darkergreen $ Polygon[(-1,0),(-2,-2),(-1,-2),(0.5,-0.5),(1,-2),(2,-2),(1,0),(2,1),(1,2),(-1,2),(-2,1)]
                , translate (-0.5) (1) $ circleSolid 0.2
                , translate (0.5) (1) $ circleSolid 0.2
                , line[(-1,0),(-2,-2),(-1,-2),(0,-1),(1,-2),(2,-2),(1,0),(2,1),(1,2),(-1,2),(-2,1)]
                , line[(-1,0),(-0.5,-0.5),(0.5,-0.5),(1,0)]
                , scale (0.5)(0.5)$ translate (0)(0.5) $ line[(-1,0),(-0.5,-0.5),(0.5,-0.5),(1,0)]]

-- | Tree Fractal.
--      Based on ANUPlot code by Clem Baker-Finch.

-- Stumpfform
stump :: Color -> Picture
stump color
        = Color color
        $ Polygon [(30,0), (15,300), (-15,300), (-30,0)]


-- Baum-Fraktal erzeugen
tree    :: Int          -- Fractal degree
        -> Float        -- time
        -> Color        -- Color for the stump
        -> Picture

tree 0 time color = stump color
tree n time color
 = let  smallTree
                = Rotate (2*sin time)
                $ Scale 0.5 0.5
                $ tree (n-1) (- time) (greener color)
   in   Pictures
                [ stump color
                , Translate 0 300 $ smallTree
                , Translate 0 240 $ Rotate 20    smallTree
                , Translate 0 180 $ Rotate (-20) smallTree
                , Translate 0 120 $ Rotate 40    smallTree
                , Translate 0  60 $ Rotate (-40) smallTree ]


-- Stumpffarbe
brown :: Color
brown =  makeColorI 139 100 35  255


-- mache das Grün noch grüner
greener :: Color -> Color
greener c = mixColors 1 10 green c
