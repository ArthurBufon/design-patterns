-- Espelho da migration Laravel `2026_05_08_000000_create_carros_table.php`.
-- Ajuste tipos conforme seu SGBD (ex.: `BIGSERIAL` no Postgres no lugar de `BIGINT AUTO_INCREMENT`).

CREATE TABLE IF NOT EXISTS carros (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    marca VARCHAR(80) NOT NULL,
    modelo VARCHAR(120) NOT NULL,
    ano SMALLINT UNSIGNED NOT NULL,
    cor VARCHAR(40) NULL,
    placa VARCHAR(10) NOT NULL,
    km INT UNSIGNED NOT NULL DEFAULT 0,
    created_at TIMESTAMP NULL DEFAULT NULL,
    updated_at TIMESTAMP NULL DEFAULT NULL,
    UNIQUE KEY carros_placa_unique (placa)
);
