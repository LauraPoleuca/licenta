class MenuOptions:
    DATA_GENERATION: str = "Data generation"
    GRAPHICS: str = "Graphics"
    DATABASE_PREVIEW: str = "Database preview"
    CLASSIFIERS: str = "Classifiers"
    EXIT: str = "Exit"


class DataGenerationOptions:
    CSV_Generation = "CSV Generation"
    Database_Population = "Database population"


class GraphingOptions:
    Signal_Banding = "Signal Banding"
    Naive_Bayes_Classifier_Histogram = "Naive Bayes Classifier Histogram"


FEATURE_IDENTIFIERS = {
    "Approximate entropy": "ae",
    "Sample entropy": "se",
    "Power spectral density": "psd",
    "Root mean square": "rms",
    "Autocorrelation": "corr"
}


class BooleanOptions:
    Yes = "Yes"
    No = "No"


class DatabasePreviewOptions:
    Users = "Users"
    Trials = "Trials"
    Recordings = "Recordings"


TABLE_FORMAT = "rounded_grid"