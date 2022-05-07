
import Graphics.Gloss

main :: IO ()
main
    = display
        (InWindow
               "A simple orange square"     -- Fenstertitel
                (300, 150)                  -- Fenstergröße
                (10, 10))                   -- Festerposition
        blue                            -- Hintergrundfarbe
        picture                         -- darzustellendes Bild

picture :: Picture
picture = 
          pictures[translate (-50) (0) $ color violet $ rectangleSolid 30 30    -- violettes Quadrat
                  , color orange $ translate (50) (0) $ circleSolid(30)]        -- oranger Kreis
                  