DATABASE_PATH = "database.db"

FOREIGN_KEYS_ENABLED = "PRAGMA foreign_keys = 1"

CREATE_USER_TABLE_SCRIPT = "CREATE TABLE users (\
    user_id TEXT PRIMARY KEY,\
    gender TEXT)"

CREATE_TRIAL_TABLE_SCRIPT = "CREATE TABLE trials (\
    user_id TEXT,\
    trial_id INT,\
    valence FLOAT,\
    arousal FLOAT,\
    quadrant INTEGER,\
    PRIMARY KEY (user_id, trial_id),\
    FOREIGN KEY (user_id) REFERENCES users(user_id))"

CREATE_RECORDINGS_TABLE_SCRIPT = "CREATE TABLE recordings (\
    user_id TEXT,\
    trial_id INTEGER,\
    channel_id TEXT,\
    alpha_ae TEXT,\
    alpha_se TEXT,\
    alpha_psd TEXT,\
    alpha_rms TEXT,\
    alpha_corr TEXT,\
    beta_ae TEXT,\
    beta_se TEXT,\
    beta_psd TEXT,\
    beta_rms TEXT,\
    beta_corr TEXT,\
    gamma_ae TEXT,\
    gamma_se TEXT,\
    gamma_psd TEXT,\
    gamma_rms TEXT,\
    gamma_corr TEXT,\
    PRIMARY KEY (user_id, trial_id, channel_id),\
    FOREIGN KEY (user_id, trial_id) REFERENCES trials (user_id, trial_id))"

CREATE_NEW_RECORDINGS_TABLE_SCRIPT = "CREATE TABLE new_recordings (\
    user_id TEXT,\
    trial_id INTEGER,\
    channel_id TEXT,\
    bandth_type TEXT,\
    ae TEXT,\
    se TEXT,\
    psd TEXT,\
    rms TEXT,\
    corr TEXT,\
    PRIMARY KEY (user_id, trial_id, channel_id, bandth_type),\
    FOREIGN KEY (user_id, trial_id) REFERENCES trials (user_id, trial_id))"

INSERT_RANGE_TABLE_USERS = "INSERT INTO users VALUES(?, ?)"

INSERT_RANGE_TABLE_TRIALS = "INSERT INTO trials VALUES(?, ?, ?, ?, ?)"

INSERT_RANGE_TABLE_RECORDINGS = "INSERT INTO recordings VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

INSERT_NEW_RANGE_TABLE_RECORDINGS = "INSERT INTO new_recordings VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"

SELECT_USERS = "SELECT * FROM USERS"

SELECT_TRIALS = "SELECT * FROM TRIALS"

SELECT_RECORDINGS = "SELECT * FROM RECORDINGS"

SELECT_NEW_RECORDINGS = "SELECT * FROM NEW_RECORDINGS"
