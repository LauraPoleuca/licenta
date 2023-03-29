DATABASE_PATH = "database.db"

CREATE_USER_TABLE_SCRIPT = "CREATE TABLE users (\
    user_id TEXT PRIMARY KEY,\
    gender TEXT)"

CREATE_TRIAL_TABLE_SCRIPT = "CREATE TABLE trials (\
    user_id TEXT,\
    trial_id INT,\
    valence FLOAT,\
    arousal FLOAT,\
    PRIMARY KEY (user_id, trial_id),\
    FOREIGN KEY (user_id) REFERENCES users(user_id))"

CREATE_RECORDINGS_TABLE_SCRIPT = "CREATE TABLE recordings (\
    user_id TEXT,\
    trial_id INTEGER,\
    channel_id TEXT,\
    alpha_es TEXT,\
    alpha_as TEXT,\
    alpha_psd TEXT,\
    alpha_rms TEXT,\
    beta_es TEXT,\
    beta_as TEXT,\
    beta_psd TEXT,\
    beta_rms TEXT,\
    gamma_es TEXT,\
    gamma_as TEXT,\
    gamma_psd TEXT,\
    gamma_rms TEXT,\
    PRIMARY KEY (user_id, trial_id, channel_id),\
    FOREIGN KEY (user_id, trial_id) REFERENCES trials (user_id, trial_id))"

INSERT_RANGE_TABLE_USERS = "INSERT INTO users VALUES(?, ?)"

INSERT_RANGE_TABLE_TRIALS = "INSERT INTO trials VALUES(?, ?, ?, ?)"

INSERT_RANGE_TABLE_RECORDINGS = "INSERT INTO recordings VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
