
import Graphics.Gloss

main :: IO ()
main
    = display
        (InWindow
               "A simple orange square"     -- Fenstertitel
                (300, 150)                  -- Fenstergröße
                (10, 10))                   -- Festerposition
        blue                                -- Hintergrundfarbe
        picture                             -- darzustellendes Bild

picture :: Picture
picture
        = color orange $ Polygon[(-20,0), (20,0),(20,40), (-20,40)]   -- oranges Quadrat
                   
                   