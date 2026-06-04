-- ============================================================
-- OS SCHEDULER SIMULATOR — Base de datos MySQL
-- Ejecutar en phpMyAdmin o consola MySQL de XAMPP
-- ============================================================

CREATE DATABASE IF NOT EXISTS os_scheduler_sim
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE os_scheduler_sim;

-- ------------------------------------------------------------
-- Tabla de Experimentos (cada experimento = 1 escenario
-- corrido con todos los algoritmos para comparar)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS experiments (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(150) NOT NULL DEFAULT 'Experimento sin nombre',
    scenario        VARCHAR(10)  NOT NULL COMMENT 'A=5proc, B=20proc, C=100proc, D=500proc',
    num_processes   INT          NOT NULL,
    quantum         INT          NOT NULL DEFAULT 2 COMMENT 'Quantum para Round Robin',
    created_at      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Tabla de Simulaciones (1 fila por algoritmo por experimento)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS simulations (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    experiment_id       INT          NOT NULL,
    algorithm           VARCHAR(25)  NOT NULL COMMENT 'FCFS|SJF|RR|PRIORITY|MLQ',
    avg_waiting_time    DECIMAL(12,4) DEFAULT 0,
    avg_turnaround      DECIMAL(12,4) DEFAULT 0,
    throughput          DECIMAL(12,6) DEFAULT 0,
    cpu_utilization     DECIMAL(6,2)  DEFAULT 0,
    FOREIGN KEY (experiment_id) REFERENCES experiments(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Tabla de Procesos individuales de cada simulación
-- (permite ver el detalle por proceso por algoritmo)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS simulation_processes (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    simulation_id   INT          NOT NULL,
    pid             VARCHAR(15)  NOT NULL,
    arrival_time    INT          NOT NULL,
    burst_time      INT          NOT NULL,
    priority        INT          NOT NULL DEFAULT 1,
    completion_time INT          DEFAULT 0,
    turnaround_time INT          DEFAULT 0,
    waiting_time    INT          DEFAULT 0,
    FOREIGN KEY (simulation_id) REFERENCES simulations(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Índices para mejorar rendimiento en consultas frecuentes
-- ------------------------------------------------------------
CREATE INDEX idx_simulations_experiment ON simulations(experiment_id);
CREATE INDEX idx_processes_simulation   ON simulation_processes(simulation_id);
CREATE INDEX idx_experiments_created    ON experiments(created_at);

-- ------------------------------------------------------------
-- Vista útil: resumen comparativo de un experimento
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW vw_experiment_comparison AS
SELECT
    e.id          AS experiment_id,
    e.name        AS experiment_name,
    e.scenario,
    e.num_processes,
    e.quantum,
    e.created_at,
    s.algorithm,
    s.avg_waiting_time,
    s.avg_turnaround,
    s.throughput,
    s.cpu_utilization
FROM experiments e
JOIN simulations s ON s.experiment_id = e.id
ORDER BY e.created_at DESC, s.algorithm;
