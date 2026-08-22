CREATE DATABASE IF NOT EXISTS libelli CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE libelli;

CREATE TABLE IF NOT EXISTS usuarios (
 id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(120) NOT NULL, email VARCHAR(150) NOT NULL UNIQUE,
 senha_hash VARCHAR(255) NOT NULL, criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS disciplinas (
 id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(120) NOT NULL, descricao TEXT, usuario_id INT NOT NULL,
 criado_em DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS conteudos (
 id INT AUTO_INCREMENT PRIMARY KEY, titulo VARCHAR(150), conteudo TEXT, disciplina_id INT NOT NULL,
 criado_em DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS comentarios (
 id INT AUTO_INCREMENT PRIMARY KEY, titulo VARCHAR(150), texto TEXT, disciplina_id INT NOT NULL, conteudo_id INT NULL,
 criado_em DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE,
 FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS quizzes (
 id INT AUTO_INCREMENT PRIMARY KEY, titulo VARCHAR(150), conteudo TEXT, perguntas TEXT, disciplina_id INT NOT NULL, conteudo_id INT NULL,
 criado_em DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE,
 FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS resumos (
 id INT AUTO_INCREMENT PRIMARY KEY, titulo VARCHAR(150), conteudo TEXT, gerado_por_ia BOOLEAN DEFAULT FALSE, disciplina_id INT NOT NULL, conteudo_id INT NULL,
 criado_em DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE,
 FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS revisoes (
 id INT AUTO_INCREMENT PRIMARY KEY, titulo VARCHAR(150), conteudo TEXT, data_revisao DATETIME NULL, status ENUM('pendente','concluida') DEFAULT 'pendente',
 disciplina_id INT NOT NULL, conteudo_id INT NULL, criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE, FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

DROP PROCEDURE IF EXISTS sp_buscar_usuario_por_email;
DELIMITER $$
CREATE PROCEDURE sp_buscar_usuario_por_email(IN p_email VARCHAR(150)) BEGIN SELECT * FROM usuarios WHERE email=p_email LIMIT 1; END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_listar_usuarios_com_disciplinas_count;
DELIMITER $$
CREATE PROCEDURE sp_listar_usuarios_com_disciplinas_count(IN p_usuario_id INT) BEGIN
 SELECT u.*,COUNT(d.id) disciplinas_count FROM usuarios u LEFT JOIN disciplinas d ON d.usuario_id=u.id
 WHERE p_usuario_id IS NULL OR u.id=p_usuario_id GROUP BY u.id; END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_listar_disciplinas_por_usuario;
DELIMITER $$
CREATE PROCEDURE sp_listar_disciplinas_por_usuario(IN p_usuario_id INT) BEGIN SELECT * FROM disciplinas WHERE usuario_id=p_usuario_id; END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_listar_disciplinas_com_materiais_count;
DELIMITER $$
CREATE PROCEDURE sp_listar_disciplinas_com_materiais_count(IN p_usuario_id INT) BEGIN
 SELECT d.*, (SELECT COUNT(*) FROM conteudos c WHERE c.disciplina_id=d.id)+(SELECT COUNT(*) FROM comentarios c WHERE c.disciplina_id=d.id)+(SELECT COUNT(*) FROM quizzes q WHERE q.disciplina_id=d.id)+(SELECT COUNT(*) FROM resumos r WHERE r.disciplina_id=d.id)+(SELECT COUNT(*) FROM revisoes v WHERE v.disciplina_id=d.id) materiais_count
 FROM disciplinas d WHERE p_usuario_id IS NULL OR d.usuario_id=p_usuario_id; END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_buscar_estudos;
DELIMITER $$
CREATE PROCEDURE sp_buscar_estudos(IN p_usuario_id INT, IN p_termo VARCHAR(150), IN p_disciplina_id INT, IN p_tipo VARCHAR(20), IN p_ordenar_por VARCHAR(20), IN p_direcao VARCHAR(4))
BEGIN
 SELECT * FROM (
  SELECT c.id,c.titulo,c.conteudo,NULL perguntas,NULL gerado_por_ia,NULL data_revisao,NULL status,c.disciplina_id,NULL conteudo_id,c.criado_em,'conteudo' tipo,d.nome disciplina_nome FROM conteudos c JOIN disciplinas d ON d.id=c.disciplina_id
  UNION ALL SELECT c.id,c.titulo,c.texto,NULL,NULL,NULL,NULL,c.disciplina_id,c.conteudo_id,c.criado_em,'comentario',d.nome FROM comentarios c JOIN disciplinas d ON d.id=c.disciplina_id
  UNION ALL SELECT q.id,q.titulo,q.conteudo,q.perguntas,NULL,NULL,NULL,q.disciplina_id,q.conteudo_id,q.criado_em,'quiz',d.nome FROM quizzes q JOIN disciplinas d ON d.id=q.disciplina_id
  UNION ALL SELECT r.id,r.titulo,r.conteudo,NULL,r.gerado_por_ia,NULL,NULL,r.disciplina_id,r.conteudo_id,r.criado_em,'resumo',d.nome FROM resumos r JOIN disciplinas d ON d.id=r.disciplina_id
  UNION ALL SELECT v.id,v.titulo,v.conteudo,NULL,NULL,v.data_revisao,v.status,v.disciplina_id,v.conteudo_id,v.criado_em,'revisao',d.nome FROM revisoes v JOIN disciplinas d ON d.id=v.disciplina_id
 ) estudos WHERE estudos.disciplina_id IN (SELECT id FROM disciplinas WHERE usuario_id=p_usuario_id)
 AND (p_termo IS NULL OR p_termo='' OR estudos.titulo LIKE CONCAT('%',p_termo,'%') OR estudos.conteudo LIKE CONCAT('%',p_termo,'%'))
 AND (p_disciplina_id IS NULL OR estudos.disciplina_id=p_disciplina_id) AND (p_tipo IS NULL OR estudos.tipo=p_tipo)
 ORDER BY CASE WHEN p_ordenar_por='titulo' AND p_direcao='ASC' THEN titulo END ASC, CASE WHEN p_ordenar_por='titulo' AND p_direcao='DESC' THEN titulo END DESC,
 CASE WHEN p_ordenar_por='tipo' AND p_direcao='ASC' THEN tipo END ASC, CASE WHEN p_ordenar_por='tipo' AND p_direcao='DESC' THEN tipo END DESC,
 CASE WHEN p_ordenar_por='disciplina' AND p_direcao='ASC' THEN disciplina_nome END ASC, CASE WHEN p_ordenar_por='disciplina' AND p_direcao='DESC' THEN disciplina_nome END DESC,
 CASE WHEN p_ordenar_por='criado_em' AND p_direcao='ASC' THEN criado_em END ASC, CASE WHEN p_ordenar_por='criado_em' AND p_direcao='DESC' THEN criado_em END DESC;
END$$
DELIMITER ;
