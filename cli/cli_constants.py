class MenuOptions:
    DATA_GENERATION: str = "Generare date"
    GRAPHICS: str = "Reprezentare grafica"
    DATABASE_PREVIEW: str = "Previzualizare baza de date"
    CLASSIFIERS: str = "Clasificatori"
    EXIT: str = "Iesire"


class DataGenerationOptions:
    CSV_Generation = "Generare fisiere .csv"
    Database_Population = "Populare baza de date"


class GraphingOptions:
    Signal_Banding = "Reprezentare grafica semnal si benzi de frecventa"
    Naive_Bayes_Classifier_Histogram = "Histograma"


FEATURE_IDENTIFIERS = {
    "Approximate entropy": "ae",
    "Sample entropy": "se",
    "Power spectral density": "psd",
    "Root mean square": "rms",
    "Autocorrelation": "corr"
}


class BooleanOptions:
    Yes = "Da"
    No = "Nu"


class DatabasePreviewOptions:
    Users = "Users"
    Trials = "Trials"
    Recordings = "Recordings"


TABLE_FORMAT = "rounded_grid"
