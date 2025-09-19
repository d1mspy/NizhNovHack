CREATE TYPE sex_enum AS ENUM ('male', 'female');

CREATE TABLE "user"(
    id UUID PRIMARY KEY,

    first_name TEXT NOT NULL CHECK (btrim(first_name) <> '' AND char_length(first_name) <= 50),
    last_name  TEXT NOT NULL CHECK (btrim(last_name)  <> '' AND char_length(last_name)  <= 50),

    sex sex_enum NOT NULL,
    birth_date DATE NOT NULL CHECK (birth_date <= CURRENT_DATE 
                                    AND birth_date > CURRENT_DATE - INTERVAL '120 years'),

    current_position TEXT NOT NULL CHECK (current_position ~ '[^[:space:]]'),

    education TEXT,

    experience_years SMALLINT NOT NULL DEFAULT 0 CHECK (experience_years >= 0 AND experience_years <= 80),
    experience_months SMALLINT NOT NULL DEFAULT 0 CHECK (experience_months BETWEEN 0 AND 11),

    experience_total_months INTEGER GENERATED ALWAYS AS (experience_years * 12 + experience_months) STORED,

    experience_description TEXT,

    hard_skills TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE vacancy(
    id UUID PRIMARY KEY,

    description TEXT NOT NULL,

    min_exp_months SMALLINT,
    max_exp_months SMALLINT,
    CHECK (
      min_exp_months IS NULL
      OR max_exp_months IS NULL
      OR min_exp_months <= max_exp_months
    ),

    must_have TEXT[] NOT NULL DEFAULT '{}',
    nice_to_have TEXT[] NOT NULL DEFAULT '{}',

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);