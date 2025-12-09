-- Tabela: Pessoas Físicas (clientes individuais)
CREATE TABLE IF NOT EXISTS pessoa_fisica(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    renda_mensal REAL NOT NULL CHECK(renda_mensal >= 0),
    idade INTEGER NOT NULL CHECK(idade >= 18),
    nome_completo TEXT NOT NULL,
    celular TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    categoria TEXT NOT NULL,
    saldo REAL NOT NULL DEFAULT 0.0 CHECK(saldo >= 0),
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance em pessoa_fisica
CREATE INDEX IF NOT EXISTS idx_pessoa_fisica_email ON pessoa_fisica(email);
CREATE INDEX IF NOT EXISTS idx_pessoa_fisica_celular ON pessoa_fisica(celular);

-- Trigger para atualizar automaticamente o campo atualizado_em em pessoa_fisica
CREATE TRIGGER IF NOT EXISTS atualizar_pessoa_fisica_timestamp
AFTER UPDATE ON pessoa_fisica
FOR EACH ROW
BEGIN
    UPDATE pessoa_fisica SET atualizado_em = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Tabela: Pessoas Jurídicas (empresas)
CREATE TABLE IF NOT EXISTS pessoa_juridica(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faturamento REAL NOT NULL CHECK(faturamento >= 0),
    idade INTEGER NOT NULL CHECK(idade >= 0),
    nome_fantasia TEXT NOT NULL,
    celular TEXT NOT NULL UNIQUE,
    email_corporativo TEXT NOT NULL UNIQUE,
    categoria TEXT NOT NULL,
    saldo REAL NOT NULL DEFAULT 0.0 CHECK(saldo >= 0),
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance em pessoa_juridica
CREATE INDEX IF NOT EXISTS idx_pessoa_juridica_email ON pessoa_juridica(email_corporativo);
CREATE INDEX IF NOT EXISTS idx_pessoa_juridica_celular ON pessoa_juridica(celular);

-- Trigger para atualizar automaticamente o campo atualizado_em em pessoa_juridica
CREATE TRIGGER IF NOT EXISTS atualizar_pessoa_juridica_timestamp
AFTER UPDATE ON pessoa_juridica
FOR EACH ROW
BEGIN
    UPDATE pessoa_juridica SET atualizado_em = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

INSERT INTO pessoa_fisica (renda_mensal, idade, nome_completo, celular, email, categoria, saldo) VALUES
(85000.00, 38, 'Harvey Specter', '555-1001', 'hervey.specter@personhardman.com', 'Socio Senior', 2500000.00),
(45000.00, 28, 'Mike Ross', '555-1002', 'mike.ross@personhardman.com', 'Associado', 1500000.00),
(75000.00, 42, 'Jessica Person', '555-1003', 'jessica.person@personhardman.com', 'Socia Gerente', 500000.00),
(55000.00, 35, 'Louis Litt', '555-1004', 'louis.litt@pearsonhardman.com', 'Sócio Júnior', 800000.00),
(35000.00, 32, 'Rachel Zane', '555-1005', 'rachel.zane@pearsonhardman.com', 'Paralegal', 120000.00),
(40000.00, 34, 'Donna Paulsen', '555-1006', 'donna.paulsen@pearsonhardman.com', 'Secretária Executiva', 200000.00);

INSERT INTO pessoa_juridica (faturamento, idade, nome_fantasia, celular, email_corporativo, categoria, saldo) VALUES
(50000000.00, 25, 'Pearson Hardman', '555-2001', 'contato@pearsonhardman.com', 'Escritório de Advocacia', 120000000.00),
(35000000.00, 18, 'Pearson Specter', '555-2002', 'contato@pearsonspecter.com', 'Escritório de Advocacia', 85000000.00),
(40000000.00, 20, 'Pearson Specter Litt', '555-2003', 'contato@psl.com', 'Escritório de Advocacia', 95000000.00),
(25000000.00, 15, 'Zane Specter Litt', '555-2004', 'contato@zsl.com', 'Escritório de Advocacia', 60000000.00),
(80000000.00, 30, 'Darby International', '555-2005', 'contato@darbyintl.com', 'Escritório Internacional', 200000000.00),
(15000000.00, 8, 'Rand Corporation', '555-2006', 'contato@randcorp.com', 'Cliente Corporativo', 500000000.00);
