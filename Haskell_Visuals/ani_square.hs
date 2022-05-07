
import Graphics.Gloss

main :: IO ()
main
    = animate
        (InWindow
               "A simple orange square"     -- Fenstertitel
                (300, 150)                  -- Fenstergröße
                (10, 10))                   -- Festerposition
        blue                            -- Hintergrundfarbe
        picture                         -- darzustellendes Bild

picture :: Float -> Picture
picture time
        = 
          pictures[translate ((-50)*sin(time)) ((-40)*cos(time)) $ color violet $ rectangleSolid 30 30    -- violettes Quadrat
                  , color orange $ translate (50*sin(time)) (40*cos(time)) $ circleSolid 30               -- oranger Kreis
                  , color black $ translate (50*sin(time)+10*cos(time*3)) (40*cos(time)+10*sin(time*3)) $ circleSolid 10            
                  , translate (-120) (60) $ scale 0.1 0.1 $ text (show time)]                              --Zeitanzeige


